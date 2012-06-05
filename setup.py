# http://cx_freeze.readthedocs.org/en/latest/distutils.html#distutils

import sys, os
from cx_Freeze import setup, Executable

base = None
targetName = "platex"
includes = []
if sys.platform == "win32":
    base = "Win32GUI"
    targetName = "platex.exe"
    includes.extend(['numpy.core.multiarray', 'serial.win32'])

Platex_Target = Executable( script = "platex.pyw",
                            initScript = None,
                            base = base,
                            targetName = targetName,
                            compress = True,
                            copyDependentFiles = True,
                            appendScriptToExe = False,
                            appendScriptToLibrary = False,
                            shortcutName = "Platex",
                            shortcutDir = "ProgramMenuFolder")

include_files = ['avrdude/']

build_exe_options = {"packages": [],
                     "includes": includes,
                     "excludes": [],
                     "include_files": include_files}

setup(  name = "Platex",
        version = "0.2",
        description = "Control Arduino from your computer",
        options = {"build_exe": build_exe_options},
        executables = [Platex_Target])
