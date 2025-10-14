import sys # Importa el módulo sys, que proporciona acceso a funciones y variables del sistema.
import os # Importa el módulo os, que permite interactuar con el sistema operativo, como manejar rutas de archivos.
import mysql.connector

# Agrega el directorio padre al sys.path para poder importar módulos desde otros directorios del proyecto.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

# Obtener la ruta absoluta del directorio "img"
ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'img'))

from PIL import Image # Importa la clase Image de la biblioteca Pillow para manipulación de imágenes

from conexion_DB.conexionDB import Conexion_DB # Importa la clase Conexion_DB desde el módulo conexion_DB.conexionDB para la conexión con la base de datos

import customtkinter as ctk # Importa la biblioteca CustomTkinter y la asigna al alias 'ctk' para facilitar su uso.

from verificar_datos_db.verificar_datos import cargar_datos_db

# Importa funciones específicas del módulo 'abrir' dentro del paquete 'abrirventanas', 
# cada una de estas funciones abre una ventana diferente en la aplicación.
from abrirventanas.abrir import (abrir_ventana_alergias, 
                                abrir_ventana_aislamiento,
                                abrir_ventana_rango_edad, 
                                abrir_ventana_estudio_ordenado,
                                abrir_ventana_modalidad,
                                abrir_ventana_estados,
                                abrir_ventana_sedes,
                                abrir_ventana_ratrasos,
                                abrir_ventana_cargos,
                                abrir_ventana_usuarios_admon,
                                abrir_ventana_inicio,
                                abrir_ventana_pacientes_admon
                                )

from abrirventanasemergentes.abrir_ventanas import admon_debes_hacer_primero, abrir_ventana_conn_exito, abrir_ventana_conn_fallida, cerrar_conexion

