import os
import openai
import sys
import json
import requests
import time
import re
import emoji
import pandas as pd
# import spacy
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

openai.api_key = os.getenv("OPENAI_API_KEY")

sentimientos_permitidos = [
        "abandono", "abatimiento", "abrumamiento", "aburrimiento", "abuso", "aceptación",
        "acompañamiento", "admiración", "adoración", "afectación", "afecto", "aflicción",
        "agobio", "agradecimiento", "agravio", "agresión", "alarma", "alborozo", "alegría",
        "alivio", "alteración", "amabilidad", "amargura", "ambivalencia", "amor", "angustia",
        "anhelo", "ansiedad", "añoranza", "apatía", "apego", "apoyo", "aprobación", "armonía",
        "arrepentimiento", "arrogancia", "arrojo", "asco", "asombro", "atracción", "ausencia",
        "autonomía", "aversión", "benevolencia", "bondad", "calma", "cansancio", "cariño",
        "celos", "censura", "cercanía", "cólera", "compasión", "competencia", "comprensión",
        "compromiso", "concentración", "condescendencia", "confianza", "confusión", "congoja",
        "consideración", "consuelo", "contento", "contrariedad", "correspondencia", "cuidado",
        "culpa", "curiosidad", "decepción", "dependencia", "depresión", "derrota", "desaliento",
        "desamor", "desamparo", "desánimo", "desasosiego", "desconcierto", "desconfianza",
        "desconsideración", "desconsuelo", "desdén", "desdicha", "desencanto", "deseo",
        "desesperación", "desgano", "desidia", "desilusión", "desmotivación", "desolación",
        "desorientación", "desprecio", "desprestigio", "desprotección", "destrucción",
        "desvalimiento", "desventura", "devaluación", "dicha", "dignidad", "disforia",
        "disgusto", "diversión", "dolor", "dominación", "duda", "duelo", "ecuanimidad",
        "embelesamiento", "emoción", "empatía", "enamoramiento", "encanto", "enfado",
        "engaño", "enjuiciamiento", "enojo", "enternecimiento", "entusiasmo", "envidia",
        "espanto", "esperanza", "estima", "estremecimiento", "estupor", "euforia",
        "exaltación", "exasperación", "excitación", "expectativa", "éxtasis", "extrañeza",
        "fastidio", "felicidad", "fervor", "firmeza", "fobia", "fortaleza", "fracaso",
        "fragilidad", "frenesí", "frustración", "furia", "generosidad", "gozo", "gratitud",
        "hastío", "herida", "honestidad", "honorabilidad", "horror", "hostilidad", "humildad",
        "humillación", "ilusión", "impaciencia", "imperturbabilidad", "impotencia", "impresión",
        "incapacidad", "incomodidad", "incompatibilidad", "incomprensión", "inconformidad",
        "incongruencia", "incredulidad", "indiferencia", "indignación", "inestabilidad",
        "infelicidad", "inferioridad", "injusticia", "inquietud", "insatisfacción", "inseguridad",
        "insuficiencia", "integridad", "interés", "intimidad", "intolerancia", "intranquilidad",
        "intrepidez", "intriga", "invasión", "ira", "irritación", "jocosidad", "júbilo", "justicia",
        "lamento", "lástima", "libertad", "logro", "lujuria", "manipulación", "melancolía",
        "menosprecio", "mezquindad", "miedo", "molestia", "motivación", "necesidad", "nerviosismo",
        "nostalgia", "obligación", "obnubilación", "obstinación", "odio", "omnipotencia",
        "opresión", "optimismo", "orgullo", "ostentación", "paciencia", "pánico", "parálisis",
        "pasión", "pavor", "paz", "pena", "pereza", "persecución", "pertenencia", "pesadumbre",
        "pesimismo", "placer", "plenitud", "preocupación", "prepotencia", "pudor", "rabia",
        "rebeldía", "recelo", "rechazo", "regocijo", "remordimiento", "rencor", "repudio",
        "resentimiento", "reserva", "resignación", "respeto", "resquemor", "revelarse", "romance",
        "satisfacción", "seguridad", "serenidad", "simpatía", "soledad", "solidaridad", "sometimiento",
        "sorpresa", "sosiego", "suficiencia", "sumisión", "susto", "temor", "templanza", "tentación",
        "ternura", "terquedad", "terror", "timidez", "tolerancia", "traición", "tranquilidad",
        "tristeza", "triunfo", "turbación", "unidad", "vacilación", "vacío", "valentía", "valoración",
        "venganza", "verguenza", "violencia", "vulnerabilidad"
]

conversation_history = []
url = 'https://dragonnext-unicorn-proxy.hf.space/proxy/openai/v1/chat/completions'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer lensThabieweegri'}

