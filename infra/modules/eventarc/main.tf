resource "google_eventarc_trigger" "gcs_to_run" {
  name     = var.trigger_name
  location = var.region

  service_account = var.trigger_service_account

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.storage.object.v1.finalized"
  }

  matching_criteria {
    attribute = "bucket"
    value     = var.raw_bucket_name
  }

  destination {
    cloud_run_service {
      service = var.cloud_run_service_name
      region  = var.region
    }
  }
}