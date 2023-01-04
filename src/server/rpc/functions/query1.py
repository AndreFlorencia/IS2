import psycopg2


def query1():
    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="localhost",
                                      port="5432",
                                      database="is")
        
        cursor = connection.cursor()
        cursor.execute("SELECT unnest(xpath('//Estacao/Nome/text()',xml)),file_name from imported_documents")
            

        result = cursor.fetchall()
        return result





    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:

        if connection:
            cursor.close()
            connection.close()