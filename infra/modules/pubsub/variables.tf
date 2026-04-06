variable "project_id" {
  type        = string
  description = "The project ID to manage the Pub/Sub resources."
}
variable "topic_name" {
  type        = string
  description = "The Pub/Sub topic name."
}
variable "create_topic" {
  type        = bool
  description = "Specify true if you want to create a topic."
  default     = true
}
variable "topic_labels" {
  type        = map(string)
  description = "A map of labels to assign to the Pub/Sub topic."
  default     = {}
}
variable "subscription_name" {
  type        = string
  description = "The Pub/Sub subscription name."
}
variable "subscription_labels" {
  type        = map(string)
  description = "A set of key/value label pairs to assign to the subscription."
  default     = null
}
variable "raw_bucket_name" {
  type        = string
  description = "The name of the raw bucket."
}