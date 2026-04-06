variable "project_id" {
 description = "GCP Project ID"
 type = string
}
variable "region" {
 description = "Vertex AI region"
 type = string
}
variable "vector_index_name" {
  type    = string
  description = "Name of the Vertex AI Index to be created."
}
variable "description" {
  type    = string
  default = "Index for document embeddings used in semantic search."
  description = "Description of the Vertex AI Index."
}
variable "index_bucket" {
 description = "GCS bucket for storing index data"
 type = string
}
variable "embedding_dimensions" {
  description = "Embedding vector size"
  type = number
}
variable "node_embedding_count" {
  description = "Number of embeddings to store in each leaf node of the index."
  type = number
}
variable "neighbor_count" {
  description = "Number of approximate nearest neighbors to return in search results."
  type = number
}
variable "distance_measure_type" {
  description = "The distance measure type to use for the index."
  type = string
  default = "DOT_PRODUCT_DISTANCE"
}
variable "feature_norm_type" {
  description = "The feature normalization type to use for the index."
  type = string
  default = "NO_NORMALIZATION"
}
variable "shard_size" {
  description = "The number of vectors to store in each shard of the index."
  type = string
  default = "SHARD_SIZE_SMALL"
}
variable "leaf_nodes" {
  description = "The percentage of leaf nodes to search during query execution."
  type = number
  default = 10
}
variable "vector_endpoint_name" {
  type    = string
  description = "Name of the Vertex AI Index Endpoint to be created."
}
variable "deployment_index_id" {
  type    = string
  description = "The ID to use for the deployed index resource. Must be unique within the index endpoint."
}
variable "machine_type" {
  type = string
  description = "The CPU and memory configuration for the deployed index."
  default = "e2-standard-2"
}
variable "min_count" {
  type = number
  description = "The minimum number of replicas for the deployed index."
  default = 1
}
variable "max_count" {
  type = number
  description = "The maximum number of replicas for the deployed index."
  default = 3
}