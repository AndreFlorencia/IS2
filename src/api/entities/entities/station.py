import uuid
from datetime import datetime


class Station:
    def __init__(self, id_: str, name: str, class_: str, country_id: str, horario_id: str, iata: str, icao: str, pes: float, fonte: str, created_on: str, updated_on: str):
        self.id = id_
        self.name = name
        self.class_ = class_
        self.country_id = country_id
        self.horario_id = horario_id
        self.iata = iata
        self.icao = icao
        self.pes = pes
        self.fonte = fonte
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()
