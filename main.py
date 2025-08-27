import sys
import os
import mysql.connector
#import customtkinter as ctk # Importa la biblioteca CustomTkinter y la asigna al alias 'ctk' para facilitar su uso.
# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Obtener la ruta absoluta del directorio "img"
#ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__),'img'))

#ruta_ojo_abierto = os.path.join(ruta_base, "ojoabierto.png")
#ruta_ojo_cerrado = os.path.join(ruta_base, "ojo-cerrado.png")


#from PIL import Image # Importa la clase Image de la biblioteca Pillow para manipulación de imágenes

from ventanas.ventana_inicio import VentanaInicioPrograma #esta es la linea que queda
from ventanas.ventana_db_inicio import VentanaDB

# Importa la función para leer el archivo JSON
from verificar_datos_db.verificar_datos import cargar_datos_db

def verificar_db():
    
    # Cargar imágenes para los iconos de visibilidad de contraseña, ajustando su tamaño
    #ojo_abierto = ctk.CTkImage(light_image=Image.open(ruta_ojo_abierto).resize((50, 50)), size=(50, 50))
    #ojo_cerrado = ctk.CTkImage(light_image=Image.open(ruta_ojo_cerrado).resize((50, 50)), size=(50, 50))
    
    # Cargar los datos de conexión desde el archivo JSON
    datos = cargar_datos_db()
    
    # try:
    # Conexión con la base de datos
    conexion = mysql.connector.connect(
        host=datos['host'],
        user=datos['user'],
        password=datos['password'],
        port = datos['port']
    )
    cursor = conexion.cursor()
    cursor.execute("SHOW DATABASES LIKE 'entregaturno';")
    db_existe = cursor.fetchone() is not None
    conexion.close()
    # return db_exists
        # return "nombre_de_tu_db" in bases_de_datos  # Cambia esto por el nombre real de tu DB
    # except mysql.connector.Error as e:
    #     print(f"Error al conectar con MySQL: {e}")
    #     return False


    return db_existe


if __name__ == "__main__":
    
    db_exists = verificar_db()

    if db_exists:  # Si tanto la DB como el JSON existen
        
        ventana_inicio = VentanaInicioPrograma()
        ventana_mostrar = ventana_inicio.obtener_ventana()

    else:
        
        ventana_inicio_db = VentanaDB()
        ventana_mostrar = ventana_inicio_db.obtener_ventana()
    
    ventana_mostrar.mainloop()