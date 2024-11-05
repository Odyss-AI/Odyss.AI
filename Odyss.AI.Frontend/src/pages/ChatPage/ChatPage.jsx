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

function ChatPage() {
    const [selectedChat, setSelectedChat] = React.useState(null);
    const [newChatName, setNewChatName] = React.useState("");
    const [showMiddle, setShowMiddle] = React.useState(true); // Zustand für die Anzeige der mittleren Spalte

    const chats = useChatStore((state) => state.chatList);
    const allChats = useChatStore((state) => state.chats);
    const sendMessage = useChatStore((state) => state.sendMessage);
    const addChat = useChatStore((state) => state.addChat);
    const deleteChat = useChatStore((state) => state.deleteChat);
    const addFilesToChat = useChatStore((state) => state.addFilesToChat);
    const removeFileFromChat = useChatStore((state) => state.removeFileFromChat);
    const setSelectedFile = useChatStore((state) => state.setSelectedFile);

    const chatMessages = selectedChat ? allChats[selectedChat.id]?.messages || [] : [];
    const chatFiles = selectedChat ? allChats[selectedChat.id]?.files || [] : [];
    const selectedFile = selectedChat ? allChats[selectedChat.id]?.selectedFile : null;

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

    const handleAddChat = () => {
        if (newChatName.trim()) {
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
                <div className={styles.sidebarContainer}>
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

                {/* Mittlere Spalte ein-/ausblenden */}
                {selectedChat && (
                    <>
                        <button className={styles.toggleMiddleButton} onClick={() => setShowMiddle(!showMiddle)}>
                            {showMiddle ? '<' : '>'}
                        </button>
                        {showMiddle && (
                            <div className={styles.middleContainer}>
                                <SelectModell />
                                <DragAndDrop onFileDrop={handleFileDrop} />
                                {selectedFile && <PDFPreview file={selectedFile} />} {/* Zeigt die ausgewählte PDF-Datei */}
                                <PDFPreviewList
                                    files={chatFiles}
                                    onRemoveFile={handleRemoveFile}
                                    onSelectFile={(file) => setSelectedFile(selectedChat.id, file)}
                                /> {/* PDF-Liste zum Auswählen */}
                            </div>
                        )}
                    </>
                )}

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
                </div>
            </div>
            <Footer />
        </div>
    );
}

export default ChatPage;
