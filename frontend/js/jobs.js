async function submitJob() {
  const cmd = document.getElementById("jobCmd").value;
  const outputBox = document.getElementById("jobOutput");

  outputBox.textContent = "Running...";

  try {
    const result = await apiPost("/jobs/submit", { command: cmd });

    if (result.status === "error" || result.error) {
      outputBox.textContent = result.message || result.error;
      return;
    }

    // Show output cleanly
    outputBox.textContent = result.output || "Job completed";

    // Refresh history
    loadJobHistory();

  } catch (err) {
    outputBox.textContent = "Backend error or server not responding";
  }
}


async function loadJobHistory() {
  const jobs = await apiGet("/jobs/history");
  const table = document.getElementById("jobTable");

  table.innerHTML = "";

  jobs.forEach(job => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${job.job_id}</td>
      <td>${job.node_id}</td>
      <td>${job.status}</td>
      <td>${job.execution_time}s</td>
    `;
    table.appendChild(row);
  });
}
