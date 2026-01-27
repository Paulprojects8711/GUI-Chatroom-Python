from networking_client import *
import threading

ip = input("IP: ")
port = int(input("Port: "))
username = input("Username: ")
if username == "":
    print("Username cannot be empty")
    quit()
c = client(ip, port)
c.send("join", username)
c.send("chat", input("send what: "))

recv_thread = threading.Thread(target=c.recv, args=(1024,), daemon=True)
recv_thread.start()

while True:
    pass
