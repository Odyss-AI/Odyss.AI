// src/store/chatStore.js
import { create } from 'zustand';

const useChatStore = create((set) => ({
    chats: {},  // Ein Objekt, in dem die Nachrichten und Dateien für jeden Chat gespeichert werden
    chatList: [],  // Eine Liste von Chats, die es gibt (mit Name und ID)

    // Funktion zum Senden einer Nachricht an einen bestimmten Chat
    sendMessage: (chatId, message) =>
        set((state) => ({
            chats: {
                ...state.chats,
                [chatId]: {
                    ...state.chats[chatId],
                    messages: [
                        ...(state.chats[chatId]?.messages || []),
                        { sender: 'user', text: message, timestamp: new Date().toLocaleTimeString() }
                    ],
                },
            },
        })),

    // Funktion zum Empfangen einer Nachricht in einem bestimmten Chat
    receiveMessage: (chatId, message) =>
        set((state) => ({
            chats: {
                ...state.chats,
                [chatId]: {
                    ...state.chats[chatId],
                    messages: [
                        ...(state.chats[chatId]?.messages || []),
                        { sender: 'bot', text: message, timestamp: new Date().toLocaleTimeString() }
                    ],
                },
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
                    [newChatId]: { messages: [], files: [] }  // Initialer leerer Chat mit Nachrichten und Dateien
                }
            };
        }),

    // Funktion zum Löschen eines Chats
    deleteChat: (chatId) =>
        set((state) => {
            const updatedChatList = state.chatList.filter((chat) => chat.id !== chatId);
            const { [chatId]: _, ...updatedChats } = state.chats;  // Entfernt den Chat aus den Nachrichten und Dateien
            return {
                chatList: updatedChatList,
                chats: updatedChats
            };
        }),

    // Funktionen für die Dateiverwaltung pro Chat
    addFilesToChat: (chatId, newFiles) =>
        set((state) => {
            const existingFiles = state.chats[chatId]?.files || [];
            return {
                chats: {
                    ...state.chats,
                    [chatId]: {
                        ...state.chats[chatId],
                        files: [...existingFiles, ...newFiles],
                    },
                },
            };
        }),

    removeFileFromChat: (chatId, fileIndex) =>
        set((state) => {
            const updatedFiles = [...(state.chats[chatId]?.files || [])];
            updatedFiles.splice(fileIndex, 1);
            return {
                chats: {
                    ...state.chats,
                    [chatId]: {
                        ...state.chats[chatId],
                        files: updatedFiles,
                    },
                },
            };
        }),

    setSelectedFile: (chatId, file) =>
        set((state) => ({
            chats: {
                ...state.chats,
                [chatId]: {
                    ...state.chats[chatId],
                    selectedFile: file,
                },
            },
        })),
}));

export default useChatStore;
