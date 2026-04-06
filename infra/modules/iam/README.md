
# IAM Terraform Module

This module provisions Google Cloud IAM resources and service accounts for secure, least-privilege access in a data pipeline.

## What it does

- Creates a service account for batch processing
- Assigns custom project roles to the service account
- Creates a Cloud Function execution service account

## Required Parameters

| Name                | Type         | Description                                 |
|---------------------|--------------|---------------------------------------------|
| `project`           | string       | GCP project ID                              |
| `account_id`        | string       | Service account ID for batch processor      |
| `pubsub_topic_name` | string       | Name of the Pub/Sub topic                   |
| `raw_bucket_name`   | string       | Name of the raw input bucket                |
| `project_roles`     | list(string) | List of IAM roles to assign to the account  |
| `display_name`      | string       | Display name for Cloud Function SA          |

## Outputs

- `service_account_email`: Email of the Cloud Function execution service account