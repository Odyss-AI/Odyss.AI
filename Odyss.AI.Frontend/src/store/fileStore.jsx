// src/store/fileStore.js
import { create } from 'zustand';

// Zustand Store zur Verwaltung der hochgeladenen PDF-Dateien
const useFileStore = create((set) => ({
    files: [], // Der Zustand, um mehrere Dateien zu speichern
    selectedFile: null, // Speichert die aktuell ausgewählte Datei zur Vorschau
    hasUploadedFiles: false, // Neu: Boolean, um zu wissen, ob bereits Dateien hochgeladen sind

    // Setzt neue Dateien, ohne `selectedFile` zu überschreiben, wenn bereits eine Datei ausgewählt ist
    setFiles: (newFiles) => {
        set((state) => {
            const combinedFiles = [...state.files, ...newFiles]; // Bestehende Dateien und neue Dateien kombinieren
            return {
                files: combinedFiles,
                selectedFile: state.selectedFile ? state.selectedFile : combinedFiles[0] || null, // Behalte die ausgewählte Datei bei oder setze die erste Datei, wenn keine ausgewählt ist
                hasUploadedFiles: combinedFiles.length > 0,
            };
        });
    },

    // Funktion zum Setzen der ausgewählten Datei
    setSelectedFile: (file) => {
        set({ selectedFile: file });
    },

    // Funktion zum Leeren der Dateien
    clearFiles: () => {
        set((state) => {
            if (state.selectedFile) {
                URL.revokeObjectURL(URL.createObjectURL(state.selectedFile));
            }
            return {
                files: [],
                selectedFile: null,
                hasUploadedFiles: false,
            };
        });
    },
}));

export default useFileStore;
