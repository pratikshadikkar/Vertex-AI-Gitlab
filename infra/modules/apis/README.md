# Google Cloud APIs Terraform Module

This module enables Google Cloud APIs for a project, allowing required services to be provisioned for your data pipeline or application.

## Required Parameters

| Name                        | Type         | Description                                                      |
|-----------------------------|--------------|------------------------------------------------------------------|
| `project_id`                | string       | GCP project ID                                                   |
| `gcp_service_list`          | list(string) | List of Google Cloud APIs to enable                              |
| `disable_services_on_destroy`| bool         | Disable APIs when destroying resources (default: false)           |

## Outputs

- (No outputs defined)
