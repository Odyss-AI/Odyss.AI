// src/store/chatStore.js
import { create } from 'zustand';

const useChatStore = create((set) => ({
    messages: [],  // Liste aller Nachrichten im Chat

    sendMessage: (message) =>
        set((state) => ({
            messages: [...state.messages, { sender: 'user', text: message, timestamp: new Date().toLocaleTimeString() }],  // Neue Benutzer-Nachricht mit Zeitstempel hinzufügen
        })),

    receiveMessage: (message) =>
        set((state) => ({
            messages: [...state.messages, { sender: 'bot', text: message, timestamp: new Date().toLocaleTimeString() }],  // Neue Bot-Nachricht hinzufügen
        })),
}));

export default useChatStore;
