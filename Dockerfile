# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies if needed for sentence-transformers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Forcing cpu-only installs as not doing this pulls-in all kinds of cuda related dependencies as well
# RUN pip install --no-cache-dir -r requirements.txt -f https://download.pytorch.org/whl/cpu

# RUN pip install --no-cache-dir -f https://download.pytorch.org/whl/cpu torch==2.4.0+cpu torchvision==0.19.0+cpu torchaudio==2.4.0+cpu && pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu


# Copy application code
COPY . .

# Expose the port
EXPOSE 9007

# Create a volume for persistent storage
VOLUME ["/app/data"]

# Set the default storage path to use the volume
ENV STORAGE_PATH=/app/data/tool_embeddings.json

# Run the application
CMD ["python", "app.py", "--transport", "http", "--port", "9007", "--host", "0.0.0.0", "--storage_path", "/app/data/tool_embeddings.json"]
