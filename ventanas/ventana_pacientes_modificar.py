import sys # Importa el módulo sys para manipular el path del sistema
import os # Importa el módulo os para manejar rutas de archivos y directorios

"""Añade al path del sistema la ruta del directorio padre del archivo actual.
Esto permite importar módulos desde la carpeta superior."""

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))  # Añade al path el directorio padre del archivo actual

# Importación de librerías necesarias para la interfaz

import customtkinter as ctk # Versión personalizada de Tkinter con mejor apariencia

import tkinter as tk # Importa la librería estándar Tkinter para interfaces gráficas

from usuarioactual.usuario_actual import UsuarioActual

from datetime import datetime

from tkcalendar import DateEntry # Widget calendario para seleccionar fechas

from conexion_DB.conexionDB import Conexion_DB # Importa la clase Conexion_DB desde el módulo conexion_DB.conexionDB para la conexión con la base de datos

# Importa funciones para abrir ventanas emergentes
from abrirventanasemergentes.abrir_ventanas import (abrir_ventana_conn_exito, 
                                                    abrir_ventana_conn_fallida,
                                                    modificacion_realizada,
                                                    cerrar_conexion
                                                    )

from abrirventanas.abrir import cerrar_ppal

# Clase para la ventana de modificación de pacientes
class PacientesModificar():
    
    conexion_realizada = False # Variable de clase para indicar si ya se realizó la conexión a la base de datos
    db = None # Variable de clase para almacenar la conexión a la base de datos
    
    # Constructor de la clase que recibe la ventana y el paciente a modificar
    def __init__(self, ventana, paciente):

        self.ventana = ventana  # Guarda la referencia a la ventana en un atributo

        # Configura el layout de la ventana principal usando grid
        self.ventana.grid_rowconfigure(0, weight=1)  # Frame superior (10% del alto total)
        self.ventana.grid_rowconfigure(1, weight=1)  # Frame superior (10% del alto total)
        self.ventana.grid_rowconfigure(2, weight=8)  # Frames inferiores (90% del alto total)
        self.ventana.grid_columnconfigure(0, weight=1)  # Frame 1
        self.ventana.grid_columnconfigure(1, weight=1)  # Frame 2
        self.ventana.grid_columnconfigure(2, weight=1)  # Frame 3
        
        # Frame principal con scroll
        self.frame_ppal = ctk.CTkScrollableFrame(self.ventana, bg_color="white", fg_color='transparent') # Frame desplazable
        self.frame_ppal.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew") # ocupa toda la ventana
        
        # Configura grid interno del frame superior
        self.frame_ppal.grid_rowconfigure(0, weight=1) # configura la fila interna
        self.frame_ppal.grid_columnconfigure(0, weight=1) # configura la columna interna

        # Frame superior
        self.frame_sup = ctk.CTkFrame(self.frame_ppal, bg_color="white", fg_color='transparent')
        self.frame_sup.grid(row=0, column=0, columnspan=3, sticky="nsew") # Ubicación en la grilla
        
        # Configura grid interno del frame superior
        self.frame_sup.grid_rowconfigure(0, weight=1) # configura la fila interna
        self.frame_sup.grid_columnconfigure(0, weight=1) # configura la columna interna
        
        # Frame superior
        self.frame_sup1 = ctk.CTkFrame(self.frame_ppal, bg_color="white", fg_color='transparent')
        self.frame_sup1.grid(row=1, column=0, columnspan=3, sticky="nsew") # Ubicación en la grilla
        
        # Configura grid interno del frame superior
        self.frame_sup1.grid_rowconfigure(0, weight=1) # configura la columna interna
        
        # Configurar columnas internas del frame_sup1
        self.frame_sup1.grid_columnconfigure(0, weight=1)
        self.frame_sup1.grid_columnconfigure(1, weight=1)
        self.frame_sup1.grid_columnconfigure(2, weight=1)

        # Frame 1
        self.frame1 = ctk.CTkFrame(self.frame_ppal, bg_color="white", fg_color='transparent')
        self.frame1.grid(row=2, column=0, sticky="nsew") # Ubicación en la grilla
        
        self.frame1.grid_rowconfigure(0, weight=1) # configura la fila interna
        self.frame1.grid_columnconfigure(0, weight=1) # configura la columna interna

        # Frame 2
        self.frame2 = ctk.CTkFrame(self.frame_ppal, bg_color="white", fg_color='transparent')
        self.frame2.grid(row=2, column=1, sticky="nsew") # Ubicación en la grilla
        
        self.frame2.grid_rowconfigure(0, weight=1) # configura la fila interna
        self.frame2.grid_columnconfigure(0, weight=1) # configura la columna interna

        # Frame 3
        self.frame3 = ctk.CTkFrame(self.frame_ppal, bg_color="white", fg_color='transparent')
        self.frame3.grid(row=2, column=2, sticky="nsew") # Ubicación en la grilla
        
        self.frame3.grid_rowconfigure(0, weight=1) # configura la fila interna
        self.frame3.grid_columnconfigure(0, weight=1) # configura la columna interna

        if not PacientesModificar.conexion_realizada: # Si no se ha hecho la conexión a la BD
            try:
                PacientesModificar.db = Conexion_DB() # Crea una instancia de la conexión
                PacientesModificar.db.conectar() # Establece la conexión
                abrir_ventana_conn_exito() # Muestra ventana de conexión exitosa
                PacientesModificar.conexion_realizada = True # Marca la conexión como realizada
                
            except:
                
                abrir_ventana_conn_fallida() # Si no se establece la conexión, muestra ventana de fallo
        else:

            pass
            
        self.db = PacientesModificar.db # Guarda la referencia de la conexión en el objeto actual
        
        # Diccionario con estilos de fuente para los textos
        self.fonts = {

            "title": ("Verdana", 26, 'bold'),

            "title_frame": ("Verdana", 24, 'bold'),

            "label_title": ("Verdana", 14, 'bold'),
            
            "label": ("Verdana", 12 ),
            
            "date": ("Verdana", 12 ),
            
            "boton": ("Verdana", 14, 'bold'),

        }
        
        self.paciente_modificar = paciente # Guarda el paciente a modificar

        print("el paciente recibido es :", self.paciente_modificar)
        
        # se obtiene la informacion de la base de datos para luego ponerla en los entrys
        self.rangos_extraidos = self.obtener_rango_edad()
        self.modalidades_extraidas = self.obtener_modalidades()
        self.estado_extraido = self.obtener_estado()
        self.sedes_extraidas = self.obtener_sede()
        self.alergias_extraidas = self.obtener_alergia()
        self.aislamiento_extraido = self.obtener_aislamientos()
        self.estudio_extraido = []
        #self.estudio_extraido = self.obtener_estudios_ordenados()
        self.causales_retrasos_extraidos = self.obtener_causal_retraso()
        self.horas_extraidas = self.obtener_hora_citacion_realizacion(paciente)

        # se crean los contenidos de visualización para el usuario
        self.contenidotituloppalmodificar()
        self.contenidosframe1modificar()
        self.contenidosframe2modificar()
        self.contenidosframe3modificar()
        
        # Llena los campos con la información del paciente
        self.llenado_pacientes()
        # Bind que activa la función al hacer clic o doble clic
        self.entry_texto_est_ord.bind("<ButtonRelease-1>", self.agregar_seleccion_a_lista)
        #self.entry_texto_est_ord.bind("<Double-Button-1>", self.agregar_seleccion_a_lista)
        
        # Cambiar cursor al pasar el mouse (como hipervínculo)
        self.entry_texto_est_ord.bind("<Enter>", lambda e: self.entry_texto_est_ord.configure(cursor="hand2"))
        self.entry_texto_est_ord.bind("<Leave>", lambda e: self.entry_texto_est_ord.configure(cursor="xterm"))

    # Devuelve la ventana actual
    def obtener_ventana(self):
        
        return self.ventana
    
    # comparamos y extraemos información para mostrar
    
    def comparar_extraer_rango_edad(self): 
        
        # Buscar el rango_edad en paciente_modificar (que es un diccionario)
        for i, v in self.paciente_modificar.items():
            if i == "rango_edad":
                valor = v
                break  # ya encontramos lo que buscamos

        if valor is None:
            return None  # si no existe, no seguimos

        # Buscar coincidencia en rangos_extraidos (lista de diccionarios)
        for fila in self.rangos_extraidos:   
            if fila["id_rangoedad"] == valor:
                return fila["rango"]   # devolvemos solo el valor asociado

        return None
    
    def comparar_extraer_modalidad(self):
        # Buscar la modalidad en paciente_modificar (que es un diccionario)
        
        for i,v in self.paciente_modificar.items():
            if i == 'modalidad':
                
                valor = v
                
                break # ya encontramos lo que buscamos
            
        if valor is None:
            return None # si no existe, no seguimos
        
        # Buscar coincidencia en rangos_extraidos (lista de diccionarios)
        for fila in self.modalidades_extraidas:
            if fila ["id_modalidad"] == valor:
                return fila["nombre_modalidad"]  # devolvemos solo el valor asociado
        return None
    
    def comparar_extraer_sede(self):
        # Buscar la sede en paciente_modificar (que es un diccionario)
        
        for i,v in self.paciente_modificar.items():
            if i == 'sede':
                
                valor = v
                
                break # ya encontramos lo que buscamos
            
        if valor is None:
            return None # si no existe, no seguimos
        
        # Buscar coincidencia en rangos_extraidos (lista de diccionarios)
        for fila in self.sedes_extraidas:
            if fila ["id_sede"] == valor:
                return fila["nombre_sede"]  # devolvemos solo el valor asociado
        return None
    
    def comparar_extraer_estado(self):
        
        valor = None
        
        # Buscar el estado en paciente_modificar (que es un diccionario)
        
        for i,v in self.paciente_modificar.items():
            if i == 'estado':
                
                valor = v
                
                break # ya encontramos lo que buscamos
            
        if valor is None:
            return None # si no existe, no seguimos
        
        # Buscar coincidencia en rangos_extraidos (lista de diccionarios)
        for fila in self.estado_extraido:
            if fila ["id_estado"] == valor:
                return fila["nombre_estado"]  # devolvemos solo el valor asociado
        return None
    
    def comparar_extraer_alergia(self):
        
        valor = None
        
        # Buscar la alergia en paciente_modificar (que es un diccionario)
        
        for i,v in self.paciente_modificar.items():
            if i == 'tipo_alergia':
                
                valor = v
                
                break # ya encontramos lo que buscamos
            
        if valor is None:
            return None # si no existe, no seguimos
        
        # Buscar coincidencia en rangos_extraidos (lista de diccionarios)
        for fila in self.alergias_extraidas:
            if fila ["id_alergia"] == valor:
                return fila["nombre_alergia"]  # devolvemos solo el valor asociado
        return None
    
    def comparar_extraer_aislamiento(self):
        
        valor = None
        
        # Buscar el aislamiento en paciente_modificar (que es un diccionario)
        
        for i,v in self.paciente_modificar.items():
            if i == 'tipo_aislamiento':
                
                valor = v
                
                break # ya encontramos lo que buscamos
            
        if valor is None:
            return None # si no existe, no seguimos
        
        # Buscar coincidencia en rangos_extraidos (lista de diccionarios)
        for fila in self.aislamiento_extraido:
            if fila ["id_aislamiento"] == valor:
                return fila["nombre_aislamiento"]  # devolvemos solo el valor asociado
        return None
    
    def comparar_extraer_estudios_ordenados(self):
        
        valor = None  # <-- inicializamos
        
        # Buscar los estudios ordenados en paciente_modificar (que es un diccionario)
        
        for i,v in self.paciente_modificar.items():
            if i == 'estudios_ordenados':
                
                valor = v
                
                break # ya encontramos lo que buscamos
            
        if valor is None:
            return None # si no existe, no seguimos
        
        # Buscar coincidencia en rangos_extraidos (lista de diccionarios)
        for fila in self.estudio_extraido:
            if fila ["id_estudio"] == valor:
                return fila["nombre_estudio"]  # devolvemos solo el valor asociado
        return None
    
    def comparar_extraer_causales_retrasos(self):
        
        valor = None  # <-- inicializamos
        
        # Buscar los estudios ordenados en paciente_modificar (que es un diccionario)
        
        for i, v in self.paciente_modificar.items():
            
            if i == 'causal_retraso':
                
                valor = v
                
                break # ya encontramos lo que buscamos
            
        if valor is None:
            
            return None # si no existe, no seguimos
            
        # Buscar coincidencia en rangos_extraidos (lista de diccionarios)
        for fila in self.causales_retrasos_extraidos:
            
            if fila["id_retraso"] == valor:
                
                return fila["causal_retraso"]  # devolvemos solo el valor asociado
            
        return None
    
    def comparar_extraer_horas(self):
        
        identificacion_patient = None
        
        # Buscar las horas en paciente_modificar (que es un diccionario)
        
        for i,v in self.paciente_modificar.items():
            if i == 'identificacion_paciente':
                
                identificacion_patient = v
                
                break # ya encontramos lo que buscamos
            
        if identificacion_patient is None:
            return None # si no existe, no seguimos
        
        # Buscar coincidencia en rangos_extraidos (lista de diccionarios)
        for fila in self.horas_extraidas:
            if fila ["identificacion_paciente"] == identificacion_patient:
                
                return [{
                    "citacion" : fila["hora_citacion"],  # devolvemos solo el valor asociado
                    "realizacion" : fila["hora_realizacion"]  # devolvemos solo el valor asociado
                }]
                
        return None
    
    # parte de la visualizacion de la información
    
    def contenidotituloppalmodificar(self):
        
        self.titulo = ctk.CTkLabel(self.frame_sup, text='Modificar Datos Del Paciente', font=self.fonts['title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.titulo.grid(row=0, column=0, columnspan=3, sticky="nsew") 
    
    def contenidosframe1modificar(self):

        self.titulo_frame = ctk.CTkLabel(self.frame_sup1, text='Datos Del Paciente', font=self.fonts['title_frame'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.titulo_frame.grid(row=0, column=0, sticky='nsew')
        
        self.lab_identificacion = ctk.CTkLabel(self.frame1, text='Identificación Del Paciente', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_identificacion.grid(row=0, column=0, pady= 4, columnspan=2, sticky='ew')
        
        self.entry_identificacion_paciente = ctk.CTkEntry(self.frame1, 
                                                    font=self.fonts['label'],
                                                    width= 293,
                                                    height= 26,
                                                    fg_color='lightgray',
                                                    bg_color='white',
                                                    corner_radius=10,
                                                    text_color='black'
                                                    )
        self.entry_identificacion_paciente.grid(row=1, column=0, padx= 15, pady= 4, columnspan=2, sticky='nsew')
        
        self.lab_nombre = ctk.CTkLabel(self.frame1, text='Nombre Del Paciente', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_nombre.grid(row=2, column=0, pady= 4, columnspan=2, sticky='nsew')
        
        self.entry_nombre_paciente = ctk.CTkEntry(self.frame1, 
                                            font=self.fonts['label'],
                                            width= 600,
                                            height= 26,
                                            fg_color='lightgray',
                                            bg_color='white',
                                            corner_radius=10,
                                            text_color='black'
                                            )
        self.entry_nombre_paciente.grid(row=3, column=0, padx= 15, pady= 4, columnspan=2, sticky='nsew')
        
        self.entry_nombre_paciente.bind("<KeyRelease>", self.poner_title_nombre)
        
        self.lab_edad = ctk.CTkLabel(self.frame1, text='Edad', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_edad.grid(row=4, column=0, pady= 4, sticky='nsew')
        
        self.entry_edad_paciente = ctk.CTkEntry(self.frame1, 
                                        font=self.fonts['label'],
                                        width= 293,
                                        height= 26,
                                        fg_color='lightgray',
                                        bg_color='white',
                                        corner_radius=10,
                                        text_color='black'
                                        )
        self.entry_edad_paciente.grid(row=5, column=0, padx= 15, pady= 4, sticky='nsew')
        
        self.lab_rango_edad = ctk.CTkLabel(self.frame1, text='Rango Edad', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_rango_edad.grid(row=4, column=1, pady= 4, sticky='nsew')
        
        self.entry_rango_edad_paciente = ctk.CTkOptionMenu(self.frame1,
                                                    font=self.fonts['label'],
                                                    state="normal",
                                                    width= 285,
                                                    height= 26,
                                                    fg_color='lightgray',
                                                    bg_color='white',
                                                    corner_radius=10,
                                                    text_color='black',
                                                    values=[] ,
                                                    button_color="lightgray",
                                                    button_hover_color='lightgreen'
                                                    )
        self.entry_rango_edad_paciente.grid(row=5, column=1, sticky='nsew', padx= 15, pady= 4)
        
        self.lab_historia_clin = ctk.CTkLabel(self.frame1, text='Historia Clinica', font=self.fonts['label_title'], fg_color='white',bg_color='white', text_color= "#484a4b")
        self.lab_historia_clin.grid(row=6, column=0, pady= 4, columnspan=2, sticky='nsew')
        
        self.entry_historia_clin_paciente = ctk.CTkEntry(self.frame1, 
                                                    font=self.fonts['label'],
                                                    width= 293,
                                                    height= 26,
                                                    fg_color='lightgray',
                                                    bg_color='white',
                                                    corner_radius=10,
                                                    text_color='black'
                                                    )
        self.entry_historia_clin_paciente.grid(row=7, column=0, padx= 15, pady= 4, columnspan=2, sticky='nsew')
        
        self.lab_ubicacion = ctk.CTkLabel(self.frame1, text='Ubicación Paciente', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_ubicacion.grid(row=8, column=0, pady= 4, columnspan=2, sticky='nsew')
        
        self.entry_ubicacion_paciente = ctk.CTkEntry(self.frame1, 
                                                font=self.fonts['label'],
                                                width= 293,
                                                height= 26,
                                                fg_color='lightgray',
                                                bg_color='white',
                                                corner_radius=10,
                                                text_color='black'
                                                )
        self.entry_ubicacion_paciente.grid(row=9, column=0, padx= 15, pady= 4, columnspan=2, sticky='nsew')
        
        self.lab_sede = ctk.CTkLabel(self.frame1, text='Sede', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_sede.grid(row=10, column=0, pady= 4, columnspan=2, sticky='nsew')
        
        self.entry_sede_paciente = ctk.CTkOptionMenu(self.frame1,
                                            font=self.fonts['label'],
                                            state="normal",
                                            width= 285,
                                            height= 26,
                                            fg_color='lightgray',
                                            bg_color='white',
                                            corner_radius=10,
                                            text_color='black',
                                            values=[],
                                            button_color="lightgray",
                                            button_hover_color='lightgreen'
                                            )
        self.entry_sede_paciente.grid(row=11, column=0, padx= 15, pady= 4, columnspan=2, sticky='nsew')
        
        # Frame contenedor solo para los radios
        self.frame_radios = ctk.CTkFrame(self.frame1, fg_color="white",bg_color='white')
        self.frame_radios.grid(row=12, column=0, columnspan=3, sticky="nsew")

        # Configura 2 columnas en el sub-frame
        self.frame_radios.grid_rowconfigure(0, weight=1)
        self.frame_radios.grid_rowconfigure(1, weight=1)
        self.frame_radios.grid_columnconfigure(0, weight=1)
        self.frame_radios.grid_columnconfigure(1, weight=1)
        
        self.lab_alergias_paciente = ctk.CTkLabel(self.frame_radios, text='Alergias', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_alergias_paciente.grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        self.var_alergias = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_alergias1 = ctk.CTkRadioButton(self.frame_radios,
                                        text="Sí",
                                        variable = self.var_alergias,
                                        value=1,
                                        font=self.fonts['label'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray'
                                        )
        self.radio_alergias1.grid(row=1, column=0, padx=55, pady= 25, sticky='ew')

        # Botón de opción 2
        self.radio_alergias2 = ctk.CTkRadioButton(self.frame_radios,
                                        text="No",
                                        variable = self.var_alergias,
                                        value=0,
                                        font=self.fonts['label'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray',
                                        )
        self.radio_alergias2.grid(row=1, column=1, sticky='nsew')
        
        self.lab_tipo_alergia = ctk.CTkLabel(self.frame_radios, text='Selección de Alergias', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_tipo_alergia.grid(row=0, column= 2, sticky='nsew')
        
        self.entry_tipo_alergia_paciente = ctk.CTkOptionMenu(self.frame_radios,
                                                    font=self.fonts['label'],
                                                    state="normal",
                                                    width= 285,
                                                    height= 26,
                                                    fg_color='lightgray',
                                                    bg_color='white',
                                                    corner_radius=10,
                                                    text_color='black',
                                                    values=[],
                                                    button_color="lightgray",
                                                    button_hover_color='lightgreen',
                                                    command=self.llenar_textbox_alergia
                                                    )
        self.entry_tipo_alergia_paciente.grid(row=1, column= 2, padx= 20, pady= 4, sticky='ew')
        
        self.lab_alergias_paciente = ctk.CTkLabel(self.frame1, text='Alergias del Paciente', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_alergias_paciente.grid(row=13, column=0, pady = 4, columnspan = 2,  sticky='nsew')
        
        self.entry_texto_alergias_paciente = ctk.CTkTextbox(self.frame1,
                                    wrap=tk.WORD,
                                    height=50,
                                    width=560,
                                    fg_color="lightgray",
                                    bg_color= 'white',
                                    corner_radius= 10,
                                    font= self.fonts['label'],
                                    text_color='black',
                                    scrollbar_button_color= "lightgreen"
                                    )
        self.entry_texto_alergias_paciente.configure(state="disable")
        self.entry_texto_alergias_paciente.grid(row=14, column=0, columnspan= 2, pady=4, padx= 15, sticky='nsew')
        
        # Frame contenedor solo para los radios
        self.frame_radios1 = ctk.CTkFrame(self.frame1, fg_color="white",bg_color='white')
        self.frame_radios1.grid(row=15, column=0, columnspan=3, pady=4, sticky="nsew")

        # Configura 2 columnas en el sub-frame
        self.frame_radios1.grid_rowconfigure(0, weight=1)
        self.frame_radios1.grid_rowconfigure(1, weight=1)
        self.frame_radios1.grid_columnconfigure(0, weight=1)
        self.frame_radios1.grid_columnconfigure(1, weight=1)
        
        self.lab_aislamiento_paciente = ctk.CTkLabel(self.frame_radios1, text='Aislamiento', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_aislamiento_paciente.grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        self.var_aislamiento = tk.IntVar(value=0)  # Valor predeterminado es No

        # Botón de opción 1
        self.radio_aislamiento1 = ctk.CTkRadioButton(self.frame_radios1,
                                            text="Sí",
                                            variable = self.var_aislamiento,
                                            value=1,
                                            font=self.fonts['label'],
                                            fg_color= 'black',
                                            bg_color='white',
                                            border_color= 'lightgray'
                                            )
        self.radio_aislamiento1.grid(row=1, column=0, padx=55, sticky='ew')

        # Botón de opción 2
        self.radio_aislamiento2 = ctk.CTkRadioButton(self.frame_radios1,
                                            text="No",
                                            variable = self.var_aislamiento,
                                            value=0,
                                            font=self.fonts['label'],
                                            fg_color= 'black',
                                            bg_color='white',
                                            border_color= 'lightgray'
                                            )
        self.radio_aislamiento2.grid(row=1, column=1, sticky='ew')
        
        self.lab_tipo_aislamiento = ctk.CTkLabel(self.frame_radios1, text='Tipo De Aislamiento', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_tipo_aislamiento.grid(row=0, column= 2, pady= 4, sticky='nsew')
        
        self.entry_tipo_aislamiento_paciente = ctk.CTkOptionMenu(self.frame_radios1,
                                                        font=self.fonts['label'],
                                                        state="normal",
                                                        width= 285,
                                                        height= 26,
                                                        fg_color='lightgray',
                                                        bg_color='white',
                                                        corner_radius=10,
                                                        text_color='black',
                                                        values=[],
                                                        button_color="lightgray",
                                                        button_hover_color='lightgreen',
                                                        command=self.llenar_textbox_aislamiento
                                                        )
        self.entry_tipo_aislamiento_paciente.grid(row=1, column= 2, padx= 20, pady= 4, sticky='nsew')
        
        self.lab_aislam_paciente = ctk.CTkLabel(self.frame1, text='Aislamientos del Paciente', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_aislam_paciente.grid(row=16, column=0, pady = 4, columnspan = 2,  sticky='nsew')
        
        self.entry_texto_aislamientos_paciente = ctk.CTkTextbox(self.frame1,
                                    wrap=tk.WORD,
                                    height=50,
                                    width=560,
                                    fg_color="lightgray",
                                    bg_color= 'white',
                                    corner_radius= 10,
                                    font= self.fonts['label'],
                                    text_color='black',
                                    scrollbar_button_color= "lightgreen"
                                    )
        self.entry_texto_aislamientos_paciente.configure(state="disable")
        self.entry_texto_aislamientos_paciente.grid(row=17, column=0, columnspan= 2, pady=4, padx= 15, sticky='nsew')
        
        self.lab_estado = ctk.CTkLabel(self.frame1, text='Estado', font=self.fonts['label_title'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_estado.grid(row=18, column= 0, pady=4, columnspan=2, sticky='nsew')
        
        self.entry_estado_paciente = ctk.CTkOptionMenu(self.frame1,
                                                font=self.fonts['label'],
                                                state="normal",
                                                width= 285,
                                                height= 26,
                                                fg_color='lightgray',
                                                bg_color='white',
                                                corner_radius=10,
                                                text_color='black',
                                                values=[],
                                                button_color="lightgray",
                                                button_hover_color='lightgreen',
                                                command= self.cambio_diferido_a_pendiente
                                                )
        self.entry_estado_paciente.grid(row=19, column= 0, padx= 15, pady= 4, columnspan=2, sticky='nsew')
    
    def contenidosframe2modificar (self):
        
        self.titulo = ctk.CTkLabel(self.frame_sup1, text='Datos Del Estudio', font= self.fonts['title_frame'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.titulo.grid(row=0, column=1, sticky='nsew')
        
        self.lab_fecha_orden = ctk.CTkLabel(self.frame2, font= self.fonts['label_title'], fg_color= 'white', text='Fecha De La Orden', bg_color= 'white', text_color= "#484a4b")
        self.lab_fecha_orden.grid(row= 0, column= 0, sticky= 'nsew', pady= 4)
        
        self.entry_fecha_orden = DateEntry(self.frame2,
                                    width=20,
                                    background='lightgray',
                                    foreground='white',
                                    date_pattern= 'dd/MM/yyyy',
                                    font=self.fonts['date'],
                                    locale = 'es')
        self.entry_fecha_orden.grid(row=1, column=0, pady=4, padx=15, sticky='nsew')
        
        self.entry_fecha_orden.delete(0, 'end')
        
        self.lab_fecha_citacion = ctk.CTkLabel(self.frame2, font= self.fonts['label_title'], fg_color= 'white', text='Fecha De La Cita', bg_color= 'white', text_color= "#484a4b")
        self.lab_fecha_citacion.grid(row= 2, column= 0, sticky= 'nsew', pady= 4)
        
        self.entry_fecha_cita = DateEntry(self.frame2,
                                width=20,
                                background='lightgray',
                                foreground='white',
                                date_pattern= 'dd/MM/yyyy',
                                font= self.fonts['date'],
                                locale = 'es'
                                )
        self.entry_fecha_cita.grid(row=3, column=0, pady=4, padx=15, sticky='nsew')
        
        self.lab_modalidad = ctk.CTkLabel(self.frame2, text='Modalidad', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_modalidad.grid(row=4, column=0, pady = 4, sticky='nsew')
        
        self.entry_modalidad = ctk.CTkOptionMenu(self.frame2,
                                        font= self.fonts['label'],
                                        state="normal",
                                        width= 275,
                                        height= 26,
                                        fg_color='lightgray',
                                        bg_color= 'white',
                                        corner_radius=10,
                                        text_color='black',
                                        values=[],
                                        button_color="lightgray",
                                        button_hover_color='lightgreen',
                                        command=self.actualizar_estudios
                                        )
        self.entry_modalidad.grid(row=5, column=0, sticky='nsew', padx= 15, pady= 4)
        
        self.lab_estud_ordenados = ctk.CTkLabel(self.frame2, text='Lista de Estudios', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_estud_ordenados.grid(row=6, column=0, pady = 4, sticky='nsew')
        
        self.entry_texto_est_ord = ctk.CTkTextbox(self.frame2,
                                    wrap=tk.WORD,
                                    height=100,
                                    width=560,
                                    fg_color="lightgray",
                                    bg_color= 'white',
                                    corner_radius= 10,
                                    font= self.fonts['label'],
                                    text_color='black',
                                    scrollbar_button_color= "lightgreen"
                                    )
        self.entry_texto_est_ord.configure(state="disable")
        self.entry_texto_est_ord.grid(row=7, column=0, columnspan= 4, pady=4, padx= 15, sticky='nsew')
        
        self.lab_estud_ordenados = ctk.CTkLabel(self.frame2, text='Estudios Ordenados Al Paciente', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_estud_ordenados.grid(row=8, column=0, pady = 4, sticky='nsew')
        
        self.entry_list_estud_ordenados = ctk.CTkTextbox(self.frame2,
                                                    wrap=tk.WORD,
                                                    height=150,
                                                    width=560,
                                                    fg_color="lightgray",
                                                    bg_color= 'white',
                                                    corner_radius= 10,
                                                    font= self.fonts['label'],
                                                    text_color='black',
                                                    scrollbar_button_color= "lightgreen"
                                                    )
        self.entry_list_estud_ordenados.configure(state= 'disable')
        self.entry_list_estud_ordenados.grid(row=9, column=0, columnspan= 4, pady=4, padx= 15, sticky='nsew')
        
        self.lab_estud_ordenados = ctk.CTkLabel(self.frame2, text='Buscador de Estudios', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_estud_ordenados.grid(row=10, column=0, pady = 4, sticky='nsew')
        
        self.entry_busqueda = ctk.CTkEntry(self.frame2,
                                    font= self.fonts['label'],
                                    width= 275,
                                    height= 20,
                                    fg_color='lightgray',
                                    bg_color= 'white',
                                    corner_radius=10,
                                    text_color='black'
                                    )
        self.entry_busqueda.grid (row=11, column=0, pady=4, padx= 15, sticky='nsew')
        
        self.entry_busqueda.bind("<KeyRelease>", self.buscar_estudios_en_textbox)
        
        # Frame contenedor solo para los radios
        self.frame_radios2 = ctk.CTkFrame(self.frame2, fg_color="white",bg_color='white')
        self.frame_radios2.grid(row=12, column=0, columnspan=4, sticky="nsew")

        # Configura 2 columnas en el sub-frame
        self.frame_radios2.grid_rowconfigure(0, weight=1)
        self.frame_radios2.grid_rowconfigure(1, weight=1)
        self.frame_radios2.grid_columnconfigure(0, weight=1)
        self.frame_radios2.grid_columnconfigure(1, weight=1)
        
        self.lab_ayuno_paciente = ctk.CTkLabel(self.frame_radios2, text='Ayuno', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_ayuno_paciente.grid(row=0, column=0, columnspan = 2, sticky='nsew')
        
        self.var_ayuno = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_ayuno1 = ctk.CTkRadioButton(self.frame_radios2,
                                    text="Sí",
                                    variable = self.var_ayuno,
                                    value=1,
                                    font= self.fonts['label'],
                                    bg_color= 'white',
                                    fg_color= 'black',
                                    border_color= 'lightgray'
                                    )
        self.radio_ayuno1.grid(row=1, column=0, padx=55, sticky='nsew')

        # Botón de opción 2
        self.radio_ayuno2 = ctk.CTkRadioButton(self.frame_radios2,
                                    text="No",
                                    variable = self.var_ayuno,
                                    value=0,
                                    font= self.fonts['label'],
                                    bg_color= 'white',
                                    fg_color= 'black',
                                    border_color= 'lightgray'
                                    )
        self.radio_ayuno2.grid(row=1, column=1, sticky='nsew')
        
        self.lab_diferido_paciente = ctk.CTkLabel(self.frame_radios2, text='Diferido', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_diferido_paciente.grid(row=0, column=2, columnspan = 2, sticky='nsew')
        
        self.var_diferido = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_diferido1 = ctk.CTkRadioButton(self.frame_radios2,
                                        text="Sí",
                                        variable = self.var_diferido,
                                        value=1,
                                        font= self.fonts['label'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray',
                                        command=self.cambio_diferido_a_pendiente
                                        )
        self.radio_diferido1.grid(row=1, column=2, padx=12, sticky='nsew')

        # Botón de opción 2
        self.radio_diferido2 = ctk.CTkRadioButton(self.frame_radios2,
                                        text="No",
                                        variable = self.var_diferido,
                                        value=0,
                                        font= self.fonts['label'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray',
                                        command=self.cambio_diferido_a_pendiente
                                        )
        self.radio_diferido2.grid(row=1, column=3, sticky='nsew')
        
        self.lab_autorizacion_paciente = ctk.CTkLabel(self.frame_radios2, text='Autorización', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_autorizacion_paciente.grid(row=2, column=0, columnspan =2, sticky='nsew')
        
        self.var_autorizacion = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_autorizacion1 = ctk.CTkRadioButton(self.frame_radios2,
                                            text="Sí",
                                            variable = self.var_autorizacion,
                                            value=1,
                                            font= self.fonts['label'],
                                            bg_color= 'white',
                                            fg_color= 'black',
                                            border_color= 'lightgray'
                                            )
        self.radio_autorizacion1.grid(row=3, column=0, padx=55, sticky='nsew')

        # Botón de opción 2
        self.radio_autorizacion2 = ctk.CTkRadioButton(self.frame_radios2,
                                            text="No",
                                            variable = self.var_autorizacion,
                                            value=0,
                                            font= self.fonts['label'],
                                            bg_color= 'white',
                                            fg_color= "#bd0936",
                                            border_color= 'lightgray'
                                            )
        self.radio_autorizacion2.grid(row=3, column=1, sticky='nsew')
        
        self.lab_anestesia_paciente = ctk.CTkLabel(self.frame_radios2, text='Anestesia', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_anestesia_paciente.grid(row=2, column= 2, columnspan = 2, sticky='nsew')
        
        self.var_anestesia = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_anestesia1 = ctk.CTkRadioButton(self.frame_radios2,
                                        text="Sí",
                                        variable = self.var_anestesia,
                                        value=1,
                                        font= self.fonts['label'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray'
                                        )
        self.radio_anestesia1.grid(row=3, column=2, padx=12, sticky='nsew')

        # Botón de opción 2
        self.radio_anestesia2 = ctk.CTkRadioButton(self.frame_radios2,
                                        text="No",
                                        variable = self.var_anestesia,
                                        value=0,
                                        font= self.fonts['label'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray'
                                        )
        self.radio_anestesia2.grid(row=3, column=3, sticky='nsew')
        
        self.lab_diagnostico = ctk.CTkLabel(self.frame2, text='Diagnóstico', font= self.fonts['label_title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_diagnostico.grid(row=13, column=0, pady = 8, sticky='nsew')
        
        self.entry_texto_diagnostico = ctk.CTkTextbox(self.frame2,
                                        wrap=tk.WORD,
                                        height=100,
                                        width=560,
                                        fg_color="lightgray",
                                        bg_color= "white",
                                        corner_radius= 10,
                                        font= self.fonts['label'],
                                        text_color='black',
                                        scrollbar_button_color= "lightgreen"
                                        )
        self.entry_texto_diagnostico.grid(row=14, column=0, columnspan= 4, pady=10, padx= 15, sticky='nsew')
    
    def contenidosframe3modificar (self):
        
        from abrirventanas.abrir import cerrar_ppal
        
        self.titulo = ctk.CTkLabel(self.frame_sup1, text='Realización Del Estudio', fg_color='white', font=self.fonts['title_frame'], bg_color= 'white')
        self.titulo.grid(row=0, column=2, sticky='nsew')
        
        self.lab_hora_citacion = ctk.CTkLabel(self.frame3, font=self.fonts['label_title'], fg_color= 'white', text='Hora De La Cita', bg_color= 'white')
        self.lab_hora_citacion.grid(row = 0, column = 0, sticky='nsew')
        
        self.horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 5)]  # Intervalos de 5 minutos
        self.entry_combobox_hora_citacion = ctk.CTkOptionMenu(self.frame3,
                                                    font=self.fonts['label'],
                                                    state="normal",
                                                    width= 285,
                                                    height= 26,
                                                    fg_color='lightgray',
                                                    bg_color= 'white',
                                                    corner_radius=10,
                                                    text_color='black',
                                                    button_color="lightgray",
                                                    button_hover_color='lightgreen',
                                                    values=['Seleccione Una Hora'] + self.horas
                                                    )
        self.entry_combobox_hora_citacion.grid(row=1, column=0, pady=4, padx=15, sticky='nsew')
        
        self.lab_hora_realizacion = ctk.CTkLabel(self.frame3, font=self.fonts['label_title'], fg_color= 'white', text='Hora Realización Estudio', bg_color= 'white')
        self.lab_hora_realizacion.grid(row = 2, column = 0, sticky='nsew', pady=4)
        
        self.entry_combobox_hora_realizacion = ctk.CTkOptionMenu(self.frame3,
                                                    font=self.fonts['label'],
                                                    state="normal",
                                                    width= 285,
                                                    height= 26,
                                                    fg_color='lightgray',
                                                    bg_color= 'white',
                                                    corner_radius=10,
                                                    text_color='black',
                                                    button_color="lightgray",
                                                    button_hover_color='lightgreen',
                                                    values=['Seleccione Una Hora'] + self.horas
                                                    )
        self.entry_combobox_hora_realizacion.grid(row=3, column=0, pady=4, padx=15, sticky='nsew')
        
        self.lab_causal_retraso = ctk.CTkLabel(self.frame3, font=self.fonts['label_title'], fg_color= 'white', text='Causal Del Retraso', bg_color= 'white')
        self.lab_causal_retraso.grid(row = 4, column = 0, sticky = 'nsew', pady=4)
        
        self.entry_list_caus_retraso = ctk.CTkOptionMenu(self.frame3,
                                                font=self.fonts['label'],
                                                state="normal",
                                                width= 610,
                                                height= 26,
                                                fg_color='lightgray',
                                                bg_color= 'white',
                                                corner_radius=10,
                                                text_color='black',
                                                values=[],
                                                button_color="lightgray",
                                                button_hover_color='lightgreen'
                                                )
        self.entry_list_caus_retraso.grid(row=5, column=0, pady=4, padx=15, sticky='nsew')
        
        self.lab_coment_tecnologo = ctk.CTkLabel(self.frame3, text='Comentarios Tecnólogo', font=self.fonts['label_title'], fg_color='white')
        self.lab_coment_tecnologo.grid(row=6, column=0, pady = 8, sticky='nsew')
        
        self.entry_texto_coment_tecnologo = ctk.CTkTextbox(self.frame3,
                                                    wrap=tk.WORD,
                                                    height=100,
                                                    width=610,
                                                    fg_color="lightgray",
                                                    bg_color= 'white',
                                                    corner_radius= 10,
                                                    font=self.fonts['label'],
                                                    text_color='black',
                                                    scrollbar_button_color= "lightgreen"
                                                    )
        self.entry_texto_coment_tecnologo.grid(row=7, column=0, pady=4, padx= 15, sticky='nsew')
        
        # Frame contenedor solo para los radios
        self.frame_radios = ctk.CTkFrame(self.frame3, fg_color="white",bg_color='white')
        self.frame_radios.grid(row=8, column=0, columnspan =2, pady = 10, sticky="nsew")

        # Configura 2 columnas en el sub-frame
        self.frame_radios.grid_rowconfigure(0, weight=1)
        self.frame_radios.grid_rowconfigure(1, weight=1)
        self.frame_radios.grid_columnconfigure(0, weight=1)
        self.frame_radios.grid_columnconfigure(1, weight=1)
        
        self.lab_coment_al_radiologo = ctk.CTkLabel(self.frame_radios, font=self.fonts['label_title'], fg_color= 'white', text='Comentar Estudio Con Radiólogo', bg_color= 'white')
        self.lab_coment_al_radiologo.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')
        
        self.var_coment_al_rad = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_coment_radiologo1 = ctk.CTkRadioButton(self.frame_radios,
                                                    text="Sí", 
                                                    variable = self.var_coment_al_rad, 
                                                    value=1, font=self.fonts['label'], 
                                                    bg_color= 'white',
                                                    fg_color= 'black',
                                                    border_color= 'lightgray'
                                                    )
        self.radio_coment_radiologo1.grid(row=1, column=0, padx=150, pady= 10, sticky='nsew')

        # Botón de opción 2
        self.radio_coment_radiologo2 = ctk.CTkRadioButton(self.frame_radios, 
                                                    text="No",
                                                    variable = self.var_coment_al_rad,
                                                    value=0, font=self.fonts['label'],
                                                    bg_color= 'white',
                                                    fg_color= 'black',
                                                    border_color= 'lightgray')
        self.radio_coment_radiologo2.grid(row=1, column=1, pady= 10, sticky='nsew')
        
        # frame_coment_radiologo = tk.Frame(self.frame, bg= 'white')
        # frame_coment_radiologo.grid(row=9, column=0, pady=10, sticky='nsew')
        
        self.lab_coment_radiologo = ctk.CTkLabel(self.frame3, text='Comentarios Radiólogo', font=self.fonts['label_title'], fg_color='white', bg_color= 'white')
        self.lab_coment_radiologo.grid(row=9, column=0, pady = 8, sticky='nsew')
        
        self.entry_texto_coment_radiologo = ctk.CTkTextbox(self.frame3,
                                                    wrap=tk.WORD,
                                                    height=100,
                                                    width=610,
                                                    fg_color="lightgray",
                                                    bg_color= 'white',
                                                    corner_radius= 10,
                                                    font=self.fonts['label'],
                                                    text_color='black',
                                                    scrollbar_button_color= "lightgreen"
                                                    )
        self.entry_texto_coment_radiologo.configure(state = 'disable')
        self.entry_texto_coment_radiologo.grid(row=10, column=0, pady=4, padx= 15, sticky='nsew')
        
        self.frame_buttons = ctk.CTkFrame(self.frame3,
                                    width=610,
                                    height=230,
                                    fg_color='white',
                                    bg_color= 'white'
                                    )
        self.frame_buttons.grid(row= 11, column=0, sticky='nsew', padx= 15, pady= 4)
        
        # Configura las columnas dentro de frame_buttons para que se expandan
        self.frame_buttons.grid_columnconfigure(list(range(3)), weight=1)

        self.frame_buttons.grid_rowconfigure(0, weight=1)
        
        self.btn_modificar = ctk.CTkButton(self.frame_buttons,
                                text='Modificar Paciente',
                                text_color='White',
                                font=self.fonts['boton'],
                                width=20,
                                height=50,
                                corner_radius=20,
                                fg_color='#00155c',
                                bg_color= 'white',
                                hover_color = 'lightgreen',
                                anchor='center',
                                command= self.mostrar
                                )
        
        self.btn_modificar.grid(row= 0, column= 0, padx= 4, pady= 70, sticky='nsew')
        
        self.btn_atras = ctk.CTkButton(self.frame_buttons,
                                text='Atrás',
                                text_color='white',
                                font=self.fonts['boton'],
                                width=20,
                                height=50,
                                corner_radius=20,
                                fg_color='#00155c',
                                bg_color= 'white',
                                hover_color = 'lightgreen',
                                anchor='center',
                                command= lambda: cerrar_ppal(self.frame3.winfo_toplevel())
                                )
        
        self.btn_atras.grid(row= 0, column= 2, padx= 4, pady= 70, sticky='nsew')
    
    def llenado_pacientes(self):
        
        mapping = {
            'identificacion_paciente': self.entry_identificacion_paciente,
            'nombre_paciente': self.entry_nombre_paciente,
            'edad': self.entry_edad_paciente,
            'rango_edad': self.entry_rango_edad_paciente,
            'hc': self.entry_historia_clin_paciente,
            'ubicacion': self.entry_ubicacion_paciente,
            'sede': self.entry_sede_paciente,
            'alergia': self.var_alergias,
            'alergia_texto' : self.entry_tipo_alergia_paciente,
            'tipo_alergia': self.entry_texto_alergias_paciente,
            'aislamiento': self.var_aislamiento,
            'aislamiento_texto': self.entry_tipo_aislamiento_paciente,
            'tipo_aislamiento': self.entry_texto_aislamientos_paciente,
            'estado': self.entry_estado_paciente,
            'fecha_orden': self.entry_fecha_orden,
            'fecha_citacion': self.entry_fecha_cita,
            'modalidad': self.entry_modalidad,
            'estudios_ordenados_texto': self.entry_texto_est_ord,
            'estudios_ordenados_paciente': self.entry_list_estud_ordenados,
            'ayuno': self.var_ayuno,
            'diferido' : self.var_diferido,
            'autorizacion' : self.var_autorizacion,
            'anestesia' : self.var_anestesia,
            'diagnostico' : self.entry_texto_diagnostico,
            'hora_citacion' : self.entry_combobox_hora_citacion,
            'hora_realizacion' : self.entry_combobox_hora_realizacion,
            'causal_retraso' : self.entry_list_caus_retraso,
            'comentarios_tecnologo' : self.entry_texto_coment_tecnologo,
            'comentar_radiologo' : self.var_coment_al_rad,
            'comentarios_radiologo' : self.entry_texto_coment_radiologo
        }
        
        # Mapeo de ComboBox a funciones que convierten ID a nombre
                
        for clave, widget in mapping.items():
            valor = self.paciente_modificar.get(clave)
            
            # para los entrys
            if isinstance(widget, ctk.CTkEntry):

                widget.delete(0, "end")
                if valor is not None:
                    widget.insert(0, str(valor))
                    
                # Solo habilitamos 
                if clave in ("ubicacion", "edad", "nombre_paciente"):
                    widget.configure(state="normal")
                else:
                    widget.configure(state="disable")
            
            # Para los Textbox
            elif isinstance(widget, ctk.CTkTextbox):

                # Si es diagnóstico o comentarios del tecnólogo, permitimos edición
                if clave in ["diagnostico", "comentarios_tecnologo", "estudios_ordenados_paciente"]:
                    widget.configure(state="normal")
                    widget.delete("0.0", "end")
                    if valor is not None:
                        widget.insert("0.0", str(valor)) 
                
                # Si es estudios disponibles (solo lectura)
                elif clave == "estudios_ordenados_texto":
                    widget.configure(state="normal")
                    widget.delete("0.0", "end")
                    if valor is not None:
                        widget.insert("0.0", str(valor))
                    self.llenar_textbox_estudios()  # esto llena entry_texto_est_ord
                    widget.configure(state="disable")  # Solo lectura
                
                elif clave == "tipo_alergia":
                    widget.configure(state="normal")
                    widget.delete("0.0", "end")
                    if valor is not None:
                        widget.insert("0.0", str(valor))
                    valor = self.comparar_extraer_alergia()  # esto llena entry_texto_alergia
                
                elif clave == "tipo_aislamiento":
                    widget.configure(state="normal")
                    widget.delete("0.0", "end")
                    if valor is not None:
                        widget.insert("0.0", str(valor))
                    valor = self.comparar_extraer_aislamiento()  # esto llena entry_texto_aislamiento
                
                # Otros Textbox que se bloquean
                else:
                    widget.configure(state="normal")
                    widget.delete("0.0", "end")
                    if valor is not None:
                        widget.insert("0.0", str(valor))
                    widget.configure(state="disable")

            # para los combobox
            elif isinstance(widget, ctk.CTkOptionMenu):

                opciones = []
                
                # Hacer que el ComboBox sea solo de selección
                widget.configure(state="normal")
                
                # Bloquear escritura manual (solo permite seleccionar)
                def bloquear_escritura(event):
                    return "break"
                widget.bind("<Key>", bloquear_escritura)
            
                # Determinar las opciones según el ComboBox
                if clave == "rango_edad":
                    self.llenar_combobox_rango_edad()
                    valor = self.comparar_extraer_rango_edad()
                    
                if clave == "modalidad":
                    
                    self.llenar_combobox_modalidad()
                    valor = self.comparar_extraer_modalidad() # aquí usamos el valor traducido con comparar_extraer

                if clave == "sede":
                    
                    self.llenar_combobox_sedes()
                    valor = self.comparar_extraer_sede() # aquí usamos el valor traducido con comparar_extraer

                if clave == "estado":
                    
                    self.llenar_combobox_estados()
                    valor = self.comparar_extraer_estado()# aquí usamos el valor traducido con comparar_extraer

                if clave == "alergia_texto":
                    
                    self.llenar_combobox_alergia()
                    
                if clave == "aislamiento_texto":
                    
                    self.llenar_combobox_aislamiento()
                    
                if clave == "causal_retraso":
                    
                    self.llenar_combobox_causal_retraso()
                    valor = self.comparar_extraer_causales_retrasos() # aquí usamos el valor traducido con comparar_extraer

                resultado = self.comparar_extraer_horas()

                if resultado:  # Si no es None
                    citacion_timedelta = resultado[0]["citacion"]
                    realizacion_timedelta = resultado[0]["realizacion"]

                    # Convertimos a string HH:MM:SS
                    citacion_str = str(citacion_timedelta)
                    realizacion_str = str(realizacion_timedelta)

                    # Actualizamos los widgets usando tu mapping
                    mapping['hora_citacion'].set(citacion_str)
                    mapping['hora_realizacion'].set(realizacion_str)
                    
                # Finalmente, asignar el valor del paciente o la opción por defecto
                if valor is not None and valor in widget.cget("values"):
                    widget.set(str(valor))
                else:
                    if opciones:
                        widget.set(opciones[0])  # primera opción como default

            # para los radiobutton
            elif isinstance(widget, tk.Variable):  # Para IntVar de radio buttons
                if valor is not None:
                    # Convertir de 'si'/'no' a 1/2 según el caso
                    if valor.title() == "Si":
                        widget.set(1)
                    else:
                        widget.set(0)
            
            # Para DateEntry
            elif isinstance(widget, DateEntry):
                if valor is not None:
                    widget.set_date(valor)
    
    # traemos la informacion de la base de datos de las diferentes tablas

    def obtener_modalidades(self):
        """Obtiene las modalidades de la db y lo guardamos en una lista."""
        
        self.modalidades = []
        
        sql = "SELECT * FROM modalidades"
        self.db.cursor.execute(sql)
        
        columnas = self.db.cursor.column_names
        
        filas = self.db.cursor.fetchall()
        
        modalidad = (dict(zip(columnas, fila)) for fila in filas)
        
        self.modalidades.clear()
        self.modalidades.extend(modalidad)
        
        return self.modalidades
    
    def obtener_rango_edad(self):
        
        """Obtiene los rangos de edades de la db y lo guardamos en una lista."""
        
        self.rangos = []
        
        """Obtiene el nombre del rango edad desde la base de datos usando su ID."""
        sql = "SELECT * FROM rangosedades"
        self.db.cursor.execute(sql)
        
        columnas = self.db.cursor.column_names
        
        filas = self.db.cursor.fetchall()
        
        resultado = [dict(zip(columnas, fila)) for fila in filas]
        
        self.rangos.clear()
        self.rangos.extend(resultado)
        
        return self.rangos
    
    def obtener_aislamientos(self):
        """Obtiene los aislamientos de la db y lo guardamos en una lista."""
        
        self.aislamientos = []
        
        sql = "SELECT * FROM aislamientos"
        self.db.cursor.execute(sql)
        
        columnas = self.db.cursor.column_names
        
        filas = self.db.cursor.fetchall()
        
        aislamiento = (dict(zip(columnas, fila)) for fila in filas)
        
        self.aislamientos.clear()
        self.aislamientos.extend(aislamiento)
        
        return self.aislamientos
    
    def obtener_estado(self):
        """Obtiene los estados de la db y lo guardamos en una lista."""
        
        self.estado = []
        
        sql = "SELECT  * FROM estados"
        self.db.cursor.execute(sql)
        
        columnas = self.db.cursor.column_names
        
        filas = self.db.cursor.fetchall()
        
        estados = (dict(zip(columnas, fila))for fila in filas)
        
        self.estado.clear()
        self.estado.extend(estados)
        
        return self.estado

    def obtener_sede(self):
        """Obtiene las sedes de la db y lo guardamos en una lista."""
        
        self.sedes = []
        
        sql = "SELECT * FROM sedes"
        self.db.cursor.execute(sql)
        
        columnas = self.db.cursor.column_names
        
        filas = self.db.cursor.fetchall()
        
        sede = (dict(zip(columnas, fila)) for fila in filas)
        
        self.sedes.clear()
        self.sedes.extend(sede)
    
        return self.sedes

    def obtener_alergia(self):
        
        """Obtiene las alergias de la db y lo guardamos en una lista."""
        
        self.alergias = []
        
        sql = "SELECT * FROM alergias"
        
        self.db.cursor.execute(sql)
        
        columnas = self.db.cursor.column_names
        
        filas = self.db.cursor.fetchall()
        
        alergia = (dict(zip(columnas, fila)) for fila in filas)
        
        self.alergias.clear()
        self.alergias.extend(alergia)
        
        return self.alergias
    
    def obtener_estudios_ordenados(self):
        
        """Obtiene los estudios de la db y lo guardamos en una lista."""
        
        self.estudios = []
        
        sql = "SELECT * FROM listaestudios"
        self.db.cursor.execute(sql)
        
        columnas = self.db.cursor.column_names
        
        filas = self.db.cursor.fetchall()
        
        estudio_encontrado = [dict(zip(columnas, fila)) for fila in filas]
        
        # Obtener la modalidad seleccionada
        modalidad_seleccionada = self.entry_modalidad.get()
        
        if not modalidad_seleccionada:
            return []  # Si no hay modalidad seleccionada, devolvemos lista vacía

        # Tomar la primera palabra de la modalidad
        primera_palabra_mod = modalidad_seleccionada.split()[0].title()

        # Filtrar los estudios cuyo nombre comience con la primera palabra de la modalidad
        for estudio in estudio_encontrado:
            nombre_estudio = estudio.get("nombre_estudio", "").title()
            if nombre_estudio.startswith(primera_palabra_mod):
                
                self.estudios.append(estudio)
                
        return self.estudios
    
    def obtener_hora_citacion_realizacion(self, paciente):

        """Obtiene todos los ids con su hora de citación y hora estudio y los devuelve como lista de diccionarios."""
        
        self.horas = []
        
        # Estado del paciente (número)
        estado_id = paciente.get("estado")

        # Buscar el nombre del estado en la lista de estados
        estado_nombre = next(
            (e["nombre_estado"] for e in self.estado_extraido if e["id_estado"] == estado_id),
            None
        )
        
        # Definir tabla según estado
        if estado_nombre == 'Diferido':
            tabla = "registrospacientesdiferidos"
        else:  # Pendiente o comentado
            tabla = "registrospacientes"
        
        sql = f"SELECT identificacion_paciente, hora_citacion, hora_realizacion FROM {tabla}"
        
        #sql = "SELECT identificacion_paciente, hora_citacion, hora_realizacion FROM registrospacientes"
        self.db.cursor.execute(sql)
        filas = self.db.cursor.fetchall()
        
        resultado = [{"identificacion_paciente": fila[0], "hora_citacion": fila[1], "hora_realizacion": fila[2]} for fila in filas]
        
        self.horas.clear()
        self.horas.extend(resultado)
        
        return self.horas
    
    def obtener_causal_retraso(self):
        
        """Obtiene las causales de retraso de la db y lo guardamos en una lista."""
        
        self.retrasos = []
        
        sql = "SELECT * FROM retrasos"
        
        self.db.cursor.execute(sql)
        
        columnas = self.db.cursor.column_names
        
        filas = self.db.cursor.fetchall()
        
        resultado = (dict(zip(columnas, fila)) for fila in filas)
        
        self.retrasos.clear()
        self.retrasos.extend(resultado)
        
        return self.retrasos

    # realizamos la consulta para llenar los combobox
    
    def llenar_combobox_rango_edad(self):
        
        informacion = self.obtener_rango_edad()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["rango"] for fila in informacion]

        # Insertar la opción por defecto solo si no existe
        if "Elige un rango de edad" not in opciones:
            opciones.insert(0, "Elige un rango de edad")
            
        self.entry_rango_edad_paciente.configure(values=opciones)

    def llenar_combobox_modalidad(self):
        
        informacion = self.obtener_modalidades()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["nombre_modalidad"] for fila in informacion]

        # Insertar la opción por defecto solo si no existe
        if "Elige una Modalidad" not in opciones:
            opciones.insert(0, "Elige una Modalidad")
            
        self.entry_modalidad.configure(values=opciones)

    def llenar_combobox_sedes(self):
        
        informacion = self.obtener_sede()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["nombre_sede"] for fila in informacion]

        # Insertar la opción por defecto solo si no existe
        if "Elige una Sede" not in opciones:
            opciones.insert(0, "Elige una Sede")
            
        self.entry_sede_paciente.configure(values=opciones)
    
    def llenar_combobox_alergia(self):
        
        informacion = self.obtener_alergia()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["nombre_alergia"] for fila in informacion]

        # Insertar la opción por defecto solo si no existe
        if "Elige un Tipo de Alergia" not in opciones:
            opciones.insert(0, "Elige un Tipo de Alergia")
            
        self.entry_tipo_alergia_paciente.configure(values=opciones)
        self.entry_tipo_alergia_paciente.set(opciones[0])
    
    def llenar_textbox_alergia(self, valor_seleccionado):
        
        if not valor_seleccionado or valor_seleccionado == "Elige un Tipo de Alergia":
            return

        widget_text = self.entry_texto_alergias_paciente
        widget_text.configure(state="normal")

        contenido_actual = widget_text.get("0.0", "end").strip()

        # Evitar duplicados
        lista_valores = [v.strip() for v in contenido_actual.split(",") if v.strip()]
        if valor_seleccionado not in lista_valores:
            lista_valores.append(valor_seleccionado)

        widget_text.delete("0.0", "end")
        widget_text.insert("0.0", ", ".join(lista_valores))
        #widget_text.configure(state="disable")
    
    def llenar_combobox_aislamiento(self):
        
        informacion = self.obtener_aislamientos()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["nombre_aislamiento"] for fila in informacion]

        # Insertar la opción por defecto solo si no existe
        if "Elige un Tipo de Aislamiento" not in opciones:
            opciones.insert(0, "Elige un Tipo de Aislamiento")
            
        self.entry_tipo_aislamiento_paciente.configure(values=opciones)
        self.entry_tipo_aislamiento_paciente.set(opciones[0])
    
    def llenar_textbox_aislamiento(self, valor_seleccionado):
        
        if not valor_seleccionado or valor_seleccionado == "Elige un Tipo de Aislamiento":
            return

        widget_text = self.entry_texto_aislamientos_paciente
        widget_text.configure(state="normal")

        contenido_actual = widget_text.get("0.0", "end").strip()

        # Evitar duplicados
        lista_valores = [v.strip() for v in contenido_actual.split(",") if v.strip()]
        if valor_seleccionado not in lista_valores:
            lista_valores.append(valor_seleccionado)

        widget_text.delete("0.0", "end")
        widget_text.insert("0.0", ", ".join(lista_valores))
        #widget_text.configure(state="disable")
    
    def llenar_combobox_estados(self):
        
        informacion = self.obtener_estado()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["nombre_estado"] for fila in informacion]

        # Insertar la opción por defecto solo si no existe
        if "Elige un Estado" not in opciones:
            opciones.insert(0, "Elige un Estado")
            
        self.entry_estado_paciente.configure(values=opciones)

    def llenar_combobox_causal_retraso(self):
        
        informacion = self.obtener_causal_retraso()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["causal_retraso"] for fila in informacion]

        # Insertar la opción por defecto solo si no existe
        if "Elige una causal de Retraso" not in opciones:
            opciones.insert(0, "Elige una causal de Retraso")
            
        self.entry_list_caus_retraso.configure(values=opciones)
    
    def llenar_textbox_estudios(self):
        
        informacion = self.obtener_estudios_ordenados()
        opciones = [fila["nombre_estudio"] for fila in informacion]

        self.entry_texto_est_ord.configure(state="normal")
        self.entry_texto_est_ord.delete("0.0", "end")

        for nombre in opciones:
            self.entry_texto_est_ord.insert("end", nombre + "\n")

        self.entry_texto_est_ord.configure(state="disable")

    # para caundo se cambia de estado diferido a pendiente
    def actualizar_estudios(self, event=None):
        
        self.estudio_extraido = self.obtener_estudios_ordenados()
        self.llenar_textbox_estudios()
    
    def cambio_diferido_a_pendiente(self, *_):
            
        valor = self.var_diferido.get()  # 1 = Sí, 0 = No

        if valor == 1:  # Opción "Sí"
            self.entry_estado_paciente.set('Diferido')

        else:  # Opción "No"
            comentario = self.entry_texto_coment_radiologo.get("1.0", "end").strip()

            if comentario == "":
                self.entry_estado_paciente.set('Pendiente')
            else:
                self.entry_estado_paciente.set('Comentado')

    # Agregar selección del Textbox a la lista de estudios ordenados
    def agregar_seleccion_a_lista(self, event=None):
        
        # Habilitar temporalmente la lista para modificarla
        self.entry_list_estud_ordenados.configure(state="normal")

        # Obtener la posición del clic
        index = self.entry_texto_est_ord.index(f"@{event.x},{event.y}")
        linea = self.entry_texto_est_ord.get(f"{index} linestart", f"{index} lineend").strip()

        if linea:  # Si hay algo en la línea
            # Agregar al Textbox de lista, conservando lo que ya estaba
            contenido_actual = self.entry_list_estud_ordenados.get("0.0", "end").strip()
            if contenido_actual:
                self.entry_list_estud_ordenados.insert("end", ", " + linea)
            else:
                self.entry_list_estud_ordenados.insert("end", linea)
    
    def buscar_estudios_en_textbox(self, event=None):
            
        # Tomamos el texto del Entry
        texto_busqueda = self.entry_busqueda.get()

        # Convertir a Title solo si el texto tiene al menos 2 caracteres
        if len(texto_busqueda) >= 2:
            self.entry_busqueda.delete(0, "end")
            self.entry_busqueda.insert(0, texto_busqueda.title())
            texto_busqueda = texto_busqueda.title()

        # Limpiar los resaltados anteriores
        self.entry_texto_est_ord.tag_remove("resaltar", "0.0", "end")

        if texto_busqueda.strip() == "":
            return

        # Buscar coincidencias y resaltarlas
        start_pos = "0.0"
        primera_coincidencia = None
        while True:
            start_pos = self.entry_texto_est_ord.search(texto_busqueda, start_pos, nocase=1, stopindex="end")
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(texto_busqueda)}c"
            self.entry_texto_est_ord.tag_add("resaltar", start_pos, end_pos)
            if primera_coincidencia is None:
                primera_coincidencia = start_pos
            start_pos = end_pos

        self.entry_texto_est_ord.tag_config("resaltar", background="lightgreen", foreground="black")

        # Hacer scroll hasta la primera coincidencia
        if primera_coincidencia:
            self.entry_texto_est_ord.see(primera_coincidencia)
    
    def poner_title_nombre(self, event=None):
            
        # Tomamos el texto del Entry
        texto_ingresado = self.entry_nombre_paciente.get()

        # Convertir a Title solo si el texto tiene al menos 2 caracteres
        if len(texto_ingresado) >= 2:
            self.entry_nombre_paciente.delete(0, "end")
            self.entry_nombre_paciente.insert(0, texto_ingresado.title())
            texto_ingresado = texto_ingresado.title()
    
    def modificar_datos(self):
        
        # Diccionario con todas las variables tipo IntVar
        vars_si_no = {
            "aislamiento": self.var_aislamiento,
            "alergia": self.var_alergias,
            "ayuno" : self.var_ayuno,
            "diferido" : self.var_diferido,
            "autorizacion" : self.var_autorizacion,
            "anestesia" : self.var_anestesia,
            "coment_estudio" : self.var_coment_al_rad
        }

        # Convertimos todas a "Si"/"No"
        valores = {key: "Si" if valor.get() == 1 else "No" for key, valor in vars_si_no.items()}

        # Obtener valores de widgets
        identificacion = self.entry_identificacion_paciente.get()
        nombre = self.entry_nombre_paciente.get()
        edad = self.entry_edad_paciente.get()
        seleccion_rango = self.entry_rango_edad_paciente.get()
        id_rango = next((r["id_rangoedad"] for r in self.rangos if r["rango"] == seleccion_rango), None)
        hc = self.entry_historia_clin_paciente.get()
        ubicacion = self.entry_ubicacion_paciente.get()
        seleccion_sede = self.entry_sede_paciente.get()
        id_sede = next((r["id_sede"] for r in self.sedes if r["nombre_sede"] == seleccion_sede), None)
        tipo_alergia = self.entry_texto_alergias_paciente.get("1.0", "end-1c")
        tipo_aislamiento = self.entry_texto_aislamientos_paciente.get("1.0", "end-1c")
        
        estado = self.entry_estado_paciente.get()
        if estado == 'Pendiente' or estado == 'Comentado':
            id_estado = next((r["id_estado"] for r in self.estado if r["nombre_estado"] == estado), None)
        elif estado == 'Modificado':
            id_estado = self.obtener_id_estado('Modificado')
        elif estado == 'Diferido':
            id_estado = self.obtener_id_estado('Diferido')

        fecha1 = self.entry_fecha_orden.get()
        fecha_orden = datetime.strptime(fecha1, "%d/%m/%Y").date().isoformat()
        fecha2 = self.entry_fecha_cita.get()
        fecha_cita = datetime.strptime(fecha2, "%d/%m/%Y").date().isoformat()
        modalidad = self.entry_modalidad.get()
        id_modalidad = next((r["id_modalidad"] for r in self.modalidades if r["nombre_modalidad"] == modalidad), None)
        estud_ord = self.entry_list_estud_ordenados.get("1.0", "end-1c")
        diagnostico = self.entry_texto_diagnostico.get("1.0", "end-1c")
        hora_cita = self.entry_combobox_hora_citacion.get()
        hora_realizacion = self.entry_combobox_hora_realizacion.get()
        causal_retraso = self.entry_list_caus_retraso.get()
        id_retraso = next((r["id_retraso"] for r in self.retrasos if r["causal_retraso"] == causal_retraso), None)
        coment_tecnologo = self.entry_texto_coment_tecnologo.get("1.0", "end-1c")
        coment_radiologo = self.entry_texto_coment_radiologo.get("1.0", "end-1c")

        # Listas de valores para SQL
        # valores1 ya recalculado con "Si"/"No"
        valores1 = (
            nombre, identificacion, edad, id_rango, fecha_orden, fecha_cita, hc,
            ubicacion, id_modalidad, estud_ord, diagnostico, valores['ayuno'],
            valores['diferido'], valores['alergia'], tipo_alergia, valores['aislamiento'],
            tipo_aislamiento, valores['autorizacion'], valores['anestesia'], id_estado,
            id_sede, hora_cita, hora_realizacion, id_retraso, coment_tecnologo,
            valores['coment_estudio'], coment_radiologo, UsuarioActual.id_usuario, identificacion
        )

        valores_modificados = (nombre, identificacion, edad, id_rango, fecha_orden, fecha_cita, hc,
                            ubicacion, id_modalidad, estud_ord, diagnostico, valores['ayuno'],
                            valores['diferido'], valores['alergia'], tipo_alergia, valores['aislamiento'],
                            tipo_aislamiento, valores['autorizacion'], valores['anestesia'], id_estado,
                            id_sede, hora_cita, hora_realizacion, id_retraso, coment_tecnologo,
                            valores['coment_estudio'], coment_radiologo, UsuarioActual.id_usuario)

        # Consultar último estado del paciente
        sql_ultimo_estado = "SELECT estado FROM registrospacientes WHERE identificacion_paciente = %s ORDER BY id_registro DESC LIMIT 1"
        
        print("DEBUG diferido IntVar:", self.var_diferido.get())
        print("DEBUG valores['diferido'] (Si/No):", valores['diferido'])
        self.db.cursor.execute(sql_ultimo_estado, (identificacion,))
        fila = self.db.cursor.fetchone()

        if fila:
            ultimo_estado = fila[0]
            if ultimo_estado in [self.obtener_id_estado('Pendiente'), self.obtener_id_estado('Comentado'), self.obtener_id_estado('Diferido')]:
                
                print("DEBUG ultimo_estado:", ultimo_estado, type(ultimo_estado))
                print("DEBUG id Pendiente:", self.obtener_id_estado('Pendiente'))
                print("DEBUG id Comentado:", self.obtener_id_estado('Comentado'))
                
                # UPDATE registrospacientes
                sql_update = """UPDATE registrospacientes 
                                SET nombre_paciente = %s, identificacion_paciente = %s, edad = %s,
                                    rango_edad = %s, fecha_orden = %s, fecha_citacion = %s, hc = %s,
                                    ubicacion = %s, modalidad = %s, estudios_ordenados_paciente = %s,
                                    diagnostico = %s, ayuno = %s, diferido = %s, alergia = %s,
                                    tipo_alergia = %s, aislamiento = %s, tipo_aislamiento = %s,
                                    autorizacion = %s, anestesia = %s, estado = %s, sede = %s,
                                    hora_citacion = %s, hora_realizacion = %s, causal_retraso = %s,
                                    comentarios_tecnologo = %s, comentar_radiologo = %s,
                                    comentarios_radiologo = %s, usuario = %s
                                WHERE identificacion_paciente = %s"""
                                
                print("\n--- DEBUG IDENTIFICACIONES ---")
                print("Identificación ingresada en el formulario:", identificacion)
                print("Identificación usada en WHERE:", valores1[-1])
                print("Identificación que se actualizará en la columna:", valores1[1])
                print("¿Coinciden las dos?:", valores1[-1] == valores1[1])
                print("-------------------------------\n")
                self.db.cursor.execute(sql_update, valores1)
                print("DEBUG2 diferido IntVar:", self.var_diferido.get())
                print("DEBUG2 valores['diferido'] (Si/No):", valores['diferido'])
            else:
                # Último estado no Pendiente/Comentado → INSERT nuevo
                sql_insert = """INSERT INTO registrospacientes 
                                (nombre_paciente, identificacion_paciente, edad, rango_edad, fecha_orden,
                                fecha_citacion, hc, ubicacion, modalidad, estudios_ordenados_paciente,
                                diagnostico, ayuno, diferido, alergia, tipo_alergia, aislamiento,
                                tipo_aislamiento, autorizacion, anestesia, estado, sede, hora_citacion,
                                hora_realizacion, causal_retraso, comentarios_tecnologo, comentar_radiologo,
                                comentarios_radiologo, usuario)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                self.db.cursor.execute(sql_insert, valores_modificados)
                print("DEBUG3 diferido IntVar:", self.var_diferido.get())
                print("DEBUG3 valores['diferido'] (Si/No):", valores['diferido'])
        else:
            # No existe → INSERT
            sql_insert = """INSERT INTO registrospacientes 
                            (nombre_paciente, identificacion_paciente, edad, rango_edad, fecha_orden,
                            fecha_citacion, hc, ubicacion, modalidad, estudios_ordenados_paciente,
                            diagnostico, ayuno, diferido, alergia, tipo_alergia, aislamiento,
                            tipo_aislamiento, autorizacion, anestesia, estado, sede, hora_citacion,
                            hora_realizacion, causal_retraso, comentarios_tecnologo, comentar_radiologo,
                            comentarios_radiologo, usuario)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            self.db.cursor.execute(sql_insert, valores_modificados)
            print("DEBUG4 diferido IntVar:", self.var_diferido.get())
            print("DEBUG4 valores['diferido'] (Si/No):", valores['diferido'])
            
        print("DEBUG Se ejecutó UPDATE o INSERT en registrospacientes:", "UPDATE" if ultimo_estado in [self.obtener_id_estado('Pendiente'), self.obtener_id_estado('Comentado')] else "INSERT")

        # Siempre insertar en registrospacientesmodificados
        sql_modificados = """INSERT INTO registrospacientesmodificados
                            (nombre_paciente, identificacion_paciente, edad, rango_edad, fecha_orden,
                            fecha_citacion, hc, ubicacion, modalidad, estudios_ordenados_paciente,
                            diagnostico, ayuno, diferido, alergia, tipo_alergia, aislamiento,
                            tipo_aislamiento, autorizacion, anestesia, estado, sede, hora_citacion,
                            hora_realizacion, causal_retraso, comentarios_tecnologo, comentar_radiologo,
                            comentarios_radiologo, usuario)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        self.db.cursor.execute(sql_modificados, valores_modificados)
        print("DEBUG4 diferido IntVar:", self.var_diferido.get())
        print("DEBUG4 valores['diferido'] (Si/No):", valores['diferido'])
        
        """sql_diferidos = "INSERT INTO registrospacientesdiferidos
                            (nombre_paciente, identificacion_paciente, edad, rango_edad, fecha_orden,
                            fecha_citacion, hc, ubicacion, modalidad, estudios_ordenados_paciente,
                            diagnostico, ayuno, diferido, alergia, tipo_alergia, aislamiento,
                            tipo_aislamiento, autorizacion, anestesia, estado, sede, hora_citacion,
                            hora_realizacion, causal_retraso, comentarios_tecnologo, comentar_radiologo,
                            comentarios_radiologo, usuario)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.db.cursor.execute(sql_diferidos, valores_modificados)"""
        
        # UPDATE registrospacientes
        sql_diferidos = """UPDATE registrospacientesdiferidos 
                        SET nombre_paciente = %s, identificacion_paciente = %s, edad = %s,
                            rango_edad = %s, fecha_orden = %s, fecha_citacion = %s, hc = %s,
                            ubicacion = %s, modalidad = %s, estudios_ordenados_paciente = %s,
                            diagnostico = %s, ayuno = %s, diferido = %s, alergia = %s,
                            tipo_alergia = %s, aislamiento = %s, tipo_aislamiento = %s,
                            autorizacion = %s, anestesia = %s, estado = %s, sede = %s,
                            hora_citacion = %s, hora_realizacion = %s, causal_retraso = %s,
                            comentarios_tecnologo = %s, comentar_radiologo = %s,
                            comentarios_radiologo = %s, usuario = %s
                        WHERE identificacion_paciente = %s"""
        self.db.cursor.execute(sql_diferidos, valores1)
        print("DEBUG5 diferido IntVar:", self.var_diferido.get())
        print("DEBUG5 valores['diferido'] (Si/No):", valores['diferido'])

        self.db.conexion.commit()
        
        # Verifica en la DB
        self.db.cursor.execute(
            "SELECT diferido, estado FROM registrospacientes WHERE identificacion_paciente = %s ORDER BY id_registro DESC LIMIT 1", 
            (identificacion,)
        )
        print("DB row after update:", self.db.cursor.fetchone())
        
    """def actualizar_pantalla(self):
        
        if self.db:
            self.db.cerrar_conexion()
            PacientesModificar.conexion_realizada = None
        cerrar_conexion()
        
        if not PacientesModificar.conexion_realizada:
            try:
                PacientesModificar.db = Conexion_DB()
                PacientesModificar.db.conectar()
                abrir_ventana_conn_exito()
                PacientesModificar.conexion_realizada = True
            except Exception:

                abrir_ventana_conn_fallida()
                
        else:
            
            pass

        self.db = PacientesModificar.db
        
        self.cargar_pacientes()
        
        self.obtener_pacientes_filtrados()
        
        self.visual_principal_datos()
        
        self.ventana.after(600000, self.actualizar_pantalla)"""

    def obtener_id_estado(self, nombre_estado):
        """Obtiene el ID del estado basado en el nombre del estado."""
        # solo tomamos el nombre
        nombre_estado = nombre_estado.split(' (')[0]
        
        sql = "SELECT id_estado FROM estados WHERE nombre_estado = %s"
        self.db.cursor.execute(sql, (nombre_estado,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None

    def mostrar(self):
        
        self.modificar_datos()
        modificacion_realizada()
        cerrar_ppal(self.frame3.winfo_toplevel())
        