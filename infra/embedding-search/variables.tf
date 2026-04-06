variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "trigger_service_account" {
  type = string
  description = "The email of the service account to be used by the Eventarc trigger."
  default = "eventarc-trigger-sa@us-con-gcp-sbx-dep0029-081524.iam.gserviceaccount.com"
}

variable "display_name" {
  type = string
  default = "embedding_search"
}

variable "labels" {
  type = map(string)
  default = {
    "team": "search-platform",
    "application": "product-search",
    "environment": "production",
    "use_case": "semantic-search",
    "cost_center": "engineering",
    "index_type": "tree-ah",
    "vector_dimension": "768",
    "data_source": "product-catalog"
  }
}

variable "service" {
  type = object({
    name           = string
    image          = string
    env            = map(string)
    min_instances  = number
    max_instances  = number
    ingress        = string # "INGRESS_TRAFFIC_ALL" | "INGRESS_TRAFFIC_INTERNAL_ONLY" | "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"
    cpu            = string
    memory         = string
    #invoker_member = string # e.g., "allUsers" or "serviceAccount:xxx@yyy.iam.gserviceaccount.com"
  })
}

variable "jobs" {
  type = map(object({
    name        = string
    image       = string
    env         = map(string)
    task_count  = number
    parallelism = number
    max_retries = number
    timeout     = string
    jobs_memory  = string
    jobs_cpu     = string
  }))
}

variable "distance_measure_type" {
  description = "The distance measure type to use for the index."
  type = string
  default = "DOT_PRODUCT_DISTANCE"
}
variable "feature_norm_type" {
  description = "The feature normalization type to use for the index."
  type = string
  default = "FEATURE_NORM_TYPE_UNSPECIFIED "
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
variable "node_embedding_count" {
  description = "Number of embeddings to store in each leaf node of the index."
  type = number
  default = 1000
}
variable "neighbor_count" {
  description = "Number of approximate nearest neighbors to return in search results."
  type = number
  default = 10
}
variable "embedding_dimensions" {
  description = "Embedding vector size"
  type = number
  default = 768
}