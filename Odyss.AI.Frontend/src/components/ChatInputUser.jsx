import React from 'react';
import '../assets/styles/ChatInputUser.css'; // Importiere die CSS-Datei

const ChatInputUser = () => {
    return (
        <div className="chat-input-container">
            {/* Upload-Button mit einem Icon */}
            <button className="chat-upload-button">
                {/* Beispiel: Upload-Icon als SVG */}
                <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M5 20h14v-2H5v2zm7-18L5.33 10h3.67v4h4v-4h3.67L12 2z" />
                </svg>
            </button>
            {/* Texteingabe */}
            <input type="text" className="chat-input" placeholder="Nachricht eingeben..." />
        </div>
    );
};

export default ChatInputUser;