class VentanaAdmon():
    
    def __init__(self):
        
        self.botones =[]
        
        # Define el ancho y alto de la nueva ventana.
        ancho_ventana_nueva = 600
        alto_ventana_nueva = 500
        
        ctk.set_appearance_mode('light') # Establece el modo de apariencia de la interfaz en "light" (claro).
        ctk.set_default_color_theme('green') # Establece el tema de color por defecto en "green" (verde).
        
        self.root = ctk.CTk() # Crea una nueva ventana con la biblioteca CustomTkinter.
        
        self.root.protocol("WM_DELETE_WINDOW", lambda: None) # Evita que la ventana se cierre al hacer clic en el botón de cierre.
        
        # Calcula la posición para centrar la ventana en la pantalla.
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)  
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        # Establece el tamaño y posición de la ventana en el centro de la pantalla.
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.title('Ventana Admnistrador') # Establece el título de la ventana.
        
        self.root.iconbitmap('img/documento.ico') # Establece el icono de la ventana.
        
        self.root.resizable(False,False) # Evita que la ventana se redimensione.
        
        try:
            
            # Intentar establecer la conexión con la base de datos
            self.db = Conexion_DB()
            self.db.conectar()
            abrir_ventana_conn_exito() # Abrir ventana indicando que la conexión fue exitosa
        
        except Exception:
            
            abrir_ventana_conn_fallida() # Si ocurre un error, abrir ventana indicando que la conexión falló
        
        # Define una estructura para almacenar fuentes tipográficas utilizadas en la interfaz.
        self.fonts = {
            
            'title': ('verdana', 26, 'bold'),
            'boton': ('verdana', 14, 'bold'),
        }
        
        # Cargar imágenes para los iconos de visibilidad de contraseña, ajustando su tamaño
        self.ojo_abierto = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "ojoabierto.png")).resize((50, 50)), size=(50, 50))
        self.ojo_cerrado = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "ojo-cerrado.png")).resize((50, 50)), size=(50, 50))
        
        # Configura la grilla de la ventana principal para distribuir los elementos de manera uniforme.
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Crea el primer frame con un color de fondo transparente.
        self.frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame.grid(row= 0, column = 0, sticky = 'nsew')  # Lo posiciona en la fila 0 y lo expande.
        
        # Crea el segundo frame con un color de fondo transparente.
        self.frame1 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame1.grid(row= 1, column = 0, sticky = 'nsew') # Lo posiciona en la fila 1 y lo expande.
        
        # Configura la grilla del primer frame para que los elementos se expandan uniformemente.
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1) # Configura la grilla del frame para que se expanda en la fila 0.
        
        # Configura la grilla del segundo frame para permitir distribución equitativa de elementos.
        self.frame1.grid_columnconfigure(0, weight=1) # Configura la grilla del frame1 para que se expanda en la columna 0.
        self.frame1.grid_columnconfigure(1, weight=1) # Configura la grilla del frame1 para que se expanda en la columna 1.
        
        # Configura la grilla del segundo frame para distribuir elementos en 6 filas.
        for i in range(6):
            
            self.frame1.grid_rowconfigure(i, weight=1)
        
        # Llama al método widgets_admon() para agregar los widgets a la interfaz.
        self.widgets_admon()
        
    def obtener_ventana(self):
        
        """
        Retorna la instancia de la ventana principal (self.root).

        Esto permite que otros módulos o clases puedan acceder a la ventana principal
        y manipularla si es necesario.
        """
        
        return self.root 
    
    def widgets_admon(self):
        
        """
        Configura y crea los widgets de la ventana de administración.
        Los botones se habilitan dinámicamente según si hay un administrador registrado.
        """

        # Encabezado
        campos = [{'label': 'Administrar\nBases De Datos'}]

        # Botones primera columna
        campos1 = [
            {'label': 'Pacientes', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_pacientes_admon(self.root), self.root.iconify()), 'state': 'disabled'},
            {'label': 'Usuarios', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_usuarios_admon(self.root), self.root.iconify()), 'state': 'disabled'},
            {'label': 'Alergias', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_alergias(self.root), self.root.iconify()), 'state': 'disabled'},
            {'label': 'Aislamientos', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_aislamiento(self.root), self.root.iconify()), 'state': 'disabled'},
            {'label': 'Rango Edades', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_rango_edad(self.root), self.root.iconify()), 'state': 'disabled'},
            {'label': 'Lista De Estudios', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_estudio_ordenado(self.root), self.root.iconify()), 'state': 'disabled'},
        ]

        # Botones segunda columna
        campos2 = [
            {'label': 'Modalidades', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_modalidad(self.root), self.root.iconify()), 'state': 'disabled'},
            {'label': 'Estados', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_estados(self.root), self.root.iconify()), 'state': 'disabled'},
            {'label': 'Sedes', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_sedes(self.root), self.root.iconify()), 'state': 'disabled'},
            {'label': 'Retrasos', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_ratrasos(self.root), self.root.iconify()), 'state': 'disabled'},
            {'label': 'Cargos', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': lambda: (abrir_ventana_cargos(self.root), self.root.iconify()), 'state': 'disabled'},
            {'label': 'Salir', 'tipo': 'boton', 'ancho': 50, 'alto': 40, 'command': self.cerrar, 'state': 'disabled'},
        ]
        
        # Crear label del encabezado
        for i, campo in enumerate(campos):
            self.crear_label(self.frame, campo['label'], self.fonts['title'], fila=0, columna=0)

        # Crear botones primera columna
        for i, campo in enumerate(campos1):
            boton = self.crear_boton(
                self.frame1,
                text=campo['label'],
                font=self.fonts['boton'],
                fila=i,
                columna=0,
                command=campo['command'],
                widget_alto=campo['alto'],
                widget_ancho=campo['ancho'],
                state=campo['state']
            )
            
            self.botones.append(boton)

        # Crear botones segunda columna
        for i, campo in enumerate(campos2):
            boton = self.crear_boton(
                self.frame1,
                text=campo['label'],
                font=self.fonts['boton'],
                fila=i,
                columna=1,
                command=campo['command'],
                widget_alto=campo['alto'],
                widget_ancho=campo['ancho'],
                state=campo['state']
            )
            
            self.botones.append(boton)
        
        # ajustar el estado real de los botones
        self.ajustar_estado_botones()
        
    def crear_label(self, parent, texto, fuente, fila, columna, ancho = 1, alto = 1):
        
        """
        Crea y posiciona un widget de etiqueta (label) en la interfaz.

        Parámetros:
        - parent: Frame o ventana donde se ubicará el label.
        - texto: Texto que se mostrará en la etiqueta.
        - fuente: Fuente utilizada para el texto del label.
        - fila: Número de fila en la que se ubicará dentro del grid.
        - columna: Número de columna en la que se ubicará dentro del grid.
        - ancho (opcional): Número de columnas que abarcará (por defecto, 1).
        - alto (opcional): Número de filas que abarcará (por defecto, 1).

        Retorna:
        - El objeto label creado.
        """
        
        # Crea un label con el texto y la fuente especificados
        label = ctk.CTkLabel(parent,
                            text= texto,
                            font= fuente,
                            text_color = "#484a4b"
                            )
        
        # Ubica el label en la grilla del parent, permitiendo que se expanda
        label.grid(row=fila, column=columna, sticky='nsew', columnspan = ancho, rowspan = alto)
        
        return label 
    
    def crear_boton(self, parent, text, font, fila, columna, command, widget_ancho = 60, widget_alto = 30, state = 'normal'):
        
        """
        Crea y posiciona un botón en la interfaz.

        Parámetros:
        - parent: Frame o ventana donde se ubicará el botón.
        - text: Texto que se mostrará en el botón.
        - font: Fuente utilizada para el texto del botón.
        - fila: Número de fila en la que se ubicará dentro del grid.
        - columna: Número de columna en la que se ubicará dentro del grid.
        - command: Función que se ejecutará al presionar el botón.
        - widget_ancho (opcional): Ancho del botón en píxeles (valor predeterminado: 60).
        - widget_alto (opcional): Alto del botón en píxeles (valor predeterminado: 30).

        Retorna:
        - El objeto botón creado.
        """
        
        # Crea un botón con el texto, fuente y otras propiedades visuales
        boton = ctk.CTkButton(parent,
                            text=text,                  # Texto que mostrará el botón
                            font=font,                  # Fuente del texto
                            text_color='white',         # Color del texto en el botón
                            corner_radius=10,           # Radio de las esquinas para un diseño redondeado
                            command=command,            # Acción que se ejecutará al hacer clic en el botón
                            width=widget_ancho,         # Ancho del botón
                            height=widget_alto,         # Alto del botón
                            state= state,               # estado del boton
                            hover_color= "lightgreen",  # al pasar el mouse
                            fg_color= "#00155C"
                            )
        
        # Posiciona el botón dentro de la grilla del contenedor
        boton.grid(row= fila, column = columna, sticky= 'ew', pady = 5, padx = 5)
        
        return boton # Devuelve el objeto del botón para su posible reutilización

    def admin_registrado(self):
        """
        Devuelve True si hay al menos un usuario con cargo 'Administrador' en la DB, False si no.
        """
        datos = cargar_datos_db()
        if datos is None:
            print("⚠️ No hay datos de conexión a la base de datos.")
            return False

        try:
            #conexion = mysql.connector.connect(
            host=datos['host'],
            user=datos['user'],
            password=datos['password'],
            database='entregaturno',
            port=datos['port']
            
            
            id_cargo = self.obtener_id_cargo('Administrador')
            
            self.db.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE cargo = %s;", (id_cargo,))
            cantidad = self.db.cursor.fetchone()[0]
            
            return cantidad > 0

        except mysql.connector.Error as e:
            print(f"❌ Error al verificar administrador: {e}")
            return False

    def ajustar_estado_botones(self):
        """
        Habilita o deshabilita los botones según si hay administrador registrado.
        """
                
        tiene_admin = self.admin_registrado()

        for boton in self.botones:
            texto = boton.cget("text")
            if tiene_admin:
                boton.configure(state="normal")
            else:
                if texto in ["Modalidades", "Cargos", "Salir"]:
                    
                    boton.configure(state="normal")
                    
                else:
                    
                    boton.configure(state="disabled")

        # Solo mostrar ventana si NO hay administrador
        if not tiene_admin:
            admon_debes_hacer_primero()

        self.root.update_idletasks()
        
    def obtener_id_cargo(self, nombre_cargo):
        
        # solo tomamos el nombre
        nombre_cargo = nombre_cargo.split(' (')[0]
        
        sql = "SELECT * FROM cargos WHERE nombre_cargo = %s"
        
        self.db.cursor.execute(sql, (nombre_cargo,))
        
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None

    def cerrar(self):
        
        """Método personalizado para el botón Salir.
        """
        # Si existe una conexión a la base de datos, se cierra
        if self.db:
            
            self.db.cerrar_conexion()  # Llamamos al método de la clase 'Conexion_DB' para cerrar la conexión con la base de datos
            
            cerrar_conexion()
        
        self.root.destroy() # Cierra la ventana actual de la aplicación
            
        abrir_ventana_inicio()

#a=VentanaAdmon()
#b=a.obtener_ventana()
#b.mainloop()