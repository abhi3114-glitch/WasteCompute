import subprocess
import time

def execute_job(command: str, timeout: int):
    start = time.time()

    try:
        # Split command safely (works on Windows & Linux)
        cmd_parts = command.strip().split()

        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            timeout=timeout,
            text=True
        )

        execution_time = round(time.time() - start, 2)

        if result.returncode != 0:
            return {
                "status": "error",
                "output": result.stderr.strip(),
                "execution_time": execution_time
            }

        return {
            "status": "completed",
            "output": result.stdout.strip(),
            "execution_time": execution_time
        }

    except Exception as e:
        return {
            "status": "error",
            "output": str(e),
            "execution_time": 0
        }
