import sys
import os
from datetime import datetime, date
from tkinter import TclError

"""Añade al path del sistema la ruta del directorio padre del archivo actual.
Esto permite importar módulos desde la carpeta superior."""

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'img'))

# Importación de librerías necesarias para la interfaz

import customtkinter as ctk # Versión personalizada de Tkinter con mejor apariencia

from PIL import Image, ImageTk

from tkcalendar import DateEntry # Widget calendario para seleccionar fechas

from usuarioactual.usuario_actual import UsuarioActual

from ventanas.ventanasprograma import VentanaPrincipal

from abrirventanasemergentes.abrir_ventanas import (abrir_ventana_conn_exito,
                                                    abrir_ventana_conn_fallida,
                                                    cerrar_conexion,
                                                    debes_hacer_primero,
                                                    si_la_db_esta_vacia,
                                                    )

# Importa funciones para abrir una nueva ventana y cerrar la principal
#from abrirventanas.abrir import (abrir_ventana_ingreso, )

# Importar la clase de conexión a la base de datos desde el módulo correspondiente
from conexion_DB.conexionDB import Conexion_DB

# Clase que define el panel principal de visualización
class PanelPrincipalVisualizacionRealizados():
    
    conexion_realizada = False  # variable de clase para controlar si ya se conectó
    db = None
    
    # Constructor de la clase
    def __init__(self, frame_sup, frame):
        self.frame_sup = frame_sup
        self.frame = frame  # Contenedor principal

        self.ventana = self.frame.winfo_toplevel()
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir)

        if not PanelPrincipalVisualizacionRealizados.conexion_realizada:
            try:
                PanelPrincipalVisualizacionRealizados.db = Conexion_DB()
                PanelPrincipalVisualizacionRealizados.db.conectar()
                abrir_ventana_conn_exito()
                PanelPrincipalVisualizacionRealizados.conexion_realizada = True
            except Exception:

                abrir_ventana_conn_fallida()
                
        else:
            
            pass

        self.db = PanelPrincipalVisualizacionRealizados.db

        # Configuración de grid para que filas y columnas se expandan
        self.frame_sup.grid_rowconfigure(list(range(4)), weight=1)
        self.frame_sup.grid_columnconfigure(list(range(16)), weight=1)
        self.frame.grid_rowconfigure(list(range(4)), weight=1)
        self.frame.grid_columnconfigure(list(range(16)), weight=1)
        
        self.frame_ppal_visual_datos = ctk.CTkFrame(self.frame, fg_color='transparent')
        self.frame_ppal_visual_datos.grid(row=0, column=0, columnspan = 16, sticky='nsew')
        self.frame_ppal_visual_datos.grid_rowconfigure(list(range(4)), weight=1)  # Permitir que todas las filas se expandan
        self.frame_ppal_visual_datos.grid_columnconfigure(list(range(16)), weight=1)

        # Fuentes usadas
        self.fonts = {
            'title': ('verdana', 26, 'bold'),
            #'title_frame': ('verdana', 24, 'bold'),
            'label_title': ('verdana', 12, 'bold'),
            'label': ('verdana', 12 ),
            'boton': ('verdana', 14, 'bold'),
        }
        
        self.entries = {}
        self.textbox = {}

        self.paciente_seleccionado = None
        
        # Inicializamos para asegurar que exista el atributo
        self.combobox_sede = None

        self.cargar_pacientes()
    
    def cargar_pacientes(self):
        
        self.datos_db = []
        #print("Ejecutando cargar_pacientes...")
        
        consulta_pacientes = "SELECT * FROM registrospacientesrealizados ORDER BY hora_citacion"
        
        self.db.cursor.execute(consulta_pacientes)
        
        columnas = self.db.cursor.column_names
        #print("Columnas:", columnas)
        
        filas = self.db.cursor.fetchall()

        nuevos_datos = [dict(zip(columnas, fila)) for fila in filas]

        # Evitar duplicados
        self.datos_db.clear()
        self.datos_db.extend(nuevos_datos)
        
        #print(self.datos_db)
    
    def visual_principal_titulo(self):
        
        self.refresh_db = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, "refresh.png")).resize((50, 50)), size=(50, 50))
        
        # Crea el primer frame principal para los títulos y lo hace transparente
        visual_datos_ppal = ctk.CTkFrame(self.frame_sup, fg_color= 'white')
        visual_datos_ppal.grid(row=0, column=0, sticky='nsew', columnspan = 16) # Ocupa la primera fila y todas las columnas

        # Configura el grid interno del frame
        visual_datos_ppal.grid_columnconfigure(0, weight=1)
        visual_datos_ppal.grid_rowconfigure(0, weight=1)
        
        # Crea una línea divisoria de color azul claro entre secciones
        linea = ctk.CTkFrame(self.frame_sup, fg_color="#00155c", height=10, width=0)
        linea.grid(row=1, column=0, columnspan=16, sticky="ew", pady=10)

        # Fija la altura de la línea para que no se modifique con el contenido
        linea.grid_propagate(False)
        
        # Segundo frame principal donde estarán los filtros y campos interactivos
        visual_datos_ppal1 = ctk.CTkFrame(self.frame_sup, fg_color= 'transparent')
        visual_datos_ppal1.grid(row=2, column=0, sticky='nsew', columnspan = 16)
        
        # Configura todas las columnas del grid del segundo frame para distribuir el contenido uniformemente
        for col in range(16):
            visual_datos_ppal1.grid_columnconfigure(col, weight=1)  # Asignar peso igual a todas las columnas

        visual_datos_ppal1.grid_rowconfigure(0, weight=1)
        
        # Lista de campos que forman parte del encabezado visual
        campos = [
            
            {"label": "Visualizacion De Pacientes Realizados", "valor": "", "ancho": 400, "tipo": "label"},
            
        ]
        
        self.obtener_sedes()
        
        # Lista de campos que componen los filtros y botones de acción
        campos1 =[
            
            {"label": "Sede", "valor": None, "ancho": 130, "tipo": "combobox", "opciones": self.sedes},
            {"label": "Fecha", "valor": None, "ancho": 100, "tipo": "fecha"},
            {"label": "Todos", "color": "#00155c", "tipo": "boton", "alto": 26, "ancho":10, "command": self.limpiar_fecha},
            {"label": "Identificación\nPaciente", "columna": "identificacion paciente", "valor": "", "ancho": 130, "tipo": "entry"},

        ]
        
        # Agrega el título principal al primer frame
        for i, campo in enumerate(campos):
            
            label = self.crear_label(visual_datos_ppal, campo["label"], self.fonts['title'], 0, i)
            label.grid(sticky='nsew')
        
        # Recorre los campos de filtros/botones y los agrega dinámicamente al segundo frame
        for i, campo in enumerate(campos1):
            
            # Si es un combobox (sede)
            if campo["label"] == "Sede":
                
                self.sede_var = ctk.StringVar(value=None)
                self.crear_label(visual_datos_ppal1, campo["label"], self.fonts['label_title'], 0, i*2)
                
                # Función para actualizar la variable cuando se seleccione un valor
                def actualizar_sede(valor):
                    if isinstance(valor, (tuple, list)):
                        valor = valor[0]
                    self.sede_var.set(valor)
                    # Solo llamar a la visualización, que internamente llamará a obtener_pacientes_filtrados
                    self.visual_principal_datos()
                
                combobox = self.crear_combobox(
                    visual_datos_ppal1,
                    self.fonts['label'],
                    fila=0,
                    columna=i*2+1,
                    ancho_widget=campo["ancho"],
                    opciones=campo["opciones"],
                    valor_predeterminado="",
                    comando=actualizar_sede
                )
                
                self.combobox_sede = combobox
            
            # Si es un campo de fecha
            if campo ["tipo"] == "fecha":
                
                self.crear_label(visual_datos_ppal1, campo["label"], self.fonts['label_title'], 0, i*2)
                
                self.fecha = DateEntry(visual_datos_ppal1,
                                    width=5,
                                    background='lightgray',
                                    foreground='white',
                                    borderwidth=2,
                                    date_pattern= 'dd/MM/yyyy',
                                    font=self.fonts['label'],
                                    locale = 'es'
                                    )
                
                self.fecha.grid(row=0, column= i*2+1, padx=5, sticky= 'nsew')
                
                self.fecha.delete(0, 'end')
                
                # Cuando el usuario elige fecha, actualiza datos
                self.fecha.bind("<<DateEntrySelected>>", lambda e: self.visual_principal_datos())
            
            # Si es un campo de texto (entry)
            if campo["tipo"] == "entry":
                var_entry = ctk.StringVar(value=campo.get('valor', ''))
                
                self.crear_label(visual_datos_ppal1, campo["label"], self.fonts['label_title'], 0, i*2)
                
                habilitar = campo["label"] == "Identificación\nPaciente"
                
                # Solo el campo de identificación tendrá trace
                if habilitar:
                    
                    """def depurar(*args):
                        print("Valor del Entry de identificación:", var_entry.get())
                        self.obtener_pacientes_filtrados()"""
                    
                    var_entry.trace_add("write", lambda *args: self.visual_principal_datos())
                    self.identificacion_var = var_entry  # Guardamos la variable de identificación
                
                self.crear_entry(
                    visual_datos_ppal1,
                    self.fonts['label'],
                    campo["label"],
                    campo['columna'],
                    valor_predeterminado=campo.get('valor', ''),
                    fila=0,
                    columna=i*2+1,
                    ancho_widget=campo['ancho'],
                    habilitado=habilitar,
                    textvariable=var_entry
                )
            
            # Si es un botón  
            if campo['tipo'] == 'boton':
                
                self.crear_boton(visual_datos_ppal1, self.fonts['boton'], campo['label'], campo['color'], 0, i*2+1, campo['alto'], campo['ancho'], command=campo['command'], image=campo.get('image'))
        
        # Segunda línea divisoria al final del panel
        linea1 = ctk.CTkFrame(self.frame_sup, fg_color="#00155c", height=10, width=0)
        linea1.grid(row=3, column=0, columnspan=16, sticky="ew", pady=10)

        # Fijar altura para evitar que se estire
        linea1.grid_propagate(False)
    
    def crear_label(self,parent, texto, font, fila, columna, ancho=1, alto=1):
        
        # Crea un widget de etiqueta (label) usando CTkLabel con los parámetros dados
        label = ctk.CTkLabel(
            parent, # Frame o contenedor donde se insertará el label
            text=texto, # Texto que mostrará el label
            font=font, # Fuente del texto (debe estar definida previamente)
            anchor='center', # Alineación del texto dentro del label
            text_color='#484a4b' # Color del texto
        )
        # Ubica el label en el grid del contenedor padre con sus coordenadas y tamaños
        label.grid(
            row=fila, # Fila en la que se ubicará el label
            column=columna, # Columna en la que se ubicará el label
            columnspan=ancho, # Número de columnas que ocupará el label
            rowspan=alto, # Número de filas que ocupará el label
            padx=5, # Espaciado horizontal entre el label y los bordes adyacentes
            pady = 5,
            sticky='nsew' # El label se expandirá en todas las direcciones dentro de su celda
            )
        
        return label # Devuelve el widget creado para que pueda ser reutilizado o modificado si es necesario
    
    def crear_entry(self, parent, font, campo_label,campo_columna, valor_predeterminado, fila, columna, ancho=1, alto=1, 
                ancho_widget=30, alto_widget=26, habilitado=False, textvariable=None):
    
        # Si no se pasa una variable, se crea una nueva
        
        if textvariable is None:
            textvariable = ctk.StringVar(value=valor_predeterminado)

        # Determinar el color de fondo según el valor 
        if campo_columna == "autorizacion" and valor_predeterminado != "Si":
            color_fondo = "#bd0936"  # rojo
        
        else:
            color_fondo = "lightgray"  # por defecto
        
        # Crea el widget Entry
        entry = ctk.CTkEntry(
            parent,
            font=font,
            text_color='black',
            corner_radius=10,
            width=ancho_widget,
            height=alto_widget,
            fg_color=color_fondo,
            textvariable=textvariable
        )
        
        # Configura habilitado/deshabilitado
        if habilitado:
            entry.configure(state='normal')
        else:
            #entry.configure(state='normal')  # Necesario para insertar el valor
            #entry.delete(0, 'end')
            #entry.insert(0, valor_predeterminado)
            entry.configure(state='disable')

        # Posiciona en el grid
        entry.grid(
            row=fila,
            column=columna,
            columnspan=ancho,
            rowspan=alto,
            padx=5,
            sticky='ew'
        )
        
        return entry, textvariable  # Devuelve el widget y la variable asociada
    
    def crear_textbox(self,parent, font, campo_col, fila, columna, ancho=1, alto_widget=65, ancho_widget=30, valor_db=None):

        # Obtener valor real según el campo
        if campo_col == "tipo_aislamiento":
            valor_real = str(valor_db or "")
        else:
            valor_real = str(valor_db or "")

        # Normalizamos el valor (separando por comas y quitando espacios)
        valor_normalizado = [v.strip().title() for v in valor_real.split(",")]
        
        if campo_col == "comentarios del radiologo"  and valor_real.strip() != "":
            
            color_fondo = "lightgreen"

        elif campo_col == "tipo_aislamiento" and any(v in ["Tbc", "Covid"] for v in valor_normalizado):
            
            color_fondo = "#bd0936" # rojo
        
        else:
            
            color_fondo = "lightgray"  # valor por defecto
        
        # Crea un widget tipo Textbox (área de texto) personalizado, útil para mostrar información de varias líneas

        textbox = ctk.CTkTextbox(
            parent,  # Crea un widget tipo Textbox (área de texto) personalizado, útil para mostrar información de varias líneas
            font=font, # Fuente del texto
            text_color='black', # Color del texto
            corner_radius=12, # Bordes redondeados
            width=ancho_widget, # Ancho del widget
            height=alto_widget, # Alto del widget
            fg_color=color_fondo,
            scrollbar_button_color= "lightgreen"
        )

        textbox.configure(state='normal') # Se habilita el textbox para poder insertar texto
        textbox.insert('0.0', valor_real) # Inserta el texto predeterminado en la posición inicial (línea 0, carácter 0)
        textbox.configure(state='disable') # Se desactiva el textbox para que el usuario no lo pueda editar
        
        # Posiciona el textbox dentro del grid del contenedor
        textbox.grid(
            row=fila, # Fila en la que se colocará el widget
            column=columna, # Columna en la que se colocará el widget
            columnspan=ancho, # Número de columnas que ocupará
            rowspan=alto_widget, # Número de filas que ocupará (se usa como alto visual, no estructural) 
            padx=5, # Margen horizontal
            sticky='ew' # El widget se expandirá horizontalmente
            )
        
        return textbox # Devuelve el widget creado, por si se necesita manipular después

    def crear_combobox(self, parent, font, fila, columna, alto_widget=26, ancho_widget=130, ancho=1, opciones=None, valor_predeterminado='', comando=None):
        """
        Crea un combobox personalizado usando CTkOptionMenu.
        
        Parámetros:
        - parent: contenedor donde se ubicará el combobox
        - font: fuente del texto
        - fila, columna: posición en la grilla
        - alto_widget, ancho_widget: tamaño del combobox
        - ancho: número de columnas que ocupa
        - opciones: lista de opciones
        - valor_predeterminado: valor inicial mostrado
        - comando: función que se ejecuta al cambiar la opción
        """

        # Si no se pasan opciones, inicializa con 'Ninguna'
        if opciones is None:
            opciones = []

        # Asegura que el valor predeterminado esté en la lista
        if valor_predeterminado and valor_predeterminado not in opciones:
            opciones = [valor_predeterminado] + opciones

        # Crear el combobox
        combobox = ctk.CTkOptionMenu(
            parent,
            font=font,
            text_color='black',
            corner_radius=10,
            width=ancho_widget,
            height=alto_widget,
            fg_color='lightgray',
            values=opciones,
            command=comando,  # Función al cambiar selección
            button_color= "lightgray",
            button_hover_color= "lightgreen"
        )

        # Establecer valor predeterminado
        if valor_predeterminado:
            combobox.set(valor_predeterminado)
        elif opciones:
            combobox.set(opciones[0])

        # Ubicar en el grid
        combobox.grid(
            row=fila,
            column=columna,
            columnspan=ancho,
            rowspan=1,
            padx=5,
            sticky='ew'
        )

        return combobox

    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, ancho=70, alto=50, command=None, image = None):
        
        boton = ctk.CTkButton(
            parent,
            font=font,
            text=texto,
            fg_color=color_fondo,
            text_color='white',
            height=alto,
            width= ancho,
            command=command,
            image = image,
            corner_radius=10,
            hover_color= "lightgreen"
        )
        boton.grid(row=fila, column=columna, rowspan=alto, padx=5, sticky='ew')
        return boton

    # filtros
    
    def obtener_pacientes_filtrados(self):

        # Obtener la sede seleccionada
        sede_seleccionada = self.sede_var.get()
        if isinstance(sede_seleccionada, tuple):
            sede_seleccionada = sede_seleccionada[0]  # Tomar solo el string
        if sede_seleccionada == "Elije una opción":
            print("No se ha seleccionado una sede válida.")
            return [], False # No continuar si no hay sede
        #print("La sede es:", sede_seleccionada)

        # Convertir nombre de sede a ID
        id_sede = self.obtener_id_sede(sede_seleccionada)
        #print("El ID es:", id_sede)
        if not id_sede:
            return [], False

        # Filtrar pacientes por sede
        id_realizado = self.obtener_id_estado("Realizado")
        pacientes_por_sede = [
            paciente for paciente in self.datos_db
            if paciente.get("sede") == id_sede
            and paciente.get("estado", "") in ((id_realizado, ))
        ]

        # Filtrar por fecha si está seleccionada
        fecha_str = self.fecha.get().strip()
        if fecha_str:
            
            fecha_sel = datetime.strptime(fecha_str, "%d/%m/%Y").date()
            pacientes_por_sede_y_fecha = [
                paciente for paciente in pacientes_por_sede
                if paciente.get("fecha_citacion") == fecha_sel
            ]
            
            # Filtrar por identificación si hay texto
            identificacion_texto = self.identificacion_var.get().strip()

            if identificacion_texto:
                pacientes_por_sede_y_fecha = [
                    p for p in pacientes_por_sede_y_fecha
                    if identificacion_texto in str(p.get("identificacion_paciente", ""))
                ]
            
            return pacientes_por_sede_y_fecha, True

        else:
            # Filtrar por identificación si hay texto
            identificacion_texto = self.identificacion_var.get().strip()
            #print("ID ingresada:", identificacion_texto)
            if identificacion_texto:
                pacientes_por_sede = [
                    p for p in pacientes_por_sede
                    if identificacion_texto in str(p.get("identificacion_paciente", ""))
                ]

        return pacientes_por_sede, True  # Retorna solo sede + identificación

    def visual_principal_datos(self):
        
        # Limpiar la galería o tabla antes de recargar
        for widget in self.frame_ppal_visual_datos.winfo_children():  # Ajusta frame_pacientes al frame donde muestras los pacientes
            widget.destroy()

        pacientes_filtrados, se_filtro = self.obtener_pacientes_filtrados()
        #print("Ejecutando visual...")
        #print(pacientes_filtrados)

        if not se_filtro:
            # No se ha filtrado nada
            debes_hacer_primero()
            return
        elif not pacientes_filtrados:
            # Se filtró pero no hay pacientes
            si_la_db_esta_vacia()
            return
            
        
        for fila_paciente, paciente in enumerate(pacientes_filtrados):
            
            # Para cada paciente, repetimos toda la estructura en una nueva "fila" vertical (grid row)
            # Pero como hay tres frames por paciente y luego una línea, asignamos filas escalonadas:
            # paciente 0 usa filas 0,1,2,3 ; paciente 1 usa filas 4,5,6,7 ; etc.

            base_row = fila_paciente * 4  # Multiplicamos para espaciar bloques por paciente

            datos_paciente_visual_ppal = ctk.CTkFrame(self.frame_ppal_visual_datos, fg_color='transparent')
            datos_paciente_visual_ppal.grid(row=base_row, column=0, columnspan = 16, sticky='nsew')
            datos_paciente_visual_ppal.grid_rowconfigure(list(range(2)), weight = 1)
            for col in range(15):
                datos_paciente_visual_ppal.grid_columnconfigure(col, weight=1)
            
            datos_paciente_visual_ppal1 = ctk.CTkFrame(self.frame_ppal_visual_datos, fg_color='transparent')
            datos_paciente_visual_ppal1.grid(row=base_row+1, column=0, sticky='nsew', columnspan = 15)
            datos_paciente_visual_ppal1.grid_rowconfigure(list(range(2)), weight = 1)
            for col in range(15):
                datos_paciente_visual_ppal1.grid_columnconfigure(col, weight=1)
                
            datos_paciente_visual_ppal2 = ctk.CTkFrame(self.frame_ppal_visual_datos, fg_color='transparent')
            datos_paciente_visual_ppal2.grid(row=base_row+2, column=0, sticky='nsew', columnspan = 15)
            datos_paciente_visual_ppal2.grid_rowconfigure(list(range(2)), weight = 1)
            for col in range(15):
                datos_paciente_visual_ppal2.grid_columnconfigure(col, weight=1)
                
            # Crear el frame como una línea negra
            linea1 = ctk.CTkFrame(self.frame_ppal_visual_datos, fg_color="#228822", height=10, width=0)
            linea1.grid(row=base_row+3, column=0, columnspan=15, sticky="ew", pady=10)

            # Asegurar que el alto del frame no cambie
            linea1.grid_propagate(False)
            
            # Configuración de datos
            campos = [
                {"label": "Identificación\nPaciente", "columna": "identificacion_paciente", "valor": paciente.get("identificacion_paciente", ""), "ancho": 130, "tipo": "entry"},
                {"label": "Nombre\nPaciente", "columna": "nombre_paciente", "valor": paciente.get("nombre_paciente", ""), "ancho": 350, "tipo": "entry"},
                {"label": "Fecha\nOrden", "columna": "fecha_orden", "valor": paciente.get("fecha_orden", ""), "ancho": 100, "tipo": "entry"},
                {"label": "Fecha\nEstudio", "columna": "fecha_citacion", "valor": paciente.get("fecha_citacion", ""), "ancho": 100, "tipo": "entry"},
                {"label": "Historia\nClinica", "columna": "hc", "valor": paciente.get("hc", ""), "ancho": 130, "tipo": "entry"},
                {"label": "Edad", "columna": "edad", "valor": paciente.get("edad", ""), "ancho": 40, "tipo": "entry"},
                {"label": "Rango\nEdad", "columna": "rango_edad", "valor": self.obtener_nombre_rango_edad(paciente.get("rango_edad", "")), "ancho": 60, "tipo": "entry"},
                {"label": "Ubicación\nPaciente", "columna": "ubicacion", "valor": paciente.get("ubicacion", ""), "ancho": 90, "tipo": "entry"},
                {"label": "Modalidad", "columna": "modalidad", "valor": self.obtener_nombre_modalidad(paciente.get("modalidad", "")), "ancho": 250, "tipo": "entry"},
                {"label": "Ayuno", "columna": "ayuno", "valor": paciente.get("ayuno", ""), "ancho": 40, "tipo": "entry"},
                {"label": "Diferido", "columna": "diferido", "valor": paciente.get("diferido", ""), "ancho": 40, "tipo": "entry"},
                {"label": "Autorización", "columna": "autorizacion", "valor": paciente.get("autorizacion", ""), "ancho": 40, "tipo": "entry"},
                {"label": "Anestesia", "columna": "anestesia", "valor": paciente.get("anestesia", ""), "ancho": 40, "tipo": "entry"},
                {"label": "Hora\nCitación\nEstudio", "columna": "hora citacion estudio", "valor": paciente.get("hora_citacion", ""), "ancho": 75, "tipo": "entry"},
                {"label": "Hora\nRealización\nEstudio", "columna": "hora realizacion estudio", "valor": paciente.get("hora_realizacion", ""), "ancho": 60, "tipo": "entry"},
                
            ]
            
            campos1 = [
                
                {"label": "Alergia","columna": "alergia", "valor": paciente.get("alergia", ""), "ancho": 40, "tipo": "entry"},
                {"label": "Tipo\nAlergia","columna": "tipo_alergia", "valor": paciente.get("tipo_alergia", ""), "ancho": 280, "tipo": "textbox"},
                {"label": "Estado","columna": "estado", "valor": self.obtener_nombre_estado(paciente.get("estado", "")), "ancho": 100, "tipo": "entry"},
                {"label": "Sede","columna": "sede", "valor": self.obtener_nombre_sede(paciente.get("sede", "")), "ancho": 100, "tipo": "entry"},
                {"label": "Causal Retraso","columna": "causal retraso", "valor": self.obtener_nombre_causal_retraso(paciente.get("causal_retraso", "")), "ancho": 300, "tipo": "entry"},
                {"label": "Aislamiento","columna": "aislamiento", "valor": paciente.get("aislamiento", ""), "ancho": 40, "tipo": "entry"},
                {"label": "Tipo\nAislamiento","columna": "tipo_aislamiento", "valor": paciente.get("tipo_aislamiento", ""), "ancho": 280, "tipo": "textbox"},
                {"label": "Diagnóstico","columna": "diagnostico", "valor": paciente.get("diagnostico", ""), "ancho": 300, "tipo": "textbox"},
                {"label": "Estudios Ordenados\nAl Paciente","columna": "estudios ordenados", "valor": paciente.get("estudios_ordenados_paciente", ""), "ancho": 300, "tipo": "textbox"},
            ]
            
            campos2 = [
                {"label": "Comentarios Tecnólogos","columna": "comentarios tecnologos", "valor": paciente.get("comentarios_tecnologo", ""), "ancho": 300, "tipo": "textbox"},
                {"label": "Comentar Con\nRadiólogo","columna": "comentar con radiologo", "valor": paciente.get("comentar_radiologo", ""), "ancho": 40, "tipo": "entry"},
                {"label": "Comentarios Del Radiólogo","columna": "comentarios del radiologo", "valor": paciente.get("comentarios_radiologo", ""), "ancho": 300, "tipo": "textbox"},
                {"label": "Personal A Cargo","columna": "personal a cargo", "valor": UsuarioActual.nombre, "ancho": 300, "tipo": "entry"},
                {"label": "Atrás", "color": "#00155c", "tipo": "boton", "ancho": 70, "alto":50, "command": self.salir, 'image' : None},
            ]

            # Generar etiquetas y entradas dinámicamente en fila 0 y 1
            for i, campo in enumerate(campos):
                # datos_paciente_visual_ppal.grid_columnconfigure(i, weight=campo["ancho"])
                self.crear_label(datos_paciente_visual_ppal, campo["label"], self.fonts['label_title'], 0, i)
                
                if campo["tipo"] == "entry":
                    
                    habilitar = campo["label"] == ""
                
                    datos, var = self.crear_entry(datos_paciente_visual_ppal, self.fonts['label'], campo["label"], campo["columna"], campo["valor"], 1, i, ancho_widget=campo["ancho"], habilitado=habilitar)
                    
                    self.entries[campo["columna"]] = var

            # Generar etiquetas y entradas dinámicamente en fila 2 y 3
            for i, campo1 in enumerate(campos1):
                
                self.crear_label(datos_paciente_visual_ppal1, campo1['label'], self.fonts['label_title'], 0, i)
                
                if campo1["tipo"] == "entry":
                    
                    habilitar = campo1["label"] == ""
                    datos, var = self.crear_entry(datos_paciente_visual_ppal1, self.fonts['label'], campo1["label"], campo1["columna"], campo1["valor"], 1, i, ancho_widget=campo1["ancho"], habilitado=habilitar)
                    self.entries[campo1["columna"]] = var
                    
                elif campo1["tipo"] == "textbox":
                    
                    textbox = self.crear_textbox(datos_paciente_visual_ppal1, self.fonts['label'],campo1["columna"], 1, i, ancho_widget=campo1["ancho"], valor_db=campo1["valor"])
                    self.textbox[campo1["columna"]] = textbox
                    
            # Generar etiquetas y entradas dinámicamente en fila 4 y 5
            for i, campo2 in enumerate(campos2):
                
                if campo2["tipo"] == "entry":
                    
                    self.crear_label(datos_paciente_visual_ppal2, campo2['label'], self.fonts['label_title'], 0, i)
                    habilitar = campo2["label"] == ""
                    
                    datos, var = self.crear_entry(datos_paciente_visual_ppal2, self.fonts['label'], campo2["label"], campo2["columna"], campo2["valor"], 1, i, ancho_widget=campo2["ancho"], habilitado=habilitar)
                    self.entries[campo2["columna"]] = var
                    
                elif campo2["tipo"] == "textbox":
                    
                    self.crear_label(datos_paciente_visual_ppal2, campo2['label'], self.fonts['label_title'], 0, i)
                    textbox = self.crear_textbox(datos_paciente_visual_ppal2, self.fonts['label'],campo2["columna"], 1, i, ancho_widget=campo2["ancho"], valor_db=campo2["valor"])
                    self.textbox[campo2["columna"]] = textbox
                    
                elif campo2["tipo"] == "boton":
                    self.crear_boton(
                        datos_paciente_visual_ppal2,
                        self.fonts['boton'],
                        campo2['label'],
                        campo2['color'],
                        1, 
                        i,
                        ancho=campo2["ancho"],
                        alto = campo2["alto"],
                        command=campo2['command'],
                        image= campo2['image']
                    )
        
    # obtener datos de la db
    
    def obtener_nombre_modalidad(self, id_modalidad):
        """Obtiene el nombre de la modalidad desde la base de datos usando su ID."""
        sql = "SELECT nombre_modalidad FROM modalidades WHERE id_modalidad = %s"
        self.db.cursor.execute(sql, (id_modalidad,))
        resultado = self.db.cursor.fetchone()
        return resultado[0] if resultado else None
    
    def obtener_id_modalidad(self, nombre_modalidad):
        """Obtiene el ID de modalidad basado en el nombre de la modalidad."""
        # La modalidad está en formato 'nombre (abreviación)', por lo que solo tomamos el nombre
        nombre_modalidad = nombre_modalidad.split(' (')[0]
        
        sql = "SELECT id_modalidad FROM modalidades WHERE nombre_modalidad = %s"
        self.db.cursor.execute(sql, (nombre_modalidad,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None
    
    def obtener_nombre_rango_edad(self, id_rangoedad):
        """Obtiene el nombre del rango edad desde la base de datos usando su ID."""
        sql = "SELECT rango FROM rangosedades WHERE id_rangoedad = %s"
        self.db.cursor.execute(sql, (id_rangoedad,))
        resultado = self.db.cursor.fetchone()
        return resultado[0] if resultado else None
    
    def obtener_id_rangoedad(self, rango):
        """Obtiene el ID de rango edad basado en el nombre del rango edad."""
        # tomamos el nombre del rango de edad
        nombre_rango_edad = rango.split(' (')[0]
        
        sql = "SELECT id_rangoedad FROM rangosedades WHERE rango = %s"
        self.db.cursor.execute(sql, (nombre_rango_edad,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None
    
    def obtener_nombre_aislamiento(self, id_aislamiento):
        """Obtiene el nombre del aislamiento desde la base de datos usando su ID."""
        sql = "SELECT nombre_aislamiento FROM aislamientos WHERE id_aislamiento = %s"
        self.db.cursor.execute(sql, (id_aislamiento,))
        resultado = self.db.cursor.fetchone()
        return resultado[0] if resultado else None
    
    def obtener_id_aislamiento(self, nombre_aislamiento):
        """Obtiene el ID del aislamiento basado en el nombre del aislamiento."""
        # tomamos el nombre
        nombre_aislamiento = nombre_aislamiento.split(' (')[0]
        
        sql = "SELECT id_aislamiento FROM aislamientos WHERE nombre_aislamiento = %s"
        self.db.cursor.execute(sql, (nombre_aislamiento,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None
    
    def obtener_nombre_estado(self, id_estado):
        """Obtiene el nombre del estado desde la base de datos usando su ID."""
        sql = "SELECT nombre_estado FROM estados WHERE id_estado = %s"
        self.db.cursor.execute(sql, (id_estado,))
        resultado = self.db.cursor.fetchone()
        return resultado[0] if resultado else None
    
    def obtener_id_estado(self, nombre_estado):
        """Obtiene el ID del estado basado en el nombre del estado."""
        # solo tomamos el nombre
        nombre_estado = nombre_estado.split(' (')[0]
        
        sql = "SELECT id_estado FROM estados WHERE nombre_estado = %s"
        self.db.cursor.execute(sql, (nombre_estado,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None
    
    def obtener_nombre_sede(self, id_sede):
        """Obtiene el nombre de la sede desde la base de datos usando su ID."""
        sql = "SELECT nombre_sede FROM sedes WHERE id_sede = %s"
        self.db.cursor.execute(sql, (id_sede,))
        resultado = self.db.cursor.fetchone()
    
        return resultado[0] if resultado else None
    
    def obtener_id_sede(self, nombre_sede):
        """Obtiene el ID de sede basado en el nombre de la sede."""
        # solo tomamos el nombre
        nombre_sede = nombre_sede.split(' (')[0]
        
        sql = "SELECT id_sede FROM sedes WHERE nombre_sede = %s"
        self.db.cursor.execute(sql, (nombre_sede,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None
    
    def obtener_sedes(self):
        
        # onbtenemos las sedes desde la DB
        
        sql = "SELECT nombre_sede FROM sedes"
        
        self.db.cursor.execute(sql)
        
        self.sedes = [fila[0] for fila in self.db.cursor.fetchall()]

        # Insertar opción por defecto
        
        if "Elige una opción" not in self.sedes:
            self.sedes.insert(0, "Elige una opción")
    
    def obtener_nombre_causal_retraso(self, id_retraso):
        """Obtiene el nombre del retraso desde la base de datos usando su ID."""
        sql = "SELECT causal_retraso FROM retrasos WHERE id_retraso = %s"
        self.db.cursor.execute(sql, (id_retraso,))
        resultado = self.db.cursor.fetchone()
        return resultado[0] if resultado else None
    
    def obtener_id_retraso(self, causal_retraso):
        """Obtiene el ID del retraso basado en el nombre del retraso."""
        # solo tomamos el nombre
        causal_retraso = causal_retraso.split(' (')[0]
        
        sql = "SELECT id_retraso FROM retrasos WHERE causal_retraso = %s"
        self.db.cursor.execute(sql, (causal_retraso,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None

    def obtener_nombre_usuario(self, id_usuario):
        """Obtiene el nombre del usuario desde la base de datos usando su ID."""
        sql = "SELECT nombre_usuario FROM usuarios WHERE id_usuario = %s"
        self.db.cursor.execute(sql, (id_usuario,))
        resultado = self.db.cursor.fetchone()
        return resultado[0] if resultado else None
    
    def obtener_id_usuario(self, nombre_usuario):
        """Obtiene el ID del usuario basado en el nombre del usuario."""
        # solo tomamos el nombre
        nombre_usuario = nombre_usuario.split(' (')[0]
        
        sql = "SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s"
        self.db.cursor.execute(sql, (nombre_usuario,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None
    
    def obtener_nombre_alergia(self, id_alergia):
        """Obtiene el nombre de la alergia desde la base de datos usando su ID."""
        sql = "SELECT nombre_alergia FROM alergias WHERE id_alergia = %s"
        self.db.cursor.execute(sql, (id_alergia,))
        resultado = self.db.cursor.fetchone()
        return resultado[0] if resultado else None
    
    def obtener_id_alergia(self, nombre_alergia):
        """Obtiene el ID de la alergia basado en el nombre de la alergia."""
        # solo tomamos el nombre
        nombre_alergia = nombre_alergia.split(' (')[0]
        
        sql = "SELECT id_alergia FROM alergias WHERE nombre_alergia = %s"
        self.db.cursor.execute(sql, (nombre_alergia,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None

    # limpiar la fecha
    
    def limpiar_fecha(self):
            
        """Muestra todos los pacientes de la sede actual (quita filtro de fecha)."""
        self.fecha.delete(0, 'end')  # Limpiar el Entry de fecha
        
        # Volver a mostrar pacientes filtrados solo por sede
        self.visual_principal_datos()
            
    def salir(self):
        
        from abrirventanas.abrir import abrir_ventana_visualizar_datos_ppal
        
        """Método personalizado para el botón Salir.
        Cierra la ventana de aislamientos y restablece la ventana de administración."""
        
        if self.db:
            self.db.cerrar_conexion()
            PanelPrincipalVisualizacionRealizados.conexion_realizada = None
        cerrar_conexion()

        # Cancelar cualquier after pendiente de este frame
        try:
            for after_id in self.frame.tk.eval('after info').split():
                try:
                    self.frame.after_cancel(after_id)
                except:
                    pass
        except:
            pass

        # Destruir todos los widgets hijos del frame principal, incluyendo scrollable frames
        def destruir_completo(widget):
            for child in widget.winfo_children():
                destruir_completo(child)
            try:
                widget.destroy()
            except:
                pass

        destruir_completo(self.frame.winfo_toplevel())
        
        abrir_ventana_visualizar_datos_ppal()
