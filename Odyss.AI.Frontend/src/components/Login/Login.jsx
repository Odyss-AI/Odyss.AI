// src/components/Login.js
import React, { useState } from 'react';
import useAuthStore from '../../store/authStore.jsx';

function Login() {
    const [username, setUsername] = useState('');  // Benutzername
    const [password, setPassword] = useState('');  // Passwort
    const login = useAuthStore((state) => state.login);  // Login-Funktion holen

    const handleLogin = () => {
        if (username && password) {
            login(username);  // Login-Logik hier
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
