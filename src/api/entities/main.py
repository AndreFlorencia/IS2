import sys

from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

from entities import Country, Horario, Station

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

def execute_query(query: str, params: tuple) -> int:
    conn = psycopg2.connect(host='db-rel', database='is',
                            user='is', password='is')
    cur = conn.cursor()

    cur.execute(query, params)
    conn.commit()

    affected_rows = cur.rowcount

    cur.close()
    conn.close()

    return affected_rows

def select_query(query: str, params: tuple) -> list:
    conn = psycopg2.connect(host='db-rel', database='is',
                            user='is', password='is')
    cur = conn.cursor()

    cur.execute(query, params)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows





@app.route('/')
def home():

    return "hello world"


@app.route('/api/countries/', methods=['GET'])
def get_countries():
    rows = select_query("SELECT * FROM country", ())
    return jsonify(rows)

@app.route('/api/countries/<country_id>', methods=['GET'])
def get_country(country_id):
    rows = select_query("SELECT * FROM country where id =%s", (country_id,))
    return jsonify(rows)

@app.route('/api/stations', methods=['GET'])
def get_stations():
    query = "SELECT * FROM station"
    rows = select_query(query, ())
    return jsonify(rows)

@app.route('/api/stations/<station_id>', methods=['GET'])
def get_station(station_id):
    rows = select_query("SELECT * FROM station WHERE id = %s", (station_id,))
    return jsonify(rows)

@app.route('/api/horarios', methods=['GET'])
def get_horarios():
    query = "SELECT * FROM horario"
    rows = select_query(query, ())
    return jsonify(rows)

@app.route('/api/horarios/<horario_id>', methods=['GET'])
def get_horario(horario_id):
    rows = select_query("SELECT * FROM horario WHERE id = %s", (horario_id,))
    return jsonify(rows)

@app.route('/api/stations/<station_id>/country', methods=['GET'])
def get_station_country(station_id):
    query = """
        SELECT c.*
        FROM station s
        JOIN country c ON s.country_id = c.id
        WHERE s.id = %s
    """
    rows = select_query(query, (station_id,))
    return jsonify(rows)

@app.route('/api/stations/<station_id>/horario', methods=['GET'])
def get_station_horario(station_id):
    query = """
        SELECT h.*
        FROM station s
        JOIN horario h ON s.horario_id = h.id
        WHERE s.id = %s
    """
    rows = select_query(query, (station_id,))
    return jsonify(rows)


@app.route('/api/stations', methods=['POST'])
def create_station():
    # Get the request data
    data = request.get_json()

    # Extract the values from the request data
    name = data.get('name')
    class_ = data.get('class')
    country_id = data.get('country_id')
    horario_id = data.get('horario_id')
    iata = data.get('iata')
    icao = data.get('icao')
    pes = data.get('pes')
    fonte = data.get('fonte')

    # Insert the new row into the station table
    query = """
        INSERT INTO station (name, class, country_id, horario_id, iata, icao, pes, fonte)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    result = execute_query(query, (name, class_, country_id, horario_id, iata, icao, pes, fonte))

    if result == 1:
        return jsonify({'message': 'Station created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create station'}), 500
    # Return a success message

@app.route('/api/countries', methods=['POST'])
def create_country():
    # Get the request data
    data = request.get_json()

    # Extract the values from the request data
    nome = data.get('nome')

    # Insert the new row into the table
    query = "INSERT INTO country (nome) VALUES (%s)"
    result = execute_query(query, (nome,))

    # Return a success message or an error if the query failed
    if result == 1:
        return jsonify({'message': 'Country created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create country'}), 500   

@app.route('/api/horarios', methods=['POST'])
def create_horario():
    # Get the request data
    data = request.get_json()

    # Extract the values from the request data
    fusohorario = data.get('fusohorario')
    diferencaUTC = data.get('diferencaUTC')
    horarioVerao = data.get('horarioVerao')

    # Insert the new row into the table
    query = """
        INSERT INTO horario (fusohorario, diferencaUTC, horarioVerao)
        VALUES (%s, %s, %s)
    """
    result = execute_query(query, (fusohorario, diferencaUTC, horarioVerao))

    # Return a success message or an error if the query failed
    if result == 1:
        return jsonify({'message': 'Horario created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create horario'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
