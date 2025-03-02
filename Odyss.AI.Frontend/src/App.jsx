// src/App.js
import React from 'react';
import ChatPage from './pages/ChatPage/ChatPage.jsx';
import LoginPage from './pages/LoginPage/LoginPage.jsx';
import useAuthStore from './store/authStore';
import Header from './components/Header/Header.jsx';
import Footer from './components/Footer/Footer.jsx';

function App() {
    const isLoggedIn = useAuthStore((state) => state.isLoggedIn);  // Authentifizierungsstatus holen

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
            <Header />
            {/* Zeige entweder die Login-Seite oder die Chat-Seite basierend auf dem Login-Status */}
            <div style={{ padding: '20px', height: '100%', overflowY: 'auto' }}>
                {isLoggedIn ? <ChatPage /> : <LoginPage />}
            </div>
            <Footer />
        </div>
    );
}

export default App;