// src/components/PDFPreview/PDFPreview.jsx
import React from 'react';
import useFileStore from '../../store/fileStore.jsx';

const PDFPreview = () => {
    const selectedFile = useFileStore((state) => state.selectedFile); // Zugriff auf die aktuell ausgewählte Datei zur Vorschau

    console.log("Rendering PDFPreview with file: ", selectedFile);

    if (!selectedFile) {
        return <p></p>;
    }

    const fileURL = URL.createObjectURL(selectedFile); // Erzeugt eine URL zur Anzeige der PDF

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
