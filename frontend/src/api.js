import axios from 'axios';

const API_BASE_URL = "http://127.0.0.1:8000";

export const fetchHistory = async () => {
    const response = await axios.get(`${API_BASE_URL}/api/history`);
    return response.data;
};

export const fetchStatus = async () => {
    const response = await axios.get(`${API_BASE_URL}/api/status`);
    return response.data;
};

export const updateSettings = async (city, interval) => {
    const response = await axios.post(`${API_BASE_URL}/api/settings`, {
        city,
        interval: parseInt(interval)
    });
    return response.data;
};