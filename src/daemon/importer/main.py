import asyncio
import time
import uuid
import psycopg2
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from utils.to_xml_converter import CSVtoXMLConverter


def add_xmlDocument(xml_path):

    try:
        with open(xml_path, "r") as f:
            xml = f.read()
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="host.docker.internal",
                                      port=10001,
                                      database="is")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO imported_documents (file_name, xml) VALUES (%s, %s)", (xml_path, xml))
        connection.commit()
        print(f"Inserido ficheiro'{xml_path}' ")
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert data", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def add_convertedDocument(src, dst):
    file_size = os.stat(src).st_size

    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="host.docker.internal",
                                      port=10001,
                                      database="is")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO converted_documents (src, file_size, dst) VALUES (%s, %s, %s)", (src, file_size, dst))
        connection.commit()
        print(f"Inserido ficheiro'{src}' ")
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert data", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']


def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"


def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    file = open(out_path, "w")
    file.write(converter.to_xml_str())


class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in await self.get_converted_files():
            print(f"Este ficheiro: '{csv_path}' já se encontra convertido")
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate a unique file name for the XML file
        xml_path = generate_unique_file_name(self._output_path)

        # we do the conversion

        convert_csv_to_xml(csv_path, xml_path)
        print(csv_path, xml_path)
        # !TODO: once the conversion is done, we should updated the converted_documents tables
        add_convertedDocument(csv_path, xml_path)
        print(f"new xml file generated: '{xml_path}'")

        # !TODO: we should store the XML document into the imported_documents table
        add_xmlDocument(xml_path)

    async def get_converted_files(self):
        # !TODO: you should retrieve from the database the files that were already converted before

        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(user="is",
                                          password="is",
                                          host="host.docker.internal",
                                          port=10001,
                                          database="is")

            cursor = connection.cursor()
            cursor.execute("SELECT src FROM converted_documents ")
            convertidos = cursor.fetchall()
            res = [''.join(i) for i in convertidos]
            return res
        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/shared/output"

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
