import socket
import os

HOST = input("IP: ")
port = 65432
s = socket.socket()

s.connect((HOST, port))
while True:
    fileinfo = s.recv(1024).decode().split("//")
    filename = fileinfo[0]
    filesize = fileinfo[1]
    print(f"Recived: Filename:{filename} Filesize:{filesize} Bytes")
    if len(filename) > 0:
        with open(filename, 'wb') as f:
            while True:
                data = s.recv(4096)
                if data == b"__':;END_OF_FILE;:'__":
                    print("Downloaded")
                    filename = ""
                    break
                f.write(data)
