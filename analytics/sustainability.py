def carbon_savings(cpu_seconds: float):
    # Assume 0.0004 kg CO2 saved per CPU second reused
    saved = cpu_seconds * 0.0004
    return round(saved, 3)
