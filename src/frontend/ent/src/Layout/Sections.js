import Countries from "../Tables/Countries"
import FusoHorario from "../Tables/FusoHorario";
import Stations from "../Tables/Stations";

const Sections = [

    {
        id: "stations",
        label: "Stations",
        content: <Stations />
    },

    {
        id: "fusoHorario",
        label: "Fuso-Horario",
        content: <FusoHorario />
    },

    {
        id: "countries",
        label: "Countries",
        content: <Countries />
    }

];

export default Sections;