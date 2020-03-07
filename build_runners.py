import os
import sys
import shutil
import subprocess

from argparse import ArgumentParser

from os import path

parser = ArgumentParser(description='Build PyInstaller Exes')
parser.add_argument('--py-exe', help='The python exe to use. USE PYTHON 3.6', required=True)
cmd_args = parser.parse_args()

RUNNERS_DIR      = path.join(os.getcwd(), "runners")
RUNNERS_DIST_DIR = path.join(RUNNERS_DIR, "dist")
ICONS_DIR        = path.join(os.getcwd(), "icons")

def build_exe(script_name, icon_name):
    subprocess.run([
        cmd_args.py_exe, "-m",
        "PyInstaller", "-F",
        "--noconsole",
        "--icon='%s"' % (path.join(ICONS_DIR, icon_name)),
        "%s" % (script_name)])

MEK_PROGRAMS = (
    ("Mozzarilla.py",  "mozzarilla.ico"),
    ("Pool.py",        "pool.ico"),
    ("Refinery.py",    "refinery.ico"),
    ("MEK_Updater.py", "meke.ico"),
)

for program in MEK_PROGRAMS:
    build_exe(*program)

# Copy the runners into the main directory.
runner_names = filter(lambda n : n.lower().endswith(".exe"),
                    os.listdir(RUNNERS_DIR))

for name in runner_names:
    shutil.copyfile(path.join(runners_path, name), path.join(BUILD_DIR, name))
