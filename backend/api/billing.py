from fastapi import APIRouter
from billing.invoices import generate_invoice
from billing.pricing import get_pricing_info

router = APIRouter()

@router.get("/invoice")
def get_invoice():
    """Get detailed invoice with all transactions."""
    from analytics.usage_tracker import get_usage
    from billing.calculator import calculate_compute_cost
    
    usage_data = get_usage()
    real_transactions = calculate_compute_cost(usage_data)
    
    return generate_invoice("Enterprise_Admin", real_transactions)

@router.get("/pricing")
def get_current_pricing():
    """Get current pricing information including dynamic multipliers."""
    return get_pricing_info()

@router.get("/summary")
def billing_summary():
    """Get quick billing summary."""
    from analytics.usage_tracker import get_usage
    from billing.calculator import calculate_compute_cost
    
    usage_data = get_usage()
    transactions = calculate_compute_cost(usage_data)
    
    total = sum(t["cost"]["total_cost"] for t in transactions)
    
    return {
        "total_jobs": len(transactions),
        "total_amount": round(total, 4),
        "currency": "USD",
        "pricing_info": get_pricing_info()
    }
