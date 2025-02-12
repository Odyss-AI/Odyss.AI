// src/store/chatStore.js
import { create } from 'zustand';

const useChatStore = create((set) => ({
    chats: {},  // Ein Objekt, in dem die Nachrichten für jeden Chat gespeichert werden
    chatList: [],  // Eine Liste von Chats, die es gibt (mit Name und ID)

    // Funktion zum Senden einer Nachricht an einen bestimmten Chat
    sendMessage: (chatId, message, isUser, timestamp, chunks = []) =>
        set((state) => ({
            chats: {
                ...state.chats,
                [chatId]: {
                    ...state.chats[chatId],
                    messages: [
                        ...(state.chats[chatId]?.messages || []),
                        { isUser: isUser, text: message, timestamp: timestamp, chunks: chunks }
                    ],
                },
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
    addChat: (chatName, files, messages, id) =>
        set((state) => {
            return {
                chatList: [
                    ...state.chatList,
                    { id: id, name: chatName }
                ],
                chats: {
                    ...state.chats,
                    [id]: {
                        messages: messages || [],
                        files: files || [],
                        selectedFile: null,
                        showDragAndDrop: true, // Default-Wert true, das Feld ist standardmäßig sichtbar
                    }
                }
            };
        }),

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

    // Funktion zum Löschen eines Chats anhand der chatId
    deleteChat: (chatId) =>
        set((state) => {
            const { [chatId]: _, ...remainingChats } = state.chats;
            return {
                chats: remainingChats,
                chatList: state.chatList.filter(chat => chat.id !== chatId),
            };
        }),
}));


export default useChatStore;
