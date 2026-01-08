// Console Logger Utility
function logToConsole(msg, type = 'info') {
  const consoleDiv = document.getElementById("consoleOutput");
  const line = document.createElement("div");
  line.className = `log-line ${type}`;
  line.textContent = `> ${msg}`;
  consoleDiv.appendChild(line);
  consoleDiv.scrollTop = consoleDiv.scrollHeight;
}

async function provisionNode() {
  logToConsole("Provisioning new compute node...", "warn");
  const btn = document.querySelector("button[onclick='provisionNode()']");
  btn.disabled = true;
  btn.textContent = "Provisioning...";

  try {
    await apiPost("/nodes/provision", {});
    logToConsole("Node provisioned successfully.", "success");
    loadNodes(); // Refresh list
  } catch (e) {
    logToConsole("Failed to provision node.", "error");
  } finally {
    setTimeout(() => {
      btn.disabled = false;
      btn.textContent = "+ Provision Node";
    }, 1000);
  }
}

// Override default submitJob for console effect
window.submitJob = async function () {
  const command = document.getElementById("jobCommand").value;
  const resourceSelect = document.getElementById("resourceType");
  const resourceType = resourceSelect ? resourceSelect.value : "cpu";

  logToConsole(`Initializing secure ${resourceType.toUpperCase()} environment...`, "info");
  logToConsole(`Submitting workload: ${command}`, "info");
  logToConsole(`Resource: ${resourceType.toUpperCase()}`, "info");

  try {
    const res = await apiPost("/jobs/submit", { command: command, resource_type: resourceType });
    if (res.job_id) {
      logToConsole(`Workload dispatched on ${resourceType.toUpperCase()} (Job ID: ${res.job_id})`, "success");
      logToConsole(`Result: ${res.output.replace(/\n/g, ' ')}`, "success"); // Flatten output for single line log
      loadJobHistory();
    } else {
      logToConsole(`Execution failed: ${res.message || 'Unknown error'}`, "error");
    }
  } catch (e) {
    logToConsole(`Connection error: ${e}`, "error");
  }
}

// Global Promise Error Handler
window.onunhandledrejection = function (event) {
  alert("Async Error: " + event.reason);
  console.error("Async Error", event.reason);
};

// View Persistence logic
window.switchView = function (viewId) {
  // Hide all views
  document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
  // Show target
  document.getElementById(viewId).classList.add('active');

  // Update sidebar state
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  // Find the link that calls this view
  const links = document.querySelectorAll('.nav-item');
  if (viewId === 'view-console') links[1].classList.add('active');
  if (viewId === 'view-nodes') {
    links[2].classList.add('active');
    loadNodes(); // Force refresh when entering view
  }
  if (viewId === 'view-invoices') {
    links[3].classList.add('active');
    loadFinancials(); // Force refresh
  }
}

async function loadFinancials() {
  const invoice = await getInvoice();
  const usage = await getUsage();

  // Load sustainability data
  try {
    const sustainability = await getSustainability();
    const sustainEl = document.getElementById("sustainabilityStats");
    if (sustainEl && sustainability) {
      sustainEl.innerHTML = `
        <div style="margin-bottom: 4px">CO₂ Saved: <span style="color: #4ade80">${sustainability.carbon_saved_kg.toFixed(4)} kg</span></div>
        <div style="margin-bottom: 4px">🌳 Trees: <span style="color: #4ade80">${sustainability.trees_equivalent.toFixed(4)}</span></div>
        <div>Score: <span style="color: #00ffff">${sustainability.sustainability_score}/100</span></div>
      `;
    }
  } catch (e) {
    console.error("Sustainability error:", e);
    const sustainEl = document.getElementById("sustainabilityStats");
    if (sustainEl) {
      sustainEl.innerHTML = `<div style="color: #666">Run jobs to track carbon savings</div>`;
    }
  }

  if (invoice) {
    const totalEl = document.getElementById("invoiceTotal");
    if (totalEl) totalEl.textContent = `$${invoice.total_amount.toFixed(2)}`;

    // Populate Invoice Table
    const table = document.getElementById("invoiceTable");
    if (table) {
      table.innerHTML = `
            <thead>
                <tr>
                    <th style="text-align: left; padding: 12px; border-bottom: 1px solid #333;">Reference</th>
                    <th style="text-align: right; padding: 12px; border-bottom: 1px solid #333;">Usage</th>
                    <th style="text-align: right; padding: 12px; border-bottom: 1px solid #333;">Cost</th>
                </tr>
            </thead>
            <tbody>
                ${invoice.transactions.map(t => `
                    <tr>
                        <td style="padding: 12px; border-bottom: 1px solid #222; color: #ccc;">${t.reference}</td>
                        <td style="padding: 12px; border-bottom: 1px solid #222; text-align: right; font-family: monospace;">${t.usage}</td>
                        <td style="padding: 12px; border-bottom: 1px solid #222; text-align: right; color: #fff;">$${t.cost.total_cost.toFixed(4)}</td>
                    </tr>
                `).join('')}
            </tbody>
          `;
    }
  }

  if (usage) {
    const cpuJobs = usage.filter(u => u.resource_type === 'cpu' || !u.resource_type).length;
    const gpuJobs = usage.filter(u => u.resource_type === 'gpu').length;
    const totalCpuTime = usage.reduce((acc, curr) => acc + curr.cpu_seconds, 0);

    const usageEl = document.getElementById("usageStats");
    if (usageEl) {
      usageEl.innerHTML = `
        <div style="margin-bottom: 4px">Jobs: <span style="color: #fff">${usage.length}</span> (<span style="color: #4ade80">${cpuJobs} CPU</span> / <span style="color: #00ffff">${gpuJobs} GPU</span>)</div>
        <div>Compute Time: <span style="color: #fff">${totalCpuTime.toFixed(2)}s</span></div>
      `;
    }
  }
}

function refreshDashboard() {
  loadNodes();
  loadJobHistory();
  loadFinancials();
}

setInterval(refreshDashboard, 5000);
// console.log("Auto-refresh disabled for debugging");
loadNodes(); // Initial load
loadJobHistory();
loadFinancials();
refreshDashboard();
