
import os
import sys
import json
from datetime import datetime
from typing import List, Dict
import tiktoken
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.vision_models import MultiModalEmbeddingModel, Image
import vertexai

# Add shared utilities to path
sys.path.insert(0, '/app/shared')
from utils import (
    read_from_gcs, read_bytes_from_gcs, write_to_gcs,
    trigger_job, delete_gcs_directory, gcs_file_exists
)

# Initialize Vertex AI
project_id = os.environ.get('GCP_PROJECT')
region = os.environ.get('GCP_REGION', 'us-central1')
vertexai.init(project=project_id, location=region)

# Token encoder
encoding = tiktoken.get_encoding("cl100k_base")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    """Chunk text into overlapping segments"""
    tokens = encoding.encode(text)
    chunks = []
    
    start = 0
    chunk_index = 0
    
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        
        chunks.append({
            'chunk_index': chunk_index,
            'text': chunk_text,
            'token_count': len(chunk_tokens),
            'start_token': start,
            'end_token': end
        })
        
        chunk_index += 1
        start = end - overlap
    
    return chunks


def embed_text_chunks(chunks: List[Dict], source_info: Dict) -> List[Dict]:
    """Embed text chunks using text-embedding-004"""
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    
    print(f"Embedding {len(chunks)} text chunks...")
    
    # Batch by token count 
    max_tokens_per_batch = 15000 
    embedded_chunks = []
    
    current_batch = []
    current_token_count = 0
    batch_number = 1
    
    for chunk in chunks:
        chunk_tokens = chunk['token_count']
        
        # If adding this chunk would exceed limit, process current batch first
        if current_token_count + chunk_tokens > max_tokens_per_batch and current_batch:
            # Process current batch
            try:
                texts = [c['text'] for c in current_batch]
                inputs = [TextEmbeddingInput(text=text, task_type="RETRIEVAL_DOCUMENT") for text in texts]
                
                print(f"Embedding batch {batch_number} ({len(current_batch)} chunks, {current_token_count} tokens)...")
                embeddings = model.get_embeddings(inputs)
                
                for c, embedding in zip(current_batch, embeddings):
                    embedded_chunks.append({
                        'vector_id': f"{source_info['run_id']}_text_chunk_{c['chunk_index']}",
                        'text': c['text'],
                        'embedding': embedding.values,
                        'metadata': {
                            'filename': source_info['filename'],
                            'generation': source_info['generation'],
                            'source_type': source_info['type'],
                            'chunk_index': c['chunk_index'],
                            'token_count': c['token_count'],
                            'upload_timestamp': source_info['upload_timestamp'],
                            'gcs_source': source_info['gcs_path']
                        }
                    })
                
                print(f"Batch {batch_number} complete ({len(current_batch)} chunks embedded)")
                batch_number += 1
            
            except Exception as e:
                print(f"Error embedding batch {batch_number}: {e}")
                raise
            
            # Reset batch
            current_batch = []
            current_token_count = 0
        
        # Add chunk to current batch
        current_batch.append(chunk)
        current_token_count += chunk_tokens
    
    # Process final batch
    if current_batch:
        try:
            texts = [c['text'] for c in current_batch]
            inputs = [TextEmbeddingInput(text=text, task_type="RETRIEVAL_DOCUMENT") for text in texts]
            
            print(f"Embedding batch {batch_number} ({len(current_batch)} chunks, {current_token_count} tokens)...")
            embeddings = model.get_embeddings(inputs)
            
            for c, embedding in zip(current_batch, embeddings):
                embedded_chunks.append({
                    'vector_id': f"{source_info['run_id']}_text_chunk_{c['chunk_index']}",
                    'text': c['text'],
                    'embedding': embedding.values,
                    'metadata': {
                        'filename': source_info['filename'],
                        'generation': source_info['generation'],
                        'source_type': source_info['type'],
                        'chunk_index': c['chunk_index'],
                        'token_count': c['token_count'],
                        'upload_timestamp': source_info['upload_timestamp'],
                        'gcs_source': source_info['gcs_path']
                    }
                })
            
            print(f"Batch {batch_number} complete ({len(current_batch)} chunks embedded)")
        
        except Exception as e:
            print(f"Error embedding final batch: {e}")
            raise
    
    print(f"Total embedded: {len(embedded_chunks)} chunks across {batch_number} batches")
    return embedded_chunks

def embed_images(images: List[Dict], source_info: Dict) -> List[Dict]:
    """Embed images using multimodal-embedding"""
    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")
    
    print(f"🖼️  Embedding {len(images)} images...")
    
    embedded_images = []
    
    for img_data in images:
        try:
            # Read image from GCS
            image_bytes = read_bytes_from_gcs(img_data['gcs_path'])
            image = Image(image_bytes=image_bytes)
            
            # Get embedding
            embeddings = model.get_embeddings(image=image)
            
            embedded_images.append({
                'vector_id': f"{source_info['run_id']}_img_{img_data['image_index']}",
                'embedding': embeddings.image_embedding,
                'metadata': {
                    'filename': source_info['filename'],
                    'generation': source_info['generation'],
                    'source_type': f"{source_info['type']}_image",
                    'image_index': img_data['image_index'],
                    'image_gcs_path': img_data['gcs_path'],
                    'dimensions': img_data['dimensions'],
                    'page_number': img_data.get('page'),
                    'upload_timestamp': source_info['upload_timestamp'],
                    'gcs_source': source_info['gcs_path']
                }
            })
            
            print(f"✓ Embedded image {img_data['image_index'] + 1}/{len(images)}")
        
        except Exception as e:
            print(f"❌ Error embedding image {img_data['image_index']}: {e}")
            raise
    
    return embedded_images

