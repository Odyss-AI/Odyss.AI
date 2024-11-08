// src/components/BotMessage.js
import React from 'react';

function BotMessage({ text }) {
    return (
        <div className="bot-message">
            <p><strong>Nauta:</strong> {text}</p> {/* Fügt "Nauta:" vor jeder Nachricht hinzu */}
        </div>
    );
}

export default BotMessage;
