import sys  # Módulo para interactuar con el sistema y modificar rutas de búsqueda de módulos
import os  # Módulo para interactuar con el sistema operativo (rutas, directorios, archivos)
import re# Importar módulo de expresiones regulares
import bcrypt # Importar bcrypt para el manejo de contraseñas cifradas
import customtkinter as ctk # Importar CustomTkinter para la interfaz gráfica

# Agrega al path del sistema el directorio padre del script actual
# Esto permite importar módulos desde un nivel superior en la jerarquía de carpetas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

# Obtener la ruta absoluta del directorio "img"
ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'img'))

from PIL import Image # Importar PIL (Pillow) para la manipulación de imágenes

# Importar la clase de conexión a la base de datos desde el módulo correspondiente
from conexion_DB.conexionDB import Conexion_DB

# Importar funciones para abrir ventanas emergentes desde el módulo correspondiente
from abrirventanasemergentes.abrir_ventanas import (
    
    abrir_ventana_conn_fallida,  # Muestra una ventana si la conexión a la base de datos falla
    abrir_ventana_conn_exito,  # Muestra una ventana si la conexión a la base de datos es exitosa
    usuario_ingresado,  # Indica que un usuario ha ingresado correctamente
    usuario_no_ingresado,  # Indica que un usuario no ha podido ingresar
    campos_requeridos,  # Verifica si se han completado los campos obligatorios
    contrasena_coincide,  # Valida si la contraseña ingresada coincide con la almacenada
    contrasena_formato,  # Verifica el formato de la contraseña
    email_formato,  # Verifica que el email tenga un formato válido
    telefono_extension,  # Valida la extensión del número de teléfono
    modalidad_cargo,  # Verifica la modalidad del cargo del usuario
    usuario_existe,  # Comprueba si un usuario ya está registrado en la base de datos
    cerrar_conexion  # Cierra la conexión con la base de datos
)

