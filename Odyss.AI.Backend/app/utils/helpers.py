import asyncio

from openai import OpenAI
from app.models.enum import ALLOWED_EXTENSIONS
from mistralai import Mistral
from app.config import Config
from app.utils.prompts import summary_prompt_builder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def call_mistral_api_async(prompt: list):
    api_key = Config.MISTRAL_KEY
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model = model,
        messages = prompt
    )

    return chat_response.choices[0].message.content

async def call_chatgpt_api_async(prompt: list):
    client = OpenAI()

    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = prompt
    )

    return completion.choices[0].message
