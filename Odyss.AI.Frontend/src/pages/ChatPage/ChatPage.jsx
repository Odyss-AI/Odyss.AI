/* src/pages/ChatPage/ChatPage.jsx */
import React, { useState } from 'react';
import ChatWindow from '../../components/ChatWindow/ChatWindow.jsx';
import UserInput from '../../components/UserInput/UserInput.jsx';
import DragAndDrop from '../../components/DragAndDrop/DragAndDrop.jsx';
import SelectModell from '../../components/SelectModell/SelectModell.jsx';
import Sidebar from '../../components/Sidebar/Sidebar.jsx';
import Footer from '../../components/Footer/Footer.jsx';
import styles from './ChatPage.module.css';
import useChatStore from '../../store/chatStore';
import PDFPreview from '../../components/PDFPreview/PDFPreview.jsx';

function ChatPage() {
    const [selectedChat, setSelectedChat] = useState(null);
    const [newChatName, setNewChatName] = useState("");

    const chats = useChatStore((state) => state.chatList);
    const allChats = useChatStore((state) => state.chats);
    const sendMessage = useChatStore((state) => state.sendMessage);
    const addChat = useChatStore((state) => state.addChat);
    const deleteChat = useChatStore((state) => state.deleteChat);

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
            <header className={styles.header}></header>
            <div className={styles.mainContent}>
                {/* Linke Spalte: Neuer Chat hinzufügen und Sidebar */}
                <div className={styles.sidebarContainer}>
                    <div className={styles.newChatContainer}>
                        <input
                            type="text"
                            value={newChatName}
                            onChange={(e) => setNewChatName(e.target.value)}
                            placeholder="Neuen Chat hinzufügen..."
                        />
                        <button onClick={handleAddChat}>Hinzufügen</button>
                    </div>
                    <Sidebar chats={chats} onSelectChat={handleSelectChat} selectedChatId={selectedChat?.id} onDeleteChat={handleDeleteChat} />
                </div>

                {/* Mittlere Spalte: SelectModell, DragAndDrop, PDFPreview */}
                <div className={styles.middleContainer}>
                    <SelectModell />
                    <DragAndDrop />
                    <PDFPreview />
                </div>

                {/* Rechte Spalte: ChatWindow, UserInput */}
                <div className={styles.rightContainer}>
                    <div className={styles.chatWindowContainer}>
                        {selectedChat ? (
                            <ChatWindow messages={chatMessages} />
                        ) : (
                            <p>Wähle einen Chat aus der Seitenleiste aus, um zu starten</p>
                        )}
                    </div>
                    <UserInput onSendMessage={handleSendMessage} />
                </div>
            </div>
            <Footer />
        </div>
    );
}

export default ChatPage;