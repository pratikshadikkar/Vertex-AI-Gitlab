output "vector_index_name" {
  value = google_vertex_ai_index.vector_index.display_name
}
output "vector_endpoint_name" {
  value = google_vertex_ai_index_endpoint.vector_endpoint.display_name
}
