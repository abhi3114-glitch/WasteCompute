usage_log = []

def track_usage(job_id: int, node_id: str, cpu_time: float, ram_mb: float, resource_type: str = "cpu"):
    """Track resource usage for a job.
    
    Args:
        job_id: Unique job identifier
        node_id: Node that executed the job
        cpu_time: Execution time in seconds
        ram_mb: Memory used in MB
        resource_type: "cpu" or "gpu"
    """
    record = {
        "job_id": job_id,
        "node_id": node_id,
        "cpu_seconds": cpu_time,
        "ram_mb": ram_mb,
        "resource_type": resource_type
    }
    usage_log.append(record)
    return record

def get_usage():
    """Get all usage records."""
    return usage_log

def get_usage_summary():
    """Get aggregated usage statistics."""
    if not usage_log:
        return {"total_jobs": 0, "total_cpu_seconds": 0, "total_gpu_seconds": 0}
    
    cpu_seconds = sum(r["cpu_seconds"] for r in usage_log if r.get("resource_type") == "cpu")
    gpu_seconds = sum(r["cpu_seconds"] for r in usage_log if r.get("resource_type") == "gpu")
    
    return {
        "total_jobs": len(usage_log),
        "total_cpu_seconds": round(cpu_seconds, 2),
        "total_gpu_seconds": round(gpu_seconds, 2),
        "cpu_jobs": len([r for r in usage_log if r.get("resource_type") == "cpu"]),
        "gpu_jobs": len([r for r in usage_log if r.get("resource_type") == "gpu"])
    }
