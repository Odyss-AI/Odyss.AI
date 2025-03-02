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
import useAuthStore from '../../store/authStore.jsx';
import useWebSocket from '../../useWebSocket.jsx';
import { createChat, deleteChatFromDb, uploadDocument } from '../../utils.js';

function ChatPage() {
    const [selectedChat, setSelectedChat] = React.useState(null);
    const [newChatName, setNewChatName] = React.useState("");
    const [showMiddle, setShowMiddle] = React.useState(true);
    const [selectedModel, setSelectedModel] = React.useState("mistral");

    const chats = useChatStore((state) => state.chatList);
    const allChats = useChatStore((state) => state.chats);
    const sendMessage = useChatStore((state) => state.sendMessage);
    const deleteChat = useChatStore((state) => state.deleteChat);
    const removeFileFromChat = useChatStore((state) => state.removeFileFromChat);
    const setSelectedFile = useChatStore((state) => state.setSelectedFile);
    const toggleDragAndDrop = useChatStore((state) => state.toggleDragAndDrop);
    const username = useAuthStore((state) => state.username);

    const chatMessages = selectedChat ? allChats[selectedChat.id]?.messages || [] : [];
    const chatFiles = selectedChat ? allChats[selectedChat.id]?.files || [] : [];
    const selectedFile = selectedChat ? allChats[selectedChat.id]?.selectedFile : null;
    const showDragAndDrop = selectedChat ? allChats[selectedChat.id]?.showDragAndDrop : true;

    const { sendMessageToOdyss } = useWebSocket();

    useEffect(() => {
        if (chatFiles.length > 0 && !selectedFile) {
            setSelectedFile(selectedChat.id, chatFiles[0]);
        }
    }, [chatFiles, selectedFile, selectedChat, setSelectedFile]);

    const handleSelectChat = (chat) => {
        console.log("Chat ausgewählt: ", chat);
        setSelectedChat(chat);
    };

    const handleSendMessage = (message) => {
        if (selectedChat) {
            const timestamp = new Date().toISOString();
            console.log("Message sent: ", message, selectedChat);
            sendMessage(selectedChat.id, message, true, timestamp);
            sendMessageToOdyss(message, selectedChat.id, username.user.username, selectedModel, timestamp);
        }
    };

    const handleDeleteChat = async (chatId) => {
        if (selectedChat && selectedChat.id === chatId) {
            console.log("Chat löschen: ", chatId);
            const chatDeleteMsg = await deleteChatFromDb(chatId);
            console.log("Chat gelöscht: ", chatDeleteMsg);
            if (!chatDeleteMsg) {
                console.error("Fehler beim Löschen des Chats");
                alert("Fehler beim Löschen des Chats");
                return;
            }
            deleteChat(chatId);
            setSelectedChat(null);
        }
    };

    // const handleFileDrop = async (newFiles) => {
    //     if (selectedChat) {
    //         const files = await uploadDocument(newFiles, username.user.username, selectedChat.id);
    //         if (!files) {
    //             console.error("Fehler beim Hochladen der Datei");
    //             alert("Fehler beim Hochladen der Datei");
    //             return;
    //         }
    //         addFilesToChat(selectedChat.id, newFiles);
    //     }
    // };

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

                    <Sidebar
                        chats={chats}
                        onSelectChat={handleSelectChat}
                        selectedChatId={selectedChat?.id}
                        onDeleteChat={handleDeleteChat}
                    />
                </div>
                {!selectedChat && <div className={styles.noChatSelected}>Wähle einen Chat aus oder erstelle einen neuen 🎯</div>}
                {selectedChat && <div className={styles.mainContentContainer}>
                    <div className={styles.chatWindowAndInputContainer}>
                        {selectedChat && showMiddle && (
                        <div className={styles.chatWindowContainer}>
                            {console.log(chatMessages)}
                            {<ChatWindow messages={chatMessages} /> }
                        </div>)}
                        
                        {selectedChat && <UserInput onSendMessage={handleSendMessage} />}
                        {selectedChat && <SelectModell setSelectedModel={setSelectedModel}/>}
                    </div>

                    <div className={styles.pdfPreviewContainer}>
                        {showDragAndDrop ? (<DragAndDrop username={username} selectedChat={selectedChat}/>
                        ) : (
                            <button className={styles.toggleDragAndDropButton} onClick={() => toggleDragAndDrop(selectedChat.id)}>
                                Weitere PDF-Dateien hochladen
                            </button>
                        )}
                        {selectedFile && <PDFPreview file={selectedFile} />}
                        <PDFPreviewList
                            files={chatFiles}
                            onRemoveFile={handleRemoveFile}
                            onSelectFile={(file) => setSelectedFile(selectedChat.id, file)}/>
                    </div>
                </div>}
            </div>
        </div>
    );
}

export default ChatPage;
