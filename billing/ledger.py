billing_ledger = []

def record_transaction(job_id: int, user: str, cost: dict):
    entry = {
        "job_id": job_id,
        "user": user,
        "cost": cost
    }
    billing_ledger.append(entry)
    return entry

def get_ledger():
    return billing_ledger
