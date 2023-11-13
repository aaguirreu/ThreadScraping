import pandas as pd
import json
import os
import sys

# Funciones para obtener concepto, género, grupo etáreo y escolaridad
def obtener_concepto(texto):
    # Implementa la lógica para obtener el concepto
    return False

def obtener_genero_grupo_etareo(username):
    # Implementa la lógica para obtener el género y grupo etáreo
    return "N/A", "N/A"

def obtener_escolaridad(username):
    # Implementa la lógica para obtener la escolaridad
    return "N/A"

def procesar_archivo_json(input_file):
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"El archivo '{input_file}' no se encontró.")
        return
    except json.JSONDecodeError as e:
        print(f"Error al cargar el archivo JSON: {e}")
        return

    output_data = []

    for item in data["threads"]:
        thread = item["thread"]
        replies = item["replies"]

        concepto = obtener_concepto(thread["text"])
        genero, grupo_etareo = obtener_genero_grupo_etareo(thread["username"])
        escolaridad = obtener_escolaridad(thread["username"])

        output_data.append({
            "Texto": thread["text"],
            "Fecha": pd.to_datetime(thread["published_on"], unit="s"),
            "Concepto": concepto,
            "Género": genero,
            "Grupo Etáreo": grupo_etareo,
            "Nombre Usuario": thread["username"],
            "Escolaridad": escolaridad,
            "Fuente": thread["url"]
        })

        for reply in replies:
            concepto = obtener_concepto(reply["text"])
            genero, grupo_etareo = obtener_genero_grupo_etareo(reply["username"])
            escolaridad = obtener_escolaridad(reply["username"])

            output_data.append({
                "Texto": reply["text"],
                "Fecha": pd.to_datetime(reply["published_on"], unit="s"),
                "Concepto": concepto,
                "Género": genero,
                "Grupo Etáreo": grupo_etareo,
                "Nombre Usuario": reply["username"],
                "Escolaridad": escolaridad,
                "Fuente": reply["url"]
            })

    return pd.DataFrame(data=output_data)

def main(path):
    # Directorio actual
    json_directory = os.path.abspath(path)

    # Lista de archivos JSON en el directorio actual
    json_files = [f for f in os.listdir(json_directory) if f.endswith('.json')]

    # Crear un DataFrame vacío
    combined_data = pd.DataFrame()

    for json_file in json_files:
        file_path = os.path.join(json_directory, json_file)
        df = procesar_archivo_json(file_path)
        combined_data = pd.concat([combined_data, df], ignore_index=True)

    # Guardar en un archivo CSV
    combined_data.to_csv('dataset.csv', index=False, encoding="utf-8")
    # Guardar en Excel
    combined_data.to_excel('dataset.xlsx', index=False, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py json_files_path")
    else:
        path = sys.argv[1]
        main(path)
