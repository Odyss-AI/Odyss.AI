// src/components/Sidebar/Sidebar.jsx
import React from 'react';
import styles from './Sidebar.module.css';

function Sidebar({ chats, onSelectChat, selectedChatId, onDeleteChat }) {
    return (
        <div className={styles.sidebar}>
            <h2>Chats</h2>
            <ul className={styles.chatList}>
                {chats.map((chat) => (
                    <li
                        key={chat.id}
                        className={`${styles.chatItem} ${selectedChatId === chat.id ? styles.active : ''}`}
                    >
                        <span onClick={() => onSelectChat(chat)} className={styles.chatName}>
                          {chat.name}
                        </span>
                        <button onClick={() => onDeleteChat(chat.id)} className={styles.deleteButton}>
                            Löschen
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Sidebar;
