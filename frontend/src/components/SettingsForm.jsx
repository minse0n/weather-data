import React, { useState, useEffect } from 'react';

const SettingsForm = ({ currentSettings, onUpdate }) => {
    const [city, setCity] = useState("");
    const [interval, setInterval] = useState(30);

    useEffect(() => {
        if (currentSettings) {
            setCity(currentSettings.city);
            setInterval(currentSettings.interval);
        }
    }, [currentSettings]);

    const handleSubmit = (e) => {
        e.preventDefault();
        onUpdate(city, interval);
    };

    return (
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
            <h3>⚙️ Configuration</h3>
            <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px', alignItems: 'flex-end' }}>
                <div>
                    <label>Target City:</label><br/>
                    <input 
                        type="text" 
                        value={city} 
                        onChange={(e) => setCity(e.target.value)} 
                        style={{ padding: '8px' }}
                    />
                </div>
                <div>
                    <label>Interval (min):</label><br/>
                    <input 
                        type="number" 
                        value={interval} 
                        onChange={(e) => setInterval(e.target.value)} 
                        style={{ padding: '8px' }}
                    />
                </div>
                <button type="submit" style={{ padding: '8px 16px', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Update & Run
                </button>
            </form>
        </div>
    );
};

export default SettingsForm;