# Utils for ingestion pipeline
import json
import os
import re
from datetime import datetime
from google.cloud import storage, run_v2
from typing import Dict, Any, Optional

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be GCS-safe"""
    name, ext = os.path.splitext(filename)
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    return f"{name}{ext}"

def get_run_id(filename: str, generation: str) -> str:
    """Generate unique run ID"""
    sanitized = sanitize_filename(filename).replace('.', '_')
    return f"{sanitized}_{generation}"

def parse_gcs_path(gcs_path: str) -> tuple:
    """Parse gs://bucket/path into (bucket, path)"""
    parts = gcs_path.replace('gs://', '').split('/', 1)
    return parts[0], parts[1] if len(parts) > 1 else ''

def write_to_gcs(bucket_name: str, file_path: str, data: Any) -> str:
    """Write JSON data to GCS"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    
    blob.upload_from_string(
        json.dumps(data, indent=2, ensure_ascii=False),
        content_type='application/json'
    )
    
    full_path = f"gs://{bucket_name}/{file_path}"
    print(f"✓ Written to: {full_path}")
    return full_path

def write_bytes_to_gcs(bucket_name: str, file_path: str, data: bytes, content_type: str) -> str:
    """Write binary data to GCS"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    
    blob.upload_from_string(data, content_type=content_type)
    
    full_path = f"gs://{bucket_name}/{file_path}"
    return full_path

def read_from_gcs(gcs_path: str) -> Dict:
    """Read JSON data from GCS"""
    bucket_name, file_path = parse_gcs_path(gcs_path)
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    
    content = blob.download_as_string()
    return json.loads(content)

def read_bytes_from_gcs(gcs_path: str) -> bytes:
    """Read binary data from GCS"""
    bucket_name, file_path = parse_gcs_path(gcs_path)
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    
    return blob.download_as_bytes()

def gcs_file_exists(gcs_path: str) -> bool:
    """Check if GCS file exists"""
    try:
        bucket_name, file_path = parse_gcs_path(gcs_path)
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        return blob.exists()
    except Exception:
        return False

def delete_gcs_directory(gcs_path: str):
    """Delete all files in a GCS directory"""
    try:
        bucket_name, prefix = parse_gcs_path(gcs_path)
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        blobs = bucket.list_blobs(prefix=prefix)
        for blob in blobs:
            blob.delete()
            print(f"🗑️  Deleted: gs://{bucket_name}/{blob.name}")
    except Exception as e:
        print(f"⚠️  Error deleting directory {gcs_path}: {e}")

def trigger_job(job_name: str, env_vars: Dict[str, str]):
    """Trigger Cloud Run Job with environment variables"""
    project_id = os.environ.get('GCP_PROJECT')
    region = os.environ.get('GCP_REGION', 'us-central1')
    
    client = run_v2.JobsClient()
    
    request = run_v2.RunJobRequest(
        name=f"projects/{project_id}/locations/{region}/jobs/{job_name}",
        overrides=run_v2.RunJobRequest.Overrides(
            container_overrides=[
                run_v2.RunJobRequest.Overrides.ContainerOverride(
                    env=[
                        run_v2.EnvVar(name=k, value=v) 
                        for k, v in env_vars.items()
                    ]
                )
            ]
        )
    )
    
    print(f"Triggering {job_name}...")
    client.run_job(request=request)
    print(f"Triggered {job_name}")

def get_file_metadata(gcs_path: str) -> Dict:
    """Get file metadata from GCS"""
    bucket_name, file_path = parse_gcs_path(gcs_path)
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.reload()
    
    return {
        'size': blob.size,
        'content_type': blob.content_type,
        'generation': str(blob.generation),
        'created': blob.time_created.isoformat() if blob.time_created else None,
        'updated': blob.updated.isoformat() if blob.updated else None
    }
