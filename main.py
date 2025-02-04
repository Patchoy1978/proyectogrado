import sys
import os

import mysql.connector

# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from ventanas.ventanasprograma import VentanaPrincipal
from ventanas.ventana_inicio import VentanaInicioPrograma #esta es la linea que queda
from ventanas.ventana_db_inicio import VentanaDB
# from ventanas.ventana_registro_usuario import VentanaRegistroUsuario

# from ventanas.ventana_recuperacion_contrasena import RecuperacionContrasena

# from ventanas.ventana_admon import VentanaAdmon
def verificar_db():
    
    # try:
    # Conexión con la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="Julian",
        password="",
        port = 3307
    )
    cursor = conexion.cursor()
    cursor.execute("SHOW DATABASES LIKE 'entregaturno';")
    db_exists = cursor.fetchone() is not None
    conexion.close()
    return db_exists
        # return "nombre_de_tu_db" in bases_de_datos  # Cambia esto por el nombre real de tu DB
    # except mysql.connector.Error as e:
    #     print(f"Error al conectar con MySQL: {e}")
    #     return False


if __name__ == "__main__":
    
    # ventana_programa = VentanaPrincipal()
    # ventana = ventana_programa.obtener_ventana()
# este es el codigo 

    if verificar_db():  # Si la base de datos ya está configurada
        ventana_inicio = VentanaInicioPrograma()
        ventana_mostrar = ventana_inicio.obtener_ventana()
    else:  # Si no está configurada, mostrar la ventana de configuración
        ventana_inicio_db = VentanaDB()
        ventana_mostrar = ventana_inicio_db.obtener_ventana()
    
    # ventana_mostrar.deiconify()  # Asegura que la ventana sea visible
    # ventana_mostrar.lift()  # Trae la ventana al frente
    
    # ventana_registro_usuario = VentanaRegistroUsuario()
    # ventana_mostrar = ventana_registro_usuario.obtener_ventana()
    
    # ventana_recuperacion = RecuperacionContrasena()
    
    # ventana_mostrar = ventana_recuperacion.obtener_ventana()
    
    # ventana_admon_abrir = VentanaAdmon()
    
    # abrir_ventana = ventana_admon_abrir.obtener_ventana()
    
    

    # abrir_ventana.mainloop()
    ventana_mostrar.mainloop()