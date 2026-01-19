from networking_server import *
import threading

port = int(input("Port: "))
s = server(port)
recv_thread = threading.Thread(target=s.recv, args=(1024,), daemon=True)
recv_thread.start()
s.broadcast("hi")
while True:
    pass
