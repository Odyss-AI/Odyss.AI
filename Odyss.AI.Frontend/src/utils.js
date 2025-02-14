import axios from 'axios';

const BaseUrl = "http://141.75.150.74:443";
// const BaseUrl = "http://0.0.0.0:443";

// GET-Anfrage
const getUser = async (user) => {
    try{
        const response = await axios.get(`${BaseUrl}/v1/user/get`, {
            params: {
                username: user
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error(error);
        return null;
    }
}

const createUser = async (user) => {
    console.log(user);
    try{
        const response = await axios.post(`${BaseUrl}/v1/user/add`, {
            username: user
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error(error);
        return null;
    }
}

const uploadDocument = async (files, user, chatId) => {
    try {
        const formData = new FormData();
        files.forEach((file, index) => {
            formData.append('file' + index, file);
        });
        console.log("Start uploading new document");
        const response = await axios.post(`${BaseUrl}/v1/doc/upload`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
            params: {
                username: user,
                chatId: chatId
            }
        });
        console.log(response.data);
        return response.data;
    }
    catch (error) {
        console.error(error);
    }
}

const getChats = async (user) => {
    try {
      const response = await axios.get(`${BaseUrl}/v1/user/chat/get`, {
        params: {
          username: user
        }
      });
      return response.data.chats;
    } catch (error) {
      console.error(error);
      return [];
    }
  };

const createChat = async (user, chatName, docIds = []) => {
    try {
        const response = await axios.post(`${BaseUrl}/v1/user/chat/add`, {
            username: user,
            name: chatName,
            docs: docIds
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

const deleteChatFromDb = async (chatId) => {
    try {
        const response = await axios.delete(`${BaseUrl}/v1/user/chat/delete`, {
            params: {
                chatid: chatId
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

export { getUser, createUser, uploadDocument, getChats, createChat, deleteChatFromDb };