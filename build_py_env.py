import os
import sys
import shutil
import zipfile
import subprocess
import traceback

from os import path
from urllib import request
from zipfile import ZipFile

##### Function stolen from mek installer:
def download_mek_to_folder(install_dir, src_url):
    '''
    Downloads the mek scripts from the mek repo master and extracts them into
    install_dir.
    '''

    print('Downloading newest version of MEK from: "%s"' % src_url)

    mek_zipfile_path, _ = request.urlretrieve(src_url)
    if not mek_zipfile_path:
        print("  Could not download.\n")
        return
    else:
        print("  Finished.\n")

    setup_filepath = '' if "__file__" not in globals() else __file__
    setup_filepath = setup_filepath.lower()
    setup_filename = setup_filepath.split(os.sep)[-1]

    try:
        with open(__file__, 'rb') as f:
            setup_file_data = f.read()
    except Exception:
        setup_file_data = None

    new_installer_path = None

    print('Unpacking MEK to "%s"' % install_dir)
    with ZipFile(mek_zipfile_path) as mek_zipfile:
        for zip_name in mek_zipfile.namelist():
            # ignore the root directory of the zipfile
            filepath = zip_name.split("/", 1)[-1]
            if filepath[:1] == '.' or zip_name[-1:] == "/":
                continue

            try:
                filepath = path.join(install_dir, filepath)

                os.makedirs(path.dirname(filepath), exist_ok=True)

                with mek_zipfile.open(zip_name) as zf, open(filepath, "wb+") as f:
                    filedata = zf.read()
                    f.write(filedata)
            except Exception:
                print(traceback.format_exc())

    try: os.remove(mek_zipfile_path)
    except Exception: pass


EMBEDDED_PYTHON_URL = "https://www.python.org/ftp/python/3.8.2/python-3.8.2-embed-amd64.zip"
MEK_URL             = "https://github.com/Sigmmma/mek/archive/update2.zip"
BUILD_DIR           = os.path.join(os.getcwd(), "build")
EMBEDDED_PY_DIR     = os.path.join(BUILD_DIR, "mek_python")
WHEELS_DIR          = os.path.join(EMBEDDED_PY_DIR, "wheels")
LIB_DIR             = os.path.join(EMBEDDED_PY_DIR, "Lib")
SITEPACKAGES_DIR    = os.path.join(LIB_DIR, "site-packages")
MEK_DIR             = os.path.join(EMBEDDED_PY_DIR, "mek")

MEK_LIBRARIES = ["refinery", "mozzarilla", "hek_pool"]

# Clean up first
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

# Create the root build directory
os.makedirs(BUILD_DIR)
os.makedirs(EMBEDDED_PY_DIR)

# Download embedded python
embedded_python_zip, _ = request.urlretrieve(EMBEDDED_PYTHON_URL)

# Extract embedded puthon into our embedded python dir
with zipfile.ZipFile(embedded_python_zip, 'r') as file:
    file.extractall(EMBEDDED_PY_DIR)

# Create a wheels directory to store pip and setuptools in.
os.makedirs(WHEELS_DIR)

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
    file.extractall(os.path.join(EMBEDDED_PY_DIR, "tkinter"))
# Install tcl/tk which is required by tkinter.
with zipfile.ZipFile("includes/tcl.zip", 'r') as file:
    file.extractall(os.path.join(EMBEDDED_PY_DIR, "tcl"))

#create ._pth file with all the lookup directories for our embedded Python.
with open(os.path.join(EMBEDDED_PY_DIR, "python38._pth"), "w") as pth_file:
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
    [os.path.join(EMBEDDED_PY_DIR, "python.exe"), "-m", "pip",
    "install", *MEK_LIBRARIES])

# Install the MEK to the directory we've designated. The way that the MEK
# installer would have done it.
os.makedirs(MEK_DIR)

download_mek_to_folder(MEK_DIR, MEK_URL)
