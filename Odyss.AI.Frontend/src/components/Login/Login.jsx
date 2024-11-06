// src/components/Login.js
import React, { useState } from 'react';
import useAuthStore from '../../store/authStore.jsx';
import { getUser, getChats, createUser } from '../../utils.js';

function Login({isRegister}) {
    const [username, setUsername] = useState('');  // Benutzername
    const [password, setPassword] = useState('');  // Passwort
    const login = useAuthStore((state) => state.login);  // Login-Funktion holen

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