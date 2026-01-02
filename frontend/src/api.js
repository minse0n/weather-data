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

export const updateSettings = async (lat, lon, interval) => {
    const response = await axios.post(`${API_BASE_URL}/api/settings`, {
        lat: parseFloat(lat),
        lon: parseFloat(lon),
        interval: parseInt(interval)
    });
    return response.data;
};

export const fetchHistoryFiltered = async ({ city, start, end, limit } = {}) => {
    const params = new URLSearchParams();
    if (city) params.append('city', city);
    if (start) params.append('start', start);
    if (end) params.append('end', end);
    if (limit) params.append('limit', limit);
    const response = await axios.get(`${API_BASE_URL}/api/history?${params.toString()}`);
    return response.data;
};

export const postSearch = async ({ query, lat, lon, start, end }) => {
    const response = await axios.post(`${API_BASE_URL}/api/search`, { query, lat, lon, start, end });
    return response.data;
};

export const fetchSearchHistory = async (limit = 50) => {
    const response = await axios.get(`${API_BASE_URL}/api/searches?limit=${limit}`);
    return response.data;
};