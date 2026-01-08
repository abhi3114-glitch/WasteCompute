async function submitJob() {
  const cmdInput = document.getElementById("jobCommand");
  const resourceSelect = document.getElementById("resourceType");
  if (!cmdInput) return;
  const cmd = cmdInput.value;
  const resourceType = resourceSelect ? resourceSelect.value : "cpu";
  const outputBox = document.getElementById("jobOutput");

  outputBox.textContent = "Running...";

  try {
    const result = await apiPost("/jobs/submit", { command: cmd, resource_type: resourceType });

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
  const table = document.getElementById("jobHistory");
  if (!table) return; // Guard clause

  const container = table.querySelector("tbody");
  if (!container) return; // Guard clause

  try {
    const history = await apiGet("/jobs/history");
    container.innerHTML = history.map(job => `
        <tr>
          <td>${job.job_id}</td>
          <td>${job.node_id}</td>
          <td style="text-transform: uppercase; font-weight: 500; color: ${job.resource_type === 'gpu' ? '#00ffff' : '#4ade80'}">${job.resource_type || 'cpu'}</td>
          <td style="font-family: monospace; color: var(--text-primary)">${job.command}</td>
          <td><span class="status-dot ${job.status}"></span> ${job.status}</td>
      <td style="font-family: monospace; font-size: 12px; color: var(--text-secondary)">${(job.output || "").toString().substring(0, 50)}...</td>
        </tr>
      `).join("");
  } catch (e) {
    console.warn("Failed to load job history", e);
  }
}
