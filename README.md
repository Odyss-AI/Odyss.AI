# Odyss.AI ![Logo](odyss_logo.png)
Odyss.AI ermöglicht das Hochladen von Dokumenten und das Stellen von Fragen zu deren Inhalten. Mithilfe von Mistral und Pixtral werden relevante Informationen extrahiert und verständlich aufbereitet.

#### Zu Odyss.AI (Uni-VPN): http://141.75.150.74

### ✨ Funktionen
- 📂 Dokumente hochladen (PDF, DOCX, PPX usw.)
- 🤖 Fragen zu den Dokumenten stellen
- 🔍 Schnelle und präzise Antworten basierend auf dem Inhalt
- 🛠 Einfache Nutzung über die Web-Oberfläche
- 🚀 Starte jetzt und lass die KI deine Dokumente für dich durchsuchen!

## Inhaltsverzeichnis
- [Übersicht🥽](#installation)
- [Installation⚙️](#übersicht)
- [ToDos🎯](#todos)

## Übersicht🥽
![Pbersicht Architektur Odyss.AI](odyss_overview.png)

### Ports:
- Frontend: 80
- Backend: 443
- OCR: 5050
- ImageTagger: 5150
- MongoDB: 27017
- QDrant: 6333
- TEI: 8080

### Deployment:
Aktuell wird eine Ubuntu VM auf dem Uni Server verwendet. Bei Push auf dev-Branch wird per Workflow mithilfe von Docker Compose alle Services auf der VM deployed.

## Installation (Lokales Debugging)⚙️
### Installation VMware 
https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware+Workstation+Pro

### Nutze vorbereitete VM:

#### Lade die VM unter folgenden Link herunter: https://technischehochschulen.sharepoint.com/:f:/s/ITProjektML/EjC_i8xo09lNiDksOgHPKUABv0gYrsBETuw8B6bp4vrtzg?e=pK1Ot1

#### Füge die VM in VMware hinzu und starte diese
- Benutzername: Odyss
- Passwort: odyss
- Branch dev-local als Beispiel für lokales debugging, bei anderem Branch -> (Backend) In config.py env auf linux stetzen, Port auf 8443 o.ä. (443 ist geblockt) (Frontend) Passe URL in utils.js und useWebsocket.jsx entsprechend an für Verbindung mit Backend
- Einstellung für Debugging der Services in launch.json vorbereitet

### Setup neue Virtual Machine

#### Erstelle eine neue VM mit Ubuntu Linux (downloade die entsprechende ISO Datei)

#### Installiere Git: sudo apt install git

#### 🐳 Docker und Docker Compose auf Ubuntu installieren
- 1.1 Paketliste aktualisieren und Abhängigkeiten installieren
```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
```
- 1.2 Docker GPG-Schlüssel hinzufügen
```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
- 1.3 Docker-Repository hinzufügen
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
```

- 1.4 Docker installieren
```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
- 1.5 Überprüfung der Installation
```bash
docker --version
```
- 1.6 (Optional) Docker ohne `sudo` verwenden
```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

- 2.1 Neuste Version von Docker Compose abrufen und installieren
```bash
LATEST_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)
sudo curl -L "https://github.com/docker/compose/releases/download/${LATEST_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
- 2.2 Überprüfung der Installation
```bash
docker-compose --version
```

---
- 3. Docker-Dienst aktivieren (optional)
Falls Docker nicht automatisch startet:
```bash
sudo systemctl enable --now docker
```

---

✅ **Fertig!** Jetzt kannst du Docker und Docker Compose auf deinem Ubuntu-System nutzen. 🚀

#### Installiere LibreOffice
```bash
sudo apt-get update && \
sudo apt-get install -y libreoffice libreoffice-writer libreoffice-impress libreoffice-calc default-jre && \
sudo apt-get clean && \
sudo rm -rf /var/lib/apt/lists/*
```
#### Falls Teseract als OCR verwendet werden soll, muss folgendes noch installiert werden
```bash
sudo apt-get update && \
sudo apt-get install -y ffmpeg libsm6 libxext6 poppler-utils tesseract-ocr && \
rm -rf /var/lib/apt/lists/*  # Entferne die nicht mehr benötigten Installationsdateien
```
#### Installiere Global Protect für Uni VPN
https://www.th-nuernberg.de/fileadmin/zentrale-einrichtungen/zit/zit_docs/ZIT_HR_VPN-Linux.pdf

#### Starte einen MongoDB, QDrant und TEI Container
- MongoDB
```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongo_data:/data/db \
  -e MONGO_INITDB_ROOT_USERNAME=odyss \
  -e MONGO_INITDB_ROOT_PASSWORD=odyss1 \
  mongo:latest
```
- QDrant
```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest
```
- TEI
```bash
docker run -d \
  --name text_embeddings_inference \
  -p 8080:8080 \
  -v tei:/data/tei \
  ghcr.io/huggingface/text-embeddings-inference:cpu-1.5 \
  --model-id BAAI/bge-large-en-v1.5 \
  --hostname 0.0.0.0 \
  --port 8080 \
  --payload-limit 20000000 \
  --max-batch-tokens 1000000 \
  --max-client-batch-size 16
```
#### Installiere Python und Pakete für Backend, LLM und OCR Service
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
```
Öffne ein Terminal in jedem Unterordner der jeweiligen Services und führe folgende Befehle aus
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Starte die einzelnen Services mit sudo .venv/bin/python3 run.py
Passe zum debuggen die launch.json an

#### Starte das Frontend
Falls nicht installiert, hole npm
```bash
sudo apt update
sudo apt install npm
npm install
```

## ToDos🎯
- Darstellung der hochgeladenen Dokumente nach erneuten einloggen (werden nicht angezeigt, in der DB weiterhin hinterlegt, also chatten mit Dokumenten trotzdem möglich)
- Finaler Dokumentenspeicher finden
- Performanceoptimierung bei Bildauswertung (Pixtral) und Zusammenfassung (Mixtral) -> Vermeidung mehrmaliges öffnen des SSH Tunnels wegen Batching
- Logausgabe funktioniert nicht in der Konsole (aktuell mit Prints gelöst)
- Formeln korrekt aus Dokumentauslesen
- Ausführliche Tests durchführen
- Code weiter aufräumen und optimieren
