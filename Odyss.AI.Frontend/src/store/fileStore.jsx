// src/store/fileStore.js
import {create} from 'zustand';

const useFileStore = create((set) => ({
    files: [],  // Liste der hochgeladenen Dateien

    uploadFiles: (newFiles) =>
        set((state) => ({
            files: [...state.files, ...newFiles],  // Neue Dateien zur Liste hinzufügen
        })),

    clearFiles: () => set({ files: [] }),  // Alle Dateien entfernen
}));

export default useFileStore;
