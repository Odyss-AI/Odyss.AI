// src/pages/ChatPage/ChatPage.jsx
import React, { useState } from 'react';
import ChatWindow from '../../components/ChatWindow/ChatWindow.jsx';
import UserInput from '../../components/UserInput/UserInput.jsx';
import DragAndDrop from '../../components/DragAndDrop/DragAndDrop.jsx';
import SelectModell from '../../components/SelectModell/SelectModell.jsx';
import Sidebar from '../../components/Sidebar/Sidebar.jsx';
import styles from './ChatPage.module.css';
import useChatStore from '../../store/chatStore';
import PDFPreview from "../../components/PDFPreview/PDFPreview.jsx";

function ChatPage() {
    const [selectedChat, setSelectedChat] = useState(null);
    const [newChatName, setNewChatName] = useState("");

    const chats = useChatStore((state) => state.chatList);
    const allChats = useChatStore((state) => state.chats);
    const sendMessage = useChatStore((state) => state.sendMessage);
    const addChat = useChatStore((state) => state.addChat);
    const deleteChat = useChatStore((state) => state.deleteChat);


    // Verwende useMemo, um die Nachrichten für den ausgewählten Chat nur dann zu berechnen, wenn sich selectedChat oder allChats ändern.
    const chatMessages = selectedChat ? allChats[selectedChat.id] || [] : [];

    const handleSelectChat = (chat) => {
        setSelectedChat(chat);
    };

    const handleSendMessage = (message) => {
        if (selectedChat) {
            sendMessage(selectedChat.id, message);
        }
    };

    const handleAddChat = () => {
        if (newChatName.trim()) {
            addChat(newChatName);
            setNewChatName("");  // Eingabefeld zurücksetzen
        }
    };

    const handleDeleteChat = (chatId) => {
        deleteChat(chatId);
        if (selectedChat && selectedChat.id === chatId) {
            setSelectedChat(null); // Setzt den ausgewählten Chat zurück, falls er gelöscht wurde
        }
    };

    return (
        <div className={styles.chatPage}>
            {/* Sidebar auf der linken Seite */}
            <Sidebar chats={chats} onSelectChat={handleSelectChat} selectedChatId={selectedChat?.id} onDeleteChat={handleDeleteChat} />

            {/* Hauptinhalt: links Drag & Drop, rechts der Chat */}
            <div className={styles.mainContent}>
                <div className={styles.leftContainer}>
                    <SelectModell /> {/* Oben platziert */}
                    <h1>PDF Drag and Drop</h1>
                    <DragAndDrop />
                    <PDFPreview />

                    {/* Eingabefeld und Button zum Hinzufügen eines neuen Chats */}
                    <div className={styles.newChatContainer}>
                        <input
                            type="text"
                            value={newChatName}
                            onChange={(e) => setNewChatName(e.target.value)}
                            placeholder="Neuen Chat hinzufügen..."
                        />
                        <button onClick={handleAddChat}>Hinzufügen</button>
                    </div>
                </div>

                <div className={styles.rightContainer}>
                    {selectedChat ? (
                        <>
                            <ChatWindow messages={chatMessages} />  {/* Nachrichtenliste übergeben */}
                            <UserInput onSendMessage={handleSendMessage} /> {/* Nachricht senden */}
                        </>
                    ) : (
                        <p>Wähle einen Chat aus der Seitenleiste aus, um zu starten</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ChatPage;
