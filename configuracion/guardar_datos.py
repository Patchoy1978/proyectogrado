import json
import sys
import os

from cryptography.fernet import Fernet

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
                   
# class Guardar_datos_email():
    
#     def __init__(self, email, password_encriptada):
        
#         """
#         Guarda la configuración del correo en un archivo JSON.
#         """
#         self.data = {
#             "email": email,
#             "password": password_encriptada
#         }
        
#         try:
#             # Obtener la ruta absoluta del archivo JSON
#             self.ruta_config = os.path.join(os.path.dirname(__file__), 'configuracion_email.json')
            
#             # Guardar los datos en el archivo JSON
#             with open(self.ruta_config, 'w') as archivo:
#                 json.dump(self.data, archivo, indent=4)
            
#             print(f"Datos del correo guardados correctamente en {self.ruta_config}")
        
#         except FileNotFoundError:
#             print("El archivo de configuración no se encuentra.")
        
#         except json.JSONDecodeError:
#             print("Hubo un error al guardar los datos en el archivo de configuración.")
            
# class Guardar_datos_key():
    
#     def __init__(self):
#         # Definir siempre la ruta de la clave al instanciar el objeto.
#         self.ruta_clave = os.path.join(os.path.dirname(__file__), 'clave_secreta.key')
    
#     def generar_clave(self):
#         return Fernet.generate_key()

#     def guardar_clave(self):
#         # Usamos self.ruta_clave, que ya fue definido en __init__
#         if not os.path.exists(self.ruta_clave):
#             clave = self.generar_clave()
#             with open(self.ruta_clave, "wb") as archivo_clave:
#                 archivo_clave.write(clave)
#             print("Clave generada y guardada.")
#         else:
#             print("Clave ya existe. Usando la clave existente.")
#             with open(self.ruta_clave, "rb") as archivo_clave:
#                 clave = archivo_clave.read()

#         return clave

#     def cargar_clave(self):
#         if not os.path.exists(self.ruta_clave):
#             print("La clave no existe.")
#             return None
#         try:
#             with open(self.ruta_clave, "rb") as archivo_clave:
#                 clave = archivo_clave.read()
#                 return clave  # Devuelve la clave
#         except Exception as e:
#             print(f"Error al cargar la clave: {e}")
#             return None

# class DesencriptarContrasena:
    
#     def cargar_datos_cifrados(self):
        
#         # Cargar la contraseña cifrada desde el archivo de configuración
#         ruta_config = os.path.join(os.path.dirname(__file__), 'configuracion_email.json')
        
#         with open(ruta_config, "r") as archivo:
#             data = json.load(archivo)
        
#         encrypted_password = data.get("password")  # La contraseña cifrada guardada
#         return encrypted_password
    
#     def desencriptar_contrasena(self):
        
#         # Cargar la clave de cifrado
#         key_manager = Guardar_datos_key()
#         clave = key_manager.cargar_clave()

#         if not clave:
#             print("Error: No se puede cargar la clave para desencriptar.")
#             return None
        
#         # Cargar la contraseña cifrada
#         encrypted_password = self.cargar_datos_cifrados()

#         if not encrypted_password:
#             print("Error: No se puede cargar la contraseña cifrada.")
#             return None
        
#         # Desencriptar la contraseña
#         f = Fernet(clave)
#         try:
#             decrypted_password = f.decrypt(encrypted_password.encode()).decode()
#             # print("Contraseña desencriptada:", decrypted_password)
#             return decrypted_password
#         except Exception as e:
#             print(f"Error al desencriptar la contraseña: {e}")
            return None
        
