# ThreadScraping

Script para hacer web scraping en threads. 
El script original es de https://scrapfly.io/blog/how-to-scrape-threads/

## Usos

### Scraping a un perfil de threads

Obtiene todos los threads de un usuario dado.
Ej. Usuario: discoverocean
```
py .\profilethread.py discoverocean
```
### Scraping a un post de threads

Si solo queremos hacer scraping a un post en específico
Ej. Post: https://www.threads.net/t/CuVdfsNtmvh/
```
py .\scrapethread.py https://www.threads.net/t/CuVdfsNtmvh/
```
### Recopilación de datos

Luego de hacer scraping a un perfil o varios necesitamos que los datos que no vayamos a utilizar desaparezcan. En este caso en específico, queremos las columnas:
|Texto|Fecha|Concepto|Género|Grupo Etáreo|Nombre Usuario|Escolaridad|Fuente|
|-|-|-|-|-|-|-|-|

Para ello utilizaremos el script dataset.py
```
py .\dataset.py 
```

### Análisis de sentimientos con chatGPT

Copiar .env_example a .env
```
cp .\.env_example .\.env
```
Agregar una key de openai en OPENAI_API_KEY. Luego ejecutar el script.
```
py .\OpenAiSentiment.py dataset.csv
```