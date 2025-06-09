import os
import asyncio
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
if not API_TOKEN:
    raise ValueError(
        "TELEGRAM_API_TOKEN environment variable is not set. "
        "Please set it in your .env file or environment."
    )

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:10000/generate")


@dp.message()
async def handle_message(message: Message):
    prompt = message.text
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(FASTAPI_URL, json={"prompt": prompt})
            reply = res.json().get("response", "No response")
        except Exception as e:
            reply = f"Error: {str(e)}"
    await message.reply(reply)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
