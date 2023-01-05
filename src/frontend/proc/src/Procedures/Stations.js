import React, { useState, useEffect } from 'react';

const API_ENDPOINT = 'http://localhost:20003/graphql';

const STATIONS_QUERY = `
  query {
    stations {
      name
    }
  }
`;

function Stations() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const response = await fetch(API_ENDPOINT, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        query: STATIONS_QUERY,
                    }),
                });
                const result = await response.json();
                setData(result.data);
            } catch (e) {
                setError(e);
            }
            setLoading(false);
        };
        fetchData();
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error :</p>;
    if (!data) return null;
    return (
        <div>
            <h1>Station Names</h1>
            <ul>
                {data.stations.map(station => (
                    <li key={station.name}>{station.name}</li>
                ))}
            </ul>
        </div>
    );
}

export default Stations;
