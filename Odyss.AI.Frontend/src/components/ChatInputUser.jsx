import React, { useState } from 'react';
import "../assets/styles/ChatInputUser.css"
import useChatStore from '../store/useChatStore';

const ChatInput = () => {
    const [input, setInput] = useState('');
    const addMessage = useChatStore((state) => state.addMessage);

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && input.trim() !== '') {
            addMessage(input);
            setInput('');  // Leert das Textfeld nach dem Absenden
        }
    };

    return (
        <input
            type="text"
            className="chat-input-container"
            placeholder="What is on your mind?"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
        />
    );
};

export default ChatInput;
