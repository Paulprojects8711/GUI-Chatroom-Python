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

import socket
import json
import time
from hash import *
from user_class import *
from helpers import *

class server:
    def __init__(self, UDP_PORT, AUTH_KEY):
        try:
            self.IP = socket.gethostbyname(socket.gethostname())
            self.PORT = UDP_PORT
            self.KEY = AUTH_KEY
            self.SALT = genSalt(32)
            self.ADDRESS = ('0.0.0.0', self.PORT) # if not 0.0.0.0 connection refuses if you use localhost on client
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(self.ADDRESS)
            self.users = [] # classes with data inside
            print(f"Server started on Port {self.PORT}")
        except Exception as e:
            print("Error:", e)
            quit()

    def recv(self, recv_bytes):
        try:
            while self.sock != None:
                data, address = self.sock.recvfrom(recv_bytes)

                if len(data) > 6:
                    if data[:6] == b"voice|":
                        self.broadcastVoice(address, data)
                        continue

                print(f"Received packet: {data}")
                splitData = data.decode("utf-8").split("|", 1)
                packetType = splitData[0]
                packetData = splitData[1]

                if packetType == "join":
                    inUse = False
                    for u in self.users:
                        if packetData == u:
                            self.sendToSingle(address, "err|" + "Username already in use")
                            inUse = True
                            break

                    if not inUse:
                        self.users.append(user(packetData, address, milli_time(), "", False, False, False))
                        if self.KEY != None:
                            self.sendToSingle(address, "auth|request")
                        else:
                            print(f"User {packetData} joined")
                            self.sendToSingle(address, "salt|" + self.SALT)
                            self.broadcast(f"join|User {packetData} joined")
                            self.broadcastUserList()
                            self.broadcastVCUsers()

                elif packetType == "auth":
                    if not verify(packetData,self.KEY):
                        u, loops = self.getUserByAddress(address)
                        assert u != None, "User is None"
                        print(f"User {u.name} got the auth key wrong")
                        self.sendToSingle(u.address, "auth|wrong")
                        del self.users[loops]
                    else:
                        u, loops = self.getUserByAddress(address)
                        assert u != None, "User is None"
                        self.sendToSingle(u.address, "auth|ok")
                        print(f"User {u.name} joined")
                        self.sendToSingle(address, "salt|" + self.SALT)
                        self.broadcast(f"join|User {u.name} joined")
                        self.broadcastUserList()
                        self.broadcastVCUsers()
            
                elif packetType == "chat":
                    u, loops = self.getUserByAddress(address)
                    assert user != None, "User is None"
                    u.lastSeen = milli_time()
                    print(f"{u.name}: {packetData}")
                    self.broadcast(f"chat|{u.name}: {packetData}")

                elif packetType == "leave":
                    u, loops = self.getUserByAddress(address)
                    assert u != None, "User is None"
                    del self.users[loops]
                    self.broadcast(f"User {u.name} left")
                    self.broadcastUserList()
                    self.broadcastVCUsers()

                elif packetType == "ping":
                    u, loops = self.getUserByAddress(address)
                    assert u != None, "User is None"
                    u.lastSeen = milli_time()
                    self.sendToSingle(u.address, "pong|")

                elif packetType == "vc":
                    if packetData == "join":
                        u, loops = self.getUserByAddress(address)
                        assert u != None, "User is None"
                        u.inVC = True
                        self.broadcast(f"info|User {u.name} joined Voice call")
                        self.broadcastVCUsers()

                    elif packetData == "leave":
                        u, loops = self.getUserByAddress(address)
                        assert u != None, "User is None"
                        u.inVC = False
                        self.broadcast(f"info|User {u.name} left Voice call")
                        self.broadcastVCUsers()

                    elif packetData == "mute":
                        u, loops = self.getUserByAddress(address)
                        assert u != None, "User is None"
                        u.mute = not u.mute
                        self.broadcastVCUsers()

                    elif packetData == "deaf":
                        u, loops = self.getUserByAddress(address)
                        assert u != None, "User is None"
                        u.deaf = not u.deaf
                        self.broadcastVCUsers()
        except Exception as e:
            print("Error:", e)
            quit()

    def broadcast(self, msg):
        packet = msg.encode("utf-8")
        for u in self.users:
            self.sock.sendto(packet, u.address) # loops through all classes in the user list and sends the packet to every user
    
    def sendToSingle(self, clientID, msg):
        self.sock.sendto(msg.encode("utf-8"), clientID)
        for u in self.users:
            if u.address == clientID:
                u.lastSent = msg # so the user doesnt get kicked while waiting for auth answer

    def broadcastVCUsers(self):
        vcList = []
        loops = 0
        for u in self.users:
            if u.inVC:
                vcUser = {"username": u.name, "mute": u.mute, "deaf": u.deaf}
                vcList.append(vcUser)
            loops += 1

        print(vcList)

        self.broadcast("vcusers|" + json.dumps(vcList))

    def broadcastUserList(self):
        userList = []
        loops = 0
        for u in self.users:
            userList.append(u.name)
            loops += 1

        print(userList)

        self.broadcast("users|" + json.dumps(userList))

    def broadcastVoice(self, senderID, sendData):
        for u in self.users:
            if u.inVC and u.address != senderID:
                self.sock.sendto(sendData, u.address)

    def stop(self, reason):
        try:
            if self.sock != None:
                self.sock.close()
                self.sock = None
        except Exception as ignored:
            pass

    def getUserByAddress(self, address):
        loops = 0
        for u in self.users:
            if u.address == address:
                return u, loops
            loops += 1
        return None, loops

    def userTimeout(self):
        try:
            while self.sock != None:
                time.sleep(5)
                if self.sock == None: break
                now = milli_time()
                loops = 0
                for u in self.users:
                    if now - u.lastSeen > 15000:
                        lastMessage = u.lastSent
                        if lastMessage == "auth|request":
                            # dont kick
                            u.lastSeen = milli_time()
                            continue

                        username = u.name
                        del self.users[loops]
                        self.broadcast(f"leave|{username} disconnected (timeout)")
                        self.broadcastUserList()
                        self.broadcastVCUsers()
        except Exception as e:
            print(e)
            quit()
