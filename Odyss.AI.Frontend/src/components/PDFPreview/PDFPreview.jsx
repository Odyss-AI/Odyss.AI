// src/components/PDFPreview/PDFPreview.jsx
import React from 'react';
import styles from './PDFPreview.module.css';

const PDFPreview = ({ file }) => {
    if (!file) {
        return <p>Keine PDF-Datei ausgewählt</p>;
    }

    const fileURL = URL.createObjectURL(file); // Erzeugt eine URL zur Anzeige der PDF

    return (
        <div className={styles.pdfDisplay}>
            <iframe
                src={fileURL}
                className={styles.pdfIframe} // Die iframe-Klasse verwenden, um das Styling konsistent zu halten
                title="PDF Vorschau"
            />
        </div>
    );
};

export default PDFPreview;
