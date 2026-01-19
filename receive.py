import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 1234

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data = sock.recv(1024).decode("utf-8") #  buffer size is 1024 bytes
    print("received message: %s" % data)
