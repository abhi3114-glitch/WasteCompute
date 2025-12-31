import time

def generate_invoice(user: str, transactions: list):
    invoice = {
        "invoice_id": f"INV-{int(time.time())}",
        "user": user,
        "date": time.ctime(),
        "transactions": transactions,
        "total_amount": sum(t["cost"]["total_cost"] for t in transactions)
    }
    return invoice
