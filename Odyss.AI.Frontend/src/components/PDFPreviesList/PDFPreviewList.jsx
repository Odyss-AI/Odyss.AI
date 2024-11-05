// src/components/PDFPreviewList/PDFPreviewList.jsx
import React from 'react';
import styles from './PDFPreviewList.module.css';

const PDFPreviewList = ({ files, onRemoveFile, onSelectFile }) => {  // Neue Props für die Dateien und Aktionen

    console.log("Rendering PDFPreviewList with files: ", files);

    if (!files || files.length === 0) {
        return <p>Keine PDF-Dateien hochgeladen</p>;
    }

    return (
        <div className={styles.pdfPreviewList}>
            {files.map((file, index) => {
                // Sicherstellen, dass file ein Blob oder File ist
                if (!(file instanceof Blob)) {
                    console.error("Invalid file type detected in PDFPreviewList:", file);
                    return null; // Überspringe ungültige Dateien
                }

                return (
                    <div
                        key={index}
                        className={styles.pdfPreviewItem}
                        onClick={(e) => {
                            e.preventDefault(); // Verhindert mögliche Standardaktionen
                            console.log("PDF clicked: ", file);
                            onSelectFile(file); // Neue Datei auswählen
                        }}
                        style={{ cursor: 'pointer' }} // Zeigt an, dass das Element klickbar ist
                    >
                        <iframe
                            src={URL.createObjectURL(file)}
                            title={`PDF Vorschau ${index}`}
                            width="200"
                            height="150"
                            className={styles.pdfPreviewFrame}
                            style={{ pointerEvents: 'none' }} // Blockiert Events auf `iframe`, damit das übergeordnete Div klickbar ist
                        />
                        <div className={styles.fileName}>{file.name}</div>
                        <button
                            onClick={(e) => {
                                e.stopPropagation(); // Verhindert, dass der Klick auf das Button auch das PDF auswählt
                                onRemoveFile(index); // Datei entfernen
                            }}
                            className={styles.removeButton}
                        >
                            Entfernen
                        </button>
                    </div>
                );
            })}
        </div>
    );
};

export default PDFPreviewList;
