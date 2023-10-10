import socket
from websocket import create_connection


def get_local_ip_address(target):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((target, 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


client_ip = get_local_ip_address('192.168.1.210')
ws = create_connection("ws://192.168.1.210:8888/websocket")

ws.send(f"Hello, je suis le client dont l'adresse IP est: {client_ip}")

result1 = ws.recv()
print(f"Reçu '{result1}'")

result2 = ws.recv()
print(f"Reçu '{result2}'")

ws.close()
