import imp
import sys
import bdb
import re
import os
import json
import types
import traceback
import urllib.request
import urllib.parse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Logger(object):
    def __init__(self, obj, stream=sys.stdout):
        self.terminal = stream
        self.log = obj

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


is_python3 = (sys.version_info[0] == 3)
if is_python3:
    import io as StringIO
else:
    import StringIO
from . import python_ui_encoder

BREAKPOINT_STR = '#break'
PYTUTOR_HIDE_STR = '#pythontutor_hide:'
PYTUTOR_INLINE_TYPE_STR = '#pythontutor_hide_type:'
CLASS_RE = re.compile('class\s+')


def globToRegex(pat):
    """Translate a shell PATTERN to a regular expression.
    There is no way to quote meta-characters.
    """
    i, n = 0, len(pat)
    res = ''
    while i < n:
        c = pat[i]
        i = i + 1
        if c == '*':
            res = res + '.*'
        elif c == '?':
            res = res + '.'
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j + 1
            if j < n and pat[j] == ']':
                j = j + 1
            while j < n and pat[j] != ']':
                j = j + 1
            if j >= n:
                res = res + '\\['
            else:
                stuff = pat[i:j].replace('\\', '\\\\')
                i = j + 1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = '%s[%s]' % (res, stuff)
        else:
            res = res + re.escape(c)
    return res + '\Z(?ms)'


def compileGlobMatch(pattern):
    # very important to use match and *not* search!
    return re.compile(globToRegex(pattern)).match


try:
    import resource

    resource_module_loaded = True
except ImportError:
    # Google App Engine doesn't seem to have the 'resource' module
    resource_module_loaded = False


class NullDevice():
    def write(self, s):
        pass


if type(__builtins__) is dict:
    BUILTIN_IMPORT = __builtins__['__import__']
else:
    assert type(__builtins__) is types.ModuleType
    BUILTIN_IMPORT = __builtins__.__import__

import random

random.seed(0)

IGNORE_VARS = set(('__builtins__', '__name__', '__exception__', '__doc__', '__package__'))


def get_user_globals(frame, at_global_scope=False):
    d = filter_var_dict(frame.f_globals)
    if not is_python3 and hasattr(frame, 'f_valuestack'):
        for (i, e) in enumerate([e for e in frame.f_valuestack if type(e) is list]):
            d['_tmp' + str(i + 1)] = e
    if '__return__' in d: del d['__return__']
    return d


def get_user_locals(frame):
    ret = filter_var_dict(frame.f_locals)
    f_name = frame.f_code.co_name
    if hasattr(frame, 'f_valuestack'):
        if not is_python3:
            for (i, e) in enumerate([e for e in frame.f_valuestack if type(e) is list]):
                ret['_tmp' + str(i + 1)] = e
        if f_name.endswith('comp>'):
            for (i, e) in enumerate([e for e in frame.f_valuestack if type(e) in (list, set, dict)]):
                ret['_tmp' + str(i + 1)] = e
    return ret


def filter_var_dict(d):
    ret = {}
    for (k, v) in d.items():
        if k not in IGNORE_VARS:
            ret[k] = v
    return ret


def visit_all_locally_reachable_function_objs(frame):
    for (k, v) in get_user_locals(frame).items():
        for e in visit_function_obj(v, set()):
            if e:  # only non-null if it's a function object
                assert type(e) in (types.FunctionType, types.MethodType)
                yield e


def visit_function_obj(v, ids_seen_set):
    v_id = id(v)
    if v_id in ids_seen_set:
        yield None
    else:
        ids_seen_set.add(v_id)
        typ = type(v)
        if typ in (types.FunctionType, types.MethodType):
            yield v
        elif typ in (list, tuple, set):
            for child in v:
                for child_res in visit_function_obj(child, ids_seen_set):
                    yield child_res
        elif typ == dict or python_ui_encoder.is_class(v) or python_ui_encoder.is_instance(v):
            contents_dict = None
            if typ == dict:
                contents_dict = v
            elif hasattr(v, '__dict__'):
                contents_dict = v.__dict__
            if contents_dict:
                for (key_child, val_child) in contents_dict.items():
                    for key_child_res in visit_function_obj(key_child, ids_seen_set):
                        yield key_child_res
                    for val_child_res in visit_function_obj(val_child, ids_seen_set):
                        yield val_child_res
        yield None