class VentanaRegistroUsuario():
    
    def __init__(self, parent_window= None): 
        
        self.parent_window = parent_window # Se guarda la ventana principal (padre) en una variable para referencias posteriores
        
        # Definición del tamaño de la nueva ventana
        ancho_ventana_nueva = 900
        alto_ventana_nueva = 400
        
        # Configuración de la apariencia de la aplicación (modo claro y tema verde)
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        self.root = ctk.CTkToplevel() # Crear una nueva ventana emergente de tipo CTkToplevel
        
        self.root.protocol("WM_DELETE_WINDOW", lambda: None) # Configurar qué sucede cuando se cierra la ventana (en este caso, no hace nada, no funciona el boton de la ventana)
        
        # Calcular las coordenadas para centrar la ventana en la pantalla
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        self.root.title('Registro Usuario') # Establecer el título de la ventana
        
        # Establecer las dimensiones de la ventana y su ubicación en la pantalla
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.resizable(False,False) # Evitar que la ventana se pueda redimensionar
        
        # Intentar conectar a la base de datos y mostrar una ventana de éxito o fracaso
        try:
            
            self.db = Conexion_DB() # Crear una instancia de la clase Conexion_DB
            self.db.conectar() # Intentar realizar la conexión
            abrir_ventana_conn_exito() # Si la conexión es exitosa, abrir una ventana de éxito
            
        except Exception:
            
            abrir_ventana_conn_fallida() # Si ocurre un error, abrir una ventana de error
            
        # Diccionarios para guardar variables y widgets entry
        self.vars = {}
        self.entries = {}
        self.combobox = {}
        self.botones_ver_contrasena = {}
        
        # Cargar imágenes para los iconos de ojo (abierto y cerrado) desde una carpeta
        self.ojo_abierto = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "ojoabierto.png")).resize((50, 50)), size=(50, 50))
        self.ojo_cerrado = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "ojo-cerrado.png")).resize((50, 50)), size=(50, 50))
        
        # Configurar las filas y columnas de la ventana principal para que se adapten al contenido
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Definir un diccionario de fuentes para los distintos elementos de la interfaz      
        self.fonts = {
            
            'title': ('verdana', 26, 'bold'),
            'label_title': ('verdana', 14, 'bold'),
            'label': ('verdana', 12, 'bold'),
            'boton': ('verdana', 14, 'bold'),
        }
        
        # Crear un marco principal para contener otros elementos de la interfaz
        self.frame = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame.grid(row= 0, column= 0, sticky= 'nsew')
        
        # Crear otros marcos para organizar los widgets en la ventana
        self.frame_widgets_sup = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame_widgets_sup.grid(row= 1, column= 0, sticky= 'nsew')
        
        self.frame_widgets_medio = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame_widgets_medio.grid(row= 2, column= 0, sticky= 'nsew')
        
        self.frame_widgets_medio1 = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame_widgets_medio1.grid(row= 3, column= 0, sticky= 'nsew')
        
        self.frame_widgets_inf = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame_widgets_inf.grid(row= 4, column= 0, sticky= 'nsew')
        
        # Configurar las columnas y filas dentro de cada marco para el diseño responsivo
        self.frame.grid_columnconfigure(0, weight= 1)
        self.frame.grid_rowconfigure(0, weight= 1)

        self.frame_widgets_sup.grid_columnconfigure(1, weight= 1)
        self.frame_widgets_sup.grid_columnconfigure(2, weight= 1)
        self.frame_widgets_sup.grid_columnconfigure(3, weight= 1)   
        
        self.frame_widgets_medio.grid_columnconfigure(1, weight= 1)
        self.frame_widgets_medio.grid_columnconfigure(2, weight= 1)
        self.frame_widgets_medio.grid_columnconfigure(3, weight= 1)
        
        self.frame_widgets_medio1.grid_columnconfigure(1, weight= 1)
        self.frame_widgets_medio1.grid_columnconfigure(2, weight= 1)
        self.frame_widgets_medio1.grid_columnconfigure(3, weight= 1)
        
        self.frame_widgets_inf.grid_columnconfigure(1, weight= 1)
        self.frame_widgets_inf.grid_columnconfigure(2, weight= 0)
        self.frame_widgets_inf.grid_columnconfigure(3, weight=1)
        self.frame_widgets_inf.grid_rowconfigure(0, weight= 1)

        # Llamar a la función que configura los elementos dentro de la ventana
        self.datos_ventana()
        
    def obtener_ventana(self):
        
        # Devuelve la ventana principal (root) de la clase
        # Esto permite acceder a la ventana desde fuera de la clase si es necesario
        return self.root
    
    def datos_ventana(self):
        
        # Definir campos para la ventana de registro del usuario
        # Campos para el encabezado
        campos = [
            
            {'label':'Bienvenido\nRegistro De Usuario'}
        ]
        
        # Campos para los datos del usuario: nombre, identificación, email
        campos1 = [
            
            {'clave':'nombre_usuario','label':'Nombre', 'ancho': 300, 'tipo':'entry', 'alto':26, 'placeholder':'Ingresa el Nombre'},
            {'clave':'identificacion','label':'Identificación', 'ancho': 150, 'tipo':'entry', 'alto':26, 'placeholder':'Identificación Usuario'},
            {'clave':'email','label':'Email', 'ancho': 300, 'tipo':'entry', 'alto':26, 'placeholder':'Ingresa el Email'},
            
        ]
        
        # Campos para la contraseña y teléfono
        campos2 = [
            
            {'clave':'contrasena','label':'Contraseña', 'ancho': 200, 'tipo':'entry', 'alto':26, 'placeholder':'Ingresa Una Contraseña'},
            {'clave':'rep_contrasena','label':'Repetir Contraseña', 'ancho': 200, 'tipo':'entry', 'alto':26, 'placeholder':'Repite la Contraseña'},
            {'clave':'telefono','label':'Telefono', 'ancho': 150, 'tipo':'entry', 'alto':26, 'placeholder':'Telefono Empresa'},
        ]
        
        # Campos para la extensión, modalidad y cargo
        campos3 = [
            
            {'clave':'extension','label':'Extensión', 'ancho': 80, 'tipo':'entry', 'alto':26, 'placeholder':'Extensión Empresa'},
            {'clave':'modalidad',"label": "Modalidad", "valor": "Alfaguara", "ancho": 200, "tipo": "combobox", "opciones": self.obtener_modalidades()},
            {'clave':'cargo',"label": "cargo", "valor": "Alfaguara", "ancho": 200, "tipo": "combobox", "opciones": self.obtener_cargos()},
        ]
        
        # Campos para los botones de acción
        campos4 = [
            
            {"label": "Registrarse", "color": "#00155c", "tipo": "boton", "ancho": 60, "alto":40, "command": self.insertar_usuario, 'image':None},
            {"label": "", "color": "transparent", "tipo": "boton", "ancho": 50, "alto":50, "command": self.alternar_contrasena, 'image': self.ojo_abierto, "clave": "ver_contrasena"},
            {"label": "Salir", "color": "#00155c", "tipo": "boton", "ancho": 60, "alto":40, "command": self.salir, 'image':None},
        ]
        
        # Crear la etiqueta del título en la ventana
        for i, campo in enumerate(campos):
            
            self.crear_label(self.frame, font=self.fonts['title'], texto=campo['label'],fila= 0, columna= i)

        # Iterar sobre los campos de entrada, contraseñas, teléfono, etc., y crear las etiquetas y campos correspondientes
        for i, (campo1, campo2, campo3) in enumerate(zip(campos1, campos2, campos3)):
            
            # Crear etiquetas para cada campo
            self.crear_label(self.frame_widgets_sup, 
                            font=self.fonts['label_title'], 
                            texto=campo1['label'], 
                            fila=0, 
                            columna=i+1
                            )
            
            self.crear_label(self.frame_widgets_medio, 
                            font=self.fonts['label_title'], 
                            texto=campo2['label'], 
                            fila=0, 
                            columna=i+1
                            )
            
            self.crear_label(self.frame_widgets_medio1, 
                            font=self.fonts['label_title'], 
                            texto=campo3['label'], 
                            fila=0, 
                            columna=i+1
                            )

            # Crear variables de control para los entries y asignar la función de verificación de contraseñas
            for campo, frame in zip([campo1, campo2, campo3], [self.frame_widgets_sup, self.frame_widgets_medio, self.frame_widgets_medio1]):
                
                if campo['tipo'] == 'entry':
                    
                    if campo['clave'] in ['contrasena', 'rep_contrasena']:
                        
                        self.vars[campo['clave']] = ctk.StringVar()
                        
                        self.entries[campo['clave']] = self.crear_entry(
                            frame, 
                            font=self.fonts['label'], 
                            fila=1, 
                            columna=i+1, 
                            ancho_widget=campo['ancho'], 
                            alto_widget=campo['alto'], 
                            placeholder=campo['placeholder'],
                            textvariable = self.vars[campo['clave']],
                            show='*', # Para contraseñas, el campo se muestra con asteriscos
                        )
                        
                    else:
                        
                        self.vars[campo['clave']] = ctk.StringVar()
                        
                        self.entries[campo['clave']] = self.crear_entry(
                            frame, 
                            font=self.fonts['label'], 
                            fila=1, 
                            columna=i+1, 
                            ancho_widget=campo['ancho'], 
                            alto_widget=campo['alto'], 
                            placeholder=campo['placeholder'],
                            textvariable = self.vars[campo['clave']],
                        )

                if campo['clave'] in ['nombre_usuario', 'identificacion', 'contrasena', 'email', 'telefono', 'extension']:
                    
                    # Añadir un trace a las entradas para actualizar el título
                    self.vars[campo['clave']].trace_add("write", self.actualizar_a_title)

                # Crear comboboxes para modalidad y cargo
                if campo3['tipo'] == 'combobox':
                    
                    self.vars[campo3['clave']] = ctk.StringVar()
                    
                    self.combobox[campo3['clave']] = self.crear_combobox(
                        self.frame_widgets_medio1,
                        self.fonts['label'],
                        fila=1,
                        columna=i+1,
                        ancho_widget=campo3["ancho"],
                        opciones=campo3.get("opciones", []),
                        valor_predeterminado=campo3["valor"]
                    )
        
        # Crear botones de acción (registrarse, alternar contraseña, salir)
        for i, campo in enumerate(campos4):
        
            boton = self.crear_boton(self.frame_widgets_inf, 
                                    self.fonts['boton'], 
                                    campo['label'], 
                                    campo['color'], 
                                    0, 
                                    i+1, 
                                    campo['alto'], 
                                    campo['ancho'], 
                                    image=campo['image'], 
                                    command=campo['command']
                                    )

            if "clave" in campo:
                self.botones_ver_contrasena["ver_contrasena"] = boton

        # Definir la consulta SQL para insertar un nuevo usuario en la base de datos
        self.sql_insertar = "INSERT into usuarios (nombre_usuario, identificacion, contrasena, email, telefono, ext, modalidad, cargo) values (%s,%s,%s,%s,%s,%s,%s,%s)"      
        
    def actualizar_a_title(self, *args):
        
        """
        Callback que actualiza los valores de ciertos campos a formato Title.
        """
        # Campos que deben ser actualizados a formato Title
        for clave in ['nombre_usuario', 'identificacion', 'modalidad', 'cargo']:
            
            # Verificar si la clave está presente en las variables de control
            if clave in self.vars:
                
                texto = self.vars[clave].get() # Obtener el texto actual de la variable
                
                texto_title = texto.title() # Convertir el texto a formato Title
                
                # Si el texto original es diferente del texto en formato Title, actualizar la variable
                if texto != texto_title:
                    
                    self.vars[clave].set(texto_title)
    
    def insertar_usuario(self):
        
        """
        Inserta un nuevo usuario en la base de datos luego de realizar las validaciones correspondientes.

        Esta función realiza las siguientes acciones:
        1. Obtiene los datos ingresados por el usuario en los campos de entrada (nombre de usuario, identificación, contraseña, etc.).
        2. Valida que todos los campos requeridos estén completos.
        3. Verifica que las contraseñas coincidan y estén en el formato correcto.
        4. Valida que el correo electrónico tenga el formato adecuado.
        5. Asegura que los campos de teléfono y extensión solo contengan números.
        6. Encripta la contraseña utilizando bcrypt para garantizar la seguridad.
        7. Verifica que la modalidad y el cargo sean válidos.
        8. Revisa si el nombre de usuario ya existe en la base de datos.
        9. Si el usuario no existe, inserta los datos en la base de datos.
        10. Limpia los campos solo si la inserción fue exitosa.

        Si alguna de las validaciones falla, muestra un mensaje de error adecuado.
        """
        # Obtener las modalidades disponibles desde la base de datos
        self.obtener_modalidades()
        
        # Obtener los datos ingresados
        nombreusuario = self.entries['nombre_usuario'].get().strip()
        identificacion = self.entries['identificacion'].get().strip()
        contrasena = self.entries['contrasena'].get().strip()
        rep_contrasena = self.entries['rep_contrasena'].get().strip()
        email = self.entries['email'].get().strip()
        telefono = self.entries['telefono'].get().strip()
        ext = self.entries['extension'].get().strip()
        modalidad = self.combobox['modalidad'].get().strip()
        cargo = self.combobox['cargo'].get().strip()
        
        # Validar que todos los campos estén completos
        if not all([nombreusuario, identificacion, contrasena, email, telefono, ext, modalidad, cargo]):
            
            campos_requeridos()
            
            return 

        # Validar la contraseña antes de continuar
        if not self.validar_contrasena(contrasena, rep_contrasena):
            
            return

        # Validar formato del correo electrónico
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(patron_email, email):
            
            email_formato()
            
            return

        # Validar que teléfono y extensión solo contengan números
        if not telefono.isdigit() or not ext.isdigit():
            
            telefono_extension()
            
            return 

        # contraseña con bcrypt para encriptarla
        salt = bcrypt.gensalt()
        contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), salt)

        # Obtener el ID de modalidad y cargo
        id_modalidad = self.opciones.get(modalidad)
        id_cargo = self.mapeo_cargos.get(cargo)

        if not id_modalidad or not id_cargo:
            
            modalidad_cargo()
            
            return 

        # Verificar si el usuario ya existe
        consulta_existencia = "SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = %s"
        self.db.cursor.execute(consulta_existencia, (nombreusuario,))
        resultado = self.db.cursor.fetchone()

        if resultado[0] > 0:
            
            usuario_existe()
            
            return

        try:

            # Insertar nuevo usuario
            sql_insert = "INSERT INTO usuarios (nombre_usuario, identificacion, contrasena, email, telefono, ext, modalidad, cargo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            self.db.cursor.execute(sql_insert, (nombreusuario, identificacion, contrasena_hash, email, telefono, ext, id_modalidad, id_cargo))
            self.db.conexion.commit()

            usuario_ingresado()
        
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            usuario_no_ingresado()

        # Limpiar los campos solo si la inserción fue exitosa
        for key in self.vars:
            
            self.vars[key].set("")
    
    def obtener_cargos(self):
        
        """Obtiene los nombres de los cargos desde la base de datos y mapea sus IDs."""

        # Ejecuta la consulta SQL para obtener los cargos desde la base de datos
        self.db.cursor.execute("SELECT id_cargo, nombre_cargo FROM cargos") 
        cargos = self.db.cursor.fetchall()

        # Crear un diccionario que mapea el nombre del cargo a su ID
        self.mapeo_cargos = {nombre: id_cargo for id_cargo, nombre in cargos}

        # Retornar solo los nombres de los cargos para el combobox
        return list(self.mapeo_cargos.keys())

    def obtener_modalidades(self):
        
        """Obtiene los nombres de las modalidades desde la base de datos."""
        
        # Ejecuta la consulta SQL para obtener las modalidades desde la base de datos
        self.db.cursor.execute("SELECT id_modalidad, nombre_modalidad, abreviacion FROM modalidades")  
        modalidades = self.db.cursor.fetchall()
        
        # Crear un diccionario que mapea el nombre de la modalidad (con la abreviación) a su ID
        self.opciones = {f'{nombre_modalidad} ({abreviacion})': id_modalidad for id_modalidad, nombre_modalidad, abreviacion in modalidades}

        # Retornar solo los nombres de las modalidades (con abreviación) para ser usados en el combobox
        return list(self.opciones.keys())
    
    def crear_label(self,parent, font, texto, fila, columna,ancho=1, alto = 1):
        
        """Crea un label en el GUI y lo coloca en una posición específica dentro de un grid."""
        
        # Crear el label con el texto y la fuente especificados
        label = ctk.CTkLabel(parent,
                            font = font,
                            text = texto,
                            text_color= "#484a4b"
                            )
        
        # Colocar el label en el grid del contenedor (parent) en la fila y columna especificadas
        # Se ajusta su tamaño con los parámetros 'ancho' y 'alto', y se utiliza 'nsew' para que ocupe todo el espacio disponible
        label.grid(row = fila, column = columna, sticky = 'nsew', columnspan = ancho, rowspan = alto)
        
        # Retorna el objeto label creado para manipulaciones posteriores
        return label
    
    def crear_entry(self, parent, font, fila, columna, ancho = 1, alto = 1, ancho_widget = 150, alto_widget = 26, placeholder='', textvariable= '', show= ''):
        
        """Crea un campo de entrada (entry) en el GUI y lo coloca en una posición específica dentro de un grid."""

        # Crear un entry con las propiedades y configuraciones proporcionadas
        entry = ctk.CTkEntry(parent,
                            font=font,  # Establecer la fuente del texto en el entry
                            width=ancho_widget,  # Ancho del widget (campo de entrada)
                            height=alto_widget,  # Alto del widget
                            text_color='black',  # Color del texto
                            corner_radius=10,  # Radio de las esquinas para bordes redondeados
                            fg_color='lightgray',  # Color de fondo del entry
                            placeholder_text=placeholder,  # Texto del placeholder cuando el campo está vacío
                            placeholder_text_color='gray',  # Color del texto del placeholder
                            textvariable=textvariable,  # Variable de control para el texto que se ingresa
                            show=show  # Caracter a mostrar en el campo 
                            )
        
        # Colocar el entry en el grid dentro del contenedor (parent), en la fila y columna especificadas
        entry.grid(row = fila, column = columna, sticky = 'nsew', padx = 5, columnspan= ancho, rowspan = alto)
        
        # Retorna el objeto entry creado para manipulaciones posteriores
        return entry
    
    def crear_combobox(self,parent, font, fila, columna, alto_widget=26, ancho_widget=130, ancho=1, opciones=None, valor_predeterminado=''):
        
        """Crea un combobox (menú desplegable) en el GUI y lo coloca en una posición específica dentro de un grid."""

        # Si no se pasan opciones, inicializa una lista con un solo valor 'Ninguna'
        if opciones is None:
            opciones = ['Ninguna']
        
        # Crear el combobox (menú desplegable) con las propiedades y configuraciones proporcionadas
        combobox = ctk.CTkOptionMenu(
            parent,  # El contenedor donde se coloca el combobox
            font=font,  # Establecer la fuente del texto en el combobox
            text_color='black',  # Color del texto en el combobox
            corner_radius=10,  # Radio de las esquinas para bordes redondeados
            width=ancho_widget,  # Ancho del combobox
            height=alto_widget,  # Alto del combobox
            fg_color='lightgray',  # Color de fondo del combobox
            values=opciones,  # Lista de opciones que se mostrarán en el combobox
            button_color= "lightgray",
            button_hover_color= "lightgreen"
        )
        
        # Establecer el valor predeterminado si está en las opciones
        if valor_predeterminado in opciones:
            
            combobox.set(valor_predeterminado)
            
        elif opciones:  # Si no está el valor predeterminado, seleccionar la primera opción
            
            combobox.set(opciones[0])
            
        # Configurar el combobox para que solo pueda seleccionar entre las opciones (sin posibilidad de escribir)
        combobox.configure(state='readonly')
        
        # Colocar el combobox en el grid en la fila y columna especificada
        combobox.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto_widget, padx=5, sticky='nsew')
        
        # Retornar el objeto combobox creado para manipulaciones posteriores
        return combobox
    
    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, ancho, alto, image, command=None):
        
        # Define una función para crear un botón personalizado con los parámetros proporcionados
        
        boton = ctk.CTkButton( # Crea un botón usando la clase CTkButton de CustomTkinter
            parent, # Widget padre donde se colocará el botón
            font=font, # Fuente del texto del botón
            text=texto, # Texto que se mostrará en el botón
            fg_color=color_fondo, # Color de fondo del botón
            text_color='white', # Color del texto del botón
            height=alto,  # Altura del botón
            width= ancho,  # Anchura del botón
            command=command, # Función que se ejecutará al presionar el botón
            corner_radius=10, # Radio de las esquinas del botón (bordes redondeados)
            image=image, # Imagen que se mostrará en el botón (si se proporciona)
            hover_color= "lightgreen"
        )
        boton.grid(row=fila, column=columna, padx=5, pady=5, sticky='nsew')
        # Coloca el botón en una cuadrícula, en la fila y columna especificadas
                
        return boton  # Retorna el botón creado para poder usarlo fuera de la función
    
    # # Función para alternar la visibilidad de las contraseñas
    def alternar_contrasena(self):
        
        # Alternar visibilidad de "contrasena" y "rep_contrasena"
        for campo in ["contrasena", "rep_contrasena"]:
            
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
            nuevo_icono = self.ojo_abierto if self.entries["contrasena"].cget("show") == '*' else self.ojo_cerrado
            
            # Cambiar la imagen del botón
            boton.configure(image=nuevo_icono)

            # Guardar la imagen en el botón para evitar que la referencia se pierda
            boton.image = nuevo_icono  # IMPORTANTE: evita que la imagen se elimine por el recolector de basura

    def validar_contrasena(self, contrasena, rep_contrasena):
        
        # Define una función para validar que las contraseñas coincidan y cumplan con ciertos requisitos

        """
        Valida que las contraseñas coincidan y cumplan con los requisitos de formato.
        """
        
        # Validar que ambas contraseñas coincidan
        if contrasena != rep_contrasena:
            
            # Si las contraseñas no son iguales, se llama a una función que informa el error
            contrasena_coincide()

            return False # Retorna False indicando que la validación falló

        # Expresión regular para validar la contraseña
        regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,20}$"

        if not re.match(regex, contrasena):
            
            # Si la contraseña no cumple con el formato, se llama a una función que informa el error
            contrasena_formato()
            
            return False # Retorna False indicando que la validación falló

        return True # Retorna True si las contraseñas coinciden y tienen el formato correcto
    
    def salir(self):
            """Método personalizado para el botón Salir.
            Cierra la ventana y restablece la ventana."""
            
            if self.db:
                
                self.db.cerrar_conexion()  # Llamamos al método de cerrar conexión
                
                cerrar_conexion()
            
            self.root.destroy()  # Cierra la ventana
            
            if self.parent_window:
                
                self.parent_window.deiconify()
                self.parent_window.lift()
