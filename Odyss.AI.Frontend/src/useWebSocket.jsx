import { useState, useEffect, useRef, useCallback } from 'react';
import useChatStore from './store/chatStore';
import useAuthStore from './store/authStore';

const URL = 'http://141.75.150.74:443/v1/chat';
// const BaseUrl = "http://0.0.0.0:443";

const useWebSocket = () => {
  const [socket, setSocket] = useState(null);
  const sendMessage = useChatStore((state) => state.sendMessage);
  const isLoggedIn = useAuthStore((state) => state.isLoggedIn);

  const initializeWebSocket = useCallback(() => {
    const ws = new WebSocket(URL);
    setSocket(ws);

    ws.onopen = () => {
      console.log('WebSocket connection established');
    };

    ws.onmessage = (event) => {
      const res = JSON.parse(event.data);
      console.log('Message from Backend:', res);
      sendMessage(res.chatId, res.message.content, false, res.message.timestamp, res.chunks);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed, attempting to reconnect...');
      setTimeout(initializeWebSocket, 1000); // Reconnect after 1 second
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
    let cleanup;
    if (isLoggedIn) {
      cleanup = initializeWebSocket();
    }
    return () => {
      if (cleanup) cleanup();
    };
  }, [isLoggedIn, initializeWebSocket]);

  const sendMessageToOdyss = useCallback((message, chatId, user, selectedModel, timestamp) => {
    console.log('Sending message to Odyss:', message, chatId, user, selectedModel, timestamp);
    if (socket && socket.readyState === WebSocket.CLOSED) {
      initializeWebSocket();
    }
      const msg = {
        message: message,
        username: user,
        chatId: chatId,
        model: selectedModel,
        timestamp: timestamp
      };

      setTimeout(() => {
        if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(msg));
        } else {
          console.error('WebSocket is not open. Ready state:', socket?.readyState);
        }

      }, 2000); // Pause for 2 seconds
  }, [socket]);

  return { initializeWebSocket, sendMessageToOdyss };
};

export default useWebSocket;