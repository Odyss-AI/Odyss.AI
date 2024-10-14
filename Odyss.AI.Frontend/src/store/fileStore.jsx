import {create} from 'zustand';

// Zustand Store zur Verwaltung der hochgeladenen PDF-Datei
const useFileStore = create((set) => ({
    file: null, // Der Zustand, um die Datei zu speichern
    setFile: (file) => set({ file }), // Methode, um die Datei zu setzen
}));

export default useFileStore;
