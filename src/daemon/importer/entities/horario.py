import xml.etree.ElementTree as ET


class Horario:

    def __init__(self, fusoHorario, diferencaUTC, horarioVerao):
        Horario.counter += 1
        self._id = Horario.counter
        self._fusoHorario = fusoHorario
        self._diferençaUTC = diferencaUTC
        self._horarioVerao = horarioVerao

    def to_xml(self):
        el = ET.Element("Estacao")
        el.set("id", str(self._id))
        el.set("fusohorario", self._fusoHorario)
        el.set("diferençaUTC", self._diferençaUTC)
        el.set("horarioVerao", self._horarioVerao)
        return el

    def __str__(self):
        return f"{self._fusoHorario}, diferençaUTC:{self._diferençaUTC}, HorarioVerao:{self._horarioVerao}"


Horario.counter = 0
