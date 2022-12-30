import sys

from flask import Flask, jsonify, request
import psycopg2

from entities import Country, Horario, Station

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000


def select_query(query: str, params: tuple) -> list:
    conn = psycopg2.connect(host='db-rel', database='is',
                            user='is', password='is')
    cur = conn.cursor()

    cur.execute(query, params)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def home():

    return "hello world"


@app.route('/api/countries/', methods=['GET'])
def get_countries():
    rows = select_query("SELECT * FROM country", ())
    return jsonify(rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
