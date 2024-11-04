project-root/
│
├── node_modules/            # Alle installierten Abhängigkeiten
├── public/                  # Statische Dateien wie index.html, favicon, etc.
│   ├── index.html           # Haupt-HTML-Datei, die Vite als Einstiegsdatei verwendet
│   └── assets/              # Statische Assets wie Bilder, Videos etc.
│       ├── Images/          # Bilder wie Logos, Icons etc.
│       │   ├── boat.png
│       │   └── ...
│       └── background.mp4   # Video-Datei für Hintergrund
│
├── src/                     # Hauptordner für den Quellcode
│   ├── assets/              # Alle projektbezogenen statischen Assets
│   │   ├── Images/          # Bilder, z.B. Benutzer-Icons oder Logos
│   │   └── Videos/          # Videos, z.B. Hintergrundvideos
│   │       └── background.mp4
│   │
│   ├── components/          # Wiederverwendbare UI-Komponenten
│   │   ├── Header/          # Header-Komponente
│   │   │   ├── Header.jsx
│   │   │   └── Header.module.css
│   │   ├── Sidebar/         # Sidebar-Komponente für Chats
│   │   │   ├── Sidebar.jsx
│   │   │   └── Sidebar.module.css
│   │   ├── Login/           # Login-Komponente
│   │   │   ├── Login.jsx
│   │   │   └── Login.module.css
│   │   ├── ChatWindow/      # Chat-Fenster-Komponente
│   │   │   ├── ChatWindow.jsx
│   │   │   └── ChatWindow.module.css
│   │   ├── DragAndDrop/     # Drag-and-Drop-Komponente für PDF-Dateien
│   │   │   ├── DragAndDrop.jsx
│   │   │   └── DragAndDrop.module.css
│   │   ├── PDFPreview/      # Vorschau für PDF-Dateien
│   │   │   ├── PDFPreview.jsx
│   │   │   └── PDFPreview.module.css
│   │   ├── UserInput/       # Eingabefeld für Benutzer-Nachrichten
│   │   │   ├── UserInput.jsx
│   │   │   └── UserInput.module.css
│   │   ├── Footer/          # Footer-Komponente
│   │   │   ├── Footer.jsx
│   │   │   └── Footer.module.css
│   │   └── Logout/          # Logout-Komponente
│   │       ├── Logout.jsx
│   │       └── Logout.module.css
│   │
│   ├── pages/               # Seiten für die Anwendung
│   │   ├── LoginPage/       # Seite für das Login
│   │   │   ├── LoginPage.jsx
│   │   │   └── LoginPage.module.css
│   │   ├── ChatPage/        # Seite für die Chats
│   │   │   ├── ChatPage.jsx
│   │   │   └── ChatPage.module.css
│   │
│   ├── store/               # Zustand-Management mit Zustand
│   │   ├── authStore.js     # Zustand für Authentifizierungsstatus (login/logout)
│   │   ├── chatStore.js     # Zustand für Chats und Nachrichten
│   │   └── fileStore.js     # Zustand für hochgeladene Dateien
│   │
│   ├── **api/**             # 🔴 Neuer Ordner für API-Interaktionen
│   │   ├── **api.js**       # 🔴 Zentrale Datei für die API-Aufrufe
│   │   └── **auth.js**      # 🔴 Datei für Authentifizierungsbezogene API-Aufrufe
│   │
│   ├── **services/**        # 🔴 Service-Layer für komplexere Logik
│   │   ├── **chatService.js**  # 🔴 Service-Datei für Chat-Logik (wie Kommunikation mit Backend)
│   │   └── **fileService.js**  # 🔴 Service-Datei für Datei-Upload-Logik
│   │
│   ├── hooks/               # Custom React Hooks für verschiedene Logiken
│   │   ├── useAuth.js       # Custom Hook für Authentifizierungs-Logik (z.B. ist der Nutzer eingeloggt?)
│   │   └── useFetch.js      # Custom Hook für allgemeine Fetch-API-Anfragen
│   │
│   ├── utils/               # Hilfsfunktionen und Tools, die in der gesamten App verwendet werden können
│   │   ├── **constants.js**   # 🔴 Konstante Werte, die in der App genutzt werden (z.B. API URLs)
│   │   └── helpers.js       # Hilfsfunktionen, wie z.B. ein Formatierungs-Helper oder ein Fehler-Handler
│   │
│   ├── App.jsx              # Hauptkomponente der App, die die Seiten rendert
│   ├── App.module.css       # Globales CSS für die App (allgemeine Stile)
│   ├── main.jsx             # Einstiegspunkt für React (wird von Vite verwendet)
│   │
│   └── index.css            # Allgemeine Stile, z.B. für den Body, Schriftarten etc.
│
├── .gitignore               # Dateien und Ordner, die Git ignorieren soll
├── package.json             # Abhängigkeiten und Scripts
├── vite.config.js           # Konfiguration für Vite
└── README.md                # Informationen über das Projekt
