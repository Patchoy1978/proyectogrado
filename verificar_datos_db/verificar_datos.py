import json
import os
import sys

# Agrega el directorio padre al sys.path para permitir importaciones desde niveles superiores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define la ruta absoluta del archivo config_db.json
ruta_archivo = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'configuracion', 'config_db.json'))

# Función para cargar los datos de conexión a la base de datos desde el archivo JSON
def cargar_datos_db():
            
    if not os.path.exists(ruta_archivo):
        # ✅ Si el archivo no existe, no mostrar ningún mensaje
        return None

    try:
        with open(ruta_archivo, 'r') as archivo:
            datos = json.load(archivo)  # Carga los datos en un diccionario
            return datos
    except json.JSONDecodeError:
        # ⚠️ Si el archivo existe pero está mal formateado
        print("⚠️ El archivo de configuración existe pero no es un JSON válido.")
        return None
    except Exception as e:
        # Otros errores inesperados
        print(f"⚠️ Error inesperado al leer el archivo de configuración: {e}")
        return None