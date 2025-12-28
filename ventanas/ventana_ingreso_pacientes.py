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

from ventanas.visualizar_datos_ppal import PanelPrincipalVisualizacion

from usuarioactual.usuario_actual import UsuarioActual

from datetime import datetime, date, timedelta, time

from tkinter import messagebox

from tkcalendar import DateEntry # Widget calendario para seleccionar fechas

from conexion_DB.conexionDB import Conexion_DB # Importa la clase Conexion_DB desde el módulo conexion_DB.conexionDB para la conexión con la base de datos

# Importa funciones para abrir ventanas emergentes
from abrirventanasemergentes.abrir_ventanas import (abrir_ventana_conn_exito, 
                                                    abrir_ventana_conn_fallida,
                                                    datos_ingresados,
                                                    tamano_edad_incorrecta,
                                                    edad_incorrecta,
                                                    edad_fuera_rango,
                                                    cerrar_conexion
                                                    )

# Clase para la ventana de modificación de pacientes
class IngresarPacientes():
    
    horas_tomadas = {}
    conexion_realizada = False # Variable de clase para indicar si ya se realizó la conexión a la base de datos
    db = None # Variable de clase para almacenar la conexión a la base de datos
    
    # Constructor de la clase que recibe la ventana y el paciente a modificar
    def __init__(self, ventana, parent_window=None):
        
        self.parent_window = parent_window  # ← esta es la ventana principal real
        self.ventana = ventana
        
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir)

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
        
        if IngresarPacientes.db is None or IngresarPacientes.db.cursor is None:
            try:
                IngresarPacientes.db = Conexion_DB()
                IngresarPacientes.db.conectar()
                abrir_ventana_conn_exito()
            except:
                abrir_ventana_conn_fallida()

        self.db = IngresarPacientes.db
        
        # Diccionario con estilos de fuente para los textos
        self.fonts = {

            "title": ("Verdana", 26, 'bold'),

            "title_frame": ("Verdana", 22, 'bold'),

            "label": ("Verdana", 12, 'bold'),
            
            "label_etiqueta": ("Verdana", 14, 'bold'),
            
            "label_boton": ("Verdana", 14, 'bold'),
            
            "date": ("Verdana", 12, 'bold')

        }
        
        # se obtiene la informacion de la base de datos para luego ponerla en los entrys
        self.rangos_extraidos = self.obtener_rango_edad()
        self.modalidades_extraidas = self.obtener_modalidades()
        self.estado_extraido = self.obtener_estado()
        self.sedes_extraidas = self.obtener_sede()
        self.alergias_extraidas = self.obtener_alergia()
        self.aislamiento_extraido = self.obtener_aislamientos()
        self.estudio_extraido = []
        self.causales_retrasos_extraidos = self.obtener_causal_retraso()
        self.horas_extraidas = self.obtener_hora_citacion_realizacion()

        # se crean los contenidos de visualización para el usuario
        self.contenidotituloppal()
        self.contenidosframe1()
        self.contenidosframe2()
        self.contenidosframe3()
        
        # Registrar validación mientras escribe
        vcmd = self.entry_edad_paciente.register(self.validar_edad_key)
        self.entry_edad_paciente.configure(validate="key", validatecommand=(vcmd, "%P"))

        # Asociar evento al perder foco
        self.entry_edad_paciente.bind("<FocusOut>", self.validar_edad_final)
        
        # Bind que activa la función al hacer clic o doble clic
        self.entry_texto_est_ord.bind("<ButtonRelease-1>", self.agregar_seleccion_a_lista)
        #self.entry_texto_est_ord.bind("<Double-Button-1>", self.agregar_seleccion_a_lista)
        
        # Cambiar cursor al pasar el mouse (como hipervínculo)
        self.entry_texto_est_ord.bind("<Enter>", lambda e: self.entry_texto_est_ord.configure(cursor="hand2"))
        self.entry_texto_est_ord.bind("<Leave>", lambda e: self.entry_texto_est_ord.configure(cursor="xterm"))
        
        self.cargar_horas()
        self._mensaje_mostrado = False  # atributo de la clase

    # Devuelve la ventana actual
    def obtener_ventana(self):
        
        return self.ventana
    
    # parte de la visualizacion de la información
    
    def contenidotituloppal(self):
        
        self.titulo = ctk.CTkLabel(self.frame_sup, text='Ingresar Datos Del Paciente', font=self.fonts['title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.titulo.grid(row=0, column=0, columnspan=3, pady = 5, sticky="nsew") 
    
    def contenidosframe1(self):

        self.titulo_frame = ctk.CTkLabel(self.frame_sup1, text='Datos Del Paciente', font=self.fonts['title_frame'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.titulo_frame.grid(row=0, column=0, pady = 5, padx = 10, sticky='nsew')
        
        self.lab_identificacion = ctk.CTkLabel(self.frame1, text='Identificación Del Paciente', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_identificacion.grid(row=0, column=0, columnspan=2, sticky='ew')
        
        self.entry_identificacion_paciente = ctk.CTkEntry(self.frame1, 
                                                    font=self.fonts['label'],
                                                    width= 250,
                                                    height= 26,
                                                    fg_color='lightgray',
                                                    bg_color='white',
                                                    corner_radius=10,
                                                    text_color='black'
                                                    )
        self.entry_identificacion_paciente.grid(row=1, column=0, padx= 15, pady= 4, columnspan=2, sticky='nsew')
        
        self.lab_nombre = ctk.CTkLabel(self.frame1, text='Nombre Del Paciente', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_nombre.grid(row=2, column=0, pady= 4, columnspan=2, sticky='nsew')
        
        self.entry_nombre_paciente = ctk.CTkEntry(self.frame1, 
                                            font=self.fonts['label'],
                                            width= 550,
                                            height= 26,
                                            fg_color='lightgray',
                                            bg_color='white',
                                            corner_radius=10,
                                            text_color='black'
                                            )
        self.entry_nombre_paciente.grid(row=3, column=0, padx= 15, pady= 4, columnspan=2, sticky='nsew')
        
        self.entry_nombre_paciente.bind("<KeyRelease>", self.poner_title_nombre)
        
        self.lab_edad = ctk.CTkLabel(self.frame1, text='Edad', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
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
        
        self.lab_rango_edad = ctk.CTkLabel(self.frame1, text='Rango Edad', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
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
        
        self.llenar_combobox_rango_edad()
        
        self.lab_historia_clin = ctk.CTkLabel(self.frame1, text='Historia Clinica', font=self.fonts['label_etiqueta'], fg_color='white',bg_color='white', text_color= "#484a4b")
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
        
        self.lab_ubicacion = ctk.CTkLabel(self.frame1, text='Ubicación Paciente', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_ubicacion.grid(row=8, column=0, pady= 5, columnspan=2, sticky='nsew')
        
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
        
        self.lab_sede = ctk.CTkLabel(self.frame1, text='Sede', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_sede.grid(row=10, column=0, pady= 8, columnspan=2, sticky='nsew')
        
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
        
        self.llenar_combobox_sedes()
        
        # Frame contenedor solo para los radios
        self.frame_radios = ctk.CTkFrame(self.frame1, fg_color="white",bg_color='white')
        self.frame_radios.grid(row=12, column=0, columnspan=3, sticky="nsew")

        # Configura 2 columnas en el sub-frame
        self.frame_radios.grid_rowconfigure(0, weight=1)
        self.frame_radios.grid_rowconfigure(1, weight=1)
        self.frame_radios.grid_columnconfigure(0, weight=1)
        self.frame_radios.grid_columnconfigure(1, weight=1)
        
        self.lab_alergias_paciente = ctk.CTkLabel(self.frame_radios, text='Alergias', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_alergias_paciente.grid(row=0, column=0, columnspan=2, pady= 4, sticky='nsew')
        
        self.var_alergias = tk.IntVar(value=2)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_alergias1 = ctk.CTkRadioButton(self.frame_radios,
                                        text="Sí",
                                        variable = self.var_alergias,
                                        value=1,
                                        font=self.fonts['label_etiqueta'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray',
                                        command=self.llenar_combobox_alergia,
                                        )
        self.radio_alergias1.grid(row=1, column=0, padx=55, sticky='ew')

        # Botón de opción 2
        self.radio_alergias2 = ctk.CTkRadioButton(self.frame_radios,
                                        text="No",
                                        variable = self.var_alergias,
                                        value=0,
                                        font=self.fonts['label_etiqueta'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray',
                                        command=self.llenar_combobox_alergia,
                                        )
        self.radio_alergias2.grid(row=1, column=1, sticky='nsew')
        
        self.lab_tipo_alergia = ctk.CTkLabel(self.frame_radios, text='Selección de Alergias', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_tipo_alergia.grid(row=0, column= 2, pady= 4, sticky='nsew')
        
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
        
        self.llenar_combobox_alergia()
        
        self.lab_alergias_paciente = ctk.CTkLabel(self.frame1, text='Alergias del Paciente', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
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
                                    border_color='black',
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
        
        self.lab_aislamiento_paciente = ctk.CTkLabel(self.frame_radios1, text='Aislamiento', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_aislamiento_paciente.grid(row=0, column=0, columnspan=2, pady= 4, sticky='nsew')
        
        self.var_aislamiento = tk.IntVar(value=2)  # Valor predeterminado es No

        # Botón de opción 1
        self.radio_aislamiento1 = ctk.CTkRadioButton(self.frame_radios1,
                                            text="Sí",
                                            variable = self.var_aislamiento,
                                            value=1,
                                            font=self.fonts['label_etiqueta'],
                                            fg_color= 'black',
                                            bg_color='white',
                                            border_color= 'lightgray',
                                            command= self.llenar_combobox_aislamiento
                                            )
        self.radio_aislamiento1.grid(row=1, column=0, padx=55, sticky='ew')

        # Botón de opción 2
        self.radio_aislamiento2 = ctk.CTkRadioButton(self.frame_radios1,
                                            text="No",
                                            variable = self.var_aislamiento,
                                            value=0,
                                            font=self.fonts['label_etiqueta'],
                                            fg_color= 'black',
                                            bg_color='white',
                                            border_color= 'lightgray',
                                            command= self.llenar_combobox_aislamiento
                                            )
        self.radio_aislamiento2.grid(row=1, column=1, sticky='ew')
        
        self.lab_tipo_aislamiento = ctk.CTkLabel(self.frame_radios1, text='Selección De Aislamientos', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
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
        
        self.llenar_combobox_aislamiento()
        
        self.lab_aislam_paciente = ctk.CTkLabel(self.frame1, text='Aislamientos del Paciente', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_aislam_paciente.grid(row=16, column=0, pady = 4, columnspan = 2, sticky='nsew')
        
        self.entry_texto_aislamientos_paciente = ctk.CTkTextbox(self.frame1,
                                    wrap=tk.WORD,
                                    height=50,
                                    width=560,
                                    fg_color="lightgray",
                                    bg_color= 'white',
                                    corner_radius= 10,
                                    font= self.fonts['label'],
                                    text_color='black',
                                    border_color='black',
                                    scrollbar_button_color= "lightgreen"
                                    )
        self.entry_texto_aislamientos_paciente.configure(state="disable")
        self.entry_texto_aislamientos_paciente.grid(row=17, column=0, columnspan= 2, pady= 4, padx= 15, sticky='nsew')
        
        self.lab_estado = ctk.CTkLabel(self.frame1, text='Estado', font=self.fonts['label_etiqueta'], fg_color='white', bg_color='white', text_color= "#484a4b")
        self.lab_estado.grid(row=18, column= 0, pady=4, columnspan=2, sticky='nsew')
        
        self.entry_estado_paciente = ctk.CTkOptionMenu(self.frame1,
                                                font=self.fonts['label'],
                                                state="disable",
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
        self.entry_estado_paciente.grid(row=19, column= 0, padx= 15, pady= 4, columnspan=2, sticky='nsew')
        
        self.llenar_combobox_estados()
    
    def contenidosframe2 (self):
        
        self.titulo = ctk.CTkLabel(self.frame_sup1, text='Datos Del Estudio', font= self.fonts['title_frame'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.titulo.grid(row=0, column=1, sticky='nsew')
        
        self.lab_fecha_orden = ctk.CTkLabel(self.frame2, font= self.fonts['label_etiqueta'], fg_color= 'white', text='Fecha De La Orden', bg_color= 'white', text_color= "#484a4b")
        self.lab_fecha_orden.grid(row= 0, column= 0, sticky= 'nsew', pady= 4)
        
        self.entry_fecha_orden = DateEntry(self.frame2,
                                    width=20,
                                    background="lightgray",
                                    foreground='white',
                                    date_pattern= 'dd/MM/yyyy',
                                    font=self.fonts['date'],
                                    locale = 'es')
        self.entry_fecha_orden.grid(row=1, column=0, pady=4, padx=15, sticky='nsew')
        
        hoy = date.today()
        
        self.entry_fecha_orden.set_date(hoy)
        
        self.lab_fecha_citacion = ctk.CTkLabel(self.frame2, font= self.fonts['label_etiqueta'], fg_color= 'white', text='Fecha De La Cita', bg_color= 'white', text_color= "#484a4b")
        self.lab_fecha_citacion.grid(row= 2, column= 0, sticky= 'nsew', pady= 8)
        
        self.entry_fecha_cita = DateEntry(self.frame2,
                                width=20,
                                background= "laightgray",
                                foreground='white',
                                date_pattern= 'dd/MM/yyyy',
                                font= self.fonts['date'],
                                locale = 'es'
                                )
        self.entry_fecha_cita.grid(row=3, column=0, pady=4, padx=15, sticky='nsew')
        
        self.entry_fecha_cita.set_date(hoy)
        self.entry_fecha_cita.bind("<<DateEntrySelected>>", lambda e: self.ejecutar_cambio_fecha())

        self.lab_modalidad = ctk.CTkLabel(self.frame2, text='Modalidad', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
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
        
        self.llenar_combobox_modalidad()
        
        self.lab_estud_ordenados = ctk.CTkLabel(self.frame2, text='Lista de Estudios', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_estud_ordenados.grid(row=6, column=0, pady = 4, sticky='nsew')
        
        self.entry_texto_est_ord = ctk.CTkTextbox(self.frame2,
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
        self.entry_texto_est_ord.configure(state="disable")
        self.entry_texto_est_ord.grid(row=7, column=0, columnspan= 4, pady=4, padx= 15, sticky='nsew')
        
        self.llenar_textbox_estudios()
        
        self.lab_estud_ordenados = ctk.CTkLabel(self.frame2, text='Estudios Ordenados Al Paciente', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_estud_ordenados.grid(row=8, column=0, pady = 4, sticky='nsew')
        
        self.entry_list_estud_ordenados = ctk.CTkTextbox(self.frame2,
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
        self.entry_list_estud_ordenados.configure(state= 'disable')
        self.entry_list_estud_ordenados.grid(row=9, column=0, columnspan= 4, pady=4, padx= 15, sticky='nsew')
        
        self.lab_estud_ordenados = ctk.CTkLabel(self.frame2, text='Buscador de Estudios', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
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
        
        self.lab_ayuno_paciente = ctk.CTkLabel(self.frame_radios2, text='Ayuno', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_ayuno_paciente.grid(row=0, column=0, columnspan = 2, pady = 2, sticky='nsew')
        
        self.var_ayuno = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_ayuno1 = ctk.CTkRadioButton(self.frame_radios2,
                                    text="Sí",
                                    variable = self.var_ayuno,
                                    value=1,
                                    font= self.fonts['label_etiqueta'],
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
                                    font= self.fonts['label_etiqueta'],
                                    bg_color= 'white',
                                    fg_color= 'black',
                                    border_color= 'lightgray'
                                    )
        self.radio_ayuno2.grid(row=1, column=1, sticky='nsew')
        
        self.lab_diferido_paciente = ctk.CTkLabel(self.frame_radios2, text='Diferido', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_diferido_paciente.grid(row=0, column=2, columnspan = 2, pady = 2, sticky='nsew')
        
        self.var_diferido = tk.IntVar(value=0)  # Valor predeterminado es No

        # Botón de opción 1
        self.radio_diferido1 = ctk.CTkRadioButton(self.frame_radios2,
                                        text="Sí",
                                        variable = self.var_diferido,
                                        value=1,
                                        font= self.fonts['label_etiqueta'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray'
                                        )
        self.radio_diferido1.grid(row=1, column=2, padx=12, sticky='nsew')

        # Botón de opción 2
        self.radio_diferido2 = ctk.CTkRadioButton(self.frame_radios2,
                                        text="No",
                                        variable = self.var_diferido,
                                        value=0,
                                        font= self.fonts['label_etiqueta'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray'
                                        )
        self.radio_diferido2.grid(row=1, column=3, sticky='nsew')
        
        self.lab_autorizacion_paciente = ctk.CTkLabel(self.frame_radios2, text='Autorización', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_autorizacion_paciente.grid(row=2, column=0, columnspan =2, pady = 2, sticky='nsew')
        
        self.var_autorizacion = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_autorizacion1 = ctk.CTkRadioButton(self.frame_radios2,
                                            text="Sí",
                                            variable = self.var_autorizacion,
                                            value=1,
                                            font= self.fonts['label_etiqueta'],
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
                                            font= self.fonts['label_etiqueta'],
                                            bg_color= 'white',
                                            fg_color= "#d2455b",
                                            border_color= 'lightgray'
                                            )
        self.radio_autorizacion2.grid(row=3, column=1, sticky='nsew')
        
        self.lab_anestesia_paciente = ctk.CTkLabel(self.frame_radios2, text='Anestesia', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_anestesia_paciente.grid(row=2, column= 2, columnspan = 2, pady = 2, sticky='nsew')
        
        self.var_anestesia = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_anestesia1 = ctk.CTkRadioButton(self.frame_radios2,
                                        text="Sí",
                                        variable = self.var_anestesia,
                                        value=1,
                                        font= self.fonts['label_etiqueta'],
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
                                        font= self.fonts['label_etiqueta'],
                                        bg_color= 'white',
                                        fg_color= 'black',
                                        border_color= 'lightgray'
                                        )
        self.radio_anestesia2.grid(row=3, column=3, sticky='nsew')
        
        self.lab_diagnostico = ctk.CTkLabel(self.frame2, text='Diagnóstico', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_diagnostico.grid(row=13, column=0, pady = 4, sticky='nsew')
        
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
    
    def contenidosframe3 (self):
        
        self.titulo = ctk.CTkLabel(self.frame_sup1, text='Realización Del Estudio', fg_color='white', font=self.fonts['title_frame'], bg_color= 'white', text_color= "#484a4b")
        self.titulo.grid(row=0, column=2, sticky='nsew')
        
        self.lab_hora_citacion = ctk.CTkLabel(self.frame3, font=self.fonts['label_etiqueta'], fg_color= 'white', text='Hora De La Cita', bg_color= 'white', text_color= "#484a4b")
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
                                                    command=self.ejecutar_cambio_hora
                                                    #command=self._al_seleccionar_hora
                                                    )
        self.entry_combobox_hora_citacion.grid(row=1, column=0, pady=4, padx=15, sticky='nsew')
        
        # Vincular el evento de escritura
        self.entry_combobox_hora_citacion.set(self.placeholder_text)
        cb = self.entry_combobox_hora_citacion        
        cb.bind("<FocusIn>", lambda e, w=cb: self._clear_placeholder(e, w))
        cb.bind("<FocusOut>", lambda e, w=cb: self.ejecutar_cambio_hora(e, w))
        
        # Click: actualizar filtro
        cb.bind("<Button-1>", lambda e, w=cb: self.filtrar_horas(e, w))

        # Tecla: SOLO filtrar, nada más
        cb.bind("<KeyRelease>", lambda e, w=cb: self.filtrar_horas(e, w))
        cb.bind("<KeyRelease>", lambda e: self._validar_hora_al_abrir_dropdown(e))
        
        # Iniciar verificación periódica automática
        self.verificar_hora_periodica()
        
        self.lab_hora_realizacion = ctk.CTkLabel(self.frame3, font=self.fonts['label_etiqueta'], fg_color= 'white', text='Hora Realización Estudio', bg_color= 'white', text_color= "#484a4b")
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
                                                    values=self.horas,
                                                    command=self.ejecutar_cambio_hora
                                                    )
        self.entry_combobox_hora_realizacion.grid(row=3, column=0, pady=4, padx=15, sticky='nsew')
        
        self.entry_combobox_hora_realizacion.set(self.placeholder_text)
            
        cb = self.entry_combobox_hora_realizacion
        cb.bind("<FocusIn>", lambda e, w=cb: self._clear_placeholder(e, w))
        cb.bind("<<ComboboxSelected>>", self.ejecutar_cambio_hora)
        cb.bind("<KeyRelease>", lambda e, w=cb: self.filtrar_horas(e, w))
        
        self.lab_causal_retraso = ctk.CTkLabel(self.frame3, font=self.fonts['label_etiqueta'], fg_color= 'white', text='Causal Del Retraso', bg_color= 'white', text_color= "#484a4b")
        self.lab_causal_retraso.grid(row = 4, column = 0, sticky = 'nsew', pady=8)
        
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
        
        self.llenar_combobox_causal_retraso()
        
        self.lab_coment_tecnologo = ctk.CTkLabel(self.frame3, text='Comentarios Tecnólogo', font=self.fonts['label_etiqueta'], fg_color='white', text_color= "#484a4b")
        self.lab_coment_tecnologo.grid(row=6, column=0, pady = 4, sticky='nsew')
        
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
        self.frame_radios.grid(row=8, column=0, columnspan =2, pady = 4, sticky="nsew")

        # Configura 2 columnas en el sub-frame
        self.frame_radios.grid_rowconfigure(0, weight=1)
        self.frame_radios.grid_rowconfigure(1, weight=1)
        self.frame_radios.grid_columnconfigure(0, weight=1)
        self.frame_radios.grid_columnconfigure(1, weight=1)
        
        self.lab_coment_al_radiologo = ctk.CTkLabel(self.frame_radios, font=self.fonts['label_etiqueta'], fg_color= 'white', text='Comentar Estudio Con Radiólogo', bg_color= 'white', text_color= "#484a4b")
        self.lab_coment_al_radiologo.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')
        
        self.var_coment_al_rad = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        self.radio_coment_radiologo1 = ctk.CTkRadioButton(self.frame_radios,
                                                    text="Sí", 
                                                    variable = self.var_coment_al_rad, 
                                                    value=1, font=self.fonts['label_etiqueta'], 
                                                    bg_color= 'white',
                                                    fg_color= 'black',
                                                    border_color= 'lightgray'
                                                    )
        self.radio_coment_radiologo1.grid(row=1, column=0, padx=150, pady= 10, sticky='nsew')

        # Botón de opción 2
        self.radio_coment_radiologo2 = ctk.CTkRadioButton(self.frame_radios, 
                                                    text="No",
                                                    variable = self.var_coment_al_rad,
                                                    value=0, font=self.fonts['label_etiqueta'],
                                                    bg_color= 'white',
                                                    fg_color= 'black',
                                                    border_color= 'lightgray')
        self.radio_coment_radiologo2.grid(row=1, column=1, pady= 10, sticky='nsew')
        
        self.lab_coment_radiologo = ctk.CTkLabel(self.frame3, text='Comentarios Radiólogo', font=self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
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
        self.frame_buttons.grid(row= 11, column=0, sticky='nsew', padx= 15, pady= 8)
        
        # Configura las columnas dentro de frame_buttons para que se expandan
        self.frame_buttons.grid_columnconfigure(list(range(3)), weight=1)

        self.frame_buttons.grid_rowconfigure(0, weight=1)
        
        self.btn_agregar_paciente = ctk.CTkButton(self.frame_buttons,
                                text='Agregar Paciente',
                                text_color='white',
                                font=self.fonts['label_boton'],
                                width=20,
                                height=50,
                                corner_radius=20,
                                fg_color='#00155C',
                                bg_color= 'white',
                                hover_color = 'lightgreen',
                                anchor='center',
                                command= self.agregar_datos
                                )
        
        self.btn_agregar_paciente.grid(row= 0, column= 0, padx= 8, pady= 70, sticky='nsew')
        
        self.btn_limpiar = ctk.CTkButton(self.frame_buttons,
                                text='Limpiar Pantalla',
                                text_color='white',
                                font=self.fonts['label_boton'],
                                width=20,
                                height=50,
                                corner_radius=20,
                                fg_color='#00155C',
                                bg_color= 'white',
                                hover_color = 'lightgreen',
                                anchor='center',
                                command= self.limpiar_campos
                                )
        
        self.btn_limpiar.grid(row= 0, column= 1, padx= 8, pady= 70, sticky='nsew')
        
        self.btn_atras = ctk.CTkButton(self.frame_buttons,
                                text='Atrás',
                                text_color='white',
                                font=self.fonts['label_boton'],
                                width=20,
                                height=50,
                                corner_radius=20,
                                fg_color='#00155C',
                                bg_color= 'white',
                                hover_color = 'lightgreen',
                                anchor='center',
                                command= self.salir #lambda: cerrar_ppal(self.frame3.winfo_toplevel())
                                )
        
        self.btn_atras.grid(row= 0, column= 2, padx= 8, pady= 70, sticky='nsew')

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
    
    def actualizar_estudios(self, event=None):
        
        self.estudio_extraido = self.obtener_estudios_ordenados()
        self.llenar_textbox_estudios()
    
    def obtener_hora_citacion_realizacion(self):

        """Obtiene todos los ids con su hora de citación y hora estudio y los devuelve como lista de diccionarios."""
        
        self.horas = []
        
        sql = "SELECT identificacion_paciente, hora_citacion, hora_realizacion FROM registrospacientes"
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
        self.entry_rango_edad_paciente.set(opciones[0])

    def llenar_combobox_modalidad(self):
        
        """Llena el ComboBox solo con las modalidades permitidas."""
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
        self.entry_sede_paciente.set(opciones[0])
    
    def llenar_combobox_alergia(self):
        
        informacion = self.obtener_alergia()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["nombre_alergia"] for fila in informacion]
        
        if self.var_alergias.get() == 1:  # Sí tiene alergia
            
            # Insertar la opción por defecto solo si no existe
            if "Elige una Alergia" not in opciones:
                opciones.insert(0, "Elige una Alergia")
                
        elif self.var_alergias.get() == 0:  # No tiene alergia
            
            opciones = ["Ninguna"]
            
        else:  # valor inicial 0 = sin selección
            
            opciones = ["Sin Opciones Disponibles"]
        
        self.entry_tipo_alergia_paciente.configure(values=opciones)

        if opciones:  # solo setear si hay algo
            
            self.entry_tipo_alergia_paciente.set(opciones[0])
            
        if self.var_alergias.get() == 0:  # Solo para “No”
            self.llenar_textbox_alergia(self.entry_tipo_alergia_paciente.get())
    
    def llenar_textbox_alergia(self, valor_seleccionado):
            
        widget_text = self.entry_texto_alergias_paciente
        widget_text.configure(state="normal")

        # Si no hay valor o es la opción guía, no hacer nada
        if not valor_seleccionado or valor_seleccionado == "Elige una Alergia":
            widget_text.configure(state="disabled")
            return

        # RadioButton "No": mostrar Ninguna y bloquear
        if self.var_alergias.get() == 0:
            widget_text.delete("0.0", "end")
            widget_text.insert("0.0", "Ninguna")
            widget_text.configure(state="disabled")
            return

        # RadioButton "Sí": limpiar Ninguna si estaba, antes de agregar nuevas
        contenido_actual = widget_text.get("0.0", "end").strip()
        if contenido_actual == "Ninguna":
            contenido_actual = ""
            widget_text.delete("0.0", "end")

        # Convertimos en lista, evitando duplicados
        lista_valores = [v.strip() for v in contenido_actual.split(", ") if v.strip()]
        if valor_seleccionado not in lista_valores:
            lista_valores.append(valor_seleccionado)

        # Insertamos de nuevo
        widget_text.delete("0.0", "end")
        widget_text.insert("0.0", ", ".join(lista_valores))
    
    def llenar_combobox_aislamiento(self):
        
        informacion = self.obtener_aislamientos()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["nombre_aislamiento"] for fila in informacion]
        
        if self.var_aislamiento.get() == 1:

            # Insertar la opción por defecto solo si no existe
            if "Elige un Aislamiento" not in opciones:
                opciones.insert(0, "Elige un Aislamiento")
        
        elif self.var_aislamiento.get() == 0:
            
            opciones = ["Ninguno"]
        
        else:
            
            opciones = ["Sin Opciones Disponibles"]
            
        self.entry_tipo_aislamiento_paciente.configure(values=opciones)
        
        if opciones:
            
            self.entry_tipo_aislamiento_paciente.set(opciones[0])
            
        if self.var_aislamiento.get() == 0:
            
            self.llenar_textbox_aislamiento(self.entry_tipo_alergia_paciente.get())
    
    def llenar_textbox_aislamiento(self, valor_seleccionado):

        widget_text = self.entry_texto_aislamientos_paciente
        widget_text.configure(state="normal")
        
        # Si no hay valor o es la opción guía, no hacer nada
        if not valor_seleccionado or valor_seleccionado == "Elige un Aislamiento":
            widget_text.configure(state="disabled")
            return
        
        # RadioButton "No": mostrar Ninguna y bloquear
        if self.var_aislamiento.get() == 0:
            widget_text.delete("0.0", "end")
            widget_text.insert("0.0", "Ninguno")
            widget_text.configure(state="disabled")
            return
        
        # RadioButton "Sí": limpiar Ninguna si estaba, antes de agregar nuevas
        contenido_actual = widget_text.get("0.0", "end").strip()
        if contenido_actual == "Ninguno":
            contenido_actual = ""
            widget_text.delete("0.0", "end")

        # Evitar duplicados
        lista_valores = [v.strip() for v in contenido_actual.split(",") if v.strip()]
        if valor_seleccionado not in lista_valores:
            lista_valores.append(valor_seleccionado)

        widget_text.delete("0.0", "end")
        widget_text.insert("0.0", ", ".join(lista_valores))
    
    def llenar_combobox_estados(self):
        
        informacion = self.obtener_estado()
        
        # Filtrar solo los estados que nos interesan
        estados_filtrados = ["Pendiente"]
        
        # Extraer los nombres de los estados que coincidan con los que queremos
        opciones = [fila["nombre_estado"] for fila in informacion if fila["nombre_estado"] in estados_filtrados]
            
        self.entry_estado_paciente.configure(values=opciones)
        self.entry_estado_paciente.set(opciones[0])

    def llenar_combobox_causal_retraso(self):
        
        informacion = self.obtener_causal_retraso()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["causal_retraso"] for fila in informacion]

        # Insertar la opción por defecto solo si no existe
        if "Elige una causal de Retraso" not in opciones:
            opciones.insert(0, "Elige una causal de Retraso")
            
        self.entry_list_caus_retraso.configure(values=opciones)
        self.entry_list_caus_retraso.set(opciones[0])
    
    def llenar_textbox_estudios(self):
        
        informacion = getattr(self, 'estudio_extraido', [])
        opciones = [fila["nombre_estudio"] for fila in informacion]

        self.entry_texto_est_ord.configure(state="normal")
        self.entry_texto_est_ord.delete("0.0", "end")

        for nombre in opciones:
            self.entry_texto_est_ord.insert("end", nombre + "\n")

        self.entry_texto_est_ord.configure(state="disable")

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
    
    def limpiar_campos(self):
        
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
        
        for key, var in vars_si_no.items():
            if key in ["aislamiento", "alergia"]:
                var.set(2)  
            else:
                var.set(0)   
        
        # variables para obtener los valores de cada widget
        
        self.entry_identificacion_paciente.delete(0, "end")
        self.entry_nombre_paciente.delete(0, "end")
        self.entry_edad_paciente.delete(0, "end")
        # Convertir nombre de rango de edad a id
        self.entry_rango_edad_paciente.set('Elige un rango de edad')
        self.entry_historia_clin_paciente.delete(0, "end")
        self.entry_ubicacion_paciente.delete(0, "end")
        self.entry_sede_paciente.set('Elige una Sede')
        self.entry_tipo_alergia_paciente.set('Elige una Alergia')
        self.entry_texto_alergias_paciente.delete("1.0", "end")
        self.entry_tipo_aislamiento_paciente.set('Elige un Aislamiento')
        self.entry_texto_aislamientos_paciente.delete("1.0", "end")
        self.entry_estado_paciente.set('Elige un Estado')
        self.entry_fecha_orden.set_date(date.today())
        self.entry_fecha_cita.set_date(date.today())
        self.entry_modalidad.set('Elige una Modalidad')
        print("Valor actual de modalidad:", repr(self.entry_modalidad.get()))
        if self.entry_modalidad.get() == 'Elige una Modalidad':
            self.entry_texto_est_ord.configure(state="normal")  # desbloquear
            self.entry_texto_est_ord.delete("1.0", "end")      # borrar contenido
            self.entry_texto_est_ord.configure(state="disable")        # Limpiar contenido
        #self.entry_list_estud_ordenados.configure(state='normal')  # Habilitar temporalmente
        self.entry_list_estud_ordenados.delete("1.0", "end")        # Limpiar contenido
        #self.entry_list_estud_ordenados.configure(state='disable')  # Volver a deshabilitar
        self.entry_texto_diagnostico.delete("1.0", "end")
        self.entry_combobox_hora_citacion.set('Seleccione Una Hora')
        self.entry_combobox_hora_realizacion.set('Seleccione Una Hora')
        self.entry_list_caus_retraso.set('Elige una Causal de Retraso')
        self.entry_texto_coment_tecnologo.delete("1.0", "end")

    def agregar_datos(self):
        
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
        
        # variables para obtener los valores de cada widget
                
        identificacion = self.entry_identificacion_paciente.get()
        nombre = self.entry_nombre_paciente.get()
        edad = self.entry_edad_paciente.get()
        # Convertir nombre de rango de edad a id
        seleccion_rango = self.entry_rango_edad_paciente.get()  # nombre
        id_rango = next((r["id_rangoedad"] for r in self.rangos if r["rango"] == seleccion_rango), None)
        hc = self.entry_historia_clin_paciente.get()
        ubicacion = self.entry_ubicacion_paciente.get()
        seleccion_sede = self.entry_sede_paciente.get()
        id_sede = next((r["id_sede"] for r in self.sedes if r["nombre_sede"] == seleccion_sede), None)
        tipo_alergia = self.entry_texto_alergias_paciente.get("1.0", "end-1c")
        tipo_aislamiento = self.entry_texto_aislamientos_paciente.get("1.0", "end-1c")
        
        if self.var_diferido.get() == 1:
        
            estado = 'Diferido'
        
        else:
            
            estado = self.entry_estado_paciente.get()
            
        id_estado = next((r["id_estado"] for r in self.estado if r["nombre_estado"] == estado), None)
        id_estado_diferido = next((r["id_estado"] for r in self.estado if r["nombre_estado"] == "Diferido"), None)
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
        
        # ----------------------------
        # Validación de campos obligatorios
        # ----------------------------

        # Campos de widgets (Entry, Combobox, Text), excluyendo comentarios_radiologo
        campos_widgets = {
            "Identificación": identificacion,
            "Nombre": nombre,
            "Edad": edad,
            "Rango de edad": id_rango,
            "Historia clínica": hc,
            "Ubicación": ubicacion,
            "Sede": id_sede,
            "Fecha orden": fecha1,
            "Fecha cita": fecha2,
            "Modalidad": id_modalidad,
            "Estudios ordenados": estud_ord,
            "Diagnóstico": diagnostico,
            "Hora citación": hora_cita,
            "Hora realización": hora_realizacion,
            "Estado": id_estado,
            "comentarios tecnologo": coment_tecnologo
        }

        # Los IntVar se validan
        campos_intvar = {key: valor.get() for key, valor in vars_si_no.items()}

        # Combinar ambos diccionarios
        todos_los_campos = {**campos_widgets, **campos_intvar}

        # Revisar cuáles están vacíos o sin seleccionar
        faltantes = [campo for campo, valor in todos_los_campos.items() if valor is None or valor == ""]

        if faltantes:
            messagebox.showerror(
                "Campos incompletos",
                f"Debe llenar o seleccionar todos los campos:\n\n{', '.join(faltantes)}"
            )
            return  # Cancelar la inserción
        
        # ----------------------------
        # Validación duplicados
        # ----------------------------

        query_check = """
            SELECT 'registrospacientes' AS tabla, nombre_paciente, e.nombre_estado AS estado, fecha_orden
            FROM registrospacientes r
            JOIN estados e ON r.estado = e.id_estado
            WHERE identificacion_paciente = %s
            AND e.nombre_estado IN ('Diferido', 'Pendiente', 'Comentado')
            
            UNION ALL
            
            SELECT 'registrospacientesdiferidos' AS tabla, nombre_paciente, 'Diferido' AS estado, fecha_orden
            FROM registrospacientesdiferidos
            WHERE identificacion_paciente = %s
        """

        self.db.cursor.execute(query_check, (identificacion, identificacion))
        resultados = self.db.cursor.fetchall()

        if resultados:
            mensaje = (
                f"⚠️ El paciente con identificación {identificacion} ya se encuentra registrado en estado activo:\n\n"
            )
            for tabla, nombre, estado, fecha in resultados:
                mensaje += f"• {nombre} ({estado}) en {tabla} (fecha orden: {fecha})\n"
            
            mensaje += "\n¿Desea continuar y registrar de todas formas?"

            respuesta = messagebox.askyesno("Paciente ya registrado", mensaje)
            if not respuesta:
                self.limpiar_campos()
                return  # Cancelar inserción

        # ----------------------------
        # Valores finales para INSERT
        # ----------------------------
        
        valores_finales = (nombre, 
                    identificacion, 
                    edad, 
                    id_rango, 
                    fecha_orden,
                    fecha_cita, 
                    hc, 
                    ubicacion, 
                    id_modalidad, 
                    estud_ord, 
                    diagnostico, 
                    valores['ayuno'], 
                    valores['diferido'],
                    valores['alergia'],
                    tipo_alergia,
                    valores['aislamiento'],
                    tipo_aislamiento,
                    valores['autorizacion'],
                    valores['anestesia'],
                    id_estado,
                    id_sede,
                    hora_cita,
                    hora_realizacion,
                    id_retraso,
                    coment_tecnologo,
                    valores['coment_estudio'],
                    coment_radiologo,
                    UsuarioActual.id_usuario
                    )
            
        if self.var_diferido.get() == 1:
                            
            sql = """INSERT INTO registrospacientesdiferidos
                    (
                    nombre_paciente, 
                    identificacion_paciente,
                    edad,
                    rango_edad,
                    fecha_orden,
                    fecha_citacion,
                    hc,
                    ubicacion,
                    modalidad,
                    estudios_ordenados_paciente,
                    diagnostico,
                    ayuno,
                    diferido,
                    alergia,
                    tipo_alergia,
                    aislamiento,
                    tipo_aislamiento,
                    autorizacion,
                    anestesia,
                    estado,
                    sede,
                    hora_citacion,
                    hora_realizacion,
                    causal_retraso,
                    comentarios_tecnologo,
                    comentar_radiologo,
                    comentarios_radiologo,
                    usuario
                    )
                    VALUES (
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            
        else:
            
            sql = """INSERT INTO registrospacientes
                    (
                    nombre_paciente, 
                    identificacion_paciente,
                    edad,
                    rango_edad,
                    fecha_orden,
                    fecha_citacion,
                    hc,
                    ubicacion,
                    modalidad,
                    estudios_ordenados_paciente,
                    diagnostico,
                    ayuno,
                    diferido,
                    alergia,
                    tipo_alergia,
                    aislamiento,
                    tipo_aislamiento,
                    autorizacion,
                    anestesia,
                    estado,
                    sede,
                    hora_citacion,
                    hora_realizacion,
                    causal_retraso,
                    comentarios_tecnologo,
                    comentar_radiologo,
                    comentarios_radiologo,
                    usuario
                    )
                    VALUES (
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
                        
        self.db.cursor.execute(sql, valores_finales)
        
        self.db.conexion.commit()
        datos_ingresados()
        
        # ----------------------------
        # Guardar la hora de citación en JSON de horas tomadas
        # ----------------------------
            
        try:
            if hasattr(self, "_pending_bloqueo") and self._pending_bloqueo:
                from ventanas.ventana_ingreso_pacientes import IngresarPacientes

                # Cargar JSON existente por si alguien más lo cambió
                IngresarPacientes.cargar_horas()
                horas_tomadas = IngresarPacientes.horas_tomadas

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
                IngresarPacientes.guardar_horas()

                # Opcional: actualizar combobox globales
                try:
                    IngresarPacientes.actualizar_horas_disponibles()
                except Exception:
                    pass

                # Limpiar pending
                self._pending_bloqueo = None

        except Exception as e:
            print(e)

        self.limpiar_campos()

    def obtener_id_estado(self, nombre_estado):
        """Obtiene el ID del estado basado en el nombre del estado."""
        # solo tomamos el nombre
        nombre_estado = nombre_estado.split(' (')[0]
        
        sql = "SELECT id_estado FROM estados WHERE nombre_estado = %s"
        self.db.cursor.execute(sql, (nombre_estado,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None

    def validar_edad_key(self, valor):
        if valor == "":
            return True
        if valor.isdigit() and len(valor) <= 3:
            return True
        return False

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
            horas_ocupadas = IngresarPacientes.horas_tomadas.get(str(id_sede), {}).get(fecha, [])

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
        
        if widget is None and event is not None:
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
                sql_union = """
                    SELECT id_registro, estado, 'r' as tabla
                    FROM registrospacientes
                    WHERE identificacion_paciente = %s
                    UNION ALL
                    SELECT id_registro, estado, 'd' as tabla
                    FROM registrospacientesdiferidos
                    WHERE identificacion_paciente = %s
                    ORDER BY id_registro DESC
                    LIMIT 1
                """
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
        print(f"[DEBUG] Pending bloqueo: {self._pending_bloqueo}")
    
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
    
    @classmethod
    def actualizar_json_horas(cls):
        """Actualiza únicamente el JSON de horas (sin tocar widgets)."""
        try:
            cls.cargar_horas()
            cls.guardar_horas()
        except Exception as e:
            print(e)
    
    #@classmethod
    def actualizar_horas_disponibles(self, event=None):
            
        """Restaura la lista de horas disponibles al cambiar la fecha o la sede."""
        try:
            fecha = self.entry_fecha_cita.get_date().strftime("%d/%m/%Y")
            nombre_sede = self.entry_sede_paciente.get().strip()
            id_sede = self.obtener_id_sede(nombre_sede)
            id_sede_str = str(id_sede) if id_sede is not None else None

            if id_sede_str and id_sede_str in IngresarPacientes.horas_tomadas:
                # Normalizamos todas las horas a 'HH:MM' strings
                horas_ocupadas_raw = IngresarPacientes.horas_tomadas[id_sede_str].get(fecha, [])
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

    @classmethod
    def cargar_horas(cls):
        """Carga el diccionario de horas tomadas desde un archivo JSON (solo 'detalles')."""
        if os.path.exists("horas_tomadas.json"):
            try:
                with open("horas_tomadas.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Asegurar que exista la clave 'detalles'
                    cls.horas_tomadas = {"detalles": data.get("detalles", {}) if isinstance(data, dict) else {}}
            except Exception as e:
                print("Error al cargar horas tomadas:", e)
                cls.horas_tomadas = {"detalles": {}}
        else:
            cls.horas_tomadas = {"detalles": {}}

    @classmethod
    def guardar_horas(cls):
        """Guarda únicamente la sección 'detalles' del diccionario de horas tomadas en un archivo JSON."""
        try:
            horas = cls.horas_tomadas
            if not isinstance(horas, dict):
                print("[ERROR] horas_tomadas no es un diccionario:", horas)
                return

            # Solo guardamos 'detalles'
            detalles = horas.get("detalles", {})

            # Serialización segura
            with open("horas_tomadas.json", "w", encoding="utf-8") as f:
                json.dump({"detalles": detalles}, f, indent=2, ensure_ascii=False)

            # DEBUG: opcional
            print(f"[DEBUG guardar_horas] Guardadas {len(detalles)} entradas en 'detalles'")

        except Exception as e:
            print(e)
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
        
        cb = self.entry_combobox_hora_citacion
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
                    detalles = IngresarPacientes.horas_tomadas.get("detalles", {})

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
                                f"y finaliza a las {fin}.\n"
                                f"Duración: {duracion_calc} minutos.",
                                parent=self.ventana
                            )
                            cb.set(self.placeholder_text)
                            break
                    else:
                        self._ultima_hora_mostrada = None

        cb.after(400, self.verificar_hora_periodica)
            
    def validar_edad_final(self, event):
        valor = self.entry_edad_paciente.get()
        parent = self.ventana.winfo_toplevel()
        
        if valor == "":  
            # Si está vacío, no mostramos error, simplemente no validamos
            return  
        if not valor.isdigit():
            edad_incorrecta(parent=parent)
        elif len(valor) > 3:
            tamano_edad_incorrecta(parent=parent)
        
        elif int(valor) > 120:
            edad_fuera_rango()   
            self.entry_edad_paciente.delete(0, "end")
            self.entry_edad_paciente.focus_set()
    
    def validar_fecha(self):
        
        fecha_orden = self.entry_fecha_orden.get_date()
        
        fecha_cita = self.entry_fecha_cita.get_date()
        
        if fecha_cita < fecha_orden:
            
            messagebox.showinfo('Error en la fecha', """La fecha de la cita no puede ser inferior a la fecha de la orden""")
            
            self.entry_fecha_cita.set_date(fecha_orden)
            
            return False
        
        return True

    def ejecutar_cambio_fecha(self):
        
        if self.validar_fecha(): # Solo si la fecha es válida
            self.actualizar_horas_disponibles()
    
    def validar_hora_cita(self):
        hora_cita = self.entry_combobox_hora_citacion.get()
        hora_realizacion = self.entry_combobox_hora_realizacion.get()
        
        # Validamos solo si AMBOS tienen una hora real (no el placeholder)
        if (hora_cita != self.placeholder_text and 
            hora_realizacion != self.placeholder_text):
            
            if hora_realizacion < hora_cita:
                messagebox.showwarning(
                    'Error en la Hora', 
                    'La hora de la realización no puede ser inferior a la hora de la cita'
                )
                # Limpiamos la hora de realización para que el usuario elija de nuevo
                self.entry_combobox_hora_realizacion.set(hora_cita)
                return False
                
        return True

    def ejecutar_cambio_hora(self, *args):
        # Este *args captura el valor si viene de 'command' o el evento si viene de 'bind'
        if self.validar_hora_cita():
            if hasattr(self, '_restore_placeholder'):
                self._restore_placeholder()
    

    def salir(self):
            
        if getattr(self, 'db', None):
            self.db.cerrar_conexion()
            self.db = None  # 🔹 Limpiar la referencia de esta instancia
            # 🔹 Limpiar la variable de clase para que la próxima vez se cree nueva conexión
            IngresarPacientes.db = None
            IngresarPacientes.conexion_realizada = False

        cerrar_conexion()

        # 2️⃣ Cancelar cualquier after pendiente de esta ventana
        if hasattr(self, "after_id_aviso") and self.after_id_aviso:
            self.ventana.after_cancel(self.after_id_aviso)
            self.after_id_aviso = None

        # 3️⃣ Destruir los frames propios de esta ventana
        for frame in ['frame1', 'frame2', 'frame3', 'frame_sup', 'frame_sup1', 'frame_ppal']:
            f = getattr(self, frame, None)
            if f and f.winfo_exists():
                try:
                    f.destroy()
                except:
                    pass

        # 4️⃣ Cerrar la ventana Toplevel
        try:
            if isinstance(self.ventana, self.ventana.__class__):
                self.ventana.grab_release()
                self.ventana.destroy()
                print("✅ Ventana de ingreso cerrada correctamente.")
        except Exception as e:
            print(f"⚠️ No se pudo cerrar la ventana de ingreso: {e}")

        # 5️⃣ Restaurar ventana principal solo si existe
        if self.parent_window and self.parent_window.winfo_exists():
            def restaurar_principal():
                try:
                    self.parent_window.deiconify()
                    self.parent_window.lift()
                    self.parent_window.focus_force()
                    self.parent_window.state("normal")
                    self.parent_window.update()
                    self.parent_window.state("zoomed")
                    print("✅ Ventana principal restaurada correctamente.")
                except Exception as e:
                    print(f"⚠️ No se pudo restaurar la ventana principal: {e}")

            self.parent_window.after(100, restaurar_principal)
        else:
            print("⚠️ No se encontró ventana principal para restaurar.")
            