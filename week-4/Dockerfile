FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make scripts executable
RUN chmod +x start.sh kill.sh

ENV PORT=10000
ENV FASTAPI_URL=http://localhost:10000/generate

EXPOSE $PORT

# Use shell form to allow environment variable substitution
CMD ./start.sh
