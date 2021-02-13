from time import sleep
import socket
import ntpath
import os

HOST = input("IP: ")
PORT = 65432
s = socket.socket()

s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
print(f"{addr} Connected.")
while True:
    filename = input("File: ")
    if os.path.exists(filename) == False:
        print("File not found.")
        continue
    conn.send(f"{ntpath.basename(filename)}//{os.path.getsize(filename)}".encode())
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                sleep(3)
                conn.send(b"__':;END_OF_FILE;:'__")
                break
            conn.send(chunk)
