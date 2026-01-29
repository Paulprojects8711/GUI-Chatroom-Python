from networking_client import *
from encrypt import *
import threading

ip = input("IP: ")
port = int(input("Port: "))
username = input("Username: ")
if username == "":
    print("Username cannot be empty")
    quit()
c = client(ip, port, username)

ping_thread = threading.Thread(target=c.ping, daemon=True)
recv_thread = threading.Thread(target=c.recv, daemon=True)
ping_thread.start()
recv_thread.start()

while c.sock != None:
    i = input()
    if i.lower() == "/leave" or i.lower() == "leave":
        c.send("leave", c.NAME)
        c.sock.close()
        quit()
    else:
        if c.KEY == "" or c.KEY == None: key = c.DEFAULT_KEY
        else: key = c.KEY
        c.send("chat", encrypt(i, c.SALT, key))
