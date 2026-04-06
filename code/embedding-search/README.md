# Embedding Search Cloud Function

This Python script implements a Google Cloud Function for embedding search as part of a Ingestion pipeline.
This function is a core part to enable semantic search and retrieval by generating embeddings for unstructured text data.

## What does it do?

- **Triggered by Pub/Sub**: The function is triggered when a new file is uploaded to a designated Google Cloud Storage (GCS) bucket and a Pub/Sub event is published.
- **Text Extraction & Chunking**: Downloads the file, splits its content into manageable text chunks.
- **Embedding Generation**: Uses Vertex AI's `text-embedding-004` model to generate vector embeddings for each chunk.
- **Output Storage**: Stores the resulting embeddings and metadata as JSONL files in an output GCS bucket.

## Main Flow

1. **Event Trigger**: Receives a Pub/Sub event with the GCS file details.
2. **File Download**: Downloads the file from the raw bucket.
3. **Chunking**: Splits the file into text chunks (default: 512 characters).
4. **Embedding**: Calls Vertex AI to generate embeddings for each chunk.
5. **Output**: Writes a JSONL file with embeddings and metadata to the output bucket.

## Environment Variables

- `PROJECT_ID`: GCP project ID
- `REGION`: GCP region
- `RAW_BUCKET`: Name of the input GCS bucket
- `OUT_BUCKET`: Name of the output GCS bucket

## Requirements

Install dependencies with:
```sh
pip install -r requirements.txt
```

## Usage

This script is designed to be deployed as a Google Cloud Function. It is not intended for direct execution. To deploy, use Terraform or the Google Cloud Console, ensuring all environment variables are set.

## File Structure

- `main.py`: Cloud Function source code
- `requirements.txt`: Python dependencies

[//]: # (Containerization and Artifactory Upload)

## Prerequisites

- Ensure you have [Docker](https://docs.docker.com/get-docker/) installed and running on your machine.
- Access credentials for your organization's Artifactory repository (username, password/API key, and repository URL).
- Python dependencies should be listed in `embedding-func/requirements.txt`.
- Building and pushing the container image will bepart of the CI?CD pipeline.

## Building and Pushing the Container Image

1. **Navigate to the project directory:**
	```sh
	cd embedding-func
	```

2. **Create a `Dockerfile`** (if not already present) 

3. **Create Artifact Registry repo (one-time activity) if not already present**

4. **Build the Docker image:**
	```sh
	docker build -t <your-artifactory-url>/<repo>/<image-name>:<tag> .
	```

5. **Authenticate to Artifactory:**
	```sh
	docker login <your-artifactory-url> -u <username> -p <password-or-api-key>
	```

6. **Push the image to Artifactory:**
	```sh
	docker push <your-artifactory-url>/<repo>/<image-name>:<tag>
	```

Replace `<your-artifactory-url>`, `<repo>`, `<image-name>`, `<tag>`, `<username>`, and `<password-or-api-key>` with your actual values.

---