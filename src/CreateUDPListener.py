import socket
from Packets import Packets


class UDPListener:
    def __init__(self, udp_ip, udp_port):
        self.UDP_IP = udp_ip
        self.UDP_PORT = udp_port
        self.packet = Packets()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))

    def startUDPListener(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            data = data.decode().strip()
            print("addr:", addr)
            self.packet.set(info=data, ip=addr[0], port=addr[1])
