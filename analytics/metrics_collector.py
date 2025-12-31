from analytics.usage_tracker import usage_log

def compute_metrics():
    total_cpu = sum(u["cpu_seconds"] for u in usage_log)
    total_ram = sum(u["ram_mb_seconds"] for u in usage_log)

    return {
        "total_cpu_seconds": round(total_cpu, 2),
        "total_ram_mb_seconds": round(total_ram, 2),
        "total_jobs": len(usage_log)
    }
