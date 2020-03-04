@echo off
if exist mek_python\pythonw.exe (
    start mek_python\pythonw.exe -m hek_pool %*
) else (
    start msg %username% "Couldn't load Python from mek_python directory. Make sure that you are running Pool from the same directory that contains mek_python.    Reinstalling should fix this error."
)
