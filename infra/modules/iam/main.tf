data "google_project" "current" {}

resource "google_service_account" "processor" {
  account_id   = var.account_id
  display_name = "Batch Processor SA"
  project      = var.project
}

resource "google_project_iam_member" "roles" {
  for_each = toset(var.project_roles)

  project = var.project
  role    = each.value
  member  = "serviceAccount:${google_service_account.processor.email}"
}