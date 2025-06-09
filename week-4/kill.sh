#!/bin/bash

echo "Stopping services..."

# Kill FastAPI server
pkill -f "uvicorn app:app" || true

# Kill Telegram bot
pkill -f "python bot.py" || true

# Kill Ollama (only if it was started by our start.sh)
if pgrep -f "ollama serve" > /dev/null; then
    echo "Stopping Ollama service..."
    pkill -f "ollama serve" || true
fi

echo "All services stopped" 