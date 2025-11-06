# Importa la biblioteca CustomTkinter y la asigna al alias 'ctk' para facilitar su uso.
import customtkinter as ctk 

class VentanaPrincipal():
    
    def __init__(self):
        
        ctk.set_appearance_mode('light') # Establece el modo de apariencia de la interfaz en "light" (claro).
        ctk.set_default_color_theme('green') # Define el tema de color predeterminado como "green".
        
        self.root = ctk.CTk()
        
        self.ancho_ventana = self.root.winfo_screenwidth() # Obtiene el ancho de la pantalla del usuario.
        self.alto_ventana = self.root.winfo_screenheight() # Obtiene el alto de la pantalla del usuario.
        
        self.root.title('Entrega de Turno') # Crea una ventana principal usando la clase CTk de CustomTkinter.
        
        self.root.iconbitmap('img/documento.ico') # Establece el icono de la ventana principal.
        
        self.root.geometry(f'{self.ancho_ventana}x{self.alto_ventana}+0+0') # Establece el tamaño y la posición de la ventana principal.
        
        self.root.state('zoomed') # Establece la ventana principal en modo de pantalla completa.
        
        self.root.resizable(True, True) # Permite que la ventana principal se redimensione.
        
    def obtener_ventana(self):
        
        # Retorna el objeto ventana principal
        return self.root
    
    def aplicar_ajustes_a_ventana(self, ventana_secundaria):
        
        # Establecer el tamaño de la ventana al tamaño de la pantalla
        self.root.geometry(f'{self.ancho_ventana}x{self.alto_ventana}+0+0')
        
        ventana_secundaria.state('zoomed') # Establece la ventana secundaria en modo de pantalla completa.
        
        ventana_secundaria.resizable(True, True) # Permite que la ventana secundaria se redimensione.
