resource "google_vertex_ai_index" "vector_index" {
  project      = var.project_id
  region       = var.region
  description = var.description
  display_name = var.vector_index_name
  metadata {
    contents_delta_uri = "gs://${var.index_bucket}/"
    config {
     dimensions                 = var.embedding_dimensions
     approximate_neighbors_count = var.neighbor_count
     distance_measure_type       = var.distance_measure_type
     #feature_norm_type           = var.feature_norm_type
     shard_size = var.shard_size
       algorithm_config {
       tree_ah_config {
         leaf_node_embedding_count    = var.node_embedding_count
         leaf_nodes_to_search_percent = var.leaf_nodes
        }
      }
    }
  }
  index_update_method = "STREAM_UPDATE"
}

resource "google_vertex_ai_index_endpoint" "vector_endpoint" {
  project      = var.project_id
  region       = var.region
  display_name = var.vector_endpoint_name
  description = var.description

  public_endpoint_enabled = true
}

resource "google_vertex_ai_index_endpoint_deployed_index" "deploy_index" {
  deployed_index_id = var.deployment_index_id
  index_endpoint     = google_vertex_ai_index_endpoint.vector_endpoint.id
  index              = google_vertex_ai_index.vector_index.id
  dedicated_resources {
    machine_spec {
      machine_type = var.machine_type
    }
    min_replica_count = var.min_count
    max_replica_count = var.max_count
  }
}
