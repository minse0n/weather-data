import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ConfigForm = ({ currentConfig, onSave }) => {
  // 입력값 상태 관리
  const [formData, setFormData] = useState({
    lat: 53.0793,
    lon: 8.8017,
    interval_minutes: 30
  });

  // 부모(App)에서 받은 설정값이 있으면 폼에 채워넣기
  useEffect(() => {
    if (currentConfig) {
      setFormData(currentConfig);
    }
  }, [currentConfig]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: parseFloat(value) // 숫자로 변환
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData); // 부모 컴포넌트의 저장 함수 호출
  };

  return (
    <div style={styles.card}>
      <h3>⚙️ System Configuration</h3>
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.inputGroup}>
          <label>Latitude (위도)</label>
          <input
            type="number" step="0.0001" name="lat"
            value={formData.lat} onChange={handleChange}
            style={styles.input}
          />
        </div>
        <div style={styles.inputGroup}>
          <label>Longitude (경도)</label>
          <input
            type="number" step="0.0001" name="lon"
            value={formData.lon} onChange={handleChange}
            style={styles.input}
          />
        </div>
        <div style={styles.inputGroup}>
          <label>Interval (분)</label>
          <input
            type="number" name="interval_minutes"
            value={formData.interval_minutes} onChange={handleChange}
            style={styles.input}
          />
        </div>
        <button type="submit" style={styles.button}>Save & Apply</button>
      </form>
    </div>
  );
};

// 간단한 스타일 (CSS 파일 대신 사용)
const styles = {
  card: { padding: '20px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '20px', backgroundColor: '#f9f9f9' },
  form: { display: 'flex', gap: '15px', alignItems: 'flex-end', flexWrap: 'wrap' },
  inputGroup: { display: 'flex', flexDirection: 'column' },
  input: { padding: '8px', border: '1px solid #ccc', borderRadius: '4px' },
  button: { padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }
};

export default ConfigForm;