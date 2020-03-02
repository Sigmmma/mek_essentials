#define PROGRAM_NAME MEK_Updater
#define ARGUMENTS ""
#include "shared.h"

int main() {
    if (python_check()) return ERROR_PYTHON_NOT_FOUND;
    if (run_updater()) return ERROR_SCRIPT_CRASH;
    return 0;
}
