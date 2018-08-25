#!/usr/bin/env python
from os.path import dirname, join
from cx_Freeze import setup, Executable
'''
from reclaimer.h2.defs import *
from reclaimer.hek.defs import *
from reclaimer.misc.defs import *
from reclaimer.os_hek.defs import *
from reclaimer.os_v3_hek.defs import *
from reclaimer.os_v4_hek.defs import *
'''
import os
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
SITE_PACKAGES_DIR = os.path.join(PYTHON_INSTALL_DIR, 'lib', 'site-packages')
HEK_POOL_DIR = os.path.join(SITE_PACKAGES_DIR, 'hek_pool')
REFINERY_DIR = os.path.join(SITE_PACKAGES_DIR, 'refinery')
MOZZARILLA_DIR = os.path.join(SITE_PACKAGES_DIR, 'mozzarilla')

os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY']  = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6') 

curr_dir = dirname(__file__)

setup(
    name='meke',
    author='Devin Bobadilla',
    author_email='MosesBobadilla@gmail.com',
    package_data=dict(
        hek_pool=['*.ico'],
        refinery=['*.ico'],
        mozzarilla=['*.ico'],
        ),
    license='MIT',
    executables=[
        Executable(os.path.join(HEK_POOL_DIR, 'run.py'),
            targetName='Pool.exe', base='Win32GUI',
            icon=os.path.join(curr_dir, 'rsrc', 'icons', 'pool.ico')
            ),
        Executable(os.path.join(REFINERY_DIR, 'run.py'),
            targetName='Refinery.exe',
            icon=os.path.join(curr_dir, 'rsrc', 'icons', 'refinery.ico')
            ),
        Executable(os.path.join(MOZZARILLA_DIR, 'run.py'),
            targetName='Mozzarilla.exe', base='Win32GUI',
            icon=os.path.join(curr_dir, 'rsrc', 'icons', 'mozzarilla.ico')
            ),
        ],
    options=dict(build_exe=dict(
        packages=['reclaimer', 'binilla', 'supyr_struct', 'arbytmap',
                  'mozzarilla', 'refinery', 'hek_pool', 'threadsafe_tkinter'],
        include_files=[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            os.path.join(HEK_POOL_DIR, 'ogg_v1.1.2_dll_fix.zip'),
            os.path.join(MOZZARILLA_DIR, 'styles'),
            os.path.join(curr_dir, 'rsrc', 'scripts'),
            os.path.join(curr_dir, 'rsrc', 'icons'),
            os.path.join(curr_dir, 'rsrc', 'cmd_lists'),
            os.path.join(curr_dir, 'rsrc', 'READMES'),
            os.path.join(curr_dir, 'rsrc', 'readme.txt'),
            os.path.join(curr_dir, 'rsrc', 'DO NOT RENAME OR MOVE THESE FILES.txt'),
            ]
        ))
    )
