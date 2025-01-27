import sys
import os

# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from ventanas.ventanasprograma import VentanaPrincipal
from ventanas.ventana_inicio import VentanaInicioPrograma #esta es la linea que queda
# from ventanas.ventana_registro_usuario import VentanaRegistroUsuario

# from ventanas.ventana_recuperacion_contrasena import RecuperacionContrasena


if __name__ == "__main__":
    
    # ventana_programa = VentanaPrincipal()
    # ventana = ventana_programa.obtener_ventana()
# este es el codigo 
    ventana_inicio = VentanaInicioPrograma()
    ventana_mostrar = ventana_inicio.obtener_ventana()
    
    # ventana_mostrar.deiconify()  # Asegura que la ventana sea visible
    # ventana_mostrar.lift()  # Trae la ventana al frente
    
    # ventana_registro_usuario = VentanaRegistroUsuario()
    # ventana_mostrar = ventana_registro_usuario.obtener_ventana()
    
    # ventana_recuperacion = RecuperacionContrasena()
    
    # ventana_mostrar = ventana_recuperacion.obtener_ventana()
    
    

    ventana_mostrar.mainloop()