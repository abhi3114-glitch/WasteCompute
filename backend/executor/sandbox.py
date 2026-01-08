import subprocess
import time
import threading
import psutil

# Active job monitoring
active_jobs = {}

def execute_job(command: str, timeout: int, resource_type: str = "cpu"):
    """Execute a job in a sandboxed subprocess with monitoring.
    
    Args:
        command: The command to execute
        timeout: Maximum execution time in seconds
        resource_type: "cpu" or "gpu" - affects output prefix and pricing
    """
    from backend.executor.limits import apply_resource_limits
    
    start = time.time()
    resource_prefix = f"[{resource_type.upper()} EXECUTION]\n"
    
    # Apply resource limits
    apply_resource_limits(cpu_seconds=timeout, memory_mb=512)

    try:
        # Split command safely (works on Windows & Linux)
        cmd_parts = command.strip().split()

        process = subprocess.Popen(
            cmd_parts,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Track active job
        job_info = {
            "pid": process.pid,
            "command": command,
            "resource_type": resource_type,
            "start_time": start,
            "status": "running"
        }
        active_jobs[process.pid] = job_info
        
        # Monitor in background thread
        monitor_thread = threading.Thread(
            target=monitor_job,
            args=(process.pid, timeout)
        )
        monitor_thread.start()

        stdout, stderr = process.communicate(timeout=timeout)
        execution_time = round(time.time() - start, 2)
        
        # Update job status
        if process.pid in active_jobs:
            active_jobs[process.pid]["status"] = "completed"
            active_jobs[process.pid]["execution_time"] = execution_time

        if process.returncode != 0:
            return {
                "status": "error",
                "output": resource_prefix + (stderr.strip() or "Unknown error"),
                "execution_time": execution_time,
                "resource_type": resource_type,
                "pid": process.pid
            }

        return {
            "status": "completed",
            "output": resource_prefix + stdout.strip(),
            "execution_time": execution_time,
            "resource_type": resource_type,
            "pid": process.pid
        }

    except subprocess.TimeoutExpired:
        process.kill()
        if process.pid in active_jobs:
            active_jobs[process.pid]["status"] = "timeout"
        return {
            "status": "timeout",
            "output": resource_prefix + "Job exceeded time limit",
            "execution_time": timeout,
            "resource_type": resource_type
        }

    except Exception as e:
        return {
            "status": "error",
            "output": resource_prefix + str(e),
            "execution_time": 0,
            "resource_type": resource_type
        }


def monitor_job(pid: int, timeout: int):
    """Monitor a running job's resource usage."""
    from backend.executor.monitor import monitor_process
    try:
        result = monitor_process(pid, timeout)
        if pid in active_jobs:
            active_jobs[pid]["monitor_result"] = result
    except Exception as e:
        if pid in active_jobs:
            active_jobs[pid]["monitor_result"] = f"Monitor error: {str(e)}"


def get_active_jobs():
    """Return list of currently active/recent jobs."""
    return list(active_jobs.values())
