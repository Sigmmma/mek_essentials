import os
import sys
import shutil
import tarfile
import zipfile
import subprocess
import traceback

from argparse import ArgumentParser
from os import path
from urllib import request
from zipfile import ZipFile

PY_VER_SHORT, PY_VER = "312", "3.12.2"
SOURCE_PYTHON_URL    = "https://www.python.org/ftp/python/%s/Python-%s.tar.xz" % (PY_VER, PY_VER)
EMBEDDED_PYTHON_URL  = "https://www.python.org/ftp/python/%s/python-%s-embed-amd64.zip" % (PY_VER, PY_VER)
MEK_PACKAGES    = dict(
    hek_pool            = "git+https://github.com/sigmmma/hek_pool.git",
    refinery            = "git+https://github.com/sigmmma/refinery.git",
    mozzarilla          = "git+https://github.com/sigmmma/mozzarilla.git",
    reclaimer           = "git+https://github.com/sigmmma/reclaimer.git",
    binilla             = "git+https://github.com/sigmmma/binilla.git",
    supyr_struct        = "git+https://github.com/sigmmma/supyr_struct.git",
    arbytmap            = "git+https://github.com/sigmmma/arbytmap.git",
    threadsafe_tkinter  = "git+https://github.com/sigmmma/threadsafe_tkinter.git",
    mek                 = "git+https://github.com/sigmmma/mek.git",
    )

# NOTE: this is ordered so the packages depending on others will be
#       installed first, allowing those others to be overwritten
#       with the version we may have specified on the command line.
TOPLEVEL_INSTALL_ORDER = (
    "refinery", "hek_pool", "mozzarilla"
    )
COMPLETE_INSTALL_ORDER = (
    *TOPLEVEL_INSTALL_ORDER, "reclaimer",
    "binilla", "arbytmap", "supyr_struct",
    "threadsafe_tkinter"
    )

parser = ArgumentParser(description='The script to build the executable MEKE environment.')
parser.add_argument(
    '--use-source-urls', action='store_true',
    help='Download packages from the source urls instead of PyPI.'
    )
for name in sorted(MEK_PACKAGES):
    parser.add_argument(
        '--%s-branch' % name.replace("_", "-"), default="",
        help='The branch to pull the %s module from.' % name
        )

cmd_args = parser.parse_args()

package_branch_names = {
    name: getattr(cmd_args, "%s_branch" % name, "") for name in MEK_PACKAGES
    }

INSTALL_FROM_SOURCE = cmd_args.use_source_urls
MEK_URL             = "https://github.com/Sigmmma/mek/archive/%s.zip" % (
    package_branch_names.get("mek", "master") or "master"
    )
BUILD_DIR           = os.path.join(os.getcwd(), "build")
EMBEDDED_PY_DIR     = os.path.join(BUILD_DIR, "mek_python")
INCLUDE_DIR         = os.path.join(EMBEDDED_PY_DIR, "Include")
WHEELS_DIR          = os.path.join(EMBEDDED_PY_DIR, "wheels")
LIB_DIR             = os.path.join(EMBEDDED_PY_DIR, "Lib")
SITEPACKAGES_DIR    = os.path.join(LIB_DIR, "site-packages")
MEK_DIR             = os.path.join(EMBEDDED_PY_DIR, "mek")


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


sources_to_install  = (
    (mod_name               if not cmd_args.use_source_urls else 
     MEK_PACKAGES[mod_name] if not package_branch_names.get(mod_name) else
     "%s@%s" % (MEK_PACKAGES[mod_name], package_branch_names.get(mod_name, ""))
     ).rstrip("@") or mod_name
    for mod_name in (
        COMPLETE_INSTALL_ORDER if INSTALL_FROM_SOURCE else
        TOPLEVEL_INSTALL_ORDER
        )
    )


# Clean up first
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

# Create the root build directory
os.makedirs(BUILD_DIR)
os.makedirs(EMBEDDED_PY_DIR)

