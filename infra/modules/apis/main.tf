resource "google_project_service" "service_apis" {
  for_each           = toset(var.gcp_service_list)
  project            = var.project_id
  service            = each.key
  disable_on_destroy = var.disable_services_on_destroy
}
