import socket
from user_class import *

class server:
    def __init__(self, UDP_PORT):
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = UDP_PORT
        self.ADDRESS = (self.IP, self.PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.ADDRESS)
        self.users = [] # classes with data inside
        print(self.IP, self.PORT)
    def recv(self, recv_bytes):
        while True:
            data, address = self.sock.recvfrom(recv_bytes)
            print(data, address)
    def broadcast(self, packetType, msg):
        self.sock.sendto(packetType + "|" + msg.encode("utf-8"), self.ADDRESS)
    def sendToSingle(self, msg, username):
        print("not implemented")
