
# Trigger handler for ingestion pipeline

import os
import json
import logging
import sys
from flask import Flask, request
from google.cloud import run_v2
from cloudevents.http import from_http, CloudEvent

# Configure structured logging for Cloud Run
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def trigger_job1(input_file: str, generation: str):
    """Trigger Job 1 with input file"""
    project_id = os.environ.get('GCP_PROJECT')
    region = os.environ.get('GCP_REGION', 'us-central1')
    
    logger.info(f"Initializing Jobs client for project: {project_id}, region: {region}")
    client = run_v2.JobsClient()
    
    # Fixed job name (removed the "1")
    job_name = f"projects/{project_id}/locations/{region}/jobs/ingestion-validator-parse-run"
    
    request_obj = run_v2.RunJobRequest(
        name=job_name,
        overrides=run_v2.RunJobRequest.Overrides(
            container_overrides=[
                run_v2.RunJobRequest.Overrides.ContainerOverride(
                    env=[
                        run_v2.EnvVar(name='INPUT_FILE', value=input_file),
                        run_v2.EnvVar(name='GENERATION', value=generation),
                        run_v2.EnvVar(name='GCP_PROJECT', value=project_id),
                        run_v2.EnvVar(name='GCP_REGION', value=region)
                    ]
                )
            ]
        )
    )
    
    logger.info(f"Triggering job: {job_name}")
    logger.info(f"Input file: {input_file}")
    logger.info(f"Generation: {generation}")
    
    client.run_job(request=request_obj)
    logger.info(f"Job triggered successfully")

@app.route('/', methods=['POST'])
def handle_event():
    """Handle CloudEvent from Eventarc"""
    
    logger.info("========== NEW REQUEST RECEIVED ==========")
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"Request content-type: {request.content_type}")
    
    # Check if this is a CloudEvent
    if 'ce-type' not in request.headers and 'Ce-Type' not in request.headers:
        logger.warning("Request is not a CloudEvent (missing ce-type header)")
        logger.warning("This might be a health check or bot request")
        return {'message': 'Not a CloudEvent'}, 200
    
    try:
        # Parse CloudEvent
        event = from_http(request.headers, request.get_data())
        
        logger.info(f"CloudEvent received - Type: {event['type']}")
        logger.info(f"CloudEvent ID: {event['id']}")
        logger.info(f"CloudEvent source: {event['source']}")
        logger.info(f"Event data: {json.dumps(event.data, indent=2)}")
        
        # Extract file information
        bucket = event.data.get('bucket')
        name = event.data.get('name')
        generation = str(event.data.get('generation', ''))
        
        if not bucket or not name:
            logger.error("Missing bucket or name in event data")
            return {'error': 'Missing bucket or name in event'}, 400
        
        # Construct full GCS path
        input_file = f"gs://{bucket}/{name}"
        
        logger.info(f"File details:")
        logger.info(f"  Bucket: {bucket}")
        logger.info(f"  Name: {name}")
        logger.info(f"  Full path: {input_file}")
        logger.info(f"  Generation: {generation}")
        
        # Validate that file is in expected location
        if 'text/' not in name and 'multi/' not in name:
            logger.info(f"File not in text/ or multi/ directory - Path: {name}")
            logger.info("Skipping this file")
            return {'message': 'File not in monitored directory'}, 200
        
        logger.info(f"File is in monitored directory, triggering pipeline")
        
        # Trigger Job 1
        trigger_job1(input_file, generation)
        
        logger.info("Pipeline triggered successfully")
        return {
            'message': 'Pipeline triggered successfully',
            'file': input_file,
            'generation': generation
        }, 200
    
    except Exception as e:
        logger.error(f"Error processing event: {e}", exc_info=True)
        return {'error': str(e)}, 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting server on port {port}")
    logger.info(f"GCP_PROJECT: {os.environ.get('GCP_PROJECT')}")
    logger.info(f"GCP_REGION: {os.environ.get('GCP_REGION')}")
    app.run(host='0.0.0.0', port=port)
