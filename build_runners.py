import os
import sys
import shutil
import subprocess

from argparse import ArgumentParser

from os import path

parser = ArgumentParser(description='Build PyInstaller Exes')
parser.add_argument('--py-exe', help='The python exe to use. USE PYTHON 3.6', required=True)
cmd_args = parser.parse_args()

BUILD_DIR        = path.join(os.getcwd(), "build")
RUNNERS_DIR      = path.join(os.getcwd(), "runners")
RUNNERS_DIST_DIR = path.join(RUNNERS_DIR, "dist")
ICONS_DIR        = path.join(os.getcwd(), "icons")

def build_exe(script_name, icon_name):
    subprocess.run([
        cmd_args.py_exe, "-m",
        "PyInstaller", "-F",
        "--noconsole",
        "--icon=%s" % (icon_name),
        "%s" % (script_name)], cwd=RUNNERS_DIR)

MEK_PROGRAMS = (
    ("Mozzarilla.py",  "../icons/mozzarilla.ico"),
    ("Pool.py",        "../icons/pool.ico"),
    ("Refinery.py",    "../icons/refinery.ico"),
    ("MEK_Updater.py", "../icons/meke.ico"),
)

for program in MEK_PROGRAMS:
    build_exe(*program)

# Copy the runners into the main directory.
runner_names = filter(lambda n : n.lower().endswith(".exe"),
                    os.listdir(RUNNERS_DIST_DIR))

for name in runner_names:
    shutil.copyfile(path.join(RUNNERS_DIST_DIR, name), path.join(BUILD_DIR, name))
