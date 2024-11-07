// src/components/PDFPreviewList/PDFPreviewList.jsx
import React from 'react';
import useFileStore from '../../store/fileStore.jsx';
import styles from './PDFPreviewList.module.css';

const PDFPreviewList = () => {
    const files = useFileStore((state) => state.files);
    const setSelectedFile = useFileStore((state) => state.setSelectedFile); // Zugriff auf die Funktion zum Setzen der ausgewählten Datei

    console.log("Rendering PDFPreviewList with files: ", files);

    // Funktion zum Löschen einer Datei aus der Vorschau
    const handleRemoveFile = (index) => {
        const newFiles = [...files];
        newFiles.splice(index, 1); // Entfernt die Datei mit dem angegebenen Index
        useFileStore.setState({ files: newFiles });
        console.log("After removing file, files: ", newFiles);
    };

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
                            setSelectedFile(file); // Beim Klicken wird die Datei ausgewählt
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
                                handleRemoveFile(index);
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
