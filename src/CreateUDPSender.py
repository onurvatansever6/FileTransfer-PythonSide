import socket


class UDPSender:
    def __init__(self):
        self.target_ip = None
        self.target_port = None
        self.sock = None

    def create(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message):
        self.sock.sendto(message.encode(), (self.target_ip, self.target_port))

    def close(self):
        self.sock.close()
