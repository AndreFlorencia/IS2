CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

CREATE TABLE country (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  nome varchar(50) NOT NULL,
  created_on TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_on TIMESTAMP NOT NULL DEFAULT NOW()
  );

CREATE UNIQUE INDEX CONCURRENTLY index_nome 
ON country (nome);

ALTER TABLE country 
ADD CONSTRAINT nome_unique
UNIQUE USING INDEX index_nome;


CREATE TABLE horario (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  fusohorario text NOT NULL,
  diferencaUTC float,
  horarioVerao text,
  created_on TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_on TIMESTAMP NOT NULL DEFAULT NOW(),
  CONSTRAINT unique_horario_fusohorario UNIQUE (fusohorario)
);


CREATE TABLE station (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name text NOT NULL,
  class text,
  geom GEOMETRY,
  country_id uuid REFERENCES country (id),
  horario_id uuid REFERENCES horario (id),
  iata text,
  icao text,
  pes float,
  fonte text,
  created_on TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_on TIMESTAMP NOT NULL DEFAULT NOW(),
  CONSTRAINT unique_station_name UNIQUE (name)
);