// src/components/BotMessage.js
import React from 'react';

function BotMessage({ text }) {
    return (
        <div className="bot-message">
            <p>{text}</p>
        </div>
    );
}

export default BotMessage;
