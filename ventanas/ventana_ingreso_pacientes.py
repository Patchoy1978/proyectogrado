import sys # Importa el módulo sys para manipular el path del sistema
import os # Importa el módulo os para manejar rutas de archivos y directorios

"""Añade al path del sistema la ruta del directorio padre del archivo actual.
Esto permite importar módulos desde la carpeta superior."""

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))  # Añade al path el directorio padre del archivo actual

# Importación de librerías necesarias para la interfaz

import customtkinter as ctk # Versión personalizada de Tkinter con mejor apariencia

import tkinter as tk # Importa la librería estándar Tkinter para interfaces gráficas

from usuarioactual.usuario_actual import UsuarioActual

from datetime import datetime, date, timedelta

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

from abrirventanas.abrir import abrir_ventana_visualizar_datos_ppal

# Clase para la ventana de modificación de pacientes
class IngresarPacientes():
    
    conexion_realizada = False # Variable de clase para indicar si ya se realizó la conexión a la base de datos
    db = None # Variable de clase para almacenar la conexión a la base de datos
    
    # Constructor de la clase que recibe la ventana y el paciente a modificar
    def __init__(self, ventana):

        self.ventana = ventana  # Guarda la referencia a la ventana en un atributo
        
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

        if not IngresarPacientes.conexion_realizada: # Si no se ha hecho la conexión a la BD
            try:
                IngresarPacientes.db = Conexion_DB() # Crea una instancia de la conexión
                IngresarPacientes.db.conectar() # Establece la conexión
                abrir_ventana_conn_exito() # Muestra ventana de conexión exitosa
                IngresarPacientes.conexion_realizada = True # Marca la conexión como realizada
                
            except:
                
                abrir_ventana_conn_fallida() # Si no se establece la conexión, muestra ventana de fallo
        else:

            pass
            
        self.db = IngresarPacientes.db # Guarda la referencia de la conexión en el objeto actual
        
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
        self.contenidotituloppalmodificar()
        self.contenidosframe1modificar()
        self.contenidosframe2modificar()
        self.contenidosframe3modificar()
        
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
        
        """self.horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 5)]  # Intervalos de 5 minutos 
        
        self.horas = sorted(list(set(self.horas)))
        self.horas = [str(hora) if not isinstance(hora, dict) else "" for hora in self.horas]"""

    # Devuelve la ventana actual
    def obtener_ventana(self):
        
        return self.ventana
    
    # parte de la visualizacion de la información
    
    def contenidotituloppalmodificar(self):
        
        self.titulo = ctk.CTkLabel(self.frame_sup, text='Ingresar Datos Del Paciente', font=self.fonts['title'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.titulo.grid(row=0, column=0, columnspan=3, pady = 5, sticky="nsew") 
    
    def contenidosframe1modificar(self):

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
        
        self.var_alergias = tk.IntVar(value=0)  # Valor predeterminado es 0

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
                                        value=2,
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
        
        self.var_aislamiento = tk.IntVar(value=0)  # Valor predeterminado es No

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
                                            value=2,
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
    
    def contenidosframe2modificar (self):
        
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
                                    value=2,
                                    font= self.fonts['label_etiqueta'],
                                    bg_color= 'white',
                                    fg_color= 'black',
                                    border_color= 'lightgray'
                                    )
        self.radio_ayuno2.grid(row=1, column=1, sticky='nsew')
        
        self.lab_diferido_paciente = ctk.CTkLabel(self.frame_radios2, text='Diferido', font= self.fonts['label_etiqueta'], fg_color='white', bg_color= 'white', text_color= "#484a4b")
        self.lab_diferido_paciente.grid(row=0, column=2, columnspan = 2, pady = 2, sticky='nsew')
        
        self.var_diferido = tk.IntVar(value=2)  # Valor predeterminado es No

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
                                        value=2,
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
                                            value=2,
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
                                        value=2,
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
    
    def contenidosframe3modificar (self):
        
        #from abrirventanas.abrir import abrir_ventana_visualizar_datos_ppal, cerrar_ppal
        
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
                                                    values=self.horas
                                                    )
        self.entry_combobox_hora_citacion.grid(row=1, column=0, pady=4, padx=15, sticky='nsew')
        
        # Vincular el evento de escritura
        self.entry_combobox_hora_citacion.set(self.placeholder_text)

        """# Vincular eventos
        self.entry_combobox_hora_citacion.bind("<FocusIn>", self._clear_placeholder)
        self.entry_combobox_hora_citacion.bind("<FocusOut>", self._restore_placeholder)
        self.entry_combobox_hora_citacion.bind("<KeyRelease>", self.filtrar_horas)"""
        
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
                                                    values=self.horas
                                                    )
        self.entry_combobox_hora_realizacion.grid(row=3, column=0, pady=4, padx=15, sticky='nsew')
        
        self.entry_combobox_hora_realizacion.set(self.placeholder_text)

        """# Vincular eventos
        self.entry_combobox_hora_realizacion.bind("<FocusIn>", self._clear_placeholder)
        self.entry_combobox_hora_realizacion.bind("<FocusOut>", self._restore_placeholder)
        self.entry_combobox_hora_realizacion.bind("<KeyRelease>", self.filtrar_horas)"""
        
        for cb in (self.entry_combobox_hora_citacion, self.entry_combobox_hora_realizacion):
            # pasamos el widget explícitamente al handler mediante lambda
            cb.bind("<FocusIn>", lambda e, w=cb: self._clear_placeholder(e, w))
            cb.bind("<FocusOut>", lambda e, w=cb: self._restore_placeholder(e, w))
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
                                                    value=2, font=self.fonts['label_etiqueta'],
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
        
        self.btn_nuevo = ctk.CTkButton(self.frame_buttons,
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
        
        self.btn_nuevo.grid(row= 0, column= 0, padx= 8, pady= 70, sticky='nsew')
        
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
        
        informacion = self.obtener_modalidades()
        
        # Extraer solo los nombres de rango_edad
        opciones = [fila["nombre_modalidad"] for fila in informacion]

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
                
        elif self.var_alergias.get() == 2:  # No tiene alergia
            
            opciones = ["Ninguna"]
            
        else:  # valor inicial 0 = sin selección
            
            opciones = ["Sin Opciones Disponibles"]
        
        self.entry_tipo_alergia_paciente.configure(values=opciones)

        if opciones:  # solo setear si hay algo
            
            self.entry_tipo_alergia_paciente.set(opciones[0])
            
        if self.var_alergias.get() == 2:  # Solo para “No”
            self.llenar_textbox_alergia(self.entry_tipo_alergia_paciente.get())
    
    def llenar_textbox_alergia(self, valor_seleccionado):
            
        widget_text = self.entry_texto_alergias_paciente
        widget_text.configure(state="normal")

        # Si no hay valor o es la opción guía, no hacer nada
        if not valor_seleccionado or valor_seleccionado == "Elige una Alergia":
            widget_text.configure(state="disabled")
            return

        # RadioButton "No": mostrar Ninguna y bloquear
        if self.var_alergias.get() == 2:
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
        
        elif self.var_aislamiento.get() == 2:
            
            opciones = ["Ninguno"]
        
        else:
            
            opciones = ["Sin Opciones Disponibles"]
            
        self.entry_tipo_aislamiento_paciente.configure(values=opciones)
        
        if opciones:
            
            self.entry_tipo_aislamiento_paciente.set(opciones[0])
            
        if self.var_aislamiento.get() == 2:
            
            self.llenar_textbox_aislamiento(self.entry_tipo_alergia_paciente.get())
    
    def llenar_textbox_aislamiento(self, valor_seleccionado):

        widget_text = self.entry_texto_aislamientos_paciente
        widget_text.configure(state="normal")
        
        # Si no hay valor o es la opción guía, no hacer nada
        if not valor_seleccionado or valor_seleccionado == "Elige un Aislamiento":
            widget_text.configure(state="disabled")
            return
        
        # RadioButton "No": mostrar Ninguna y bloquear
        if self.var_aislamiento.get() == 2:
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
        
        for var in vars_si_no.values():
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
        self.entry_list_estud_ordenados.delete("1.0", "end")
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
        faltantes = [campo for campo, valor in todos_los_campos.items() if not valor]

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

    """def _clear_placeholder(self, event):
        Borra el texto de placeholder cuando el usuario entra al campo.
        if self.entry_combobox_hora_citacion.get() == self.placeholder_text:
            self.entry_combobox_hora_citacion.set("")


    def _restore_placeholder(self, event):
        Restaura el placeholder si el campo está vacío al perder el foco.
        if self.entry_combobox_hora_citacion.get().strip() == "":
            self.entry_combobox_hora_citacion.set(self.placeholder_text)
            # restaurar la lista completa
            self.entry_combobox_hora_citacion.configure(values=self.horas)


    def filtrar_horas(self, event):
        Filtra las horas mientras el usuario escribe.
        texto = self.entry_combobox_hora_citacion.get().strip()

        if texto == "" or texto == self.placeholder_text:
            filtradas = self.horas
        else:
            filtradas = [hora for hora in self.horas if texto in hora]

        self.entry_combobox_hora_citacion.configure(values=filtradas)"""
        
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
        Filtra las horas leyendo el texto REAL del entry interno si existe.
        Recibe event (por bind) y opcionalmente widget (cuando se pasa por lambda).
        """
        if widget is None:
            widget = event.widget

        # Leer texto del entry interno si existe (captura lo que tecleas en tiempo real)
        entry = getattr(widget, "_entry", None)
        try:
            texto = (entry.get() if entry is not None else widget.get()).strip()
        except Exception:
            texto = widget.get().strip()

        if texto == "" or texto == self.placeholder_text:
            filtradas = self.horas
        else:
            filtradas = [hora for hora in self.horas if hora.startswith(texto)]

        # Actualizar solo el combobox activo
        try:
            widget.configure(values=filtradas)
        except Exception:
            pass
    
    

    # Función que se llama al perder foco
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
        
    def salir(self):
        """Método personalizado para el botón Salir.
        """
        
        if self.db:
            self.db.cerrar_conexion()
            IngresarPacientes.conexion_realizada = None
        cerrar_conexion()
        
        # Destruir todos los widgets hijos del frame principal, incluyendo scrollable frames
        def destruir_completo(widget):
            for child in widget.winfo_children():
                destruir_completo(child)
            try:
                widget.destroy()
            except:
                pass

        destruir_completo(self.frame3.winfo_toplevel())
        destruir_completo(self.frame1.winfo_toplevel())
        destruir_completo(self.frame2.winfo_toplevel())
        
        #self.frame3.winfo_toplevel().destroy()
        
        abrir_ventana_visualizar_datos_ppal()
        