import React from 'react';
import useFileStore from '../../store/fileStore.jsx';

const PDFPreview = () => {
    const firstFile = useFileStore((state) => state.firstFile); // Zugriff auf die erste Datei

    if (!firstFile) {
        return <p>Keine PDF-Datei ausgewählt</p>;
    }

    const fileURL = URL.createObjectURL(firstFile); // Erzeugt eine URL zur Anzeige der PDF

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
