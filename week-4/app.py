from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
import json
from pathlib import Path
import wandb
from datetime import datetime

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

# Initialize W&B
wandb.init(
    project=os.getenv("WANDB_PROJECT"),
    config={
        "model": MODEL_NAME,
        "system_prompt": SYSTEM_PROMPT,
    },
)


class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate")
async def generate_text(req: PromptRequest):
    start_time = datetime.now()
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

            # Log metrics to W&B
            end_time = datetime.now()
            inference_time = (end_time - start_time).total_seconds()
            response_length = len(data.get("response", ""))

            wandb.log(
                {
                    "inference_time": inference_time,
                    "response_length": response_length,
                    "prompt_length": len(req.prompt),
                    "timestamp": datetime.now().isoformat(),
                }
            )

            return {"response": data.get("response", "No output")}
    except httpx.HTTPError as e:
        error_msg = f"HTTP error occurred: {str(e)}"
        if hasattr(e, "response") and e.response is not None:
            try:
                error_detail = e.response.json()
                error_msg = f"Ollama API error: {error_detail}"
            except:
                error_msg = f"Ollama API error: {e.response.text}"

        # Log error to W&B
        wandb.log({"error": error_msg, "timestamp": datetime.now().isoformat()})

        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        # Log unexpected errors to W&B
        wandb.log({"error": str(e), "timestamp": datetime.now().isoformat()})

        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    wandb.finish()
