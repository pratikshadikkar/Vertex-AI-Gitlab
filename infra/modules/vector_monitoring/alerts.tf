resource "google_monitoring_alert_policy" "errors" {
  display_name = "Vertex Endpoint Errors"

  conditions {
    display_name = "Error Count High"

    condition_threshold {
      filter = <<EOT
metric.type="aiplatform.googleapis.com/index_endpoint/error_count"
resource.type="aiplatform.googleapis.com/IndexEndpoint"
resource.label.display_name="${var.endpoint_display_name}"
EOT

      comparison      = "COMPARISON_GT"
      threshold_value = var.error_threshold
      duration        = "300s"

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  combiner = "OR"
  notification_channels = var.notification_channels
}

resource "google_monitoring_alert_policy" "latency" {
  display_name = "Vertex Endpoint Latency"
  combiner     = "OR"
  conditions {
    display_name = "High Latency"

    condition_threshold {
      filter = <<EOT
metric.type="aiplatform.googleapis.com/index_endpoint/request_latencies"
resource.type="aiplatform.googleapis.com/IndexEndpoint"
resource.label.display_name="${var.endpoint_display_name}"
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

  notification_channels = var.notification_channels
}

resource "google_monitoring_alert_policy" "deployment_health" {
  display_name = "Vertex Deployed Index Missing"
  combiner     = "OR"
  conditions {
    display_name = "No Deployed Index"

    condition_threshold {
      filter = <<EOT
metric.type="aiplatform.googleapis.com/index_endpoint/deployed_indexes_count"
resource.type="aiplatform.googleapis.com/IndexEndpoint"
resource.label.display_name="${var.endpoint_display_name}"
EOT

      comparison      = "COMPARISON_LT"
      threshold_value = var.min_deployed_indexes
      duration        = "300s"

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_MIN"
      }
    }
  }

  notification_channels = var.notification_channels
}

resource "google_monitoring_alert_policy" "traffic_drop" {
  display_name = "Vertex Traffic Drop"
  combiner     = "OR"
  conditions {
    display_name = "Request Rate Drop"

    condition_threshold {
      filter = <<EOT
metric.type="aiplatform.googleapis.com/index_endpoint/request_count"
resource.type="aiplatform.googleapis.com/IndexEndpoint"
resource.label.display_name="${var.endpoint_display_name}"
EOT

      comparison      = "COMPARISON_LT"
      threshold_value = 1
      duration        = "600s"

      aggregations {
        alignment_period   = "120s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = var.notification_channels
}

