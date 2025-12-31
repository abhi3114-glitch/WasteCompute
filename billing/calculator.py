from billing.pricing import (
    CPU_COST_PER_SEC,
    RAM_COST_PER_MB_SEC,
    PLATFORM_FEE_PERCENT
)

def calculate_cost(cpu_seconds: float, ram_mb_seconds: float):
    base_cost = (
        cpu_seconds * CPU_COST_PER_SEC +
        ram_mb_seconds * RAM_COST_PER_MB_SEC
    )

    platform_fee = (PLATFORM_FEE_PERCENT / 100) * base_cost
    total = round(base_cost + platform_fee, 2)

    return {
        "base_cost": round(base_cost, 2),
        "platform_fee": round(platform_fee, 2),
        "total_cost": total
    }
