// src/components/PDFPreview/PDFPreview.jsx
import React from 'react';

const PDFPreview = ({ file }) => {  // File wird jetzt als Prop übergeben
    if (!file) {
        return <p>Keine PDF-Datei ausgewählt</p>;
    }

    const fileURL = URL.createObjectURL(file); // Erzeugt eine URL zur Anzeige der PDF

    return (
        <div className="pdf-display">
            <iframe
                src={fileURL}
                type="application/pdf"
                width="600"
                height="500"
                title="PDF Vorschau"
                style={{ border: 'none' }}
            />
        </div>
    );
};

export default PDFPreview;
