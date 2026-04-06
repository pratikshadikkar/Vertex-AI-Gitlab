import base64
import json
import os
import uuid
import logging

from google.cloud import storage
import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

# -------------------------
# Environment variables
# -------------------------
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
RAW_BUCKET = os.getenv("RAW_BUCKET")
OUT_BUCKET = os.getenv("OUT_BUCKET")

if not all([PROJECT_ID, REGION, RAW_BUCKET, OUT_BUCKET]):
    raise RuntimeError("Missing required environment variables")

# -------------------------
# Init clients (global = reused)
# -------------------------
vertexai.init(project=PROJECT_ID, location=REGION)
embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
storage_client = storage.Client()

logging.basicConfig(level=logging.INFO)

# -------------------------
# Helpers
# -------------------------
def chunk_text(text: str, chunk_size: int = 512):
    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
        if text[i:i + chunk_size].strip()
    ]

# -------------------------
# Cloud Function Entry Point
# -------------------------
def ingest_pubsub(event, context):
    """
    Triggered from a Pub/Sub message.
    """

    try:
        data = base64.b64decode(event["data"]).decode("utf-8")
        payload = json.loads(data)

        bucket_name = payload["bucket"]
        file_name = payload["name"]

        logging.info(f"Processing file: gs://{bucket_name}/{file_name}")

        if bucket_name != RAW_BUCKET:
            logging.warning("Skipping unexpected bucket")
            return

        # Download file
        blob = storage_client.bucket(bucket_name).blob(file_name)
        text = blob.download_as_text()

        chunks = chunk_text(text)
        if not chunks:
            logging.warning("No text chunks found")
            return

        # Generate embeddings
        embeddings = embedding_model.get_embeddings(chunks)

        # Build JSONL
        records = []
        for i, emb in enumerate(embeddings):
            records.append({
                "id": f"{file_name}-{i}",
                "embedding": emb.values,
                "metadata": {
                    "source_file": file_name,
                    "chunk_index": i
                }
            })

        jsonl_data = "\n".join(json.dumps(r) for r in records)

        # Upload output
        out_blob = storage_client.bucket(OUT_BUCKET).blob(
            f"{file_name}-{uuid.uuid4()}.json"
        )
        out_blob.upload_from_string(jsonl_data, content_type="application/json")

        logging.info(f"Successfully processed {len(records)} chunks")

    except Exception as e:
        logging.exception("Processing failed")
        raise
