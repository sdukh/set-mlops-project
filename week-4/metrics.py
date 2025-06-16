"""
Prometheus metrics for FastAPI LLM application.
This module centralizes all metrics definitions and provides helper functions.
"""

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from datetime import datetime
from typing import Optional


# General API metrics
REQUEST_COUNT = Counter(
    "app_request_count", "Total count of requests", ["endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Request latency in seconds", ["endpoint"]
)
RESPONSE_SIZE = Histogram(
    "app_response_size_bytes", "Response size in bytes", ["endpoint"]
)

# LLM-specific metrics
PROMPT_LENGTH = Histogram(
    "llm_prompt_length_chars", "Length of input prompts in characters", ["model"]
)
RESPONSE_LENGTH = Histogram(
    "llm_response_length_chars", "Length of LLM responses in characters", ["model"]
)
LLM_INFERENCE_TIME = Histogram(
    "llm_inference_time_seconds", "Time taken for LLM inference", ["model"]
)
LLM_REQUESTS_TOTAL = Counter(
    "llm_requests_total", "Total LLM requests", ["model", "status"]
)
LLM_ERRORS = Counter("llm_errors_total", "Total LLM errors", ["model", "error_type"])
ACTIVE_REQUESTS = Gauge(
    "llm_active_requests", "Number of active LLM requests", ["model"]
)
PROMPT_TOKENS_ESTIMATE = Histogram(
    "llm_prompt_tokens_estimate", "Estimated tokens in prompt (chars/4)", ["model"]
)
RESPONSE_TOKENS_ESTIMATE = Histogram(
    "llm_response_tokens_estimate", "Estimated tokens in response (chars/4)", ["model"]
)


def record_request_start(model_name: str, prompt_length: int) -> None:
    """Record metrics when a request starts."""
    ACTIVE_REQUESTS.labels(model=model_name).inc()
    PROMPT_LENGTH.labels(model=model_name).observe(prompt_length)
    PROMPT_TOKENS_ESTIMATE.labels(model=model_name).observe(prompt_length / 4)


def record_request_success(
    model_name: str, inference_time: float, response_length: int, prompt_length: int
) -> None:
    """Record metrics for a successful request."""
    # General API metrics
    REQUEST_COUNT.labels(endpoint="/generate", status="success").inc()
    REQUEST_LATENCY.labels(endpoint="/generate").observe(inference_time)
    RESPONSE_SIZE.labels(endpoint="/generate").observe(response_length)

    # LLM-specific metrics
    LLM_REQUESTS_TOTAL.labels(model=model_name, status="success").inc()
    LLM_INFERENCE_TIME.labels(model=model_name).observe(inference_time)
    RESPONSE_LENGTH.labels(model=model_name).observe(response_length)
    RESPONSE_TOKENS_ESTIMATE.labels(model=model_name).observe(response_length / 4)

    # Decrease active requests
    ACTIVE_REQUESTS.labels(model=model_name).dec()


def record_request_error(
    model_name: str, error_type: str, inference_time: float
) -> None:
    """Record metrics for a failed request."""
    # General API metrics
    REQUEST_COUNT.labels(endpoint="/generate", status="error").inc()
    REQUEST_LATENCY.labels(endpoint="/generate").observe(inference_time)

    # LLM-specific error metrics
    LLM_REQUESTS_TOTAL.labels(model=model_name, status="error").inc()
    LLM_ERRORS.labels(model=model_name, error_type=error_type).inc()
    ACTIVE_REQUESTS.labels(model=model_name).dec()


def get_metrics_response():
    """Generate Prometheus metrics response."""
    return generate_latest(), CONTENT_TYPE_LATEST


def get_current_active_requests(model_name: str) -> float:
    """Get current number of active requests for a model."""
    return ACTIVE_REQUESTS.labels(model=model_name)._value._value
