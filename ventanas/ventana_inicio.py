import sys # Importa el módulo sys para interactuar con el sistema y modificar rutas de importación
import os # Importa el módulo os para manipular rutas y directorios del sistema operativo
import customtkinter as ctk # Importa la biblioteca CustomTkinter para la creación de interfaces gráficas
import bcrypt # Importa la biblioteca bcrypt para el manejo y cifrado de contraseñas seguras

# Agregar el directorio padre al sys.path para permitir importaciones desde niveles superiores

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

# Obtener la ruta absoluta del directorio "img"

ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'img'))

from PIL import Image # Importa la clase Image de la biblioteca Pillow para manipulación de imágenes

from usuarioactual.usuario_actual import UsuarioActual

from ventanas.ventana_admon import VentanaAdmon

from conexion_DB.conexionDB import Conexion_DB # Importa la clase Conexion_DB desde el módulo conexion_DB.conexionDB para la conexión con la base de datos

# Importa funciones para abrir diferentes ventanas dentro de la aplicación

from abrirventanas.abrir import (abrir_ventana_visualizar_datos_ppal, 
                                abrir_ventana_registro_usuario, 
                                abrir_ventana_envio_codigo, 
                                abrir_ventana_admon,
                                abrir_ventana_visualizar_datos_ppal_radiologo
                                )
# Importa funciones para abrir ventanas emergentes con diferentes mensajes de error o éxito
from abrirventanasemergentes.abrir_ventanas import (abrir_ventana_conn_exito, 
                                                    abrir_ventana_conn_fallida, 
                                                    email_incorrecto, 
                                                    contrasena_incorrecta, 
                                                    campos_requeridos,
                                                    cerrar_conexion
                                                    )

