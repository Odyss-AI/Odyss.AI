// src/store/chatStore.js
import { create } from 'zustand';

const useChatStore = create((set) => ({
    chats: {},  // Ein Objekt, in dem die Nachrichten für jeden Chat gespeichert werden
    chatList: [],  // Eine Liste von Chats, die es gibt (mit Name und ID)

    // Funktion zum Senden einer Nachricht an einen bestimmten Chat
    sendMessage: (chatId, message) =>
        set((state) => ({
            chats: {
                ...state.chats,
                [chatId]: [
                    ...(state.chats[chatId] || []),  // Vorhandene Nachrichten für den Chat abrufen (oder leeres Array, falls keine existieren)
                    { sender: 'user', text: message, timestamp: new Date().toLocaleTimeString() }
                ],
            },
        })),

    // Funktion zum Empfangen einer Nachricht in einem bestimmten Chat
    receiveMessage: (chatId, message) =>
        set((state) => ({
            chats: {
                ...state.chats,
                [chatId]: [
                    ...(state.chats[chatId] || []),
                    { sender: 'bot', text: message, timestamp: new Date().toLocaleTimeString() }
                ],
            },
        })),

    // Funktion zum Hinzufügen eines neuen Chats
    addChat: (chatName) =>
        set((state) => {
            const newChatId = state.chatList.length + 1; // ID basierend auf der Länge der aktuellen Liste generieren
            return {
                chatList: [
                    ...state.chatList,
                    { id: newChatId, name: chatName }
                ],
                chats: {
                    ...state.chats,
                    [newChatId]: []  // Initialer leerer Chat
                }
            };
        }),

    // Funktion zum Löschen eines Chats
    deleteChat: (chatId) =>
        set((state) => {
            const updatedChatList = state.chatList.filter((chat) => chat.id !== chatId);
            const { [chatId]: _, ...updatedChats } = state.chats;  // Entfernt den Chat aus den Nachrichten
            return {
                chatList: updatedChatList,
                chats: updatedChats
            };
        }),
}));

export default useChatStore;