def main():
    print("=" * 60)
    print("JOB 2: CHUNK & EMBED")
    print("=" * 60)
    
    # Get environment variables
    parsed_file = os.environ.get('PARSED_FILE')
    mode = os.environ.get('MODE')
    run_id = os.environ.get('RUN_ID')
    output_dir = os.environ.get('OUTPUT_DIR')
    project_id = os.environ.get('GCP_PROJECT')
    region = os.environ.get('GCP_REGION', 'us-central1')
    
    if not all([parsed_file, mode, run_id, output_dir, project_id]):
        raise ValueError("Missing required environment variables")
    
    print(f"Parsed file: {parsed_file}")
    print(f"Mode: {mode}")
    print(f"Run ID: {run_id}")
    
    processed_bucket = f"embed-search-processed-bucket"
    
    # Check if output already exists (idempotency)
    text_output_path = f"gs://{processed_bucket}/{output_dir}/chunked/text_chunks_embeddings.json"
    image_output_path = f"gs://{processed_bucket}/{output_dir}/chunked/image_chunks_embeddings.json"
    
    if gcs_file_exists(text_output_path) or gcs_file_exists(image_output_path):
        print("Chunked embeddings already exist, using cached version")
        
        # Trigger Job 3 with existing files
        env_vars = {
            'RUN_ID': run_id,
            'OUTPUT_DIR': output_dir,
            'MODE': mode,
            'GCP_PROJECT': project_id,
            'GCP_REGION': region
        }
        
        if gcs_file_exists(text_output_path):
            env_vars['TEXT_CHUNKS_FILE'] = text_output_path
        
        if gcs_file_exists(image_output_path):
            env_vars['IMAGE_CHUNKS_FILE'] = image_output_path
        
        trigger_job('ingestion-index-upserter-run', env_vars)
        return
    
    try:
        # Read parsed data
        print("Reading parsed data...")
        parsed_data = read_from_gcs(parsed_file)
        
        source_info = {
            'run_id': run_id,
            'filename': parsed_data['source']['filename'],
            'generation': parsed_data['source']['generation'],
            'gcs_path': parsed_data['source']['gcs_path'],
            'upload_timestamp': parsed_data['source']['upload_timestamp'],
            'type': parsed_data['type']
        }
        
        text_embedded_chunks = []
        image_embedded_chunks = []
        
        # Process based on type
        if parsed_data['type'] == 'text':
            # Pure text file
            print("Chunking text...")
            chunks = chunk_text(parsed_data['content'])
            print(f"Created {len(chunks)} chunks")
            
            text_embedded_chunks = embed_text_chunks(chunks, source_info)
        
        elif parsed_data['type'] == 'image':
            # Standalone image
            image_embedded_chunks = embed_images(parsed_data['images'], source_info)
        
        elif parsed_data['type'] == 'pdf':
            # PDF with text and images
            
            # Chunk text from all pages
            if parsed_data['text_pages']:
                print("Chunking PDF text...")
                all_text = '\n\n'.join([page['text'] for page in parsed_data['text_pages']])
                text_chunks = chunk_text(all_text)
                print(f"Created {len(text_chunks)} text chunks")
                
                # Add page number metadata
                for chunk in text_chunks:
                    # Approximate which pages this chunk covers
                    chunk['pages'] = [page['page'] for page in parsed_data['text_pages']]
                
                text_embedded_chunks = embed_text_chunks(text_chunks, source_info)
            
            # Embed images
            if parsed_data['images']:
                image_embedded_chunks = embed_images(parsed_data['images'], source_info)
        
        # Write outputs to GCS
        if text_embedded_chunks:
            text_output = write_to_gcs(
                bucket_name=processed_bucket,
                file_path=f"{output_dir}/chunked/text_chunks_embeddings.json",
                data=text_embedded_chunks
            )
            print(f"✓ Wrote {len(text_embedded_chunks)} text embeddings")
        
        if image_embedded_chunks:
            image_output = write_to_gcs(
                bucket_name=processed_bucket,
                file_path=f"{output_dir}/chunked/image_chunks_embeddings.json",
                data=image_embedded_chunks
            )
            print(f"Wrote {len(image_embedded_chunks)} image embeddings")
        
        # Trigger Job 3
        env_vars = {
            'RUN_ID': run_id,
            'OUTPUT_DIR': output_dir,
            'MODE': mode,
            'GCP_PROJECT': project_id,
            'GCP_REGION': region
        }
        
        if text_embedded_chunks:
            env_vars['TEXT_CHUNKS_FILE'] = text_output
        
        if image_embedded_chunks:
            env_vars['IMAGE_CHUNKS_FILE'] = image_output
        
        trigger_job('ingestion-index-upserter-run', env_vars)
        
        print("=" * 60)
        print("JOB 2 COMPLETE")
        print("=" * 60)
    
    except Exception as e:
        print(f"ERROR: {e}")
        print("Cleaning up partial outputs...")
        delete_gcs_directory(f"gs://{processed_bucket}/{output_dir}")
        sys.exit(1)

if __name__ == '__main__':
    main()
