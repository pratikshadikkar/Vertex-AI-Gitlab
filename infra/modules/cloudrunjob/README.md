# Google Cloud Run Job Terraform Module

This module provisions a Google Cloud Run Job for running containerized workloads on demand.

## Required Parameters

| Name                   | Type   | Description                                      |
|------------------------|--------|--------------------------------------------------|
| `name`                 | string | Name of the Cloud Run Job (unique per project/location) |
| `location`             | string | GCP region for the job                           |
| `image`                | string | Container image to run                           |
| `service_account_email`| string | Service account email for the job                |

## Optional Parameters

| Name             | Type         | Description                                      | Default   |
|------------------|--------------|--------------------------------------------------|-----------|
| `env`            | map(string)  | Environment variables for the job                 | `{}`      |
| `task_count`     | number       | Total number of tasks to run                     | `1`       |
| `parallelism`    | number       | Number of tasks to run in parallel               | `1`       |
| `max_retries`    | number       | Maximum number of retries for a task             | `3`       |
| `timeout`        | string       | Maximum duration a task can run                  | `3600s`   |
| `cpu`            | string       | CPU units to allocate                            | `2`       |
| `memory`         | string       | Memory to allocate                               | `2Gi`     |

## Outputs

- `name`: Name of the Cloud Run Job created

---

This module is intended for use in data pipelines or batch processing scenarios where containerized jobs need to be executed on demand in Google Cloud Platform.
