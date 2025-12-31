import os
import platform

def apply_resource_limits(cpu_seconds: int, memory_mb: int):
    """
    Apply resource limits.
    Works on Linux/macOS.
    Skips limits on Windows (safe fallback).
    """
    if platform.system() == "Windows":
        # Windows does not support resource module
        return

    import resource

    # CPU time limit
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))

    # Memory limit (MB → bytes)
    memory_bytes = memory_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
