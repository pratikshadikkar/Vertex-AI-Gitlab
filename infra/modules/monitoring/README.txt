lsMONITORINGMONITORING MODULE README

Overview

This Terraform module provisions enterprise-grade monitoring for Cloud
Run microservices. It automatically creates alerting, dashboards, log
metrics, and notification channels.

The module is designed to be reusable across environments (dev, stage,
prod) and supports multiple services dynamically.

------------------------------------------------------------------------

Features

-   Per-service alerting
-   Error rate monitoring
-   Latency monitoring (P95)
-   CPU utilization monitoring
-   Memory utilization monitoring
-   Log-based failure metrics
-   Central monitoring dashboard
-   Email notification channel
-   Automatic API enablement

------------------------------------------------------------------------

Architecture Concept

This module does NOT create application services.

Instead it attaches observability to existing infrastructure.

Flow:

Cloud Run → Metrics → Monitoring → Alert Policy → Notification

------------------------------------------------------------------------

Requirements

-   Terraform >= 1.3
-   GCP project with billing enabled
-   Monitoring API permissions
-   Logging API permissions

Required IAM roles for deployer: - Monitoring Admin - Logging Admin -
Service Account Admin (if IAM bindings used)

------------------------------------------------------------------------

Inputs

project_id (string) GCP project id

region (string) Deployment region

services (list(string)) List of Cloud Run service names to monitor

notification_email (string) Email address for alerts

latency_threshold_ms (number) Default: 2000

error_rate_threshold (number) Default: 0.05

cpu_threshold (number) Default: 0.8

memory_threshold (number) Default: 0.85

------------------------------------------------------------------------

Outputs

dashboard_id Monitoring dashboard ID

alert_policies List of alert policy objects created

------------------------------------------------------------------------

Example Usage

module “monitoring” { source = “./modules/monitoring”

project_id = “my-project” region = “us-central1”

services = [ “validator-parser”, “chunker-embedder”, “index-upserter”,
“trigger-handler” ]

notification_email = “alerts@company.com” }

------------------------------------------------------------------------

Alert Logic

Error Alert Triggers if 5xx responses exceed threshold.

Latency Alert Triggers if P95 latency exceeds threshold.

CPU Alert Triggers if CPU utilization exceeds threshold.

Memory Alert Triggers if memory utilization exceeds threshold.

Log Failure Metric Counts logs with severity >= ERROR.

------------------------------------------------------------------------

Testing the Module

1.  Deploy module terraform apply

2.  Generate traffic to services

3.  Force error add temporary exception in code

4.  Verify alerts received

5.  Check dashboard metrics

------------------------------------------------------------------------

Common Errors & Fixes

Service already exists Import resource into Terraform state

IAM actAs denied Grant roles/iam.serviceAccountUser

Invalid metric aligner Use ALIGN_PERCENTILE_95 for distribution metrics

State lock error Run terraform force-unlock LOCK_ID

------------------------------------------------------------------------

Best Practices

-   Always import existing resources before managing them
-   Never disable state locking in production
-   Use separate monitoring thresholds for each environment
-   Keep alert thresholds realistic to avoid noise
-   Use dashboards for real-time visibility

------------------------------------------------------------------------

Production Recommendations

For enterprise setups also consider:

-   PagerDuty or Slack notifications
-   SLO-based alerts
-   Synthetic uptime checks
-   Log export to BigQuery
-   Cost monitoring alerts

------------------------------------------------------------------------

Module Design Principles

Reusable Scalable Environment-agnostic Non-invasive Production-safe

------------------------------------------------------------------------

Author Notes

This module follows Site Reliability Engineering monitoring design
standards. It is safe for production environments and supports scaling
to large microservice architectures.

------------------------------------------------------------------------

End of File
