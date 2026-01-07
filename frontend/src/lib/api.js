import axios from 'axios';

const api = axios.create({
    baseURL: '/api/v1', // Proxy handles this in dev, Nginx in prod
    timeout: 10000,
});

export default api;
