#Variable file for dev env
project_id = "project-908c61b1-26ec-4b3e-8b9
region     = "us-central1"


service = {
  name           = "trigger-handler"
  image          = "us-central1-docker.pkg.dev/us-con-gcp-sbx-dep0029-081524/embed-search-images/trigger-handler:latest"
  env            = { 
        GCP_PROJECT = "us-con-gcp-sbx-dep0029-081524"
        GCP_REGION = "us-central1"
  }
  min_instances  = 0
  max_instances  = 10
  ingress        = "INGRESS_TRAFFIC_ALL"
  cpu            = "1"
  memory         = "512Mi"
  #invoker_member = "allUsers"
}

jobs = {
  job1 = {
    name        = "ingestion-validator-parse-run"
    image       = "us-central1-docker.pkg.dev/us-con-gcp-sbx-dep0029-081524/embed-search-images/validator-parser:latest"
    env         = {
        GCP_PROJECT = "us-con-gcp-sbx-dep0029-081524"
        GCP_REGION = "us-central1"
        TEXT_INDEX_ID = "8833786479831416832"
        MULTIMODAL_INDEX_ID = "5174664559151022080"
        LOG_LEVEL = "INFO"
     }
    task_count  = 1
    parallelism = 1
    max_retries = 3
    timeout     = "3600s"
    jobs_memory  = "2Gi"
    jobs_cpu     = "2"
  }
  job2 = {
    name        = "ingestion-chunker-embedder-run"
    image       ="us-central1-docker.pkg.dev/us-con-gcp-sbx-dep0029-081524/embed-search-images/chunker-embedder:latest"
    env         = {
        GCP_PROJECT = "us-con-gcp-sbx-dep0029-081524"
        GCP_REGION = "us-central1"
        TEXT_INDEX_ID = "8833786479831416832"
        MULTIMODAL_INDEX_ID = "5174664559151022080"
        LOG_LEVEL = "INFO"
     }
    task_count  = 1
    parallelism = 1
    max_retries = 3
    timeout     = "3600s"
    jobs_memory  = "2Gi"
    jobs_cpu     = "2"
  }
  job3 = {
    name        = "ingestion-index-upserter-run"
    image       = "us-central1-docker.pkg.dev/us-con-gcp-sbx-dep0029-081524/embed-search-images/index-upserter:latest"
    env         = {
        GCP_PROJECT = "us-con-gcp-sbx-dep0029-081524"
        GCP_REGION = "us-central1"
        TEXT_INDEX_ID = "8833786479831416832"
        MULTIMODAL_INDEX_ID = "5174664559151022080"
        LOG_LEVEL = "INFO"
     }
    task_count  = 1
    parallelism = 1
    max_retries = 3
    timeout     = "3600s"
    jobs_memory  = "2Gi"
    jobs_cpu     = "2"
  }
}