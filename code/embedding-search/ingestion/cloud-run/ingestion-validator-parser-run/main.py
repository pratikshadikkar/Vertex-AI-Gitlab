# Cloud run job-1 to validate and parse the incoming file in GCS bucket
import os
import sys
import json
from datetime import datetime
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io


# Add shared utilities to path
sys.path.insert(0, '/app/shared')
from utils import (
    sanitize_filename, get_run_id, parse_gcs_path,
    write_to_gcs, write_bytes_to_gcs, read_bytes_from_gcs,
    trigger_job, get_file_metadata, delete_gcs_directory
)

def validate_text_file(file_content: bytes) -> dict:
    """Validate .txt file"""
    try:
        # Try to decode as UTF-8
        text = file_content.decode('utf-8')
        
        return {
            'valid': True,
            'encoding': 'utf-8',
            'char_count': len(text),
            'line_count': text.count('\n') + 1
        }
    except UnicodeDecodeError:
        return {
            'valid': False,
            'error': 'File is not valid UTF-8'
        }

def parse_text_file(file_content: bytes, metadata: dict) -> dict:
    """Parse .txt file"""
    text = file_content.decode('utf-8')
    
    return {
        'type': 'text',
        'content': text,
        'metadata': {
            'char_count': len(text),
            'line_count': text.count('\n') + 1,
            'encoding': 'utf-8'
        }
    }

def validate_image_file(file_content: bytes) -> dict:
    """Validate .jpg/.jpeg file"""
    try:
        image = Image.open(io.BytesIO(file_content))
        
        return {
            'valid': True,
            'format': image.format,
            'dimensions': f"{image.width}x{image.height}",
            'mode': image.mode
        }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

def parse_image_file(file_content: bytes, metadata: dict, output_dir: str, bucket_name: str) -> dict:
    """Parse standalone image file"""
    image = Image.open(io.BytesIO(file_content))
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Save to processed bucket
    img_buffer = io.BytesIO()
    image.save(img_buffer, format='JPEG', quality=95)
    img_bytes = img_buffer.getvalue()
    
    image_path = f"{output_dir}/images/image_0.jpg"
    image_gcs_path = write_bytes_to_gcs(bucket_name, image_path, img_bytes, 'image/jpeg')
    
    return {
        'type': 'image',
        'images': [{
            'image_index': 0,
            'gcs_path': image_gcs_path,
            'dimensions': f"{image.width}x{image.height}"
        }],
        'metadata': {
            'format': image.format,
            'dimensions': f"{image.width}x{image.height}",
            'mode': image.mode
        }
    }

def validate_pdf_file(file_content: bytes) -> dict:
    """Validate PDF file"""
    try:
        doc = fitz.open(stream=file_content, filetype="pdf")
        
        return {
            'valid': True,
            'page_count': len(doc),
            'metadata': doc.metadata
        }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

def parse_pdf_file(file_content: bytes, metadata: dict, output_dir: str, bucket_name: str) -> dict:
    """Parse PDF - extract text and images"""

    doc = fitz.open(stream=file_content, filetype="pdf")
    all_text = []
    images = []
    image_counter = 0
    total_pages = len(doc)
    for page_num in range(len(doc)):
        page = doc[page_num]
        # Extract text
        page_text = page.get_text()
        if page_text.strip():
            all_text.append({
                'page': page_num + 1,
                'text': page_text
            })
        
        # Extract images
        image_list = page.get_images()
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            # Convert to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            # Save to GCS
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='JPEG', quality=95)
            img_bytes = img_buffer.getvalue()
            image_path = f"{output_dir}/images/page_{page_num + 1}_img_{img_index}.jpg"
            image_gcs_path = write_bytes_to_gcs(bucket_name, image_path, img_bytes, 'image/jpeg')
            images.append({
                'image_index': image_counter,
                'page': page_num + 1,
                'gcs_path': image_gcs_path,
                'dimensions': f"{image.width}x{image.height}"
            })
            image_counter += 1
    doc.close()
    return {
        'type': 'pdf',
        'text_pages': all_text,
        'images': images,
        'metadata': {
            'page_count': total_pages,
            'text_page_count': len(all_text),
            'image_count': len(images)
        }
    }
    


