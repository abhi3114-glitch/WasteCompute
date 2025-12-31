async function loadNodes() {
  const nodes = await apiGet("/nodes");
  const container = document.getElementById("nodes");
  container.innerHTML = "";

  nodes.forEach(n => {
    const div = document.createElement("div");
    div.textContent = `${n.node_id} | CPU: ${n.cpu}% | RAM: ${n.ram}% | ${n.status}`;
    container.appendChild(div);
  });
}
