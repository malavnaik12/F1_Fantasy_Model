import axios from 'axios';

const apiClient = axios.create({
    // baseURL: 'https://f1-fantasy-model-backend.onrender.com/',
    baseURL: 'http://localhost:8000', 
});

export default apiClient;