def main():
    print("=" * 60)
    print("JOB 1: VALIDATE & PARSE")
    print("=" * 60)
    
    # Get environment variables
    input_file = os.environ.get('INPUT_FILE')
    if not input_file:
        raise ValueError("INPUT_FILE environment variable not set")
    
    project_id = os.environ.get('GCP_PROJECT')
    region = os.environ.get('GCP_REGION', 'us-central1')
    
    print(f"Input: {input_file}")
    
    # Determine mode (text or multi) from path
    if '/text/' in input_file:
        mode = 'text'
    elif '/multi/' in input_file:
        mode = 'multi'
    else:
        raise ValueError("Cannot determine mode from path (must contain /text/ or /multi/)")
    
    print(f"Mode: {mode}")
    
    # Get file metadata
    file_metadata = get_file_metadata(input_file)
    filename = input_file.split('/')[-1]
    generation = file_metadata['generation']
    
    print(f"Filename: {filename}")
    print(f"Generation: {generation}")
    
    # Generate run ID and output directory
    run_id = get_run_id(filename, generation)
    processed_bucket = f"embed-search-processed-bucket"
    output_dir = f"{mode}/{run_id}"
    
    print(f"Output directory: {output_dir}")
    
    try:
        # Read file from GCS
        print("Reading file from GCS...")
        file_content = read_bytes_from_gcs(input_file)
        
        # Determine file type
        file_ext = Path(filename).suffix.lower()
        
        # Validate and parse based on file type
        if file_ext == '.txt':
            print("Validating text file...")
            validation = validate_text_file(file_content)
            
            if not validation['valid']:
                raise Exception(f"Validation failed: {validation['error']}")
            
            print("Validation passed")
            print("Parsing text file...")
            parsed_data = parse_text_file(file_content, file_metadata)
        
        elif file_ext in ['.jpg', '.jpeg']:
            print("Validating image file...")
            validation = validate_image_file(file_content)
            
            if not validation['valid']:
                raise Exception(f"Validation failed: {validation['error']}")
            
            print("✓ Validation passed")
            print("⚙️  Parsing image file...")
            parsed_data = parse_image_file(file_content, file_metadata, output_dir, processed_bucket)
        
        elif file_ext == '.pdf':
            print("Validating PDF file...")
            validation = validate_pdf_file(file_content)
            
            if not validation['valid']:
                raise Exception(f"Validation failed: {validation['error']}")
            
            print("✓ Validation passed")
            print(f"📄 PDF has {validation['page_count']} pages")
            print("⚙️  Parsing PDF (extracting text and images)...")
            parsed_data = parse_pdf_file(file_content, file_metadata, output_dir, processed_bucket)
            print(f"✓ Extracted text from {parsed_data['metadata']['text_page_count']} pages")
            print(f"✓ Extracted {parsed_data['metadata']['image_count']} images")
        
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Add common metadata
        parsed_data['source'] = {
            'filename': filename,
            'generation': generation,
            'gcs_path': input_file,
            'upload_timestamp': file_metadata['created'],
            'file_size': file_metadata['size']
        }
        
        # Write parsed data to GCS
        parsed_path = write_to_gcs(
            bucket_name=processed_bucket,
            file_path=f"{output_dir}/parsed/content.json",
            data=parsed_data
        )
        
        # Trigger Job 2
        trigger_job(
            job_name='ingestion-chunker-embedder-run',
            env_vars={
                'PARSED_FILE': parsed_path,
                'MODE': mode,
                'RUN_ID': run_id,
                'OUTPUT_DIR': output_dir,
                'GCP_PROJECT': project_id,
                'GCP_REGION': region
            }
        )
        
        print("=" * 60)
        print("JOB 1 COMPLETE")
        print("=" * 60)
    
    except Exception as e:
        print(f"ERROR: {e}")
        print("Cleaning up partial outputs...")
        delete_gcs_directory(f"gs://{processed_bucket}/{output_dir}")
        sys.exit(1)

if __name__ == '__main__':
    main()
