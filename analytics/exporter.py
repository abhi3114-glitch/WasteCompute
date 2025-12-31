import json
from analytics.metrics_collector import compute_metrics

def export_metrics():
    data = compute_metrics()
    with open("analytics_report.json", "w") as f:
        json.dump(data, f, indent=2)
    return data
