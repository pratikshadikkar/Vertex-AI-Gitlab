resource "google_service_account_iam_member" "allow_actas" {
  service_account_id = var.target_service_account_id
  role               = "roles/iam.serviceAccountUser"
  member             = var.deployer_principal
}