from fastapi import FastAPI
from backend.api import nodes, jobs, metrics
from backend.utils.logger import setup_logger
from fastapi.middleware.cors import CORSMiddleware
from backend.database.db import nodes_db
logger = setup_logger()

app = FastAPI(
    title="WasteCompute Backend",
    version="1.0.0",
    description="Enterprise-grade compute scheduling backend"
)

app.include_router(nodes.router, prefix="/nodes", tags=["Nodes"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])

@app.get("/")
def root():
    logger.info("Health check called")
    return {"status": "Backend running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)




nodes_db["demo-node-1"] = {
    "node_id": "demo-node-1",
    "cpu": 5,
    "ram": 20,
    "status": "idle"
}

