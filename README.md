# Odyss.AI ![Logo](odyss_logo.png)
Odyss.AI ermöglicht das Hochladen von Dokumenten und das Stellen von Fragen zu deren Inhalten. Mithilfe von Mistral und Pixtral werden relevante Informationen extrahiert und verständlich aufbereitet.

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
![Übersicht Architektur Odyss.AI](odyss_overview.png)

## Installation⚙️
### Installation VMware 
https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware+Workstation+Pro

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

### Nutze VM mit allen vorherigen Einstellungen vorbereitet
- Ziehe VM von:
- Öffne VMware und füge die VM hinzu
- Starte die VM, dort ist das komplette Projekt vorhanden auf dem dev-local Branch. Es gibt eine launch.json für debugging der Services. Beachte das die Ports für Backend geändert wurde. Entsprechend müssen in OCR, LLM und Frontend (utils.js) geändert werden. Auf dev-local ist das bereits umgestellt, reiner debugging Branch.

### Nutze Docker Compose
Mithilfe von Docker Compose können alle Services einfach hochgefahren werden. Deployment auf den Uni Server genau damit durchgeführt.

### Github Runner
Zum besseren Debugging wurde ein Github Runner auf der VM installiert. Dieser wird aktiv sobald eine änderung an dem dev Branch festgestellt wurde. Nach einer Änderung des dev Branches führt der Runner folgende Schritte aus:
          cd /var/opt/Odyss.AI
          sudo git pull origin dev
          sudo docker-compose down
          sudo docker-compose build
          sudo docker-compose up -d

Die deploy.yml ist in dem .github/workflows ordner zu finden.
Nachfolgend wird die installation des Runners erklärt.

### GitHub Repository konfigurieren

1. **Repository erstellen**
  - Erstelle ein neues Repository auf GitHub oder nutze ein bestehendes Repository.

2. **GitHub Runner Token generieren**
  - Gehe zu den Einstellungen deines Repositorys.
  - Navigiere zu `Settings` > `Actions` > `Runners` > `New self-hosted runner`.
  - Wähle das Betriebssystem und die Architektur aus und klicke auf `Generate new token`.

3. **Runner konfigurieren**
  - Folge den Anweisungen auf der GitHub-Seite, um den Runner zu konfigurieren. Nutze den generierten Token bei der Konfiguration.

4. **Workflow-Datei erstellen**
  - Erstelle eine neue Datei `.github/workflows/deploy.yml` in deinem Repository mit folgendem Inhalt:
  ```yaml
name: Deploy with Docker

on:
  push:
    branches:
      - dev

jobs:
  deploy:
    runs-on: self-hosted
    steps:
      - name: Configure Git Safe Directory
        run: git config --global --add safe.directory /var/opt/Odyss.AI

      - name: Deploy with Docker
        run: |
          cd /var/opt/Odyss.AI
          sudo git pull origin dev
          sudo docker-compose down
          sudo docker-compose build
          sudo docker-compose up -d
  ```

5. **Workflow aktivieren**
  - Sobald du Änderungen an den `dev` Branch pushst, wird der GitHub Runner den Workflow ausführen und die neuesten Änderungen auf der VM deployen.

Der GitHub Runner ist nun konfiguriert und wird automatisch aktiviert, wenn Änderungen an deinem Repository vorgenommen werden. 🚀

### GitHub Runner installieren

1. **GitHub Runner herunterladen**
  - Lade die neueste Version des GitHub Runners herunter:
  ```bash
  mkdir actions-runner && cd actions-runner
  curl -o actions-runner-linux-x64-2.303.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.303.0/actions-runner-linux-x64-2.303.0.tar.gz
  tar xzf ./actions-runner-linux-x64-2.303.0.tar.gz
  ```

2. **Abhängigkeiten installieren**
  - Stelle sicher, dass die notwendigen Abhängigkeiten installiert sind:
  ```bash
  sudo apt-get install -y libicu-dev libkrb5-dev
  ```

3. **Runner konfigurieren**
  - Konfiguriere den Runner mit deinem Repository:
  ```bash
  ./config.sh --url https://github.com/USERNAME/REPOSITORY --token YOUR_TOKEN
  ```

4. **Runner als Dienst installieren**
  - Installiere und starte den Runner als Dienst:
  ```bash
  sudo ./svc.sh install
  sudo ./svc.sh start
  ```

5. **Überprüfung**
  - Überprüfe, ob der Runner erfolgreich installiert und gestartet wurde:
  ```bash
  sudo ./svc.sh status
  ```

Der GitHub Runner sollte nun auf deiner VM installiert und einsatzbereit sein. 🚀

## ToDos🎯
- Darstellung der hochgeladenen Dokumente nach erneuten einloggen
- Finaler Dokumentenspeicher finden
- Leere Textliste von OCR zurückgegeben
- TEI Embeddings Tokenoverlow
