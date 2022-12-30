import psycopg2
def listarXML():
    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="localhost",
                                      port="5432",
                                      database="is")

        cursor = connection.cursor()

        postgres_insert_query = """SELECT file_name,deleted from imported_documents where NOT deleted=%s """
        cursor.execute(postgres_insert_query,("s"))

        result = cursor.fetchall()
        return result


    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:

        if connection:
            cursor.close()
            connection.close()