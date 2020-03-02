#define PROGRAM_NAME MEK_Updater
#define ARGUMENTS ""
#define UPDATER_PATH "mek_python\\mek\\MEK_Installer.py"
#define ESSENTIALS_VERSION 2.0.0.0
#define UPDATER_ARGS

#include <windows> // MessageBox()
#include <stdlib.h> // system()

#define PYTHON_EXE "mek_python\\python.exe"

#define ERROR_PYTHON_NOT_FOUND 100
#define ERROR_SCRIPT_CRASH 101

int main() {
    if(system("PYTHON_EXE -c \"import sys; sys.exit(0)\"")) {
        MessageBox(NULL,
            "Couldn't load Python from mek_python directory. "
            "Make sure that you are running PROGRAM_NAME from "
            "the same directory that contains mek_python.\n\n"
            "Reinstalling should fix this error.",

            "Error Loading Python.",
            MB_OK | MB_ICONERROR
        );
        return ERROR_PYTHON_NOT_FOUND;
    }
    if(system("PYTHON_EXE UPDATER_PATH")) {
        MessageBox(NULL,
            "PROGRAM_NAME closed with an error. "
            "If this happened before it showed try reinstalling or running "
            "the updater. You can also debug it using startup_crash.log.\n\n "
            "You can also request help in the"
            "#mek-discussion channel in the CE Reclaimers Discord server.",

            "Error.",
            MB_OK | MB_ICONERROR
        );
        return ERROR_SCRIPT_CRASH;
    }
    return 0;
}
