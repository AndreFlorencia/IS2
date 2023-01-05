import Stations from "../Procedures/Stations";
import MaiorPes from "../Procedures/MaiorPes";
import OrdenarPais from "../Procedures/OrdernarPais"
import SelectPais from "../Procedures/SelectPais"


const Sections = [

    {
        id: "stations",
        label: "Stations",
        content: <Stations />
    },

    {
        id: "maior-pes",
        label: "Estacão Mais Elevada",
        content: <MaiorPes />
    },
    {
        id: "numero-pais",
        label: "Número De Estações Por País",
        content: <OrdenarPais />
    },
    {
        id: "select-pais",
        label: "Estações Por Pais",
        content: <SelectPais />
    }

];

export default Sections;