import requests
import time
from config import DOWNLOAD_CHUNK_SIZE

EXPECTED_SIZE = 100 * 1024 * 1024   # 100MB

def download_file(url):

    try:
        start = time.time()

        response = requests.get(url, stream=True, timeout=15)

        total_bytes = 0
        chunk_intervals = []

        last_time = time.time()

        for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):

            if chunk:
                total_bytes += len(chunk)

                now = time.time()
                interval = now - last_time
                chunk_intervals.append(interval)
                last_time = now

        end = time.time()

        return {
            "bytes_downloaded": total_bytes,
            "download_time": end - start,
            "chunk_intervals": chunk_intervals
        }

    except Exception as e:

        print("Download error:", e)

        return None