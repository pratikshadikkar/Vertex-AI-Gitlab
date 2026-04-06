FROM python:3.11-slim

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    mupdf-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy shared utilities
COPY shared /app/shared/

# Copy job-specific code
COPY cloud-run/ingestion-validator-parser-run/main.py /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/shared/requirements.txt

CMD ["python", "main.py"]
