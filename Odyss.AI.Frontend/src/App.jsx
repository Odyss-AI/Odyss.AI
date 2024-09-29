import React from 'react';
import './App.css';
import ChatInputUser from "./components/ChatInputUser.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import Header from "./components/Header.jsx";
import DragAndDropField from "./components/DragAndDropField.jsx";

const App = () => {
  return (
      <div>
      <Header/>
        <DragAndDropField/>
        <ChatWindow/>
        <ChatInputUser/>
      </div>
  );
};

export default App;
