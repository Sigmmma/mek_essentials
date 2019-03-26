#!/usr/bin/env python
from os.path import dirname, join
from cx_Freeze import setup, Executable
import os

REQUIRED_MODULES = (
    'reclaimer', 'binilla', 'supyr_struct', 'arbytmap',
    'mozzarilla', 'refinery', 'hek_pool', 'threadsafe_tkinter'
    )

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
SITE_PACKAGES_DIR = os.path.join(PYTHON_INSTALL_DIR, 'lib', 'site-packages')

module_dirs = {n: os.path.join(SITE_PACKAGES_DIR, n) for n in REQUIRED_MODULES}


os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY']  = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6') 

curr_dir = dirname(__file__)
setup(
    name='meke',
    author='Devin Bobadilla',
    author_email='MosesBobadilla@gmail.com',
    license='MIT',
    executables=[
        Executable(os.path.join(module_dirs["hek_pool"], 'run.py'),
            targetName='Pool.exe', base='Win32GUI',
            icon=os.path.join(curr_dir, 'rsrc', 'icons', 'pool.ico')
            ),
        Executable(os.path.join(module_dirs["refinery"], 'run.py'),
            targetName='Refinery.exe',
            icon=os.path.join(curr_dir, 'rsrc', 'icons', 'refinery.ico')
            ),
        Executable(os.path.join(module_dirs["mozzarilla"], 'run.py'),
            targetName='Mozzarilla.exe', base='Win32GUI',
            icon=os.path.join(curr_dir, 'rsrc', 'icons', 'mozzarilla.ico')
            ),
        ],
    options=dict(
        build_exe=dict(
            packages=REQUIRED_MODULES,
            include_files=[
                os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                os.path.join(module_dirs["hek_pool"], 'ogg_v1.1.2_dll_fix.zip'),
                os.path.join(module_dirs["mozzarilla"], 'styles'),
                os.path.join(module_dirs["hek_pool"], 'msg.dat'),
                os.path.join(module_dirs["refinery"], 'msg.dat'),
                os.path.join(module_dirs["mozzarilla"], 'msg.dat'),
                os.path.join(curr_dir, 'rsrc', '3ds_max_scripts'),
                os.path.join(curr_dir, 'rsrc', 'icons'),
                os.path.join(curr_dir, 'rsrc', 'cmd_lists'),
                os.path.join(curr_dir, 'rsrc', 'READMES'),
                os.path.join(curr_dir, 'rsrc', 'readme.txt'),
                os.path.join(curr_dir, 'rsrc', 'DO NOT RENAME OR MOVE THESE FILES.txt'),
                ]
            )
        )
    )
