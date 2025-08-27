import sys
import os
import mysql.connector
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Conexion_DB():
    
    """_instance = None  # variable de clase para la instancia única
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return  # evita reinicializar si ya está creado
        
        config_path = os.path.join(os.path.dirname(__file__), "..", "configuracion", "config_db.json")
        
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            raise Exception("El archivo de configuración no existe.")
        
        self.host = config.get("host")
        self.user = config.get("user")
        self.password = config.get("password")
        self.port = config.get("port")
        self.conexion = None
        self.cursor = None
        
        self._initialized = True
        
    def conectar(self):
        if self.conexion is None or not self.conexion.is_connected():
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database='entregaturno'
            )
            self.cursor = self.conexion.cursor()
            print(f"Conectado a la base de datos en {self.host} con usuario {self.user}")
        else:
            print("Ya existe una conexión abierta.")
    
    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conexion:
            self.conexion.close()
            self.conexion = None
        print("Conexión cerrada.")"""
    
    def __init__(self):
        
        config_path = os.path.join(os.path.dirname(__file__), "..", "configuracion", "config_db.json")
        
        # Abrir y cargar el archivo JSON
        try:
            
            with open(config_path, "r") as f:
                
                config = json.load(f)
                
        except FileNotFoundError:
            
            raise Exception("El archivo de configuración no existe. Asegúrate de haber guardado la configuración.")

        self.host = config.get("host")
        self.user = config.get("user")
        self.password = config.get("password")
        self.port = config.get("port")
        self.conexion = ''
        self.cursor = ''
    
    def conectar(self):
                
        self.conexion = mysql.connector.connect(
            
            host = self.host,
            user = self.user,
            password = self.password,
            port = self.port,
            database = 'entregaturno'
        )
        
        print(self.conexion)
        
        self.cursor = self.conexion.cursor(buffered=True)
        
        #print(f"Conectando a la base de datos en {self.host} con el usuario {self.user}")
    
    def cerrar_conexion(self):
        
        #Cierra la conexión y el cursor de la base de datos.
        
        if self.cursor:
            
            self.cursor.close()
            
            #print("Cursor cerrado.")
            
        if self.conexion:
            
            self.conexion.close()
            
            #print("Conexión cerrada.")
    
    
