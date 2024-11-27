import asyncio
import base64
import requests
import json
import aiohttp

from tqdm import tqdm
from openai import OpenAI
from sshtunnel import SSHTunnelForwarder
from app.models.enum import ALLOWED_EXTENSIONS
from app.config import config
from app.utils.prompts import summary_prompt_builder
from io import BytesIO
from PIL import Image as PILImage
from app.models.user import Document
from sshtunnel import SSHTunnelForwarder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def call_chatgpt_api_async(prompt: list):
    client = OpenAI()

    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = prompt
    )

    return completion.choices[0].message

# Funktion zum Abrufen der Bildklasse vom Image Tagger Service
async def get_image_class_async(image_path):
    with open(image_path, "rb") as image_file:
        response = requests.post(config.image_tagger, files={"file": image_file})  # URL zum Image Tagger Service
        if response.status_code == 200:
            return response.json().get('tag')  # Rückgabe der Bildklasse
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

# Anfrage an das Pixtral-Modell
async def query_pixtral_async(doc:Document):
    # OpenAI-API-Einstellungen
    openai_api_key = config.openai_api_key
    openai_api_base = config.openai_api_base  # Pixtral-Modell-URL
    client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)
    # Bildklasse vom Image Tagger holen

    models = client.models.list()
    model = models.data[0].id

    print(model)

    for img in tqdm(doc.imgList, desc="Processing images"):
        image_class = await get_image_class_async(img.link)

        # Wenn die Klasse "just_img" ist, zur nächsten Iteration springen
        if image_class == "just_img":
            continue

        # Bild laden und in Base64 kodieren
        image = PILImage.open(img.link)
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
            model=model,  
            max_tokens=256,
        )

        # Ergebnis anzeigen
        img.llm_output = chat_completion_from_base64.choices[0].message.content

    return doc
    
    

async def query_mixtral_async(prompt: list):
    # Sondertokens definieren
    BOS_ID = "<s>"
    EOS_ID = "</s>"
    INST_ID = "[INST]"
    END_INST_ID = "[/INST]"
    
    # JSON-Format für den API-Aufruf
    data = {
        "inputs": f"{BOS_ID} {INST_ID} {str(prompt)} {END_INST_ID} Model answer {EOS_ID}"
    }
    try:
        # Sende die Anfrage über den Tunnel
        response = requests.post(config.mistral_api_base, json=data)
        
        if response.status_code == 200:
            result = json.loads(response.text)
            answer = result[0]['generated_text']
            return answer
        else:
            print("Fehler beim Abrufen der Antwort:", response.status_code, response.text)

    except Exception as e:
        print("Verbindungsfehler:", e)    
            


# Anfrage an das Pixtral-Modell
async def query_pixtral_with_ssh_async(doc:Document):
    # OpenAI-API-Einstellungen
    openai_api_key = config.openai_api_key
    openai_api_base = config.openai_api_base  # Pixtral-Modell-URL
    client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)
    # Bildklasse vom Image Tagger holen

    with SSHTunnelForwarder(
    (config.ssh_host, config.ssh_port),
    ssh_username=config.ssh_username,
    local_bind_address=('localhost', config.local_port_pixtral),
    remote_bind_address=('localhost', config.remote_port_pixtral)
) as tunnel:
        print(f"SSH-Tunnel hergestellt: localhost:{config.local_port} -> {config.ssh_host}:{config.remote_port}")
        tunnel.start()  # Ensure tunnel is started
        models = client.models.list()
        model = models.data[0].id

        print(model)

        for img in tqdm(doc.imgList, desc="Processing images"):
            image_class = await get_image_class_async(img.link)

            # Wenn die Klasse "just_img" ist, zur nächsten Iteration springen
            if image_class == "just_img":
                continue

            # Bild laden und in Base64 kodieren
            image = PILImage.open(img.link)
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
                model=model,  
                max_tokens=256,
            )

            # Ergebnis anzeigen
            img.llm_output = chat_completion_from_base64.choices[0].message.content

        return doc
    
    

async def query_mixtral_with_ssh_async(prompt: list):
    # Sondertokens definieren
    BOS_ID = "<s>"
    EOS_ID = "</s>"
    INST_ID = "[INST]"
    END_INST_ID = "[/INST]"

    # Prompt-Formatierung
    formatted_prompt = "\n".join([f"{message['role']}: {message['content']}" for message in prompt])
    data = {
        "inputs": f"{BOS_ID} {INST_ID} {formatted_prompt} {END_INST_ID} Model answer {EOS_ID}"
    }

    try:
        # SSH-Tunnel-Forwarder einrichten
        with SSHTunnelForwarder(
            (config.ssh_host, config.ssh_port),
            ssh_username=config.ssh_username,
            local_bind_address=('localhost', config.local_port),
            remote_bind_address=('localhost', config.remote_port)
        ) as tunnel:
            
            print(f"SSH-Tunnel hergestellt: localhost:{config.local_port} -> {config.ssh_host}:{config.remote_port}")

            # Anfrage über den Tunnel senden
            async with aiohttp.ClientSession() as session:
                async with session.post(config.mistral_api_base, json=data) as response:
                    if response.status == 200:
                        try:
                            result = await response.json()
                            if isinstance(result, list) and 'generated_text' in result[0]:
                                return result[0]['generated_text']
                            else:
                                print("Unerwartetes Antwortformat:", result)
                        except Exception as e:
                            print("Fehler beim Verarbeiten der JSON-Antwort:", e)
                    else:
                        print("Fehler beim Abrufen der Antwort:", response.status, await response.text())

    except Exception as e:
        print("Verbindungsfehler:", e) 