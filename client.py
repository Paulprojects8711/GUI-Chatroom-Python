"""
    GUI-Chatroom-Python  An end-to-end encrypted Graphical User Interface Chatroom but remade in Python
    Copyright (C) 2026  Paul8711

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
