import sys
import os

# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
                
import tkinter as tk
import customtkinter as ctk

class FrameBaseVisualizacion():
    
    def __init__(self, ventana, alto_pantalla_sup):
        
        self.ventana = ventana
        
        # Configura el layout de la ventana principal usando grid
        self.ventana.grid_rowconfigure(0, weight=0)  # Frame superior (10% del alto total)
        self.ventana.grid_columnconfigure(0, weight=1)  # Frame 1
        self.ventana.grid_columnconfigure(0, weight=1) 
        
        # Frame superior
        self.frame_sup = ctk.CTkFrame(self.ventana, fg_color="white", height=alto_pantalla_sup)
        self.frame_sup.grid(row=0, column=0, columnspan=17, sticky="nsew")
        

        # Frame 1
        self.frame1 = ctk.CTkFrame(self.ventana, fg_color="white")
        self.frame1.grid(row=1, column=0, columnspan=16, sticky="nsew")
        
        # Canvas y scrollbar para frame1

        self.canvas = tk.Canvas(self.frame1)

        self.scrollbar = ctk.CTkScrollbar(self.frame1, command=self.canvas.yview, button_color="lightblue", fg_color='transparent', width=15,)

        self.scrollable_frame = tk.Frame(self.canvas, bg="lightblue")

        # Configurar el canvas

        self.scrollable_frame.bind(

            "<Configure>",

            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configurar el scrollbar

        self.scrollbar.configure(command=self.canvas.yview)

        # Ubicar el canvas y el scrollbar

        self.scrollbar.grid(row=0, column=16, sticky='ns')

        self.canvas.grid(row=0, column=0, sticky='nsew')
        
        # Asegúrate de que el canvas se expanda

        self.frame1.grid_rowconfigure(0, weight=1)  # Permitir que el canvas ocupe el espacio

        self.frame1.grid_columnconfigure(0, weight=1)

        self.frames = {
            "framesup": self.frame_sup,
            "frame1": self.frame1,
        }
    
    def obtener_frames(self):
        return self.frames