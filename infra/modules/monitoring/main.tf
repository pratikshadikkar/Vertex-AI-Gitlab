# notification
resource "google_monitoring_notification_channel" "email" {
  display_name = "Email Alerts"
  type         = "email"

  labels = {
    email_address = var.notification_email
  }
}

########################
# alerts ###############

locals {
  services = toset(var.services)
}

################################
# ERROR RATE ALERT
################################
resource "google_monitoring_alert_policy" "error_rate" {
  for_each = local.services

  display_name = "${each.value} error rate > ${var.error_rate_threshold * 100}%"
  combiner     = "OR"

  conditions {
    display_name = "Error rate"

    condition_threshold {
      filter = <<EOT
resource.type="cloud_run_revision"
metric.type="run.googleapis.com/request_count"
resource.label.service_name="${each.value}"
metric.label.response_code_class="5xx"
EOT

      comparison      = "COMPARISON_GT"
      threshold_value = var.error_rate_threshold
      duration        = "300s"

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.id]
}

########################
# LATENCY ALERT
################################
resource "google_monitoring_alert_policy" "latency" {
  for_each = local.services

  display_name = "${each.value} latency high"
  combiner     = "OR"

  conditions {
    display_name = "Latency > threshold"

    condition_threshold {
      filter = <<EOT
resource.type="cloud_run_revision"
metric.type="run.googleapis.com/request_latencies"
resource.label.service_name="${each.value}"
EOT

      comparison      = "COMPARISON_GT"
      threshold_value = var.latency_threshold_ms
      duration        = "300s"

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_PERCENTILE_95"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.id]
}

################################
# CPU ALERT
################################
resource "google_monitoring_alert_policy" "cpu" {
  for_each = local.services

  display_name = "${each.value} CPU high"

  combiner = "OR"

  conditions {
    display_name = "CPU usage"

    condition_threshold {
      filter = <<EOT
resource.type="cloud_run_revision"
metric.type="run.googleapis.com/container/cpu/utilizations"
resource.label.service_name="${each.value}"
EOT

      comparison      = "COMPARISON_GT"
      threshold_value = var.cpu_threshold
      duration        = "300s"

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_PERCENTILE_95"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.id]
}

################################
# MEMORY ALERT
################################
resource "google_monitoring_alert_policy" "memory" {
  for_each = local.services

  display_name = "${each.value} memory high"

  combiner = "OR"

  conditions {
    display_name = "Memory usage"

    condition_threshold {
      filter = <<EOT
resource.type="cloud_run_revision"
metric.type="run.googleapis.com/container/memory/utilizations"
resource.label.service_name="${each.value}"
EOT

      comparison      = "COMPARISON_GT"
      threshold_value = var.memory_threshold
      duration        = "300s"

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_PERCENTILE_95"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.id]
}

########################
# LOG METRICS
########################

resource "google_logging_metric" "pipeline_failures" {
  name   = "pipeline_failures"
  filter = "severity>=ERROR"

  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
  }
}

########################
# DASHBOARD
########################
resource "google_monitoring_dashboard" "pipeline" {
  dashboard_json = jsonencode({
    displayName = "Pipeline Observability"
    gridLayout = {
      columns = 2
      widgets = [
        {
          title = "Request Count"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"run.googleapis.com/request_count\""
                }
              }
            }]
          }
        },
        {
          title = "Error Count"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"logging.googleapis.com/user/pipeline_failures\""
                }
              }
            }]
          }
        }
      ]
    }
  })
}
