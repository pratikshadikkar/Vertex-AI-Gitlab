variable "name"     { 
  type = string
  description = "Name of the Cloud Run Service. Must be unique within the project and location."
}
variable "location" { 
  type = string
  description = "Location of the Cloud Run Service. Must be a valid GCP region."
}
variable "image"    { 
  type = string
  description = "Container image to be used for the Cloud Run Service."
}
variable "env"      { 
  type = map(string) 
  description = "Environment variables for the Cloud Run Service."
  default = {} 
}

variable "service_account_email" {
  type = string
  description = "The email of the service account to be used by the Cloud Run Service."
}

variable "min_instances" { 
  type = number
  description = "The minimum number of instances for the Cloud Run Service."
  default = 0
}
variable "max_instances" { 
  type = number
  description = "The maximum number of instances for the Cloud Run Service."
  default = 3
}

variable "ingress" {
  type    = string
  description = "The ingress settings for the Cloud Run Service."
  default = "INGRESS_TRAFFIC_ALL"
}

variable "invoker_member" {
  type    = string
  description = "The member (user, service account, etc.) to be granted the 'roles/run.invoker' role for the Cloud Run Service."
  default = null
}

variable "cpu" {
  type    = string
  description = "The number of CPU units to allocate for the Cloud Run Service."
  default = "1"
}
variable "memory" {
  type    = string
  description = "The amount of memory to allocate for the Cloud Run Service."
  default = "512Mi"
}

