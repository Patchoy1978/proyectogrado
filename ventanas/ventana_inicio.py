import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import customtkinter as ctk


class VentanaInicioPrograma():
    
    def __init__(self):
        
        # Definir el tamaño de la nueva ventana

        ancho_nueva_ventana = 500

        alto_nueva_ventana = 400
        
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        self.root = ctk.CTk()
        
        # Calcular la posición para centrar la ventana

        x = (self.root.winfo_screenwidth() // 2) - (ancho_nueva_ventana // 2)

        y = (self.root.winfo_screenheight() // 2) - (alto_nueva_ventana // 2)
        
        self.root.geometry(f"{ancho_nueva_ventana}x{alto_nueva_ventana}+{x}+{y}")
        
        self.root.title('Entrega De Turno')
        
        self.root.resizable(False, False)
        
        # Configuración de filas del root
        self.root.grid_rowconfigure(0, weight=1)  # Frame 1 (superior)
        self.root.grid_rowconfigure(1, weight=1)  # Frame 2 (medio)
        self.root.grid_rowconfigure(2, weight=1)  # Frame 3 (inferior)
        self.root.grid_columnconfigure(0, weight=1)
        # self.root.grid_columnconfigure(1, weight=1)
        # self.root.grid_columnconfigure(2, weight=1)
        
        self.fonts = {
            'title':('Verdana', 30, 'bold'),
            'label':('Verdana', 14, 'bold'),
            'label_titulo':('Verdana', 18, 'bold'),
            'boton':('Verdana', 18, 'bold'),
        }
        
        self.frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame.grid(row= 0, column= 0, sticky= 'nsew')
        
        # self.frame.grid_rowconfigure(0, weight=1)
        # self.frame.grid_columnconfigure(0, weight=1)
        
        self.frame1 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame1.grid(row= 1, column= 0, sticky= 'nsew')
        
        self.frame2 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame2.grid(row= 2, column= 0, sticky= 'nsew')
        
        # Configurar las columnas en cada frame
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)
        
        self.frame2.grid_columnconfigure(1, weight=1)  # Espacio a la izquierda
        self.frame2.grid_columnconfigure(2, weight=1)  # Columna para los botones
        self.frame2.grid_columnconfigure(3, weight=1)  # Espacio a la derecha

        self.frame2.grid_rowconfigure(0, weight=1)  # Espacio arriba
        self.frame2.grid_rowconfigure(1, weight=1)  # Fila para los botones
        self.frame2.grid_rowconfigure(2, weight=1)  # Espacio abajo
        
        self.ventana_datos_ingreso()
        
    def obtener_ventana(self):
        
        return self.root

    def ventana_datos_ingreso(self):
        
        from abrirventanas.abrir import abrir_ventana_visualizar_datos_ppal, abrir_ventana_registro_usuario, abrir_ventana_recuperacion_contrasena
        
        campos = [
            
            {'label': 'Bienvenido Al Sistema\nEntrega De Turno', 'ancho': 400, 'tipo': 'label'},
            
        ]
        
        campos1 = [
            
            {'label': 'Email', 'ancho': 400, 'tipo': 'entry'},
            {'label': 'Password', 'ancho': 400, 'tipo': 'entry'},
        ]
        
        campos2 = [
            
            {"label": "Registrarse", "color": "blue", "tipo": "boton", "ancho": 50, "alto":10, "command": lambda: (abrir_ventana_registro_usuario(), self.root.destroy())},
            {"label": " Ingresar ", "color": "greenyellow", "tipo": "boton", "ancho": 50, "alto":10, "command": lambda:(abrir_ventana_visualizar_datos_ppal(), self.root.destroy())},
            {"label": "Olvido\nContraseña", "color": "lightblue", "tipo": "boton", "ancho": 50, "alto":10, "command": lambda: (abrir_ventana_recuperacion_contrasena(), self.root.destroy())},

        ]
        
        for i, campo in enumerate(campos):
            
            self.crear_label(self.frame, texto= campo['label'], font=self.fonts['title'], fila=0, columna=0, ancho=campo['ancho'])
        
        for i, campo1 in enumerate(campos1):
            
            self.crear_label(self.frame1, texto= campo1['label'], font=self.fonts['label_titulo'], fila=i*2+1,columna=0, ancho=campo1['ancho'])
            
            self.crear_entry(self.frame1,
                            font=self.fonts['label'],
                            fila= i*2+2,
                            columna= 0,
                            ancho_widget=campo1['ancho']
                            )
        
        for i, campo2 in enumerate(campos2):
            
            self.crear_boton(self.frame2, self.fonts['boton'], campo2['label'], campo2['color'], 1, i+1, campo2['alto'], campo2['ancho'], command=campo2['command'])
        
    def crear_label(self,parent, texto, font, fila, columna, ancho = 1, alto = 1):
        
        label = ctk.CTkLabel(parent,
                            text= texto,
                            font=font,
                            
                            )
        label.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto, pady= 10, sticky= 'nsew')
        
        return label
    
    def crear_entry(self,parent, font, fila, columna, ancho=1, alto=1, ancho_widget=150, alto_widget=26):
        
        entry = ctk.CTkEntry(parent,
                             font = font,
                             text_color='black',
                             corner_radius=10,
                             width=ancho_widget,
                             height=alto_widget,
                             fg_color='lightblue'
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
        boton.grid(row=fila, column=columna, rowspan=alto, padx=15, pady= 15, sticky='ew')
        return boton
