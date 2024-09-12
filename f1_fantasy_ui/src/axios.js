import axios from 'axios';

const apiClient = axios.create({
    // baseURL: 'https://f1-fantasy-model-backend.onrender.com',
    baseURL: 'http://localhost:8000', // Replace with your API base URL
    headers: {
    // 'Content-Type': 'application/json',
// Add other default headers if necessary
},
//   timeout: 10000, // Optional: specify a timeout for requests
});

export default apiClient;
