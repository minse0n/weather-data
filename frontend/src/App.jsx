import React, { useEffect, useState } from 'react';
import { fetchHistory, fetchStatus, updateSettings } from './api';
import WeatherChart from './components/WeatherChart';
import SettingsForm from './components/SettingsForm';

function App() {
    const [history, setHistory] = useState([]);
    const [settings, setSettings] = useState(null);
    const [loading, setLoading] = useState(true);

    const loadData = async () => {
        try {
            const [historyData, statusData] = await Promise.all([
                fetchHistory(),
                fetchStatus()
            ]);
            setHistory(historyData);
            setSettings(statusData);
        } catch (error) {
            console.error("Failed to fetch data:", error);
            alert("Failed to connect to backend. Is the server running?");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);


    const handleUpdateSettings = async (lat, lon, interval) => {
        try {
            setLoading(true);
            await updateSettings(lat, lon, interval);
            alert(`Settings updated: Lat ${lat}, Lon ${lon} (${interval} min)`);
            await loadData();
        } catch (error) {
            console.error(error);
            alert("Failed to update settings");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            
            {loading && <p style={{ textAlign: 'center' }}>Loading...</p>}
            
            {!loading && settings && (
                <SettingsForm 
                    currentSettings={settings} 
                    onUpdate={handleUpdateSettings} 
                />
            )}

            {!loading && history.length > 0 && (
                <>
                    <WeatherChart history={history} />
                    
                    <div style={{ marginTop: '30px' }}>
                        <h3>Recent History</h3>
                        <table border="1" cellPadding="10" style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
                            <thead style={{ background: '#f4f4f4' }}>
                                <tr>
                                    <th>Time</th>
                                    <th>City</th>
                                    <th>Temp (°C)</th>
                                    <th>Humidity (%)</th>
                                    <th>Latitude</th>
                                    <th>Longitude</th> 
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                {history.map((row, idx) => (
                                    <tr key={idx}>
                                        <td>{row.timestamp}</td>
                                        <td>{row.city}</td>
                                        <td>{row.temp}</td>
                                        <td>{row.humidity}</td>
                                        <td>{row.lat}</td>
                                        <td>{row.lon}</td> 
                                        <td>{row.description}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </>
            )}
        </div>
    );
}

export default App;