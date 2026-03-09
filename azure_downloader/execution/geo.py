from urllib.parse import urlparse
import socket

def get_server_ip(url):
    parsed = urlparse(url)
    hostname = parsed.hostname
    ip = socket.gethostbyname(hostname)
    scheme = parsed.scheme
    return ip, scheme