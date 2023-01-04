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

function getDST(character) {
    switch (character) {
        case "E":
            return "Europe";
        case "A":
            return "US/Canada";
        case "S":
            return "South America";
        case "O":
            return "Australia";
        case "Z":
            return "New Zealand";
        case "N":
            return "None";
        case "U":
            return "Unknown";
        default:
            return "";
    }
}

function FusoHorario() {

    const [maxDataSize, setMaxDataSize] = useState(0);
    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);


    useEffect(() => {
        // Fetch station data from the API
        fetch(`http://localhost:20001/api/horarios`)
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
                            <TableCell>Hour Offset</TableCell>
                            <TableCell>Horário de Verâo</TableCell>
                            <TableCell>Created On</TableCell>
                            <TableCell>Updated On</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {data.map(timezone => (
                            <TableRow key={timezone[0]}>
                                <TableCell>{timezone[0]}</TableCell>
                                <TableCell>{timezone[1]}</TableCell>
                                <TableCell>{timezone[2]}</TableCell>
                                <TableCell>{getDST(timezone[3])}</TableCell>
                                <TableCell>{timezone[4]}</TableCell>
                                <TableCell>{timezone[5]}</TableCell>
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

export default FusoHorario;