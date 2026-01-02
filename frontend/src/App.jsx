import React, { useEffect, useState } from 'react';
import { fetchHistory, fetchStatus, updateSettings } from './api';
import WeatherChart from './components/WeatherChart';
import SettingsForm from './components/SettingsForm';

function App() {
    const [history, setHistory] = useState([]);
    const [settings, setSettings] = useState(null);
    const [loading, setLoading] = useState(true);

    // 데이터 불러오기 함수
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
            alert("Backend 연결 실패! 서버가 켜져 있나요?");
        } finally {
            setLoading(false);
        }
    };

    // 초기 실행
    useEffect(() => {
        loadData();
    }, []);

    // 설정 업데이트 핸들러
    const handleUpdateSettings = async (city, interval) => {
        try {
            setLoading(true);
            await updateSettings(city, interval);
            alert(`설정 변경 완료: ${city} (${interval}분)`);
            // 설정 변경 후 최신 데이터 다시 로드
            await loadData();
        } catch (error) {
            alert("설정 업데이트 실패");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1 style={{ textAlign: 'center' }}>🌤️ Weather Dashboard (React)</h1>
            
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
                        <h3>📜 Recent History</h3>
                        <table border="1" cellPadding="10" style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
                            <thead style={{ background: '#f4f4f4' }}>
                                <tr>
                                    <th>Time</th>
                                    <th>City</th>
                                    <th>Temp (°C)</th>
                                    <th>Humidity (%)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {history.map((row, idx) => (
                                    <tr key={idx}>
                                        <td>{row.timestamp}</td>
                                        <td>{row.city}</td>
                                        <td>{row.temp}</td>
                                        <td>{row.humidity}</td>
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