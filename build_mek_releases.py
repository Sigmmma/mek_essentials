import fnmatch
import os
import shutil
import subprocess
import tempfile
import traceback
import zipfile

from urllib import request

mek_modules = (
    "arbytmap", "binilla",
    "hek_pool", "mozzarilla",
    "reclaimer", "refinery",
    "supyr_struct", "threadsafe_tkinter"
    )

# Set these manually
repos_dir = "F:\\My Files\\Applications\\My Repos\\"
prebuilt_mek_zip_path = os.path.join(os.curdir.rstrip("/\\"), "MEK_Prebuilt.zip")
meke_dir = os.path.join(repos_dir, "MEKE")
meke_build_script = os.path.join(meke_dir, "src", "build.bat")

temp_root = os.path.realpath(os.path.join(tempfile.gettempdir(), "mek_build_temp_folder"))
prebuilt_mek_dir = os.path.join(temp_root, "MEK_Prebuilt")

mek_download_url = "https://bitbucket.org/Moses_of_Egypt/mek/get/default.zip"
script_test = (
    input("Type 'y' to do an actual upload: ").strip().lower() != 'y')

def unzip_zipfile(zipfile_path, dst, del_zipfile=False):
    with zipfile.ZipFile(zipfile_path) as zf:
        for zip_name in zf.namelist():
            filepath = zip_name.split("/", 1)[-1]
            if filepath[:1] == '.':
                continue

            try:
                filepath = os.path.join(dst, filepath).replace("\\", "/")
                filename = os.path.basename(filepath)
                dirpath = os.path.dirname(filepath)

                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)

                with zf.open(zip_name) as zzf, open(filepath, "wb+") as f:
                    f.write(zzf.read())
            except Exception:
                print(traceback.format_exc())

    if del_zipfile:
        try: os.remove(zipfile_path)
        except Exception: pass


def get_matches_ignore_file(filepath, ignore):
    return False


def copy_module_files(src, dst):
    os.makedirs(dst, exist_ok=True)
    for _, dirs, __ in os.walk(src):
        for dirname in dirs:
            if dirname.lower() not in (
                    ".hg", ".vs", "test_files", "x64", "__pycache__",
                    "arbytmap_ext", "bitmap_io_ext", "dds_defs_ext",
                    "raw_packer_ext", "raw_unpacker_ext", "swizzler_ext",
                    "tiler_ext"):
                shutil.copytree(os.path.join(src, dirname),
                                os.path.join(dst, dirname))

        # only copy the root folders
        break

    for _, __, files in os.walk(src):
        for filename in files:
            name = os.path.splitext(filename)[0].lower()
            ext = os.path.splitext(filename)[-1].lower()

            if ext == ".txt" and name in ("todo", ):
                continue
            elif ext in (".backup", ".sln", ".user", ".filters", ".vcxproj"):
                continue
            elif ext == "" and name == ".hgignore":
                continue

            shutil.copy(os.path.join(src, filename),
                        os.path.join(dst, filename))

        # only copy the root files
        break

    glob_ignore = []
    ignore_filepath = os.path.join(src, ".hgignore")
    try:
        with open(ignore_filepath, "r") as f:
            for line in f:
                line = line.strip(" \n")
                if line and line[0] != "#":
                    glob_ignore.append(line.replace("\\", "/"))

        # ignore the first line
        if glob_ignore:
            syntax_line = tuple(
                s.strip() for s in glob_ignore.pop(0).lower().split(" ") if s)
            if syntax_line != ("syntax:", "glob"):
                glob_ignore = ()

    except Exception:
        pass

    # remove compiled python files and ignored files
    for root, dirs, files in os.walk(dst):
        for filename in files:
            filepath = os.path.realpath(os.path.join(root, filename))
            rel_filepath = os.path.relpath(filepath, dst)
            # explicitly include any .pyd accelerators
            if os.path.splitext(filename)[-1].lower() != ".pyd":
                for pattern in glob_ignore:
                    if fnmatch.fnmatch(rel_filepath, pattern):
                        os.remove(filepath)
                        break

        for dirname in dirs:
            dirpath = os.path.realpath(os.path.join(root, dirname))
            rel_dirpath = os.path.join(os.path.normpath(
                    os.path.join("/", os.path.relpath(dirpath, dst))), "")
            for pattern in glob_ignore:
                if fnmatch.fnmatch(rel_dirpath, pattern):
                    shutil.rmtree(dirpath)
                    break


