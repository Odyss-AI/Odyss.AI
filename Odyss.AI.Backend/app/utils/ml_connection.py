import asyncio
import base64
import requests

from openai import OpenAI
from app.models.enum import ALLOWED_EXTENSIONS
from app.config import config
from app.utils.prompts import summary_prompt_builder
from io import BytesIO
from PIL import Image
from app.models.user import Image

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



async def call_chatgpt_api_async(prompt: list):
    client = OpenAI()

    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = prompt
    )

    return completion.choices[0].message


client = OpenAI(api_key=config.openai_api_key, base_url=config.openai_api_base)


models = client.models.list()
model = models.data[0].id

# Funktion zum Abrufen der Bildklasse vom Image Tagger Service
async def get_image_class_async(image_path):
    with open(image_path, "rb") as image_file:
        response = await requests.post(config.image_tagger, files={"file": image_file})  # URL zum Image Tagger Service
        if response.status_code == 200:
            return response.json().get('tag')  # Rückgabe der Bildklasse
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
# Anfrage an das Pixtral-Modell

async def query_pixtral_async(image:Image):
    # Bildklasse vom Image Tagger holen
    image_class = get_image_class_async(image.link)

    # Bild laden und in Base64 kodieren
    image = Image.open(image.link)
    buffered = BytesIO()
    image.save(buffered, format="PNG")  # Speichern im PNG-Format
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Pixtral-Anfrage mit der eingebetteten Klasse
    chat_completion_from_base64 = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"The image shows a {image_class}. Please describe what I see."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_str}"
                    },
                },
            ],
        }],
        model=model,  # Anpassen an den korrekten Modellnamen
        max_tokens=256,
    )

    # Ergebnis anzeigen
    result = chat_completion_from_base64.choices[0].message.content
    image.llm_output = result
    return image

async def query_mixtral_async(prompt: list):
    # Mixtral-Anfrage mit der eingebetteten Klasse
    chat_completion_from_base64 = client.chat.completions.create(
       messages = prompt,
        model=model,  # Anpassen an den korrekten Modellnamen
        max_tokens=256,
    )

    # Ergebnis anzeigen
    result = chat_completion_from_base64.choices[0].message.content
    
    return result