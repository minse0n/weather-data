import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const HistoryChart = ({ data }) => {
  // 차트는 시간 순서대로(과거->현재) 그려야 하므로 데이터를 뒤집어줍니다.
  // 백엔드에서는 최신순(DESC)으로 오기 때문입니다.
  const chartData = [...data].reverse();

  return (
    <div style={{ height: '400px', width: '100%', marginBottom: '30px' }}>
      <h3>📈 Weather History</h3>
      <ResponsiveContainer>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="timestamp" 
            tickFormatter={(time) => new Date(time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} 
          />
          <YAxis />
          <Tooltip labelFormatter={(label) => new Date(label).toLocaleString()} />
          <Legend />
          <Line type="monotone" dataKey="temp" stroke="#8884d8" name="Temperature (°C)" strokeWidth={2} />
          <Line type="monotone" dataKey="humidity" stroke="#82ca9d" name="Humidity (%)" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HistoryChart;