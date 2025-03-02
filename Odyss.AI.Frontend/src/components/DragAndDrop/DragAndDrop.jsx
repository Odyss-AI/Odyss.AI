// src/components/DragAndDrop/DragAndDrop.jsx
import React, { useState } from 'react';
import useFileStore from '../../store/fileStore.jsx';
import styles from './DragAndDrop.module.css';
import { uploadDocument } from '../../utils.js';

const DragAndDrop = ({username, selectedChat}) => {
    // Lokaler Zustand
    const [dragging, setDragging] = useState(false);

    // Globaler Zustand aus dem File Store
    const setFiles = useFileStore((state) => state.setFiles); // Zugriff auf die setFiles-Funktion

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
                    pdfFiles.push(file);
                } else if (file.type === 'application/zip') {
                    const extractedFiles = await extractPDFsFromZip(file);
                    pdfFiles = pdfFiles.concat(extractedFiles);
                } else {
                    alert("Bitte nur PDF-Dateien oder ZIP-Ordner hochladen!");
                    return;
                }
            }
            
            console.log("PDF-Dateien:", pdfFiles);
            console.log("Benutzername:", username.user.username);
            console.log("Ausgewählter Chat:", selectedChat);
            if (selectedChat) {
                const files = await uploadDocument(pdfFiles, username.user.username, selectedChat.id);
                if (!files) {
                    console.error("Fehler beim Hochladen der Datei");
                    alert("Fehler beim Hochladen der Datei");
                    return;
                }
            }

            setFiles(pdfFiles); // Füge die neuen Dateien hinzu, anstatt die bestehenden zu überschreiben
        }
    };

    // Funktion zum Extrahieren von PDF-Dateien aus einem Zip-Ordner
    const extractPDFsFromZip = async (zipFile) => {
        const pdfFiles = [];
        try {
            const JSZip = await import('jszip'); // Dynamischer Import von JSZip
            const zip = await JSZip.loadAsync(zipFile);

            for (const fileName of Object.keys(zip.files)) {
                // Filtert Dateien, die mit "__MACOSX/" oder "._" beginnen, heraus
                if (fileName.startsWith('__MACOSX/') || fileName.startsWith('._')) {
                    continue; // Ignorieren dieser Dateien
                }

                if (fileName.endsWith('.pdf')) {
                    const fileData = await zip.files[fileName].async('blob');
                    pdfFiles.push(new File([fileData], fileName, { type: 'application/pdf' }));
                }
            }
        } catch (error) {
            console.error("Fehler beim Extrahieren der PDF-Dateien aus dem Zip-Ordner:", error);
        }
        return pdfFiles;
    };

    const handleFileInputChange = async (e) => {
        const files = Array.from(e.target.files);
        let pdfFiles = [];
        for (const file of files) {
            if (file.type === 'application/pdf') {
                pdfFiles.push(file);
            } else if (file.type === 'application/zip') {
                const extractedFiles = await extractPDFsFromZip(file);
                pdfFiles = pdfFiles.concat(extractedFiles);
            } else {
                alert("Bitte nur PDF-Dateien oder ZIP-Ordner hochladen!");
                return;
            }
        }

        if (selectedChat) {
            console.log("Benutzername:", username);
            const files = await uploadDocument(pdfFiles, username, selectedChat.id);
            if (!files) {
                console.error("Fehler beim Hochladen der Datei");
                alert("Fehler beim Hochladen der Datei");
                return;
            }
        }
        setFiles(pdfFiles);
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
