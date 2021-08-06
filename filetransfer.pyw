import tkinter.filedialog as fd
import threading
from tkinter import *
import os
import time
import socket

def clear(listbox):
    listbox.delete(0,END)

def get_filez(root,listbox):
    global filez
    filez = fd.askopenfilenames(parent=root, title='Choose a file')
    for values in filez:
        listbox.insert(END, values)
    return

def recv(root,listbox,port_entry,ip_entry):
    lable = Label(root,text="Listening for connections...")
    lable.grid(row=5,column=0,columnspan=3)

    recvd = []
    sock = socket.socket()
    sock.bind((ip_entry.get(),int(port_entry.get())))
    sock.listen()
    conn,addr = sock.accept()
    lable['text'] = "Connected: " + addr[0]
    lable.grid(row=5,column=0,columnspan=3)
    
    amount_of_files = int(conn.recv(1024).decode())
    for _ in range(0,int(amount_of_files)):
        try:
            filename = conn.recv(1024).decode()
            lable['text'] = filename
            lable.grid(row=5,column=0,columnspan=3)
            with open(filename,"wb") as outfile:
                while True:
                    data = conn.recv(1024)
                    if data == b"!__END_OF_TRANSFER__!":
                        break
                    else:
                        outfile.write(data)
        except:
            lable['text'] = "Error transfering file."
            lable.grid(row=5,column=0,columnspan=3)
        listbox.insert(END,os.path.abspath(filename))
        
    sock.close()
    lable["text"] = "Done."
    lable.grid(row=5,column=0,columnspan=3)
    return


def send(root,listbox,port_entry,ip_entry):
    lable = Label(root,text="Connecting...")
    lable.grid(row=5,column=0,columnspan=3)
    items = list(listbox.get(0,END))
    sock = socket.socket()
 
    while True:
        try:
            sock.connect((ip_entry.get(),int(port_entry.get())))
            break
        except ConnectionRefusedError:
            continue
    
    lable["text"] = "Connection succesful."
    lable.grid(row=5,column=0,columnspan=3)

    time.sleep(1)
    sock.send(str(len(items)).encode())
    for file in items:
        lable["text"] = os.path.basename(file)
        lable.grid(row=5,column=0,columnspan=3)
        time.sleep(0.1)
        sock.send(os.path.basename(file).encode())
        time.sleep(0.1)
        with open(file,"rb") as infile:
            while True:
                out = infile.read(1024)
                if len(out) > 0:
                    sock.send(out)
                else:
                    time.sleep(1)
                    sock.send(b"!__END_OF_TRANSFER__!")
                    break
    sock.close()
    lable["text"] = "Done."
    lable.grid(row=5,column=0,columnspan=3)
    return


root = Tk()
root.resizable(False,False)
root.title("File transfer")

filez = []

listbox = Listbox(width=50)

ip_label = Label(text="Ip address")
port_lable = Label(text="Port")
ip_entry = Entry()
port_entry = Entry()
send_thread = threading.Thread(target=lambda:send(root,listbox,port_entry,ip_entry))
recv_thread = threading.Thread(target=lambda:recv(root,listbox,port_entry,ip_entry))
get_button = Button(width=20,text="Choose files(s)",command = lambda: get_filez(root,listbox))
send_button = Button(width=20,text="Send",command = lambda:send_thread.start())
recv_button = Button(width=20,text="Recieve",command = lambda:recv_thread.start())
clear_button = Button(width=20,text="Clear",command = lambda:clear(listbox))

ip_label.grid(row=0,column=0)
ip_entry.grid(row=1,column=0)
port_lable.grid(row=0,column=1)
port_entry.grid(row=1,column=1)
send_button.grid(row=2,column=0)
recv_button.grid(row=2,column=1)
listbox.grid(row=3,column=0,columnspan=2)
get_button.grid(row=4,column=0)
clear_button.grid(row=4,column=1)

root.mainloop()
