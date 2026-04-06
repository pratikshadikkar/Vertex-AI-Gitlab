terraform {
  backend "gcs" {
    bucket = "deloitte-tfstate-demo-embedding-search-tf"
    prefix = "embedding-search/state"
  }
}