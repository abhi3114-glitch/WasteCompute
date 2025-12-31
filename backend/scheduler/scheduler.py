from backend.executor.sandbox import execute_job
from backend.database.db import job_db
import time

job_counter = 0

def schedule_job(job):
    global job_counter

    from backend.scheduler.scoring import select_best_node
    node = select_best_node()

    if not node:
        return {
            "status": "error",
            "message": "No idle nodes available"
        }

    job_counter += 1

    try:
        result = execute_job(job.command, job.max_runtime)

        record = {
            "job_id": job_counter,
            "command": job.command,
            "node_id": node["node_id"],
            "status": result["status"],
            "execution_time": result["execution_time"],
            "output": result["output"],
            "timestamp": time.time()
        }

        job_db.append(record)
        return record

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
