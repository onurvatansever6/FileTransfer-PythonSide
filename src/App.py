import asyncio
import socket
import threading
import time

from src.CreateUDPListener import UDPListener
from src.CreateUDPSender import UDPSender
from src.WebsocketClient import WebSocketServer


class App:
    def __init__(self):
        self.pcName = socket.gethostname()
        self.pcIP = socket.gethostbyname(self.pcName)
        self.privateSender = UDPSender()
        self.serverWebSocketPort = 3232
        self.serverWebSocket = WebSocketServer(self.pcIP, self.serverWebSocketPort)

    def applicationStart(self):
        print(self.pcIP, self.serverWebSocketPort)
        globalListener = UDPListener(udp_ip="0.0.0.0", udp_port=5000)
        t_globalListener = threading.Thread(target=globalListener.startUDPListener)
        t_globalListener.start()

        while True:
            if globalListener.packet.isUpdated:
                lastPacket = globalListener.packet
                payload = lastPacket.received_message_info
                print(f"Payload = {payload}")
                if payload == "WHO":
                    # send private socket created info from private sender to remote ip
                    self.privateSender.create(target_ip=lastPacket.received_message_ip,
                                              target_port=lastPacket.received_message_port)

                    self.privateSender.send(f"{self.pcName}:{self.pcIP}")
                    print("I sent my PCNAME and PCIP")
                    self.privateSender.close()

                if payload == "CONNECT":
                    print("connect side")
                    # create private websocket
                    t_websocketListener = threading.Thread(target=asyncio.run(self.serverWebSocket.run()))
                    t_websocketListener.start()
                    print("websock list. started")
                    while not self.serverWebSocket.finish:
                        print("wait connect ")
                        time.sleep(0.1)
                    t_websocketListener.join()
                    t_websocketListener = None

                elif lastPacket.received_message_info == "PRIVATE":
                    privateListener = UDPListener(lastPacket.received_message_ip,
                                                  lastPacket.received_message_port)
                    t_privateListener = threading.Thread(target=privateListener.startUDPListener)
                    t_privateListener.start()

                    privateLastIP = privateListener.packet.received_message_ip
                    privateLastPort = privateListener.packet.received_message_port

                    print(f"{privateLastIP}:{privateLastPort}")

                globalListener.packet.isUpdated = False
                print("packet restore")
            # wait
            time.sleep(0.5)


application = App()
application.applicationStart()
