FLOAT_PRECISION = 4

from collections import defaultdict
import re, types
import sys
import math

typeRE = re.compile("<type '(.*)'>")
classRE = re.compile("<class '(.*)'>")

import inspect

is_python3 = (sys.version_info[0] == 3)
if is_python3:
    long = int
    unicode = str

is_class = lambda dat: isinstance(dat, type) if is_python3 else type(dat) in (types.ClassType, types.TypeType)
get_name = lambda obj: obj.__name__ if hasattr(obj, '__name__') else get_name(type(obj))


def is_instance(dat):
    if is_python3:
        return type(dat) not in PRIMITIVE_TYPES and \
               isinstance(type(dat), type) and \
               not isinstance(dat, type)
    else:
        return type(dat) == types.InstanceType or classRE.match(str(type(dat)))


PRIMITIVE_TYPES = (int, long, float, str, unicode, bool, type(None))


def encode_primitive(dat):
    t = type(dat)
    if t is float:
        if math.isinf(dat):
            if dat > 0:
                return ['SPECIAL_FLOAT', 'Infinity']
            else:
                return ['SPECIAL_FLOAT', '-Infinity']
        elif math.isnan(dat):
            return ['SPECIAL_FLOAT', 'NaN']
        else:
            if dat == int(dat):
                return ['SPECIAL_FLOAT', '%.1f' % dat]
            else:
                return round(dat, FLOAT_PRECISION)
    elif t is str and (not is_python3):
        return dat.decode('utf-8', 'replace')
    else:
        return dat


def create_lambda_line_number(codeobj, line_to_lambda_code):
    try:
        lambda_lineno = codeobj.co_firstlineno
        lineno_str = str(lambda_lineno)
        return ' <line ' + lineno_str + '>'
    except:
        return ''


