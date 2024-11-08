// src/components/ChatWindow/ChatWindow.jsx
import React from 'react';
import UserMessage from '../UserMessage/UserMessage';
import BotMessage from '../BotMessage/BotMessage';
import styles from './ChatWindow.module.css';

function ChatWindow({ messages }) {
    // Dauerhaft angezeigte Beispielnachricht für den Bot
    const defaultMessage = [
        { sender: 'bot', text: 'Hallo! Ich bin Nauta, dein Begleiter auf der Reise zu Lösungen. Wie kann ich dir helfen?' }
    ];

    // Die Default-Nachricht bleibt immer als erste Nachricht
    const allMessages = [...defaultMessage, ...messages];

    return (
        <div className={styles.chatWindow}>
            {allMessages.map((msg, index) => (
                msg.sender === 'user' ?  // Prüfen auf 'sender'
                    <div className={styles.userMessageContainer} key={index}>
                        <UserMessage message={msg.text} />
                    </div> :
                    <div className={styles.botMessageContainer} key={index}>
                        <BotMessage text={msg.text} />
                    </div>
            ))}
        </div>
    );
}

export default ChatWindow;
