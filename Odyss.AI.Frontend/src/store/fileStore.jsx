import { create } from 'zustand';

const useFileStore = create((set) => ({
    files: [],  // Liste hochgeladener Dateien

    // Action zum Hochladen einer Datei
    uploadFile: (file) => set((state) => ({
        files: [...state.files, file]  // Datei zur Liste der Dateien hinzufügen
    })),

    // Dateien zurücksetzen oder löschen
    resetFiles: () => set({ files: [] })
}));

export default useFileStore;
