# 🤖 LLM Inference: FastAPI + Ollama + Telegram Bot

A local LLM service using Gemma 3B via Ollama, exposed through FastAPI and accessible via Telegram bot.

## 🚀 Features

- 🔍 FastAPI inference endpoint
- 🧠 Gemma 3B via Ollama
- 💬 Telegram bot interface
- 🐳 Docker containerization

## 📁 Project Structure

```
gemma-llm-inference/
├── app.py             # FastAPI wrapper
├── bot.py             # Telegram bot
├── requirements.txt   # Dependencies
├── Dockerfile         # Container config
├── start.sh           # Start script
```

## 🧪 Setup

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com)
- Telegram bot token ([@BotFather](https://t.me/BotFather))

### Installation

1. Pull Gemma model:
```bash
ollama pull gemma:3b
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export TELEGRAM_API_TOKEN=your_bot_token_here
```

### Running the Service

1. Start FastAPI:
```bash
uvicorn app:app --reload --port 10000
```

2. Start Telegram bot:
```bash
python bot.py
```

Or use the start script:
```bash
chmod +x start.sh
./start.sh
```

## 📬 API Reference

**POST** `/generate`

Request:
```json
{
  "prompt": "Tell me a joke about Berlin."
}
```

Response:
```json
{
  "response": "Why did the Berliner refuse to jaywalk? Because they follow ze rules!"
}
```

## 🧰 Tech Stack

- Gemma 3B (Ollama)
- FastAPI
- Telegram (Aiogram)
- Docker

## 📄 License

MIT

## 🤝 Contributing

Contributions welcome — feel free to fork, PR, or submit issues!
