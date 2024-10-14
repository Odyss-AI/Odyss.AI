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

    // Beispiel-Chats, die angezeigt werden
    const chats = [
        { id: 1, name: 'Chat mit Bot A' },
        { id: 2, name: 'Chat mit Bot B' },
        { id: 3, name: 'Chat mit Bot C' },
    ];

    const messages = useChatStore((state) => state.messages); // Nachrichten aus Zustand
    const sendMessage = useChatStore((state) => state.sendMessage); // Nachricht senden

    const handleSelectChat = (chat) => {
        setSelectedChat(chat);
        // Hier könntest du auch Logik hinzufügen, um die Nachrichten für den ausgewählten Chat zu laden
    };

    return (
        <div className={styles.chatPage}>
            {/* Sidebar auf der linken Seite */}
            <Sidebar chats={chats} onSelectChat={handleSelectChat} />

            {/* Hauptinhalt: links Drag & Drop, rechts der Chat */}
            <div className={styles.mainContent}>
                <div className={styles.leftContainer}>
                    <SelectModell /> {/* Oben platziert */}
                    <h1>PDF Drag and Drop</h1>
                    <DragAndDrop />
                    <PDFPreview />
                </div>

                <div className={styles.rightContainer}>
                    {selectedChat ? (
                        <>
                            <ChatWindow messages={messages} />  {/* Nachrichtenliste übergeben */}
                            <UserInput onSendMessage={sendMessage} /> {/* Nachricht senden */}
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
