# Sustainability & Carbon Footprint Tracking

# Constants based on research:
# - Average server: 0.5 kW
# - Grid carbon intensity: 0.4 kg CO2/kWh (global average)
# - Reusing idle compute saves the embedded carbon of new hardware

WATTS_PER_CPU_CORE = 15  # Typical TDP per core
WATTS_PER_GPU = 250      # Typical GPU TDP
CARBON_INTENSITY = 0.0004  # kg CO2 per Wh (400g/kWh)
EMBEDDED_CARBON_SAVED_PER_HOUR = 0.05  # kg CO2 saved by not buying new hardware

def carbon_savings(cpu_seconds: float, resource_type: str = "cpu"):
    """Calculate CO2 savings from reusing idle compute.
    
    Args:
        cpu_seconds: Total compute seconds used
        resource_type: "cpu" or "gpu"
    
    Returns:
        dict with carbon metrics
    """
    hours = cpu_seconds / 3600
    
    if resource_type == "gpu":
        watts = WATTS_PER_GPU
    else:
        watts = WATTS_PER_CPU_CORE
    
    # Energy used (Wh)
    energy_wh = watts * hours
    
    # Operational carbon (kg CO2)
    operational_carbon = energy_wh * CARBON_INTENSITY
    
    # Embedded carbon saved by reusing hardware
    embedded_saved = hours * EMBEDDED_CARBON_SAVED_PER_HOUR
    
    # Net savings (we're reusing idle hardware, so we save embedded carbon)
    net_savings = embedded_saved - operational_carbon
    
    return {
        "cpu_seconds": cpu_seconds,
        "resource_type": resource_type,
        "energy_wh": round(energy_wh, 4),
        "operational_carbon_kg": round(operational_carbon, 6),
        "embedded_carbon_saved_kg": round(embedded_saved, 6),
        "net_carbon_saved_kg": round(max(0, net_savings), 6),
        "trees_equivalent": round(net_savings / 21, 4)  # 1 tree absorbs ~21kg CO2/year
    }


def get_sustainability_report(usage_data: list):
    """Generate sustainability report from usage data."""
    total_cpu_seconds = sum(u.get("cpu_seconds", 0) for u in usage_data)
    total_gpu_seconds = sum(u.get("gpu_seconds", 0) for u in usage_data if u.get("resource_type") == "gpu")
    
    cpu_savings = carbon_savings(total_cpu_seconds, "cpu")
    gpu_savings = carbon_savings(total_gpu_seconds, "gpu")
    
    return {
        "total_jobs": len(usage_data),
        "total_cpu_seconds": total_cpu_seconds,
        "total_gpu_seconds": total_gpu_seconds,
        "carbon_saved_kg": round(cpu_savings["net_carbon_saved_kg"] + gpu_savings["net_carbon_saved_kg"], 4),
        "trees_equivalent": round(cpu_savings["trees_equivalent"] + gpu_savings["trees_equivalent"], 4),
        "sustainability_score": min(100, len(usage_data) * 5)  # Score based on utilization
    }
