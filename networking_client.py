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

from default_key import *
from helpers import *
from encrypt import *
import socket
import json

class client:
    def __init__(self, UDP_IP, UDP_PORT, USERNAME):
        self.IP = socket.gethostbyname(UDP_IP) # gethostbyname for example converts localhost to 127.0.0.1
        self.PORT = UDP_PORT
        self.ADDRESS = (self.IP, self.PORT) # saves the address tuple to a variable
        self.NAME = USERNAME
        self.DEFAULT_KEY = DefaultKeyManager.get_default_key().get("key")
        self.KEY = None
        self.SALT = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # creates the socket for UDP
        self.sock.settimeout(5.0) # 5 sec timeout
        self.sock.connect(self.ADDRESS) # connects to the remote socket
        print(f"Connected to {self.IP} on Port {self.PORT}")
        self.send("join", self.NAME)

        authRequestReceived = False
        start = milli_time()
        waitTimeoutMs = 10000 # 10 s timeout for salt
        while self.SALT == None and self.sock != None:
            try:
                data = self.sock.recv(1024).decode("utf-8")
                time.sleep(0.05)

                if data != None:
                    if data == "auth|request":
                        authRequestReceived = True
                        start = milli_time()
                        self.KEY = input("Enter Auth Key: ")
                        self.send("auth", self.KEY)
                    elif data == "auth|wrong":
                        authRequestReceived = False
                        start = milli_time()
                        print(self.stop("Wrong Auth Key"))
                        quit()
                    elif data == "auth|ok":
                        authRequestReceived = False
                        print("Auth OK")
                    elif data.split("|")[0] == "salt":
                        self.SALT = data.split("|")[1]
                        if self.KEY == None: self.KEY = ""
                else:
                    if not authRequestReceived and milli_time() - start  > waitTimeoutMs and self.sock != None:
                        print(disconnect("Server Timeout"))
                        quit()
            except Exception as e:
                print("Error:", e)
                quit()

    def recv(self):
        try:
            while self.sock != None: # for thread (multithreading)
                data = self.sock.recv(1024).decode("utf-8") # receives data from whoever sends it
                # filters the type of the received data
                splitData = data.split("|", 1) # splits at the seperator (<type>|<data>)
                packetType = splitData[0]
                if len(splitData) >= 2: # if it is less than two error happened
                    data = splitData[1]
                    if packetType == "chat":
                        splitMSG = data.split(": ", 1)
                        msg = splitMSG[1]
                        sender = splitMSG[0] + ": "
                        if self.KEY == "" or self.KEY == None: key = self.DEFAULT_KEY
                        else: key = self.KEY
                        print(sender + decrypt(msg, self.SALT, key))
                    elif packetType == "err":
                        self.sock.close()
                        self.sock = None
                        self.SALT = None
                        self.KEY = None
                        if data == "Username already in use":
                            print(data)
                        else:
                            print("Error:", data)
                    elif packetType == "vcusers":
                        vc_list = json.loads(data)

                        vc_user_list = []

                        for user_obj in vc_list:
                            username = user_obj.get("username", "")
                            mute = bool(user_obj.get("mute"))
                            deaf = bool(user_obj.get("deaf"))

                            display = username

                            if mute:
                                display += " [M]"
                            if deaf:
                                display += " [D]"

                            vc_user_list.append(display)
                        
                        print("Voice Chat Users")
                        print(", ".join(vc_user_list))
                    elif packetType == "users":
                        u_list = json.loads(data)
                        u_list.sort()
                        print("Users")
                        print(", ".join(u_list))
                    elif packetType == "info":
                        print(data)

        except Exception as e:
            print("Error:", e)
            quit()

    def send(self, packetType, msg):
        try:
            packet = (packetType + "|" + msg).encode("utf-8")
            if len(packet) > 1024:
                if packetType == "chat":
                    print("Message too long")
                    return
                else:
                    print("Packet too big")
                    return
            self.sock.sendto(packet, self.ADDRESS) # sends msg to the remote socket
        except Exception as e:
            print("Error:", e)
            quit()
    
    def ping(self):
        try:
            while self.sock != None:
                time.sleep(5)
                if self.sock == None: break
                self.send("ping", "")
        except Exception as e:
            print("Error:", e)
            quit()

    def disconnect(self, reason):
        self.send("leave", self.NAME)
        self.sock.close() # close the socket what do you expect
        self.sock = None
        self.SALT = None
        self.KEY = None
        return reason
