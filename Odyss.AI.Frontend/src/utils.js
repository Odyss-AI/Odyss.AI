import axios from 'axios';

const BaseUrl = "http://127.0.0.1:5000";

// GET-Anfrage
const getUser = (user) => {
    axios.get(`${BaseUrl}/users/getuser`, {
        params: {
            username: user
        }
    })
    .then(response => {
        console.log(response.data);
        return response.data;
    })
    .catch(error => {
        console.error(error);
    });
}

const createUser = (user) => {
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

const uploadDocument = (document, user) => {
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

export { getUser, createUser, uploadDocument, getChats };