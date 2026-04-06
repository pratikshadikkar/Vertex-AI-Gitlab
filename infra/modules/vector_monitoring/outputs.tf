output "alert_ids" {
  value = [
    google_monitoring_alert_policy.errors.id,
    google_monitoring_alert_policy.latency.id,
    google_monitoring_alert_policy.deployment_health.id,
    google_monitoring_alert_policy.traffic_drop.id
  ]
}