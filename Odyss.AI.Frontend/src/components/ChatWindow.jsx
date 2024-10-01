import React from 'react';
import '../assets/styles/ChatWindow.css'
import useChatStore from '../store/useChatStore';

const ChatWindow = () => {
    const { messages } = useChatStore();

    return (
        <div className="chat-window-container">
            {messages.length === 0 ? (
                <p>No messages yet</p>
            ) : (
                messages.map((msg, index) => <div key={index} className="message">{msg}</div>)
            )}
        </div>
    );
};

export default ChatWindow;


