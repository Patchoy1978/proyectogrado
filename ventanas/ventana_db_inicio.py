import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk

class VentanaDB():
    
    def __init__(self):
        
        ancho_ventana_nueva = 500
        alto_ventana_nueva = 450
        
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        self.root = ctk.CTk()
        
        self.root.protocol("WM_DELETE_WINDOW", lambda:None)
        
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.resizable(False,False)
        
        self.root.title('Entrega de Turno')
        
        self.fonts = {
            
            'title': ('verdana', 26,  'bold'),
            'label': ('verdana', 12,  'bold'),
            'boton': ('verdana', 18,  'bold')
        }
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        self.frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame.grid(row= 0, column= 0, sticky='nsew')
        
        self.frame1 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame1.grid(row= 1, column= 0, sticky='nsew')
        
        self.frame2 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame2.grid(row= 2, column= 0, sticky='nsew')
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame2.grid_rowconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.grid_columnconfigure(2, weight=1)
        
        self.ingreso_DB()
        
    def obtener_ventana(self):
        
        return self.root
    
    def ingreso_DB(self):
        
        from abrirventanas.abrir import abrir_ventana_inicio
        
        campos = [
            
            {'label': 'Bienvenido\nPrograma Entrega de Turno'}
        ]
        
        campos1 = [
            
            {'label': 'Ingresa el Host', 'placeholder': 'Host','ancho': 100, 'alto': 26},
            {'label': 'Ingresa el Usuario', 'placeholder': 'User','ancho': 100, 'alto': 26},
            {'label': 'Ingresa el Password', 'placeholder': 'Password','ancho': 100, 'alto': 26},
            {'label': 'Ingresa el Puerto', 'placeholder': 'Port','ancho': 100, 'alto': 26},
        ]
        
        campos2 = [
            
            {'label': 'Crear DB', 'placeholder': 'Host','ancho': 100, 'alto': 50, 'color':'lightblue', 'command': lambda: (self.crear_db(), abrir_ventana_inicio(), self.root.destroy())},
            {'label': 'Salir', 'placeholder': 'User','ancho': 100, 'alto': 50, 'color':'red', 'command': self.root.destroy},
        ]
        
        
        for i, campo in enumerate(campos):
        
            self.crear_label(self.frame, text=campo['label'], font=self.fonts['title'], fila=0, columna=0)
            
        for i, campo1 in enumerate(campos1):
    
            self.crear_label(self.frame1, text=campo1['label'], font=self.fonts['label'], fila=i*2+1, columna=0)
        
            entry = self.crear_entry(self.frame1, 
                             font=self.fonts['label'], 
                             fila=i*2+2, 
                             columna= 0, 
                             ancho_widget=campo1['ancho'], 
                             alto_widget= campo1['alto'], 
                             placeholder =campo1['placeholder']
                             )   
            
            # Asignar a las variables de instancia
            if campo1['placeholder'] == 'Host':
                self.entry_host = entry
            elif campo1['placeholder'] == 'User':
                self.entry_user = entry
            elif campo1['placeholder'] == 'Password':
                self.entry_password = entry
            elif campo1['placeholder'] == 'Port':
                self.entry_port = entry

        for i, campo2 in enumerate(campos2):
        
            self.crear_boton(self.frame2, 
                             font=self.fonts['boton'], 
                             texto= campo2['label'], 
                             color_fondo= campo2['color'], 
                             fila=0, 
                             columna= i+1, 
                             ancho=campo1['ancho'], 
                             alto= campo1['alto'], 
                             command = campo2['command']
                             )
            
    def crear_db(self):
        
        from CrearDB.crear_DB import ConexionDB
        
        from configuracion.guardar_datos import Guardar_datos_db  # Importamos la función creada
        
        # Obtener los valores ingresados en los Entry
        host = self.entry_host.get()
        user = self.entry_user.get()
        password = self.entry_password.get()
        port = int(self.entry_port.get())  # Convertir el puerto a entero

        # Guardar la configuración en el archivo JSON
        Guardar_datos_db(host, user, password, port)
        
        # Llamada a la conexión u otra lógica que tengas
        ConexionDB(host, user, password, port)
        
        
    def crear_label(self, parent, text, font, fila, columna, ancho= 1, alto= 1):
        
        label = ctk.CTkLabel(parent,
                             text=text,
                             font=font,
                             text_color= 'black'
                            )
        label.grid(row= fila, column= columna, sticky='nsew', columnspan= ancho, rowspan= alto)
        
        return label
    
    def crear_entry(self,parent, font, fila, columna, placeholder, ancho=1, alto=1, ancho_widget=150, alto_widget=26):
        
        entry = ctk.CTkEntry(parent,
                             font = font,
                             text_color='black',
                             corner_radius=10,
                             width=ancho_widget,
                             height=alto_widget,
                             fg_color='lightblue',
                             placeholder_text=placeholder,
                             placeholder_text_color= 'gray'
                            )
        entry.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto, padx=5, sticky='ew')
                
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
        boton.grid(row=fila, column=columna, rowspan=alto, padx=15, pady= 15, sticky='nsew')
        return boton
                             