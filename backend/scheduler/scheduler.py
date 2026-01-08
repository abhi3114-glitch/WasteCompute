from backend.executor.sandbox import execute_job
from backend.database import db
import time

def schedule_job(job):
    from backend.scheduler.scoring import select_best_node
    node = select_best_node()

    if not node:
        return {
            "status": "error",
            "message": "No idle nodes available"
        }

    try:
        resource_type = getattr(job, 'resource_type', 'cpu')
        result = execute_job(job.command, job.max_runtime, resource_type)

        # Persist to SQLite
        job_id = db.add_job(
            command=job.command,
            node_id=node["node_id"],
            resource_type=resource_type,
            status=result["status"],
            execution_time=result["execution_time"],
            output=result["output"]
        )

        record = {
            "job_id": job_id,
            "command": job.command,
            "node_id": node["node_id"],
            "resource_type": resource_type,
            "status": result["status"],
            "execution_time": result["execution_time"],
            "output": result["output"],
            "timestamp": time.time()
        }
        
        # Link to Analytics
        from analytics.usage_tracker import track_usage
        track_usage(
            job_id=record["job_id"], 
            node_id=record["node_id"], 
            cpu_time=result["execution_time"], 
            ram_mb=128,  # Mock RAM usage for now
            resource_type=resource_type
        )
        
        return record

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
