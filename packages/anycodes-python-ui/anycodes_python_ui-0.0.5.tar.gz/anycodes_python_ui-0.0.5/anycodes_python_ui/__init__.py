from .python_ui_run import PGLogger
import getopt
import os
import sys

opts, args = getopt.getopt(sys.argv[1:], 'mhc:', ['help', 'command='])
sys.argv[:] = args
sys.path[0] = os.path.dirname(args[0])
with open(args[0], 'r') as f:
    file_data = f.read()
logger = PGLogger()
logger._runscript(file_data)
logger.finalize()
