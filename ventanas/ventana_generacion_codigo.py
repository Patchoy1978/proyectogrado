# Importación de módulos estándar y externos para el manejo de sistema de archivos y funcionalidades específicas
import sys # Permite interactuar con el sistema de Python y la configuración del entorno
import os # Permite interactuar con el sistema de archivos de Python y realizar operaciones de sistema de Python
import customtkinter as ctk # Importa el módulo de interfaz de usuario personalizado
import random # Permite generar números aleatorios
import re # Proporciona herramientas para trabajar con expresiones regulares

# Añadiendo directorios a la lista de rutas de búsqueda para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Ruta principal del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'configuracion'))) # Directorio de configuración

# Importación de funciones y módulos personalizados desde otras ubicaciones del proyecto
from abrirventanasemergentes.abrir_ventanas import ( # Funciones de ventanas emergentes y validaciones
                                                    email_formato, # Validación de formato de email
                                                    campos_requeridos,  # Validación de campos requeridos
                                                    confirmacion_codigo, # Validación de confirmación de código
                                                    validacion_cuenta, # Validación de cuenta
                                                    email_no_esta, # Validación de email no está
                                                    abrir_ventana_conn_exito, # Ventana emergente de conexión exitosa
                                                    abrir_ventana_conn_fallida , # Ventana emergente de conexión fallida
                                                    )

from abrirventanas.abrir import abrir_ventana_recuperacion_contrasena # Función para abrir la ventana de recuperación de contraseña
from conexion_DB.conexionDB import Conexion_DB # Función para la conexión a la base de datos

