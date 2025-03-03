// src/components/UserInput/UserInput.jsx
import React, { useState } from 'react';
import styles from './UserInput.module.css';

function UserInput({ onSendMessage }) {
    const [input, setInput] = useState('');

    const handleSend = () => {
        console.log('Sending message:', input);
        if (input.trim()) {
            onSendMessage(input); // Nachricht senden
            setInput(''); // Input leeren
        }
    };

    return (
        <div className={styles.userInput}>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Schreibe eine Nachricht ..."
            />
            <button onClick={handleSend}>Sende</button>
        </div>
    );
}

export default UserInput;
