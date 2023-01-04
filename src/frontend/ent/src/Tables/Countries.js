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
    TableContainer
} from "@mui/material";


function Countries() {

    const [maxDataSize, setMaxDataSize] = useState(0);
    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);


    useEffect(() => {
        // Fetch station data from the API
        fetch(`http://localhost:20001/api/countries`)
            .then(response => response.json())
            .then(data => {
                // Update the data state variable with the retrieved data
                setData(data.filter((item, index) => Math.floor(index / PAGE_SIZE) + 1 === page));
                // Update the max data size state variable with the total number of stations returned by the API
                setMaxDataSize(data.length);
            });
    }, [page]);


    if (!data) {
        return <CircularProgress />;
    }

    return (
        <>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>ID</TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>Geometry</TableCell>
                            <TableCell>Created On</TableCell>
                            <TableCell>Updated On</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {data.map(country => (
                            <TableRow key={country[0]}>
                                <TableCell>{country[0]}</TableCell>
                                <TableCell>{country[1]}</TableCell>
                                <TableCell>{country[2]}</TableCell>
                                <TableCell>{country[3]}</TableCell>
                                <TableCell>{country[4]}</TableCell>
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

export default Countries;