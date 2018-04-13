import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = 'c:/python36/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = 'c:/python36/tcl/tk8.6'

buildOptions = dict(
    packages = [],
    excludes = [],
    include_files=['c:/python36/DLLs/tcl86t.dll', 'c:/python36/DLLs/tk86t.dll']
)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Main.py', base=base)
]

setup(name='editor',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
