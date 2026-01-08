import sqlite3
import os
import time

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), "wastecompute.db")

def get_connection():
    """Get a database connection with row factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create nodes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            node_id TEXT PRIMARY KEY,
            cpu REAL,
            ram REAL,
            gpu TEXT DEFAULT 'Unknown',
            status TEXT DEFAULT 'idle',
            last_heartbeat REAL
        )
    ''')
    
    # Create jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT,
            node_id TEXT,
            resource_type TEXT DEFAULT 'cpu',
            status TEXT,
            execution_time REAL,
            output TEXT,
            timestamp REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"[DB] Initialized SQLite database at {DB_PATH}")

# --- NODE OPERATIONS ---

def add_node(node_id: str, cpu: float, ram: float, gpu: str = "Unknown", status: str = "idle"):
    """Add or update a node in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO nodes (node_id, cpu, ram, gpu, status, last_heartbeat)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (node_id, cpu, ram, gpu, status, time.time()))
    conn.commit()
    conn.close()

def get_nodes():
    """Get all nodes from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nodes')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_node(node_id: str):
    """Get a specific node by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nodes WHERE node_id = ?', (node_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# --- JOB OPERATIONS ---

def add_job(command: str, node_id: str, resource_type: str, status: str, execution_time: float, output: str):
    """Add a job record to the database. Returns the job_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO jobs (command, node_id, resource_type, status, execution_time, output, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (command, node_id, resource_type, status, execution_time, output, time.time()))
    job_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return job_id

def get_jobs():
    """Get all jobs from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs ORDER BY job_id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_job(job_id: int):
    """Get a specific job by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE job_id = ?', (job_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# --- LEGACY COMPATIBILITY ---
# These are kept for backward compatibility during migration
# They will be populated from the database on startup

nodes_db = {}  # Legacy: Will be deprecated
job_db = []    # Legacy: Will be deprecated
job_counter = 0  # Legacy: Will be deprecated

def sync_from_db():
    """Sync in-memory structures from database (for legacy code)."""
    global nodes_db, job_db, job_counter
    nodes_db = {n['node_id']: n for n in get_nodes()}
    job_db = get_jobs()
    if job_db:
        job_counter = max(j['job_id'] for j in job_db)
    else:
        job_counter = 0

# Initialize database on module load
init_db()
sync_from_db()
