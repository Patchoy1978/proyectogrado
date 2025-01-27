import sys
import os

# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
                
import tkinter as tk

class FrameBaseVisualizacion():
    
    def __init__(self, ventana, alto_pantalla_sup):
        
        self.ventana = ventana
        
        # Configura el layout de la ventana principal usando grid
        self.ventana.grid_rowconfigure(0, weight=0)  # Frame superior (10% del alto total)
        self.ventana.grid_columnconfigure(0, weight=1)  # Frame 1
        
        # Frame superior
        self.frame_sup = tk.Frame(self.ventana, bg="white", height=alto_pantalla_sup, borderwidth=1)
        self.frame_sup.grid(row=0, column=0, columnspan=16, sticky="nsew")
        

        # Frame 1
        self.frame1 = tk.Frame(self.ventana, bg="white", borderwidth=1)
        self.frame1.grid(row=1, column=0, columnspan=15, sticky="ew")
        
        self.frames = {
            "framesup": self.frame_sup,
            "frame1": self.frame1,
        }
    
    def obtener_frames(self):
        return self.frames