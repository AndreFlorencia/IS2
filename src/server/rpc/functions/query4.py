import psycopg2


def query4(ficheiro,nome):
    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="localhost",
                                      port="5432",
                                      database="is")
        if(ficheiro==2):
            cursor = connection.cursor()
            cursor.execute("SELECT file_name, unnest(xpath('/Catalog/Estacao/Cidade/text()', xml::xml))::TEXT AS Cidade FROM imported_documents ORDER BY Cidade DESC, file_name")

            result = cursor.fetchall()
            return result
        else:
            cursor = connection.cursor()

            postgres_insert_query = """SELECT file_name, unnest(xpath('/Catalog/Estacao/Cidade/text()', xml::xml))::TEXT AS Cidade FROM imported_documents where %s=file_name ORDER BY Cidade DESC, file_name"""
            cursor.execute(postgres_insert_query, (nome,))

            result = cursor.fetchall()
            return result





    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:

        if connection:
            cursor.close()
            connection.close()