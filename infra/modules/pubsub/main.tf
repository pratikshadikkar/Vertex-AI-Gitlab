resource "google_pubsub_topic" "ingest" {
  count   = var.create_topic ? 1 : 0
  name    = var.topic_name
  project = var.project_id
  labels  = var.topic_labels
}

resource "google_pubsub_subscription" "push" {
  name  = var.subscription_name
  topic = var.create_topic ? google_pubsub_topic.ingest[0].name : var.topic_name
  project = var.project_id
  labels  = var.subscription_labels
  ack_deadline_seconds = 10
  depends_on = [google_pubsub_topic.ingest]
}

resource "google_storage_notification" "raw_events" {
  bucket         = var.raw_bucket_name
  topic          = google_pubsub_topic.ingest.id
  payload_format = "JSON_API_V1"
  event_types    = ["OBJECT_FINALIZE"]

  depends_on = [google_pubsub_topic_iam_member.gcs_publisher]
}