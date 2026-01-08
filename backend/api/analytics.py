from fastapi import APIRouter
from analytics.usage_tracker import get_usage
from analytics.sustainability import get_sustainability_report

router = APIRouter()

@router.get("/usage")
def usage_stats():
    """Get all usage records."""
    return get_usage()

@router.get("/sustainability")
def sustainability_stats():
    """Get carbon footprint and sustainability metrics."""
    usage_data = get_usage()
    return get_sustainability_report(usage_data)

@router.get("/summary")
def analytics_summary():
    """Get a quick summary of analytics."""
    usage_data = get_usage()
    sustainability = get_sustainability_report(usage_data)
    
    return {
        "total_jobs": len(usage_data),
        "total_cpu_seconds": sum(u.get("cpu_seconds", 0) for u in usage_data),
        "carbon_saved_kg": sustainability["carbon_saved_kg"],
        "sustainability_score": sustainability["sustainability_score"]
    }
