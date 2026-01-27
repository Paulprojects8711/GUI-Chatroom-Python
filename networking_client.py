import socket

class client:
    def __init__(self, UDP_IP, UDP_PORT):
        self.IP = socket.gethostbyname(UDP_IP) # gethostbyname for example converts localhost to 127.0.0.1
        self.PORT = UDP_PORT
        self.ADDRESS = (self.IP, self.PORT) # saves the address tuple to a variable
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # creates the socket for UDP
        self.sock.settimeout(15.0) # 15 sec timeout
        self.sock.connect(self.ADDRESS) # connects to the remote socket
        print(self.IP)

    def recv(self, recv_bytes):
        while True: # for thread (multithreading)
            data = self.sock.recv(recv_bytes).decode("utf-8") # receives data from whoever sends it
            # filters the type of the received data
            splitData = data.split("|", 1) # splits at the seperator (<type>|<data>)
            packetType = splitData[0]
            if len(splitData) >= 2: # if it is less than two error happened
                data = splitData[1]
                if packetType == "chat":
                    print(data)
    def send(self, packetType, msg):
        self.sock.sendto((packetType + "|" + msg).encode("utf-8"), self.ADDRESS) # sends msg to the remote socket
    
    def close(self, reason):
        self.sock.close() # close the socket what do you expect
        self.sock = None
        return reason
