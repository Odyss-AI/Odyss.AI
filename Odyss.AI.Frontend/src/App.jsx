import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [user, setUser] = useState('');
  const [chats, setChats] = useState([]);
  const [message, setMessage] = useState('');
  const [isUser, setIsUser] = useState(false);

  const handleChatInputChange = (event) => {
    setMessage(event.target.value);
  };

  const handleUserInputChange = (event) => {
    setUser(event.target.value);
  }

  const handleSendMessage = () => {
    console.log('Message:', message);
    setChats([...chats, { user: user, message: message, isUser: true }, { user: 'Odyss.AI', message: 'I am a bot', isUser: false }]);
  };

  return (
    <>
      {!isUser && <header>
        <h1>Welcome to Odyss.AI</h1>
        <div>
          <input onChange={handleUserInputChange} type="text" placeholder='Insert username' />
          <button>Create</button>
          <button onClick={() => setIsUser(true)}>Sign In</button>
        </div>

        <div>
          <h3>Upload Document</h3>
          <div>
            <input type="file" />
            <button>Upload</button>
          </div>
        </div>
      </header>}

      {isUser && <main>
        <h3>Chat Test</h3>
        <div className="chat-container">
          <div>
            {chats.map((chat, index) => (
              <div key={index} className={`chat-message ${chat.isUser ? 'user' : 'bot'}`}>
                <p className='chat-user'>{chat.user}</p>
                <p className='chat-msg'>{chat.message}</p>
              </div>
            ))}
          </div>
        </div>
        <div className='chat-input-container'>
            <input
              type="text"
              placeholder='Type a message'
              value={message}
              onChange={handleChatInputChange}
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
      </main>}
    </>
  );
}

export default App;