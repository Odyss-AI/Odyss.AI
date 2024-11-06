// src/components/Login.js
import React, { useState } from 'react';
import useAuthStore from '../../store/authStore.jsx';
import useChatStore from '../../store/chatStore.jsx';
import { getUser, getChats, createUser } from '../../utils.js';
import useWebSocket from '../../useWebSocket.jsx';

function Login({isRegister}) {
    const [username, setUsername] = useState('');  // Benutzername
    const [password, setPassword] = useState('');  // Passwort
    const login = useAuthStore((state) => state.login);  // Login-Funktion holen
    const addChat = useChatStore((state) => state.addChat);  // Chat hinzufügen
    const sendMessage = useChatStore((state) => state.sendMessage);  // Nachricht senden

    const { initializeWebSocket } = useWebSocket();

    const handleLogin = async () => {

        if (username && password) {
            const user = await getUser(username);  // Benutzerdaten überprüfen
            if (!user) {
                console.log('User not found');
                alert('User not found');
                return;
            }
            login(user);  // Login-Logik hier
            
            const chats = await getChats(username);  // Chats des Benutzers laden
            if (!chats) {
                console.log('Error fetching chats');
                alert('Error fetching chats');
                return;
            }
            
            chats.forEach(chat => {
                //TODO: Hole tatsächliche Dokumente anhand der file_ids
                addChat(chat.chat_name, [], chat.messages, chat.id);  // Chat hinzufügen
                chat.messages.forEach(message => {
                    sendMessage(chat.id, message.text, message.isUser, message.timestamp);  // Nachrichten hinzufügen
                })
            });

            initializeWebSocket();  // WebSocket initialisieren
        }
        else {
            alert('Please enter username and password');
        }
    };

    return (
        <div className="login">
            <h2>Login</h2>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleLogin}>Login</button>
        </div>
    );
}

export default Login;