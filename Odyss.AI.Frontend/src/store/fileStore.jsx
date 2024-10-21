// src/store/fileStore.js
import { create } from 'zustand';

// Zustand Store zur Verwaltung der hochgeladenen PDF-Dateien
const useFileStore = create((set) => ({
    files: [], // Der Zustand, um mehrere Dateien zu speichern
    firstFile: null, // Speichert die erste Datei zur Vorschau
    setFiles: (newFiles) => {
        set({ files: newFiles, firstFile: newFiles[0] || null }); // Speichert alle Dateien und die erste Datei separat
    },
    clearFiles: () => {
        set((state) => {
            if (state.firstFile) {
                URL.revokeObjectURL(URL.createObjectURL(state.firstFile));
            }
            return { files: [], firstFile: null };
        });
    },

}));

// Füge dies hinzu, um den Store global zugänglich zu machen
if (typeof window !== 'undefined') {
    window.store = useFileStore;
}

export default useFileStore;