class ObjectEncoder:
    def __init__(self, parent):
        self.parent = parent  # should be a PGLogger object
        self.encoded_heap_objects = {}
        self.render_heap_primitives = parent.render_heap_primitives
        self.id_to_small_IDs = {}
        self.cur_small_ID = 1
        self.line_to_lambda_code = defaultdict(list)

    def should_hide_var(self, var):
        return self.parent.should_hide_var(var)

    def should_inline_object_by_type(self, obj):
        if not self.parent.types_to_inline: return False
        typ = type(obj)
        typename = typ.__name__
        if typ in (types.FunctionType, types.MethodType, types.BuiltinFunctionType, types.BuiltinMethodType):
            typename = 'function'
        if not typename: return False
        alt_typename = None
        if is_class(obj):
            alt_typename = 'class'
        elif is_instance(obj) and typename != 'function':
            typename = 'instance'
            class_name = get_name(obj.__class__) if hasattr(obj, '__class__') else get_name(type(obj))
            alt_typename = class_name
        for re_match in self.parent.types_to_inline:
            if re_match(typename): return True
            if alt_typename and re_match(alt_typename): return True
        return False

    def get_heap(self):
        return self.encoded_heap_objects

    def reset_heap(self):
        self.encoded_heap_objects = {}

    def set_function_parent_frame_ID(self, ref_obj, enclosing_frame_id):
        assert ref_obj[0] == 'REF'
        func_obj = self.encoded_heap_objects[ref_obj[1]]
        assert func_obj[0] == 'FUNCTION'
        func_obj[-1] = enclosing_frame_id

    def encode(self, dat, get_parent):
        if not self.render_heap_primitives and type(dat) in PRIMITIVE_TYPES:
            return encode_primitive(dat)
        else:
            is_externally_defined = False  # is dat defined in external (i.e., non-user) code?
            try:
                gsf = inspect.getmodule(dat).__file__
                if not gsf:
                    gsf = inspect.getsourcefile(dat)
                if gsf and gsf[0] == '/' and 'generate_json_trace.py' not in gsf:
                    is_externally_defined = True
            except (AttributeError, TypeError):
                pass  # fail soft
            my_id = id(dat)
            if (is_instance(dat) and
                    type(dat) not in (
                            types.FunctionType, types.MethodType, types.BuiltinFunctionType,
                            types.BuiltinMethodType) and
                    hasattr(dat, '__class__') and (get_name(dat.__class__) != 'ABCMeta')):
                is_externally_defined = False
            if is_externally_defined:
                label = 'object'
                try:
                    label = type(dat).__name__
                    if is_class(dat):
                        label = 'class'
                    elif is_instance(dat):
                        label = 'object'
                except:
                    pass
                return ['IMPORTED_FAUX_PRIMITIVE', 'imported ' + label]  # punt early!
            if self.should_inline_object_by_type(dat):
                label = 'object'
                try:
                    label = type(dat).__name__
                    if is_class(dat):
                        class_name = get_name(dat)
                        label = class_name + ' class'
                    elif is_instance(dat):
                        class_name = get_name(dat.__class__) if hasattr(dat, '__class__') else get_name(type(dat))
                        label = class_name + ' instance' if class_name else 'instance'
                except:
                    pass
                return ['IMPORTED_FAUX_PRIMITIVE', label + ' (hidden)']  # punt early!
            try:
                my_small_id = self.id_to_small_IDs[my_id]
            except KeyError:
                my_small_id = self.cur_small_ID
                self.id_to_small_IDs[my_id] = self.cur_small_ID
                self.cur_small_ID += 1
            del my_id  # to prevent bugs later in this function
            ret = ['REF', my_small_id]
            if my_small_id in self.encoded_heap_objects: return ret
            new_obj = []
            self.encoded_heap_objects[my_small_id] = new_obj
            typ = type(dat)
            if typ == list:
                new_obj.append('LIST')
                for e in dat:
                    new_obj.append(self.encode(e, get_parent))
            elif typ == tuple:
                new_obj.append('TUPLE')
                for e in dat:
                    new_obj.append(self.encode(e, get_parent))
            elif typ == set:
                new_obj.append('SET')
                for e in dat:
                    new_obj.append(self.encode(e, get_parent))
            elif typ == dict:
                new_obj.append('DICT')
                for (k, v) in dat.items():
                    if k not in ('__module__', '__return__', '__locals__'):
                        new_obj.append([self.encode(k, get_parent), self.encode(v, get_parent)])
            elif typ in (types.FunctionType, types.MethodType):
                argspec = inspect.getfullargspec(dat) if is_python3 else inspect.getargspec(dat)
                printed_args = [e for e in argspec.args]
                default_arg_names_and_vals = []
                if argspec.defaults:
                    num_missing_defaults = len(printed_args) - len(argspec.defaults)
                    assert num_missing_defaults >= 0
                    for i in range(num_missing_defaults, len(printed_args)):
                        default_arg_names_and_vals.append(
                            (printed_args[i], self.encode(argspec.defaults[i - num_missing_defaults], get_parent)))
                if argspec.varargs:
                    printed_args.append('*' + argspec.varargs)
                if is_python3:
                    if argspec.kwonlyargs:
                        printed_args.extend(argspec.kwonlyargs)
                        if argspec.kwonlydefaults:
                            for varname in argspec.kwonlyargs:
                                if varname in argspec.kwonlydefaults:
                                    val = argspec.kwonlydefaults[varname]
                                    default_arg_names_and_vals.append((varname, self.encode(val, get_parent)))
                    if argspec.varkw:
                        printed_args.append('**' + argspec.varkw)
                else:
                    if argspec.keywords:
                        printed_args.append('**' + argspec.keywords)
                func_name = get_name(dat)
                pretty_name = func_name
                try:
                    pretty_name += '(' + ', '.join(printed_args) + ')'
                except TypeError:
                    pass
                if func_name == '<lambda>':
                    cod = (dat.__code__ if is_python3 else dat.func_code)  # ugh!
                    lst = self.line_to_lambda_code[cod.co_firstlineno]
                    if cod not in lst: lst.append(cod)
                    pretty_name += create_lambda_line_number(cod, self.line_to_lambda_code)
                encoded_val = ['FUNCTION', pretty_name, None]
                if get_parent:
                    enclosing_frame_id = get_parent(dat)
                    encoded_val[2] = enclosing_frame_id
                new_obj.extend(encoded_val)
                if default_arg_names_and_vals:
                    new_obj.append(default_arg_names_and_vals)  # *append* it as a single list element
            elif typ is types.BuiltinFunctionType:
                pretty_name = get_name(dat) + '(...)'
                new_obj.extend(['FUNCTION', pretty_name, None])
            elif is_class(dat) or is_instance(dat):
                self.encode_class_or_instance(dat, new_obj)
            elif typ is types.ModuleType:
                new_obj.extend(['module', dat.__name__])
            elif typ in PRIMITIVE_TYPES:
                assert self.render_heap_primitives
                new_obj.extend(['HEAP_PRIMITIVE', type(dat).__name__, encode_primitive(dat)])
            else:
                typeStr = str(typ)
                m = typeRE.match(typeStr)
                if not m:  m = classRE.match(typeStr)
                assert m, typ
                encoded_dat = str(dat) if is_python3 else str(dat).decode('utf-8', 'replace')
                new_obj.extend([m.group(1), encoded_dat])
            return ret

    def encode_class_or_instance(self, dat, new_obj):
        if is_instance(dat):
            class_name = get_name(dat.__class__) if hasattr(dat, '__class__') else get_name(type(dat))
            pprint_str = None
            if hasattr(dat, '__str__'):
                try:
                    pprint_str = dat.__str__()
                    if pprint_str[0] == '<' and pprint_str[-1] == '>' and (
                            ' at ' in pprint_str or pprint_str.startswith('<module')):
                        pprint_str = None
                except:
                    pass
            if pprint_str:
                new_obj.extend(['INSTANCE_PPRINT', class_name, pprint_str])
            else:
                new_obj.extend(['INSTANCE', class_name])
            if class_name == 'module': return
        else:
            superclass_names = [e.__name__ for e in dat.__bases__ if e is not object]
            new_obj.extend(['CLASS', get_name(dat), superclass_names])
        hidden = ('__doc__', '__module__', '__return__', '__dict__', '__locals__', '__weakref__', '__qualname__')
        user_attrs = sorted([e for e in dat.__dict__ if e not in hidden]) if hasattr(dat, '__dict__') else []
        for attr in user_attrs:
            if not self.should_hide_var(attr):
                new_obj.append([self.encode(attr, None), self.encode(dat.__dict__[attr], None)])
