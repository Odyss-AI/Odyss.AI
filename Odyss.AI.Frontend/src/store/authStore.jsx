// src/store/authStore.js
import {create} from 'zustand';

const useAuthStore = create((set) => ({
    isLoggedIn: false,  // Status, ob der Benutzer eingeloggt ist
    username: '',

    login: (username) => set({ isLoggedIn: true, username }),  // Login-Funktion
    logout: () => set({ isLoggedIn: false, username: '' }),  // Logout-Funktion
}));

export default useAuthStore;
