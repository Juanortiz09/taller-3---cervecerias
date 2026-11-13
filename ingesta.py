import os
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

# 1. Configuración de conexión a MongoDB Atlas
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://<usuario>:<password>@cluster0.agikcu9.mongodb.net/?retryWrites=true&w=majority"
)
DB_NAME = "cervecerias_db"
COLLECTION_NAME = "cervecerias"

# 2. URL de la API pública Open Brewery DB
API_URL = "https://api.openbrewerydb.org/v1/breweries"


def extraer_datos_api(total_paginas=5, por_pagina=200):
    """Extrae registros paginados de la API de Open Brewery DB."""
    todas_las_cervecerias = []
    print("Iniciando extracción desde Open Brewery DB...")

    for pagina in range(1, total_paginas + 1):
        params = {"page": pagina, "per_page": por_pagina}
        try:
            respuesta = requests.get(API_URL, params=params, timeout=15)
            respuesta.raise_for_status()
            datos = respuesta.json()

            if not datos:
                break

            todas_las_cervecerias.extend(datos)
            print(f"Página {pagina}: {len(datos)} registros descargados.")
        except requests.exceptions.RequestException as e:
            print(f"Error al consultar la página {pagina}: {e}")
            break

    print(f"Total de registros extraídos: {len(todas_las_cervecerias)}")
    return todas_las_cervecerias


def cargar_en_mongodb(datos):
    """Inserta los documentos extraídos en MongoDB."""
    if not datos:
        print("No hay datos para insertar.")
        return

    cliente = None
    try:
        cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
        cliente.admin.command("ping")
        print("Conexión exitosa a MongoDB Atlas.")

        db = cliente[DB_NAME]
        coleccion = db[COLLECTION_NAME]

        # Limpiar colección previa si se vuelve a ejecutar el script
        coleccion.delete_many({})

        resultado = coleccion.insert_many(datos)
        print(f"Se insertaron {len(resultado.inserted_ids)} documentos en '{DB_NAME}.{COLLECTION_NAME}'.")

        total_en_db = coleccion.count_documents({})
        print(f"Total de documentos verificados en MongoDB: {total_en_db}")

    except ConnectionFailure:
        print("Error: No se pudo conectar a MongoDB. Revisa tu contraseña en MONGO_URI y el acceso IP (0.0.0.0/0).")
    except PyMongoError as e:
        print(f"Error de MongoDB al insertar datos: {e}")
    finally:
        if cliente:
            cliente.close()


if __name__ == "__main__":
    cervecerias = extraer_datos_api(total_paginas=5, por_pagina=200)
    cargar_en_mongodb(cervecerias)