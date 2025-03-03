// src/components/Sidebar/Sidebar.jsx
import React, { useState } from 'react';
import styles from './Sidebar.module.css';
import { createChat } from '../../utils.js';
import useChatStore from '../../store/chatStore';
import useAuthStore from '../../store/authStore';

function Sidebar({ chats, onSelectChat, selectedChatId, onDeleteChat }) {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true); // Zustand für das Öffnen/Schließen der Sidebar
    const addChat = useChatStore((state) => state.addChat);
    const username = useAuthStore((state) => state.username);
    const [newChatName, setNewChatName] = React.useState("");

    // const msg1 = { content: "Hallo", isUser: true, timestamp: "2021-07-01T12:00:00.000Z" };
    // const msg2 = { content: "Hallo zurück", isUser: false, timestamp: "2021-07-01T12:01:00.000Z" };
    // const chatTest = { chat_name:  "test", messages: [msg1, msg2], id: 2 };

    const handleAddChat = async () => {
        console.log(username);
        if (newChatName.trim()) {
            const newChat = await createChat(username, newChatName);
            // newChat enthält neben dem Chat-Namen auch die ID und andere Informationen
            if (!newChat) {
                console.error("Fehler beim Erstellen des Chats");
                alert("Fehler beim Erstellen des Chats");
            }
            else {
                console.log("Neuer Chat erstellt: ", newChat);
                addChat(newChat.chat_name, [], newChat.messages, newChat.id);
            }

            setNewChatName("");
        }
    };

    // Funktion zum Umschalten der Sidebar
    const toggleSidebar = () => {
        setIsSidebarOpen((prev) => !prev);
    };

    return (
        <div className={`${styles.sidebar} ${isSidebarOpen ? styles.open : styles.closed}`}>
            <div className={styles.sidebarHeader}>
                <button onClick={toggleSidebar} className={styles.submitButton}>
                    {isSidebarOpen ? '<' : '>'}
                </button>

                {isSidebarOpen && <div className={styles.newChatContainer}>
                    <input
                        type="text"
                        value={newChatName}
                        className={styles.inputField}
                        onChange={(e) => setNewChatName(e.target.value)}
                        placeholder="Neuer Chat hinzufügen ..."
                    />
                    <button className={styles.submitButton} onClick={handleAddChat}>+</button>
                </div>}
            </div>

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
