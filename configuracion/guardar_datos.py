import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Guardar_datos_db():

    def __init__(self, host, user, password, port):
        """
        Guarda la configuración de conexión en un archivo JSON.
        """
        self.data = {
            "host": host,
            "user": user,
            "password": password,
            "port": port
        }
        
        # Ubicación del archivo, por ejemplo, en el mismo paquete 'configuracion'
        self.file_path = os.path.join(os.path.dirname(__file__), "config_db.json")
        
        with open(self.file_path, "w") as f:
            
            json.dump(self.data, f, indent=4)