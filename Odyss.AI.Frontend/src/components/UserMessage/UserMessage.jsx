// src/components/UserMessage/UserMessage.jsx
import React from 'react';
import styles from './UserMessage.module.css';

function UserMessage({ message }) {  // 'message' ist jetzt ein String
    return (
        <div className={styles.userMessage}>
            <p>{message}</p> {/* Direkt den Text der Nachricht anzeigen */}
            {/* Optional: Zeitstempel hier hinzufügen, wenn notwendig */}
        </div>
    );
}

export default UserMessage;