class EnvioRecuperacionContrasena():
    
    def __init__(self, parent_window = None):
        
        # Inicialización de la ventana y parámetros
        self.parent_window = parent_window
        
        ancho_ventana_nueva = 450 # Definir el ancho de la ventana
        alto_ventana_nueva = 250 # Definir el alto de la ventana
        
        # Configuración del tema de la ventana
        ctk.set_appearance_mode('light') # Modo claro para la apariencia
        ctk.set_default_color_theme('green') # Color de fondo de la ventana
        
        # Crea una ventana secundaria (Toplevel)
        self.root = ctk.CTkToplevel()
        
        # Configuración de la acción de cierre
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Centrar la ventana en la pantalla
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        # Definir tamaño y ubicación de la ventana
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        # Configurar propiedades de la ventana
        self.root.title('Envio Código Para Recuperacion Contraseña') # Titulo de la ventana
        self.root.iconbitmap('img/documento.ico') # Icono de la ventana
        self.root.resizable(False, False)  # Ventana no se puede redimensionar
        
        # Configuración de las filas y columnas para el diseño en la ventana
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        
        # Intentar conectar con la base de datos
        try:
            
            self.db = Conexion_DB() # Crea una instancia para la conexión a la base de datos
            self.db.conectar() # Conecta con la base de datos
            abrir_ventana_conn_exito() # Si la conexión es exitosa, muestra la ventana de éxito
        
        except Exception:
            
            abrir_ventana_conn_fallida() # Si ocurre un error, muestra la ventana de error
        
        # Definición de fuentes para los textos
        self.fonts = {
            
            'title': ('verdana', 26,  'bold'),
            'label_title': ('verdana', 14,  'bold'),
            'label': ('verdana', 12,  'bold'),
            'boton': ('verdana', 14,  'bold')
        }
        
        # Crear los frames donde se organizarán los elementos en la ventana
        self.frame = ctk.CTkFrame(self.root, fg_color='transparent')
        
        self.frame.grid(row= 0, column = 0, sticky = 'nsew')  # Ubicación del frame en la ventana
        
        self.frame_1 = ctk.CTkFrame(self.root, fg_color='transparent')
        
        self.frame_1.grid(row= 1, column = 0, sticky = 'nsew')  # Ubicación del frame en la ventana
        
        self.frame_2 = ctk.CTkFrame(self.root, fg_color='transparent')
        
        self.frame_2.grid(row= 2, column = 0, sticky = 'nsew')  # Ubicación del frame en la ventana
        
        # Configuración de las columnas y filas dentro de los frames
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        self.frame_1.grid_columnconfigure(0, weight=1)
        
        self.frame_2.grid_columnconfigure(1, weight=1)
        self.frame_2.grid_columnconfigure(2, weight=1)
        self.frame_2.grid_rowconfigure(0, weight=1)
        
        # Diccionarios para almacenar entradas, variables y botones de la interfaz
        self.entries = {}
        self.vars = {}
        self.botones_ver_contrasena = {}
        
        self.ventana_validacion() # Llamada al método de validación de la ventana

    def obtener_ventana(self):
        
        return self.root # Retorna la instancia de la ventana principal
    
    def ventana_validacion(self):
        
        # Definición de los campos que se utilizarán en la ventana de validación
        # Campo para mostrar un mensaje de título
        campos = [
            
            {'label': 'Solicitar\nCódigo de Recuperación', 'tipo': 'label'},
        ]
        
        # Campos para ingresar el email
        campos1 = [
            
            {'clave': 'email','label': 'Email', 'tipo': 'entry', 'ancho': 350, 'alto': 26, 'placeholder': 'Introduce tú Email'},
            
        ]
        
        # Botones para enviar código o salir
        campos2 = [
            
            {"label": "Enviar", "color": "#00155c", "tipo": "boton", "ancho": 50, "alto":50, "command": self.enviar_codigo, 'image': None,},
            {"label": "Salir", "color": "#00155c", "tipo": "boton", "ancho": 50, "alto":50, "command": self.salir, 'image': None,},
        ]       
        
        # Crear los labels de la ventana
        for i, campo in enumerate(campos):
            
            self.crear_label(self.frame, texto=campo['label'], fuente=self.fonts['title'], fila= 0, columna=0)
        
        # Crear los campos de entrada (entry) para el email
        for i, campo1 in enumerate(campos1):
            
            self.crear_label(self.frame_1, campo1['label'], self.fonts['label_title'], fila= i*2+1, columna=0)
            
            if campo1['tipo'] == 'entry':
                
                # Crear un StringVar y el campo de entrada para el email                    
                self.vars[campo1['clave']] = ctk.StringVar()
                
                self.entries[campo1['clave']] = self.crear_entry(self.frame_1,
                                                                font=self.fonts['label'],
                                                                fila = i*2+2,
                                                                columna=0,
                                                                ancho_widget=campo1['ancho'],
                                                                alto_widget=campo1['alto'],
                                                                placeholder=campo1['placeholder'],
                                                            )               
        
        # Crear los botones de la ventana (enviar y salir)     
        for i, campo2 in enumerate(campos2):
            
            self.crear_boton(self.frame_2, self.fonts['boton'], campo2['label'], campo2['color'], 0, i+1, image=campo2['image'], ancho_widget=campo2['ancho'], alto_widget=campo2['alto'], command=campo2['command'])
                
        self.root.after(100, self.entries['email'].focus()) # Focalizar el cursor en el campo de email después de un pequeño retraso
            
    # Generar un código de verificación de 6 dígitos
    def generar_codigo(self):
        
        return str(random.randint(100000, 999999)) # Genera un código aleatorio de 6 dígitos entre 100000 y 999999

    # Enviar correo con código de confirmación
    def enviar_codigo(self):

        # Obtener el valor del campo 'email' del formulario y quitar los espacios innecesarios
        email = self.entries['email'].get().strip()
        
        # Verificar si el campo 'email' está vacío
        if not email:
            
            campos_requeridos() # Si está vacío, llamar a la función que muestra el mensaje de campo requerido
            
            return
        
        # Definir el patrón de expresión regular para validar el formato del email
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Verificar si el email coincide con el patrón
        if not re.match(patron_email, email):
            
            email_formato() # Si el formato del email no es válido, llamar a la función que muestra el mensaje de formato incorrecto
            
            return
        
        # Consulta SQL para verificar si el email existe en la base de datos
        sql_validar_email = "SELECT email FROM usuarios WHERE email = %s"
        
        self.db.cursor.execute(sql_validar_email, (email,))
        
        validacion = self.db.cursor.fetchone() # Obtener el resultado de la consulta
        
        # Si el email está registrado en la base de datos
        if validacion:
    
            codigo = self.generar_codigo() # Generar un código de recuperación

            # Consulta SQL para actualizar el código en la base de datos
            sql_codigo = "UPDATE usuarios SET codigo = %s WHERE email = %s"
            
            self.db.cursor.execute(sql_codigo, (codigo, email))
            
            self.db.conexion.commit() # Confirmar los cambios en la base de datos
            
        else:
            
            email_no_esta() # Si el email no está registrado, mostrar mensaje de error
                
        # Verificar si el código fue realmente guardado en la base de datos
        sql_verificar = "SELECT codigo FROM usuarios WHERE email = %s"
        self.db.cursor.execute(sql_verificar, (email,))
        resultado = self.db.cursor.fetchone()

        # Si el código fue guardado correctamente
        if resultado:
            
            codigo = resultado[0] # Obtener el código generado
            
            # Mostrar mensaje de confirmación
            confirmacion_codigo()
            
            self.root.destroy() # Cerrar la ventana actual
            
            # Abrir la ventana de actualización de contraseña después de cerrar el mensaje
            abrir_ventana_recuperacion_contrasena()
            
        else:
            
            validacion_cuenta() # Si no se pudo guardar el código, mostrar mensaje de error
    
    # Definición de la función 'crear_label' para crear un widget de tipo etiqueta (label) en la interfaz
    def crear_label(self, parent, texto, fuente, fila, columna, ancho = 1, alto = 1):
        
        # Crear una etiqueta (label) usando customtkinter (ctk)
        label = ctk.CTkLabel(parent,
                            text=texto,
                            font=fuente,
                            text_color= "#484a4b"
                            )
        
        # Colocar la etiqueta en el grid (rejilla) del layout de la ventana
        label.grid(row=fila, column=columna, sticky='ew', columnspan=ancho, rowspan=alto, padx = 5)
        
        return label # Retornar el widget de la etiqueta creada para poder usarla más tarde
    
    # Definición de la función 'crear_entry' para crear un widget de tipo campo de texto (entry) en la interfaz
    def crear_entry(self, parent, font, fila, columna, ancho_widget = '', alto_widget = '', placeholder = '', show= ''):
        
        # Crear un campo de texto (entry) usando customtkinter (ctk)
        entry = ctk.CTkEntry(parent,
                            font= font, # Fuente (tipo y tamaño de letra) del campo de texto
                            width= ancho_widget, # Ancho del campo de texto
                            height= alto_widget, # Alto del campo de texto
                            text_color='black', # Color del texto dentro del campo de texto
                            corner_radius=10, # Radio de curvatura de las esquinas del campo de texto
                            fg_color='lightgray', # Color de fondo del campo de texto
                            placeholder_text= placeholder, # Texto de ayuda (placeholder) dentro del campo de texto
                            placeholder_text_color= 'gray', # Color del texto de ayuda (placeholder)
                            show= show # Especifica si debe mostrar un carácter especial
                            )
        
        # Colocar el campo de texto en el grid (rejilla) de la ventana
        entry.grid(row = fila, column = columna, sticky= 'ew', padx = 5)
        
        return entry # Retornar el widget del campo de texto creado para poder usarlo más tarde
    
    # Definición de la función 'crear_boton' para crear un botón en la interfaz gráfica
    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, image, ancho=1, alto=1, ancho_widget = '', alto_widget = '', command=None):
        
        # Crear un botón utilizando customtkinter (ctk)
        boton = ctk.CTkButton(
                                parent, # Ventana o marco donde se agregará el botón
                                font=font, # Fuente (tipo y tamaño de letra) del botón
                                text=texto, # Texto del botón
                                fg_color=color_fondo, # Color de fondo del botón
                                text_color='white', # Color del texto del botón
                                height=alto_widget, # Alto del botón
                                width= ancho_widget, # Ancho del botón
                                command=command, # Acción a realizar cuando se presione el botón
                                corner_radius=10, # Radio de curvatura de las esquinas del botón
                                image=image, # Imagen a mostrar en el botón
                                hover_color= "lightgreen"
                            )
        
        # Colocar el botón en la rejilla de la ventana (grid) en la posición especificada
        boton.grid(row=fila, column=columna, rowspan=alto, columnspan = ancho, padx=5, pady= 5, sticky='nsew')
        
        return boton  # Retornar el botón creado para poder utilizarlo más adelante si es necesario
    
    # Definición de la función 'limpiar_campos' para limpiar los campos de entrada en la interfaz gráfica
    def limpiar_campos(self):
        
        # Limpiar el contenido del campo de entrada de email
        self.entries['email'].delete(0, ctk.END)
        
        self.vars['email'].set('') # Restablecer el valor de la variable asociada al campo 'email' a una cadena vacía

        self.entries['email'].focus() # Focalizar el campo de entrada 'email' para que el cursor esté listo para recibir nuevos datos
    
    # Definición de la función 'salir' que se ejecuta cuando el usuario hace clic en el botón "Salir"
    def salir(self):
        
        """Método personalizado para el botón Salir.
        """
        # Si existe una conexión a la base de datos, se cierra
        if self.db:
            
            self.db.cerrar_conexion()  # Llamamos al método de la clase 'Conexion_DB' para cerrar la conexión con la base de datos
        
        self.root.destroy() # Cierra la ventana actual de la aplicación
        
        # Si hay una ventana principal asociada, la restauramos
        if self.parent_window:
            
            self.parent_window.deiconify() # Muestra nuevamente la ventana principal si estaba minimizada o escondida
            
            self.parent_window.lift() # Asegura que la ventana principal esté por encima de otras ventanas abiertas
