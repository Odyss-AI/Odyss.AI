import React from 'react';
import useFileStore from '../../store/fileStore.jsx';

const PDFPreview = () => {
    const file = useFileStore((state) => state.file);

    if (!file) {
        return <p>Keine PDF-Datei ausgewählt</p>;
    }

    const fileURL = URL.createObjectURL(file); // Erzeugt eine URL zur Anzeige der PDF

    return (
        <div className="pdf-display">
            <embed src={fileURL} type="application/pdf" width="600" height="500" />
        </div>
    );
};

export default PDFPreview;
