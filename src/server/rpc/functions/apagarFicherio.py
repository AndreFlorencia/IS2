import psycopg2


def apagar(nome):
    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="localhost",
                                      port="5432",
                                      database="is")

        cursor = connection.cursor()

        postgres_insert_query = """Update imported_documents set deleted=%s where %s=file_name"""
        cursor.execute(postgres_insert_query, ("s",nome))
        updated_rows = cursor.rowcount
        # Commit the changes to the database
        connection.commit()
        # Close communication with the PostgreSQL database
        return updated_rows

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:

        if connection:
            cursor.close()
            connection.close()

