from networking_server import *
from hash import *
import threading
import sys

port = int(input("Port: "))
key = input("Auth Key: ")
if key == "":
    s = server(port, None)
else:
    s = server(port, hash(key))
recv_thread = threading.Thread(target=s.recv, args=(1024,), daemon=True)
timeout_thread = threading.Thread(target=s.userTimeout, daemon=True)
recv_thread.start()
timeout_thread.start()
while True:
    i = input().lower()
    if i == "/stop" or i == "stop":
        break
