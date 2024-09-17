import { useState, useEffect, useRef, useCallback } from 'react';

const URL = 'http://127.0.0.1:5000/chat';

const useWebSocket = (isUser, chatsCalled) => {
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  
  // Funktion zum Senden einer Nachricht über den WebSocket
  const sendMessage = useCallback((message, chatId, user) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const msg = {
            message: message,
            username: user,
            chat_id: chatId,
        };
        socket.send(JSON.stringify(msg));
      } else {
        // Füge die Nachricht zur Liste hinzu, auch wenn keine Verbindung besteht
        setMessages((prevMessages) => [...prevMessages, {  }]);
      }
    }, [socket]);

  useEffect(() => {
    if (!isUser && !chatsCalled) return;

    // WebSocket-Verbindung erstellen
    const ws = new WebSocket(URL);
    setSocket(ws);

    // WebSocket-Nachrichten-Handler
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log('Message from Backend:', message);
      setMessages((prevMessages) => [...prevMessages, message]);
      console.log('Messages in Websocket:', messages);
    };

    // WebSocket-Verbindung schließen beim Unmounten der Komponente
    return () => {
      ws.close();
    };
  }, [isUser]);

  return { messages, sendMessage };
};

export default useWebSocket;