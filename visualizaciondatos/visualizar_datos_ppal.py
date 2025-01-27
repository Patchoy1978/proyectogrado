import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import customtkinter as ctk
# import tkinter as tk
# import tkinter.font as tkfont

class PanelPrincipalVisualizacion():
    
    def __init__(self, frame):
        
        self.frame = frame
        
        frame.grid_rowconfigure(list(range(3)), weight = 1)
        frame.grid_columnconfigure(list(range(3)), weight = 1)
        
        self.fonts = {
            
            'title': ('verdana', 30, 'bold'),
            'title_frame': ('verdana', 24, 'bold'),
            'label': ('verdana', 11, 'bold'),
            'boton': ('verdana', 18, 'bold'),
        }

    def visual_principal_titulo(self):
        
        visual_datos_ppal = ctk.CTkFrame(self.frame, fg_color= 'transparent')
        visual_datos_ppal.grid(row=0, column=0, sticky='nsew', columnspan = 15)
        
        # Configurar las columnas del grid para que tengan el mismo peso
        for col in range(15):
            visual_datos_ppal.grid_columnconfigure(col, weight=1)  # Asignar peso igual a todas las columnas

        visual_datos_ppal.grid_rowconfigure(0, weight=1)
        
        titulo = ctk.CTkLabel(visual_datos_ppal, text='Visualización de datos', font=self.fonts['title'], anchor='center', text_color='black')
        titulo.grid(row=0, column=0, sticky='nsew', columnspan = 16)
        
        lab_identificacion_busc = ctk.CTkLabel(visual_datos_ppal, text='Identificación\nPaciente', font=self.fonts['label'],anchor='w', text_color= 'black')
        lab_identificacion_busc.grid(row=1, column=0, padx = 5, sticky='nsew')
        
        entry_identificacion_busc_paciente = ctk.CTkEntry(visual_datos_ppal,
                                                     font=self.fonts['label'],
                                                     text_color= 'black',
                                                     corner_radius= 30,
                                                     width= 180,
                                                     height= 26,
                                                     fg_color='lightblue')
        entry_identificacion_busc_paciente.configure(state='normal')
        entry_identificacion_busc_paciente.grid(row=1, column=1, sticky='nsew')
    
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


    def crear_entry(self,parent, font, valor_predeterminado, fila, columna, ancho=1, alto=1, ancho_widget=30, alto_widget=26):
        
        entry = ctk.CTkEntry(
            parent,
            font=font,
            text_color='black',
            corner_radius=10,
            width=ancho_widget,
            height=alto_widget,
            fg_color='lightblue'
        )
        entry.configure(state='normal')
        entry.insert('0', valor_predeterminado)
        entry.configure(state='disable')
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

    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, ancho=1, alto=1):
        
        boton = ctk.CTkButton(
            parent,
            font=font,
            text=texto,
            fg_color=color_fondo,
            text_color='black',
            height=50,
            width= 70,
            # command=comando,
            corner_radius=10
        )
        boton.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto, padx=5, sticky='ew')
        return boton

    def visual_principal_datos(self):
        
        datos_paciente_visual_ppal = ctk.CTkFrame(self.frame, fg_color='transparent')
        datos_paciente_visual_ppal.grid(row=0, column=0, columnspan = 15, sticky='nsew')
        
        datos_paciente_visual_ppal.grid_rowconfigure(list(range(2)), weight = 1)
        for col in range(15):
            datos_paciente_visual_ppal.grid_columnconfigure(col, weight=1)
        
        datos_paciente_visual_ppal1 = ctk.CTkFrame(self.frame, fg_color='transparent')
        datos_paciente_visual_ppal1.grid(row=1, column=0, sticky='nsew', columnspan = 9)
        
        datos_paciente_visual_ppal1.grid_rowconfigure(list(range(2)), weight = 1)
        for col in range(9):
            datos_paciente_visual_ppal1.grid_columnconfigure(col, weight=1)
            
        datos_paciente_visual_ppal2 = ctk.CTkFrame(self.frame, fg_color='transparent')
        datos_paciente_visual_ppal2.grid(row=2, column=0, sticky='nsew', columnspan = 9)
        
        datos_paciente_visual_ppal2.grid_rowconfigure(list(range(2)), weight = 1)
        for col in range(9):
            datos_paciente_visual_ppal2.grid_columnconfigure(col, weight=1)
        
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
            {"label": "Modificar", "color": "blue", "tipo": "boton"},
            {"label": "Cancelar", "color": "red", "tipo": "boton"},
            {"label": "Diferido", "color": "lightblue", "tipo": "boton"},
            {"label": "Realizado", "color": "greenyellow", "tipo": "boton"},
        ]

        # Generar etiquetas y entradas dinámicamente en fila 0 y 1
        for i, campo in enumerate(campos):
            # datos_paciente_visual_ppal.grid_columnconfigure(i, weight=campo["ancho"])
            self.crear_label(datos_paciente_visual_ppal, campo["label"], self.fonts['label'], 0, i)
            
            if campo["tipo"] == "entry":
                self.crear_entry(datos_paciente_visual_ppal, self.fonts['label'], campo["valor"], 1, i, ancho_widget=campo["ancho"])

        # Generar etiquetas y entradas dinámicamente en fila 2 y 3
        for i, campo1 in enumerate(campos1):
            
            self.crear_label(datos_paciente_visual_ppal1, campo1['label'], self.fonts['label'], 0, i)

            if campo1["tipo"] == "entry":
                
                self.crear_entry(datos_paciente_visual_ppal1, self.fonts['label'], campo1["valor"], 1, i, ancho_widget=campo1["ancho"])
                
            elif campo1["tipo"] == "textbox":
                
                self.crear_textbox(datos_paciente_visual_ppal1, self.fonts['label'], 1, i, ancho_widget=campo1["ancho"], valor_predeterminado=campo1["valor"])
        
        # Generar etiquetas y entradas dinámicamente en fila 4 y 5
        for i, campo2 in enumerate(campos2):
            
            

            if campo2["tipo"] == "entry":
                
                self.crear_label(datos_paciente_visual_ppal2, campo2['label'], self.fonts['label'], 0, i)
                self.crear_entry(datos_paciente_visual_ppal2, self.fonts['label'], campo2["valor"], 1, i, ancho_widget=campo2["ancho"])
                
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
                    i   
                )
        