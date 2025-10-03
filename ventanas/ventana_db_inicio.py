# Importación de los módulos necesarios del sistema
import sys
import os

# Agrega el directorio padre al sys.path para permitir importaciones desde niveles superiores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Obtener la ruta absoluta del directorio "img"
ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'img'))

from PIL import Image # Importa la clase Image de la biblioteca Pillow para manipulación de imágenes

# Importación de la biblioteca CustomTkinter para la interfaz gráfica
import customtkinter as ctk

# Importación de funciones específicas desde el módulo abrir_ventanas dentro del paquete abrirventanasemergentes
from abrirventanasemergentes.abrir_ventanas import archivo_creado, archivo_fallido, campos_requeridos

class VentanaDB():
    
    # Método constructor de la clase
    def __init__(self):
        
        # Definición de dimensiones de la ventana
        ancho_ventana_nueva = 500
        alto_ventana_nueva = 450
        
        # Configuración de la apariencia de la interfaz
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        # Creación de la ventana principal
        self.root = ctk.CTk()
        
        # Evita el cierre accidental de la ventana
        self.root.protocol("WM_DELETE_WINDOW", lambda:None)
        
        # Cálculo de la posición de la ventana en el centro de la pantalla
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        # Establece el tamaño y la posición de la ventana
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.resizable(False,False) # Evita que la ventana sea redimensionable
        
        self.root.title('Entrega de Turno') # Título de la ventana
        
        # Definición de estilos de fuente para los widgets
        self.fonts = {
            
            'title': ('verdana', 26,  'bold'),
            'label_title': ('verdana', 14,  'bold'),
            'label': ('verdana', 12,  'bold'),
            'boton': ('verdana', 14,  'bold')
        }
        
        # Configuración de la estructura de la cuadrícula de la ventana
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        # Cargar imágenes para los iconos de visibilidad de contraseña, ajustando su tamaño
        self.ojo_abierto = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "ojoabierto.png")).resize((50, 50)), size=(50, 50))
        self.ojo_cerrado = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "ojo-cerrado.png")).resize((50, 50)), size=(50, 50))
        
        # Creación y configuración de los frames contenedores
        self.frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame.grid(row= 0, column= 0, sticky='nsew')
        
        self.frame1 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame1.grid(row= 1, column= 0, sticky='nsew')
        
        self.frame2 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame2.grid(row= 2, column= 0, sticky='nsew')
        
        # Configuración de las columnas y filas de los frames
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame2.grid_rowconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.grid_columnconfigure(2, weight=1)
        
        # Diccionarios para almacenar botones
        self.botones_ver_contrasena = {}
        
        self.ingreso_DB() # Llamada al método que maneja el ingreso a la base de datos
    
    # Método que devuelve la ventana principal
    def obtener_ventana(self):
        
        return self.root # Retorna la instancia de la ventana principal
    
    # Método para gestionar la entrada de datos de la base de datos
    def ingreso_DB(self):
        
        # Lista de campos que incluyen el mensaje de bienvenida
        campos = [
            
            {'label': 'Bienvenido\nPrograma Entrega de Turno'}
        ]
        
        # Campos para ingresar la información de la base de datos
        campos1 = [
            
            {'label': 'Ingresa el Host', 'placeholder': 'Host','ancho': 100, 'alto': 26, 'clave': 'Host'},
            {'label': 'Ingresa el Usuario', 'placeholder': 'User','ancho': 100, 'alto': 26, 'clave': 'User'},
            {'label': 'Ingresa el Password', 'placeholder': 'Password','ancho': 100, 'alto': 26, 'clave': 'Password'},
            {'label': 'Ingresa el Puerto', 'placeholder': 'Port','ancho': 100, 'alto': 26, 'clave': 'Port'},
        ]
        
        # Campos para los botones de acción
        campos2 = [
            
            {'label': 'Crear DB', 'placeholder': 'Host','ancho': 100, 'alto': 50, 'color':'#00155c', 'image': None, 'command': self.validacion_entrada_sistema},
            {"label": "", "color": "transparent", "tipo": "boton", "ancho": 50, "alto":50, "command": self.alternar_contrasena, 'image': self.ojo_abierto, "clave": "ver_contrasena"},
            {'label': 'Salir', 'placeholder': 'User','ancho': 100, 'alto': 50, 'color':'#00155c','image': None, 'command': self.cerrar},
        ]
        
        # Crear etiquetas de bienvenida
        for i, campo in enumerate(campos):
        
            self.crear_label(self.frame, text=campo['label'], font=self.fonts['title'], fila=0, columna=0)
        
        # Crear etiquetas y entradas para cada campo de la base de datos
        for i, campo1 in enumerate(campos1):
    
            self.crear_label(self.frame1, text=campo1['label'], font=self.fonts['label_title'], fila=i*2+1, columna=0)

            if campo1['clave'] == 'Password':
                
                # Crear entradas para Host, Usuario, Password y Puerto
                entry = self.crear_entry(self.frame1, 
                                font=self.fonts['label'], 
                                fila=i*2+2, 
                                columna= 0, 
                                ancho_widget=campo1['ancho'], 
                                alto_widget= campo1['alto'], 
                                placeholder =campo1['placeholder'],
                                show= '*'
                                ) 

                self.entry_password = entry
                
            else:
                
                # Crear entradas para Host, Usuario, Password y Puerto
                entry = self.crear_entry(self.frame1, 
                                font=self.fonts['label'], 
                                fila=i*2+2, 
                                columna= 0, 
                                ancho_widget=campo1['ancho'], 
                                alto_widget= campo1['alto'], 
                                placeholder =campo1['placeholder']
                                )   
                
                # Asignar a las variables de instancia
                if campo1['placeholder'] == 'Host':
                    self.entry_host = entry
                elif campo1['placeholder'] == 'User':
                    self.entry_user = entry
                elif campo1['placeholder'] == 'Password':
                    self.entry_password = entry
                elif campo1['placeholder'] == 'Port':
                    self.entry_port = entry

        # Crear botones para las acciones de crear DB y salir
        for i, campo2 in enumerate(campos2):
            
            boton = self.crear_boton(self.frame2, 
                            font=self.fonts['boton'], 
                            texto= campo2['label'], 
                            color_fondo= campo2['color'], 
                            fila=0, 
                            columna= i+1, 
                            ancho=campo1['ancho'], 
                            alto= campo1['alto'], 
                            command = campo2['command'],
                            image = campo2['image']
                            )
            
            # Guardar referencia al botón de alternar contraseña
            if "clave" in campo2:
                self.botones_ver_contrasena["ver_contrasena"] = boton
    
    # Método para crear la base de datos
    def crear_db(self):
        
        # Importa las clases necesarias para la conexión y la configuración        
        from CrearDB.crear_DB import ConexionDB
        from configuracion.guardar_datos import Guardar_datos_db 
        
        # Obtener los valores ingresados en los campos de entrada (Entry)
        host = self.entry_host.get() # Obtener el valor del Host
        user = self.entry_user.get() # Obtener el valor del Usuario
        password = self.entry_password.get() # Obtener el valor de la contraseña
        port = int(self.entry_port.get())  # Convertir el puerto a entero
        
        try:

            # Guardar la configuración en el archivo JSON
            Guardar_datos_db(host, user, password, port)
            
            archivo_creado() # Si se guarda correctamente, mostrar un mensaje de éxito
            
        except Exception:
            
            archivo_fallido() # Si ocurre algún error al guardar, mostrar un mensaje de fallo
        
        
        ConexionDB(host, user, password, port) 
    
    # Método para crear un label (etiqueta) en la interfaz gráfica
    def crear_label(self, parent, text, font, fila, columna, ancho= 1, alto= 1):
        
        # Crear un objeto CTkLabel con el texto, la fuente y el color de texto especificado
        label = ctk.CTkLabel(parent,
                            text=text, # El texto que aparecerá en la etiqueta
                            font=font, # La fuente del texto
                            text_color= '#484a4b' # El color del texto
                            )
        
        # Colocar el label en la cuadrícula con las propiedades de fila, columna, ancho y alto
        label.grid(row= fila, column= columna, sticky='nsew', columnspan= ancho, rowspan= alto)
        
        return label # Retornar el objeto label creado
    
    # Método para crear un campo de entrada (Entry) en la interfaz gráfica
    def crear_entry(self,parent, font, fila, columna, placeholder, ancho=1, alto=1, ancho_widget=150, alto_widget=26, show = ''):
        
        # Crear un objeto CTkEntry con las propiedades especificadas como fuente, tamaño, color, y el texto de marcador de posición
        entry = ctk.CTkEntry(parent,
                            font = font, # La fuente del texto dentro del entry
                            text_color='black', # El color del texto dentro del entry
                            corner_radius=10, # El radio de las esquinas del entry
                            width=ancho_widget, # El ancho del entry
                            height=alto_widget, # El alto del entry
                            fg_color='lightgray', # El color de fondo del entry
                            placeholder_text=placeholder, # El texto de marcador de posición
                            placeholder_text_color= 'gray', # El color del texto de marcador de posición
                            show = show 
                            )
        
        # Colocar el entry en la cuadrícula con las propiedades de fila, columna, ancho y alto
        entry.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto, padx=5, sticky='ew')
                
        return entry # Retornar el objeto entry creado
    
    # Método para crear un botón en la interfaz gráfica   
    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, image, ancho=70, alto=70, command=None):
        
        # Crear un objeto CTkButton con las propiedades especificadas como texto, color de fondo, tamaño, y acción al hacer clic
        boton = ctk.CTkButton(
                                parent, # El contenedor o marco donde se colocará el botón
                                font=font,  # La fuente del texto del botón
                                text=texto, # El texto que aparecerá en el botón
                                fg_color=color_fondo, # El color de fondo del botón
                                text_color='white', # El color del texto del botón
                                height=alto, # El alto del botón
                                width= ancho, # El ancho del botón
                                command=command, # La acción a realizar al hacer clic en el botón
                                corner_radius=10, # El radio de las esquinas del botón
                                image= image,
                                hover_color= "lightgreen"
                            )
        
        # Colocar el botón en la cuadrícula con las propiedades de fila, columna, tamaño y espaciado
        boton.grid(row=fila, column=columna, rowspan=alto, padx=15, pady= 15, sticky='nsew')
        
        return boton # Retornar el objeto botón creado
    
    # metodo para cerrar y abrir ventana
    def cerrar(self):
        
        self.root.destroy() #cierra la ventana actual
        sys.exit()  # Cierra completamente el programa
    
    # Método que valida si todos los campos requeridos para la conexión a la base de datos han sido ingresados            
    def validacion_entrada_sistema(self):
        
        # Importa la función para abrir la ventana de inicio
        from abrirventanas.abrir import abrir_ventana_admon
        
        host = self.entry_host.get().strip() # Obtiene el valor ingresado en el campo 'Host', eliminando espacios al inicio y final
        user = self.entry_user.get().strip() # Obtiene el valor ingresado en el campo 'Usuario'
        password = self.entry_password.get().strip() # Obtiene el valor ingresado en el campo 'Contraseña'
        port = self.entry_port.get().strip() # Obtiene el valor ingresado en el campo 'Puerto'
        
        # Verifica si alguno de los campos está vacío
        if not all([host,user,password,port]):
            
            campos_requeridos() # Si falta alguno, muestra un mensaje de advertencia usando la función importada
            
            return # Detiene la ejecución del método
        
        else:
            
            self.crear_db()  # Si todos los campos están completos, llama al método para crear la base de datos
            self.root.destroy()
            abrir_ventana_admon()

    def alternar_contrasena(self):
        
        # Alternar visibilidad del campo de contraseña
        if self.entry_password.cget('show') == '*':
            self.entry_password.configure(show='')  # Mostrar la contraseña
            nuevo_icono = self.ojo_cerrado
        else:
            self.entry_password.configure(show='*')  # Ocultar la contraseña
            nuevo_icono = self.ojo_abierto

        # Cambiar la imagen del botón
        if "ver_contrasena" in self.botones_ver_contrasena:
            boton = self.botones_ver_contrasena["ver_contrasena"]
            boton.configure(image=nuevo_icono)
            boton.image = nuevo_icono  # Evita que se elimine por el recolector de basura
            
#a = VentanaDB()
#b= a.obtener_ventana()
#b.mainloop()