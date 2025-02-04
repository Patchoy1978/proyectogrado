import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk

class VentanaAdmon():
    
    def __init__(self):
        
        ancho_ventana_nueva = 600
        alto_ventana_nueva = 500
        
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        self.root = ctk.CTk()
        
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.title('Ventana Admnistrador')
        
        self.root.resizable(False,False)
        
        self.fonts = {
            
            'title': ('verdana', 30, 'bold'),
            'boton': ('verdana', 16, 'bold'),
        }
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self.frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame.grid(row= 0, column = 0, sticky = 'nsew')
        
        self.frame1 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame1.grid(row= 1, column = 0, sticky = 'nsew')
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(1, weight=1)
        
        for i in range(6):
            
            self.frame1.grid_rowconfigure(i, weight=1)
        
        
        self.widgets_admon()
        
    def obtener_ventana(self):
        
        return self.root
    
    def widgets_admon(self):
        
        campos = [
            
            {'label': 'Administrar\nBases De Datos'}
        ]
        
        campos1 = [
            
            {'label': 'Pacientes', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
            {'label': 'Usuarios', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
            {'label': 'Alergias', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
            {'label': 'Aislamientos', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
            {'label': 'Rango Edades', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
            {'label': 'Estudios Ordenados', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
        ]
        
        campos2 = [
            
            {'label': 'Modalidades', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
            {'label': 'Estados', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
            {'label': 'Sedes', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
            {'label': 'Retrasos', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
            {'label': 'Cargos', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': None},
            {'label': 'Salir', 'tipo': 'boton', 'ancho' : 50, 'alto': 40, 'command': self.root.destroy},
        ]
        
        for i, campo in enumerate(campos):
        
            self.crear_label(self.frame, campo['label'], self.fonts['title'], fila = 0, columna = 0)
            
        for i, campo1 in enumerate(campos1):
            
            self.crear_boton(self.frame1,text= campo1['label'], font= self.fonts['boton'], fila = i, columna = 0, command= None, widget_alto = campo1['alto'], widget_ancho = campo1['ancho'])
        
        for i, campo1 in enumerate(campos2):
            
            self.crear_boton(self.frame1,text= campo1['label'], font= self.fonts['boton'], fila = i, columna = 1, command= campo1['command'], widget_alto = campo1['alto'], widget_ancho = campo1['ancho'])
        
    def crear_label(self, parent, texto, fuente, fila, columna, ancho = 1, alto = 1):
        
        label = ctk.CTkLabel(parent,
                             text= texto,
                             font= fuente
                             )
        label.grid(row=fila, column=columna, sticky='nsew', columnspan = ancho, rowspan = alto)
        
        return label
    
    def crear_boton(self, parent, text, font, fila, columna, command, widget_ancho = 60, widget_alto = 30):
        
        boton = ctk.CTkButton(parent,
                              text=text,
                              font=font,
                              text_color='black',
                              corner_radius=10,
                              command=command,
                              width=widget_ancho,
                              height=widget_alto,
                              )
        boton.grid(row= fila, column = columna, sticky= 'ew', pady = 5, padx = 5)
        
        return boton