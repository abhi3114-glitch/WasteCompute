const API_BASE = "http://127.0.0.1:8000";

/* GET request */
async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}/`, {
    method: "GET",
  });
  return res.json();
}

/* POST request */
async function apiPost(path, data) {
  const res = await fetch(`${API_BASE}${path}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return res.json();
}
// Nodes
apiGet("/nodes");

// Submit job
apiPost("/jobs/submit", { command: "python jobs/sample_job.py" });

// Metrics
apiGet("/metrics/summary");
