import React, { useState } from 'react';
import useFileStore from '../../store/fileStore.jsx';

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
            className={`drag-drop-zone ${dragging ? 'dragging' : ''}`}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
        >
            <p>{dragging ? "Loslassen zum Hochladen" : "PDF-Datei hierhin ziehen"}</p>
        </div>
    );
};

export default DragAndDrop;
