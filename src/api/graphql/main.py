import sys

import graphene
from flask_cors import CORS
from flask import Flask
from flask_graphql import GraphQLView
import uuid
from graphene.types.datetime import DateTime
import psycopg2

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

class CountryWithStationsType(graphene.ObjectType):
    name = graphene.Field(graphene.String, required=True)
    stationCount = graphene.Field(graphene.Int, required=True)

class CountryType(graphene.ObjectType):
    id = graphene.Field(graphene.UUID, required=True)
    name = graphene.Field(graphene.String, required=True)
    created_on = graphene.Field(DateTime, required=True)
    updated_on = graphene.Field(DateTime, required=True)

class HorarioType(graphene.ObjectType):
    id = graphene.Field(graphene.UUID, required=True)
    fuso_horario = graphene.Field(graphene.String, required=True)
    diferenca_utc = graphene.Field(graphene.Float, required=True)
    horario_verao = graphene.Field(graphene.String)
    created_on = graphene.Field(DateTime, required=True)
    updated_on = graphene.Field(DateTime, required=True)

class StationType(graphene.ObjectType):
    id = graphene.Field(graphene.UUID, required=True)
    name = graphene.Field(graphene.String, required=True)
    class_ = graphene.Field(graphene.String)
    countryId = graphene.Field(graphene.UUID, required=True)
    horarioId = graphene.Field(graphene.UUID, required=True)
    iata = graphene.Field(graphene.String)
    icao = graphene.Field(graphene.String)
    pes = graphene.Field(graphene.Float)
    fonte = graphene.Field(graphene.String)
    createdOn = graphene.Field(DateTime, required=True)
    updatedOn = graphene.Field(DateTime, required=True)

class Query(graphene.ObjectType):
   
    countries = graphene.List(CountryType)
    stations = graphene.List(StationType)
    maiorPes = graphene.Field(StationType)
    stationCountByCountry = graphene.List(CountryWithStationsType)
    stationsInCountry = graphene.List(StationType, countryName=graphene.String(required=True))

    def resolve_countries(self, info):
     conn = psycopg2.connect(
            host='db-rel', database='is', user='is', password='is'
        )
     cur = conn.cursor()

     cur.execute('SELECT id,nome,created_on,updated_on FROM country')
     rows = cur.fetchall()

     countries = []
     for row in rows:
        countries.append(CountryType(id=row[0], name=row[1], created_on=row[2], updated_on=row[3]))

     return countries


    def resolve_maiorPes(self, info):
        conn = psycopg2.connect(
            host='db-rel', database='is',
                            user='is', password='is'
        )
        cur = conn.cursor()

        cur.execute('SELECT id,name,class,country_id,horario_id,iata,icao,pes,fonte,created_on,updated_on FROM station ORDER BY pes DESC LIMIT 1')
        row = cur.fetchone()

        return StationType(id=row[0], name=row[1], class_=row[2], countryId=row[3], horarioId=row[4], iata=row[5], icao=row[6], pes=row[7], fonte=row[8], createdOn=row[9], updatedOn=row[10])

    def resolve_stations(self, info):
        conn = psycopg2.connect(
            host='db-rel', database='is',
                            user='is', password='is'
        )
        cur = conn.cursor()

        cur.execute('SELECT id,name,class,country_id,horario_id,iata,icao,pes,fonte,created_on,updated_on FROM station')
        rows = cur.fetchall()

        # Create a list of StationType objects
        stations = []
        for row in rows:
            stations.append(StationType(id=row[0], name=row[1], class_=row[2], countryId=row[3], horarioId=row[4], iata=row[5], icao=row[6], pes=row[7], fonte=row[8], createdOn=row[9], updatedOn=row[10]))
        
        return stations

    def resolve_stationCountByCountry(self, info):
        conn = psycopg2.connect(
            host='db-rel', database='is',
                        user='is', password='is'
        )
        cur = conn.cursor()

        cur.execute('''
            SELECT c.nome, COUNT(s.id) as station_count
            FROM country c
            JOIN station s ON s.country_id = c.id
            GROUP BY c.nome
        ''')
        rows = cur.fetchall()
        countriesWithStations = []
        for row in rows:
            countriesWithStations.append(CountryWithStationsType(name=row[0], stationCount=row[1]))

        return countriesWithStations    

    def resolve_stationsInCountry(self, info, countryName):
        conn = psycopg2.connect(
            host='db-rel', database='is',
                        user='is', password='is'
        )
        cur = conn.cursor()
        cur.execute("SELECT station.id, name, class, country_id, horario_id, iata, icao, pes, fonte, station.created_on, station.updated_on FROM station INNER JOIN country ON station.country_id = country.id WHERE country.nome = %s", (countryName,))
        rows = cur.fetchall()
        # Create a list of StationType objects
        stations = []
        for row in rows:
            stations.append(StationType(id=row[0], name=row[1], class_=row[2], countryId=row[3], horarioId=row[4], iata=row[5], icao=row[6], pes=row[7], fonte=row[8], createdOn=row[9], updatedOn=row[10]))

        # Close the cursor and connection
        cur.close()
        conn.close()

        return stations

schema = graphene.Schema(query=Query)

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    app.config["DEBUG"] = True
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    app.run(host="0.0.0.0", port=PORT)
