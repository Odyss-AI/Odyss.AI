// src/components/UserInput/UserInput.jsx
import React, { useState } from 'react';
import styles from './UserInput.module.css';

function UserInput({ onSendMessage }) {
    const [input, setInput] = useState('');

    const handleSend = () => {
        if (input.trim()) {
            onSendMessage(input); // Nachricht senden
            setInput(''); // Eingabefeld zurücksetzen
        }
    };

    return (
        <div className={styles.userInput}>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type your message..."
            />
            <button onClick={handleSend}>Send</button>
        </div>
    );
}

export default UserInput;
