@echo off
ESSENTIALS_VERSION=2.0.0
if exist mek_python\pythonw.exe (
    start mek_python\pythonw.exe mek_python\\mek\\MEK_Installer.pyw --install-dir mek_python\\mek --disable-uninstall-btn --essentials-version %ESSENTIALS_VERSION%
) else (
    start msg %username% "Couldn't load Python from mek_python directory. Make sure that you are running Update_MEK from the same directory that contains mek_python.    Reinstalling should fix this error."
)
