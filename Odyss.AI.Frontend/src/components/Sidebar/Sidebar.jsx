// src/components/Sidebar/Sidebar.jsx
import React, { useState } from 'react';
import styles from './Sidebar.module.css';

function Sidebar({ chats, onSelectChat }) {
    const [selectedChat, setSelectedChat] = useState(null);

    const handleChatClick = (chat) => {
        setSelectedChat(chat.id);
        onSelectChat(chat); // Informiere die ChatPage über den neuen Chat
    };

    return (
        <div className={styles.sidebar}>
            <h2>Chats</h2>
            <ul className={styles.chatList}>
                {chats.map((chat) => (
                    <li
                        key={chat.id}
                        className={`${styles.chatItem} ${selectedChat === chat.id ? styles.active : ''}`}
                        onClick={() => handleChatClick(chat)}
                    >
                        {chat.name}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Sidebar;
