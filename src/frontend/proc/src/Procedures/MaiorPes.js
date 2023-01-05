import React, { useState, useEffect } from 'react';

const API_ENDPOINT = 'http://localhost:20003/graphql';

const MAIOR_PES_QUERY = `
query {
    maiorPes {
      id
      name
      class_
      countryId
      horarioId
      iata
      icao
      pes
      fonte
      createdOn
      updatedOn
    }
  }
`;

function MaiorPes() {
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
                        query: MAIOR_PES_QUERY,
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
            <h1>Station with Highest PES</h1>
            <ul>
                <li>ID: {data.maiorPes.id}</li>
                <li>Name: {data.maiorPes.name}</li>
                <li>Class: {data.maiorPes.class_}</li>
                <li>Country ID: {data.maiorPes.countryId}</li>
                <li>Horario ID: {data.maiorPes.horarioId}</li>
                <li>IATA: {data.maiorPes.iata}</li>
                <li>ICAO: {data.maiorPes.icao}</li>
                <li>PES: {data.maiorPes.pes}</li>
                <li>Fonte: {data.maiorPes.fonte}</li>
                <li>Created On: {data.maiorPes.createdOn}</li>
                <li>Updated On: {data.maiorPes.updatedOn}</li>
            </ul>
        </div>
    );
}

export default MaiorPes;

