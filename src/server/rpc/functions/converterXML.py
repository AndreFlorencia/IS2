import csv
import requests
import time

def latitudeLongitude(s: str):
    response = requests.get(
        'https://nominatim.openstreetmap.org/search?',
        params={'q': s,
                'format': 'json'},
    )
    time.sleep(1)

    api=response.json()

    return api
def convert_row(row):

    try:
        api=latitudeLongitude(row[1])
        return """    \n\t<Estacao id="%i">
        <Nome>%s</Nome>
        <Cidade>%s</Cidade>
        <Pais>%s</Pais>
        <Siglas>
            <IATA>%s</IATA>
            <ICAO>%s</ICAO>
        </Siglas>
        <Api>    
            <LatGraus>%f</LatGraus>
            <LongGraus>%f</LongGraus>
            <class>%s</class>
            <tipo>%s</tipo>
        </Api>
        <AltitudePes>%f</AltitudePes>
        <Horario>
            <DiferencaUTC>%f</DiferencaUTC>
            <HorarioVerao>%s</HorarioVerao>
            <FusoHorario>%s</FusoHorario>
        </Horario>
        <Fonte>%s</Fonte>
    </Estacao>""" % (
        int(row[0]), row[1], row[2], row[3], row[4], row[5], float(api[0]['lat']), float(api[0]['lon']), api[0]['class'],api[0]['type'],float(row[8]), float(row[9]), row[10], row[11], row[13])
    except (Exception) as error:
        print("Failed to fetch data for ",  row[1])
        return ""


def converterXML(path: str):
    f = open(path)
    csv_f = csv.reader(f)
    data = []

    for row in csv_f:
        data.append(row)
    f.close()

    xml = ''.join([convert_row(row) for row in data[10:20]])
    xml = "<Catalog>"+xml+"\n</Catalog>"
    return xml
