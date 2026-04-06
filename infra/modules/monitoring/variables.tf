########################
# variables.tf
########################
variable "project_id" { type = string }
variable "region" { type = string }

variable "services" {
  description = "List of Cloud Run service names"
  type        = list(string)
}

variable "notification_email" {
  type = string
}

variable "latency_threshold_ms" {
  default = 2000
}

variable "error_rate_threshold" {
  default = 0.05
}

variable "cpu_threshold" {
  default = 0.8
}

variable "memory_threshold" {
  default = 0.85
}

variable "deployer_principal" {
  type = string
}

variable "target_service_account_id" {
  description = "Service account ID to grant permissions on"
  type        = string
}