import React, { useEffect, useState, useCallback } from 'react'; // useCallback 추가
import axios from 'axios';
// 파일 경로가 정확한지 꼭 확인하세요!
import ConfigForm from './components/ConfigForm';
import HistoryChart from './components/HistoryChart';

// 백엔드 주소 (마지막에 슬래시 / 없도록 주의)
const API_URL = "http://127.0.0.1:8000";

function App() {
  const [logs, setLogs] = useState([]);
  const [config, setConfig] = useState(null);

  // 1. fetchData 함수 정의 (useCallback으로 감싸서 메모이제이션)
  // 이렇게 하면 useEffect의 의존성 배열에 넣어도 무한 루프가 돌지 않습니다.
  const fetchData = useCallback(async () => {
    try {
      // API 호출 두 개를 병렬로 처리 (속도 향상)
      const [logsRes, configRes] = await Promise.all([
        axios.get(`${API_URL}/history`),
        axios.get(`${API_URL}/config`)
      ]);
      
      setLogs(logsRes.data);
      setConfig(configRes.data);
    } catch (error) {
      console.error("❌ Data Fetch Error:", error);
    }
  }, []); // 의존성 없음 (컴포넌트 로드 시 한 번만 생성)

  // 2. 초기 로딩 및 주기적 갱신
  useEffect(() => {
    fetchData(); // 최초 실행

    const interval = setInterval(() => {
      fetchData(); // 1분마다 실행
    }, 60000);

    return () => clearInterval(interval); // 컴포넌트가 사라질 때 타이머 정리
  }, [fetchData]); // fetchData가 변경될 때만 실행 (실질적으로는 한 번)

  // 3. 설정 저장 핸들러
  const handleSaveConfig = async (newConfig) => {
    try {
      await axios.post(`${API_URL}/config`, newConfig);
      alert("✅ 설정이 저장되고 스케줄러가 업데이트되었습니다.");
      fetchData(); // 변경된 내용 즉시 반영을 위해 다시 불러오기
    } catch (error) {
      console.error(error);
      alert("❌ 저장 실패: 백엔드 연결을 확인하세요.");
    }
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '20px', fontFamily: 'Arial' }}>
      <h1>🌦️ Weather Monitoring Dashboard</h1>
      
      {/* ConfigForm에 현재 설정값(config)과 저장 함수(handleSaveConfig) 전달 */}
      <ConfigForm currentConfig={config} onSave={handleSaveConfig} />

      {/* 차트 */}
      {/* 데이터가 있을 때만 차트를 렌더링하여 오류 방지 */}
      {logs.length > 0 ? <HistoryChart data={logs} /> : <p>Loading data...</p>}

      <h3>📋 Recent Logs</h3>
      <table border="1" cellPadding="8" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'center' }}>
        <thead style={{ backgroundColor: '#eee' }}>
          <tr>
            <th>Time</th>
            <th>City</th>
            <th>Temp</th>
            <th>Humidity</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr key={log.id}>
              <td>{new Date(log.timestamp).toLocaleString()}</td>
              <td>{log.city}</td>
              <td>{log.temp} °C</td>
              <td>{log.humidity} %</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;