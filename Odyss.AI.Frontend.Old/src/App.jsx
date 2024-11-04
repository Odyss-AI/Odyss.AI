// src/App.js
import React from 'react';
import ChatPage from './pages/ChatPage/ChatPage.jsx';
import LoginPage from './pages/LoginPage/LoginPage.jsx';
import useAuthStore from './store/authStore';
import Header from './components/Header/Header.jsx';


function App() {
    const isLoggedIn = useAuthStore((state) => state.isLoggedIn);  // Authentifizierungsstatus holen

    return (
        <div>
            <Header />
            {/* Zeige entweder die Login-Seite oder die Chat-Seite basierend auf dem Login-Status */}
            {isLoggedIn ? <ChatPage /> : <LoginPage />}
        </div>
    );
}

export default App;