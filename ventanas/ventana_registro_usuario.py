import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import customtkinter as ctk

class VentanaRegistroUsuario():
    
    def __init__(self):
        
        ancho_ventana_nueva = 900
    
        alto_ventana_nueva = 400
        
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        self.root = ctk.CTk()
        
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)

        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        self.root.title('Registro Usuario')
        
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.resizable(False,False)
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
               
        self.fonts = {
            
            'title': ('verdana', 26, 'bold'),
            'label': ('verdana', 14, 'bold'),
            'boton': ('verdana', 18, 'bold'),
        }
        
        self.frame = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame.grid(row= 0, column= 0, sticky= 'nsew')
        
        self.frame_widgets_sup = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame_widgets_sup.grid(row= 1, column= 0, sticky= 'nsew')
        
        self.frame_widgets_medio = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame_widgets_medio.grid(row= 2, column= 0, sticky= 'nsew')
        
        self.frame_widgets_medio1 = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame_widgets_medio1.grid(row= 3, column= 0, sticky= 'nsew')
        
        self.frame_widgets_inf = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame_widgets_inf.grid(row= 4, column= 0, sticky= 'nsew')
        
        self.frame.grid_columnconfigure(0, weight= 1)
        self.frame.grid_rowconfigure(0, weight= 1)
        # self.frame.grid_columnconfigure(1, weight= 1)
        # self.frame.grid_columnconfigure(2, weight= 1)
        # self.frame_widgets_sup.grid_rowconfigure(0, weight= 1)
        # self.frame_widgets_sup.grid_rowconfigure(1, weight= 1)
        
        self.frame_widgets_sup.grid_columnconfigure(1, weight= 1)
        self.frame_widgets_sup.grid_columnconfigure(2, weight= 1)
        self.frame_widgets_sup.grid_columnconfigure(3, weight= 1)
        # self.frame_widgets_sup.grid_rowconfigure(0, weight= 1)
        # self.frame_widgets_sup.grid_rowconfigure(1, weight= 1)
        
        
        self.frame_widgets_medio.grid_columnconfigure(1, weight= 1)
        self.frame_widgets_medio.grid_columnconfigure(2, weight= 1)
        self.frame_widgets_medio.grid_columnconfigure(3, weight= 1)
        
        self.frame_widgets_medio1.grid_columnconfigure(1, weight= 1)
        self.frame_widgets_medio1.grid_columnconfigure(2, weight= 1)
        self.frame_widgets_medio1.grid_columnconfigure(3, weight= 1)
        
        self.frame_widgets_inf.grid_columnconfigure(1, weight= 1)
        self.frame_widgets_inf.grid_columnconfigure(2, weight= 1)
        self.frame_widgets_inf.grid_columnconfigure(3, weight= 1)
        self.frame_widgets_inf.grid_rowconfigure(0, weight= 1)
        
        
        self.datos_ventana()
        
    def obtener_ventana(self):
        
        return self.root
    
    def datos_ventana(self):
        
        from abrirventanas.abrir import abrir_ventana_inicio
        
        campos = [
            
            {'label':'Bienvenido\nRegistro De Usuario'}
        ]
        
        campos1 = [
            
            {'label':'Nombre', 'ancho': 300, 'tipo':'entry', 'alto':26, 'placeholder':'Ingresa el Nombre'},
            {'label':'Identificación', 'ancho': 150, 'tipo':'entry', 'alto':26, 'placeholder':'Identificación Usuario'},
            {'label':'Email', 'ancho': 300, 'tipo':'entry', 'alto':26, 'placeholder':'Ingresa el Email'},
            
        ]
        
        campos2 = [
            
            {'label':'Contraseña', 'ancho': 200, 'tipo':'entry', 'alto':26, 'placeholder':'Ingresa Una Contraseña'},
            {'label':'Repetir Contraseña', 'ancho': 200, 'tipo':'entry', 'alto':26, 'placeholder':'Repite la Contraseña'},
            {'label':'Telefono', 'ancho': 150, 'tipo':'entry', 'alto':26, 'placeholder':'Telefono Empresa'},
        ]
        
        campos3 = [
            
            {'label':'Extensión', 'ancho': 80, 'tipo':'entry', 'alto':26, 'placeholder':'Extensión Empresa'},
            {"label": "Modalidad", "valor": "Alfaguara", "ancho": 200, "tipo": "combobox", "opciones": ["Resonancia", "Tomografia"]},
            {"label": "cargo", "valor": "Alfaguara", "ancho": 200, "tipo": "combobox", "opciones": ["Tecnólogo III", "Tecnólogo II"]},
        ]
        
        campos4 = [
            
            {"label": "Registrarse", "color": "yellow", "tipo": "boton", "ancho": 60, "alto":40, "command": None},
            {"label": "Regresar", "color": "lightgreen", "tipo": "boton", "ancho": 60, "alto":40, "command": lambda:(abrir_ventana_inicio(),self.root.destroy())},
            {"label": "Salir", "color": "red", "tipo": "boton", "ancho": 60, "alto":40, "command": self.root.destroy},
        ]
        
        for i, campo in enumerate(campos):
            
            self.crear_label(self.frame, font=self.fonts['title'], texto=campo['label'],fila= 0, columna= i)
        
        for i , campo in enumerate(campos1):
            
            self.crear_label(self.frame_widgets_sup, font=self.fonts['label'], texto=campo['label'],fila= 0, columna= i+1)
            
            self.crear_entry(self.frame_widgets_sup, font= self.fonts['label'], fila = 1, columna=i+1, ancho_widget = campo['ancho'], alto_widget= campo['alto'], placeholder= campo['placeholder'])
            
        for i , campo in enumerate(campos2):
            
            self.crear_label(self.frame_widgets_medio, font=self.fonts['label'], texto=campo['label'],fila= 0, columna= i+1)
            
            self.crear_entry(self.frame_widgets_medio, font= self.fonts['label'], fila = 1, columna=i+1, ancho_widget = campo['ancho'], alto_widget= campo['alto'], placeholder= campo['placeholder'])
            
        for i , campo in enumerate(campos3):
            
            if campo['tipo'] == 'entry':
                
                self.crear_label(self.frame_widgets_medio1, font=self.fonts['label'], texto=campo['label'],fila= 0, columna= i+1)
            
                self.crear_entry(self.frame_widgets_medio1, font= self.fonts['label'], fila = 1, columna=i+1, ancho_widget = campo['ancho'], alto_widget= campo['alto'], placeholder= campo['placeholder'])
            
            if campo['tipo'] == 'combobox':
                
                self.crear_label(self.frame_widgets_medio1, font=self.fonts['label'], texto=campo['label'],fila= 0, columna= i+1)
                
                self.crear_combobox(self.frame_widgets_medio1, 
                                    self.fonts['label'],
                                    fila=1,
                                    columna=i+1,
                                    ancho_widget=campo["ancho"],
                                    opciones=campo.get("opciones", []), 
                                    valor_predeterminado=campo["valor"]
                                    )
        
        for i, campo in enumerate(campos4):
        
            self.crear_boton(self.frame_widgets_inf, self.fonts['boton'], campo['label'], campo['color'], 0, i+1, campo['alto'], campo['ancho'], command=campo['command'])

    def crear_label(self,parent, font, texto, fila, columna,ancho=1, alto = 1):
        
        label = ctk.CTkLabel(parent,
                             font = font,
                             text = texto,
                             )
        label.grid(row = fila, column = columna, sticky = 'nsew', columnspan = ancho, rowspan = alto)
        
        return label
    
    def crear_entry(self, parent, font, fila, columna, ancho = 1, alto = 1, ancho_widget = 150, alto_widget = 26, placeholder=''):
        
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
        entry.grid(row = fila, column = columna, sticky = 'nsew', padx = 5, columnspan= ancho, rowspan = alto)
        
        return entry
    
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
        combobox.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto_widget, padx=5, sticky='nsew')
        return combobox
    
    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, ancho, alto, command=None):
        
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