// src/components/ChatWindow/ChatWindow.jsx
import React from 'react';
import UserMessage from '../UserMessage/UserMessage';
import BotMessage from '../BotMessage/BotMessage';
import styles from './ChatWindow.module.css';

function ChatWindow({ messages }) {
    return (
        <div className={styles.chatWindow}>
            {messages.map((msg, index) => (
                msg.sender === 'user' ?  // Prüfen auf 'sender', nicht 'type'
                    <div className={styles.userMessageContainer} key={index}>
                        <UserMessage message={msg.text} />
                    </div> :
                    <div className={styles.botMessageContainer} key={index}>
                        <BotMessage message={msg.text} />
                    </div>
            ))}
        </div>
    );
}

export default ChatWindow;
