import axios from 'axios';

const BaseUrl = "http://127.0.0.1:443";

// GET-Anfrage
const getUser = async (user) => {
    try{
        const response = await axios.get(`${BaseUrl}/users/getuser`, {
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
    axios.post(`${BaseUrl}/users/adduser`, {
        id: "",
        username: user,
        documents: []
    })
    .then(response => {
        console.log(response.data);
        return response.data;
    })
    .catch(error => {
        console.error(error);
    });
}

const uploadDocument = async (document, user) => {
    axios.post(`${BaseUrl}/docs/upload`, 
        document,
        {
            headers: { 'Content-Type': 'multipart/form-data'},
            params: {
                username: user
            }
        }
    )
    .then(response => {
        console.log(response.data);
        return response.data;
    })
    .catch(error => {
        console.error(error);
    });
}

const getChats = async (user) => {
    try {
      const response = await axios.get(`${BaseUrl}/users/getchats`, {
        params: {
          username: user
        }
      });
      console.log(response.data);
      return response.data.chats[0];
    } catch (error) {
      console.error(error);
      return [];
    }
  };

const createChat = async (user, chatName, docIds = []) => {
    try {
        const response = await axios.post(`${BaseUrl}/users/addchat`, {
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

export { getUser, createUser, uploadDocument, getChats, createChat };