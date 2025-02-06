import sys
import os
import mysql.connector
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Conexion_DB():
    
    def __init__(self):
        
        config_path = os.path.join(os.path.dirname(__file__), "..", "configuracion", "config_db.json")
        
        # Abrir y cargar el archivo JSON
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            raise Exception("El archivo de configuración no existe. Asegúrate de haber guardado la configuración.")

        # Asignar los valores a atributos de la clase o usarlos según necesites.
        self.host = config.get("host")
        self.user = config.get("user")
        self.password = config.get("password")
        self.port = config.get("port")
        self.conexion = ''
        self.cursor = ''
        
    def conectar(self):
        # Aquí implementarías la lógica para conectarte a la base de datos utilizando self.host, etc.
        
        self.conexion = mysql.connector.connect(
            
            host = self.host,
            user = self.user,
            password = self.password,
            port = self.port,
            database = 'entregaturno'
        )
        
        print(self.conexion)
        
        self.cursor = self.conexion.cursor()
        
        print(f"Conectando a la base de datos en {self.host} con el usuario {self.user}")
    
    def cerrar_conexion(self):
        
        """Cierra la conexión y el cursor de la base de datos."""
        if self.cursor:
            self.cursor.close()
            print("Cursor cerrado.")
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")
        
        # self.conexion.close()
        
# Conexion_DB().conectar()