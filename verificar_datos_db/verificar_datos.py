import json
import os
import sys

# Agrega el directorio padre al sys.path para permitir importaciones desde niveles superiores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define la ruta absoluta del archivo config_db.json
ruta_archivo = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'configuracion', 'config_db.json'))

# Función para cargar los datos de conexión a la base de datos desde el archivo JSON
def cargar_datos_db():
    try:
        # Abre el archivo JSON en modo lectura
        with open(ruta_archivo, 'r') as archivo:
            datos = json.load(archivo)  # Carga los datos en un diccionario
            return datos
    except Exception as e:
        # Si ocurre un error (por ejemplo, archivo no encontrado o mal formado), lo imprime
        print(f"Error al leer el archivo de configuración: {e}")
        return None