class PGLogger(bdb.Bdb):
    def __init__(self):
        bdb.Bdb.__init__(self)
        self.mainpyfile = ''
        self._wait_for_mainpyfile = 0

        self.probe_exprs = None

        self.separate_stdout_by_module = False
        self.stdout_by_module = {}  # Key: module name, Value: StringIO faux-stdout

        self.modules_to_trace = set(['__main__'])  # always trace __main__!

        # Key: module name
        # Value: module's python code as a string
        self.custom_modules = None
        if self.custom_modules:
            for module_name in self.custom_modules:
                self.modules_to_trace.add(module_name)

        self.disable_security_checks = False
        # if we allow all modules, we shouldn't do security checks
        # either since otherwise users can't really import anything
        # because that will likely involve opening files on disk, which
        # is disallowed by security checks
        self.disable_security_checks = True

        # if True, then displays ALL stack frames that have ever existed
        # rather than only those currently on the stack (and their
        # lexical parents)
        self.cumulative_mode = False

        # if True, then render certain primitive objects as heap objects
        self.render_heap_primitives = False

        # if True, then don't render any data structures in the trace,
        # and show only outputs
        self.show_only_outputs = False

        # Run using the custom Py2crazy Python interpreter
        self.crazy_mode = False

        # each entry contains a dict with the information for a single
        # executed line
        self.trace = []

        # if this is true, don't put any more stuff into self.trace
        self.done = False

        # if this is non-null, don't do any more tracing until a
        # 'return' instruction with a stack gotten from
        # get_stack_code_IDs() that matches wait_for_return_stack
        self.wait_for_return_stack = None

        # http://stackoverflow.com/questions/2112396/in-python-in-google-app-engine-how-do-you-capture-output-produced-by-the-print
        self.GAE_STDOUT = sys.stdout

        # Key:   function object
        # Value: parent frame
        self.closures = {}

        # Key:   code object for a lambda
        # Value: parent frame
        self.lambda_closures = {}

        # set of function objects that were defined in the global scope
        self.globally_defined_funcs = set()

        # Key: frame object
        # Value: monotonically increasing small ID, based on call order
        self.frame_ordered_ids = {}
        self.cur_frame_id = 1

        # List of frames to KEEP AROUND after the function exits.
        # If cumulative_mode is True, then keep ALL frames in
        # zombie_frames; otherwise keep only frames where
        # nested functions were defined within them.
        self.zombie_frames = []

        # set of elements within zombie_frames that are also
        # LEXICAL PARENTS of other frames
        self.parent_frames_set = set()

        # all globals that ever appeared in the program, in the order in
        # which they appeared. note that this might be a superset of all
        # the globals that exist at any particular execution point,
        # since globals might have been deleted (using, say, 'del')
        self.all_globals_in_order = []

        # very important for this single object to persist throughout
        # execution, or else canonical small IDs won't be consistent.
        self.encoder = python_ui_encoder.ObjectEncoder(self)

        self.executed_script = None  # Python script to be executed!

        # if there is at least one line that ends with BREAKPOINT_STR,
        # then activate "breakpoint mode", where execution should stop
        # ONLY at breakpoint lines.
        self.breakpoints = []

        self.vars_to_hide = set()  # a set of regex match objects
        # created by compileGlobMatch() from
        # the contents of PYTUTOR_HIDE_STR
        self.types_to_inline = set()  # a set of regex match objects derived from PYTUTOR_INLINE_TYPE_STR

        self.prev_lineno = -1

    def should_hide_var(self, var):
        for re_match in self.vars_to_hide:
            if re_match(var):
                return True
        return False

    def get_user_stdout(self):
        def encode_stringio(sio):
            if not is_python3:
                sio.buflist = [(e.decode('utf-8', 'replace') if type(e) is str else e) for e in sio.buflist]
            return sio.getvalue()

        if self.separate_stdout_by_module:
            ret = {}
            for module_name in self.stdout_by_module:
                ret[module_name] = encode_stringio(self.stdout_by_module[module_name])
            return ret
        else:
            return encode_stringio(self.user_stdout)

    def get_frame_id(self, cur_frame):
        return self.frame_ordered_ids[cur_frame]

    def get_parent_of_function(self, val):
        if val in self.closures:
            return self.get_frame_id(self.closures[val])
        elif val in self.lambda_closures:
            return self.get_frame_id(self.lambda_closures[val])
        else:
            return None

    def get_parent_frame(self, frame):
        for (func_obj, parent_frame) in self.closures.items():
            if func_obj.__code__ == frame.f_code:
                all_matched = True
                for k in frame.f_locals:
                    # Do not try to match local names
                    if k in frame.f_code.co_varnames:
                        continue
                    if k != '__return__' and k in parent_frame.f_locals:
                        if parent_frame.f_locals[k] != frame.f_locals[k]:
                            all_matched = False
                            break
                if all_matched: return parent_frame
        for (lambda_code_obj, parent_frame) in self.lambda_closures.items():
            if lambda_code_obj == frame.f_code: return parent_frame
        return None

    def lookup_zombie_frame_by_id(self, frame_id):
        for e in self.zombie_frames:
            if self.get_frame_id(e) == frame_id:
                return e
        assert False  # should never get here

    def forget(self):
        self.lineno = None
        self.stack = []
        self.curindex = 0
        self.curframe = None

    def setup(self, f, t):
        self.forget()
        self.stack, self.curindex = self.get_stack(f, t)
        self.curframe = self.stack[self.curindex][0]

    def get_stack_code_IDs(self):
        return [id(e[0].f_code) for e in self.stack]

    def user_call(self, frame, argument_list):
        if self.done: return
        if self._wait_for_mainpyfile: return
        if self.stop_here(frame):
            try:
                del frame.f_locals['__return__']
            except KeyError:
                pass
            self.interaction(frame, None, 'call')

    def user_line(self, frame):
        if self.done: return
        if self._wait_for_mainpyfile:
            if ((frame.f_globals['__name__'] not in self.modules_to_trace) or frame.f_lineno <= 0): return
            self._wait_for_mainpyfile = 0
        self.interaction(frame, None, 'step_line')

    def user_return(self, frame, return_value):
        if self.done: return
        frame.f_locals['__return__'] = return_value
        self.interaction(frame, None, 'return')

    def user_exception(self, frame, exc_info):
        if self.done: return
        exc_type, exc_value, exc_traceback = exc_info
        frame.f_locals['__exception__'] = exc_type, exc_value
        self.interaction(frame, exc_traceback, 'exception')

    def get_script_line(self, n):
        return self.executed_script_lines[n - 1]

    def interaction(self, frame, traceback, event_type):
        self.setup(frame, traceback)
        tos = self.stack[self.curindex]
        top_frame = tos[0]
        lineno = tos[1]
        topframe_module = top_frame.f_globals['__name__']
        if topframe_module not in self.modules_to_trace: return
        if top_frame.f_code.co_name == '__new__': return
        if top_frame.f_code.co_name == '__repr__': return
        if self.wait_for_return_stack:
            if event_type == 'return' and \
                    (self.wait_for_return_stack == self.get_stack_code_IDs()):
                self.wait_for_return_stack = None  # reset!
            return  # always bail!
        else:
            if event_type == 'call':
                first_lineno = top_frame.f_code.co_firstlineno
                if topframe_module == "__main__":
                    func_line = self.get_script_line(first_lineno)
                elif topframe_module in self.custom_modules:
                    module_code = self.custom_modules[topframe_module]
                    module_code_lines = module_code.splitlines()  # TODO: maybe pre-split lines?
                    func_line = module_code_lines[first_lineno - 1]
                else:
                    func_line = ''
                if CLASS_RE.match(func_line.lstrip()):  # ignore leading spaces
                    self.wait_for_return_stack = self.get_stack_code_IDs()
                    return

        self.encoder.reset_heap()  # VERY VERY VERY IMPORTANT,
        if event_type == 'call':
            self.frame_ordered_ids[top_frame] = self.cur_frame_id
            self.cur_frame_id += 1
            if self.cumulative_mode:
                self.zombie_frames.append(top_frame)

        if self.separate_stdout_by_module:
            if event_type == 'call':
                if topframe_module in self.stdout_by_module:
                    sys.stdout = self.stdout_by_module[topframe_module]
                else:
                    sys.stdout = self.stdout_by_module["<other>"]
            elif event_type == 'return' and self.curindex > 0:
                prev_tos = self.stack[self.curindex - 1]
                prev_topframe = prev_tos[0]
                prev_topframe_module = prev_topframe.f_globals['__name__']
                if prev_topframe_module in self.stdout_by_module:
                    sys.stdout = self.stdout_by_module[prev_topframe_module]
                else:
                    sys.stdout = self.stdout_by_module["<other>"]
        cur_stack_frames = [e[0] for e in self.stack[:self.curindex + 1]]
        zombie_frames_to_render = [e for e in self.zombie_frames if e not in cur_stack_frames]
        encoded_stack_locals = []

        def create_encoded_stack_entry(cur_frame):
            parent_frame_id_list = []
            f = cur_frame
            while True:
                p = self.get_parent_frame(f)
                if p:
                    pid = self.get_frame_id(p)
                    assert pid
                    parent_frame_id_list.append(pid)
                    f = p
                else:
                    break
            cur_name = cur_frame.f_code.co_name
            if cur_name == '':
                cur_name = 'unnamed function'
            if cur_name == '<lambda>':
                cur_name += python_ui_encoder.create_lambda_line_number(cur_frame.f_code,
                                                                        self.encoder.line_to_lambda_code)
            encoded_locals = {}
            for (k, v) in get_user_locals(cur_frame).items():
                is_in_parent_frame = False
                for pid in parent_frame_id_list:
                    parent_frame = self.lookup_zombie_frame_by_id(pid)
                    if k in parent_frame.f_locals:
                        if k != '__return__':
                            if parent_frame.f_locals[k] == v:
                                is_in_parent_frame = True
                if is_in_parent_frame and k not in cur_frame.f_code.co_varnames:
                    continue
                if k == '__module__':
                    continue
                if self.should_hide_var(k):
                    continue
                encoded_val = self.encoder.encode(v, self.get_parent_of_function)
                encoded_locals[k] = encoded_val
            ordered_varnames = []
            for e in cur_frame.f_code.co_varnames:
                if e in encoded_locals:
                    ordered_varnames.append(e)
            for e in sorted(encoded_locals.keys()):
                if e != '__return__' and e not in ordered_varnames:
                    ordered_varnames.append(e)
            if '__return__' in encoded_locals:
                ordered_varnames.append('__return__')
            if '__locals__' in encoded_locals:
                ordered_varnames.remove('__locals__')
                local = encoded_locals.pop('__locals__')
                if encoded_locals.get('__return__', True) is None:
                    encoded_locals['__return__'] = local
            assert len(ordered_varnames) == len(encoded_locals)
            for e in ordered_varnames:
                assert e in encoded_locals
            return dict(func_name=cur_name,
                        is_parent=(cur_frame in self.parent_frames_set),
                        frame_id=self.get_frame_id(cur_frame),
                        parent_frame_id_list=parent_frame_id_list,
                        encoded_locals=encoded_locals,
                        ordered_varnames=ordered_varnames)

        i = self.curindex
        if i > 1:  # i == 1 implies that there's only a global scope visible
            for v in visit_all_locally_reachable_function_objs(top_frame):
                if (v not in self.closures and \
                        v not in self.globally_defined_funcs):
                    chosen_parent_frame = None
                    for (my_frame, my_lineno) in reversed(self.stack):
                        if chosen_parent_frame:
                            break
                        for frame_const in my_frame.f_code.co_consts:
                            if frame_const is (v.__code__ if is_python3 else v.func_code):
                                chosen_parent_frame = my_frame
                                break
                    if chosen_parent_frame in self.frame_ordered_ids:
                        self.closures[v] = chosen_parent_frame
                        self.parent_frames_set.add(chosen_parent_frame)
                        if not chosen_parent_frame in self.zombie_frames:
                            self.zombie_frames.append(chosen_parent_frame)
            else:
                if top_frame.f_code.co_consts:
                    for e in top_frame.f_code.co_consts:
                        if type(e) == types.CodeType and e.co_name == '<lambda>':
                            self.lambda_closures[e] = top_frame
                            self.parent_frames_set.add(top_frame)  # copy-paste from above
                            if not top_frame in self.zombie_frames:
                                self.zombie_frames.append(top_frame)
        else:
            for (k, v) in get_user_globals(top_frame).items():
                if (type(v) in (types.FunctionType, types.MethodType) and v not in self.closures):
                    self.globally_defined_funcs.add(v)
        top_frame = None
        while True:
            cur_frame = self.stack[i][0]
            cur_name = cur_frame.f_code.co_name
            if cur_name == '<module>':
                break
            if cur_frame in self.frame_ordered_ids:
                encoded_stack_locals.append(create_encoded_stack_entry(cur_frame))
                if not top_frame:
                    top_frame = cur_frame
            i -= 1
        zombie_encoded_stack_locals = [create_encoded_stack_entry(e) for e in zombie_frames_to_render]
        encoded_globals = {}
        cur_globals_dict = get_user_globals(tos[0], at_global_scope=(self.curindex <= 1))
        for (k, v) in cur_globals_dict.items():
            if self.should_hide_var(k):
                continue
            encoded_val = self.encoder.encode(v, self.get_parent_of_function)
            encoded_globals[k] = encoded_val
            if k not in self.all_globals_in_order:
                self.all_globals_in_order.append(k)
        ordered_globals = [e for e in self.all_globals_in_order if e in encoded_globals]
        assert len(ordered_globals) == len(encoded_globals)
        stack_to_render = []
        if encoded_stack_locals:
            for e in encoded_stack_locals:
                e['is_zombie'] = False
                e['is_highlighted'] = False
                stack_to_render.append(e)
            stack_to_render[0]['is_highlighted'] = True
        for e in zombie_encoded_stack_locals:
            e['is_zombie'] = True
            e['is_highlighted'] = False  # never highlight zombie entries
            stack_to_render.append(e)
        stack_to_render.sort(key=lambda e: e['frame_id'])
        for e in stack_to_render:
            hash_str = e['func_name']
            hash_str += '_f' + str(e['frame_id'])
            if e['is_parent']:
                hash_str += '_p'
            if e['is_zombie']:
                hash_str += '_z'
            e['unique_hash'] = hash_str
        encoded_probe_vals = {}
        if self.probe_exprs:
            if top_frame:  # are we in a function call?
                top_frame_locals = get_user_locals(top_frame)
            else:
                top_frame_locals = {}
            for e in self.probe_exprs:
                try:
                    probe_val = eval(e, cur_globals_dict, top_frame_locals)
                    encoded_probe_vals[e] = self.encoder.encode(probe_val, self.get_parent_of_function)
                except:
                    pass
        if self.show_only_outputs:
            trace_entry = dict(line=lineno,
                               event=event_type,
                               func_name=tos[0].f_code.co_name,
                               globals={},
                               ordered_globals=[],
                               stack_to_render=[],
                               heap={},
                               stdout=self.get_user_stdout())
        else:
            trace_entry = dict(line=lineno,
                               event=event_type,
                               func_name=tos[0].f_code.co_name,
                               globals=encoded_globals,
                               ordered_globals=ordered_globals,
                               stack_to_render=stack_to_render,
                               heap=self.encoder.get_heap(),
                               stdout=self.get_user_stdout())
            if encoded_probe_vals:
                trace_entry['probe_exprs'] = encoded_probe_vals
        if self.crazy_mode:
            trace_entry['column'] = frame.f_colno
            if frame.f_lasti >= 0:
                key = (frame.f_code.co_code, frame.f_lineno, frame.f_colno, frame.f_lasti)
                if key in self.bytecode_map:
                    v = self.bytecode_map[key]
                    trace_entry['expr_start_col'] = v.start_col
                    trace_entry['expr_width'] = v.extent
                    trace_entry['opcode'] = v.opcode
        if topframe_module != "__main__":
            trace_entry['custom_module_name'] = topframe_module
        if event_type == 'exception':
            exc = frame.f_locals['__exception__']
            trace_entry['exception_msg'] = exc[0].__name__ + ': ' + str(exc[1])
        append_to_trace = True
        if self.breakpoints:
            if not ((lineno in self.breakpoints) or (self.prev_lineno in self.breakpoints)):
                append_to_trace = False
            if event_type == 'exception':
                append_to_trace = True
        self.prev_lineno = lineno
        if append_to_trace:
            self.trace.append(trace_entry)
        self.forget()

    def _runscript(self, script_str):
        self.executed_script = script_str
        self.executed_script_lines = self.executed_script.splitlines()

        for (i, line) in enumerate(self.executed_script_lines):
            line_no = i + 1
            if line.endswith(BREAKPOINT_STR) and not line.strip().startswith(BREAKPOINT_STR):
                self.breakpoints.append(line_no)
            if line.startswith(PYTUTOR_HIDE_STR):
                hide_vars = line[len(PYTUTOR_HIDE_STR):]
                hide_vars = [compileGlobMatch(e.strip()) for e in hide_vars.split(',')]
                self.vars_to_hide.update(hide_vars)
            if line.startswith(PYTUTOR_INLINE_TYPE_STR):
                listed_types = line[len(PYTUTOR_INLINE_TYPE_STR):]
                listed_types = [compileGlobMatch(e.strip()) for e in listed_types.split(',')]
                self.types_to_inline.update(listed_types)
        if self.crazy_mode:
            import super_dis
            try:
                self.bytecode_map = super_dis.get_bytecode_map(self.executed_script)
            except:
                self.bytecode_map = {}
        self._wait_for_mainpyfile = 1
        user_builtins = {}
        if type(__builtins__) is dict:
            builtin_items = __builtins__.items()
        else:
            assert type(__builtins__) is types.ModuleType
            builtin_items = []
            for k in dir(__builtins__):
                builtin_items.append((k, getattr(__builtins__, k)))
        for (k, v) in builtin_items:
            user_builtins[k] = v

        if self.separate_stdout_by_module:
            self.stdout_by_module["__main__"] = StringIO.StringIO()
            if self.custom_modules:
                for module_name in self.custom_modules:
                    self.stdout_by_module[module_name] = StringIO.StringIO()
            self.stdout_by_module["<other>"] = StringIO.StringIO()  # catch-all for all other modules we're NOT tracing
            sys.stdout = self.stdout_by_module["<other>"]  # start with <other>
        else:
            self.user_stdout = StringIO.StringIO()
            sys.stdout = Logger(self.user_stdout, sys.stdout)
        self.ORIGINAL_STDERR = sys.stderr
        user_globals = {}
        if self.custom_modules:
            for mn in self.custom_modules:
                new_m = imp.new_module(mn)
                exec(self.custom_modules[mn], new_m.__dict__)  # exec in custom globals
                user_globals.update(new_m.__dict__)
        user_globals.update({"__name__": "__main__", "__builtins__": user_builtins})
        try:
            import ast
            try:
                all_modules_to_preimport = []
                tree = ast.parse(script_str)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for n in node.names:
                            all_modules_to_preimport.append(n.name)
                    elif isinstance(node, ast.ImportFrom):
                        all_modules_to_preimport(node.module)
                for m in all_modules_to_preimport:
                    if m in script_str:  # optimization: load only modules that appear in script_str
                        try:
                            __import__(m)
                        except ImportError:
                            pass
            except:
                pass
            self.run(script_str, user_globals, user_globals)
        except SystemExit:
            raise SystemExit(traceback.format_exc())
        except Exception as e:
            trace_entry = dict(event='uncaught_exception')
            (exc_type, exc_val, exc_tb) = sys.exc_info()
            if hasattr(exc_val, 'lineno'):
                trace_entry['line'] = exc_val.lineno
            if hasattr(exc_val, 'offset'):
                trace_entry['offset'] = exc_val.offset
            trace_entry['exception_msg'] = type(exc_val).__name__ + ": " + str(exc_val)
            already_caught = False
            for e in self.trace:
                if e['event'] == 'exception':
                    already_caught = True
                    break
            if not already_caught:
                if not self.done:
                    self.trace.append(trace_entry)
            result = str(traceback.format_exc())
            raise Exception(result)

    def force_terminate(self):
        raise bdb.BdbQuit  # need to forceably STOP execution

    def finalize(self):
        sys.stdout = self.GAE_STDOUT  # very important!
        sys.stderr = self.ORIGINAL_STDERR
        res = self.trace
        if len(res) >= 2 and \
                res[-2]['event'] == 'exception' and \
                res[-1]['event'] == 'return' and res[-1]['func_name'] == '<module>':
            res.pop()
        self.trace = res

        # 数据上报
        try:
            url = 'https://api.anycodes.cn/v1/stack/ui'
            post_data = {
                "container_id": os.environ.get("CONNECTID"),
                "stack_ui": json.dumps(self.trace)
            }
            urllib.request.urlopen(
                urllib.request.Request(
                    url=url,
                    data=urllib.parse.urlencode(post_data).encode("utf-8"),
                    headers={
                        "User-Agent": "Chrome"
                    }
                )
            )
        except:
            pass
