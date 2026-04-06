FROM python:3.11-slim

WORKDIR /app

# Copy shared utilities
COPY shared /app/shared/

# Copy job-specific code
COPY cloud-run/ingestion-chunker-embedder-run/main.py /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/shared/requirements.txt

CMD ["python", "main.py"]
