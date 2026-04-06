output "raw_bucket" { value = module.gcs_raw.bucket_name }
output "out_bucket" { value = module.gcs_out.bucket_name }
#output "pubsub_topic" { value = module.pubsub.topic_id }
#output "pubsub_subscription" { value = module.pubsub.subscription_id }

output "service_uri" {
  value = module.service.uri
}

output "job_names" {
  value = { for k, m in module.jobs : k => m.name }
}

#output "cloud_run_uri" { value = module.cloud_run.uri }

#output "pubsub_topic"        { value = module.pubsub.topic_id }
#output "pubsub_subscription" { value = module.pubsub_gcs_push.subscription_id }

#output "vertex_index_id"          { value = module.vertex.index_id }
#output "vertex_index_endpoint_id" { value = module.vertex.endpoint_id }
#output "vertex_deployed_index_id" { value = module.vertex.deployed_index_id }