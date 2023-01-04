import React, { useEffect, useState } from "react";
import { Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import axios from 'axios';

const makeGraphQLRequest = function (query, variables = {}) {
    return axios({
        url: '/graphql',
        method: 'POST',
        data: {
            query,
            variables,
        },
    });
};


const COUNTRIES = [...new Set(DEMO_TEAMS.map(team => team.country))];


function TopTeams() {

    const [selectedCountry, setSelectedCountry] = useState("");

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);

    useEffect(() => {
        setProcData(null);
        setGQLData(null);

        if (selectedCountry) {
            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}`);
                setProcData(DEMO_TEAMS.filter(t => t.country === selectedCountry));
            }, 500);

            // Make the GraphQL request to get the data for the selected country
            const query = `
            query GetCountries($name: String!) {
              countries(name: $name) {
                name
              }
            }
          `;

            const variables = {
                country: selectedCountry,
            };

            makeGraphQLRequest(query, variables).then(response => {
                console.log(`fetching from ${process.env.REACT_APP_API_GRAPHQL_URL}`);
                setGQLData(response.data.teams);
            });
        }
    }, [selectedCountry]);

    return (
        <>
            <h1>Top Teams</h1>

            <Container maxWidth="100%"
                sx={{ backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem" }}>
                <Box>
                    <h2 style={{ color: "white" }}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">Country</InputLabel>
                        <Select
                            labelId="countries-select-label"
                            id="demo-simple-select"
                            value={selectedCountry}
                            label="Country"
                            onChange={(e, v) => {
                                setSelectedCountry(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                                COUNTRIES.map(c => <MenuItem key={c} value={c}>{c}</MenuItem>)
                            }
                        </Select>
                    </FormControl>
                </Box>
            </Container>

            <Container maxWidth="100%" sx={{
                backgroundColor: 'info.dark',
                padding: "2rem",
                marginTop: "2rem",
                borderRadius: "1rem",
                color: "white"
            }}>
                <h2>Results <small>(PROC)</small></h2>
                {
                    procData ?
                        <ul>
                            {
                                procData.map(data => <li>{data.team}</li>)
                            }
                        </ul> :
                        selectedCountry ? <CircularProgress /> : "--"
                }
                <h2>Results <small>(GraphQL)</small></h2>
                {
                    gqlData ?
                        <ul>
                            {
                                gqlData.map(data => <li>{data.team}</li>)
                            }
                        </ul> :
                        selectedCountry ? <CircularProgress /> : "--"
                }
            </Container>
        </>
    );
}

export default TopTeams;
