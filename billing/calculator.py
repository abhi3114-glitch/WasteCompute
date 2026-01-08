from billing.pricing import calculate_job_cost

def calculate_compute_cost(usage_records: list, rate_per_second: float = 0.05):
    """
    Convert raw usage records into billed transactions using dynamic pricing.
    """
    transactions = []
    
    for record in usage_records:
        resource_type = record.get('resource_type', 'cpu')
        cpu_seconds = record.get('cpu_seconds', 0)
        ram_mb = record.get('ram_mb', 128)  # Default 128MB
        
        # Use dynamic pricing model
        cost_breakdown = calculate_job_cost(cpu_seconds, ram_mb, resource_type)
        
        transactions.append({
            "id": f"tx_{record['job_id']}",
            "reference": f"Job #{record['job_id']} ({record['node_id']})",
            "usage": f"{cpu_seconds}s ({resource_type.upper()})",
            "resource_type": resource_type,
            "cost": cost_breakdown
        })
        
    return transactions
