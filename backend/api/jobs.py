from fastapi import APIRouter
from backend.database.models import JobRequest
from backend.scheduler.scheduler import schedule_job
from backend.database import db

router = APIRouter()

@router.post("/submit/")
def submit_job(job: JobRequest):
    return schedule_job(job)

@router.get("/history/")
def job_history():
    return db.get_jobs()
