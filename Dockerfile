# Initialize python version 3.10 environment
FROM python:3.10-slim

# Set working directory for the container
WORKDIR /code

# Install system dependencies required for database compilation
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies for the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

EXPOSE 7860

# 🔥 CRITICAL HUGGING FACE SECURITY FIX:
# Securely mount the Repository Secret to a file path at build-time, 
# extract the string using 'cat', and execute the pipelines smoothly.
RUN --mount=type=secret,id=SUPABASE_DB_URL,mode=0444,required=true \
    SUPABASE_DB_URL=$(cat /run/secrets/SUPABASE_DB_URL) python src/etl_pipeline.py && \
    SUPABASE_DB_URL=$(cat /run/secrets/SUPABASE_DB_URL) python src/train.py

# Serve the FastAPI application on Hugging Face default port 7860
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "7860"]

