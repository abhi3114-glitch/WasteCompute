from pydantic import BaseModel
from typing import Optional
import time

class Node(BaseModel):
    node_id: str
    cpu: float
    ram: float
    gpu: str = "Unknown"  # GPU name or "None"
    status: str
    last_heartbeat: float = time.time()

class JobRequest(BaseModel):
    command: str
    max_runtime: int = 10
    priority: int = 1
    resource_type: str = "cpu"  # "cpu" or "gpu"

class JobRecord(BaseModel):
    job_id: int
    command: str
    node_id: str
    status: str
    execution_time: float
    output: str
    timestamp: float
