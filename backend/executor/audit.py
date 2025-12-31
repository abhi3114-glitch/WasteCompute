import time

audit_log = []

def log_event(event_type: str, details: dict):
    record = {
        "timestamp": time.time(),
        "event": event_type,
        "details": details
    }
    audit_log.append(record)

def get_audit_log():
    return audit_log
