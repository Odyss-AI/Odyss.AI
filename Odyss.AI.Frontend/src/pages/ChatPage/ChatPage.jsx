// src/pages/ChatPage/ChatPage.jsx
import React, { useEffect } from 'react';
import ChatWindow from '../../components/ChatWindow/ChatWindow.jsx';
import UserInput from '../../components/UserInput/UserInput.jsx';
import DragAndDrop from '../../components/DragAndDrop/DragAndDrop.jsx';
import SelectModell from '../../components/SelectModell/SelectModell.jsx';
import Sidebar from '../../components/Sidebar/Sidebar.jsx';
import Footer from '../../components/Footer/Footer.jsx';
import styles from './ChatPage.module.css';
import useChatStore from '../../store/chatStore';
import PDFPreview from '../../components/PDFPreview/PDFPreview.jsx';
import PDFPreviewList from '../../components/PDFPreviesList/PDFPreviewList.jsx';
import useFileStore from '../../store/fileStore.jsx';
import useAuthStore from '../../store/authStore.jsx';
import { createChat } from '../../utils.js';
import { Alert } from '@mui/material';

function ChatPage() {
    const [selectedChat, setSelectedChat] = React.useState(null);
    const [newChatName, setNewChatName] = React.useState("");
    const [showMiddle, setShowMiddle] = React.useState(true);

    const chats = useChatStore((state) => state.chatList);
    const allChats = useChatStore((state) => state.chats);
    const sendMessage = useChatStore((state) => state.sendMessage);
    const addChat = useChatStore((state) => state.addChat);
    const deleteChat = useChatStore((state) => state.deleteChat);
    const addFilesToChat = useChatStore((state) => state.addFilesToChat);
    const removeFileFromChat = useChatStore((state) => state.removeFileFromChat);
    const setSelectedFile = useChatStore((state) => state.setSelectedFile);
    const toggleDragAndDrop = useChatStore((state) => state.toggleDragAndDrop);

    const chatMessages = selectedChat ? allChats[selectedChat.id]?.messages || [] : [];
    const chatFiles = selectedChat ? allChats[selectedChat.id]?.files || [] : [];
    const selectedFile = selectedChat ? allChats[selectedChat.id]?.selectedFile : null;
    const showDragAndDrop = selectedChat ? allChats[selectedChat.id]?.showDragAndDrop : true;

    useEffect(() => {
        if (chatFiles.length > 0 && !selectedFile) {
            setSelectedFile(selectedChat.id, chatFiles[0]);
        }
    }, [chatFiles, selectedFile, selectedChat, setSelectedFile]);

    const handleSelectChat = (chat) => {
        setSelectedChat(chat);
    };

    const handleSendMessage = (message) => {
        if (selectedChat) {
            sendMessage(selectedChat.id, message);
        }
    };

    const handleAddChat = async () => {
        if (newChatName.trim()) {
            const newChat = await createChat(username, newChatName);
            // newChat enthält neben dem Chat-Namen auch die ID und andere Informationen
            if (!newChat) {
                console.error("Fehler beim Erstellen des Chats");
                alert("Fehler beim Erstellen des Chats");
            }
            else {
                console.log("Neuer Chat erstellt");
                addChat(newChat.chat_name);
            }

            setNewChatName("");  // Eingabefeld zurücksetzen
            addChat(newChatName);
            setNewChatName("");
        }
    };

    const handleDeleteChat = (chatId) => {
        deleteChat(chatId);
        if (selectedChat && selectedChat.id === chatId) {
            setSelectedChat(null);
        }
    };

    const handleFileDrop = (newFiles) => {
        if (selectedChat) {
            addFilesToChat(selectedChat.id, newFiles);
        }
    };

    const handleRemoveFile = (fileIndex) => {
        if (selectedChat) {
            removeFileFromChat(selectedChat.id, fileIndex);
        }
    };

    return (
        <div className={styles.chatPage}>
            <div className={styles.mainContent}>
                {/* Linke Spalte */}
                <div className={styles.sidebarContainer}>
                    <button onClick={()=>setDocViewOpen(!docViewOpen)}>Zeige Dokumente</button>
                    <div className={styles.newChatContainer}>
                        <input
                            type="text"
                            value={newChatName}
                            onChange={(e) => setNewChatName(e.target.value)}
                            placeholder="Neuen Chat hinzufügen..."
                        />
                        <button onClick={handleAddChat}>Hinzufügen</button>
                    </div>
                    <Sidebar
                        chats={chats}
                        onSelectChat={handleSelectChat}
                        selectedChatId={selectedChat?.id}
                        onDeleteChat={handleDeleteChat}
                    />
                </div>

                {/* Toggle Button für die mittlere Spalte */}
                {selectedChat && (
                    <button className={styles.toggleMiddleButton} onClick={() => setShowMiddle(!showMiddle)}>
                        {showMiddle ? '<' : '>'}
                    </button>
                )}

                {/* Mittlere Spalte */}
                {selectedChat && showMiddle && (
                    <div className={styles.middleContainer}>
                        {showDragAndDrop ? (
                            <DragAndDrop onFileDrop={handleFileDrop} />
                        ) : (
                            <button className={styles.toggleDragAndDropButton} onClick={() => toggleDragAndDrop(selectedChat.id)}>
                                Weitere PDF-Dateien hochladen
                            </button>
                        )}
                        {selectedFile && <PDFPreview file={selectedFile} />}
                        <PDFPreviewList
                            files={chatFiles}
                            onRemoveFile={handleRemoveFile}
                            onSelectFile={(file) => setSelectedFile(selectedChat.id, file)}
                        />
                    </div>
                )}

                {/* Rechte Spalte */}
                <div className={
                    selectedChat
                        ? showMiddle
                            ? styles.rightContainer
                            : styles.rightContainerExpanded
                        : styles.rightContainerExpanded
                }>
                    <div className={styles.chatWindowContainer}>
                        {selectedChat ? (
                            <ChatWindow messages={chatMessages} />
                        ) : (
                            <p>Wähle einen Chat aus der Seitenleiste aus, um zu starten</p>
                        )}
                    </div>
                    <UserInput onSendMessage={handleSendMessage} />
                    <SelectModell />
                </div>
            </div>
            <Footer />
        </div>
    );
}

export default ChatPage;
