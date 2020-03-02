#define PROGRAM_NAME "refinery"
#define ARGUMENTS ""
#include "shared.h"

int main() {
    if (python_check()) return ERROR_PYTHON_NOT_FOUND;
    if (run_module()) return ERROR_SCRIPT_CRASH;
    return 0;
}
