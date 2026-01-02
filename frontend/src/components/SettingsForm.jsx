import React, { useState, useEffect } from 'react';

const SettingsForm = ({ currentSettings, onUpdate }) => {
    const [formState, setFormState] = useState({ lat: "", lon: "", interval: 30 });

    useEffect(() => {
        if (currentSettings) {
            setFormState({
                lat: currentSettings.lat,
                lon: currentSettings.lon,
                interval: currentSettings.interval
            });
        }
    }, [currentSettings]);

    const handleSubmit = (e) => {
        e.preventDefault();
        onUpdate(formState.lat, formState.lon, formState.interval);
    }; 

    return (
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
            <h3>⚙️ Configuration (Coordinates)</h3>
            <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
                <div>
                    <label>Latitude:</label><br/>
                    <input 
                        type="number" step="any"
                        value={formState.lat} 
                        onChange={(e) => setFormState(prev => ({ ...prev, lat: e.target.value }))} 
                        style={{ padding: '8px', width: '100px' }}
                    />
                </div>
                <div>
                    <label>Longitude:</label><br/>
                    <input 
                        type="number" step="any"
                        value={formState.lon} 
                        onChange={(e) => setFormState(prev => ({ ...prev, lon: e.target.value }))} 
                        style={{ padding: '8px', width: '100px' }}
                    />
                </div>
                <div>
                    <label>Interval (min):</label><br/>
                    <input 
                        type="number" 
                        value={formState.interval} 
                        onChange={(e) => setFormState(prev => ({ ...prev, interval: e.target.value }))} 
                        style={{ padding: '8px', width: '80px' }}
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