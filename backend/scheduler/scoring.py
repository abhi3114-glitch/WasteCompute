from backend.database.db import nodes_db

def select_best_node():
    for node in nodes_db.values():
        if node.get("status") == "idle":
            return node
    return None
