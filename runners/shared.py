import subprocess
import sys
import os

from os import path
from traceback import format_exc

ESSENTIALS_VERSION = "2.0.0"

MEKE_FOLDER = path.dirname(sys.executable)
PY_EXE  = path.join(MEKE_FOLDER, "mek_python", "python.exe")
PYW_EXE = path.join(MEKE_FOLDER, "mek_python", "pythonw.exe")
UPDATER_FILE = path.join(MEKE_FOLDER, "mek_python", "mek", "MEK_Installer.pyw")

FILE_NOT_FOUND_TEMPL = (
    "Couldn't load Python from mek_python directory. "
    "Make sure that you are running %s from the same "
    "directory that contains mek_python.\n\nReinstalling the MEK "
    "Essentials should fix this error.")

UNKNOWN_TEMPL = (
    "Error %s while trying to run %s.\n\nDetails:\n%s\n\nReinstalling the MEK "
    "Essentials might fix this error.")

def execute_module(module_name, console_enabled):
    py_exe = PY_EXE if console_enabled else PYW_EXE
    try:
        subprocess.Popen([
            py_exe, "-m", module_name, *sys.argv[1: ]]).returncode
        sys.exit(0)
    except FileNotFoundError:
        subprocess.run(["msg", os.getlogin(),
            FILE_NOT_FOUND_TEMPL % (module_name)])
        sys.exit(1)
    except Exception as e:
        subprocess.run(["msg", os.getlogin(),
            UNKNOWN_TEMPL % (e, module_name, format_exc())])
        sys.exit(1)

def execute_updater():
    module_name = "MEK_Updater"
    try:
        subprocess.Popen([
            PYW_EXE, UPDATER_FILE,
            "--install-dir", "mek_python/mek",
            "--disable-uninstall-btn",
            "--essentials-version", ESSENTIALS_VERSION,
            "--meke-dir", MEKE_FOLDER]).returncode
        sys.exit(0)
    except FileNotFoundError:
        subprocess.run(["msg", os.getlogin(),
            FILE_NOT_FOUND_TEMPL % (module_name)])
        sys.exit(1)
    except Exception as e:
        subprocess.run(["msg", os.username,
            UNKNOWN_TEMPL % (e, module_name, format_exc())])
        sys.exit(1)
