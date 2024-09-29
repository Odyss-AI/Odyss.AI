import React from 'react';
import '../assets/styles/DragAndDropField.css'; // Importiere die CSS-Datei

const DragAndDropField = () => {
    return (
        <div className="drag-drop-container">
            {/* Beispiel-Icon für Drag-and-Drop */}
            <svg
                className="drag-drop-icon"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 10h8M8 14h8m-4-8h4l-4-4-4 4h4z"
                />
            </svg>
            <div className="drag-drop-text">
                Ziehen Sie hier Ihre PDF-Dateien hinein
            </div>
        </div>
    );
};

export default DragAndDropField;
