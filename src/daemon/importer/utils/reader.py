from csv import DictReader


class CSVReader:
    countries = []

    def __init__(self, path, delimiter=','):
        self._path = path
        self._delimiter = delimiter

    def loop(self):
        with open(self._path, 'r') as file:
            for row in DictReader(file, delimiter=self._delimiter):
                yield row
        file.close()

    def read_entities(self, attr, builder, after_create=None):
        entities = {}
        entity_ids = {}

        id_counter = 0

        for row in self.loop():
            e = row[attr]
            if e not in entities:
                entity = builder(row)
                entity._id = id_counter
                entity_ids[e] = id_counter
                id_counter += 1
                entities[e] = entity
                after_create is not None and after_create(entity, row)

        if attr == "Country":
            self.countries = list(entities.values())

        return entities
