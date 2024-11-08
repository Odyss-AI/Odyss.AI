// src/components/PDFPreview/PDFPreview.jsx
import React from 'react';
import styles from './PDFPreview.module.css';

// Die PDFPreview-Komponente ist verantwortlich für die Anzeige der PDF-Datei im iframe-Element.
// Die Datei wird von einem Byte-Stream in ein Blob umgewandelt, um eine URL zu erzeugen, die das iframe nutzen kann.
const PDFPreview = ({ file }) => {
    // Erzeugt eine URL aus dem Byte-Stream (falls vorhanden), indem ein Blob erstellt wird, das vom iframe verwendet werden kann
    const fileURL = file ? URL.createObjectURL(new Blob([file], { type: 'application/pdf' })) : null;

    // Wenn keine Datei vorhanden ist, wird ein Hinweistext angezeigt
    if (!file) {
        return <p>Keine PDF-Datei ausgewählt</p>;
    }

    return (
        <div className={styles.pdfDisplay}>
            {/* Das iframe zeigt die generierte URL der PDF-Datei an */}
            <iframe
                src={fileURL}
                className={styles.pdfIframe}
                title="PDF Vorschau"
            />
        </div>
    );
};

export default PDFPreview;