class VentanaInicioPrograma():
    
    def __init__(self, parent_window=None):
        
        # Inicialización de la ventana y parámetros
        self.parent_window = parent_window
        if parent_window:
            self.root = ctk.CTkToplevel()
            self.root.transient(parent_window)  # hace que la ventana esté asociada
        else:
            self.root = ctk.CTk()
        
        # Definir el tamaño de la nueva ventana
        ancho_nueva_ventana = 500
        alto_nueva_ventana = 330
        
        # Establecer el modo de apariencia y el tema de color predeterminado
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        # Configuración de la acción de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.salir)
        
        # Calcular la posición para centrar la ventana
        x = (self.root.winfo_screenwidth() // 2) - (ancho_nueva_ventana // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto_nueva_ventana // 2)
        
        # Establecer las dimensiones y la posición de la ventana
        self.root.geometry(f"{ancho_nueva_ventana}x{alto_nueva_ventana}+{x}+{y}")
        
        self.root.title('Entrega De Turno') # Establecer el título de la ventana
        
        icon_path = os.path.join(ruta_base, 'documento.ico')
        self.root.iconbitmap(icon_path)
        
        self.root.resizable(False, False) # Evitar que la ventana pueda ser redimensionada
        
        # Configuración de las filas y columnas en la ventana principal para distribuir el contenido
        self.root.grid_rowconfigure(0, weight=1)  
        self.root.grid_rowconfigure(1, weight=1)  
        self.root.grid_rowconfigure(2, weight=1)  
        self.root.grid_columnconfigure(0, weight=1)
        
        try:
            
            # Intentar establecer la conexión con la base de datos
            self.db = Conexion_DB()
            self.db.conectar()
            abrir_ventana_conn_exito() # Abrir ventana indicando que la conexión fue exitosa
        
        except Exception:
            
            abrir_ventana_conn_fallida() # Si ocurre un error, abrir ventana indicando que la conexión falló
        
        # Cargar imágenes para los iconos de visibilidad de contraseña, ajustando su tamaño
        self.ojo_abierto = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "ojoabierto.png")).resize((30, 30)), size=(30, 30))
        self.ojo_cerrado = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "ojo-cerrado.png")).resize((30, 30)), size=(30, 30))
        
        # Definir un diccionario con las fuentes de los textos utilizados en la interfaz
        self.fonts = {
            'title':('Verdana', 26, 'bold'),
            'label':('Verdana', 14, 'bold'),
            'label_titulo':('Verdana', 14, 'bold'),
            'boton':('Verdana', 14, 'bold'),
        }
        
        # Crear y configurar los frames que estructuran la ventana
        self.frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame.grid(row= 0, column= 0, sticky= 'nsew')
        
        self.frame1 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame1.grid(row= 1, column= 0, sticky= 'nsew')
        
        self.frame2 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame2.grid(row= 2, column= 0, sticky= 'nsew')
        
        # Configurar las columnas en cada frame para ajustar distribución del contenido
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)
        
        # Configuración específica de columnas en frame2
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.grid_columnconfigure(2, weight=1)
        self.frame2.grid_columnconfigure(3, weight=0)
        self.frame2.grid_columnconfigure(4, weight=1)

        # Configuración de filas en frame2
        self.frame2.grid_rowconfigure(0, weight=1)
        
        # Diccionarios para almacenar variables, entradas y botones
        self.vars = {}
        self.entries = {}
        self.botones_ver_contrasena = {}
        
        self.ventana_datos_ingreso() # Llamar a la función que configura los elementos de la ventana de ingreso de datos
        
    def obtener_ventana(self):
        
        return self.root # Retorna la ventana principal de la aplicación

    def ventana_datos_ingreso(self):
        
        # Lista de campos de texto que se mostrarán como etiquetas
        campos = [
            
            {'label': 'Bienvenido Al Sistema\nEntrega De Turno', 'ancho': 400, 'tipo': 'label'},
            
        ]
        
        # Lista de campos de entrada para el usuario
        campos1 = [
            
            {'clave': 'email', 'label': 'Email', 'ancho': 400, 'tipo': 'entry'},
            {'clave': 'contrasena', 'label': 'Password', 'ancho': 400, 'tipo': 'entry'},
        ]
        
        # Lista de botones con sus configuraciones y acciones
        campos2 = [
            
            {"label": "Registrarse", "color": "#00155C", "tipo": "boton", "ancho": 50, "alto":10, 'image': None, "command": lambda: (abrir_ventana_registro_usuario(self.root), self.root.iconify())},
            {"label": " Ingresar ", "color": "#00155C", "tipo": "boton", "ancho": 50, "alto":10, 'image': None, "command": self.validacion_entrada_sistema},
            {"label": "", "color": "transparent", "tipo": "boton", "ancho": 50, "alto":50, "command": self.alternar_contrasena, 'image': self.ojo_abierto, "clave": "ver_contrasena"},
            {"label": "Olvidó\nContraseña", "color": "#00155C", "tipo": "boton", "ancho": 50, "alto":10, 'image': None, "command": lambda: (abrir_ventana_envio_codigo(self.root), self.root.iconify())},

        ]
        
        # Crear etiquetas en el primer frame
        for i, campo in enumerate(campos):
            
            self.crear_label(self.frame, texto= campo['label'], font=self.fonts['title'], fila=0, columna=0, ancho=campo['ancho'])
        
        # Crear etiquetas y campos de entrada en el segundo frame
        for i, campo1 in enumerate(campos1):
            
            if campo1['tipo'] == 'entry':
                
                # Crear etiqueta para el campo de entrada
                self.crear_label(self.frame1, texto= campo1['label'], font=self.fonts['label_titulo'], fila=i*2+1,columna=0, ancho=campo1['ancho'])
                
                # Crear campo de entrada según su tipo (email o contraseña)
                if campo1['clave'] == 'email':
                    
                    self.vars['clave']= ctk.StringVar()
            
                    self.entries['email'] = self.crear_entry(self.frame1,
                                font=self.fonts['label'],
                                fila= i*2+2,
                                columna= 0,
                                ancho_widget=campo1['ancho'],
                                show= '',
                                )
                    
                    # --- Poner focus automáticamente ---
                    self.entries['email'].after(100, lambda: self.entries['email'].focus())
                
                else:
                    
                    self.vars['clave']= ctk.StringVar()
                    
                    self.entries['contrasena'] = self.crear_entry(self.frame1,
                                font=self.fonts['label'],
                                fila= i*2+2,
                                columna= 0,
                                ancho_widget=campo1['ancho'],
                                show= '*'
                                )
        
        # Crear botones en el tercer frame
        for i, campo2 in enumerate(campos2):
            
            boton = self.crear_boton(self.frame2, self.fonts['boton'], campo2['label'], campo2['color'], 1, i+1, image=campo2['image'], alto=campo2['alto'], ancho=campo2['ancho'], command=campo2['command'])

            # Guardar referencia al botón de alternar contraseña
            if "clave" in campo2:
                self.botones_ver_contrasena["ver_contrasena"] = boton
            
    def validacion_entrada_sistema(self):
        
        # Obtener y limpiar los datos ingresados por el usuario
        email = self.entries['email'].get().strip()
        contrasena = self.entries['contrasena'].get().strip()
        
        # Verificar si los campos están vacíos
        if not all([email, contrasena]):
            
            campos_requeridos()
            
            return

        # Consulta SQL para obtener el ID de usuario, cargo y contraseña encriptada
        consulta = 'SELECT u.id_usuario, c.nombre_cargo, u.contrasena, u.nombre_usuario FROM usuarios u JOIN cargos c ON u.cargo = c.id_cargo WHERE u.email = %s'
        self.db.cursor.execute(consulta, (email,)) # Ejecutar la consulta con el email proporcionado
        resultado = self.db.cursor.fetchone() # Obtener el resultado de la consulta
        
        # Si el correo no está registrado en la base de datos
        if not resultado:
            
            email_incorrecto()
            
            return
        
        id_usuario, cargo, hash_almacenado, nombre = resultado  # Desempaquetar los valores obtenidos
        
        # Verificar la contraseña con bcrypt
        if not bcrypt.checkpw(contrasena.encode('utf-8'), hash_almacenado.encode('utf-8')):
            
            contrasena_incorrecta() # Mostrar mensaje de error si la contraseña es incorrecta
            
            return
        
        UsuarioActual.set_usuario(email, nombre, cargo, id_usuario)
        
        self.root.destroy() # Cerrar la ventana actual después de la validación exitosa
        
        # Abrir la ventana correspondiente según el rol del usuario
        if cargo== 'Administrador':

            abrir_ventana_admon()
            
        elif cargo== 'Radiologo':
            
            abrir_ventana_visualizar_datos_ppal_radiologo()
        
        else:
            
            abrir_ventana_visualizar_datos_ppal() # Abrir la ventana de usuario estándar

    def crear_label(self,parent, texto, font, fila, columna, ancho = 1, alto = 1):
        
        # Crear un label con los parámetros dados
        label = ctk.CTkLabel(parent,
                            text= texto,
                            font=font,
                            
                            )
        
        # Posicionar el label en la cuadrícula
        label.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto, pady= 10, sticky= 'nsew')
        
        return label # Retornar el label creado
    
    def crear_entry(self,parent, font, fila, columna, ancho=1, alto=1, ancho_widget=150, alto_widget=26, show = ''):
        
        # Crear un campo de entrada con los parámetros dados
        entry = ctk.CTkEntry(parent,
                            font = font,
                            text_color='black',
                            corner_radius=10,
                            width=ancho_widget,
                            height=alto_widget,
                            fg_color='lightgray',
                            show = show
                            )
        
        # Posicionar el campo de entrada en la cuadrícula
        entry.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto, padx=5, sticky='ew')
                
        return entry # Retornar el campo de entrada creado
        
    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, image, ancho=70, alto=70, command=None):
        
        # Crear un botón con los parámetros especificados
        boton = ctk.CTkButton(
                                parent,
                                font=font,
                                text=texto,
                                fg_color=color_fondo,
                                text_color='white',
                                height=alto,
                                width= ancho,
                                command=command,
                                corner_radius=10,
                                image = image,
                                hover_color= 'lightgreen'
                                
                            )
        
        # Posicionar el botón en la cuadrícula
        boton.grid(row=fila, column=columna, rowspan=alto, padx=5, pady= 5, sticky='nsew')
        
        if image is not None:
            
            boton.image = image  # ✅ mantener referencia para evitar garbage collection
        
        return boton # Retornar el botón creado

    def alternar_contrasena(self):
        
        # Alternar visibilidad de "contrasena"
        for campo in ["contrasena"]:
            if campo in self.entries:
                entry = self.entries[campo]
                if entry.cget('show') == '*':
                    entry.configure(show='')
                    nuevo_icono = self.ojo_cerrado
                else:
                    entry.configure(show='*')
                    nuevo_icono = self.ojo_abierto

        # Cambiar la imagen del botón alternar
        if "ver_contrasena" in self.botones_ver_contrasena:
            boton = self.botones_ver_contrasena["ver_contrasena"]
            boton.configure(image=nuevo_icono)
            boton.image = nuevo_icono  # Mantener referencia para evitar garbage collection

    # Definición de la función 'salir' que se ejecuta cuando el usuario hace clic en el botón "Salir"
    def salir(self):
        
        """Método personalizado para el botón Salir.
        """
        # Si existe una conexión a la base de datos, se cierra
        if self.db:
            
            self.db.cerrar_conexion()  # Llamamos al método de la clase 'Conexion_DB' para cerrar la conexión con la base de datos
            
            cerrar_conexion()
        
        self.root.destroy() # Cierra la ventana actual de la aplicación
        
        # Si hay una ventana principal asociada, la restauramos
        if self.parent_window:
            
            self.parent_window.deiconify() # Muestra nuevamente la ventana principal si estaba minimizada o escondida
            
            self.parent_window.lift() # Asegura que la ventana principal esté por encima de otras ventanas abiertas
