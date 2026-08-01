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
        quit()
