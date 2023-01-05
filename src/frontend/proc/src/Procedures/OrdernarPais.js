import React, { useState, useEffect } from 'react';
import { Table } from 'react-bootstrap';

const API_ENDPOINT = 'http://localhost:20003/graphql';

const stationCountByCountryQuery = `
  query {
    stationCountByCountry {
      name
      stationCount
    }
  }
`;

function OrdenarPais() {
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
                        query: stationCountByCountryQuery,
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
    if (error) return <p>Error : {error.message}</p>;
    if (!data) return null;
    return (
        <div>
            <h1>Número de Estações por País</h1>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>País</th>
                        <th>Número de Estações</th>
                    </tr>
                </thead>
                <tbody>
                    {data.stationCountByCountry.map(country => (
                        <tr key={country.name}>
                            <td>{country.name}</td>
                            <td>{country.stationCount}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
}

export default OrdenarPais;
