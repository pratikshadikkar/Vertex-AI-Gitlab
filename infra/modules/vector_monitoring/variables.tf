variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "endpoint_display_name" {
  type = string
}

variable "notification_channels" {
  type = list(string)
}

variable "latency_threshold_ms" {
  type    = number
  default = 2000
}

variable "error_threshold" {
  type    = number
  default = 5
}

variable "min_deployed_indexes" {
  type    = number
  default = 1
}