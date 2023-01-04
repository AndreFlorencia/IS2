import sys

import graphene
from flask_cors import CORS
from flask import Flask
from flask_graphql import GraphQLView
import uuid
from graphene.types.datetime import DateTime
import psycopg2

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

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
    country_id = graphene.Field(graphene.UUID, required=True)
    horario_id = graphene.Field(graphene.UUID, required=True)
    iata = graphene.Field(graphene.String)
    icao = graphene.Field(graphene.String)
    pes = graphene.Field(graphene.Float)
    fonte = graphene.Field(graphene.String)
    created_on = graphene.Field(DateTime, required=True)
    updated_on = graphene.Field(DateTime, required=True)

class Query(graphene.ObjectType):
    countries = graphene.List(CountryType)
    horarios = graphene.List(HorarioType)
    stations = graphene.List(StationType)

    def resolve_countries(self, info):
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='is',
            user='is',
            password='is'
        )
        cur = conn.cursor()

        # execute the query
        cur.execute("SELECT name FROM station")
        results = cur.fetchall()

        # close the cursor and connection
        cur.close()
        conn.close()

        return [result[0] for result in results]

    # def resolve_horarios(self, info):
    #     # fetch horarios from database
    #     return horarios

    # def resolve_stations(self, info):
    #     # fetch stations from database
    #     return stations
schema = graphene.Schema(query=Query)

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    app.config["DEBUG"] = True
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    app.run(host="0.0.0.0", port=PORT)
