// src/components/ChatWindow/ChatWindow.jsx
import React from 'react';
import styles from './ChatWindow.module.css';
import useAuthStore from '../../store/authStore';

function ChatWindow({ messages }) {

    const username = useAuthStore((state) => state.username);
    console.log("user: "+  username);
    return (
        <div className={styles.chatWindow}>
            {messages.map((msg, index) => (
                <div key={index} className={msg.isUser ? styles.userMessageContainer : styles.botMessageContainer}>
                    <span>{msg.text}</span>
                    <div className={styles.messageInfo}>
                        {msg.isUser && <span>{username}</span>}
                        {!msg.isUser && <span>odyss</span>}
                        <span>{new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})}</span>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default ChatWindow;
