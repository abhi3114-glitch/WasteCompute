from fastapi import FastAPI
from backend.api import nodes, jobs, metrics
from backend.utils.logger import setup_logger
from fastapi.middleware.cors import CORSMiddleware
from backend.database.db import nodes_db
from fastapi.staticfiles import StaticFiles
logger = setup_logger()

app = FastAPI(
    title="WasteCompute Backend",
    version="1.0.0",
    description="Enterprise-grade compute scheduling backend"
)

app.include_router(nodes.router, prefix="/nodes", tags=["Nodes"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])

# New Modules
from backend.api import billing, analytics
app.include_router(billing.router, prefix="/billing", tags=["Billing"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])


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

import os
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")





nodes_db["demo-node-1"] = {
    "node_id": "demo-node-1",
    "cpu": 5,
    "ram": 20,
    "status": "idle"
}

