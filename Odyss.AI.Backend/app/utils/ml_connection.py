import asyncio
import base64
import requests
import paramiko
import logging
import json

from openai import OpenAI
from sshtunnel import SSHTunnelForwarder
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


# client = OpenAI(api_key=config.openai_api_key, base_url=config.openai_api_base)

#SSH-Verbindungsdetailss
ssh_host = "141.75.89.10"
ssh_port = 22
ssh_username = "oppelfe89127"
local_port = 8093
remote_port = 8093

# Funktion zum Einrichten des SSH-Tunnels
def create_ssh_tunnel():     
    client = paramiko.SSHClient()    
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
    client.connect(ssh_host, port=ssh_port, username=ssh_username)     
    stdin, stdout, stderr = client.exec_command("echo Test")
    if stdout.read().decode().strip() == "Test":
        print("SSH-Verbindung erfolgreich")
    else:
        print("SSH-Verbindung fehlgeschlagen")
    tunnel = client.get_transport().open_channel("direct-tcpip", ("127.0.0.1", remote_port), ("127.0.0.1", local_port) ) 
    return client, tunnel

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
    ssh_client, ssh_tunnel = create_ssh_tunnel()

    openai_api_base = f"http://127.0.0.1:8092/v1"

    image_class = get_image_class_async(image.link)
    client = OpenAI(api_key=config.openai_api_key, base_url=openai_api_base) 
    models = client.models.list()
    model = models.data[0].id

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
    ssh_client.close()
    ssh_tunnel.close()
    return image

async def query_mixtral_async(prompt: str, msg: str):

    data = {
        "inputs": f"<s> [INST] Beantworte die folgende Frage in 3-8 Sätzen in einer formalen Sprache: {msg} [/INST] Model answer</s>"
    }
        
    try:
        # SSH-Tunnel-Forwarder einrichten
        with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_username,
            local_bind_address=('localhost', local_port),
            remote_bind_address=('localhost', remote_port)
        ) as tunnel:
        
            print(f"SSH-Tunnel hergestellt: localhost:{local_port} -> {ssh_host}:{remote_port}")
        
            # Warte, bis der Tunnel aktiv ist
            tunnel.start()
        
            # Sende die Anfrage über den Tunnel
            response = requests.post(f"http://localhost:{local_port}", json=data)
        
            # Ausgabe der Antwort
            if response.status_code == 200:
                data = json.loads(response.text)
                return data[0]['generated_text']
            else:
                print("Fehler beim Abrufen der Antwort:", response.status_code, response.text)
    
    except Exception as e:
        print("Verbindungsfehler:", e)