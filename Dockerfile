FROM python:3.10-slim

WORKDIR /code

# Install system dependencies required for database compilation
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 🔥 CRITICAL FIX: Explicitly bind the secret into the build engine state context
ARG SUPABASE_DB_URL
ENV SUPABASE_DB_URL=$SUPABASE_DB_URL

# Now the script can read the variable during compilation
RUN python src/etl_pipeline.py && python src/train.py

EXPOSE 7860

# Serve the FastAPI application on Hugging Face default port 7860
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "7860"]
