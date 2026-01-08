const API_BASE = window.location.origin;

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

async function getInvoice() {
  return apiGet("/billing/invoice");
}

async function getUsage() {
  return apiGet("/analytics/usage");
}

async function getSustainability() {
  return apiGet("/analytics/sustainability");
}

async function getPricing() {
  return apiGet("/billing/pricing");
}

async function getAnalyticsSummary() {
  return apiGet("/analytics/summary");
}
