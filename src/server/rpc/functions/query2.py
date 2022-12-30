import psycopg2


def query2(ficheiro,nome):
    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="localhost",
                                      port="5432",
                                      database="is")
        if(ficheiro==2):
            cursor = connection.cursor()
            cursor.execute("SELECT unnest(xpath('/Catalog/Estacao[AltitudePes=//Estacao/AltitudePes [not(.<//Estacao/AltitudePes)]]/Cidade/text()',xml)),file_name from imported_documents")


            result = cursor.fetchall()
            return result
        else:
            cursor = connection.cursor()

            postgres_insert_query = """SELECT unnest(xpath('/Catalog/Estacao[AltitudePes=//Estacao/AltitudePes [not(.<//Estacao/AltitudePes)]]/Cidade/text()',xml)) from imported_documents where %s=file_name"""
            cursor.execute(postgres_insert_query, (nome,))

            result = cursor.fetchall()
            return result





    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:

        if connection:
            cursor.close()
            connection.close()