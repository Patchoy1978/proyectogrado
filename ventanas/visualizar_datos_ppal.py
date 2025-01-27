import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import customtkinter as ctk
from tkcalendar import DateEntry
# import tkinter.font as tkfont

class PanelPrincipalVisualizacion():
    
    def __init__(self, frame):
        
        self.frame = frame
        
        # Configura el layout del frame usando grid

        self.frame.grid_rowconfigure(list(range(4)), weight=1)  # Permitir que todas las filas se expandan

        self.frame.grid_columnconfigure(list(range(16)), weight=1) 
        
        self.fonts = {
            
            'title': ('verdana', 30, 'bold'),
            'title_frame': ('verdana', 24, 'bold'),
            'label': ('verdana', 11, 'bold'),
            'boton': ('verdana', 18, 'bold'),
        }

    def visual_principal_titulo(self):
        
        from abrirventanas.abrir import abrir_ventana_ingreso, cerrar_ppal
        
        visual_datos_ppal = ctk.CTkFrame(self.frame, fg_color= 'transparent')
        visual_datos_ppal.grid(row=0, column=0, sticky='nsew', columnspan = 16)

        visual_datos_ppal.grid_columnconfigure(0, weight=1)
        visual_datos_ppal.grid_rowconfigure(0, weight=1)
        
        # Crear el frame como una línea negra
        linea = ctk.CTkFrame(self.frame, fg_color="lightblue", height=10, width=0)
        linea.grid(row=1, column=0, columnspan=16, sticky="ew", pady=10)

        # Asegurar que el alto del frame no cambie
        linea.grid_propagate(False)
        
        visual_datos_ppal1 = ctk.CTkFrame(self.frame, fg_color= 'transparent')
        visual_datos_ppal1.grid(row=2, column=0, sticky='nsew', columnspan = 16)
        
        # Configurar las columnas del grid para que tengan el mismo peso
        for col in range(16):
            visual_datos_ppal1.grid_columnconfigure(col, weight=1)  # Asignar peso igual a todas las columnas

        visual_datos_ppal1.grid_rowconfigure(0, weight=1)
        
        campos = [
            
            {"label": "Visualizacion De Datos", "valor": "", "ancho": 400, "tipo": "label"},
            
        ]
        
        campos1 =[
            
            {"label": "Sede", "valor": "Alfaguara", "ancho": 130, "tipo": "combobox", "opciones": ["Alfaguara", "San Joaquín", "Pance"]},
            {"label": "Fecha", "valor": "01/12/2024", "ancho": 100, "tipo": "fecha"},
            {"label": "Todos", "color": "greenyellow", "tipo": "boton", "alto": 26, "ancho":10, "command": None},
            {"label": "Identificación\nPaciente", "valor": "", "ancho": 130, "tipo": "entry"},
            {"label": "Ver\nDiferidos", "color": "lightblue", "tipo": "boton", "ancho": 26, "alto":30, "command": None},
            {"label": "Ver\nRealizados", "color": "yellow", "tipo": "boton", "ancho": 26, "alto":30, "command": None},
            {"label": "Nuevo\nPaciente", "color": "lightgreen", "tipo": "boton", "ancho": 26, "alto":30, "command": lambda:(abrir_ventana_ingreso(), cerrar_ppal(self.frame.winfo_toplevel()))},
        ]
        
        for i, campo in enumerate(campos):
            
            label = self.crear_label(visual_datos_ppal, campo["label"], self.fonts['title'], 0, i)
            label.grid(sticky='nsew')
        
        for i, campo in enumerate(campos1):
            
            if campo ["tipo"] == "combobox":
                
                self.crear_label(visual_datos_ppal1, campo["label"], self.fonts['label'], 0, i*2)
                
                self.crear_combobox(visual_datos_ppal1, 
                                    self.fonts['label'],
                                    fila=0,
                                    columna=i*2+1, 
                                    ancho_widget=campo["ancho"],
                                    opciones=campo.get("opciones", []), 
                                    valor_predeterminado=campo["valor"]
                                    )
            
            if campo ["tipo"] == "fecha":
                
                self.crear_label(visual_datos_ppal1, campo["label"], self.fonts['label'], 0, i*2)
                
                fecha = DateEntry(visual_datos_ppal1,
                                    width=5,
                                    background='lightblue',
                                    foreground='white',
                                    borderwidth=2,
                                    date_pattern= 'dd/MM/yyyy',
                                    font=self.fonts['label'],
                                    locale = 'es')
                
                fecha.grid(row=0, column= i*2+1, padx=5, sticky= 'nsew')

            if campo ["tipo"] == "entry":
                
                self.crear_label(visual_datos_ppal1, campo["label"], self.fonts['label'], 0, i*2)
                
                habilitar = campo["label"] == "Identificación\nPaciente"
                
                self.crear_entry(visual_datos_ppal1, self.fonts['label'],campo['valor'],0,i*2+1, ancho_widget=campo['ancho'], habilitado=habilitar)
                
            if campo['tipo'] == 'boton':
                
                self.crear_boton(visual_datos_ppal1, self.fonts['boton'], campo['label'], campo['color'], 0, i*2+1, campo['alto'], campo['ancho'], command=campo['command'])
        
        # Crear el frame como una línea negra
        linea1 = ctk.CTkFrame(self.frame, fg_color="lightblue", height=10, width=0)
        linea1.grid(row=3, column=0, columnspan=16, sticky="ew", pady=10)

        # Asegurar que el alto del frame no cambie
        linea1.grid_propagate(False)
    
    def crear_label(self,parent, texto, font, fila, columna, ancho=1, alto=1):
        
        label = ctk.CTkLabel(
            parent,
            text=texto,
            font=font,
            anchor='center',
            text_color='black'
        )
        label.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto, padx=5, sticky='nsew')
        return label


    def crear_entry(self,parent, font, valor_predeterminado, fila, columna, ancho=1, alto=1, ancho_widget=30, alto_widget=26, habilitado=False):
        
        entry = ctk.CTkEntry(
            parent,
            font=font,
            text_color='black',
            corner_radius=10,
            width=ancho_widget,
            height=alto_widget,
            fg_color='lightblue'
        )
        if habilitado:
            entry.configure(state='normal')  # Habilitar para escritura
        else:
            entry.configure(state='normal')
            entry.insert('0', valor_predeterminado)
            entry.configure(state='disable')  # Deshabilitar
            
        entry.insert('0', valor_predeterminado)
        entry.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto, padx=5, sticky='ew')
        return entry
    
    def crear_textbox(self,parent, font, fila, columna, ancho=1, alto_widget=65, ancho_widget=30, valor_predeterminado=''):
        
        textbox = ctk.CTkTextbox(
            parent,
            font=font,
            text_color='black',
            corner_radius=12,
            width=ancho_widget,
            height=alto_widget,
            fg_color='lightblue'
        )
        textbox.configure(state='normal')
        textbox.insert('0.0', valor_predeterminado)
        textbox.configure(state='disable')
        textbox.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto_widget, padx=5, sticky='ew')
        return textbox

    def crear_combobox(self,parent, font, fila, columna, alto_widget=26, ancho_widget=130, ancho=1, opciones=None, valor_predeterminado=''):
        
        # Si no hay opciones definidas, inicializamos una lista vacía
        if opciones is None:
            opciones = ['Ninguna']
        
        combobox = ctk.CTkOptionMenu(
            parent,
            font=font,
            text_color='black',
            corner_radius=10,
            width=ancho_widget,
            height=alto_widget,
            fg_color='lightblue',
            values=opciones,
        )
        # Establecer el valor predeterminado si está en las opciones
        if valor_predeterminado in opciones:
            combobox.set(valor_predeterminado)
        elif opciones:  # Si no está, selecciona la primera opción como predeterminada
            combobox.set(opciones[0])
        combobox.configure(state='readonly')
        combobox.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto_widget, padx=5, sticky='ew')
        return combobox

    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, ancho=70, alto=50, command=None):
        
        boton = ctk.CTkButton(
            parent,
            font=font,
            text=texto,
            fg_color=color_fondo,
            text_color='black',
            height=alto,
            width= ancho,
            command=command,
            corner_radius=10
        )
        boton.grid(row=fila, column=columna, rowspan=alto, padx=5, sticky='ew')
        return boton

    def visual_principal_datos(self):
        
        from abrirventanas.abrir import abrir_ventana_modificar, cerrar_ppal
        
        frame_ppal_visual_datos = ctk.CTkFrame(self.frame, fg_color='transparent')
        frame_ppal_visual_datos.grid(row=0, column=0, columnspan = 16, sticky='nsew')
        
        frame_ppal_visual_datos.grid_rowconfigure(list(range(4)), weight=1)  # Permitir que todas las filas se expandan

        frame_ppal_visual_datos.grid_columnconfigure(list(range(16)), weight=1) 
        
        datos_paciente_visual_ppal = ctk.CTkFrame(frame_ppal_visual_datos, fg_color='transparent')
        datos_paciente_visual_ppal.grid(row=0, column=0, columnspan = 16, sticky='nsew')
        
        datos_paciente_visual_ppal.grid_rowconfigure(list(range(2)), weight = 1)
        for col in range(15):
            datos_paciente_visual_ppal.grid_columnconfigure(col, weight=1)
        
        datos_paciente_visual_ppal1 = ctk.CTkFrame(frame_ppal_visual_datos, fg_color='transparent')
        datos_paciente_visual_ppal1.grid(row=1, column=0, sticky='nsew', columnspan = 15)
        
        datos_paciente_visual_ppal1.grid_rowconfigure(list(range(2)), weight = 1)
        for col in range(15):
            datos_paciente_visual_ppal1.grid_columnconfigure(col, weight=1)
            
        datos_paciente_visual_ppal2 = ctk.CTkFrame(frame_ppal_visual_datos, fg_color='transparent')
        datos_paciente_visual_ppal2.grid(row=2, column=0, sticky='nsew', columnspan = 15)
        
        datos_paciente_visual_ppal2.grid_rowconfigure(list(range(2)), weight = 1)
        for col in range(15):
            datos_paciente_visual_ppal2.grid_columnconfigure(col, weight=1)
            
        # Crear el frame como una línea negra
        linea1 = ctk.CTkFrame(frame_ppal_visual_datos, fg_color="lightblue", height=10, width=0)
        linea1.grid(row=3, column=0, columnspan=15, sticky="ew", pady=10)

        # Asegurar que el alto del frame no cambie
        linea1.grid_propagate(False)
        
        # Configuración de datos
        campos = [
            {"label": "Identificación\nPaciente", "valor": "1111222333444", "ancho": 130, "tipo": "entry"},
            {"label": "Nombre\nPaciente", "valor": "Francisco Julian Valencia Beltran", "ancho": 350, "tipo": "entry"},
            {"label": "Fecha\nOrden", "valor": "01/12/2024", "ancho": 100, "tipo": "entry"},
            {"label": "Fecha\nEstudio", "valor": "01/12/2024", "ancho": 100, "tipo": "entry"},
            {"label": "Historia\nClinica", "valor": "HC-1111222333", "ancho": 130, "tipo": "entry"},
            {"label": "Edad", "valor": "999", "ancho": 40, "tipo": "entry"},
            {"label": "Rango\nEdad", "valor": "Meses", "ancho": 60, "tipo": "entry"},
            {"label": "Ubicación\nPaciente", "valor": "SI-UPR27", "ancho": 90, "tipo": "entry"},
            {"label": "Modalidad", "valor": "Tomografia Axial Computarizada", "ancho": 250, "tipo": "entry"},
            {"label": "Ayuno", "valor": "Si", "ancho": 40, "tipo": "entry"},
            {"label": "Diferido", "valor": "No", "ancho": 40, "tipo": "entry"},
            {"label": "Autorización", "valor": "Si", "ancho": 40, "tipo": "entry"},
            {"label": "Anestesia", "valor": "No", "ancho": 40, "tipo": "entry"},
            {"label": "Hora\nCitación\nEstudio", "valor": "23:59", "ancho": 60, "tipo": "entry"},
            {"label": "Hora\nRealización\nEstudio", "valor": "23:59", "ancho": 60, "tipo": "entry"},
        ]
        
        campos1 = [
            
            {"label": "Alergia", "valor": "No", "ancho": 40, "tipo": "entry"},
            {"label": "Tipo\nAlergia", "valor": "Ninguno", "ancho": 300, "tipo": "textbox"},
            {"label": "Estado", "valor": "Modificado", "ancho": 100, "tipo": "entry"},
            {"label": "Sede", "valor": "Alfaguara", "ancho": 100, "tipo": "entry"},
            {"label": "Causal Retraso", "valor": "Ninguno", "ancho": 300, "tipo": "entry"},
            {"label": "Aislamiento", "valor": "No", "ancho": 40, "tipo": "entry"},
            {"label": "Tipo Aislamiento", "valor": "Ninguno", "ancho": 300, "tipo": "textbox"},
            {"label": "Diagnóstico", "valor": "Emesis", "ancho": 300, "tipo": "textbox"},
            {"label": "Estudios Ordenados", "valor": "Resonancia magnetica de abdomen", "ancho": 300, "tipo": "textbox"},
        ]
        
        campos2 = [
            
            {"label": "Comentarios Tecnólogos", "valor": "Paciente Colabora", "ancho": 300, "tipo": "textbox"},
            {"label": "Comentar Con\nRadiólogo", "valor": "No", "ancho": 40, "tipo": "entry"},
            {"label": "Comentarios Del Radiólogo", "valor": "Ningún Comentario", "ancho": 300, "tipo": "textbox"},
            {"label": "Personal A Cargo", "valor": "Francisco Julian Valencia Beltran", "ancho": 300, "tipo": "entry"},
            {"label": "Modificar", "color": "blue", "tipo": "boton", "ancho": 70, "alto":50, "command": lambda:(abrir_ventana_modificar(), cerrar_ppal(self.frame.winfo_toplevel()))},
            {"label": "Cancelar", "color": "red", "tipo": "boton", "ancho": 70, "alto":50, "command": None},
            {"label": "Diferido", "color": "lightblue", "tipo": "boton", "ancho": 70, "alto":50, "command": None},
            {"label": "Realizado", "color": "greenyellow", "tipo": "boton", "ancho": 70, "alto":50, "command": None},
        ]

        # Generar etiquetas y entradas dinámicamente en fila 0 y 1
        for i, campo in enumerate(campos):
            # datos_paciente_visual_ppal.grid_columnconfigure(i, weight=campo["ancho"])
            self.crear_label(datos_paciente_visual_ppal, campo["label"], self.fonts['label'], 0, i)
            
            if campo["tipo"] == "entry":
                
                habilitar = campo["label"] == ""
                self.crear_entry(datos_paciente_visual_ppal, self.fonts['label'], campo["valor"], 1, i, ancho_widget=campo["ancho"], habilitado=habilitar)

        # Generar etiquetas y entradas dinámicamente en fila 2 y 3
        for i, campo1 in enumerate(campos1):
            
            self.crear_label(datos_paciente_visual_ppal1, campo1['label'], self.fonts['label'], 0, i)

            if campo1["tipo"] == "entry":
                
                habilitar = campo["label"] == ""
                self.crear_entry(datos_paciente_visual_ppal1, self.fonts['label'], campo1["valor"], 1, i, ancho_widget=campo1["ancho"], habilitado=habilitar)
                
            elif campo1["tipo"] == "textbox":
                
                self.crear_textbox(datos_paciente_visual_ppal1, self.fonts['label'], 1, i, ancho_widget=campo1["ancho"], valor_predeterminado=campo1["valor"])
        
        # Generar etiquetas y entradas dinámicamente en fila 4 y 5
        for i, campo2 in enumerate(campos2):

            if campo2["tipo"] == "entry":
                
                self.crear_label(datos_paciente_visual_ppal2, campo2['label'], self.fonts['label'], 0, i)
                habilitar = campo["label"] == ""
                self.crear_entry(datos_paciente_visual_ppal2, self.fonts['label'], campo2["valor"], 1, i, ancho_widget=campo2["ancho"], habilitado=habilitar)
                
            elif campo2["tipo"] == "textbox":
                
                self.crear_label(datos_paciente_visual_ppal2, campo2['label'], self.fonts['label'], 0, i)
                self.crear_textbox(datos_paciente_visual_ppal2, self.fonts['label'], 1, i, ancho_widget=campo2["ancho"], valor_predeterminado=campo2["valor"])
                
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
                    command=campo2['command']
                )
        