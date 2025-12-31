function refreshDashboard() {
  loadNodes();
  loadJobHistory();
}

setInterval(refreshDashboard, 5000);
refreshDashboard();