# Download source and embedded python
embedded_python_zip,  _ = request.urlretrieve(EMBEDDED_PYTHON_URL)

# Extract embedded puthon into our embedded python dir
with zipfile.ZipFile(embedded_python_zip, 'r') as file:
    file.extractall(EMBEDDED_PY_DIR)

# if installing from sources, the python header files are required
if INSTALL_FROM_SOURCE:
    source_python_tar_xz, _ = request.urlretrieve(SOURCE_PYTHON_URL)
    with tarfile.open(source_python_tar_xz) as tf:
        members = [
            member for member in tf.getmembers() 
            if member.name.count("/") > 1
            and member.name.split("/")[1].lower() == "include"
            ]
        # change the extraction folder and extract
        for member in members:
            member.name = member.name.split('/', 2)[2]
            tf.extract(member, INCLUDE_DIR)

    shutil.copyfile("includes/pyconfig.h", os.path.join(INCLUDE_DIR, "pyconfig.h"))

    # Install libs required for linking
    with zipfile.ZipFile("includes/libs.zip", 'r') as file:
        file.extractall(os.path.join(EMBEDDED_PY_DIR, "libs"))


# Create a wheels directory to store pip and setuptools in.
os.makedirs(WHEELS_DIR)

# Download the wheels to the wheels directory
subprocess.run(
    [sys.executable, "-m", "pip", "download",
    # NOTE: something in v75.9.0 of setuptools is breaking the
    #       build, so we're locking to the latest working one.
    "setuptools<=v75.8.2", "pip", "--no-cache-dir",
    ],
    cwd=WHEELS_DIR)

wheels = os.listdir(WHEELS_DIR)
for i in range(len(wheels)):
    wheels[i] = "wheels/" + wheels[i]

# Create the Lib directory, this is where the local packages will be installed.
os.makedirs(LIB_DIR)
# This is where our packages will be installed.
os.makedirs(SITEPACKAGES_DIR)

# For some reason, jaraco has no __init__.py in its root, which makes
# setuptools unable to find it. This makes wheels effectively useless
# for installing jaraco, soooo we're gonna need to install it to the
# sitepackages and create an empty __init__.py in its root.
#    See - https://github.com/jaraco/jaraco.classes/issues/2
subprocess.run(
    [sys.executable, "-m", "pip", "install", 
    "jaraco.collections", "jaraco.functools", "jaraco.text", 
    "--target", SITEPACKAGES_DIR, "--no-cache-dir"
    ])
with open(os.path.join(SITEPACKAGES_DIR, "jaraco", "__init__.py"), "w") as init_file:
    pass

# Install tkinter.
with zipfile.ZipFile("includes/tkinter.zip", 'r') as file:
    file.extractall(os.path.join(EMBEDDED_PY_DIR, "tkinter"))

# Install tcl/tk which is required by tkinter.
with zipfile.ZipFile("includes/tcl.zip", 'r') as file:
    file.extractall(os.path.join(EMBEDDED_PY_DIR, "tcl"))

#create ._pth file with all the lookup directories for our embedded Python.
with open(os.path.join(EMBEDDED_PY_DIR, "python%s._pth" % PY_VER_SHORT), "w") as pth_file:
    pth_file.write("\n".join([
        # Locally installed:
        "Lib",
        # pip and setuptools:
        *wheels,
        # tkinter:
        "tkinter",
        # These are in there by default:
        ("python%s.zip" % PY_VER_SHORT),
        ".",
        # This is needed so the site-packages from Lib are actually seen.
        "import site"
    ]))
    pth_file.flush()

# Install the current version of the mek libraries to the local libs folder
# in our build directory.
subprocess.run(
    [os.path.join(EMBEDDED_PY_DIR, "python.exe"), "-m", "pip",
    "install", *sources_to_install, "--force-reinstall", "--no-cache-dir"
    ])

# Install the MEK to the directory we've designated. The way that the MEK
# installer would have done it.
os.makedirs(MEK_DIR)

download_mek_to_folder(MEK_DIR, MEK_URL)
