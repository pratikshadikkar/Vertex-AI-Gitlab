resource "google_cloud_run_v2_job" "this" {
  name     = var.name
  location = var.location

  template {
    template {
      service_account = var.service_account_email
      containers {
        image = var.image

        dynamic "env" {
          for_each = var.env
          content {
            name  = env.key
            value = env.value
          }
        }
        resources {
          limits = {
            cpu    = var.cpu
            memory = var.memory
          }
        }

    }
    max_retries = var.max_retries
    timeout     = var.timeout
    #task_count  = var.task_count
    #parallelism = var.parallelism
  }
}
}