// src/components/DragAndDrop/DragAndDrop.jsx
import React, { useState } from 'react';
import styles from './DragAndDrop.module.css';
import useFileStore from '../../store/fileStore';  // Zustand-Store für Dateien

function DragAndDrop() {
    const [dragActive, setDragActive] = useState(false);  // Zustand für Drag-Status
    const uploadFile = useFileStore((state) => state.uploadFile);  // Zustand-Action zum Hochladen von Dateien

    // Funktion, die beim DragEnter-Event ausgeführt wird
    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(true);  // Aktiviert den Drag-Status
    };

    // Funktion, die beim DragLeave-Event ausgeführt wird
    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);  // Deaktiviert den Drag-Status
    };

    // Funktion, die bei einem DragOver-Event ausgeführt wird (verhindert Standardverhalten)
    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    // Funktion, die beim Drop-Event ausgeführt wird (Datei wird fallen gelassen)
    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);  // Drag-Status deaktivieren

        // Überprüfen, ob Dateien vorhanden sind
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];  // Nur die erste Datei behandeln

            console.log(file);  // Hier wird die Datei korrekt geloggt

            // Überprüfen, ob es eine PDF- oder ZIP-Datei ist
            if (file.type === "application/pdf") {
                uploadFile(file);  // PDF-Datei hochladen
            } else if (file.type === "application/zip") {
                validateZip(file).then(isValid => {
                    if (isValid) {
                        uploadFile(file);  // ZIP-Datei hochladen
                    } else {
                        alert("Die ZIP-Datei muss mindestens eine PDF-Datei enthalten.");
                    }
                });
            } else {
                alert("Nur PDF-Dateien oder ZIP-Ordner sind erlaubt.");
            }
        }
    };

    // ZIP-Datei validieren (nur falls notwendig)
    const validateZip = async (zipFile) => {
        const JSZip = (await import('jszip')).default;  // Importiere JSZip dynamisch
        const zip = new JSZip();
        const zipContent = await zip.loadAsync(zipFile);
        const files = Object.keys(zipContent.files); // Liste der Dateien in der ZIP

        // Überprüfen, ob mindestens eine PDF-Datei vorhanden ist
        return files.some(fileName => fileName.endsWith('.pdf'));
    };

    return (
        <div
            className={`${styles.dragAndDrop} ${dragActive ? styles.active : ''}`}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onDragOver={handleDragOver}  // Muss vorhanden sein, um Drop zu ermöglichen
        >
            <p>Drag and drop your PDF or ZIP files here</p>
        </div>
    );
}

export default DragAndDrop;
