import datetime
from config import CLIENT_NODE_NAME

def build_record(server, ip, latency, handshake, metrics):
    record = {
        "timestamp": datetime.datetime.utcnow(),
        "client_node": CLIENT_NODE_NAME,
        "server_name": server["name"],
        "server_url": server["url"],
        "server_ip": ip,
        "latency_ms": latency,
        "tcp_handshake_ms": handshake,
        "file_size_MB": metrics["file_size_MB"],
        "download_time_sec": metrics["download_time_sec"],
        "throughput_Mbps": metrics["throughput_Mbps"],
        "transfer_variance": metrics["transfer_variance"],
        "chunk_count": metrics["chunk_count"]
    }
    return record