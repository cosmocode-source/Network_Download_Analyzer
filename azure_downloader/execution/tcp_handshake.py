import socket
import time

def measure_tcp_handshake(host, port):
    start = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((host, port))
    except:
        sock.close()
        return None
    end = time.time()
    sock.close()
    return round((end - start) * 1000, 2)