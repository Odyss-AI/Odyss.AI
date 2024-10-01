import React from 'react';
import './App.css';
import ChatInputUser from "./components/ChatInputUser.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import Header from "./components/Header.jsx";
import DragAndDropField from "./components/DragAndDropField.jsx";
import {useState} from "react";



const App = () => {
    const [isUserLogidIn, setUserLogidIn] = useState(false);

    return (
      <>
      <Header/>
          {!isUserLogidIn && <>
              <DragAndDropField/>
              <ChatWindow/>
              <ChatInputUser/>
          </>}

      </>
  );
};

export default App;