def openaiInit():
    try:
        # Texto que deseas enviar a ChatGPT
        input_text = "Por favor, de un texto dado responde con un solo sentimiento de una lista que te daré, es decir, tu respuesta debe ser solo UNA PALABRA. Puede ser cualquier sentimiento de la lista de emociones proporcionada. El texto son comentarios o posts de Threads, una red social.\nLista de emociones:\n"+str(sentimientos_permitidos)+"\nPor ejemplo, si el texto es 'Estoy muy feliz', tu respuesta debe ser 'alegría'.\nSi no sabes que responder, solo escribe 'No sé'."
        
        # Agrega el mensaje del usuario al historial de conversación
        conversation_history.append({"role": "user", "content": input_text})

        # Llamada a la API de OpenAI para obtener la respuesta
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=0,
            max_tokens=256
        )
        
        # Agrega la respuesta del asistente al historial de conversación
        conversation_history.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

        # Extraer el texto de la respuesta
        print("Inicialización exitosa")

    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
        match = re.search(r'Please try again in (\d+)m(\d+)s', str(e))
        if match :
            min = int(match.group(1))
            seg = int(match.group(2))
            print(f"Esperando {min}m{seg}s segundos")
            tiempo = min * 60 + seg
            time.sleep(int(tiempo)+1)
        else :
            tiempo = re.search(r'Please try again in (\d+)s', str(e)).group(1)
            print(f"Esperando {tiempo} segundos")
            time.sleep(int(tiempo)+1)

# nlp = spacy.load("es_core_news_sm")  # Carga el modelo en español (puedes utilizar otro idioma si es necesario)
# Arroja un error, arreglar.
# def coherente(texto):
#     doc = nlp(texto)
#     for sent in [doc.sents]:
#         # Verifica si hay al menos una oración coherente en el texto
#         if len(sent) >= 1:
#             return True
#     return False

# Función para obtener el sentimiento de un texto
def obtener_sentimiento(texto):
    try:
        global conversation_history  # Accede a la variable global conversation_history

        # Para evitar que el uso de tokens llegue al máximo, se elimina el historial de conversación
        if len(conversation_history) > 3:
            conversation_history.pop()
            conversation_history.pop()
        
        # Agrega el mensaje del usuario al historial de conversación
        conversation_history.append({"role": "user", "content": texto})
        

        # Llamada a la API de OpenAI para obtener la respuesta
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=0,
            max_tokens=256
        )
        
        # Extrae el texto de la respuesta del asistente
        respuesta_asistente = response['choices'][0]['message']['content'].lower()

        # Agrega la respuesta del asistente al historial de conversación
        conversation_history.append({"role": "assistant", "content": respuesta_asistente})

        return respuesta_asistente
        
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
        match = re.search(r'Please try again in (\d+)m(\d+)s', str(e))
        if match :
            min = int(match.group(1))
            seg = int(match.group(2))
            print(f"Esperando {min}m{seg}s segundos")
            tiempo = min * 60 + seg
            time.sleep(int(tiempo)+1)
        else :
            match = re.search(r'Please try again in (\d+)s', str(e))
            if match :
                tiempo = match.group(1)
                print(f"Esperando {tiempo} segundos")
                time.sleep(int(tiempo)+1)
            else :
                time.sleep(5)
                return False

def procesar_csv(nombre_archivo):
    try:
        # Lee el archivo CSV en un DataFrame
        df = pd.read_csv(nombre_archivo, sep=',')

        # Verifica si la columna 'Texto' existe en el DataFrame
        if 'Texto' not in df.columns:
            print("El archivo CSV no tiene una columna 'Texto'.")
            return
        
        # Itera a través de cada fila del DataFrame
        for index, row in df.iterrows():
            texto = row['Texto']
            # if not coherente(texto): return False
            print(f"Fila {index}...")
            sentimiento = row['Concepto']
            print(f"Texto: {texto}\nSentimiento: {sentimiento}")
            
            # Si ya existe un sentimiento en la columna 'Concepto', no lo cambies
            if (not (sentimiento == 'FALSO' or sentimiento is False or pd.isnull(sentimiento))): continue
            
            # Si el texto es 'None' o es solo emojies, no lo proceses
            #if (texto == '"None"' or bool(re.search(r'\b\w+\b', texto))): continue
            # Obtén el sentimiento del texto
            sentimiento = obtener_sentimiento(texto)
            print(f"Sentimiento asignado: {sentimiento}\n")
            
            # Agrega el sentimiento a la columna 'Concepto'
            df.at[index, 'Concepto'] = sentimiento

            # Guarda el DataFrame actualizado en un nuevo archivo CSV o sobrescribe el original
            df.to_csv(nombre_archivo, index=False)
            df.to_excel(f"{nombre_archivo.split('.csv')[0]}" + '.xlsx', index=False)

    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no se encontró.")

    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
        df.to_csv(nombre_archivo, encoding="utf-8", index=False)
        df.to_excel(f"{nombre_archivo.split('.csv')[0]}" + '.xlsx', index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py archivo_csv")
    else:
        input_file = sys.argv[1]
        openaiInit()
        procesar_csv(input_file)
