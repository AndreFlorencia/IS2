import sys
import time
import requests
import psycopg2

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

def updatedb(id,lat,lon):
    conn=psycopg2.connect(
        host='db-rel', database='is', user='is', password='is')
    cursor = conn.cursor()
    query = "UPDATE station SET geom = ST_SetSRID(ST_MakePoint(%s, %s), 4326) WHERE id = %s"
    data = (lat, lon, id)
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()

def get_geom(name):
  url = f"https://nominatim.openstreetmap.org/search?q={name}&format=json"
  response = requests.get(url)
  data = response.json()

  if not data:
      latitude = 0
      longitude = 0
      print(f"{name} not found")
  else:
     
      latitude = data[0]["lat"]
      longitude = data[0]["lon"]
      time.sleep(1)
      print(latitude,longitude)
  return latitude,longitude

if __name__ == "__main__":
    


    while True:
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        # !TODO: 1- Use api-gis to retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)

        response = requests.get("http://api-gis:8080/api/markers")
        # !TODO: 2- Use the entity information to retrieve coordinates from an external API
        data = response.json()
        for i in range(20):
            latitude,longitude=get_geom(data['data'][i][1])
         # !TODO: 3- Submit the changes

            updatedb(data['data'][i][0],latitude,longitude)
        
        time.sleep(POLLING_FREQ)
