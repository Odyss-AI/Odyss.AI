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
                    [newChatId]: {
                        messages: [],
                        files: [],
                        selectedFile: null,
                        showDragAndDrop: true, // Default-Wert true, das Feld ist standardmäßig sichtbar
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
                    files: [...(state.chats[chatId]?.files || []), ...files],
                    showDragAndDrop: false, // Drag-and-Drop-Feld nach dem Hochladen der Dateien ausblenden
                }
            }
        })),

    // Funktion zum Löschen einer Datei aus einem bestimmten Chat
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
                    selectedFile: file,
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
                    showDragAndDrop: !state.chats[chatId]?.showDragAndDrop,
                }
            }
        })),
}));

export default useChatStore;
