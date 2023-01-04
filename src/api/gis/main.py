import sys
import json
from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

urls = {
    "airport": "https://cdn-icons-png.flaticon.com/512/1830/1830404.png",
    "station": "https://cdn-icons-png.flaticon.com/512/2062/2062107.png",
    "unknown": "https://cdn-icons-png.flaticon.com/512/4287/4287539.png",
}

@app.route('/api/markers', methods=['GET'])
def get_markers():
    
    conn = psycopg2.connect(
         host='db-rel', database='is', user='is', password='is'
    )

    # Select the rows where the geom field is empty
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM station WHERE geom IS NULL LIMIT 20")
    rows = cursor.fetchall()

    # Build the response object
    response = {
        "data": rows
    }

    # Return the response as a JSON object
    return jsonify(response)



@app.route('/api/tile/', methods=['GET'])
def get_tile():
    # Parse the parameters from the request
    neLat = request.args.get('neLat')
    neLng = request.args.get('neLng')
    swLat = request.args.get('swLat')
    swLng = request.args.get('swLng')

    # Connect to the database
    conn = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    # Use the ST_MakeEnvelope function to create a rectangle from the given coordinates
    envelope = "ST_MakeEnvelope(%s, %s, %s, %s)" % (swLng, swLat, neLng, neLat)

    # Select all entities within the rectangle
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, class, ST_AsGeoJSON(geom), country_id, horario_id, iata, icao, pes, fonte from station WHERE geom && %s" % envelope)
    rows = cursor.fetchall()

    # Build the GeoJSON object
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    print(rows)
    for row in rows:
        feature = {
        "type": "Feature",
        "properties": {
            "id": row[0],
            "name": row[1],
            "class": row[2],
            "country_id": row[4],
            "horario_id": row[5],
            "iata": row[6],
            "icao": row[7],
            "pes": row[8],
            "fonte": row[9],
            "imgUrl":urls.get(row[2])
        },
        "geometry": json.loads(row[3])
    }
        geojson["features"].append(feature)

    return jsonify(geojson)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
