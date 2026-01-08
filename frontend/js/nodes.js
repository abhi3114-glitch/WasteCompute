async function loadNodes() {
  const container = document.getElementById("nodes-list");
  if (!container) {
    console.error("Nodes container not found!");
    return;
  }

  try {
    const nodes = await apiGet("/nodes");

    if (!nodes || nodes.length === 0) {
      container.innerHTML = `
        <div style="color: var(--text-secondary); padding: 32px; text-align: center; border: 1px dashed var(--border-subtle); border-radius: 8px;">
          <div style="margin-bottom: 8px;">No active nodes found</div>
          <div style="font-size: 12px; color: var(--text-tertiary);">Click "Provision Node" to add compute resources</div>
        </div>
      `;
      return;
    }

    console.log(`Rendering ${nodes.length} nodes...`);
    container.innerHTML = "";

    nodes.forEach((n, index) => {
      const div = document.createElement("div");
      div.className = "node-card";
      div.style.display = "flex";
      div.style.justifyContent = "space-between";
      div.style.alignItems = "center";

      // Status colors without glow
      const isIdle = n.status === "idle";
      const statusColor = isIdle ? "var(--accent-green)" : "var(--accent-red)";

      div.innerHTML = `
        <div style="display: flex; align-items: center; gap: 12px;">
          <div class="status-dot ${isIdle ? 'healthy' : 'error'}"></div>
          <div>
            <div style="font-weight: 500; font-size: 13px; color: var(--text-primary)">${n.node_id}</div>
            <div style="font-size: 11px; color: var(--text-tertiary); margin-top: 2px;">${n.gpu || 'No GPU'}</div>
          </div>
        </div>
        <div style="display: flex; gap: 20px; font-size: 12px;">
          <div>
            <span style="color: var(--text-tertiary);">CPU</span>
            <span style="color: var(--text-primary); font-weight: 500; margin-left: 4px;">${n.cpu}%</span>
          </div>
          <div>
            <span style="color: var(--text-tertiary);">RAM</span>
            <span style="color: var(--text-primary); font-weight: 500; margin-left: 4px;">${n.ram}GB</span>
          </div>
          <div style="text-transform: capitalize; color: ${statusColor}; font-weight: 500;">
            ${n.status}
          </div>
        </div>
      `;
      container.appendChild(div);
    });
  } catch (e) {
    container.innerHTML = `
      <div style="color: var(--accent-red); padding: 16px; border: 1px solid var(--accent-red); border-radius: 6px; background: rgba(239, 68, 68, 0.05);">
        <strong>Error:</strong> ${e.message}
      </div>
    `;
    console.error(e);
  }
}
