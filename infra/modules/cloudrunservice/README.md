# Google Cloud Run Service Terraform Module

This module provisions a Google Cloud Run Service for deploying containerized applications with autoscaling and managed ingress.

## Required Parameters

| Name                   | Type   | Description                                      |
|------------------------|--------|--------------------------------------------------|
| `name`                 | string | Name of the Cloud Run Service (unique per project/location) |
| `location`             | string | GCP region for the service                       |
| `image`                | string | Container image to deploy                        |
| `service_account_email`| string | Service account email for the service            |

## Optional Parameters

| Name             | Type         | Description                                      | Default   |
|------------------|--------------|--------------------------------------------------|-----------|
| `env`            | map(string)  | Environment variables for the service            | `{}`      |
| `min_instances`  | number       | Minimum number of instances                      | `0`       |
| `max_instances`  | number       | Maximum number of instances                      | `3`       |
| `cpu`            | string       | CPU units to allocate                            | (see variable) |
| `memory`         | string       | Memory to allocate                               | (see variable) |
| `ingress`        | string       | Ingress settings                                 | `INGRESS_TRAFFIC_ALL` |

## Outputs

- `name`: Name of the Cloud Run Service created
- `uri`: URI of the deployed Cloud Run Service

---

This module is intended for deploying stateless, containerized web services or APIs on Google Cloud Platform with managed scaling and ingress control.

