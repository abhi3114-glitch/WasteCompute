usage_log = []

def track_usage(job_id: int, node_id: str, cpu_time: float, ram_mb: float):
    record = {
        "job_id": job_id,
        "node_id": node_id,
        "cpu_seconds": cpu_time,
        "ram_mb_seconds": ram_mb
    }
    usage_log.append(record)
    return record

def get_usage():
    return usage_log
