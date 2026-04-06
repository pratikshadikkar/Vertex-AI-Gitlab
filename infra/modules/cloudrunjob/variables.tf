variable "name"     { 
  type = string
  description = "Name of the Cloud Run Job. Must be unique within the project and location."
}
variable "location" { 
  type = string
  description = "Location of the Cloud Run Job. Must be a valid GCP region."
}
variable "image"    { 
  type = string
  description = "Container image to be used for the Cloud Run Job."
}
variable "env"      { 
  type = map(string) 
  description = "Environment variables for the Cloud Run Job."
  default = {} 
}

variable "task_count"  { 
  type = number
  description = "The total number of tasks to run for the Cloud Run Job."
  default = 1
}
variable "parallelism" { 
  type = number
  description = "The number of tasks to run in parallel."
  default = 1
}

variable "max_retries" { 
  type = number
  description = "The maximum number of retries for a task."
  default = 3
}
variable "timeout"     { 
  type = string
  description = "The maximum duration a task can run before being terminated."
  default = "3600s"
}
variable "service_account_email" {
  type = string
  description = "The email of the service account to be used by the Cloud Run Job."
}
variable "cpu" {
  type = string
  description = "The number of CPU units to allocate for the Cloud Run Job."
  default = "2"
}
variable "memory" {
  type = string
  description = "The amount of memory to allocate for the Cloud Run Job."
  default = "2Gi"
}