def pypi_upload(root="", egg=True, wheel=True, source=False, *,
                username=None, password=None):
    if not root:
        root = os.curdir

    module_temp_dir = os.path.realpath(
        os.path.join(temp_root, os.path.basename(root)))

    # make sure the build directory is clean.
    try: shutil.rmtree(module_temp_dir)
    except FileNotFoundError: pass
    try: shutil.rmtree(os.path.join(module_temp_dir, ".egg-info"))
    except FileNotFoundError: pass
    try: shutil.rmtree(os.path.join(temp_root, "build"))
    except FileNotFoundError: pass
    os.makedirs(module_temp_dir, exist_ok=True)

    # copy the contents of root into the temp_root directory.
    copy_module_files(root, module_temp_dir)
    shutil.move(os.path.join(module_temp_dir, "setup.py"),
                os.path.join(temp_root, "setup.py"))

    if egg:
        subprocess.run('python %s sdist bdist_egg' %
                       os.path.join(temp_root, "setup.py"), cwd=temp_root)

    if wheel:
        subprocess.run('python %s sdist bdist_wheel' %
                       os.path.join(temp_root, "setup.py"), cwd=temp_root)

    if source:
        subprocess.run('python %s sdist --formats=zip' %
                       os.path.join(temp_root, "setup.py"), cwd=temp_root)

    # find the filename of the newly built module
    egg_filepath = wheel_filepath = zip_filepath = None
    for root, _, files in os.walk(os.path.join(temp_root, "dist")):
        for filename in sorted(files):
            if filename.lower().endswith(".egg"):
                egg_filepath = os.path.join(root, filename)
            elif filename.lower().endswith(".whl"):
                wheel_filepath = os.path.join(root, filename)
            elif filename.lower().endswith(".zip"):
                wheel_filepath = os.path.join(root, filename)

    extra_args = ""
    if username:
        extra_args += '-u "%s"' % username

    if password:
        extra_args += '-p "%s"' % password

    if script_test:
        return

    # upload the module with twine
    if egg_filepath:
        subprocess.run('twine upload "%s" %s' %
                       (egg_filepath, extra_args), cwd=temp_root)

    if wheel_filepath:
        subprocess.run('twine upload "%s" %s' %
                       (wheel_filepath, extra_args), cwd=temp_root)

    if zip_filepath:
        subprocess.run('twine upload "%s" %s' %
                       (zip_filepath, extra_args), cwd=temp_root)

if script_test:
    print("temp_root: ", temp_root)


uname = pword = None
if not script_test:
    uname = input("Please enter your PyPi username: ")
    pword = input("Please enter your PyPi password: ")

# make the meke
print("Building MEKE...")
try:
    # run the build script
    subprocess.run(meke_build_script, cwd=os.path.dirname(meke_build_script))
    exe_path = None
    for root, _, files in os.walk(meke_dir):
        for filename in files:
            if os.path.splitext(filename)[-1].lower() == ".exe":
                exe_path = os.path.realpath(os.path.join(root, filename))
        break

    if exe_path:
        shutil.copy(exe_path, os.path.join(os.curdir, os.path.basename(exe_path)))
except shutil.SameFileError:
    pass
except Exception:
    input(traceback.format_exc())
    raise


# make the prebuilt mek
print("Making prebuilt MEK...")
try:
    mek_zipfile_path, _ = request.urlretrieve(mek_download_url)
    mek_lib_dir = os.path.join(prebuilt_mek_dir, "mek_lib")

    # make sure the build directory is clean.
    try: shutil.rmtree(prebuilt_mek_dir)
    except FileNotFoundError: pass
    unzip_zipfile(mek_zipfile_path, prebuilt_mek_dir, True)

    for root, dirs, files in os.walk(prebuilt_mek_dir):
        for fname in files:
            test_name = fname.lower().replace(" ", "").replace("_", "")
            if ("buildtools.exe" in test_name or "getpip.py" in test_name or
                "installinstructions.txt" in test_name):
                os.remove(os.path.join(root, fname))

        break

    # copy the contents of each module into the mek_lib directory.
    for module_name in mek_modules:
        exec("import %s as module" % module_name)
        print("Copying %s" % module_name)
        copy_module_files(os.path.dirname(module.__file__),
                          os.path.join(mek_lib_dir, module_name))

    print("Creating latest release zipfile...")
    with zipfile.ZipFile(prebuilt_mek_zip_path, mode='w') as zf:
        for root, _, files in os.walk(prebuilt_mek_dir):
            for filename in sorted(files):
                filepath = os.path.join(root, filename)
                rel_filepath = os.path.relpath(filepath, prebuilt_mek_dir)
                zf.write(filepath, arcname=rel_filepath)

    if not script_test:
        try: shutil.rmtree(prebuilt_mek_dir)
        except (FileNotFoundError, OSError): pass
except Exception:
    input(traceback.format_exc())
    raise


# do the pypi uploads
print("Doing PyPi uploads...")
for module_name in mek_modules:
    try:
        exec("import %s as module" % module_name)
        print("Uploading %s" % module_name)
        if module_name == "arbytmap":
            egg = wheel = False
            source = True
        else:
            egg = wheel = True
            source = False

        pypi_upload(os.path.dirname(module.__file__),
                    egg, wheel, source, username=uname, password=pword)
    except Exception:
        input(traceback.format_exc())
        raise

input("Finished...")
