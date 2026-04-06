output "topic_name" {
  value = google_pubsub_topic.ingest.name
}

output "topic_id" {
  value = google_pubsub_topic.ingest.id
}