import subprocess

from urllib import request

# Download innosetup.
innosetup, _ = request.urlretrieve("http://files.jrsoftware.org/is/6/innosetup-6.0.3.exe")

# Install innosetup hands off.
subprocess.run([innosetup, "/SP-", "/VERYSILENT", "/SUPPRESSMSGBOXES"])

# Make an installer.
subprocess.run([
    "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe",
    "meke_installer.iss"])
