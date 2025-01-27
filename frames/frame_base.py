import sys
import os

# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
                
import tkinter as tk
# from ventanas.ventanasprograma import VentanaPrincipal
# from contenidoframes.contenido_frame1 import ContenidoFrame1
# from contenidoframes.contenido_frame2 import ContenidoFrame2
# from contenidoframes.contenido_frame3 import ContenidoFrame3
# from contenidoframesmodificar.contenido_frame1_modificar import ContenidoFrame1modificar
# from contenidoframesmodificar.contenido_frame2_modificar import ContenidoFrame2modificar
# from contenidoframesmodificar.contenido_frame3_modificar import ContenidoFrame3modificar

class FrameBase():
    
    def __init__(self, ventana, alto_pantalla_sup):
        
        self.ventana = ventana
        
        # Configura el layout de la ventana principal usando grid
        self.ventana.grid_rowconfigure(0, weight=1)  # Frame superior (10% del alto total)
        self.ventana.grid_rowconfigure(1, weight=9)  # Frames inferiores (90% del alto total)
        self.ventana.grid_columnconfigure(0, weight=1)  # Frame 1
        self.ventana.grid_columnconfigure(1, weight=1)  # Frame 2
        self.ventana.grid_columnconfigure(2, weight=1)  # Frame 3

        # Frame superior
        self.frame_sup = tk.Frame(self.ventana, bg="white", height=alto_pantalla_sup, borderwidth=1)
        self.frame_sup.grid(row=0, column=0, columnspan=3, sticky="nsew")
        

        # Frame 1
        self.frame1 = tk.Frame(self.ventana, bg="white", borderwidth=1)
        self.frame1.grid(row=1, column=0, sticky="nsew")

        # Frame 2
        self.frame2 = tk.Frame(self.ventana, bg="white", borderwidth=1)
        self.frame2.grid(row=1, column=1, sticky="nsew")

        # Frame 3
        self.frame3 = tk.Frame(self.ventana, bg="white", borderwidth=1)
        self.frame3.grid(row=1, column=2, sticky="nsew")
        
        self.frames = {
            "framesup": self.frame_sup,
            "frame1": self.frame1,
            "frame2": self.frame2,
            "frame3": self.frame3
        }

    def obtener_frames(self):
        return self.frames