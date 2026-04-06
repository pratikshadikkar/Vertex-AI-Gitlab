module "api" {
  source     = "../modules/apis"
  project_id = var.project_id

  gcp_service_list = [
    "aiplatform.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudscheduler.googleapis.com",
    "iam.googleapis.com",
    "monitoring.googleapis.com",
    "pubsub.googleapis.com",
    "secretmanager.googleapis.com",
    "storage-api.googleapis.com",
    "storage-component.googleapis.com",
    "storage.googleapis.com",
    "eventarc.googleapis.com"
  ]
}

module "gcs_raw" {
  source = "../modules/gcs"
  bucket_name = local.raw_bucket_name
  project_id = var.project_id
  region   = var.region
  labels   = var.labels
}

module "gcs_out" {
  source = "../modules/gcs"
  project_id = var.project_id
  region     = var.region
  bucket_name = local.out_bucket_name
  labels   = var.labels
}

module "gcs_index" {
  source = "../modules/gcs"
  project_id = var.project_id
  region     = var.region
  bucket_name = local.index_bucket_name
  labels   = var.labels
}


module "eventarc" {
  source = "../modules/eventarc"
  project_id = var.project_id
  region     = var.region

  trigger_name            = local.trigger_name
  raw_bucket_name         = module.gcs_raw.bucket_name
  cloud_run_service_name  = module.service.name
  trigger_service_account = var.trigger_service_account

  depends_on = [module.service] 
}

module "iam" {
  source  = "../modules/iam"
  project = var.project_id

  account_id   = local.sa_account_id

  project_roles = [
    "roles/storage.objectCreator",
    "roles/pubsub.publisher",
    "roles/aiplatform.user",
    "roles/run.invoker",
    "roles/logging.logWriter",
    "roles/run.developer",
    "roles/artifactregistry.reader",
    "roles/eventarc.eventReceiver",
    "roles/iam.serviceAccountUser",
    "roles/storage.objectViewer"
  ]
}

module "service" {
  source   = "../modules/cloudrunservice"
  name     = var.service.name
  location = var.region

  image = var.service.image
  env   = var.service.env
  service_account_email = "${local.sa_account_id}@${var.project_id}.iam.gserviceaccount.com"

  min_instances = var.service.min_instances
  max_instances = var.service.max_instances

  ingress       = var.service.ingress
  #invoker_member = var.service.invoker_member
  memory         = var.service.memory
  cpu            = var.service.cpu
}

module "jobs" {
  source   = "../modules/cloudrunjob"
  for_each = var.jobs

  name     = each.value.name
  location = var.region

  image = each.value.image
  env   = each.value.env

  #task_count  = each.value.task_count
  #parallelism = each.value.parallelism
  max_retries = each.value.max_retries
  timeout     = each.value.timeout
  memory      = each.value.jobs_memory
  cpu         = each.value.jobs_cpu

  service_account_email = "${local.sa_account_id}@${var.project_id}.iam.gserviceaccount.com"
  depends_on = [ module.vertex_ai_vector ]
}

module "vertex_ai_vector" {
  source = "../modules/vertex_ai_vector"

  project_id = var.project_id
  region     = var.region

  vector_index_name = "${var.display_name}-index"
  vector_endpoint_name = "${var.display_name}-endpoint"
  deployment_index_id = "${var.display_name}_deployment_index"

  index_bucket = module.gcs_index.bucket_name
  embedding_dimensions = var.embedding_dimensions
  distance_measure_type = var.distance_measure_type
  #feature_norm_type = var.feature_norm_type
  shard_size = var.shard_size
  leaf_nodes = var.leaf_nodes
  node_embedding_count = var.node_embedding_count
  neighbor_count = var.neighbor_count
  }

  module "monitoring" {
  source = "../modules/monitoring"

  project_id = var.project_id
  region     = var.region
  deployer_principal = "serviceAccount:${module.iam.email}"
  target_service_account_id = module.iam.name

  services = [
    "validator-parser",
    "chunker-embedder",
    "index-upserter",
    "trigger-handler"
  ]

  notification_email = "alerts@company.com"
}
