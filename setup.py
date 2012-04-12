# http://cx_freeze.readthedocs.org/en/latest/distutils.html#distutils

import sys, os
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# For Win32: 'imageformat' folder from 'PYTHONDIR\lib\site-packages\PyQt4\plugins' must be added to project root so images can be loaded

Platex_Target = Executable( script = "platex.pyw",
                            initScript = None,
                            base = None,
                            targetName = "platex",
                            compress = True,
                            copyDependentFiles = True,
                            appendScriptToExe = False,
                            appendScriptToLibrary = False)

include_files = ['avrdude/']
#include_files = []

build_exe_options = {"packages": [],
                     "excludes": [],
                     "include_files": include_files}

setup(  name = "Platex",
        version = "0.1",
        description = "Control Arduino from your computer",
        options = {"build_exe": build_exe_options},
        executables = [Platex_Target])
