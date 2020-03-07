import os
import sys
import shutil
import subprocess

from os import path

PY_EXE = "c:\\python36\\python.exe"

RUNNERS_DIR      = path.join(os.getcwd(), "runners")
RUNNERS_DIST_DIR = path.join(RUNNERS_DIR, "dist")
ICONS_DIR        = path.join(os.getcwd(), "icons")

def build_exe(script_name, icon_name):
    subprocess.run([
        PY_EXE, "-m",
        "PyInstaller", "-F",
        "--noconsole",
        "--icon=%r" % (path.join(ICONS_DIR, icon_name)),
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
