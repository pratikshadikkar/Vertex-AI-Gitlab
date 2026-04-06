terraform {
  required_version = ">= 1.4.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.20"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_project" "current" {
  project_id = var.project_id
}

# ---------------------------------------------------
# Enable APIs (safe if already enabled)
# ---------------------------------------------------
# resource "google_project_service" "apis" {
#   for_each = toset([
#     "run.googleapis.com",
#     "storage.googleapis.com",
#     "pubsub.googleapis.com",
#     "artifactregistry.googleapis.com",
#     "aiplatform.googleapis.com",
#     "cloudbuild.googleapis.com",
#     "logging.googleapis.com"
#   ])

#   service            = each.value
#   disable_on_destroy = false
# }