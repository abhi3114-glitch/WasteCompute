import psutil
import time

def monitor_process(pid: int, timeout: int):
    start = time.time()
    try:
        process = psutil.Process(pid)

        while time.time() - start < timeout:
            cpu = process.cpu_percent(interval=0.5)
            memory = process.memory_info().rss / (1024 * 1024)

            if cpu > 90:
                process.kill()
                return "CPU limit exceeded"

            time.sleep(0.5)

        return "Execution completed"

    except psutil.NoSuchProcess:
        return "Process ended"
