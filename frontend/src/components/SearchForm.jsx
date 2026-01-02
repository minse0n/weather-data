import React, { useState } from 'react';

const SearchForm = ({ onSearch }) => {
    const [query, setQuery] = useState('');
    const [lat, setLat] = useState('');
    const [lon, setLon] = useState('');
    const [start, setStart] = useState('');
    const [end, setEnd] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        const filters = {
            query: query || null,
            lat: lat ? parseFloat(lat) : null,
            lon: lon ? parseFloat(lon) : null,
            start: start || null,
            end: end || null
        };
        onSearch(filters);
    };

    return (
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '20px' }}>
            <div>
                <label>Location (name):</label><br/>
                <input value={query} onChange={(e)=>setQuery(e.target.value)} />
            </div>
            <div>
                <label>Lat:</label><br/>
                <input type="number" step="any" value={lat} onChange={(e)=>setLat(e.target.value)} />
            </div>
            <div>
                <label>Lon:</label><br/>
                <input type="number" step="any" value={lon} onChange={(e)=>setLon(e.target.value)} />
            </div>
            <div>
                <label>Start (local):</label><br/>
                <input type="datetime-local" value={start} onChange={(e)=>setStart(e.target.value)} />
            </div>
            <div>
                <label>End (local):</label><br/>
                <input type="datetime-local" value={end} onChange={(e)=>setEnd(e.target.value)} />
            </div>
            <button type="submit" style={{ padding: '8px 12px', marginLeft: '6px' }}>Search</button>
        </form>
    );
};

export default SearchForm;
