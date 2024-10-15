// src/components/DragAndDrop/DragAndDrop.jsx
import React, { useState } from 'react';
import useFileStore from '../../store/fileStore.jsx';
import styles from './DragAndDrop.module.css';

const DragAndDrop = () => {
    const [dragging, setDragging] = useState(false);
    const setFile = useFileStore((state) => state.setFile);

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

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(false);

        const files = e.dataTransfer.files;

        if (files && files.length > 0) {
            const file = files[0];

            if (file.type === 'application/pdf') {
                setFile(file); // Datei in den Zustand-Store legen
            } else {
                alert("Bitte nur PDF-Dateien hochladen!");
            }
        }
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
                <p>{dragging ? "Loslassen zum Hochladen" : "PDF-Datei hierhin ziehen oder klicken, um eine Datei auszuwählen"}</p>
                <button onClick={() => document.getElementById('fileInput').click()} className={styles.uploadButton}>
                    Datei auswählen
                </button>
                <input
                    id="fileInput"
                    type="file"
                    accept="application/pdf"
                    onChange={(e) => {
                        const file = e.target.files[0];
                        if (file && file.type === 'application/pdf') {
                            setFile(file);
                        } else {
                            alert("Bitte nur PDF-Dateien hochladen!");
                        }
                    }}
                    className={styles.fileInput}
                />
            </div>
        </div>
    );
};

export default DragAndDrop;
