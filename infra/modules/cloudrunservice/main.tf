resource "google_cloud_run_v2_service" "this" {
  name     = var.name
  location = var.location

  template {
    service_account = var.service_account_email
    containers {
      image = var.image

      resources {
        limits = {
         cpu    = var.cpu
         memory = var.memory
        }
     }

      dynamic "env" {
        for_each = var.env
        content {
          name  = env.key
          value = env.value
        }
      }
    }

    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }
  }

  ingress = var.ingress
}
