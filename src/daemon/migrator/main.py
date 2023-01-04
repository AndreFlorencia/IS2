import datetime
import sys
import time

import psycopg2
from psycopg2 import OperationalError

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 30


def migrated(db_org):
    cur = db_org.cursor()
    cur.execute(
        "UPDATE imported_documents SET migrated = 'y' WHERE migrated = 'n'")
    db_org.commit()
    cur.close()
    return


def print_horario(db_dst):
    cur = db_dst.cursor()
    cur.execute("SELECT * FROM horario")
    rows = cur.fetchall()
    headers = [desc[0] for desc in cur.description]
    for row in rows:
        print(row)
    cur.close()


def insert_station(db_dst, stations):
    cur = db_dst.cursor()
    for row in stations:
        name, class_, country_name, fusohorario, diferencaUTC, horarioVerao, iata, icao, pes, fonte = row
        try:
            cur.execute("INSERT INTO station (id, name, class, country_id, horario_id, iata, icao, pes, fonte, created_on, updated_on) "
                        "VALUES (uuid_generate_v4(), %s, %s, "
                        "(SELECT id FROM country WHERE nome = %s), "
                        "(SELECT id FROM horario WHERE fusohorario = %s AND diferencaUTC = %s AND horarioVerao = %s), "
                        "%s, %s, %s, %s, NOW(), NOW()) ON CONFLICT DO NOTHING",
                        (name, class_, country_name, fusohorario, diferencaUTC, horarioVerao, iata, icao, pes, fonte))
            db_dst.commit()
        except Exception as e:
            print("Error comitting changes:", e)
    rows_inserted = cur.rowcount
    print("Estacoes inseridas: ", rows_inserted)
    cur.close()


def insert_countries(db_dst, countries):
    cur = db_dst.cursor()
    for country in countries:
        try:
            cur.execute("INSERT INTO country (id, nome, created_on) "
                        "VALUES (uuid_generate_v4(), %s, NOW()) ON CONFLICT DO NOTHING", (country,))
            db_dst.commit()

        except Exception as e:
            print("Error comitting changes:", e, country)
    rows_inserted = cur.rowcount
    print("Paises inseridos: ", rows_inserted)
    cur.close()


def insert_horario(db_dst, horarios):

    cur = db_dst.cursor()
    for horario in horarios:
        try:

            cur.executemany(
                "INSERT INTO horario(id, fusohorario, diferencaUTC, horarioVerao) VALUES(uuid_generate_v4(), %s, %s, %s) ON CONFLICT DO NOTHING", horarios)
            db_dst.commit()

        except Exception as e:
            print("Error comitting changes:", e, horario)
    rows_inserted = cur.rowcount
    print("Horarios inseridos: ", rows_inserted)
    cur.close()


def select_station(db_org):

    stations = []
    cur = db_org.cursor()
    cur.execute(
        "SELECT DISTINCT unnest(xpath('//Station/name/text()', xml))::text, "
        "unnest(xpath('//Station/class/text()', xml))::text, "
        "unnest(xpath('//Station/country/name/text()', xml))::text, "
        "unnest(xpath('//Station/Horario/fusohorario/text()', xml))::text, "
        "unnest(xpath('//Station/Horario/diferencaUTC/text()', xml))::text, "
        "unnest(xpath('//Station/Horario/horarioVerao/text()', xml))::text, "
        "unnest(xpath('//Station/iata/text()', xml))::text, "
        "unnest(xpath('//Station/icao/text()', xml))::text, "
        "unnest(xpath('//Station/pes/text()', xml))::text, "
        "unnest(xpath('//Station/fonte/text()', xml))::text "
        "FROM imported_documents Where migrated = 'n'")

    rows = cur.fetchall()
    for row in rows:
        stations.append(row)
    cur.close()
    return stations


def select_horario(db_org):

    horario = []
    cur = db_org.cursor()
    cur.execute(
        "SELECT DISTINCT unnest(xpath('//Station/Horario/fusohorario/text()', xml))::text, "
        "unnest(xpath('//Station/Horario/diferencaUTC/text()', xml))::text, "
        "unnest(xpath('//Station/Horario/horarioVerao/text()', xml))::text "
        "FROM imported_documents Where migrated = 'n'")

    # Fetch the rows and print the country names
    rows = cur.fetchall()
    for row in rows:
        horario.append(row)
    # Close the cursor and connection
    cur.close()
    return horario


def select_country(db_org):

    countries = []
    cur = db_org.cursor()
    cur.execute(
        "SELECT DISTINCT unnest(xpath('//Station/country/name/text()', xml))::text FROM imported_documents Where migrated = 'n'")

    # Fetch the rows and print the country names
    rows = cur.fetchall()
    for row in rows:
        countries.append(row[0])
    # Close the cursor and connection
    cur.close()
    return countries


def last_update(db_org):
    changed = []
    # Create a cursor
    cursor = db_org.cursor()

    # Define the query
    cursor.execute(
        "SELECT id, updated_on FROM imported_documents")
    results = cursor.fetchall()

    changed = [(result[0], result[1]) for result in results]

    cursor.close()

    return changed


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


if __name__ == "__main__":
    time.sleep(2)
    db_org = psycopg2.connect(
        host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(
        host='db-rel', database='is', user='is', password='is')

    original = last_update(db_org)

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(
                 host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(
                host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        print("Checking updates...")
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        # !TODO: 3- Execute INSERT queries in the destination db
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        countries = select_country(db_org)
        horario = select_horario(db_org)
        station = select_station(db_org)

        # current_changed = last_update(db_org)
        # if len(current_changed) > len(original):
        #    original.extend(current_changed[len(original):])
#
        # for i, (id, date) in enumerate(current_changed):
#
        #    if date != original[i][1]:
        #        print("Record with ID {} has been updated")
        #        # Update the original list with the current date
        #        original[i] = (id, date)
        if (countries):
            insert_countries(db_dst, countries)
        if (horario):
            insert_horario(db_dst, horario)
        if (station):
            insert_station(db_dst, station)
        

        migrated(db_org)
        db_org.close()

        db_dst.close()

        time.sleep(POLLING_FREQ)
