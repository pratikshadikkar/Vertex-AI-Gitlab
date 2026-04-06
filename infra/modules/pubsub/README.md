
# Google Cloud Pub/Sub Terraform Module

This module provisions Google Cloud Pub/Sub topics and subscriptions for use in a data pipeline:
- **Topics**: For publishing messages
- **Subscriptions**: For consuming messages from topics

## Required Parameters

| Name                | Type         | Description                                 |
|---------------------|--------------|---------------------------------------------|
| `topics`            | list(object) | List of Pub/Sub topics to create            |
| `subscriptions`     | list(object) | List of Pub/Sub subscriptions to create     |
| `topic_iam`         | list(object) | IAM bindings for topics                     |
| `subscription_iam`  | list(object) | IAM bindings for subscriptions              |

## Outputs

- `topic_names`: List of created topic names
- `subscription_names`: List of created subscription names

