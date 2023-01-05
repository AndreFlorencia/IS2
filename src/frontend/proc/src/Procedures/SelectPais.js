import { useState, useEffect } from 'react';

const API_ENDPOINT = 'http://localhost:20003/graphql';

const GET_COUNTRIES_QUERY = `
  query {
    countries {
      id
      name
      createdOn
      updatedOn
    }
  }
`;

const GET_STATIONS_IN_COUNTRY_QUERY = `
  query($countryName: String!) {
    stationsInCountry(countryName: $countryName) {
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

function SelectPais() {
    const [countries, setCountries] = useState([]);
    const [stations, setStations] = useState([]);
    const [error, setError] = useState(null);
    const [country, setCountry] = useState('');

    useEffect(() => {
        async function getCountries() {
            try {
                const response = await fetch(API_ENDPOINT, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        query: GET_COUNTRIES_QUERY,
                    }),
                });
                const result = await response.json();
                setCountries(result.data.countries);
            } catch (e) {
                setError(e);
            }
        }
        getCountries();
    }, []);

    useEffect(() => {
        async function getStations() {
            try {
                const response = await fetch(API_ENDPOINT, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        query: GET_STATIONS_IN_COUNTRY_QUERY,
                        variables: { countryName: country },
                    }),
                });
                const result = await response.json();
                setStations(result.data.stationsInCountry);
            } catch (e) {
                setError(e);
            }
        }
        getStations();
    }, [country]);
    if (error) return <p>Error :(</p>;

    return (
        <div>
            <p>Selecionar País</p>
            <select onChange={e => setCountry(e.target.value)}>
                {countries.map(country => (
                    <option key={country.id} value={country.name}>
                        {country.name}
                    </option>
                ))}
            </select>
            <div className="stations-container">
                <p>List of Stations:</p>
                <ul>
                    {stations.map(station => (
                        <li key={station.id}>{station.name}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default SelectPais;
