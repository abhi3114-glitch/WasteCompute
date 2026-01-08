# Dynamic Pricing Model

# Base rates
CPU_COST_PER_SEC = 0.001      # $ per CPU second
GPU_COST_PER_SEC = 0.005      # $ per GPU second (5x CPU)
RAM_COST_PER_MB_SEC = 0.0001  # $ per MB second
PLATFORM_FEE_PERCENT = 15     # WasteCompute marketplace cut

# Time-based multipliers (demand pricing)
PEAK_HOURS = [9, 10, 11, 14, 15, 16]  # Business hours
PEAK_MULTIPLIER = 1.5
OFF_PEAK_MULTIPLIER = 0.8

def get_current_multiplier():
    """Get pricing multiplier based on time of day."""
    from datetime import datetime
    current_hour = datetime.now().hour
    if current_hour in PEAK_HOURS:
        return PEAK_MULTIPLIER
    return OFF_PEAK_MULTIPLIER


def calculate_job_cost(cpu_seconds: float, ram_mb: float, resource_type: str = "cpu"):
    """Calculate cost for a single job.
    
    Args:
        cpu_seconds: Execution time in seconds
        ram_mb: Memory used in MB
        resource_type: "cpu" or "gpu"
    
    Returns:
        dict with cost breakdown
    """
    multiplier = get_current_multiplier()
    
    if resource_type == "gpu":
        compute_cost = cpu_seconds * GPU_COST_PER_SEC * multiplier
    else:
        compute_cost = cpu_seconds * CPU_COST_PER_SEC * multiplier
    
    memory_cost = ram_mb * cpu_seconds * RAM_COST_PER_MB_SEC * multiplier
    
    subtotal = compute_cost + memory_cost
    platform_fee = subtotal * (PLATFORM_FEE_PERCENT / 100)
    total = subtotal + platform_fee
    
    return {
        "compute_cost": round(compute_cost, 6),
        "memory_cost": round(memory_cost, 6),
        "subtotal": round(subtotal, 6),
        "platform_fee": round(platform_fee, 6),
        "platform_fee_percent": PLATFORM_FEE_PERCENT,
        "total_cost": round(total, 6),
        "pricing_multiplier": multiplier,
        "resource_type": resource_type
    }


def get_pricing_info():
    """Get current pricing information for display."""
    return {
        "cpu_per_second": CPU_COST_PER_SEC,
        "gpu_per_second": GPU_COST_PER_SEC,
        "ram_per_mb_second": RAM_COST_PER_MB_SEC,
        "platform_fee_percent": PLATFORM_FEE_PERCENT,
        "current_multiplier": get_current_multiplier(),
        "peak_hours": PEAK_HOURS
    }
