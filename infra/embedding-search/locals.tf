locals {
  env    = terraform.workspace
  region = var.region

  raw_bucket_name = "es-raw-data-${local.env}"
  out_bucket_name = "es-processed-data-${local.env}"
  index_bucket_name = "es-index-data-${local.env}"

  trigger_name = "es-ingest-trigger-${local.env}"

  #function_name = "es-ingest-pubsub-${local.env}"

  #pubsub_topic_name        = "es-ingest-topic-${local.env}"
  #pubsub_subscription_name = "es-ingest-push-${local.env}"

  sa_account_id = "batch-processor-sa-${local.env}"

  #vector_index_name     = "${var.vector_index_name_base}-${local.env}"
  #vector_endpoint_name = "${var.vector_endpoint_name_base}-${local.env}"
  #deployed_index_id    = "${var.deployed_index_id_base}-${local.env}"
}