import React from 'react';
import '../assets/styles/ChatWindow.css'

const ChatWindow = () => {
    // Beispielhafte Nachrichten
    const messages = [
        { sender: 'Nauta', text: 'Hallo, wie geht es dir?' },
        { sender: 'User', text: 'Mir geht es gut, danke! Wie geht es dir, Nauta?' },
        { sender: 'Nauta', text: 'Auch gut, danke der Nachfrage!' },
        { sender: 'User', text: 'Super, was machst du heute noch?' },
        { sender: 'Nauta', text: 'Ich arbeite an einem neuen Projekt.' },
    ];

    return (
        <div className="chat-window-container">
            <div className="chat-header">
                I am your Assistend Nauto
            </div>
            {/* Nachrichten anzeigen */}
            {messages.map((message, index) => (
                <div
                    key={index}
                    className={`chat-message ${message.sender === 'User' ? 'user-message' : 'nauta-message'}`}
                >
                    {message.text}
                </div>
            ))}
        </div>
    );
};

export default ChatWindow;
