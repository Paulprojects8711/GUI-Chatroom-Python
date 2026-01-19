from networking_client import *
import threading

ip = input("IP: ")
port = int(input("Port: "))
username = input("Username: ")
c = client(ip, port)
c.send(input("send what: "))
print(c.close("test"))

recv_thread = threading.Thread(target=c.recv, args=(1024,), daemon=True)
recv_thread.start()

while True:
    pass
