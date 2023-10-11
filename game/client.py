# client.py

import socket

from websocket import create_connection
from datetime import datetime


class WebSocketClient:
    def __init__(self, target):
        self.target = target
        self.ws = None

    def get_local_ip_address(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect((self.target, 1))
            IP = sock.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            sock.close()
        return IP

    def connect(self):
        self.ws = create_connection(f"ws://{self.target}:8888/websocket")
        client_ip = self.get_local_ip_address()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Reçu sur le serveur.
        self.ws.send(
            f"Depuis le fichier client.py: {current_time}, adresse IP: {client_ip}")

    def receive(self):
        return self.ws.recv()

    def close(self):
        self.ws.close()
