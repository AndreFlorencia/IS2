

class Horario:
    def __init__(self, id_: str, fusohorario: str, diferencaUTC: int, horarioVerao: str, created_on: str, updated_on: str):
        self.id = id_
        self.fusohorario = fusohorario
        self.diferencaUTC = diferencaUTC
        self.horarioVerao = horarioVerao
        self.created_on = created_on
        self.updated_on = updated_on
