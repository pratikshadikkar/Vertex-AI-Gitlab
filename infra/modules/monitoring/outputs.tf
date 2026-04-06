output "dashboard_id" {
  value = google_monitoring_dashboard.pipeline.id
}

output "alert_policies" {
  value = [
    google_monitoring_alert_policy.error_rate,
    google_monitoring_alert_policy.latency,
    google_monitoring_alert_policy.cpu,
    google_monitoring_alert_policy.memory
  ]
}