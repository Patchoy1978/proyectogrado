import customtkinter as ctk
from PIL import Image
import os

# Crea la ventana raíz primero
root = ctk.CTk()

# Ahora carga las imágenes, pasando la referencia root si fuera necesario
ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), 'img'))
ruta_ojo_abierto = os.path.join(ruta_base, "ojoabierto.png")

ojo_abierto_img = ctk.CTkImage(light_image=Image.open(ruta_ojo_abierto).resize((50, 50)), size=(50, 50))

# Usa ojo_abierto_img en algún widget en root o en otro Frame creado desde root

root.mainloop()