# ThreadScraping

Script para hacer web scraping en threads. 
El script original es de https://scrapfly.io/blog/how-to-scrape-threads/

## Usos

### Scraping a un perfil de threads
Obtiene todos los threads de un usuario dado.
Ej. Usuario: discoverocean
```
py ./profilethread.py discoverocean
```
### Scraping a un post de threads

Ej. Post: https://www.threads.net/t/CuVdfsNtmvh/
```
py ./scrapethread.py https://www.threads.net/t/CuVdfsNtmvh/
```
### Limpieza de datos

Luego de hacer scraping a un perfil necesitamos que los datos que no vayamos a utilizar desaparezcan. En este caso en específico, queremos las columnas:
|Texto|Fecha|Concepto|Género|Grupo Etáreo|Nombre Usuario|Escolaridad|Fuente|
|-|-|-|-|-|-|-|-|-|-|

Para ello utilizaremos el script dataset.py
Ej. json_file: discoverocean.json
```
py ./dataset.py discoverocean.json
```