/*
  I kind of don't want to do any of this. I'd like maybe .bat scripts because
  we're basically writing a C program that can just be a set of shell commands.

  But our users expect this at this point.
  So we got to satisfy then with their icons and stuff.
*/

#include <windows> // MessageBox()
#include <stdlib.h> // system()

#define PYTHON_EXE "mek_python\\python.exe"

#define MEK_INSTALL_PATH mek_python\\mek
#define UPDATER_PATH MEK_INSTALL_PATH\\MEK_Installer.py
#define ESSENTIALS_VERSION 2.0.0.0
#define UPDATER_ARGS --install-dir MEK_INSTALL_PATH \
                     --disable-uninstall-btn \
                     --essentials-version ESSENTIALS_VERSION

#define ERROR_PYTHON_NOT_FOUND 100
#define ERROR_SCRIPT_CRASH 101

#define RUN_SHELL system

static inline int python_check() {
    if(RUN_SHELL("PYTHON_EXE -c \"import sys; sys.exit(0)\"")) {
        MessageBox(NULL,
            "Couldn't load Python from mek_python directory. "
            "Make sure that you are running PROGRAM_NAME from "
            "the same directory that contains mek_python.\n\n"
            "Reinstalling should fix this error.",

            "Error Loading Python.",
            MB_OK | MB_ICONERROR
        );
        return 1;
    }
    return 0;
}

static inline int run_module() {
    if(RUN_SHELL("PYTHON_EXE -m PROGRAM_NAME ARGUMENTS")) {
        MessageBox(NULL,
            "PROGRAM_NAME closed with an error. "
            "If this happened before it showed up try reinstalling or running "
            "the updater. You can also debug it using startup_crash.log.\n\n "
            "You can also request help in the"
            "#mek-discussion channel in the CE Reclaimers Discord server.",

            "Error.",
            MB_OK | MB_ICONERROR
        );
        return 1;
    }
    return 0;
}

static inline int run_updater() {
    if(RUN_SHELL("PYTHON_EXE UPDATER_PATH")) {
        MessageBox(NULL,
            "Updater closed with an error. "
            "If this happened before it showed up try reinstalling.\n\n "
            "You can also request help in the"
            "#mek-discussion channel in the CE Reclaimers Discord server.",

            "Error.",
            MB_OK | MB_ICONERROR
        );
        return 1;
    }
    return 0;
}
