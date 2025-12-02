import sys # Importa el módulo sys para manipular el path del sistema
import os # Importa el módulo os para manejar rutas de archivos y directorios
import json
import re

"""Añade al path del sistema la ruta del directorio padre del archivo actual.
Esto permite importar módulos desde la carpeta superior."""

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))  # Añade al path el directorio padre del archivo actual

# Importación de librerías necesarias para la interfaz

import customtkinter as ctk # Versión personalizada de Tkinter con mejor apariencia

import tkinter as tk # Importa la librería estándar Tkinter para interfaces gráficas

from usuarioactual.usuario_actual import UsuarioActual

from datetime import datetime, timedelta, time

from tkinter import messagebox

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
        
        self.cargar_horas()
        self._mensaje_mostrado = False  # atributo de la clase
        self._pending_bloqueo = None
        self.archivo_json = "horas_tomadas.json"

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
        
        self.entry_sede_paciente.configure(command=lambda _: self._on_cambio_sede_o_fecha(campo="sede"))
        
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
                                locale = 'es',
                                command=self.actualizar_horas_disponibles
                                )
        self.entry_fecha_cita.grid(row=3, column=0, pady=4, padx=15, sticky='nsew')
        
        #self.entry_fecha_cita.bind("<<DateEntrySelected>>", lambda e: self.actualizar_horas_disponibles())
        self.entry_fecha_cita.bind("<<DateEntrySelected>>", lambda e: self._on_cambio_sede_o_fecha(campo="fecha"))
        
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
        self.horas = sorted(list(set(self.horas)))
        
        self.placeholder_text = "Seleccione Una Hora"
        
        self.entry_combobox_hora_citacion = ctk.CTkComboBox(self.frame3,
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
                                                    values=self.horas,
                                                    command=self._al_seleccionar_hora
                                                    )
        self.entry_combobox_hora_citacion.grid(row=1, column=0, pady=4, padx=15, sticky='nsew')
        
        # Vincular el evento de escritura
        self.entry_combobox_hora_citacion.set(self.placeholder_text)
        cb = self.entry_combobox_hora_citacion        
        cb.bind("<FocusIn>", lambda e, w=cb: self._clear_placeholder(e, w))
        cb.bind("<FocusOut>", lambda e, w=cb: self._restore_placeholder(e, w))
        
        # Click: actualizar filtro
        cb.bind("<Button-1>", lambda e, w=cb: self.filtrar_horas(e, w))

        # Tecla: SOLO filtrar, nada más
        cb.bind("<KeyRelease>", lambda e, w=cb: self.filtrar_horas(e, w))
        cb.bind("<KeyRelease>", lambda e: self._validar_hora_al_abrir_dropdown(e))
        
        # Iniciar verificación periódica automática
        self.verificar_hora_periodica()
        
        self.lab_hora_realizacion = ctk.CTkLabel(self.frame3, font=self.fonts['label_title'], fg_color= 'white', text='Hora Realización Estudio', bg_color= 'white')
        self.lab_hora_realizacion.grid(row = 2, column = 0, sticky='nsew', pady=4)
        
        self.entry_combobox_hora_realizacion = ctk.CTkComboBox(self.frame3,
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
        
        self.entry_combobox_hora_realizacion.set(self.placeholder_text)
            
        cb = self.entry_combobox_hora_realizacion
        cb.bind("<FocusIn>", lambda e, w=cb: self._clear_placeholder(e, w))
        cb.bind("<FocusOut>", lambda e, w=cb: self._restore_placeholder(e, w))
        cb.bind("<KeyRelease>", lambda e, w=cb: self.filtrar_horas(e, w))
        
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

    def obtener_id_estado(self, nombre_estado):
        """Obtiene el ID del estado basado en el nombre del estado."""
        # solo tomamos el nombre
        nombre_estado = nombre_estado.split(' (')[0]
        
        sql = "SELECT id_estado FROM estados WHERE nombre_estado = %s"
        self.db.cursor.execute(sql, (nombre_estado,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None
    
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

    def obtener_id_sede(self, nombre_sede):
        """Obtiene el ID de sede basado en el nombre de la sede."""
        # solo tomamos el nombre
        nombre_sede = nombre_sede.split(' (')[0]
        
        sql = "SELECT id_sede FROM sedes WHERE nombre_sede = %s"
        self.db.cursor.execute(sql, (nombre_sede,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None
    
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
    
        # Filtrar solo las modalidades deseadas
        modalidades_permitidas = [
            "Resonancia Magnetica",
            "Tomografia Axial Computarizada",
            "Ecografia"
        ]
        
        opciones = [fila["nombre_modalidad"] for fila in informacion if fila["nombre_modalidad"] in modalidades_permitidas]

        # Insertar la opción por defecto solo si no existe
        if "Elige una Modalidad" not in opciones:
            opciones.insert(0, "Elige una Modalidad")
            
        self.entry_modalidad.configure(values=opciones)
        self.entry_modalidad.set(opciones[0])

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
        
        #print("DEBUG diferido IntVar:", self.var_diferido.get())
        #print("DEBUG valores['diferido'] (Si/No):", valores['diferido'])
        self.db.cursor.execute(sql_ultimo_estado, (identificacion,))
        fila = self.db.cursor.fetchone()

        if fila:
            ultimo_estado = fila[0]
            if ultimo_estado in [self.obtener_id_estado('Pendiente'), self.obtener_id_estado('Comentado'), self.obtener_id_estado('Diferido')]:
                
                #print("DEBUG ultimo_estado:", ultimo_estado, type(ultimo_estado))
                #print("DEBUG id Pendiente:", self.obtener_id_estado('Pendiente'))
                #print("DEBUG id Comentado:", self.obtener_id_estado('Comentado'))
                
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
                                
                #print("\n--- DEBUG IDENTIFICACIONES ---")
                #print("Identificación ingresada en el formulario:", identificacion)
                #print("Identificación usada en WHERE:", valores1[-1])
                #print("Identificación que se actualizará en la columna:", valores1[1])
                #print("¿Coinciden las dos?:", valores1[-1] == valores1[1])
                #print("-------------------------------\n")
                self.db.cursor.execute(sql_update, valores1)
                #print("DEBUG2 diferido IntVar:", self.var_diferido.get())
                #print("DEBUG2 valores['diferido'] (Si/No):", valores['diferido'])
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
                #print("DEBUG3 diferido IntVar:", self.var_diferido.get())
                #print("DEBUG3 valores['diferido'] (Si/No):", valores['diferido'])
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
            #print("DEBUG4 diferido IntVar:", self.var_diferido.get())
            #print("DEBUG4 valores['diferido'] (Si/No):", valores['diferido'])
            
        #print("DEBUG Se ejecutó UPDATE o INSERT en registrospacientes:", "UPDATE" if ultimo_estado in [self.obtener_id_estado('Pendiente'), self.obtener_id_estado('Comentado')] else "INSERT")

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
        #print("DEBUG4 diferido IntVar:", self.var_diferido.get())
        #print("DEBUG4 valores['diferido'] (Si/No):", valores['diferido'])
        
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
        #print("DEBUG5 diferido IntVar:", self.var_diferido.get())
        #print("DEBUG5 valores['diferido'] (Si/No):", valores['diferido'])

        self.db.conexion.commit()
        
        # Verifica en la DB
        self.db.cursor.execute(
            "SELECT diferido, estado FROM registrospacientes WHERE identificacion_paciente = %s ORDER BY id_registro DESC LIMIT 1", 
            (identificacion,)
        )
        #print("DB row after update:", self.db.cursor.fetchone())
        
        messagebox.showinfo("Datos Modificados", 
                            "Los Datos Se Han Modificado Exitosamente", parent=self.ventana
                            )
        
        # ----------------------------
        # Guardar la hora de citación en JSON de horas tomadas
        # ----------------------------
            
        try:
            if hasattr(self, "_pending_bloqueo") and self._pending_bloqueo:
                from ventanas.ventana_pacientes_modificar import PacientesModificar

                # Cargar JSON existente por si alguien más lo cambió
                self.cargar_horas()
                horas_tomadas = self.horas_tomadas

                pb = self._pending_bloqueo
                id_sede = pb["id_sede"]
                fecha = pb["fecha"]
                horas_list = pb["horas"]

                # Aseguramos estructura
                horas_tomadas.setdefault(id_sede, {})
                horas_tomadas.setdefault("detalles", {})

                # Insertar horas en lista por sede/fecha (si no existe)
                horas_tomadas[id_sede].setdefault(fecha, [])
                for h in horas_list:
                    if h not in horas_tomadas[id_sede][fecha]:
                        horas_tomadas[id_sede][fecha].append(h)

                # Guardar en "detalles" solo si NO es diferido
                if not pb.get("diferido", False):
                    clave = f"{id_sede}_{fecha}_{(pb.get('hora_inicio') or horas_list[0])}"
                    horas_tomadas["detalles"][clave] = horas_list

                # Guardar JSON a disco (método ya existente)
                self.guardar_horas()

                # Opcional: actualizar combobox globales
                try:
                    PacientesModificar.actualizar_horas_disponibles()
                except Exception:
                    pass

                # Limpiar pending
                self._pending_bloqueo = None

        except Exception as e:
            print(e)
    
    def _clear_placeholder(self, event, widget=None):
        """Borra el placeholder; widget puede venir por parámetro o por event.widget."""
        if widget is None:
            widget = event.widget
        # si el combobox tiene un entry interno, usarlo
        entry = getattr(widget, "_entry", None)
        try:
            if entry is not None:
                if entry.get() == self.placeholder_text:
                    entry.after(10, lambda: entry.delete(0, "end"))
            else:
                if widget.get() == self.placeholder_text:
                    widget.after(10, lambda: widget.set(""))
        except Exception:
            pass

    def _restore_placeholder(self, event, widget=None):
        """Restaura placeholder si el campo quedó vacío; widget por parámetro o event.widget."""
        if widget is None:
            widget = event.widget
        entry = getattr(widget, "_entry", None)
        try:
            if entry is not None:
                if entry.get().strip() == "":
                    entry.delete(0, "end")
                    entry.insert(0, self.placeholder_text)
                    widget.configure(values=self.horas)
            else:
                if widget.get().strip() == "":
                    widget.set(self.placeholder_text)
                    widget.configure(values=self.horas)
        except Exception:
            pass

    def filtrar_horas(self, event, widget=None):
        """
        Filtra las horas en el combobox de hora de citación según el texto escrito
        y las horas ya tomadas para la fecha y sede seleccionadas.
        """
        if widget is None:
            widget = event.widget

        # Leer el texto actual del combobox (entry interno si existe)
        entry = getattr(widget, "_entry", None)
        try:
            texto = (entry.get() if entry is not None else widget.get()).strip()
        except Exception:
            texto = widget.get().strip()

        # Obtener fecha y sede (si podemos)
        try:
            fecha = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
        except Exception:
            fecha = None

        try:
            nombre_sede = self.entry_sede_paciente.get().strip()
            id_sede = self.obtener_id_sede(nombre_sede)
        except Exception:
            id_sede = None

        # horas ocupadas del día para la sede actual (si no existe sede, asumimos global vacío)
        horas_ocupadas = []
        if id_sede is not None:
            horas_ocupadas = self.horas_tomadas.get(str(id_sede), {}).get(fecha, [])

        # Si es el combobox de hora citación, filtrar horas ocupadas por fecha y sede
        if widget == self.entry_combobox_hora_citacion:
            if texto == "" or texto == self.placeholder_text:
                filtradas = [h for h in self.horas if h not in horas_ocupadas]
            else:
                filtradas = [h for h in self.horas if h.startswith(texto) and h not in horas_ocupadas]
        else:
            # Para hora de realización no se filtra por ocupadas, solo por texto
            if texto == "" or texto == self.placeholder_text:
                filtradas = self.horas
            else:
                filtradas = [h for h in self.horas if h.startswith(texto)]

        # Actualizar solo el combobox activo
        try:
            widget.configure(values=filtradas)
        except Exception:
            pass
    
    @classmethod
    def _normalizar_hora(self, texto):
        
        """Normaliza texto o entero de hora a formato HH:MM si es válido."""
        if texto is None:
            return None

        # Si es entero tipo 900 o 930
        if isinstance(texto, int):
            h = texto // 100
            m = texto % 100
            return f"{h:02d}:{m:02d}"

        # Si es datetime.time o datetime.datetime
        if isinstance(texto, (datetime, time)):
            return texto.strftime("%H:%M")

        # Asegurar que sea string
        if not isinstance(texto, str):
            texto = str(texto)

        texto = texto.strip()
        if not texto or texto == getattr(self, "placeholder_text", ""):
            return None

        # Si es número como '7' o '08'
        if re.fullmatch(r"\d{1,2}", texto):
            return f"{int(texto):02d}:00"

        # Si tiene formato H:MM o HH:MM
        m = re.fullmatch(r"(\d{1,2}):(\d{1,2})", texto)
        if m:
            h, mi = int(m.group(1)), int(m.group(2))
            if 0 <= h <= 23 and 0 <= mi <= 59:
                return f"{h:02d}:{mi:02d}"

        return None
    
    def bloquear_hora_tomada(self, event, widget=None, duracion_minutos=None):
        
        """
        Bloquea la hora seleccionada y las siguientes según la duración elegida
        por el usuario. Si se recibe duracion_minutos, lo usa y NO muestra el diálogo.
        """
        
        """if widget is None and event is not None:
            widget = event.widget
        if widget is None:
            return

        # Solo para el combobox de hora citación
        if widget != self.entry_combobox_hora_citacion:
            return

        # 1) Validar que haya identificación
        identificacion = self.entry_identificacion_paciente.get().strip()
        if not identificacion:
            messagebox.showwarning(
                "Falta identificación",
                "Debe ingresar la identificación del paciente antes de seleccionar la hora.",
                parent=self.ventana
            )
            widget.set(self.placeholder_text)
            return

        # 2) Normalizar hora parcial
        raw = widget.get().strip()
        hora_normalizada = self._normalizar_hora(raw)

        # 2a) Validaciones inmediatas (aunque sea parcial)
        if len(raw) >= 1:  # para que salga aviso al empezar a escribir
            try:
                sql_union = 
                    SELECT id_registro, estado, 'r' as tabla
                    FROM registrospacientes
                    WHERE identificacion_paciente = %s
                    UNION ALL
                    SELECT id_registro, estado, 'd' as tabla
                    FROM registrospacientesdiferidos
                    WHERE identificacion_paciente = %s
                    ORDER BY id_registro DESC
                    LIMIT 1
                
                self.db.cursor.execute(sql_union, (identificacion, identificacion))
                fila = self.db.cursor.fetchone()

                ultimo_estado_nombre = None
                if fila:
                    estado_id = fila[1]
                    sql_est = "SELECT nombre_estado FROM estados WHERE id_estado = %s"
                    self.db.cursor.execute(sql_est, (estado_id,))
                    fila_est = self.db.cursor.fetchone()
                    if fila_est:
                        ultimo_estado_nombre = fila_est[0]

                if ultimo_estado_nombre and ultimo_estado_nombre in ("Pendiente", "Comentado", "Diferido"):
                    messagebox.showwarning(
                        "Paciente con registro activo",
                        f"El paciente con identificación {identificacion} tiene un registro activo en estado: {ultimo_estado_nombre}.\nNo se puede asignar una nueva citación mientras exista un registro activo.",
                        parent=self.ventana
                    )
                    widget.set(self.placeholder_text)
                    return

            except Exception as e:
                print("[DEBUG] Error al consultar último estado del paciente:", e)
                messagebox.showerror("Error BD", "No se pudo verificar estado del paciente en la base de datos.", parent=self.ventana)
                widget.set(self.placeholder_text)
                return

        # 2b) Solo continuar si la hora es COMPLETA y existe en la lista
        if hora_normalizada is None or hora_normalizada not in self.horas:
            return  # todavía escribiendo, no hacer nada

        # 3) Preparar pending_bloqueo
        try:
            fecha = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
        except Exception:
            messagebox.showerror("Fecha inválida", "No se pudo obtener la fecha de citación.", parent=self.ventana)
            widget.set(self.placeholder_text)
            return

        nombre_sede = self.entry_sede_paciente.get().strip()
        id_sede = self.obtener_id_sede(nombre_sede)
        if id_sede is None:
            messagebox.showwarning("Sede inválida", "No se pudo determinar la sede seleccionada.", parent=self.ventana)
            widget.set(self.placeholder_text)
            return
        id_sede_str = str(id_sede)

        # --- SI ES DIFERIDO ---
        if getattr(self, "var_diferido", None) and self.var_diferido.get() == 1:
            self._pending_bloqueo = {
                "id_sede": id_sede_str,
                "fecha": fecha,
                "horas": [hora_normalizada],
                "diferido": True
            }
            print(f"[DEBUG] Pending bloqueo (diferido): {self._pending_bloqueo}")
            return

        # --- SI NO ES DIFERIDO: PEDIR DURACIÓN SOLO AQUÍ ---
        if duracion_minutos is None:
            duracion_minutos = self._mostrar_dialogo_duracion()
            if duracion_minutos is None:
                widget.set(self.placeholder_text)
                return

        # Calcular rango de horas a bloquear
        try:
            inicio_dt = datetime.strptime(hora_normalizada, "%H:%M")
            fin_dt = inicio_dt + timedelta(minutes=duracion_minutos)
        except Exception:
            messagebox.showerror("Hora inválida", f"Formato de hora inválido: {hora_normalizada}", parent=self.ventana)
            widget.set(self.placeholder_text)
            return

        horas_a_bloquear = []
        for h in self.horas:
            try:
                h_dt = datetime.strptime(h, "%H:%M")
                if inicio_dt <= h_dt <= fin_dt:
                    horas_a_bloquear.append(h)
            except Exception:
                continue

        # Guardar pending para no tocar JSON todavía
        self._pending_bloqueo = {
            "id_sede": id_sede_str,
            "fecha": fecha,
            "horas": horas_a_bloquear,
            "diferido": False,
            "duracion_minutos": duracion_minutos,
            "hora_inicio": hora_normalizada
        }
        print(f"[DEBUG] Pending bloqueo: {self._pending_bloqueo}")"""
        
        """if widget is None and event is not None:
            widget = event.widget
        if widget is None or widget != self.entry_combobox_hora_citacion:
            return

        # Validar identificación
        identificacion = self.entry_identificacion_paciente.get().strip()
        if not identificacion:
            messagebox.showwarning(
                "Falta identificación",
                "Debe ingresar la identificación del paciente antes de seleccionar la hora.",
                parent=self.ventana
            )
            widget.set(self.placeholder_text)
            return

        # Normalizar hora
        raw = widget.get().strip()
        hora_normalizada = self._normalizar_hora(raw)
        if hora_normalizada is None or hora_normalizada not in self.horas:
            return  # todavía escribiendo

        # Obtener fecha y sede actuales
        try:
            fecha = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
        except:
            messagebox.showerror("Fecha inválida", "No se pudo obtener la fecha de citación.", parent=self.ventana)
            widget.set(self.placeholder_text)
            return

        nombre_sede = self.entry_sede_paciente.get().strip()
        id_sede = self.obtener_id_sede(nombre_sede)
        if id_sede is None:
            messagebox.showwarning("Sede inválida", "No se pudo determinar la sede seleccionada.", parent=self.ventana)
            widget.set(self.placeholder_text)
            return
        id_sede_str = str(id_sede)

        # Detectar cambios respecto a los valores originales
        sede_original = str(self.paciente_modificar.get("sede"))
        fecha_original = self.paciente_modificar.get("fecha_citacion")
        hora_original = self.paciente_modificar.get("hora_citacion")

        try:
            fecha_original = datetime.strptime(fecha_original, "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            pass
        try:
            hora_original = hora_original[:5]
        except:
            pass

        hubo_cambio = not (
            sede_original == id_sede_str and
            fecha_original == fecha and
            hora_original == hora_normalizada
        )

        # Si no hubo cambio, no hacer nada
        if not hubo_cambio:
            print("[DEBUG] No hubo cambio de sede/fecha/hora → No bloquear ni validar.")
            self._pending_bloqueo = None
            return

        # --- Si es diferido ---
        if getattr(self, "var_diferido", None) and self.var_diferido.get() == 1:
            self._pending_bloqueo = {
                "id_sede": id_sede_str,
                "fecha": fecha,
                "horas": [hora_normalizada],
                "diferido": True
            }
            print(f"[DEBUG] Pending bloqueo (diferido): {self._pending_bloqueo}")
            return

        # Pedir duración si no se recibió
        if duracion_minutos is None:
            duracion_minutos = self._mostrar_dialogo_duracion()
            if duracion_minutos is None:
                widget.set(self.placeholder_text)
                return

        # Calcular rango de horas a bloquear
        try:
            inicio_dt = datetime.strptime(hora_normalizada, "%H:%M")
            fin_dt = inicio_dt + timedelta(minutes=duracion_minutos)
        except:
            messagebox.showerror("Hora inválida", f"Formato de hora inválido: {hora_normalizada}", parent=self.ventana)
            widget.set(self.placeholder_text)
            return

        horas_a_bloquear = [h for h in self.horas if inicio_dt <= datetime.strptime(h, "%H:%M") <= fin_dt]

        # Guardar en pending
        self._pending_bloqueo = {
            "id_sede": id_sede_str,
            "fecha": fecha,
            "horas": horas_a_bloquear,
            "diferido": False,
            "duracion_minutos": duracion_minutos,
            "hora_inicio": hora_normalizada,
            "hubo_cambio": True
        }

        print(f"[DEBUG] Pending bloqueo (CAMBIO REAL): {self._pending_bloqueo}")"""
        
        if widget is None and event is not None:
            widget = event.widget
        if widget is None or widget != self.entry_combobox_hora_citacion:
            return

        # Validar identificación
        identificacion = self.entry_identificacion_paciente.get().strip()
        if not identificacion:
            messagebox.showwarning(
                "Falta identificación",
                "Debe ingresar la identificación del paciente antes de seleccionar la hora.",
                parent=self.ventana
            )
            widget.set(self.placeholder_text)
            return

        # Normalizar hora
        raw = widget.get().strip()
        hora_normalizada = self._normalizar_hora(raw)
        if hora_normalizada is None or hora_normalizada not in self.horas:
            return  # todavía escribiendo

        # Obtener fecha y sede actuales
        try:
            fecha = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
        except:
            messagebox.showerror("Fecha inválida", "No se pudo obtener la fecha de citación.", parent=self.ventana)
            widget.set(self.placeholder_text)
            return

        nombre_sede = self.entry_sede_paciente.get().strip()
        id_sede = self.obtener_id_sede(nombre_sede)
        if id_sede is None:
            messagebox.showwarning("Sede inválida", "No se pudo determinar la sede seleccionada.", parent=self.ventana)
            widget.set(self.placeholder_text)
            return
        id_sede_str = str(id_sede)

        # Detectar cambios respecto a los valores originales
        sede_original = str(self.paciente_modificar.get("sede"))
        fecha_original = self.paciente_modificar.get("fecha_citacion")
        hora_original = self.paciente_modificar.get("hora_citacion")

        try:
            fecha_original = datetime.strptime(fecha_original, "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            try:
                fecha_original = datetime.strptime(fecha_original, "%d/%m/%Y").strftime("%d/%m/%Y")
            except:
                pass
        try:
            hora_original = str(hora_original)[:5]
        except:
            pass

        hubo_cambio = not (
            sede_original == id_sede_str and
            fecha_original == fecha and
            hora_original == hora_normalizada
        )

        # Si no hubo cambio, no hacer nada
        if not hubo_cambio:
            print("[DEBUG] No hubo cambio de sede/fecha/hora → No bloquear ni validar.")
            self._pending_bloqueo = None
            return

        # --- Si es diferido ---
        if getattr(self, "var_diferido", None) and self.var_diferido.get() == 1:
            self._pending_bloqueo = {
                "id_sede": id_sede_str,
                "fecha": fecha,
                "horas": [hora_normalizada],
                "diferido": True,
                "hora_inicio": hora_normalizada,
                "hubo_cambio": True
            }
            print(f"[DEBUG] Pending bloqueo (diferido): {self._pending_bloqueo}")
            return

        # Pedir duración si no se recibió
        if duracion_minutos is None:
            duracion_minutos = self._mostrar_dialogo_duracion()
            if duracion_minutos is None:
                widget.set(self.placeholder_text)
                return

        # Calcular rango de horas a bloquear
        try:
            inicio_dt = datetime.strptime(hora_normalizada, "%H:%M")
            fin_dt = inicio_dt + timedelta(minutes=duracion_minutos)
        except:
            messagebox.showerror("Hora inválida", f"Formato de hora inválido: {hora_normalizada}", parent=self.ventana)
            widget.set(self.placeholder_text)
            return

        horas_a_bloquear = [h for h in self.horas if inicio_dt <= datetime.strptime(h, "%H:%M") <= fin_dt]

        # Guardar en pending solo la clave y horas (para guardar detalles)
        self._pending_bloqueo = {
            "id_sede": id_sede_str,
            "fecha": fecha,
            "horas": horas_a_bloquear,
            "diferido": False,
            "duracion_minutos": duracion_minutos,
            "hora_inicio": hora_normalizada,
            "hubo_cambio": True
        }

        print(f"[DEBUG] Pending bloqueo (CAMBIO REAL): {self._pending_bloqueo}")
        
    def _al_seleccionar_hora(self, valor):
        
        """
        Se ejecuta automáticamente cuando se selecciona una hora en el CTkComboBox.
        """        
        hora_texto = valor.strip()
        hora_normalizada = self._normalizar_hora(hora_texto)
        if not hora_normalizada:
            return

        # Mostrar diálogo de duración (solo aquí)
        duracion = self._mostrar_dialogo_duracion()
        if duracion is None:
            # Canceló
            self.entry_combobox_hora_citacion.set(self.placeholder_text)
            return

        # Guardar duración seleccionada temporalmente (opcional)
        self.duracion_seleccionada = duracion

        # Llamar a bloquear pasando la duración para evitar abrir el diálogo otra vez
        # notar: bloqueamos llamando con el widget correspondiente
        self.bloquear_hora_tomada(None, self.entry_combobox_hora_citacion, duracion)
    
    # -------------------------------
    # Método que se llama al cambiar sede o fecha
    # -------------------------------
    def _on_cambio_sede_o_fecha(self, campo):
        """
        Limpiar combobox de hora y mostrar aviso solo si sede o fecha cambiaron.
        """
        """# Valores actuales
        if campo == "sede":
            valor_actual = self.entry_sede_paciente.get().strip()
            valor_original = str(self.paciente_modificar.get("sede"))
        elif campo == "fecha":
            try:
                valor_actual = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
            except:
                return
            valor_original = self.paciente_modificar.get("fecha_citacion")
            try:
                valor_original = datetime.strptime(valor_original, "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                pass
        else:
            return

        # Si hay cambio, mostrar aviso y limpiar combobox
        if valor_actual != valor_original:
            messagebox.showinfo(
                "Hora requerida",
                f"Ha cambiado la {campo}. Por favor, seleccione una nueva hora para actualizar correctamente la franja.",
                parent=self.ventana
            )
            self.entry_combobox_hora_citacion.set(self.placeholder_text)
            # Limpiar _pending_bloqueo previo, si existía
            if hasattr(self, "_pending_bloqueo"):
                self._pending_bloqueo = None"""
                
        try:
            if campo == "sede":
                valor_actual = self.entry_sede_paciente.get().strip()
                valor_original = str(self.paciente_modificar.get("sede"))
            elif campo == "fecha":
                try:
                    valor_actual = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
                except Exception:
                    return
                valor_original = self.paciente_modificar.get("fecha_citacion")
                try:
                    valor_original = datetime.strptime(valor_original, "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    pass
            else:
                return

            # Usar atributo para controlar que mensaje solo salga una vez por valor cambiado
            attr_last_value = f"_last_{campo}_value"
            ultimo_valor = getattr(self, attr_last_value, None)

            if valor_actual != valor_original and valor_actual != ultimo_valor:
                # Guardamos el valor actual para que no vuelva a salir hasta que cambie otra vez
                setattr(self, attr_last_value, valor_actual)

                # Resetear combobox de hora si existe
                if hasattr(self, "entry_combobox_hora_citacion"):
                    self.entry_combobox_hora_citacion.set(self.placeholder_text)
                    self.entry_combobox_hora_realizacion.set(self.placeholder_text)

                # Crear pending de bloqueo vacío para obligar nueva hora
                self._pending_bloqueo = None

                messagebox.showinfo(
                    "Hora requerida",
                    f"Ha cambiado la {campo}. Por favor, seleccione una nueva hora para actualizar correctamente la franja.",
                    parent=self.ventana
                )

            elif valor_actual == valor_original:
                # Si el valor vuelve al original, borramos el atributo
                if hasattr(self, attr_last_value):
                    delattr(self, attr_last_value)

        except Exception as e:
            print("[DEBUG] Error en _on_cambio_sede_o_fecha:", e)

    # -------------------------------
    # Método que se llama cuando el usuario selecciona una nueva hora
    # -------------------------------
    def _al_seleccionar_hora(self, hora):
        # Aquí ya se seleccionó correctamente la hora
        #self._aviso_hora_cambiada = False
        # Llamar a la función original que bloquea hora
        self.bloquear_hora_tomada(None, widget=self.entry_combobox_hora_citacion)
    
    @classmethod
    def actualizar_json_horas(cls):
        """Actualiza únicamente el JSON de horas (sin tocar widgets)."""
        try:
            cls.cargar_horas()
            cls.guardar_horas()
        except Exception as e:
            print(e)

    def actualizar_horas_disponibles(self, event=None):
            
        """Restaura la lista de horas disponibles al cambiar la fecha o la sede."""
        try:
            fecha = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
            nombre_sede = self.entry_sede_paciente.get().strip()
            id_sede = self.obtener_id_sede(nombre_sede)
            id_sede_str = str(id_sede) if id_sede is not None else None

            if id_sede_str and id_sede_str in self.horas_tomadas:
                # Normalizamos todas las horas a 'HH:MM' strings
                horas_ocupadas_raw = self.horas_tomadas[id_sede_str].get(fecha, [])
                horas_ocupadas = [
                    self._normalizar_hora(h) if isinstance(h, str) else f"{int(h)//100:02d}:{int(h)%100:02d}"
                    for h in horas_ocupadas_raw
                ]
            else:
                horas_ocupadas = []

            horas_disponibles = [h for h in self.horas if h not in horas_ocupadas]

            # Actualizar ambos combobox con las horas libres
            self.entry_combobox_hora_citacion.configure(values=horas_disponibles)
            self.entry_combobox_hora_realizacion.configure(values=horas_disponibles)

        except Exception as e:
            print(e)

    def _validar_hora_al_abrir_dropdown(self, event):
        
        """if getattr(self, "_mensaje_mostrado", False):
            return  # ya se mostró, no repetir

        widget = event.widget
        raw = widget.get().strip()
        hora_normalizada = self._normalizar_hora(raw)
        if not hora_normalizada:
            return

        try:
            fecha = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
        except Exception:
            return

        try:
            nombre_sede = self.entry_sede_paciente.get().strip()
            id_sede = self.obtener_id_sede(nombre_sede)
        except Exception:
            id_sede = None

        detalles = self.horas_tomadas.get("detalles", {})
        prefijo = f"{id_sede}_{fecha}_" if id_sede is not None else f"_{fecha}_"

        for clave, horas_lista in detalles.items():
            if not clave.startswith(prefijo):
                continue
            if not isinstance(horas_lista, list) or len(horas_lista) == 0:
                continue

            # 🔹 Normalizar todas las horas a strings HH:MM
            horas_lista = [self._normalizar_hora(h) for h in horas_lista if h is not None]
            if not horas_lista:
                continue

            hora_busq = hora_normalizada.split(":")[0]
            if any(h.split(":")[0] == hora_busq for h in horas_lista):
                inicio = min(horas_lista)
                fin = max(horas_lista)
                duracion_min = (len(horas_lista) - 1) * 5
                self._mensaje_mostrado = True
                return

        if id_sede is not None:
            horas_tomadas_dia = self.horas_tomadas.get(str(id_sede), {}).get(fecha, [])
            if hora_normalizada in horas_tomadas_dia:
                clave_busq = f"{id_sede}_{fecha}_{hora_normalizada}"
                horas_lista = detalles.get(clave_busq)
                if isinstance(horas_lista, list) and horas_lista:
                    horas_lista = [self._normalizar_hora(h) for h in horas_lista if h is not None]
                    inicio = min(horas_lista)
                    fin = max(horas_lista)
                    duracion_min = (len(horas_lista) - 1) * 5
                else:
                    duracion_min = self._calcular_duracion_estudio(fecha, hora_normalizada)
                    fin = (datetime.strptime(hora_normalizada, "%H:%M") + timedelta(minutes=duracion_min)).strftime("%H:%M")

                self._mensaje_mostrado = True
                messagebox.showwarning(
                    "Hora no disponible",
                    f"La hora {hora_normalizada} ya está ocupada para la sede {nombre_sede}.\n"
                    f"El estudio asignado dura {duracion_min} minutos (hasta {fin}).",
                    parent=self.ventana
                )"""
                
        # Resetear mensaje si el usuario borra la hora
        cb = self.entry_combobox_hora_citacion
        widget = event.widget
        raw = widget.get().strip()
        if not raw:
            self._mensaje_mostrado = False
            return

        # 🔹 Normalizar hora
        hora_normalizada = self._normalizar_hora(raw)
        if not hora_normalizada:
            return

        # 🔹 Obtener fecha
        try:
            fecha = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
        except Exception:
            return

        # 🔹 Obtener sede
        try:
            nombre_sede = self.entry_sede_paciente.get().strip()
            id_sede = self.obtener_id_sede(nombre_sede)
        except Exception:
            id_sede = None

        # 🔹 Preparar detalles y prefijo para búsqueda
        detalles = self.horas_tomadas.get("detalles", {})
        prefijo = f"{id_sede}_{fecha}_" if id_sede is not None else f"_{fecha}_"

        # 🔹 Validar solapamiento
        for clave, horas_lista in detalles.items():
            if not clave.startswith(prefijo):
                continue
            if not isinstance(horas_lista, list) or len(horas_lista) == 0:
                continue

            # Normalizar todas las horas a HH:MM
            horas_lista = [self._normalizar_hora(h) for h in horas_lista if h is not None]
            if not horas_lista:
                continue

            # Convertir a set para validar solapamiento exacto
            horas_set = set(horas_lista)
            if hora_normalizada in horas_set:
                inicio = min(horas_lista)
                fin = max(horas_lista)
                duracion_min = (len(horas_lista) - 1) * 5

                # 🔹 Mostrar mensaje solo si no se ha mostrado antes
                if not getattr(self, "_mensaje_mostrado", False):
                    self._mensaje_mostrado = True
                    messagebox.showwarning(
                        "Hora no disponible",
                        f"La hora {hora_normalizada} ya está ocupada para la sede {nombre_sede}.\n"
                        f"El estudio asignado dura {duracion_min} minutos (hasta {fin}).",
                        parent=self.ventana
                    )
                    cb.set(self.placeholder_text)

                # 🔹 Limpiar inmediatamente el combo
                widget.set('')
                return

        # 🔹 Si no hay solapamiento, permitir la selección
        self._mensaje_mostrado = False
    
    
    def cargar_horas(self):
        """Carga el diccionario de horas tomadas desde un archivo JSON."""
        """if os.path.exists("horas_tomadas.json"):
            try:
                with open("horas_tomadas.json", "r") as f:
                    PacientesModificar.horas_tomadas = json.load(f)
            except Exception as e:
                print("Error al cargar horas tomadas:", e)
                PacientesModificar.horas_tomadas = {}
        else:
            PacientesModificar.horas_tomadas = {}"""
            
        if os.path.exists("horas_tomadas.json"):
            try:
                with open("horas_tomadas.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Guardamos solo detalles, asegurándonos que exista la clave
                    self.horas_tomadas = {"detalles": data.get("detalles", {})}
            except Exception as e:
                print("[DEBUG] Error al cargar horas tomadas:", e)
                self.horas_tomadas = {"detalles": {}}
        else:
            self.horas_tomadas = {"detalles": {}}
    
    
    def guardar_horas(self):
            
        """
        Guarda o actualiza las horas tomadas de un paciente en horas_tomadas.json.
        Si hubo un cambio en sede, fecha o hora, reemplaza la clave vieja por la nueva.
        """
            
        """try:
            # Verificaciones básicas
            if not hasattr(self, "_pending_bloqueo") or not self._pending_bloqueo:
                print("[DEBUG] No hay _pending_bloqueo para guardar.")
                return

            pb = self._pending_bloqueo
            print("[DEBUG] _pending_bloqueo recibido:", pb)

            # Datos nuevos (lo que queremos guardar)
            id_sede_new = str(pb.get("id_sede"))
            fecha_new = pb.get("fecha")
            horas_list_new = pb.get("horas", [])
            hora_inicio_new = pb.get("hora_inicio") or (horas_list_new[0] if horas_list_new else None)
            clave_nueva = f"{id_sede_new}_{fecha_new}_{hora_inicio_new}" if hora_inicio_new else f"{id_sede_new}_{fecha_new}"

            # Asegurar estructura en memoria
            if not hasattr(self, "horas_tomadas") or not isinstance(self.horas_tomadas, dict):
                self.horas_tomadas = {"detalles": {}}
            self.horas_tomadas.setdefault("detalles", {})
            detalles = self.horas_tomadas["detalles"]

            # Obtener id_registro del paciente (solo para comparaciones en memoria/debug)
            id_registro = None
            try:
                id_registro = self.paciente_modificar.get("id_registro")
            except Exception:
                id_registro = None
            print(f"[DEBUG] id_registro (memoria): {id_registro!r}")

            # Determinar clave_vieja (preferimos la que venga en pending si existe)
            clave_vieja = pb.get("clave_vieja")
            if clave_vieja:
                print(f"[DEBUG] clave_vieja proporcionada en pending: {clave_vieja}")
            else:
                # Construimos clave_old_base a partir de los datos originales cargados en pantalla
                sede_orig = str(self.paciente_modificar.get("sede"))
                fecha_orig_raw = self.paciente_modificar.get("fecha_citacion")
                hora_orig_raw = self.paciente_modificar.get("hora_citacion")
                # Normalizar fecha original a dd/MM/YYYY (varios intentos)
                try:
                    fecha_orig_n = datetime.strptime(str(fecha_orig_raw), "%Y-%m-%d").strftime("%d/%m/%Y")
                except Exception:
                    try:
                        fecha_orig_n = datetime.strptime(str(fecha_orig_raw), "%d/%m/%Y").strftime("%d/%m/%Y")
                    except Exception:
                        fecha_orig_n = str(fecha_orig_raw)
                # Normalizar hora original a HH:MM
                try:
                    if isinstance(hora_orig_raw, timedelta):
                        total_seconds = int(hora_orig_raw.total_seconds())
                        hh = total_seconds // 3600
                        mm = (total_seconds % 3600) // 60
                        hora_orig_n = f"{hh:02d}:{mm:02d}"
                    else:
                        hora_orig_n = str(hora_orig_raw)[:5]
                except Exception:
                    hora_orig_n = str(hora_orig_raw)

                clave_old_base = f"{sede_orig}_{fecha_orig_n}_{hora_orig_n}"
                print(f"[DEBUG] clave_old_base (desde paciente_modificar): {clave_old_base}")

                # Buscar en detalles la clave que coincide con la base antigua EXACTA
                claves_posibles = [k for k in detalles.keys() if k.startswith(clave_old_base)]
                if claves_posibles:
                    # Si hay varias posibles, elegimos la que coincide exactamente con la base
                    # (esto es más seguro que usar startswith genérico)
                    clave_vieja = None
                    for k in claves_posibles:
                        if k == clave_old_base:
                            clave_vieja = k
                            break
                    if clave_vieja is None:
                        # fallback: tomar la primera coincidencia encontrada
                        clave_vieja = claves_posibles[0]
                    print(f"[DEBUG] claves_posibles encontradas para base antigua: {claves_posibles}")
                else:
                    print("[DEBUG] No se encontró clave vieja en JSON basada en clave_old_base.")
                    clave_vieja = None

            # Construir representaciones con id para debug (NO se guardan en JSON)
            clave_vieja_id = f"{clave_vieja}_{id_registro}" if clave_vieja and id_registro is not None else None
            clave_nueva_id = f"{clave_nueva}_{id_registro}" if id_registro is not None else None
            print(f"[DEBUG] clave_vieja (a usar): {clave_vieja}")
            print(f"[DEBUG] clave_vieja_id (memoria, NO guardada): {clave_vieja_id}")
            print(f"[DEBUG] clave_nueva (a guardar): {clave_nueva}")
            print(f"[DEBUG] clave_nueva_id (memoria, NO guardada): {clave_nueva_id}")

            # Funcion interna: intenta borrar la clave_vieja del JSON (si existe) y devuelve (True/False, motivo)
            def borrado_json(clave):
                try:
                    if clave in detalles:
                        del detalles[clave]
                        print(f"[DEBUG borrado_json] Eliminada clave del JSON: {clave}")
                        return True, "borrado_ok"
                    else:
                        print(f"[DEBUG borrado_json] La clave no existe en JSON: {clave}")
                        return False, "no_existia"
                except Exception as e:
                    tb = traceback.format_exc()
                    print(f"[ERROR borrado_json] Error borrando clave {clave}: {e}\n{tb}")
                    return False, f"error:{e}"

            # --- Lógica de decisión clara ---
            accion = None
            try:
                # Caso 1: si clave_vieja existe y es distinta a la nueva -> borrar vieja y agregar nueva
                if clave_vieja and clave_vieja != clave_nueva:
                    print(f"[DEBUG] clave_vieja encontrada y distinta a clave_nueva -> proceder a borrar y reemplazar.")
                    ok, motivo = borrado_json(clave_vieja)
                    if not ok:
                        # Si no pudimos borrar por alguna razón, mostramos error y SALIMOS sin guardar cambios
                        print(f"[ERROR guardar_horas] No se pudo borrar la clave vieja ({clave_vieja}) antes de guardar. Motivo: {motivo}")
                        return
                    # Después de borrar, si la nueva ya existe y tiene exactamente las mismas horas, no hacemos nada.
                    if clave_nueva in detalles and detalles[clave_nueva] == horas_list_new:
                        print("[DEBUG] Después de borrar la vieja, la clave nueva ya existe y tiene las mismas horas -> no se modifica JSON.")
                        accion = "no_hacer_nada_ya_existia"
                    else:
                        detalles[clave_nueva] = horas_list_new
                        accion = "reemplazar_por_nueva"
                        print(f"[DEBUG] Clave nueva guardada (reemplazo): {clave_nueva} -> {horas_list_new}")

                # Caso 2: no hay clave_vieja encontrada (nuevo caso) -> insertar nueva solamente
                elif not clave_vieja:
                    print("[DEBUG] No se detectó clave_vieja -> insertar clave nueva (si corresponde).")
                    if clave_nueva in detalles:
                        if detalles[clave_nueva] == horas_list_new:
                            print("[DEBUG] La clave nueva ya existe con los mismos valores de horas -> no se hace nada.")
                            accion = "no_hacer_nada_ya_existia"
                        else:
                            detalles[clave_nueva] = horas_list_new
                            accion = "actualizar_horas_existente"
                            print(f"[DEBUG] Actualizadas horas de clave existente: {clave_nueva} -> {horas_list_new}")
                    else:
                        detalles[clave_nueva] = horas_list_new
                        accion = "insertar_nueva"
                        print(f"[DEBUG] Clave nueva insertada: {clave_nueva} -> {horas_list_new}")

                # Caso 3: clave_vieja == clave_nueva -> posible edición interna de horas
                else:  # clave_vieja == clave_nueva
                    print("[DEBUG] clave_vieja igual a clave_nueva -> revisar horas.")
                    if detalles.get(clave_nueva) == horas_list_new:
                        print("[DEBUG] Horas idénticas -> no se hace nada.")
                        accion = "no_hacer_nada_igual"
                    else:
                        detalles[clave_nueva] = horas_list_new
                        accion = "actualizar_mismaclave"
                        print(f"[DEBUG] Horas de la misma clave actualizadas: {clave_nueva} -> {horas_list_new}")

            except Exception as e:
                print("[ERROR guardar_horas] Error durante la lógica de reemplazo:", e)
                import traceback as _tb
                print(_tb.format_exc())
                return

            # --- Escribir JSON (solo la sección detalles) ---
            try:
                json_a_guardar = {"detalles": detalles}
                with open("horas_tomadas.json", "w", encoding="utf-8") as f:
                    json.dump(json_a_guardar, f, indent=2, ensure_ascii=False)
                print("[DEBUG guardar_horas] Guardado final en JSON (solo 'detalles'):", list(detalles.keys()))
                print(f"[DEBUG guardar_horas] Acción tomada: {accion}")
            except Exception as e:
                print("[ERROR guardar_horas] Error escribiendo JSON:", e)
                import traceback as _tb
                print(_tb.format_exc())
                return
            finally:
                # Limpiar pending_bloqueo en memoria
                try:
                    self._pending_bloqueo = None
                except Exception:
                    pass

        except Exception as e:
            print("[ERROR guardar_horas] Error general:", e)
            import traceback
            traceback.print_exc()"""
        
        try:
            # Verificaciones básicas
            if not hasattr(self, "_pending_bloqueo") or not self._pending_bloqueo:
                print("[DEBUG] No hay _pending_bloqueo para guardar.")
                return

            pb = self._pending_bloqueo
            print("[DEBUG] _pending_bloqueo recibido:", pb)

            # Datos nuevos (lo que queremos guardar)
            id_sede_new = str(pb.get("id_sede"))
            fecha_new = pb.get("fecha")
            horas_list_new = pb.get("horas", [])
            hora_inicio_new = pb.get("hora_inicio") or (horas_list_new[0] if horas_list_new else None)
            clave_nueva = f"{id_sede_new}_{fecha_new}_{hora_inicio_new}" if hora_inicio_new else f"{id_sede_new}_{fecha_new}"

            # Asegurar estructura en memoria
            if not hasattr(self, "horas_tomadas") or not isinstance(self.horas_tomadas, dict):
                self.horas_tomadas = {"detalles": {}}
            self.horas_tomadas.setdefault("detalles", {})
            detalles = self.horas_tomadas["detalles"]

            # Obtener id_registro del paciente (solo para debug, no se usa en la lógica)
            id_registro = None
            try:
                id_registro = self.paciente_modificar.get("id_registro")
            except Exception:
                id_registro = None
            print(f"[DEBUG] id_registro (memoria): {id_registro!r}")

            # Determinar clave_vieja (preferimos la que venga en pending si existe)
            clave_vieja = pb.get("clave_vieja")
            if clave_vieja:
                print(f"[DEBUG] clave_vieja proporcionada en pending: {clave_vieja}")
            else:
                # Construimos clave_old_base a partir de los datos originales cargados en pantalla
                sede_orig = str(self.paciente_modificar.get("sede"))
                fecha_orig_raw = self.paciente_modificar.get("fecha_citacion")
                hora_orig_raw = self.paciente_modificar.get("hora_citacion")
                try:
                    fecha_orig_n = datetime.strptime(str(fecha_orig_raw), "%Y-%m-%d").strftime("%d/%m/%Y")
                except Exception:
                    try:
                        fecha_orig_n = datetime.strptime(str(fecha_orig_raw), "%d/%m/%Y").strftime("%d/%m/%Y")
                    except Exception:
                        fecha_orig_n = str(fecha_orig_raw)
                try:
                    if isinstance(hora_orig_raw, timedelta):
                        total_seconds = int(hora_orig_raw.total_seconds())
                        hh = total_seconds // 3600
                        mm = (total_seconds % 3600) // 60
                        hora_orig_n = f"{hh:02d}:{mm:02d}"
                    else:
                        hora_orig_n = str(hora_orig_raw)[:5]
                except Exception:
                    hora_orig_n = str(hora_orig_raw)

                clave_old_base = f"{sede_orig}_{fecha_orig_n}_{hora_orig_n}"
                claves_posibles = [k for k in detalles.keys() if k.startswith(clave_old_base)]
                if claves_posibles:
                    # priorizamos coincidencia exacta
                    clave_vieja = clave_old_base if clave_old_base in claves_posibles else claves_posibles[0]
                    print(f"[DEBUG] claves_posibles encontradas para base antigua: {claves_posibles}")
                    print(f"[DEBUG] clave_vieja detectada automaticamente: {clave_vieja}")
                else:
                    print("[DEBUG] No se encontró clave vieja en JSON basada en clave_old_base.")
                    clave_vieja = None

            print(f"[DEBUG] clave_vieja (a usar): {clave_vieja}")
            print(f"[DEBUG] clave_nueva (a guardar): {clave_nueva}")
            print(f"[DEBUG] horas_list_new: {horas_list_new}")

            # -------- VALIDACIÓN DE SOLAPAMIENTOS --------
            try:
                # Recolectar todas las horas existentes para la misma sede+fecha EXCLUYENDO clave_vieja
                base_nueva = f"{id_sede_new}_{fecha_new}_"
                horas_existentes = []
                claves_conflictivas = []
                for k, v in detalles.items():
                    if not k.startswith(base_nueva):
                        continue
                    # ignorar la clave vieja si corresponde (porque la vamos a reemplazar)
                    if clave_vieja and k == clave_vieja:
                        print(f"[DEBUG] Ignorando clave_vieja en chequeo de solapamiento: {k}")
                        continue
                    # v debería ser lista de horas
                    if isinstance(v, list):
                        horas_existentes.extend(v)
                        claves_conflictivas.append(k)

                # Normalizar y comparar sets (evita duplicados y orden)
                set_nuevo = set(horas_list_new)
                set_existente = set(horas_existentes)

                print(f"[DEBUG] horas existentes (excluyendo clave_vieja): {claves_conflictivas} -> {sorted(list(set_existente))}")

                # Intersección detecta solapamiento directo
                interseccion = set_nuevo.intersection(set_existente)
                if interseccion:
                    # Si hay intersección => conflicto, no guardar
                    print(f"[DEBUG] Conflicto detectado, intersección horas: {sorted(list(interseccion))}")
                    try:
                        messagebox.showwarning(
                            "Hora no disponible",
                            f"Las horas seleccionadas se solapan con horarios ya bloqueados para la sede {id_sede_new} en {fecha_new}.\n"
                            f"Horas en conflicto: {', '.join(sorted(list(interseccion)))}",
                            parent=self.ventana
                        )
                    except Exception:
                        # Si falla messagebox por algún motivo, al menos imprimimos
                        print("[DEBUG] No se pudo mostrar messagebox de advertencia (widget/ventana).")

                    # Resetear combobox de hora al placeholder
                    try:
                        self.entry_combobox_hora_citacion.set(self.placeholder_text)
                    except Exception:
                        try:
                            self.entry_combobox_hora_citacion.delete(0, "end")
                            self.entry_combobox_hora_citacion.insert(0, self.placeholder_text)
                        except Exception:
                            pass

                    # No seguimos con guardado
                    return
                else:
                    print("[DEBUG] No se detectaron solapamientos con otras claves (ok).")

            except Exception as e:
                print("[ERROR guardar_horas] Error durante validación de solapamientos:", e)
                import traceback as _tb
                print(_tb.format_exc())
                # En caso de error de validación, no proceder
                return

            # -------- LÓGICA ORIGINAL DE BORRADO/REEMPLAZO (se ejecuta solo si no hay solapamiento) --------
            def borrado_json(clave):
                try:
                    if clave in detalles:
                        del detalles[clave]
                        print(f"[DEBUG borrado_json] Eliminada clave del JSON: {clave}")
                        return True, "borrado_ok"
                    else:
                        print(f"[DEBUG borrado_json] La clave no existe en JSON: {clave}")
                        return False, "no_existia"
                except Exception as e:
                    tb = traceback.format_exc()
                    print(f"[ERROR borrado_json] Error borrando clave {clave}: {e}\n{tb}")
                    return False, f"error:{e}"

            accion = None
            try:
                # Caso 1: si clave_vieja existe y es distinta a la nueva -> borrar vieja y agregar nueva
                if clave_vieja and clave_vieja != clave_nueva:
                    print(f"[DEBUG] clave_vieja encontrada y distinta a clave_nueva -> proceder a borrar y reemplazar.")
                    ok, motivo = borrado_json(clave_vieja)
                    if not ok:
                        print(f"[ERROR guardar_horas] No se pudo borrar la clave vieja ({clave_vieja}) antes de guardar. Motivo: {motivo}")
                        return
                    if clave_nueva in detalles and detalles[clave_nueva] == horas_list_new:
                        print("[DEBUG] Después de borrar la vieja, la clave nueva ya existe y tiene las mismas horas -> no se modifica JSON.")
                        accion = "no_hacer_nada_ya_existia"
                    else:
                        detalles[clave_nueva] = horas_list_new
                        accion = "reemplazar_por_nueva"
                        print(f"[DEBUG] Clave nueva guardada (reemplazo): {clave_nueva} -> {horas_list_new}")

                # Caso 2: no hay clave_vieja encontrada -> insertar nueva solamente
                elif not clave_vieja:
                    print("[DEBUG] No se detectó clave_vieja -> insertar clave nueva (si corresponde).")
                    if clave_nueva in detalles:
                        if detalles[clave_nueva] == horas_list_new:
                            print("[DEBUG] La clave nueva ya existe con los mismos valores de horas -> no se hace nada.")
                            accion = "no_hacer_nada_ya_existia"
                        else:
                            detalles[clave_nueva] = horas_list_new
                            accion = "actualizar_horas_existente"
                            print(f"[DEBUG] Actualizadas horas de clave existente: {clave_nueva} -> {horas_list_new}")
                    else:
                        detalles[clave_nueva] = horas_list_new
                        accion = "insertar_nueva"
                        print(f"[DEBUG] Clave nueva insertada: {clave_nueva} -> {horas_list_new}")

                # Caso 3: clave_vieja == clave_nueva -> posible edición interna de horas
                else:  # clave_vieja == clave_nueva
                    print("[DEBUG] clave_vieja igual a clave_nueva -> revisar horas.")
                    if detalles.get(clave_nueva) == horas_list_new:
                        print("[DEBUG] Horas idénticas -> no se hace nada.")
                        accion = "no_hacer_nada_igual"
                    else:
                        detalles[clave_nueva] = horas_list_new
                        accion = "actualizar_mismaclave"
                        print(f"[DEBUG] Horas de la misma clave actualizadas: {clave_nueva} -> {horas_list_new}")

            except Exception as e:
                print("[ERROR guardar_horas] Error durante la lógica de reemplazo:", e)
                import traceback as _tb
                print(_tb.format_exc())
                return

            # --- Escribir JSON (solo la sección detalles) ---
            try:
                json_a_guardar = {"detalles": detalles}
                with open("horas_tomadas.json", "w", encoding="utf-8") as f:
                    json.dump(json_a_guardar, f, indent=2, ensure_ascii=False)
                print("[DEBUG guardar_horas] Guardado final en JSON (solo 'detalles'):", list(detalles.keys()))
                print(f"[DEBUG guardar_horas] Acción tomada: {accion}")
            except Exception as e:
                print("[ERROR guardar_horas] Error escribiendo JSON:", e)
                import traceback as _tb
                print(_tb.format_exc())
                return
            finally:
                # Limpiar pending_bloqueo en memoria
                try:
                    self._pending_bloqueo = None
                except Exception:
                    pass

        except Exception as e:
            print("[ERROR guardar_horas] Error general:", e)
            import traceback
            traceback.print_exc()
        
        
        
        
        
        
    
    # ==========================================================
    # VENTANA EMERGENTE PERSONALIZADA
    # ==========================================================
    def _mostrar_dialogo_duracion(self):
        
        """
        Muestra un cuadro emergente tipo messagebox con botones
        para seleccionar la duración del estudio.
        Devuelve los minutos seleccionados o None si se cancela.
        """
        dialogo = ctk.CTkToplevel(self.ventana)
        dialogo.title("Duración del estudio")
        dialogo.geometry("320x320")
        dialogo.resizable(False, False)
        dialogo.grab_set()  # Bloquea interacción con otras ventanas
        dialogo.focus_force()

        # Variable para guardar el resultado
        resultado = {"valor": None}

        # Etiqueta de texto
        label = ctk.CTkLabel(dialogo, text="¿Cuánto dura el estudio?", font=("Verdana", 14, "bold"))
        label.pack(pady=15)

        # Frame para botones
        frame_botones = ctk.CTkFrame(dialogo, fg_color="transparent")
        frame_botones.pack(pady=10)

        # Función auxiliar para asignar valor y cerrar
        def seleccionar(valor):
            resultado["valor"] = valor
            dialogo.destroy()

        # Botones de duración
        opciones = [
            ("30 minutos", 30),
            ("1 hora", 60),
            ("1 hora y 30 minutos", 90),
            ("2 horas", 120),
            ("2 horas y 30 minutos", 150),
        ]
        for texto, minutos in opciones:
            btn = ctk.CTkButton(frame_botones, 
                                text=texto, 
                                text_color='white',
                                width=200,
                                corner_radius=20,
                                fg_color='#00155C',
                                bg_color= 'white',
                                command=lambda m=minutos: seleccionar(m))
            btn.pack(pady=5)

        # Botón de cancelar (similar a “No”)
        btn_cancelar = ctk.CTkButton(dialogo, 
                                    text="Cancelar",
                                    text_color='white',
                                    corner_radius=20,
                                    fg_color='#00155C',
                                    bg_color= 'white',
                                    width=200,
                                    command=lambda: seleccionar(None))
        btn_cancelar.pack(pady=10)

        dialogo.wait_window()  # Esperar hasta que se cierre el diálogo
        return resultado["valor"]
    
    def verificar_hora_periodica(self):
        
        """cb = self.entry_combobox_hora_citacion
        valor_actual = cb.get().strip()

        if valor_actual and valor_actual != self.placeholder_text:
            digitos = ''.join(c for c in valor_actual if c.isdigit())
            if len(digitos) >= 2:
                try:
                    fecha = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
                except Exception:
                    fecha = None

                nombre_sede = self.entry_sede_paciente.get().strip()
                id_sede = self.obtener_id_sede(nombre_sede)

                if fecha and id_sede:
                    id_sede = str(id_sede)
                    detalles = PacientesModificar.horas_tomadas.get("detalles", {})

                    for clave_detalle in detalles.keys():
                        if clave_detalle.startswith(f"{id_sede}_{fecha}_{valor_actual}"):
                            if getattr(self, "_ultima_hora_mostrada", None) == clave_detalle:
                                break

                            self._ultima_hora_mostrada = clave_detalle

                            horas_lista = detalles[clave_detalle]
                            if isinstance(horas_lista, list):
                                # 🔹 Normalizamos todas las horas antes de min/max
                                horas_lista = [self._normalizar_hora(h) for h in horas_lista if h is not None]

                            inicio = min(horas_lista)
                            fin = max(horas_lista)
                            duracion_calc = (len(horas_lista) - 1) * 5 if horas_lista else 0

                            print(f"[DEBUG verificar_hora_periodica] Mostrando mensaje para: {clave_detalle}")
                            messagebox.showwarning(
                                "Hora no disponible",
                                f"Ya existe un estudio en la sede {nombre_sede} para {fecha}.\n"
                                f"Comienza a las {inicio}, finaliza a las {fin}.\n"
                                f"Duración: {duracion_calc} minutos.",
                                parent=self.ventana
                            )
                            cb.set(self.placeholder_text)
                            break
                    else:
                        self._ultima_hora_mostrada = None

        cb.after(400, self.verificar_hora_periodica)"""
        
        cb = self.entry_combobox_hora_citacion
        valor_actual = cb.get().strip()

        if valor_actual and valor_actual != self.placeholder_text:
            # Validamos que haya al menos 2 dígitos
            digitos = ''.join(c for c in valor_actual if c.isdigit())
            if len(digitos) >= 2:
                try:
                    fecha = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
                except Exception:
                    fecha = None

                nombre_sede = self.entry_sede_paciente.get().strip()
                id_sede = self.obtener_id_sede(nombre_sede)

                if fecha and id_sede:
                    id_sede_str = str(id_sede)
                    detalles = PacientesModificar.horas_tomadas.get("detalles", {})

                    # Recorremos todas las claves de detalles
                    for clave_detalle, horas_lista in detalles.items():
                        # Ignoramos temporalmente las claves en el set de supresión
                        if getattr(self, "_suppress_detalle_keys", None) and clave_detalle in self._suppress_detalle_keys:
                            continue

                        # Revisamos si la clave pertenece a la sede/fecha/hora actual
                        if not clave_detalle.startswith(f"{id_sede_str}_{fecha}_{valor_actual}"):
                            continue

                        # Evitamos mostrar repetidamente el mismo warning
                        if getattr(self, "_ultima_hora_mostrada", None) == clave_detalle:
                            break

                        self._ultima_hora_mostrada = clave_detalle

                        if isinstance(horas_lista, list):
                            # Normalizamos todas las horas
                            horas_lista_norm = [self._normalizar_hora(h) for h in horas_lista if h is not None]
                            if horas_lista_norm:
                                inicio = min(horas_lista_norm)
                                fin = max(horas_lista_norm)
                                duracion_calc = (len(horas_lista_norm) - 1) * 5  # asumiendo intervalos de 5 min
                            else:
                                inicio = fin = duracion_calc = "desconocido"

                            print(f"[DEBUG verificar_hora_periodica] Mostrando mensaje para: {clave_detalle}")
                            messagebox.showwarning(
                                "Hora no disponible",
                                f"Ya existe un estudio en la sede {nombre_sede} para {fecha}.\n"
                                f"Comienza a las {inicio}, finaliza a las {fin}.\n"
                                f"Duración: {duracion_calc} minutos.",
                                parent=self.ventana
                            )
                            cb.set(self.placeholder_text)
                            break
                    else:
                        self._ultima_hora_mostrada = None
    
    def mostrar(self):
        
        self.modificar_datos()
        modificacion_realizada()
        cerrar_ppal(self.frame3.winfo_toplevel())
        