from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
import json
from pathlib import Path

from datetime import datetime
from starlette.responses import Response
from metrics import (
    record_request_start,
    record_request_success,
    record_request_error,
    get_metrics_response,
)

app = FastAPI()

# Load configuration
CONFIG_PATH = Path("config.json")
DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."
DEFAULT_MODEL = "gemma3:1b"

# Load model name from environment variable with fallback
MODEL_NAME = os.getenv("LLM_MODEL", DEFAULT_MODEL)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")


def load_system_prompt():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                config = json.load(f)
                return config.get("system_prompt", DEFAULT_SYSTEM_PROMPT)
        except Exception as e:
            print(f"Error loading config: {e}")
            return DEFAULT_SYSTEM_PROMPT
    return DEFAULT_SYSTEM_PROMPT


SYSTEM_PROMPT = load_system_prompt()


class PromptRequest(BaseModel):
    prompt: str


@app.get("/metrics")
async def metrics():
    content, media_type = get_metrics_response()
    return Response(content, media_type=media_type)


@app.get("/health")
async def health_check():
    """Health check endpoint with LLM service status"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "llm_service": "available",
                    "model": MODEL_NAME,
                    "timestamp": datetime.now().isoformat(),
                }
            else:
                return {
                    "status": "degraded",
                    "llm_service": "unavailable",
                    "model": MODEL_NAME,
                    "timestamp": datetime.now().isoformat(),
                }
    except Exception as e:
        return {
            "status": "unhealthy",
            "llm_service": "error",
            "error": str(e),
            "model": MODEL_NAME,
            "timestamp": datetime.now().isoformat(),
        }


@app.get("/model-info")
async def model_info():
    """Get information about the current LLM model"""
    return {
        "model_name": MODEL_NAME,
        "ollama_url": OLLAMA_URL,
        "system_prompt": (
            SYSTEM_PROMPT[:100] + "..." if len(SYSTEM_PROMPT) > 100 else SYSTEM_PROMPT
        ),
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/generate")
async def generate_text(req: PromptRequest):
    start_time = datetime.now()
    prompt_length = len(req.prompt)

    # Record request start metrics
    record_request_start(MODEL_NAME, prompt_length)

    ollama_payload = {
        "model": MODEL_NAME,
        "prompt": req.prompt,
        "stream": False,
        "system": SYSTEM_PROMPT,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate", json=ollama_payload
            )
            response.raise_for_status()
            data = response.json()

            end_time = datetime.now()
            inference_time = (end_time - start_time).total_seconds()
            response_text = data.get("response", "")
            response_length = len(response_text)

            # Record successful request metrics
            record_request_success(
                MODEL_NAME, inference_time, response_length, prompt_length
            )

            return {"response": response_text}
    except httpx.HTTPError as e:
        error_msg = f"HTTP error occurred: {str(e)}"
        error_type = "http_error"

        if hasattr(e, "response") and e.response is not None:
            try:
                error_detail = e.response.json()
                error_msg = f"Ollama API error: {error_detail}"
                error_type = "ollama_api_error"
            except:
                error_msg = f"Ollama API error: {e.response.text}"
                error_type = "ollama_response_error"

        # Record error metrics
        inference_time = (datetime.now() - start_time).total_seconds()
        record_request_error(MODEL_NAME, error_type, inference_time)

        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        # Record error metrics
        inference_time = (datetime.now() - start_time).total_seconds()
        record_request_error(MODEL_NAME, "unexpected_error", inference_time)

        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
