// src/components/Sidebar/Sidebar.jsx
import React, { useState } from 'react';
import styles from './Sidebar.module.css';

function Sidebar({ chats, onSelectChat, selectedChatId, onDeleteChat }) {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true); // Zustand für das Öffnen/Schließen der Sidebar

    // Funktion zum Umschalten der Sidebar
    const toggleSidebar = () => {
        setIsSidebarOpen((prev) => !prev);
    };

    return (
        <div className={`${styles.sidebar} ${isSidebarOpen ? styles.open : styles.closed}`}>
            {/* Schaltfläche zum Öffnen/Schließen der Sidebar */}
            <button onClick={toggleSidebar} className={styles.toggleButton}>
                {isSidebarOpen ? '<-' : '->'}
            </button>

            {/* Sidebar-Inhalt wird nur angezeigt, wenn die Sidebar geöffnet ist */}
            {isSidebarOpen && (
                <>
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
                </>
            )}
        </div>
    );
}

export default Sidebar;
