# Vertex AI Vector Index Terraform Module

This module provisions a Vertex AI Vector Index, Index Endpoint, and deploys the index for vector search in Google Cloud Platform.

## Required Parameters

| Name                  | Type   | Description                                      |
|-----------------------|--------|--------------------------------------------------|
| `project_id`          | string | GCP Project ID                                   |
| `region`              | string | Vertex AI region                                 |
| `vector_index_name`   | string | Name of the Vertex AI Index                      |
| `index_bucket`        | string | GCS bucket for storing index data                |
| `embedding_dimensions`| number | Embedding vector size                            |
| `embedding_count`     | number | Number of embeddings per leaf node               |
| `neighbor_count`      | number | Approximate nearest neighbors to return          |
| `vector_endpoint_name`| string | Name of the Vertex AI Index Endpoint             |
| `deployment_index_id` | string | Unique ID for the deployed index                 |
| `min_count`           | number | Minimum number of replicas for deployed index    |
| `max_count`           | number | Maximum number of replicas for deployed index    |

## Optional Parameters

| Name                  | Type   | Description                                      | Default   |
|-----------------------|--------|--------------------------------------------------|-----------|
| `description`         | string | Description of the Vertex AI Index               | "Index for document embeddings created using Terraform" |
| `distance_measure_type`| string| Distance measure type for the index              | "DOT_PRODUCT_DISTANCE" |
| `feature_norm_type`   | string | Feature normalization type                       | "None"   |
| `shard_size`          | string | Number of vectors per shard                      | "SHARD_SIZE_SMALL" |
| `leaf_nodes`          | number | Percentage of leaf nodes to search               | `10`      |
| `machine_type`        | string | CPU/memory config for deployed index             | "e2-standard-2" |

## Outputs

- `vector_index_name`: Name of the Vertex AI Index created
- `vector_endpoint_name`: Name of the Vertex AI Index Endpoint created

---

This module is intended for creating and deploying scalable vector search infrastructure using Google Vertex AI, suitable for document embedding and retrieval use cases.
# Vertex AI Vector Index Terraform Module

This module provisions a Vertex AI vector index and endpoint for storing and querying embedding vectors in Google Cloud.

## Required Parameters

| Name                | Type   | Description                                 |
|---------------------|--------|---------------------------------------------|
| `project_id`        | string | GCP project ID                              |
| `region`            | string | Vertex AI region                            |
| `out_bucket`        | string | Bucket containing embedding JSON files       |
| `embedding_dimensions` | number | Embedding vector size                      |
| `vector_index_name` | string | Name for the vector index                   |

## Outputs

- (No outputs defined)
