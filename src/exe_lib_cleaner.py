import os, shutil, sys
from traceback import format_exc

replacements = {
    '.cpython-35': '',
    }
cur_dir = os.path.dirname(__file__)
op_dir = cur_dir
if len(sys.argv) > 1:
    op_dir = sys.argv[1]

try:
    for root, dirs, files in os.walk(os.path.abspath(op_dir)):
        for folder in dirs:
            if folder.lower() in (
                    ".hg", ".vs", "styles", "docs", "test_files", "x64",
                    "arbytmap_ext", "bitmap_io_ext", "dds_defs_ext",
                    "raw_packer_ext", "raw_unpacker_ext", "swizzler_ext"):
                shutil.rmtree(os.path.join(root, folder))

        for filename in files:
            if cur_dir in os.path.join(root, filename):
                continue

            if filename.lower() in ("readme.md", "readme.rst", "readme.txt",
                                    "todo.txt", ".hgignore", "license.txt"):
                os.remove(os.path.join(root, filename))

            if os.path.splitext(filename)[-1] in (
                    ".log", ".sln", ".db", ".user", ".filters", ".vcxproj"):
                os.remove(os.path.join(root, filename))

            new_filename = filename
            for string in replacements:
                new_filename = new_filename.replace(string, replacements[string])

            if new_filename == filename:
                continue
            else:
                os.rename(os.path.join(root, filename),
                          os.path.join(root, new_filename))
except Exception:
    print(format_exc())
input("Finished")
