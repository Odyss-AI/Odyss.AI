// src/store/chatStore.js
import { create } from 'zustand';

// Der Zustandsspeicher (ChatStore) verwaltet Chats, Nachrichten und Dateien.
const useChatStore = create((set) => ({
    chats: {}, // Speichert die einzelnen Chats mit ihren Nachrichten und Dateien
    chatList: [], // Enthält die Liste der vorhandenen Chats

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
            const newChatId = state.chatList.length + 1; // Generiert eine neue Chat-ID basierend auf der aktuellen Länge der Chatliste
            return {
                chatList: [
                    ...state.chatList,
                    { id: newChatId, name: chatName }
                ],
                chats: {
                    ...state.chats,
                    [newChatId]: {
                        messages: [],
                        files: [],
                        selectedFile: null,
                        showDragAndDrop: true, // Das Drag-and-Drop-Feld ist standardmäßig sichtbar
                    }
                }
            };
        }),

    // Funktion zum Hinzufügen von Dateien zu einem bestimmten Chat
    addFilesToChat: (chatId, files) =>
        set((state) => ({
            chats: {
                ...state.chats,
                [chatId]: {
                    ...state.chats[chatId],
                    files: [...(state.chats[chatId]?.files || []), ...files.map(file => file)], // Fügt die neuen Dateien hinzu
                    showDragAndDrop: false, // Blendet das Drag-and-Drop-Feld nach dem Hochladen der Dateien aus
                }
            }
        })),

    // Funktion zum Löschen einer Datei aus einem bestimmten Chat
    removeFileFromChat: (chatId, fileIndex) =>
        set((state) => {
            const updatedFiles = [...(state.chats[chatId]?.files || [])];
            updatedFiles.splice(fileIndex, 1); // Entfernt die Datei an der angegebenen Position
            return {
                chats: {
                    ...state.chats,
                    [chatId]: {
                        ...state.chats[chatId],
                        files: updatedFiles,
                    }
                }
            };
        }),

    // Funktion zum Setzen der ausgewählten Datei in einem bestimmten Chat
    setSelectedFile: (chatId, file) =>
        set((state) => ({
            chats: {
                ...state.chats,
                [chatId]: {
                    ...state.chats[chatId],
                    selectedFile: file, // Setzt die ausgewählte Datei für den Chat
                }
            }
        })),

    // Funktion zum Umschalten des Drag-and-Drop-Felds
    toggleDragAndDrop: (chatId) =>
        set((state) => ({
            chats: {
                ...state.chats,
                [chatId]: {
                    ...state.chats[chatId],
                    showDragAndDrop: !state.chats[chatId]?.showDragAndDrop, // Ändert den Status des Drag-and-Drop-Felds
                }
            }
        })),
}));

export default useChatStore;
