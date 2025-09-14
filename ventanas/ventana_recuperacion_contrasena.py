# Importar módulos estándar del sistema
import sys
import os
import customtkinter as ctk # Importar CustomTkinter para la interfaz gráfica
import bcrypt # Importar bcrypt para el manejo de contraseñas seguras
import re # Importar re para trabajar con expresiones regulares

# Agregar el directorio padre al sys.path para importar módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Obtener la ruta absoluta del directorio "img"
ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'img'))

# Importar la conexión a la base de datos
from conexion_DB.conexionDB import Conexion_DB
from PIL import Image

# Importar funciones de ventanas emergentes
from abrirventanasemergentes.abrir_ventanas import (abrir_ventana_conn_exito,
                                                    abrir_ventana_conn_fallida,
                                                    campos_requeridos,
                                                    email_formato,
                                                    email_no_esta,
                                                    contrasena_guardada,
                                                    contrasena_no_guardada,
                                                    contrasena_coincide, 
                                                    contrasena_formato,
                                                    codigo_no_esta,
                                                    email_validado,
                                                    validacion_completa,
                                                    email_no_validado
                                                    )
                                                    
class RecuperacionContrasena():
    
    def __init__(self, parent_window = None):
        
        # Almacenar la ventana padre si se proporciona
        self.parent_window = parent_window
        
        # Definir dimensiones de la nueva ventana
        ancho_ventana_nueva = 500
        alto_ventana_nueva = 350
        
        # Configurar apariencia y tema de la interfaz
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        # Crear una ventana emergente (Toplevel)
        self.root = ctk.CTkToplevel()
        
        self.root.protocol("WM_DELETE_WINDOW", lambda: None) # Evitar el cierre de la ventana con la "X"
        
        # Calcular la posición para centrar la ventana en la pantalla
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        # Establecer tamaño y posición de la ventana
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.title('Recuperación Contraseña') # Configurar el título de la ventana
        
        self.root.iconbitmap('img/documento.ico') # Establecer el icono de la ventana
        
        self.root.resizable(False, False) # Evitar que la ventana sea redimensionable
        
        # Configurar las filas de la cuadrícula para distribuir los elementos
        self.root.grid_columnconfigure(0, weight=1)
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
        
        # Intentar establecer la conexión con la base de datos
        try:
            
            self.db = Conexion_DB()
            self.db.conectar()
            abrir_ventana_conn_exito() # Mostrar mensaje de conexión exitosa
            
        except Exception:
            
            abrir_ventana_conn_fallida() # Mostrar mensaje de error en la conexión
        
        # Definir estilos de fuente para los textos
        self.fonts = {
            
            'title': ('verdana', 26,  'bold'),
            'label_title': ('verdana', 14,  'bold'),
            'label': ('verdana', 12,  'bold'),
            'boton': ('verdana', 14,  'bold')
        }
        
        # Crear los frames de la interfaz
        self.frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame.grid(row= 0, column = 0, sticky = 'nsew')
        
        self.frame_1 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame_1.grid(row= 1, column = 0, sticky = 'nsew')
        
        self.frame_2 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame_2.grid(row= 2, column = 0, sticky = 'nsew')
        
        # Configurar el diseño de los frames
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        self.frame_1.grid_columnconfigure(0, weight=1)
        
        self.frame_2.grid_columnconfigure(1, weight=1)
        self.frame_2.grid_columnconfigure(2, weight=1)
        self.frame_2.grid_columnconfigure(3, weight=0)
        self.frame_2.grid_columnconfigure(4, weight=1)
        self.frame_2.grid_rowconfigure(0, weight=1)
        
        # Diccionarios para almacenar entradas, variables y botones de visibilidad de contraseña
        self.entries = {}
        self.vars = {}
        self.botones_ver_contrasena = {}
        
        # Variable para verificar si el correo ha sido validado
        self.email_validado = False
        
        # Cargar imágenes de los iconos de visibilidad de contraseña
        self.ojo_abierto = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "ojoabierto.png")).resize((50, 50)), size=(50, 50))
        self.ojo_cerrado = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "ojo-cerrado.png")).resize((50, 50)), size=(50, 50))
        
        # Llamar al método que construye la interfaz de recuperación de contraseña
        self.ventana_recuperacion_contrasena()

    def obtener_ventana(self):
        
        return self.root # Devuelve la ventana principal de la clase.
    
    def ventana_recuperacion_contrasena(self):
        
        """
        Crea y configura la interfaz de recuperación de contraseña.
        """
        
        # Definición de los elementos de la interfaz
        campos = [
            
            {'label': 'Recuperación De\nContraseña', 'tipo': 'label'},
        ]
        
        campos1 = [
            
            {'clave': 'email','label': 'Email', 'tipo': 'entry', 'ancho': 350, 'alto': 26, 'placeholder': 'Introduce tú Email'},
            {'clave': 'nueva_contrasena','label': 'Nueva Contraseña', 'tipo': 'entry', 'ancho': 350, 'alto': 26, 'placeholder': 'Introduce tú Nueva Contraseña'},
            {'clave': 'rep_nueva_contrasena','label': 'Repite La Nueva Contraseña', 'tipo': 'entry', 'ancho': 350, 'alto': 26, 'placeholder': 'Repite tú Nueva Contraseña'},
            
        ]
        
        campos2 = [
            
            {"label": "Registrar\nContraseña", "color": "#00155c", "tipo": "boton", "ancho": 50, "alto":10, "command": self.actualizar_contrasena, 'image': None,},
            {"label": "Validar\nEmail", "color": "#00155c", "tipo": "boton", "ancho": 50, "alto":10, "command": self.validar_email_para_recuperacion, 'image': None,},
            {"label": "", "color": "transparent", "tipo": "boton", "ancho": 50, "alto":50, "command": self.alternar_contrasena, 'image': self.ojo_abierto, "clave": "ver_contrasena"},
            {"label": "Salir", "color": "#00155c", "tipo": "boton", "ancho": 50, "alto":10, "command": self.salir, 'image': None,},
        ]       
        
        # Creación de etiquetas
        for i, campo in enumerate(campos):
            
            self.crear_label(self.frame, texto=campo['label'], fuente=self.fonts['title'], fila= 0, columna=0)
        
        # Creación de entradas 
        for i, campo1 in enumerate(campos1):
            
            self.crear_label(self.frame_1, campo1['label'], self.fonts['label_title'], fila= i*2+1, columna=0)
            
            if campo1['tipo'] == 'entry':
                    
                self.vars[campo1['clave']] = ctk.StringVar()

                self.entries[campo1['clave']] = self.crear_entry(
                    self.frame_1, 
                    font=self.fonts['label'], 
                    fila=i*2+2, 
                    columna=0, 
                    ancho_widget=campo1['ancho'], 
                    alto_widget=campo1['alto'], 
                    placeholder=campo1['placeholder'], 
                    show='*' if campo1['clave'] in ['nueva_contrasena', 'rep_nueva_contrasena'] else ''
                )
                
                # Deshabilitar los campos de contraseña al inicio
                if campo1['clave'] in ['nueva_contrasena', 'rep_nueva_contrasena']:
                    self.entries[campo1['clave']].configure(state="disabled")                      
        
        # Creación de botones      
        for i, campo2 in enumerate(campos2):
            
            boton = self.crear_boton(self.frame_2, 
                                    self.fonts['boton'],
                                    campo2['label'],
                                    campo2['color'],
                                    0,
                                    i+1,
                                    image=campo2['image'],
                                    ancho_widget=campo2['ancho'],
                                    alto_widget=campo2['alto'],
                                    command=campo2['command']
                                    )

            if "clave" in campo2:
                self.botones_ver_contrasena["ver_contrasena"] = boton
        
        # Establecer el foco en el campo de email después de 100ms      
        self.root.after(100, self.entries['email'].focus())
            
    def validar_email_para_recuperacion(self):
        
        email = self.entries['email'].get().strip()

        # Validar que el campo no esté vacío
        if not email:
            campos_requeridos()
            return None

        # Validar formato del correo electrónico
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_email, email, re.IGNORECASE):
            email_formato()
            return None

        try:
            # Buscar el email en la base de datos
            sql_buscar_codigo = "SELECT id_usuario, codigo FROM usuarios WHERE email = %s"
            self.db.cursor.execute(sql_buscar_codigo, (email,))
            resultado = self.db.cursor.fetchone()

            if resultado is None:
                email_no_esta()
                return None

            id_usuario, codigo = resultado

            if codigo is None:
                codigo_no_esta()
                return None

            # Si pasa todas las validaciones
            self.email_validado = True
            
            email_validado()

            # Habilitar campos de nueva contraseña
            for clave in ['nueva_contrasena', 'rep_nueva_contrasena']:
                self.entries[clave].configure(state="normal")

            return id_usuario  # Retorna el ID del usuario si todo está correcto

        except Exception:
            
            email_no_validado()
            
            return None

    def actualizar_contrasena(self):
        
        # Verificar si el correo ha sido validado antes de continuar con la actualización
        if not self.email_validado:  # Verifica si el correo no ha sido validado
            
            validacion_completa() # Informa al usuario que la validación debe completarse primero
            
            return 
        
        # Obtener los valores introducidos por el usuario en los campos de la ventana
        email = self.entries['email'].get().strip()
        contrasena = self.entries['nueva_contrasena'].get().strip()
        rep_contrasena = self.entries['rep_nueva_contrasena'].get().strip()
        
        # Verificar que todos los campos obligatorios estén completos
        if not email or not contrasena or not rep_contrasena:
            
            campos_requeridos() # Muestra un mensaje si falta algún campo obligatorio
            
            return
        
        # Validar que las contraseñas coincidan
        if not self.validar_contrasena(contrasena, rep_contrasena):
            
            return # Si no coinciden, detiene la ejecución

        # Encriptar la nueva contraseña con bcrypt
        salt = bcrypt.gensalt()
        contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), salt).decode('utf-8')

        # Intentar actualizar la contraseña en la base de datos
        try:
            # Definir la consulta para actualizar la contraseña en la base de datos
            sql_actualizar_contrasena = "UPDATE usuarios SET contrasena = %s, codigo = NULL WHERE email = %s"
            self.db.cursor.execute(sql_actualizar_contrasena, (contrasena_hash, email))
            self.db.conexion.commit()  # Confirmar los cambios realizados en la base de datos

            contrasena_guardada() # Notificar al usuario que la contraseña ha sido actualizada con éxito
            
            self.limpiar_campos() # Limpiar los campos de entrada después de guardar la contraseña
                    
            return

        except Exception:
            
            contrasena_no_guardada() # Informar al usuario si hubo un error al guardar la contraseña
            
            return

    def crear_label(self, parent, texto, fuente, fila, columna, ancho = 1, alto = 1):
        
        # Crear un widget de etiqueta (label) con el texto y la fuente especificados
        label = ctk.CTkLabel(parent,
                            text=texto,
                            font=fuente,
                            text_color= "#484a4b"
                            )
        
        # Colocar el label en la cuadrícula (grid) con las configuraciones de fila, columna, tamaño y espaciado
        label.grid(row=fila, column=columna, sticky='ew', columnspan=ancho, rowspan=alto, padx = 5)
        
        return label # Retornar el objeto label creado
    
    def crear_entry(self, parent, font, fila, columna, ancho_widget = '', alto_widget = '', placeholder = '', show= ''):
        
        # Crear un widget de entrada (entry) con las configuraciones especificadas (fuente, tamaño, color, etc.)
        entry = ctk.CTkEntry(parent,
                            font= font,
                            width= ancho_widget,
                            height= alto_widget,
                            text_color='black',
                            corner_radius=10,
                            fg_color='lightgray',
                            placeholder_text= placeholder,
                            placeholder_text_color= 'gray',
                            show= show
                            )
        
        # Colocar el entry en la cuadrícula (grid) con las configuraciones de fila, columna, y espaciado
        entry.grid(row = fila, column = columna, sticky= 'ew', padx = 5)
        
        return entry # Retornar el objeto entry creado
    
    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, image, ancho=1, alto=1, ancho_widget = '', alto_widget = '', command=None):
        
        # Crear un botón con las configuraciones especificadas (fuente, texto, color, tamaño, etc.)
        boton = ctk.CTkButton(
                                parent,
                                font=font,
                                text=texto,
                                fg_color=color_fondo,
                                text_color='white',
                                height=alto_widget,
                                width= ancho_widget,
                                command=command,
                                corner_radius=10,
                                image=image,
                                hover_color= "lightgreen"
                            )
        
        # Colocar el botón en la cuadrícula (grid) con las configuraciones de fila, columna, y espaciado
        boton.grid(row=fila, column=columna, rowspan=alto, columnspan = ancho, padx=5, pady= 15, sticky='nsew')
        
        return boton # Retornar el objeto botón creado
    
    def alternar_contrasena(self):
        
        # Alternar visibilidad de "contrasena" y "rep_contrasena"
        for campo in ["nueva_contrasena", "rep_nueva_contrasena"]:
            if campo in self.entries:  # Verifica que la clave existe en el diccionario
                entry = self.entries[campo]
                if entry.cget('show') == '*':  # Si la contraseña está oculta
                    entry.configure(show='')  # Mostrar la contraseña
                else:  # Si la contraseña ya está visible
                    entry.configure(show='*')  # Ocultar la contraseña
        
        # Verificar si el botón de alternar contraseña existe en el diccionario
        if "ver_contrasena" in self.botones_ver_contrasena:
            boton = self.botones_ver_contrasena["ver_contrasena"]
            
            # Determinar el nuevo icono basado en el estado actual del primer entry
            nuevo_icono = self.ojo_abierto if self.entries["nueva_contrasena"].cget("show") == '*' else self.ojo_cerrado
            
            # Cambiar la imagen del botón
            boton.configure(image=nuevo_icono)

            # Guardar la imagen en el botón para evitar que la referencia se pierda
            boton.image = nuevo_icono  # IMPORTANTE: evita que la imagen se elimine por el recolector de basura

    def validar_contrasena(self, contrasena, rep_contrasena):
        
        # Validar que ambas contraseñas coincidan
        if contrasena != rep_contrasena:
            
            contrasena_coincide()
            
            return False

        # Expresión regular para validar la contraseña
        regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,20}$"

        # Verificar que la contraseña cumple con el formato de la expresión regular
        if not re.match(regex, contrasena):
            
            contrasena_formato()
            
            return False

        return True # Si la contraseña pasa ambas validaciones, retornar True
    
    def limpiar_campos(self):
        
        # Limpiar los campos de entrada
        self.entries['email'].delete(0, ctk.END) # Eliminar texto del campo 'email'
        self.entries['nueva_contrasena'].delete(0, ctk.END) # Eliminar texto del campo 'nueva_contrasena'
        self.entries['rep_nueva_contrasena'].delete(0, ctk.END) # Eliminar texto del campo 'rep_nueva_contrasena'
        
        # Restablecer los valores de las variables asociadas a los campos
        self.vars['email'].set('')
        self.vars['nueva_contrasena'].set('')
        self.vars['rep_nueva_contrasena'].set('')
        
        self.entries['email'].focus() # Establecer el foco en el campo 'email'
    
    def salir(self):
        
            """Método personalizado para el botón Salir.
            """
            # Verificar si la conexión a la base de datos está abierta y cerrarla
            if self.db:
                
                self.db.cerrar_conexion()
            
            self.root.destroy() # Cerrar la ventana actual
            
            # Si existe una ventana principal (parent_window), restaurarla y traerla al frente
            if self.parent_window:
                
                self.parent_window.deiconify() # Hacer visible la ventana principal
                
                self.parent_window.lift() # Llevar la ventana principal al frente
