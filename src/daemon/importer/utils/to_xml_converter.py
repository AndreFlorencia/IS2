import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from utils.reader import CSVReader
from entities.country import Country
from entities.horario import Horario
from entities.Station import Station


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):
        # read countries
        countries = self._reader.read_entities(
            attr="Country",
            builder=lambda row: Country(row["Country"])
        )

        # read teams

        horarios = self._reader.read_entities(
            attr="fusohorario",
            builder=lambda row: Horario(
                fusoHorario=row["fusohorario"],
                diferencaUTC=row["diferencautc"],
                horarioVerao=row["dst"]
            )
        )

        stations = self._reader.read_entities(
            attr="Estacao",
            builder=lambda row: Station(
                name=row["Estacao"],
                classe=row["tipo"],
                country=countries[row["Country"]],
                horario=horarios[row["fusohorario"]],
                cidade=row["Cidade"],
                iata=row["IATA"],
                icao=row["ICAO"],
                pes=row["Pes"],
                fonte=row["fonte"],
            )
        )

        # generate the final xml
        root_el = ET.Element("Stations")

        for station in stations.values():
            root_el.append(station.to_xml())

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(
            self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()
