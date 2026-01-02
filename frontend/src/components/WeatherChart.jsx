import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const WeatherChart = ({ history }) => {
    
    const sortedData = [...history].reverse();
    const labels = sortedData.map(item => new Date(item.timestamp).toLocaleTimeString());
    const temps = sortedData.map(item => item.temp);
    const humidities = sortedData.map(item => item.humidity);

    const data = {
        labels,
        datasets: [
            {
                label: 'Temperature (°C)',
                data: temps,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                tension: 0.3,
            },
            {
                label: 'Humidity (%)',
                data: humidities,
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                tension: 0.3,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Temperature and Humidity Trend' },
        },
    };

    return <Line options={options} data={data} />;
};

export default WeatherChart;