import os
import sys
import shutil
import zipfile
import subprocess

from urllib import request

EMBEDDED_PYTHON_URL = "https://www.python.org/ftp/python/3.8.2/python-3.8.2-embed-amd64.zip"
BUILD_DIR           = os.path.join(os.getcwd(), "build")
EMBEDDED_PY_DIR     = os.path.join(BUILD_DIR, "mek_python")
WHEELS_DIR          = os.path.join(EMBEDDED_PY_DIR, "wheels")
LIB_DIR             = os.path.join(EMBEDDED_PY_DIR, "Lib")
SITEPACKAGES_DIR    = os.path.join(LIB_DIR, "site-packages")

MEK_LIBRARIES = ["refinery", "mozzarilla", "hek_pool"]

# Clean up first
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

# Create the root build directory
os.makedirs(BUILD_DIR)

# Download embedded python
embedded_python_zip, _ = request.urlretrieve(EMBEDDED_PYTHON_URL)

# Extract embedded puthon into our build dir
with zipfile.ZipFile(embedded_python_zip, 'r') as file:
    file.extractall(BUILD_DIR)

# Create a wheels directory to store pip and setuptools in.
os.makedirs(EMBEDDED_PY_DIR)

# Download the wheels to the wheels directory
subprocess.run(
    [sys.executable, "-m", "pip",
    "download", "setuptools", "pip"],
    cwd=WHEELS_DIR)

wheels = os.listdir(WHEELS_DIR)
for i in range(len(wheels)):
    wheels[i] = "wheels/" + wheels[i]

# Create the Lib directory, this is where the local packages will be installed.
os.makedirs(LIB_DIR)
# This is where our packages will be installed.
os.makedirs(SITEPACKAGES_DIR)

# Install tkinter.
with zipfile.ZipFile("includes/tkinter.zip", 'r') as file:
    file.extractall(os.path.join(BUILD_DIR, "tkinter"))
# Install tcl/tk which is required by tkinter.
with zipfile.ZipFile("includes/tcl.zip", 'r') as file:
    file.extractall(os.path.join(BUILD_DIR, "tcl"))

#create ._pth file with all the lookup directories for our embedded Python.
with open(os.path.join(BUILD_DIR, "python38._pth"), "w") as pth_file:
    pth_file.write("\n".join([
        # Locally installed:
        "Lib",
        # pip and setuptools:
        *wheels,
        # tkinter:
        "tkinter",
        # These are in there by default:
        "python38.zip",
        ".",
        # This is needed so the site-packages from Lib are actually seen.
        "import site"
    ]))
    pth_file.flush()

# Install the current version of the mek libraries to the local libs folder
# in our build directory.
subprocess.run(
    [os.path.join(BUILD_DIR, "python.exe"), "-m", "pip",
    "install", *MEK_LIBRARIES])
