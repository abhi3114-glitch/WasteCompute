from fastapi import APIRouter
from backend.database.db import job_db, nodes_db

router = APIRouter()

@router.get("/summary")
def summary():
    return {
        "total_nodes": len(nodes_db),
        "total_jobs": len(job_db)
    }
