from fastapi import APIRouter
from backend.database.db import nodes_db
from backend.database.models import Node
import time

router = APIRouter()

@router.post("/heartbeat")
def heartbeat(node: Node):
    node.last_heartbeat = time.time()
    nodes_db[node.node_id] = node
    return {"message": "Heartbeat received", "node": node.node_id}

@router.get("/")
def list_nodes():
    return list(nodes_db.values())
