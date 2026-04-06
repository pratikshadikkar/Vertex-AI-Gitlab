
import os
import sys
import json
from datetime import datetime
from typing import List, Dict
from google.cloud import aiplatform
from google.cloud.aiplatform import MatchingEngineIndex, MatchingEngineIndexEndpoint

# Add shared utilities to path
sys.path.insert(0, '/app/shared')
from utils import read_from_gcs, write_to_gcs

def upsert_to_index(embeddings: List[Dict], index_id: str, index_type: str) -> List[str]:
    """Upsert embeddings to Vertex AI Vector Index"""
    project_id = os.environ.get('GCP_PROJECT')
    region = os.environ.get('GCP_REGION', 'us-central1')
    
    # Initialize AI Platform
    aiplatform.init(project=project_id, location=region)
    
    print(f"Upserting {len(embeddings)} vectors to {index_type} index...")
    
    # Get index
    index = MatchingEngineIndex(index_name=index_id)
    
    # Prepare datapoints for streaming upsert
    # Streaming index uses upsert_datapoints method
    batch_size = 100
    upserted_ids = []
    
    for i in range(0, len(embeddings), batch_size):
        batch = embeddings[i:i + batch_size]
        
        # Format datapoints for Vertex AI
        datapoints = []
        for item in batch:
            datapoint = {
                "datapoint_id": item['vector_id'],
                "feature_vector": item['embedding'],
                "restricts": [
                    {"namespace": "filename", "allow_list": [item['metadata']['filename']]},
                    {"namespace": "source_type", "allow_list": [item['metadata']['source_type']]}
                ]
            }
            
            # Add text content if present (for text chunks)
            if 'text' in item:
                datapoint["restricts"].append({
                    "namespace": "text_content",
                    "allow_list": [item['text'][:1000]]  # Limit to 1000 chars
                })
            
            datapoints.append(datapoint)
        
        try:
            # Upsert batch
            index.upsert_datapoints(datapoints=datapoints)
            
            upserted_ids.extend([item['vector_id'] for item in batch])
            print(f"✓ Upserted batch {i//batch_size + 1}/{(len(embeddings)-1)//batch_size + 1}")
        
        except Exception as e:
            print(f"Error upserting batch: {e}")
            # Continue with next batch (partial success)
            print("Continuing with next batch...")
    
    print(f"Successfully upserted {len(upserted_ids)} vectors")
    return upserted_ids

def main():
    print("=" * 60)
    print("JOB 3: UPSERT TO VECTOR INDEX")
    print("=" * 60)
    
    # Get environment variables
    run_id = os.environ.get('RUN_ID')
    output_dir = os.environ.get('OUTPUT_DIR')
    mode = os.environ.get('MODE')
    text_chunks_file = os.environ.get('TEXT_CHUNKS_FILE')
    image_chunks_file = os.environ.get('IMAGE_CHUNKS_FILE')
    project_id = os.environ.get('GCP_PROJECT')
    region = os.environ.get('GCP_REGION', 'us-central1')
    
    # Get index IDs from environment
    text_index_id = os.environ.get('TEXT_INDEX_ID')
    multimodal_index_id = os.environ.get('MULTIMODAL_INDEX_ID')
    
    if not all([run_id, output_dir, project_id]):
        raise ValueError("Missing required environment variables")
    
    if not text_chunks_file and not image_chunks_file:
        raise ValueError("No chunk files provided")
    
    print(f"Run ID: {run_id}")
    print(f"Output directory: {output_dir}")
    
    processed_bucket = f"embed-search-processed-bucket"
    
    text_vector_ids = []
    image_vector_ids = []
    
    try:
        # Process text chunks
        if text_chunks_file and text_index_id:
            print("\n" + "=" * 60)
            print("PROCESSING TEXT EMBEDDINGS")
            print("=" * 60)
            
            print(f"Reading text chunks from: {text_chunks_file}")
            text_embeddings = read_from_gcs(text_chunks_file)
            
            text_vector_ids = upsert_to_index(
                embeddings=text_embeddings,
                index_id=text_index_id,
                index_type="text"
            )
            
            # Store vector IDs for search later
            text_vectors_output = {
                'run_id': run_id,
                'index_id': text_index_id,
                'index_type': 'text',
                'vector_count': len(text_vector_ids),
                'vector_ids': text_vector_ids,
                'upserted_at': datetime.utcnow().isoformat()
            }
            
            write_to_gcs(
                bucket_name=processed_bucket,
                file_path=f"{output_dir}/vectors/text_vector_ids.json",
                data=text_vectors_output
            )
        
        # Process image chunks
        if image_chunks_file and multimodal_index_id:
            print("\n" + "=" * 60)
            print("PROCESSING IMAGE EMBEDDINGS")
            print("=" * 60)
            
            print(f"📖 Reading image chunks from: {image_chunks_file}")
            image_embeddings = read_from_gcs(image_chunks_file)
            
            image_vector_ids = upsert_to_index(
                embeddings=image_embeddings,
                index_id=multimodal_index_id,
                index_type="multimodal"
            )
            
            # Store vector IDs for search later
            image_vectors_output = {
                'run_id': run_id,
                'index_id': multimodal_index_id,
                'index_type': 'multimodal',
                'vector_count': len(image_vector_ids),
                'vector_ids': image_vector_ids,
                'upserted_at': datetime.utcnow().isoformat()
            }
            
            write_to_gcs(
                bucket_name=processed_bucket,
                file_path=f"{output_dir}/vectors/image_vector_ids.json",
                data=image_vectors_output
            )
        
        # Summary
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)
        print(f"Text vectors upserted: {len(text_vector_ids)}")
        print(f"Image vectors upserted: {len(image_vector_ids)}")
        print(f"Total vectors: {len(text_vector_ids) + len(image_vector_ids)}")
    
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
