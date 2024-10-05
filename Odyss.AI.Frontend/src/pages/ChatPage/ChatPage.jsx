// src/pages/ChatPage/ChatPage.jsx
import React from 'react';
import ChatWindow from '../../components/ChatWindow/ChatWindow.jsx';
import UserInput from '../../components/UserInput/UserInput.jsx';
import DragAndDrop from '../../components/DragAndDrop/DragAndDrop.jsx';
import styles from './ChatPage.module.css';
import useChatStore from '../../store/chatStore'; // Holt den Zustand aus dem Zustand-Management

function ChatPage() {
    const messages = useChatStore((state) => state.messages); // Holt die Nachrichten aus dem Zustand
    const sendMessage = useChatStore((state) => state.sendMessage); // Holt die sendMessage-Funktion

    // Diese Funktion wird als Callback an das UserInput übergeben und von dort aufgerufen
    const handleSendMessage = (message) => {
        sendMessage(message); // Die Nachricht wird in den Zustand geschickt
    };

    return (
        <div className={styles.chatPage}>
            {/* Linke Seite: Drag and Drop Container */}
            <div className={styles.leftContainer}>
                <DragAndDrop />
            </div>

            {/* Rechte Seite: Chat Fenster und User Input */}
            <div className={styles.rightContainer}>
                <ChatWindow messages={messages} />  {/* Nachrichtenliste übergeben */}
                <UserInput onSendMessage={handleSendMessage} /> {/* Nachricht senden */}
            </div>
        </div>
    );
}

export default ChatPage;
