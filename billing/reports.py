from billing.ledger import billing_ledger

def revenue_report():
    total = sum(entry["cost"]["total_cost"] for entry in billing_ledger)
    return {
        "total_revenue": round(total, 2),
        "total_jobs": len(billing_ledger)
    }
