import React, { useEffect, useState } from 'react';
import { fetchSearchHistory } from '../api';

const SearchHistory = ({ onRun }) => {
    const [list, setList] = useState([]);

    useEffect(() => {
        fetchSearchHistory().then(setList).catch(console.error);
    }, []);

    return (
        <div style={{ marginTop: '10px' }}>
            <h4>Search History</h4>
            <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
                {list.map(item => (
                    <li key={item.id} style={{ marginBottom: '6px' }}>
                        <button onClick={() => onRun({
                            query: item.query,
                            lat: item.lat,
                            lon: item.lon,
                            start: item.start_time,
                            end: item.end_time
                        })} style={{ cursor: 'pointer' }}>
                            {item.query || `${item.lat},${item.lon}`} — {item.timestamp}
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchHistory;
