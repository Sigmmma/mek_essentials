python "%~dp0build_meke.py" build -b "%~dp0.."

echo Cleaning extraneous files and folders...
python "%~dp0exe_lib_cleaner.py" "%~dp0..\exe.win-amd64-3.5"
