import psycopg2
def importarFicheiro(data,nome):


    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="localhost",
                                      port="5432",
                                      database="is")

        cursor = connection.cursor()
        postgres_insert_query = """insert into imported_documents(file_name,xml,deleted) VALUES (%s,xmlparse(CONTENT %s),%s)"""
        record_to_insert = (nome, data,"n")
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into ficheiros table")



    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:

        if connection:

            cursor.close()
            connection.close()
