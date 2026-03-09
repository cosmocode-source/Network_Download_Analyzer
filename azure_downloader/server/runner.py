import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
from config import TEST_SERVERS
from execution.geo import get_server_ip
from execution.latency import measure_latency
from execution.tcp_handshake import measure_tcp_handshake
from execution.metrics import compute_metrics
from execution.downloader import download_file
from storage.data_formatter import build_record
from storage.db_writer import save_metrics

EXPECTED_SIZE = 100 * 1024 * 1024   # 100MB


def run_test():

    MAX_RETRIES = 3
    MAX_SUCCESS = 3

    print("===== TEST START =====")
    print("Time:", datetime.datetime.now(datetime.UTC))

    success_count = 0

    for server in TEST_SERVERS:

        if success_count >= MAX_SUCCESS:
            print("\nReached 3 successful measurements. Stopping test.")
            break

        url = server["url"]
        print("\nTesting:", server["name"])

        ip, scheme = get_server_ip(url)
        port = 443 if scheme == "https" else 80

        retries = 0

        while retries < MAX_RETRIES:

            latency = measure_latency(ip)
            handshake = measure_tcp_handshake(ip, port)

            download_data = download_file(url)

            if download_data and download_data["bytes_downloaded"] == EXPECTED_SIZE:

                metrics = compute_metrics(download_data)

                record = build_record(server, ip, latency, handshake, metrics)

                save_metrics(record)

                print("Saved:", record)

                success_count += 1
                break

            else:

                retries += 1
                print(f"Incomplete download. Retry {retries}/3")

        if retries == MAX_RETRIES:
            print("Server failed after 3 attempts. Moving to next server.")


if __name__ == "__main__":
    run_test()