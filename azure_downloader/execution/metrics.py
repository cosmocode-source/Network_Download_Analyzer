import statistics
def compute_metrics(download_data):
    bytes_downloaded = download_data["bytes_downloaded"]
    download_time = download_data["download_time"]
    intervals = download_data["chunk_intervals"]
    if download_time == 0 or bytes_downloaded == 0:
        return {
            "file_size_MB": 0,
            "download_time_sec": 0,
            "throughput_Mbps": 0,
            "transfer_variance": 0,
            "chunk_count": 0
        }
    mb_downloaded = bytes_downloaded / (1024 * 1024)
    throughput = (bytes_downloaded * 8) / (download_time * 1000000)

    if len(intervals) > 1:
        variance = statistics.pstdev(intervals)
    else:
        variance = 0

    return {
        "file_size_MB": round(mb_downloaded, 2),
        "download_time_sec": round(download_time, 2),
        "throughput_Mbps": round(throughput, 2),
        "transfer_variance": round(variance, 5),
        "chunk_count": len(intervals)
    }