import { useState, useEffect, useRef, useCallback } from 'react';
import useChatStore from './store/chatStore';

const URL = 'http://127.0.0.1:5000/chat';

const useWebSocket = () => {
  const [socket, setSocket] = useState(null);
  const sendMessage = useChatStore((state) => state.sendMessage);

  const initializeWebSocket = useCallback(() => {
    const ws = new WebSocket(URL);
    setSocket(ws);

    ws.onopen = () => {
      console.log('WebSocket connection established');
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log('Message from Backend:', message);
      sendMessage(message.chat_id, message.message);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed, attempting to reconnect...');
      setTimeout(initializeWebSocket, 10000); // Reconnect after 1 second
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      ws.close();
    };

    return () => {
      ws.close();
    };
  }, [sendMessage]);

  useEffect(() => {
    const cleanup = initializeWebSocket();
    return cleanup;
  }, [initializeWebSocket]);

  const sendMessageToOdyss = useCallback((message, chatId, user, selectedModel, timestamp) => {
    console.log('Sending message to Odyss:', message, chatId, user, selectedModel, timestamp);
    if (socket && socket.readyState === WebSocket.OPEN) {
      const msg = {
        message: message,
        username: user,
        chatId: chatId,
        model: selectedModel,
        timestamp: timestamp
      };
      socket.send(JSON.stringify(msg));
    } else {
      console.error('WebSocket is not open. Ready state:', socket?.readyState);
    }
  }, [socket]);

  return { initializeWebSocket, sendMessageToOdyss };
};

export default useWebSocket;