resource "google_monitoring_notification_channel" "email" {
  display_name = "Vertex Alerts Email"
  type         = "email"

  labels = {
    email_address = var.notification_channels[0]
  }
}