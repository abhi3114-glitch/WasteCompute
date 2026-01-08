from fastapi import APIRouter
from backend.database import db
from backend.database.models import Node
from typing import List
import time
import platform
import subprocess

router = APIRouter()

def detect_hardware():
    """Detect real CPU, RAM, and GPU from the local machine."""
    cpu_percent = 0
    ram_gb = 0
    gpu_name = "None"
    
    # Detect CPU and RAM using psutil if available, else use WMI on Windows
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=0.5)
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
    except ImportError:
        # Fallback for Windows without psutil
        if platform.system() == "Windows":
            try:
                # Get total RAM
                result = subprocess.run(
                    ["wmic", "ComputerSystem", "get", "TotalPhysicalMemory"],
                    capture_output=True, text=True, timeout=5
                )
                lines = [l.strip() for l in result.stdout.split("\n") if l.strip() and l.strip() != "TotalPhysicalMemory"]
                if lines:
                    ram_gb = round(int(lines[0]) / (1024**3), 1)
                
                # Get CPU load (approximate)
                result = subprocess.run(
                    ["wmic", "cpu", "get", "loadpercentage"],
                    capture_output=True, text=True, timeout=5
                )
                lines = [l.strip() for l in result.stdout.split("\n") if l.strip() and l.strip() != "LoadPercentage"]
                if lines:
                    cpu_percent = int(lines[0])
            except Exception:
                cpu_percent = 5
                ram_gb = 16
    
    # Detect GPU using PowerShell (wmic not available in PS)
    try:
        if platform.system() == "Windows":
            # Use PowerShell's Get-WmiObject
            result = subprocess.run(
                ["powershell", "-Command", "Get-WmiObject Win32_VideoController | Select-Object -ExpandProperty Name"],
                capture_output=True, text=True, timeout=10, shell=True
            )
            if result.returncode == 0 and result.stdout.strip():
                # Get first GPU (usually the discrete one listed first or second)
                lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
                # Prefer NVIDIA or AMD discrete GPU over integrated
                for line in lines:
                    if "NVIDIA" in line or "RTX" in line or "GTX" in line:
                        gpu_name = line
                        break
                    elif "AMD" in line and "Radeon" in line and "Graphics" not in line:
                        gpu_name = line
                        break
                else:
                    gpu_name = lines[0] if lines else "Unknown"
        else:
            # Try nvidia-smi for Linux
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                gpu_name = result.stdout.strip()
    except Exception as e:
        gpu_name = f"Detection Error: {str(e)}"
    
    return cpu_percent, ram_gb, gpu_name

@router.post("/heartbeat")
def heartbeat(node: Node):
    # Persist node heartbeat to SQLite
    db.add_node(
        node_id=node.node_id,
        cpu=node.cpu,
        ram=node.ram,
        gpu=getattr(node, 'gpu', 'Unknown'),
        status=node.status
    )
    return {"message": "Heartbeat received", "node": node.node_id}

@router.post("/provision")
def provision_node():
    import uuid
    
    # Detect real hardware
    cpu_percent, ram_gb, gpu_name = detect_hardware()
    
    new_id = f"node-{str(uuid.uuid4())[:8]}"
    
    # Persist to SQLite
    db.add_node(
        node_id=new_id,
        cpu=cpu_percent,
        ram=ram_gb,
        gpu=gpu_name,
        status="idle"
    )
    
    return {
        "node_id": new_id,
        "cpu": cpu_percent,
        "ram": ram_gb,
        "gpu": gpu_name,
        "status": "idle",
        "last_heartbeat": time.time()
    }

@router.get("/")
def list_nodes():
    return db.get_nodes()
