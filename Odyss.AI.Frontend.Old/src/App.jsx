import React, { useState, useEffect } from 'react';
import useWebSocket from './useWebSocket';
import { getUser, createUser, uploadDocument, getChats } from './utils';
import './App.css';

function App() {
  const [user, setUser] = useState('');
  const [chatsCalled, setChatsCalled] = useState(false);
  const [hasMessages, setHasMessages] = useState(false);
  const [isUser, setIsUser] = useState(false);
  const [userData, setUserData] = useState(null);
  const [lastMessage, setLastMessage] = useState(null);
  const { messages, sendMessage } = useWebSocket(isUser, chatsCalled);
  const [chats, setChats] = useState(null);
  const [chatId, setChatId] = useState('66e5930ac00137d9fa4c3782');
  const [message, setMessage] = useState('');
  const [file, setFile] = useState(null);
  const [document, setDocument] = useState(null);
  const [selectedChat, setSelectedChat] = useState(null);

  useEffect(() => {
    console.log('Chat changed:', chats);
  }, [chats]);

  const handleChatInputChange = (event) => {
    setMessage(event.target.value);
  };

  const handleUserInputChange = (event) => {
    setUser(event.target.value);
  }

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSendMessageTest = () => {
    console.log('Message:', message);
    sendMessage([...chats, { user: user, message: message, isUser: true }, { user: 'Odyss.AI', message: 'I am a bot', isUser: false }]);
  };

  const handleSendMessage = () => {
    const messageInsert = { user: user, content: message, is_user: true };
    setChats([...chats, messageInsert]);
    sendMessage(message, chatId, user);
  }

  const handleUserSignIn = () => {
    const fetchUser = getUser(user);
    setUserData(fetchUser);
    setIsUser(true);
  };

  const handleUserCreate = () => {
    const fetchUser = createUser(user);
    setUserData(fetchUser);
    setIsUser(true);
  };

  const handleUploadDocument = () => {
    if (!file) return
    const formData = new FormData();
    formData.append('file', file);
    uploadDocument(formData, user);
  }

  useEffect(() => {
    const fetchChats = async () => {
      if (isUser) {
        const fetchedChats = await getChats(user);
        console.log("Chats:", fetchedChats);
        setChats(fetchedChats.messages);
        setChatsCalled(true);
        if (fetchedChats.messages.length > 0) {
          setHasMessages(true);
        }
        if(fetchedChats?.chatId) {
          setChatId(fetchedChats.chatId);
        }
      }
    };

    fetchChats();
  }, [isUser]);

  useEffect(() => {
    console.log('Messages in app:', messages);
    if (messages.length > 0) {
      setHasMessages(true);
      const lastMessage = messages[messages.length - 1];
      console.log('Last Message:', lastMessage);
      setChats([...chats, lastMessage.message]);
      setLastMessage(lastMessage);
    }
  }, [messages]);

  return (
    <>
      {!isUser && <header>
        <h1>Welcome to Odyss.AI</h1>
        <div>
          <input onChange={handleUserInputChange} type="text" placeholder='Insert username' />
          <button onClick={handleUserCreate}>Create</button>
          <button onClick={handleUserSignIn}>Sign In</button>
        </div>

        <div>
          <h3>Upload Document</h3>
          <div>
            <input onChange={handleFileChange} type="file" />
            <button onClick={handleUploadDocument}>Upload</button>
          </div>
        </div>
      </header>}

      {isUser && <main>
        <h3>Chat {chatId}</h3>
        <div className="chat-container">
          <div>
            {hasMessages && Array.isArray(chats) && chats.map((chat, index) => (
              <div key={index} className={`chat-message ${hasMessages && chat?.is_user ? 'user' : 'bot'}`}>
                <p className='chat-user'>{user}</p>
                <p className='chat-msg'>{hasMessages && chat?.content}</p>
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

        {hasMessages && lastMessage?.chunks &&<div>
          <h3>Simalarity</h3>
          <div className="chat-container">
            <div>
              {lastMessage.chunks.map((chunkObj, index) => (
                console.log('Chunk:', chunkObj),
                <div key={index} className='chunk bot'>
                  <p className='chat-user'>{chunkObj.chunk[1]}</p>
                  <p className='chat-msg'>{chunkObj.chunk[0]}</p>
                </div>
              ))}
            </div>
          </div>
        </div>}
      </main>}
    </>
  );
}

export default App;