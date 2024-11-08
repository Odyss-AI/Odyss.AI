// src/components/PDFPreviewList/PDFPreviewList.jsx
import React, { useEffect, useState } from 'react';
import styles from './PDFPreviewList.module.css';

// Die PDFPreviewList-Komponente zeigt eine Liste von PDF-Dateien an.
// Jede Datei wird in einem iframe als Vorschau angezeigt, und die Dateien können ausgewählt oder entfernt werden.
const PDFPreviewList = ({ files, onRemoveFile, onSelectFile }) => {
    // State zum Speichern der generierten URLs für die PDF-Dateien
    const [fileURLs, setFileURLs] = useState([]);

    // useEffect wird verwendet, um die URLs der Dateien zu erzeugen, wenn sich die Dateien ändern
    useEffect(() => {
        if (files && files.length > 0) {
            // Erzeugt URLs für alle Dateien, indem jeder Datei ein Blob zugewiesen wird
            const urls = files.map(file => URL.createObjectURL(new Blob([file], { type: 'application/pdf' })));
            setFileURLs(urls);

            // Bereinigt die URLs, wenn die Komponente unmountet oder sich die Dateien ändern, um Speicherlecks zu vermeiden
            return () => {
                urls.forEach(url => URL.revokeObjectURL(url));
            };
        } else {
            // Setzt die URLs zurück, wenn keine Dateien vorhanden sind
            setFileURLs([]);
        }
    }, [files]);

    // Wenn keine Dateien vorhanden sind, wird ein Hinweistext angezeigt
    if (!files || files.length === 0) {
        return <p>Keine PDF-Dateien hochgeladen</p>;
    }

    return (
        <div className={styles.pdfPreviewList}>
            {files.map((file, index) => (
                <div
                    key={index}
                    className={styles.pdfPreviewItem}
                    onClick={(e) => {
                        e.preventDefault(); // Verhindert mögliche Standardaktionen
                        onSelectFile(file); // Neue Datei auswählen
                    }}
                    style={{ cursor: 'pointer' }} // Zeigt an, dass das Element klickbar ist
                >
                    {/* Das iframe zeigt die generierte URL der PDF-Datei an */}
                    <iframe
                        src={fileURLs[index]}
                        title={`PDF Vorschau ${index}`}
                        width="200"
                        height="150"
                        className={styles.pdfPreviewFrame}
                        style={{ pointerEvents: 'none' }} // Blockiert Events auf iframe, damit das übergeordnete Div klickbar ist
                    />
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
            ))}
        </div>
    );
};

export default PDFPreviewList;