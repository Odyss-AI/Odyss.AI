/* src/pages/ChatPage/ChatPage.jsx */
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

function ChatPage() {
    const [selectedChat, setSelectedChat] = React.useState(null);
    const [newChatName, setNewChatName] = React.useState("");

    // Zugriff auf den Zustand für PDF-Dateien und die aktuelle Auswahl
    const files = useFileStore((state) => state.files);
    const setFiles = useFileStore((state) => state.setFiles);
    const selectedFile = useFileStore((state) => state.selectedFile);
    const setSelectedFile = useFileStore((state) => state.setSelectedFile);

    // Setze die erste Datei als Standardauswahl, wenn noch keine Datei ausgewählt wurde
    useEffect(() => {
        if (files.length > 0 && !selectedFile) {
            setSelectedFile(files[0]);
            console.log("Setting default seleceted File",files[0])
        }
    }, [files, selectedFile, setSelectedFile]);

    const chats = useChatStore((state) => state.chatList);
    const allChats = useChatStore((state) => state.chats);
    const sendMessage = useChatStore((state) => state.sendMessage);
    const addChat = useChatStore((state) => state.addChat);
    const deleteChat = useChatStore((state) => state.deleteChat);

    const chatMessages = selectedChat ? allChats[selectedChat.id] || [] : [];

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
            setNewChatName("");  // Eingabefeld zurücksetzen
        }
    };

    const handleDeleteChat = (chatId) => {
        deleteChat(chatId);
        if (selectedChat && selectedChat.id === chatId) {
            setSelectedChat(null); // Setzt den ausgewählten Chat zurück, falls er gelöscht wurde
        }
    };

    const handleSelectPDF = (pdf) => {
        setSelectedFile(pdf); // Setze die neue ausgewählte PDF für die Hauptanzeige
        console.log("Selected PDF", pdf)
    };

    return (
        <div className={styles.chatPage}>
            <div className={styles.mainContent}>
                {/* Linke Spalte: Neuer Chat hinzufügen und Sidebar */}
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

                {/* Mittlere Spalte: SelectModell, DragAndDrop, PDFPreview */}
                <div className={styles.middleContainer}>
                    <SelectModell />
                    <DragAndDrop />
                    {selectedFile && <PDFPreview />} {/* Zeigt die ausgewählte PDF-Datei */}
                    <PDFPreviewList onSelectPDF={handleSelectPDF} /> {/* PDF-Liste zum Auswählen */}
                </div>

                {/* Rechte Spalte: ChatWindow, UserInput */}
                <div className={styles.rightContainer}>
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