#!/bin/bash

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Check for required environment variables
if [ -z "$WANDB_API_KEY" ]; then
    echo "ERROR: WANDB_API_KEY environment variable is not set"
    echo "Please set WANDB_API_KEY in your .env file or environment"
    exit 1
fi

if [ -z "$WANDB_PROJECT" ]; then
    echo "ERROR: WANDB_PROJECT environment variable is not set"
    echo "Please set WANDB_PROJECT in your .env file or environment"
    exit 1
fi

# Function to check if a service is ready
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    local max_attempts=30
    local attempt=1

    echo "Waiting for $service to be ready..."
    while ! curl -s "http://$host:$port/api/tags" > /dev/null; do
        if [ $attempt -eq $max_attempts ]; then
            echo "$service failed to start after $max_attempts attempts"
            exit 1
        fi
        echo "Waiting for $service... (attempt $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    echo "$service is ready!"
}

# Check if we're running in Docker
if [ -f /.dockerenv ]; then
    # In Docker, wait for Ollama to be ready
    wait_for_service ollama 11434 "Ollama"
else
    # Outside Docker, wait for Ollama to be ready
    wait_for_service localhost 11434 "Ollama"
fi

# Check if model is available and pull if needed
MODEL_NAME=${LLM_MODEL:-"gemma3:1b"}
if ! curl -s http://ollama:11434/api/tags | grep -q "\"name\":\"$MODEL_NAME\""; then
    echo "Pulling $MODEL_NAME model..."
    curl -X POST http://ollama:11434/api/pull -d "{\"name\": \"$MODEL_NAME\"}"
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to pull model $MODEL_NAME"
        exit 1
    fi
    echo "Model pulled successfully"
else
    echo "Model $MODEL_NAME already exists"
fi

# Verify config.json exists
if [ ! -f "config.json" ]; then
    echo "ERROR: config.json not found"
    exit 1
fi

# Start FastAPI server
echo "Starting FastAPI server..."
uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}