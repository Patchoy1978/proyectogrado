# import tkinter as tk
import customtkinter as ctk

class VentanaPrincipal():
    
    def __init__(self):
        
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        self.root = ctk.CTk()
        
        self.ancho_ventana = self.root.winfo_screenwidth()
        self.alto_ventana = self.root.winfo_screenheight()
        
        self.root.title('Entrega de Turno')
        
        self.root.iconbitmap('img/documento.ico')
        
        self.root.geometry(f'{self.ancho_ventana}x{self.alto_ventana}+0+0')
        
        self.root.state('zoomed')
        
        self.root.resizable(True, True)
        
    def obtener_ventana(self):
        # Retorna el objeto ventana principal
        return self.root
    
    def aplicar_ajustes_a_ventana(self, ventana_secundaria):
        # Establecer el tamaño de la ventana al tamaño de la pantalla
        self.root.geometry(f'{self.ancho_ventana}x{self.alto_ventana}+0+0')
        ventana_secundaria.state('zoomed')
        ventana_secundaria.resizable(True, True)
        