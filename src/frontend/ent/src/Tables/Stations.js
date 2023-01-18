import "./tables.css";
import { useEffect, useState } from "react";
import {
  CircularProgress,
  Pagination,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TableContainer,
} from "@mui/material";

function Stations() {
  const PAGE_SIZE = 10;
  const [page, setPage] = useState(1);
  const [data, setData] = useState(null);
  const [maxDataSize, setMaxDataSize] = useState(0);
  const [countries, setCountries] = useState(null);
  const [timezones, setTimezones] = useState(null);
  useEffect(() => {
    // Fetch station data from the API
    fetch(`http://localhost:20001/api/stations`)
      .then((response) => response.json())
      .then((data) => {
        // Update the data state variable with the retrieved data
        setData(
          data.filter(
            (item, index) => Math.floor(index / PAGE_SIZE) + 1 === page
          )
        );
        // Update the max data size state variable with the total number of stations returned by the API
        setMaxDataSize(data.length);
      });
  }, [page]);

  useEffect(() => {
    // Fetch country data from the API
    fetch(`http://localhost:20001/api/countries/`)
      .then((response) => response.json())
      .then((countriesData) => {
        // Create a map of country UUIDs to country names
        const countriesMap = new Map();
        countriesData.forEach((country) => {
          countriesMap.set(country[0], country[1]);
        });
        // Update the countries state variable with the created map
        setCountries(countriesMap);
      });
  }, []);

  useEffect(() => {
    // Fetch timezone data from the API
    fetch(`http://localhost:20001/api/horarios`)
      .then((response) => response.json())
      .then((timezonesData) => {
        // Create a map of timezone IDs to timezone names
        const timezonesMap = new Map();
        timezonesData.forEach((timezone) => {
          timezonesMap.set(timezone[0], timezone[1]);
        });
        // Update the timezones state variable with the created map
        setTimezones(timezonesMap);
      });
  }, []);

  if (!data || !countries || !timezones) {
    return <CircularProgress />;
  }

  return (
    <>
      <TableContainer component={Paper}>
        <Table className="table" size="small">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Class</TableCell>
              <TableCell>Country</TableCell>
              <TableCell>Time Zone</TableCell>
              <TableCell>IATA</TableCell>
              <TableCell>ICAO</TableCell>
              <TableCell>Elevation</TableCell>
              <TableCell>Source</TableCell>
              <TableCell>Created On</TableCell>
              <TableCell>Updated On</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((station) => (
              <TableRow key={station[0]}>
                <TableCell>{station[0]}</TableCell>
                <TableCell>{station[1]}</TableCell>
                <TableCell>{station[2]}</TableCell>
                <TableCell>{countries.get(station[4])}</TableCell>
                <TableCell>
                  {timezones.get(station[5]) === "\\N"
                    ? "Unknown"
                    : timezones.get(station[5])}
                </TableCell>
                <TableCell>
                  {station[6] === "\\N" ? "Unknown" : station[6]}
                </TableCell>
                <TableCell>
                  {station[7] === "\\N" ? "Unknown" : station[7]}
                </TableCell>
                <TableCell>{station[8]}</TableCell>
                <TableCell>{station[9]}</TableCell>
                <TableCell>{station[10]}</TableCell>
                <TableCell>{station[11]}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Pagination
        count={Math.ceil(maxDataSize / PAGE_SIZE)}
        page={page}
        onChange={(_, value) => setPage(value)}
      />
    </>
  );
}

export default Stations;
