FROM python:3.10-slim # intializing python version 3.10 environment

WORKDIR /code # setting working directory for the container

# Install system dependencies required for database compilation
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/* #installing system dependencies for the container

COPY requirements.txt . # copying the requirements.txt file to the container
RUN pip install --no-cache-dir -r requirements.txt # installing the dependencies for the container

COPY . . # copying the entire project to the container

EXPOSE 7860

# 🔥 CRITICAL HUGGING FACE SECURITY FIX:
# Securely mount the Repository Secret to a file path at build-time, 
# extract the string using 'cat', and execute the pipelines smoothly.
RUN --mount=type=secret,id=SUPABASE_DB_URL,mode=0444,required=true \
    SUPABASE_DB_URL=$(cat /run/secrets/SUPABASE_DB_URL) python src/etl_pipeline.py && \
    SUPABASE_DB_URL=$(cat /run/secrets/SUPABASE_DB_URL) python src/train.py

# Serve the FastAPI application on Hugging Face default port 7860
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "7860"]
