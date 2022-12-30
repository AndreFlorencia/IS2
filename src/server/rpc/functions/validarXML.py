import os
import xmlschema

def validarXML(xml_path: str, xsd_path: str) -> bool:


    schema = xmlschema.XMLSchema(xsd_path)
    validation_error_iterator = schema.iter_errors(xml_path)
    for idx, validation_error in enumerate(validation_error_iterator, start=1):
        print(f'[{idx}] path: {validation_error.path} | reason: {validation_error.reason}')

    resultado = schema.is_valid(xml_path)
    return resultado