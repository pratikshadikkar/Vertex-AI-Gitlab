resource "google_storage_bucket" "bucket" {
  name     = var.bucket_name
  location = var.region
  project  = var.project_id
  labels   = var.labels
  storage_class = var.storage_class
  versioning {
    enabled = var.versioning
  }
  force_destroy               = var.force_destroy
  public_access_prevention    = var.public_access_prevention
  uniform_bucket_level_access = var.bucket_policy_only
}