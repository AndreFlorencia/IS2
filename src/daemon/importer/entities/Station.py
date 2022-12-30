import xml.etree.ElementTree as ET

from entities.horario import Horario


class Station:

    def __init__(self, name, classe, country, cidade, iata, icao, pes, fonte, horario):
        Station.counter += 1
        self._id = Station.counter
        self._name = name
        self._classe = classe
        self._country = country
        self._cidade = cidade
        self._iata = iata
        self._icao = icao
        self._pes = pes
        self._fonte = fonte
        self._horario = horario

    def to_xml(self):
        station_el = ET.Element("Station")

        # add the id attribute
        station_el.set("id", str(self._id))

        # add the name attribute as a subelement
        name_el = ET.Element("name")
        name_el.text = self._name
        station_el.append(name_el)

        # add the class attribute as a subelement
        classe_el = ET.Element("class")
        classe_el.text = self._classe
        station_el.append(classe_el)

        country_el = ET.Element("country")

        country_el.set("id", str(self._country._id))

        # add the name attribute to the country element
        country_name_el = ET.Element("name")
        country_name_el.text = self._country._name
        country_el.append(country_name_el)

        # append the country element to the station element
        station_el.append(country_el)
        horario_el = ET.Element("Horario")

        # add the id attribute
        horario_el.set("id", str(self._id))

        # add the fusohorario attribute as a subelement
        fusohorario_el = ET.Element("fusohorario")
        fusohorario_el.text = self._horario._fusoHorario
        horario_el.append(fusohorario_el)

        # add the diferencaUTC attribute as a subelement
        diferencaUTC_el = ET.Element("diferencaUTC")
        diferencaUTC_el.text = str(self._horario._diferençaUTC)
        horario_el.append(diferencaUTC_el)

        # add the horarioVerao attribute as a subelement
        horarioVerao_el = ET.Element("horarioVerao")
        horarioVerao_el.text = self._horario._horarioVerao
        horario_el.append(horarioVerao_el)

        station_el.append(horario_el)

        # add the iata attribute as a subelement
        iata_el = ET.Element("iata")
        iata_el.text = self._iata
        station_el.append(iata_el)

        # add the icao attribute as a subelement
        icao_el = ET.Element("icao")
        icao_el.text = self._icao
        station_el.append(icao_el)

        pes_el = ET.Element("pes")
        pes_el.text = self._pes
        station_el.append(pes_el)

        # add the fonte attribute as a subelement
        fonte_el = ET.Element("fonte")
        fonte_el.text = self._fonte
        station_el.append(fonte_el)

        return station_el

    def __str__(self):
        return f"{self._name} ({self._id})"


Station.counter = 0
