// src/components/PDFPreviewList/PDFPreviewList.jsx
import React from 'react';
import useFileStore from '../../store/fileStore.jsx';
import styles from './PDFPreviewList.module.css';

const PDFPreviewList = () => {
    const files = useFileStore((state) => state.files);
    const setFiles = useFileStore((state) => state.setFiles);

    // Funktion zum Löschen einer Datei aus der Vorschau
    const handleRemoveFile = (index) => {
        const newFiles = [...files];
        newFiles.splice(index, 1); // Entfernt die Datei mit dem angegebenen Index
        setFiles(newFiles);
    };

    if (!files || files.length === 0) {
        return <p>Keine PDF-Dateien hochgeladen</p>;
    }

    return (
        <div className={styles.pdfPreviewList}>
            {files.map((file, index) => (
                <div key={index} className={styles.pdfPreviewItem}>
                    <iframe
                        src={URL.createObjectURL(file)}
                        title={`PDF Vorschau ${index}`}
                        width="200"
                        height="150"
                        className={styles.pdfPreviewFrame}
                    />
                    <div className={styles.fileName}>{file.name}</div>
                    <button onClick={() => handleRemoveFile(index)} className={styles.removeButton}>
                        Entfernen
                    </button>
                </div>
            ))}
        </div>
    );
};

export default PDFPreviewList;
