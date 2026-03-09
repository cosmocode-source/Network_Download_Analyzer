from ping3 import ping
from config import PING_COUNT

def measure_latency(host):
    latencies = []
    for _ in range(PING_COUNT):
        delay = ping(host, timeout=2)
        if delay is not None:
            latencies.append(delay * 1000)

    if not latencies:
        return None

    avg_latency = sum(latencies) / len(latencies)
    return round(avg_latency, 2)