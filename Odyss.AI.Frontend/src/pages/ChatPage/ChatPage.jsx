// src/pages/ChatPage/ChatPage.jsx
import React from 'react';
import ChatWindow from '../../components/ChatWindow/ChatWindow.jsx';
import UserInput from '../../components/UserInput/UserInput.jsx';
import DragAndDrop from '../../components/DragAndDrop/DragAndDrop.jsx';
import SelectModell from '../../components/SelectModell/SelectModell.jsx';
import styles from './ChatPage.module.css';
import useChatStore from '../../store/chatStore'; // Beispiel, um Nachrichten zu bekommen

function ChatPage() {
    const messages = useChatStore((state) => state.messages); // Holt die Nachrichten aus dem Zustand
    const sendMessage = useChatStore((state) => state.sendMessage); // Holt die sendMessage-Funktion

    return (
        <div className={styles.chatPage}>
            {/* Linke Seite: SelectModell und Drag and Drop Container */}
            <div className={styles.leftContainer}>
                <SelectModell /> {/* Oben platziert */}
                <DragAndDrop /> {/* Mittig platziert */}
            </div>

            {/* Rechte Seite: Chat Fenster und User Input */}
            <div className={styles.rightContainer}>
                <ChatWindow messages={messages} />  {/* Nachrichtenliste übergeben */}
                <UserInput onSendMessage={sendMessage} /> {/* Nachricht senden */}
            </div>
        </div>
    );
}

export default ChatPage;
