# Odyss.AI Backend

Diese Doku bezieht sich nur auf das Backend und alle Komponenten davon.

## Übersicht

Das Odyss.AI Backend ist eine serverseitige Anwendung, die mit Quart, einem asynchronen Web-Framework für Python, entwickelt wurde. Es bietet verschiedene Funktionen, einschließlich Benutzerverwaltung, Chat-Verarbeitung, Dokumentenverarbeitung und WebSocket-Kommunikation für Echtzeit-Interaktionen.

## Inhaltsverzeichnis
- [Odyss.AI Backend](#odyssai-backend)
  - [Übersicht](#übersicht)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Projektstruktur](#projektstruktur)
  - [Setup Dateien](#setup-dateien)
    - [setup.py](#setuppy)
      - [Beschreibung](#beschreibung)
      - [Verwendung](#verwendung)
    - [run.py](#runpy)
    - [Dockerfile](#dockerfile)
      - [Beschreibung](#beschreibung-1)
      - [Verwendung](#verwendung-1)
  - [Datenbank](#datenbank)
  - [Routes](#routes)
    - [routes / user\_routes.py](#routes--user_routespy)
      - [Endpunkte](#endpunkte)
        - [Benutzer hinzufügen](#benutzer-hinzufügen)
        - [Benutzer abrufen](#benutzer-abrufen)
        - [Chats abrufen](#chats-abrufen)
        - [Chat hinzufügen](#chat-hinzufügen)
      - [Beschreibung](#beschreibung-2)
    - [routes / websocket\_routes.py](#routes--websocket_routespy)
      - [Endpunkte](#endpunkte-1)
        - [Home](#home)
        - [WebSocket Chat](#websocket-chat)
      - [Beschreibung](#beschreibung-3)
  - [Services](#services)
    - [services / db\_service.py](#services--db_servicepy)
      - [Beschreibung](#beschreibung-4)
      - [Methoden](#methoden)
    - [services / caching.py](#services--cachingpy)
      - [Beschreibung](#beschreibung-5)
      - [Methoden](#methoden-1)
    - [services / sim\_search\_service.py](#services--sim_search_servicepy)
      - [Beschreibung](#beschreibung-6)
      - [Methoden](#methoden-2)
    - [services / message\_manager.py](#services--message_managerpy)
      - [Beschreibung](#beschreibung-7)
      - [Methoden](#methoden-3)
    - [services / document\_manager.py](#services--document_managerpy)
      - [Beschreibung](#beschreibung-8)
      - [Methoden](#methoden-4)
    - [utils / batching.py](#utils--batchingpy)
      - [Beschreibung](#beschreibung-9)
      - [Methoden](#methoden-5)
    - [utils / prompts.py](#utils--promptspy)
      - [Beschreibung](#beschreibung-10)
      - [Methoden](#methoden-6)
    - [utils / auth.py](#utils--authpy)
    - [utils / db.py](#utils--dbpy)
      - [Beschreibung](#beschreibung-11)
      - [Methoden](#methoden-7)
    - [utils / test\_data\_provider.py](#utils--test_data_providerpy)
      - [Beschreibung](#beschreibung-12)
      - [Methoden](#methoden-8)
    - [utils / pdf\_converter.py](#utils--pdf_converterpy)
      - [Beschreibung](#beschreibung-13)
      - [Methoden](#methoden-9)
    - [utils / ocr\_connection.py](#utils--ocr_connectionpy)
      - [Beschreibung](#beschreibung-14)
      - [Methoden](#methoden-10)
    - [utils / ml\_connection.py](#utils--ml_connectionpy)
      - [Beschreibung](#beschreibung-15)
      - [Methoden](#methoden-11)
    - [utils / img\_tagger\_connection.py](#utils--img_tagger_connectionpy)
      - [Beschreibung](#beschreibung-16)
      - [Methoden](#methoden-12)
    - [utils / converters.py](#utils--converterspy)
      - [Beschreibung](#beschreibung-17)
      - [Methoden](#methoden-13)

## Projektstruktur
```
Odyss.AI.Backend/ 
├── app/ 
│ ├── init.py 
│ ├── config.py 
│ ├── models/ 
│ ├── routes/ 
│ │ ├── init.py 
│ │ ├── user_routes.py
│ │ ├── document_routes.py 
│ │ ├── websocket_routes.py 
│ ├── services/
│ │ ├── caching.py
│ │ ├── db_service.py
│ │ ├── document_manager.py 
│ │ ├── message_manager.py
│ │ ├── sim_search_service.py
│ ├── utils/ 
│ │ ├── converters.py 
│ │ ├── prompts.py
│ │ ├── auth.py
│ │ ├── batching.py
│ │ ├── ...
├── .dockerignore 
├── Dockerfile 
├── requirements.txt 
├── run.py 
├── setup.py
```

## Setup Dateien

### setup.py

Die `setup.py` Datei wird verwendet, um eine virtuelle Umgebung zu erstellen und die erforderlichen Pakete für die Odyss.AI Backend-Anwendung zu installieren.

#### Beschreibung

- Überprüft, ob der Ordner `venv` existiert. Falls nicht, wird eine neue virtuelle Umgebung erstellt.
- Aktiviert die virtuelle Umgebung und installiert die Pakete aus der `requirements.txt` Datei.
- Unterscheidet zwischen Windows und Unix/MacOS, um das entsprechende Aktivierungsskript für die virtuelle Umgebung zu verwenden.

#### Verwendung

1. Führe die `setup.py` Datei aus, um die virtuelle Umgebung zu erstellen und die Pakete zu installieren:

```sh
python setup.py
```

### run.py

Die `run.py` Datei ist der Einstiegspunkt der Odyss.AI Backend-Anwendung. Sie erstellt und startet die Quart-Anwendung.

### Dockerfile

Die `Dockerfile` Datei wird verwendet, um ein Docker-Image für die Odyss.AI Backend-Anwendung zu erstellen. Sie definiert die Schritte, die erforderlich sind, um die Anwendung in einem Docker-Container auszuführen.

#### Beschreibung

- Verwendet ein offizielles Python 3.9 Slim-Image als Basis.
- Setzt das Arbeitsverzeichnis im Container auf `/app`.
- Installiert `virtualenv` und erstellt eine virtuelle Umgebung.
- Kopiert die `requirements.txt` Datei in den Container.
- Installiert LibreOffice und Java Runtime Environment.
- Aktiviert die virtuelle Umgebung und installiert die erforderlichen Pakete aus der `requirements.txt` Datei.
- Kopiert den restlichen Anwendungscode in den Container.
- Setzt die Umgebungsvariablen `ENVIRONMENT` und `OCR_ENDPOINT_SELECTION`.
- Öffnet Port 443 für den Container.
- Setzt die Umgebungsvariable `PYTHONUNBUFFERED`, um sicherzustellen, dass das Python-Logging sofort ausgegeben wird.
- Führt die Anwendung innerhalb der virtuellen Umgebung aus.

#### Verwendung

1. Baue das Docker-Image:

```sh
docker build -t odyss-ai-backend .
```

2. Starte den Docker-Container:

```sh
   docker run -d -p 443:443 --name odyss-ai-backend --env-file .env odyss-ai-backend
```

Das manuelle Bauen ist im Projektumfeld nicht nötig da die Dockerfiles zentral über `docker-compose.yml` gestartet werden.

## Datenbank

User Objekt in der Datenbank:
```json
{
  "_id": "ObjectId('672bdfe8716172ce07adac73')",
  "id": "672bdfe8716172ce07adac72",
  "username": "erik",
  "documents": [
    {
      "id": "672d30995917eb661d687488",
      "doc_id": "d60e6bd7e5fcec26153ae27f7d56409a66ad96b560a31bcca23d1975e43a8279",
      "mongo_file_id": "672d30565917eb661d687485",
      "name": "1c6d0ae6-7e41-40f8-8a0b-db10f9be52cd_SuperMarioBros.pdf",
      "timestamp": "2024-11-07T22:25:46.000+00:00",
      "summary": "k: This project uses reinforcement learning to train an agent to maste…",
      "imgList": [],
      "textList": [1],
      "path": "/home/erik/Documents/d60e6bd7e5fcec26153ae27f7d56409a66ad96b560a31bcca…"
    },
    {
      "id": "Object 1"
    },
    {
      "id": "Object 2"
    },
    {
      "id": "Object 3"
    },
    {
      "id": "Object 4"
    },
    {
      "id": "Object 5"
    },
    {
      "id": "Object 6"
    },
    {
      "id": "Object 7"
    }
  ]
}
```
Chat Objekt in der Datenbank:
```json
{
  "_id": "ObjectId('672dff46750acda3bc3e9099')",
  "id": "672dff46750acda3bc3e9098",
  "user_id": "erik",
  "messages": [
    {
      "id": "672dff86750acda3bc3e909e",
      "content": "what is reinforcement learning in super mario bros",
      "timestamp": "2024-11-08T12:09:40.650Z",
      "is_user": true,
      "selected_model": "mistral"
    },
    {
      "id": "Object 1"
    }
  ],
  "chat_name": "test",
  "doc_ids": [
    "fd1bb014b90b9fbe75028a9a7a3856673026f2875711a1bf99ab5fa786c93453"
  ]
}
```
Dokumenten Objekt in der Datenbank:
```json
{
  "_id": "ObjectId('672d30565917eb661d687485')",
  "filename": "1c6d0ae6-7e41-40f8-8a0b-db10f9be52cd_SuperMarioBros.pdf",
  "contentType": "application/pdf",
  "metadata": {
    "hash": "f142f8a0813541e221f38916fecdf457"
  },
  "chunkSize": 261120,
  "length": 43867,
  "uploadDate": "2024-11-07T21:25:43.165+00:00"
}
```

## Routes 

### routes / user_routes.py

Die `user_routes.py` Datei enthält die Routen, die mit Benutzeroperationen wie Hinzufügen eines Benutzers, Abrufen eines Benutzers und Verwalten von Chats zusammenhängen.

#### Endpunkte

##### Benutzer hinzufügen

- **Route:** `POST /users/add`
- **Beschreibung:** Fügt einen neuen Benutzer hinzu.
- **Anfrage:** JSON-Daten mit dem Benutzernamen.
- **Antwort:** Erfolgreiche Erstellung gibt den Benutzer und leere Chats zurück, Fehler bei bereits vorhandenem Benutzernamen oder anderen Problemen.

##### Benutzer abrufen

- **Route:** `GET /users/getuser`
- **Beschreibung:** Ruft einen Benutzer anhand des Benutzernamens ab.
- **Anfrage:** URL-Parameter mit dem Benutzernamen.
- **Antwort:** Erfolgreiches Abrufen gibt den Benutzer und seine Chats zurück, Fehler bei nicht gefundenem Benutzer oder anderen Problemen.

##### Chats abrufen

- **Route:** `GET /users/getchats`
- **Beschreibung:** Ruft die Chats eines Benutzers ab.
- **Anfrage:** URL-Parameter mit dem Benutzernamen.
- **Antwort:** Erfolgreiches Abrufen gibt die Chats zurück, Fehler bei nicht gefundenen Chats oder anderen Problemen.

##### Chat hinzufügen

- **Route:** `POST /users/addchat`
- **Beschreibung:** Fügt einen neuen Chat für einen Benutzer hinzu.
- **Anfrage:** JSON-Daten mit dem Benutzernamen, Dokumenten und Chat-Namen.
- **Antwort:** Erfolgreiche Erstellung gibt den Chat zurück, Fehler bei fehlendem Benutzernamen oder anderen Problemen.

#### Beschreibung

- **Importe:** Importiert notwendige Module und Funktionen wie `request`, `jsonify`, `json_util`, `User`, `Chat` und `get_db`.
- **Datenbankzugriff:** Verwendet die `get_db` Funktion, um auf die Datenbank zuzugreifen.
- **Fehlerbehandlung:** Fangt Ausnahmen ab und gibt entsprechende Fehlermeldungen zurück.

Diese Datei definiert die API-Endpunkte für die Benutzerverwaltung und Chat-Operationen im Odyss.AI Backend.

### routes / websocket_routes.py

Die `websocket_routes.py` Datei enthält die Routen, die mit WebSocket-Verbindungen für die Chat-Funktionalität zusammenhängen.

#### Endpunkte

##### Home

- **Route:** `GET /`
- **Beschreibung:** Liefert eine einfache Begrüßungsnachricht.

##### WebSocket Chat

- **Route:** `WS /chat`
- **Beschreibung:** WebSocket-Endpunkt für die Chat-Kommunikation.
- **Funktion:** 
  - Empfängt Nachrichten vom Client.
  - Verarbeitet die Nachrichten und generiert Antworten.
  - Sendet die Antworten zurück an den Client.

#### Beschreibung

- **Importe:** Importiert notwendige Module und Funktionen wie `json`, `datetime`, `websocket`, `jsonify`, `get_db`, `Chat`, `Message`, `MessageManager`, `ObjectId`, `convert_datetime` und `convert_to_model`.
- **MessageManager:** Initialisiert eine Instanz des `MessageManager`, um Nachrichten zu verarbeiten.
- **Home Route:** Definiert eine einfache Route, die eine Begrüßungsnachricht zurückgibt.
- **WebSocket Chat Route:** 
  - Verwendet eine Endlosschleife, um Nachrichten vom WebSocket zu empfangen.
  - Liest die Nachrichtendaten und extrahiert den Benutzernamen, die Nachricht, die Chat-ID und das Modell.
  - Überprüft, ob der Benutzer authentifiziert ist und existiert.
  - Erstellt eine `Message` Instanz und verarbeitet die Nachricht asynchron.
  - Sendet die Antwort und die verarbeiteten Daten zurück an den Client.

Diese Datei definiert die WebSocket-Kommunikation für die Echtzeit-Chat-Funktionalität im Odyss.AI Backend.

## Services
### services / db_service.py

Die `db_service.py` Datei enthält die `MongoDBService` Klasse, die Methoden zum Interagieren mit einer MongoDB-Datenbank bereitstellt. Sie ermöglicht das Erstellen von Benutzern, Abrufen von Benutzern, Hinzufügen von Dokumenten zu Benutzern, Abrufen von Dokumenten von Benutzern und Löschen von Dokumenten von Benutzern.

#### Beschreibung

- **Singleton Pattern:** Stellt sicher, dass nur eine Instanz der `MongoDBService` Klasse erstellt wird.
- **Datenbankverbindung:** Initialisiert den MongoDB-Client, die Datenbank und die Sammlungen.
- **Benutzerverwaltung:** Methoden zum Erstellen und Abrufen von Benutzern.
- **Dokumentenverwaltung:** Methoden zum Hinzufügen, Abrufen und Löschen von Dokumenten eines Benutzers.
- **Chat-Verwaltung:** Methoden zum Erstellen und Abrufen von Chats sowie zum Hinzufügen von Nachrichten zu Chats.
- **Datei-Upload:** Methoden zum Hochladen und Abrufen von PDF-Dateien und Bildern.

#### Methoden

- `create_user_async(username)`: Erstellt einen neuen Benutzer in der Datenbank.
- `get_user_async(username)`: Ruft einen Benutzer anhand des Benutzernamens ab.
- `add_document_to_user_async(username, document)`: Fügt ein Dokument zur Dokumentenliste eines Benutzers hinzu.
- `get_documents_of_user_async(username)`: Ruft alle Dokumente eines Benutzers ab.
- `delete_document_of_user_async(username, document_id)`: Löscht ein Dokument aus der Dokumentenliste eines Benutzers.
- `get_chat_async(chat_id)`: Ruft einen Chat anhand der Chat-ID ab.
- `get_chats_by_user_async(user)`: Ruft alle Chats eines Benutzers ab.
- `create_chat_async(user, name, doc_ids)`: Erstellt einen neuen Chat in der Datenbank.
- `add_message_to_chat_async(chat_id, message)`: Fügt eine Nachricht zu einem Chat hinzu.
- `get_messages_from_chat_async(chat_id)`: Ruft alle Nachrichten eines Chats ab.
- `upload_pdf_async(converted_file, filename, fileId_hash, user)`: Lädt eine PDF-Datei in die Datenbank hoch.
- `upload_image(file)`: Lädt ein Bild in die Datenbank hoch.
- `get_pdf_async(file_id_hash, filename)`: Lädt eine PDF-Datei aus der Datenbank herunter.
- `get_image_async(file_id)`: Lädt ein Bild aus der Datenbank herunter.

Diese Datei definiert die Datenbankoperationen für die Odyss.AI Backend-Anwendung.

### services / caching.py

Die `caching.py` Datei enthält die `CachingService` Klasse, die Methoden zum Zwischenspeichern von Daten bereitstellt. Sie verwendet `aiocache` für das Caching.

#### Beschreibung

- **Cache-Konfiguration:** Konfiguriert den Cache mit `aiocache` und verwendet den `JsonSerializer`.
- **Caching-Methoden:** Methoden zum Setzen, Abrufen, Überprüfen der Existenz, Löschen und Aktualisieren von Cache-Einträgen.

#### Methoden

- `set(key, value, ttl)`: Fügt einen neuen Wert zum Cache hinzu.
- `get(key, model)`: Ruft einen Wert aus dem Cache ab.
- `exists(key)`: Überprüft, ob ein Schlüssel im Cache existiert.
- `delete(key)`: Löscht einen Wert aus dem Cache.
- `update(key, value, ttl)`: Aktualisiert einen Wert im Cache.

Diese Datei definiert die Caching-Operationen für die Odyss.AI Backend-Anwendung.

### services / sim_search_service.py

Die `sim_search_service.py` Datei enthält die `SimailaritySearchService` Klasse, die Methoden für Ähnlichkeitssuche-Operationen mit Qdrant und TEI-Embeddings bereitstellt.

#### Beschreibung

- **Singleton Pattern:** Stellt sicher, dass nur eine Instanz der `SimailaritySearchService` Klasse erstellt wird.
- **Initialisierung:** Initialisiert die Qdrant-Client und die TEI-URL.
- **Embeddings:** Methoden zum Abrufen, Erstellen und Speichern von Embeddings.
- **Ähnlichkeitssuche:** Methoden zur Suche nach ähnlichen Dokumenten basierend auf einer Abfrage.

#### Methoden

- `fetch_embedding_async(to_embed, chunk_id)`: Ruft das Embedding für einen gegebenen Text asynchron ab.
- `create_embeddings_async(doc)`: Erstellt Embeddings für die Text- und Bildabschnitte in einem Dokument asynchron.
- `save_embedding_async(id, embeddings)`: Speichert die Embeddings asynchron in der Qdrant-Sammlung.
- `search_similar_documents_async(doc_ids, query, count)`: Sucht asynchron nach ähnlichen Dokumenten basierend auf der Abfrage und den Dokument-IDs.
- `_initialize_collection()`: Initialisiert die Qdrant-Sammlung, falls sie noch nicht existiert.

Diese Datei definiert die Ähnlichkeitssuche-Operationen für die Odyss.AI Backend-Anwendung.

### services / message_manager.py

Die `message_manager.py` Datei enthält die `MessageManager` Klasse, die Methoden zur Verwaltung von Nachrichten, Chat-Interaktionen und Ähnlichkeitssuchen bereitstellt.

#### Beschreibung

- **Cache:** Verwendet den `CachingService` für das Caching.
- **Ähnlichkeitssuche:** Verwendet den `SimailaritySearchService` für die Ähnlichkeitssuche.
- **Nachrichtenverarbeitung:** Methoden zur Verarbeitung eingehender Nachrichten und Generierung von Antworten.

#### Methoden

- `handle_message_async(message, user, chat_id)`: Verarbeitet eine eingehende Nachricht, generiert eine Antwort und gibt sie zurück.
- `get_chat_async(db, message, user, chat_id)`: Ruft den Chat aus dem Cache oder der Datenbank ab. Erstellt einen neuen Chat, falls er nicht existiert.
- `get_docs_async(db, user, chat, doc_ids)`: Ruft die Dokumente des Benutzers ab und aktualisiert die Dokument-IDs des Chats.
- `write_bot_msg_async(db, chat, answer)`: Schreibt die Antwortnachricht des Bots in den Chat und aktualisiert den Cache.
- `get_chunks_from_docs(docs, chunk_ids)`: Ruft die Textabschnitte aus den Dokumenten basierend auf den bereitgestellten Chunk-IDs ab.

Diese Datei definiert die Nachrichtenverarbeitung und Chat-Interaktionen für die Odyss.AI Backend-Anwendung.

### services / document_manager.py

Die `document_manager.py` Datei enthält die `DocumentManager` Klasse, die Methoden zur Verwaltung von Dokumenten, einschließlich Speichern, Verarbeiten und Speichern von Dokumenten, bereitstellt.

#### Beschreibung

- **Initialisierung:** Initialisiert den `SimailaritySearchService`.
- **Dokumentenverarbeitung:** Methoden zum Hochladen, Verarbeiten und Speichern von Dokumenten.

#### Methoden

- `handle_document_async(file, username, is_local)`: Verarbeitet das Hochladen, die Verarbeitung und Speicherung von Dokumenten asynchron.
- `generate_filename(original_filename)`: Generiert einen eindeutigen Namen für das Dokument.
- `get_new_doc(mongo_obj_id, hash, original_name, path)`: Erstellt ein neues `Document` Objekt.
- `handle_error(condition, error_message, file, username)`: Behandelt Fehlerbedingungen und protokolliert Fehlermeldungen.

Diese Datei definiert die Dokumentenverwaltung für die Odyss.AI Backend-Anwendung.

### utils / batching.py

Die `batching.py` Datei enthält Funktionen zur Bereinigung, Normalisierung und Batch-Verarbeitung von Textabschnitten (`TextChunk`).

#### Beschreibung

- **Textbereinigung:** Funktionen zur Bereinigung und Normalisierung von Text.
- **Batch-Verarbeitung:** Funktionen zur Aufteilung von Textabschnitten in Batches mit einer maximalen Wortanzahl.
- **Zusammenfassung:** Hauptfunktion zur Erstellung einer finalen Zusammenfassung aus den Batches.

#### Methoden

- `clean_and_normalize_text(text)`: Bereinigt und normalisiert den Text.
- `preprocess_text_chunks(chunks)`: Bereinigt die Textabschnitte.
- `count_words(text)`: Zählt die Wörter in einem Text.
- `batch_text_chunks(chunks, max_words)`: Teilt die Textabschnitte in Batches mit maximal 1000 Wörtern.
- `create_summary_with_batches(chunks, max_words, token_limit)`: Verarbeitet die Batches und erstellt eine finale Zusammenfassung.

Diese Datei definiert die Batch-Verarbeitung und Zusammenfassung von Textabschnitten für die Odyss.AI Backend-Anwendung.

### utils / prompts.py

Die `prompts.py` Datei enthält Funktionen zum Erstellen von Eingabeaufforderungen für Sprachmodelle.

#### Beschreibung

- **Eingabeaufforderungen:** Funktionen zum Erstellen von Eingabeaufforderungen für Zusammenfassungen und Frage-Antwort-Sitzungen.

#### Methoden

- `summary_prompt_builder(chunks)`: Erstellt eine Eingabeaufforderung zur Zusammenfassung von Textabschnitten.
- `qna_prompt_builder(chunks, question)`: Erstellt eine Eingabeaufforderung für eine Frage-Antwort-Sitzung basierend auf den Textabschnitten und der Frage.

Diese Datei definiert die Eingabeaufforderungen für die Sprachmodelle in der Odyss.AI Backend-Anwendung.

### utils / auth.py

Die `auth.py` Datei ist derzeit leer und kann für zukünftige Authentifizierungsfunktionen verwendet werden.

### utils / db.py

Die `db.py` Datei enthält Funktionen zur Initialisierung und zum Zugriff auf den `MongoDBService`.

#### Beschreibung

- **Datenbankinitialisierung:** Funktion zur Initialisierung der Datenbankverbindung.
- **Datenbankzugriff:** Funktion zum Zugriff auf die Datenbankverbindung in anderen Diensten.

#### Methoden

- `init_db_service()`: Initialisiert die Datenbankverbindung und stellt sicher, dass nur eine Verbindung besteht.
- `get_db()`: Gibt die Datenbankverbindung zurück.

Diese Datei definiert die Datenbankinitialisierung und den Datenbankzugriff für die Odyss.AI Backend-Anwendung.

### utils / test_data_provider.py

Die `test_data_provider.py` Datei enthält Funktionen zum Bereitstellen von Testdaten für Benutzer, Dokumente und Textabschnitte (`TextChunk`).

#### Beschreibung

- **Testdaten:** Funktionen zum Erstellen von Testbenutzern und Testdokumenten.

#### Methoden

- `get_test_user()`: Erstellt und gibt einen Testbenutzer zurück.
- `get_test_document(path)`: Erstellt und gibt ein Testdokument mit mehreren Textabschnitten zurück.

Diese Datei wird verwendet, um Testdaten für die Odyss.AI Backend-Anwendung bereitzustellen.

### utils / pdf_converter.py

Die `pdf_converter.py` Datei enthält Funktionen zum Speichern und Konvertieren von Dateien in das PDF-Format.

#### Beschreibung

- **Dateispeicherung:** Funktion zum Speichern der Originaldatei.
- **Dateikonvertierung:** Funktion zur Konvertierung von DOCX- und PPTX-Dateien in PDF mit LibreOffice.

#### Methoden

- `save_and_convert_file(file, hash_filename, db)`: Speichert die Originaldatei und konvertiert sie bei Bedarf in das PDF-Format.

Diese Datei definiert die Dateispeicherung und -konvertierung für die Odyss.AI Backend-Anwendung.

### utils / ocr_connection.py

Die `ocr_connection.py` Datei enthält Funktionen zur Extraktion von Informationen aus PDF-Dokumenten mithilfe eines OCR-Dienstes.

#### Beschreibung

- **OCR-Extraktion:** Funktion zur Extraktion von Informationen aus PDF-Dokumenten.

#### Methoden

- `extract_pdf_information_with_ocr(doc)`: Extrahiert Informationen aus einem PDF-Dokument mithilfe eines OCR-Dienstes.

Diese Datei definiert die OCR-Extraktion für die Odyss.AI Backend-Anwendung.

### utils / ml_connection.py

Die `ml_connection.py` Datei enthält Funktionen zur Verbindung mit verschiedenen maschinellen Lernmodellen und APIs.

#### Beschreibung

- **API-Verbindungen:** Funktionen zur Verbindung mit ChatGPT, Pixtral und Mistral APIs.
- **Bildklassifizierung:** Funktion zur Klassifizierung von Bildern mit einem Image Tagger Service.

#### Methoden

- `allowed_file(filename)`: Überprüft, ob die Datei eine zulässige Erweiterung hat.
- `call_chatgpt_api_async(prompt)`: Ruft die ChatGPT-API asynchron auf.
- `get_image_class_async(image_path)`: Ruft die Bildklasse vom Image Tagger Service ab. Der Funktionsaufruf ist derzeit auskommentiert, da der ImageTagger nicht mehr für den Programmablauf benötigt wird.
- `query_pixtral_async(doc)`: Sendet eine Anfrage an das Pixtral-Modell.
- `query_mixtral_async(prompt)`: Sendet eine Anfrage an das Mistral-Modell.

Diese Datei definiert die Verbindungen zu maschinellen Lernmodellen und APIs für die Odyss.AI Backend-Anwendung.

### utils / img_tagger_connection.py

Die `img_tagger_connection.py` Datei enthält Funktionen zur Verbindung mit einem Image Tagger Service.

#### Beschreibung

- **Bildklassifizierung:** Funktion zur Klassifizierung von Bildern mit einem Image Tagger Service.

#### Methoden

- `extract_pdf_information_with_ocr(doc)`: Extrahiert Informationen aus einem PDF-Dokument mithilfe eines OCR-Dienstes.

Diese Datei definiert die Bildklassifizierung für die Odyss.AI Backend-Anwendung.

### utils / converters.py

Die `converters.py` Datei enthält Funktionen zur Konvertierung von Datenformaten.

#### Beschreibung

- **Datenkonvertierung:** Funktionen zur Konvertierung von Datums- und Zeitformaten sowie zur Konvertierung von Objekten in Modelle.

#### Methoden

- `default_converter(o)`: Konvertiert ein Objekt in ein JSON-serialisierbares Format.
- `convert_to_model(chunk)`: Konvertiert einen Textabschnitt in ein `ChunkModel`.
- `convert_datetime(obj)`: Konvertiert Datums- und Zeitobjekte in ISO 8601-Format.

Diese Datei definiert die Datenkonvertierung für die Odyss.AI Backend-Anwendung.
