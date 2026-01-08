from backend.database import db

def select_best_node():
    """Select an idle node from the database."""
    nodes = db.get_nodes()
    for node in nodes:
        if node.get("status") == "idle":
            return node
    return None
