import sys
import os
import mysql.connector

# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ventanas.ventana_inicio import VentanaInicioPrograma
from ventanas.ventana_db_inicio import VentanaDB
from abrirventanasemergentes.abrir_ventanas import mostrar_inicio
from verificar_datos_db.verificar_datos import cargar_datos_db
from gestor_db.sincronizador import SincronizadorDB
from conexion_DB.conexionDB import Conexion_DB
from CrearDB.crear_DB import ConexionDB  # <-- Para obtener sql_aux y sql_principal

def verificar_db(datos):
    """
    Verifica si la base de datos 'entregaturno' existe usando los datos de conexión.
    """
    try:
        conexion = mysql.connector.connect(
            host=datos['host'],
            user=datos['user'],
            password=datos['password'],
            port=datos['port']
        )
        cursor = conexion.cursor()
        cursor.execute("SHOW DATABASES LIKE 'entregaturno';")
        db_existe = cursor.fetchone() is not None
        cursor.close()
        conexion.close()
        return db_existe
    except mysql.connector.Error:
        return False

if __name__ == "__main__":
    datos = cargar_datos_db()

    if datos is None:
        # No hay datos de conexión, se muestra ventana DB
        mostrar_inicio()
        ventana_inicio_db = VentanaDB()
        ventana_mostrar = ventana_inicio_db.obtener_ventana()

    else:
        db_exists = verificar_db(datos)

        if db_exists:
            # -----------------------------
            #   *** CONEXIÓN ÚNICA ***
            # -----------------------------
            conexion = Conexion_DB()
            conexion.conectar()  # conexión + cursor abiertos

            # Obtener definiciones de tablas desde CrearDB
            crear_db = ConexionDB(datos['host'], datos['user'], datos['password'], datos['port'])
            sql_aux = crear_db.sql_aux
            sql_principal = crear_db.sql_principal

            # Crear sincronizador usando conexión existente y definiciones
            sincronizador = SincronizadorDB(conexion.cursor, conexion.conexion, sql_aux, sql_principal)
            sincronizador.sincronizar()

            # Cerrar conexión una sola vez
            conexion.cerrar_conexion()

            # Abrir ventana principal
            ventana_inicio = VentanaInicioPrograma()
            ventana_mostrar = ventana_inicio.obtener_ventana()

        else:
            # Base de datos no existe, se muestra ventana DB
            mostrar_inicio()
            ventana_inicio_db = VentanaDB()
            ventana_mostrar = ventana_inicio_db.obtener_ventana()

    ventana_mostrar.mainloop()

