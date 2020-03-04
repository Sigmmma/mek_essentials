@echo off
if exist mek_python\python.exe (
    start mek_python\python.exe -m refinery %*
) else (
    start msg %username% "Couldn't load Python from mek_python directory. Make sure that you are running Refinery from the same directory that contains mek_python.    Reinstalling should fix this error."
)
