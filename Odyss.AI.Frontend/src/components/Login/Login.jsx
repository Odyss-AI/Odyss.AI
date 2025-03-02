// src/components/Login.js
import React, { useState } from 'react';
import useAuthStore from '../../store/authStore.jsx';
import useChatStore from '../../store/chatStore.jsx';
import { getUser, getChats, createUser } from '../../utils.js';
import useWebSocket from '../../useWebSocket.jsx';
import styles from './Login.module.css';

function Login() {
    const [username, setUsername] = useState('');  // Benutzername
    const [password, setPassword] = useState('');  // Passwort
    const login = useAuthStore((state) => state.login);  // Login-Funktion holen
    const addChat = useChatStore((state) => state.addChat);  // Chat hinzufügen
    const sendMessage = useChatStore((state) => state.sendMessage);  // Nachricht senden

    const { initializeWebSocket } = useWebSocket();

    const dummyUser = {
        id: "user123",
        username: "dummyUser",
        documents: []
    };

    // const msg1 = { content: "Hallo", isUser: true, timestamp: "2021-07-01T12:00:00.000Z" };
    // const msg2 = { content: "Hallo zurück", is_user: false, timestamp: "2021-07-01T12:01:00.000Z" };
    // const chats = [{ chat_name:  "test", messages: [msg1, msg2], id: 1 }];
    
    const handleLogin = async () => {
        if (username && password) {
            const user = await getUser(username);  // Benutzerdaten überprüfen
            if (!user) {
                console.log('User not found');
                alert('User not found');
                return;
            }
            console.log('User found:', user);
            login(username);  // Login-Logik hier
            
            const chats = await getChats(username);  // Chats des Benutzers laden
            if (!chats) {
                console.log('Error fetching chats');
                alert('Error fetching chats');
                return;
            }
            chats.forEach(chat => {
            //     //TODO: Hole tatsächliche Dokumente anhand der file_ids
                addChat(chat.chat_name, [], [], chat.id);  // Chat hinzufügen
                chat.messages.forEach(message => {
                    sendMessage(chat.id, message.content, message.is_user, message.timestamp);  // Nachrichten hinzufügen
                })
            });

            initializeWebSocket();  // WebSocket initialisieren
        }
        else {
            alert('Please enter username and password');
        }
    };

    return (
        <div className={styles.loginForm}>
            <h2>Login</h2>
            <input
                type="text"
                placeholder="Username"
                value={username}
                className={styles.input}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                className={styles.input}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button className={styles.loginButton} onClick={handleLogin}>Login</button>
        </div>
    );
}

export default Login;