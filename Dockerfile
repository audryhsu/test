FROM ghcr.io/remsky/kokoro-fastapi-gpu:latest

USER root

# Install pip (just in case)
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Activate venv and install ALL required packages
RUN . /app/.venv/bin/activate && \
    uv pip install --no-cache \
        runpod \
        pydub \
        nest-asyncio \
        azure-storage-blob==12.23.1 
        # google-generativeai

WORKDIR /app

# Copy the fine-tuned homograph model files (directly from models folder in repo)
COPY models /app/models

# Copy your final private handler.py
COPY handler.py .

EXPOSE 8000

CMD ["python", "-u", "handler.py"]
