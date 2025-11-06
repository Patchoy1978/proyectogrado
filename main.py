import sys
import os
import mysql.connector
#import customtkinter as ctk # Importa la biblioteca CustomTkinter y la asigna al alias 'ctk' para facilitar su uso.
# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ventanas.ventana_inicio import VentanaInicioPrograma #esta es la linea que queda
from ventanas.ventana_db_inicio import VentanaDB

# Importa la función para leer el archivo JSON
from verificar_datos_db.verificar_datos import cargar_datos_db

from abrirventanasemergentes.abrir_ventanas import mostrar_inicio

def verificar_db():
    
    # Cargar los datos de conexión desde el archivo JSON
    datos = cargar_datos_db()
    
    if datos is None:
        
        return False
    
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

    return db_existe

if __name__ == "__main__":
    
    db_exists = verificar_db()

    if db_exists:  # Si tanto la DB como el JSON existen
        
        ventana_inicio = VentanaInicioPrograma()
        ventana_mostrar = ventana_inicio.obtener_ventana()

    else:
        
        mostrar_inicio()
        ventana_inicio_db = VentanaDB()
        ventana_mostrar = ventana_inicio_db.obtener_ventana()
    
    ventana_mostrar.mainloop()