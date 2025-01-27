import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk

class RecuperacionContrasena():
    
    def __init__(self):
        
        ancho_ventana_nueva = 500
        alto_ventana_nueva = 350
        
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        self.root = ctk.CTk()
        
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)
        
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.title('Recuperación Contraseña')
        
        self.root.resizable(False, False)
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        
        self.fonts = {
            
            'title': ('verdana', 30,  'bold'),
            'label_title': ('verdana', 16,  'bold'),
            'label': ('verdana', 12,  'bold')
        }
        
        
        self.frame = ctk.CTkFrame(self.root, fg_color='transparent')
        
        self.frame.grid(row= 0, column = 0, sticky = 'nsew')
        
        self.frame_1 = ctk.CTkFrame(self.root, fg_color='transparent')
        
        self.frame_1.grid(row= 1, column = 0, sticky = 'nsew')
        
        self.frame_1_1 = ctk.CTkFrame(self.root, fg_color='transparent')
        
        self.frame_1_1.grid(row= 2, column = 0, sticky = 'nsew')
        
        self.frame_1_2 = ctk.CTkFrame(self.root, fg_color='transparent')
        
        self.frame_1_2.grid(row= 3, column = 0, sticky = 'nsew')
        
        self.frame_2 = ctk.CTkFrame(self.root, fg_color='transparent')
        
        self.frame_2.grid(row= 4, column = 0, sticky = 'nsew')
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        self.frame_1.grid_columnconfigure(0, weight=1)
        self.frame_1_1.grid_columnconfigure(0, weight=1)
        self.frame_1_2.grid_columnconfigure(0, weight=1)
        
        self.frame_2.grid_columnconfigure(1, weight=1)
        self.frame_2.grid_columnconfigure(2, weight=1)
        self.frame_2.grid_columnconfigure(3, weight=1)
        self.frame_2.grid_rowconfigure(0, weight=1)
        
        self.ventana_recuperacion_contrasena()
        
    def obtener_ventana(self):
        
        return self.root
    
    def ventana_recuperacion_contrasena(self):
        
        from abrirventanas.abrir import abrir_ventana_inicio
        
        campos = [
            
            {'label': 'Recuperación De\nContraseña', 'tipo': 'label'},
        ]
        
        campos1 = [
            
            {'label': 'Email', 'tipo': 'entry', 'ancho': 350, 'alto': 26, 'placeholder': 'Introduce tú Email'},
            
        ]
        
        campos1_1 = [
            
            
            {'label': 'Nueva Contraseña', 'tipo': 'entry', 'ancho': 350, 'alto': 26, 'placeholder': 'Introduce tú Nueva Contraseña'},
            
        ]
        
        campos1_2 = [
            
            
            {'label': 'Repite La Nueva Contraseña', 'tipo': 'entry', 'ancho': 350, 'alto': 26, 'placeholder': 'Repite tú Nueva Contraseña'},
            
        ]
        
        campos2 = [
            
            {"label": "Registrar\nContraseña", "color": "blue", "tipo": "boton", "ancho": 50, "alto":10, "command": None},
            {"label": "Regresar", "color": "greenyellow", "tipo": "boton", "ancho": 50, "alto":10, "command": lambda: (abrir_ventana_inicio(), self.root.destroy())},
            {"label": "Salir", "color": "red", "tipo": "boton", "ancho": 50, "alto":10, "command": self.root.destroy},
        ]       
         
        for i, campo in enumerate(campos):
            
            self.crear_label(self.frame, texto=campo['label'], fuente=self.fonts['title'], fila= 0, columna=0)
            
        for i, campo1 in enumerate(campos1):
            
            self.crear_label(self.frame_1, campo1['label'], self.fonts['label_title'], fila= i, columna=0)

            self.crear_entry(self.frame_1, font=self.fonts['label'], fila = i+1, columna=0, ancho=campo1['ancho'], alto=campo1['alto'], placeholder=campo1['placeholder'])
            
        for i, campo1_1 in enumerate(campos1_1):
            
            self.crear_label(self.frame_1_1, campo1_1['label'], self.fonts['label_title'], fila= i, columna=0)

            self.crear_entry(self.frame_1_1, font=self.fonts['label'], fila = i+1, columna=0, ancho=campo1_1['ancho'], alto=campo1_1['alto'], placeholder=campo1_1['placeholder'])
        
        for i, campo1_2 in enumerate(campos1_2):
            
            self.crear_label(self.frame_1_2, campo1_2['label'], self.fonts['label_title'], fila= i, columna=0)

            self.crear_entry(self.frame_1_2, font=self.fonts['label'], fila = i+1, columna=0, ancho=campo1_2['ancho'], alto=campo1_2['alto'], placeholder=campo1_2['placeholder'])
        
        for i, campo2 in enumerate(campos2):
            
            self.crear_boton(self.frame_2, self.fonts['label_title'], campo2['label'], campo2['color'], 0, i+1, campo2['alto'], campo2['ancho'], command=campo2['command'])
        
    def crear_label(self, parent, texto, fuente, fila, columna, ancho = 1, alto = 1):
        
        label = ctk.CTkLabel(parent,
                             text=texto,
                             font=fuente)
        
        label.grid(row=fila, column=columna, sticky='ew', columnspan=ancho, rowspan=alto, padx = 5)
        
        return label
    
    def crear_entry(self, parent, font, fila, columna, ancho = 1, alto = 1, ancho_widget = 300, alto_widget = 26, placeholder = ''):
        
        entry = ctk.CTkEntry(parent,
                            font= font,
                            width= ancho_widget,
                            height= alto_widget,
                            text_color='black',
                            corner_radius=10,
                            fg_color='lightblue',
                            placeholder_text= placeholder,
                            placeholder_text_color= 'gray'
                            )
        
        entry.grid(row = fila, column = columna, sticky= 'ew', padx = 5, columnspan = ancho, rowspan = alto)
        
        return entry
    
    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, ancho=70, alto=70, command=None):
        
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
        boton.grid(row=fila, column=columna, rowspan=alto, padx=15, pady= 15, sticky='ew')
        return boton