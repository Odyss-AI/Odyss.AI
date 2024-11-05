// src/components/DragAndDrop/DragAndDrop.jsx
import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid'; // UUID importieren
import styles from './DragAndDrop.module.css';

const DragAndDrop = ({ onFileDrop }) => {
    const [dragging, setDragging] = useState(false);

    // Drag & Drop Event-Handler
    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(false);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(false);

        const files = e.dataTransfer.files;

        if (files && files.length > 0) {
            let pdfFiles = [];
            for (const file of files) {
                if (file.type === 'application/pdf') {
                    const newFile = await createNewFile(file);
                    pdfFiles.push(newFile);
                } else if (file.type === 'application/zip') {
                    const extractedFiles = await extractPDFsFromZip(file);
                    for (const extractedFile of extractedFiles) {
                        pdfFiles.push(await createNewFile(extractedFile));
                    }
                } else {
                    alert("Bitte nur PDF-Dateien oder ZIP-Ordner hochladen!");
                    return;
                }
            }
            onFileDrop(pdfFiles);
        }
    };

    const handleFileInputChange = async (e) => {
        const files = Array.from(e.target.files);
        let pdfFiles = [];

        for (const file of files) {
            if (file.type === 'application/pdf') {
                const newFile = await createNewFile(file);
                pdfFiles.push(newFile);
            } else if (file.type === 'application/zip') {
                const extractedFiles = await extractPDFsFromZip(file);
                for (const extractedFile of extractedFiles) {
                    pdfFiles.push(await createNewFile(extractedFile));
                }
            } else {
                alert("Bitte nur PDF-Dateien oder ZIP-Ordner hochladen!");
                return;
            }
        }
        onFileDrop(pdfFiles);

        // Input-Element zurücksetzen, um sicherzustellen, dass der Browser auch das erneute Hochladen der gleichen Datei zulässt
        e.target.value = '';
    };

    // Hilfsfunktion zum Erstellen eines neuen File-Objekts aus einem bestehenden File-Objekt mit einer UUID
    const createNewFile = async (file) => {
        const fileData = await file.arrayBuffer();
        const newFile = new File([fileData], `${uuidv4()}_${file.name}`, { type: file.type, lastModified: Date.now() });
        return newFile;
    };

    // Hilfsfunktion zum Extrahieren von PDF-Dateien aus einem Zip-Ordner
    const extractPDFsFromZip = async (zipFile) => {
        const pdfFiles = [];
        try {
            const JSZip = await import('jszip');
            const zip = await JSZip.loadAsync(zipFile);

            for (const fileName of Object.keys(zip.files)) {
                if (fileName.startsWith('__MACOSX/') || fileName.startsWith('._')) {
                    continue;
                }

                if (fileName.endsWith('.pdf')) {
                    const fileData = await zip.files[fileName].async('blob');
                    const newFile = new File([fileData], `${uuidv4()}_${fileName}`, { type: 'application/pdf' });
                    pdfFiles.push(newFile);
                }
            }
        } catch (error) {
            console.error("Fehler beim Extrahieren der PDF-Dateien aus dem Zip-Ordner:", error);
        }
        return pdfFiles;
    };

    return (
        <div
            className={`${styles.dragDropZone} ${dragging ? styles.dragging : ''}`}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
        >
            <div className={styles.content}>
                <p>{dragging ? "Loslassen zum Hochladen" : "PDF-Dateien oder ZIP-Ordner hierhin ziehen oder klicken, um eine Datei auszuwählen"}</p>
                <button onClick={() => document.getElementById('fileInput').click()} className={styles.uploadButton}>
                    Datei auswählen
                </button>
                <input
                    id="fileInput"
                    type="file"
                    accept=".pdf,.zip"
                    multiple
                    onChange={handleFileInputChange}
                    className={styles.fileInput}
                />
            </div>
        </div>
    );
};

export default DragAndDrop;
