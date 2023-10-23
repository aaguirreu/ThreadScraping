import pandas as pd
import sys
import json
import os
from datetime import datetime

# Función para obtener el concepto asociado (puedes personalizar esta función según tus necesidades)
def obtener_concepto(texto):
    # Aquí puedes implementar la lógica para obtener el concepto asociado
    return False

# Función para obtener el género y grupo etáreo (puedes personalizar esta función según tus necesidades)
def obtener_genero_grupo_etareo(username):
    # Aquí puedes implementar la lógica para obtener el género y grupo etáreo
    return False, False

# Función para obtener escolaridad (puedes personalizar esta función según tus necesidades)
def obtener_escolaridad(username):
    # Aquí puedes implementar la lógica para obtener la escolaridad
    return False

def main(input_file):
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"El archivo '{input_file}' no se encontró.")
        return
    except json.JSONDecodeError as e:
        print(f"Error al cargar el archivo JSON: {e}")
        return

    # Crear listas para los datos de salida
    output_data = []
    for item in data["threads"]:
        thread = item["thread"]
        replies = item["replies"]

        concepto = obtener_concepto(thread["text"])
        genero, grupo_etareo = obtener_genero_grupo_etareo(thread["username"])
        escolaridad = obtener_escolaridad(thread["username"])
        output_data.append({
            "Texto": thread["text"],
            "Fecha": datetime.utcfromtimestamp(thread["published_on"]).strftime('%Y-%m-%d %H:%M:%S'),
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
                "Fecha": datetime.utcfromtimestamp(reply["published_on"]).strftime('%Y-%m-%d %H:%M:%S'),
                "Concepto": concepto,
                "Género": genero,
                "Grupo Etáreo": grupo_etareo,
                "Nombre Usuario": reply["username"],
                "Escolaridad": escolaridad,
                "Fuente": reply["url"]
            })
    # Crear un DataFrame de Pandas
    df = pd.DataFrame(data=output_data)
    filename = os.path.splitext(os.path.basename(input_file))[0]

    # Guardar en CSV
    df.to_csv(filename + '.csv', index=False)
    # Guardar en Excel
    df.to_excel(filename + '.xlsx', index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py archivo_json")
    else:
        input_file = sys.argv[1]
        main(input_file)
