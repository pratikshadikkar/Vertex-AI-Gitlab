
# Google Cloud Storage (GCS) Terraform Module

This module provisions two Google Cloud Storage buckets for use in a data pipeline:
- **Raw bucket**: For ingesting unprocessed files
- **Output bucket**: For storing processed/embedded results

## Required Parameters

| Name             | Type   | Description                          |
|------------------|--------|--------------------------------------|
| `project_id`     | string | GCP project ID                       |
| `region`         | string | GCP region for bucket location       |
| `raw_bucket_name`| string | Name for the raw input bucket        |
| `out_bucket_name`| string | Name for the output bucket           |

## Outputs

- `raw_bucket_name`: Name of the raw bucket created
- `out_bucket_name`: Name of the output bucket created
