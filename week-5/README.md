# FastAPI Monitoring Stack

This directory contains a complete monitoring setup for your FastAPI application using Prometheus and Grafana.

## Services

- **FastAPI App**: Your main application (port 10000)
- **Ollama**: LLM service (port 11434)
- **Prometheus**: Metrics collection (port 9090)
- **Grafana**: Metrics visualization (port 3000)

## Quick Start

1. **Start the stack**:
   ```bash
   cd week-5
   docker-compose up --build
   ```

2. **Access the services**:
   - FastAPI App: http://localhost:10000
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000

## Setting up Grafana Dashboard

### Step 1: Login to Grafana
1. Go to http://localhost:3000
2. Login with: `admin` / `admin`
3. You'll be prompted to change the password (optional)

### Step 2: Add Prometheus Data Source
1. Click on **Configuration** (gear icon) → **Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Set URL to: `http://prometheus:9090`
5. Click **Save & Test** (should show "Data source is working")

### Step 3: Create Dashboard Panels Manually
1. Click on **+** (plus icon) → **Create** → **Dashboard**
2. Click **Add visualization**
3. Select your Prometheus data source
4. Create panels using the queries below

## Create Your Dashboard

You can create custom panels based on your monitoring needs using the available metrics and Prometheus queries listed below.

## Testing the Metrics

Generate some traffic to see metrics:

```bash
# Send some requests to your FastAPI app
curl -X POST http://localhost:10000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?"}'

# Check metrics endpoint
curl http://localhost:10000/metrics
```

## Prometheus Queries

You can use these queries in Prometheus or Grafana:

### General API Queries
- **Request rate**: `rate(app_request_count_total[5m])`
- **Error rate**: `rate(app_request_count_total{status="error"}[5m]) / rate(app_request_count_total[5m]) * 100`
- **Latency 95th percentile**: `histogram_quantile(0.95, rate(app_request_latency_seconds_bucket[5m]))`
- **Average response size**: `rate(app_response_size_bytes_sum[5m]) / rate(app_response_size_bytes_count[5m])`

### LLM-Specific Queries
- **LLM request rate**: `rate(llm_requests_total[5m])`
- **LLM error rate**: `rate(llm_errors_total[5m])`
- **Average inference time**: `rate(llm_inference_time_seconds_sum[5m]) / rate(llm_inference_time_seconds_count[5m])`
- **Inference time 95th percentile**: `histogram_quantile(0.95, rate(llm_inference_time_seconds_bucket[5m]))`
- **Average prompt length**: `rate(llm_prompt_length_chars_sum[5m]) / rate(llm_prompt_length_chars_count[5m])`
- **Average response length**: `rate(llm_response_length_chars_sum[5m]) / rate(llm_response_length_chars_count[5m])`
- **Estimated tokens per second (input)**: `rate(llm_prompt_tokens_estimate_sum[5m])`
- **Estimated tokens per second (output)**: `rate(llm_response_tokens_estimate_sum[5m])`
- **Active LLM requests**: `llm_active_requests`
- **Error breakdown by type**: `rate(llm_errors_total[5m]) by (error_type)`

## Available Metrics

Your FastAPI app exposes these Prometheus metrics:

### General API Metrics
- `app_request_count_total` - Total number of requests (labeled by endpoint and status)
- `app_request_latency_seconds` - Request latency histogram
- `app_response_size_bytes` - Response size histogram

### LLM-Specific Metrics
- `llm_requests_total` - Total LLM requests (labeled by model and status)
- `llm_inference_time_seconds` - Time taken for LLM inference (labeled by model)
- `llm_prompt_length_chars` - Length of input prompts in characters (labeled by model)
- `llm_response_length_chars` - Length of LLM responses in characters (labeled by model)
- `llm_prompt_tokens_estimate` - Estimated tokens in prompt (chars/4, labeled by model)
- `llm_response_tokens_estimate` - Estimated tokens in response (chars/4, labeled by model)
- `llm_errors_total` - Total LLM errors (labeled by model and error_type)
- `llm_active_requests` - Number of currently active LLM requests (labeled by model)

## Troubleshooting

1. **No data in Grafana**: 
   - Check that Prometheus is scraping your app: http://localhost:9090/targets
   - Verify metrics endpoint: http://localhost:10000/metrics

2. **Connection issues**:
   - Ensure all services are in the same Docker network
   - Check service names in docker-compose.yml

3. **Dashboard not showing data**:
   - Verify the time range in Grafana (top right)
   - Generate some requests to create metrics
   - Check Prometheus data source configuration 