﻿import sys
import os

# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ventanas.ventanasprograma import VentanaPrincipal

def abrir_ventana_ingreso():
    
    from frames.frame_base import FrameBase
    from contenidoframes.contenido_frame1 import ContenidoFrame1
    from contenidoframes.contenido_frame2 import ContenidoFrame2
    from contenidoframes.contenido_frame3 import ContenidoFrame3
    
    ventana_programa = VentanaPrincipal()
    ventana = ventana_programa.obtener_ventana()
    
    # Aplica los ajustes de maximización y redimensionado
    ventana_programa.aplicar_ajustes_a_ventana(ventana)
    
    ventana.deiconify()  # Asegura que la ventana sea visible
    ventana.lift()  # Trae la ventana al frente
    
    alto_pantalla_sup = 1
    
    frames = FrameBase(ventana, alto_pantalla_sup)
    frames_dict = frames.obtener_frames()
    
    contenido_frame1 = ContenidoFrame1(frames_dict["framesup"])
    contenido_frame1.contenidotituloppal()
    contenido_frame1 = ContenidoFrame1(frames_dict["frame1"])
    contenido_frame1.contenidosframe1()
    contenido_frame2 = ContenidoFrame2(frames_dict["frame2"])
    contenido_frame2.contenidosframe2()
    contenido_frame3 = ContenidoFrame3(frames_dict["frame3"])
    contenido_frame3.contenidosframe3()
    
def abrir_ventana_modificar():  
    
    from frames.frame_base import FrameBase
    from contenidoframesmodificar.contenido_modificar_frame1 import ContenidoModificarFrame1
    from contenidoframesmodificar.contenido_modificar_frame2 import ContenidoModificarFrame2
    from contenidoframesmodificar.contenido_modificar_frame3 import ContenidoModificarFrame3
    
    # ventana.destroy()  # Cierra la ventana actual
    ventana_programa_modificar = VentanaPrincipal()
    ventana_modificar = ventana_programa_modificar.obtener_ventana()
    
    # Aplica los ajustes de maximización y redimensionado
    ventana_programa_modificar.aplicar_ajustes_a_ventana(ventana_modificar)
    
    ventana_modificar.deiconify()  # Asegura que la ventana sea visible
    ventana_modificar.lift()  # Trae la ventana al frente
    
    alto_pantalla_sup = 1
    
    frames_dict_modificar = FrameBase(ventana_modificar, alto_pantalla_sup)
    frames_dict_modificar = frames_dict_modificar.obtener_frames()
    
    contenido_frame1_modificar = ContenidoModificarFrame1(frames_dict_modificar["framesup"])
    contenido_frame1_modificar.contenidotituloppalmodificar()
    contenido_frame1_modificar = ContenidoModificarFrame1(frames_dict_modificar["frame1"])
    contenido_frame1_modificar.contenidosframe1modificar()
    contenido_frame2_modificar = ContenidoModificarFrame2(frames_dict_modificar["frame2"])
    contenido_frame2_modificar.contenidosframe2modificar()
    contenido_frame = ContenidoModificarFrame3(frames_dict_modificar["frame3"])
    contenido_frame.contenidosframe3modificar()
    
def abrir_ventana_visualizar_datos_ppal():
    
    from frames.frame_base_visualizacion import FrameBaseVisualizacion
    from ventanas.visualizar_datos_ppal import PanelPrincipalVisualizacion
    
    ventana_visualizar_datos = VentanaPrincipal()
    ventana_visualizar = ventana_visualizar_datos.obtener_ventana()
    
    # Aplica los ajustes de maximización y redimensionado
    ventana_visualizar_datos.aplicar_ajustes_a_ventana(ventana_visualizar)
    
    ventana_visualizar.deiconify()  # Asegura que la ventana sea visible
    ventana_visualizar.lift()  # Trae la ventana al frente
    alto_pantalla_sup = 1
    
    frames_dict = FrameBaseVisualizacion(ventana_visualizar, alto_pantalla_sup).obtener_frames()
    # frames_dict = frames_dict.obtener_frames()
    
    visualizar_datos_ppal = PanelPrincipalVisualizacion(frames_dict['framesup'])
    visualizar_datos_ppal.visual_principal_titulo()
    visualizar_datos = PanelPrincipalVisualizacion(frames_dict['frame1'])
    visualizar_datos.visual_principal_datos()

def abrir_ventana_registro_usuario():
    
    from ventanas.ventana_registro_usuario import VentanaRegistroUsuario
    
    ventana_registro_usuario = VentanaRegistroUsuario()
    ventana_registro_usuario =ventana_registro_usuario.obtener_ventana()
    
    # ventana_mostrar = ventana_registro_usuario.obtener_ventana()
    
    ventana_registro_usuario.deiconify()
    
def abrir_ventana_recuperacion_contrasena():
    
    from ventanas.ventana_recuperacion_contrasena import RecuperacionContrasena
    
    abrir_ventana_recuperacion = RecuperacionContrasena()
    
    abrir_recuperacion_contrasena = abrir_ventana_recuperacion.obtener_ventana()
    
    abrir_recuperacion_contrasena.deiconify()
    
def abrir_ventana_admon():
    
    from ventanas.ventana_admon import VentanaAdmon
    
    abrir_ventana_administrador = VentanaAdmon()
    
    mostrar_ventana_admon = abrir_ventana_administrador.obtener_ventana()
    
    mostrar_ventana_admon.deiconify()

def abrir_ventana_inicio():
    
    from ventanas.ventana_inicio import VentanaInicioPrograma
    
    ventana_inicio = VentanaInicioPrograma().obtener_ventana()
    
    ventana_inicio.deiconify()

def cerrar_ppal(venta_principal):
    
    venta_principal.destroy()

def cerrar_ppal_entrada(venta_principal, ventana_ingreso):
    
    venta_principal.destroy()
    
    ventana_ingreso.destroy()
    
# ventanas del admon

def abrir_ventana_alergias(parent_window=None):
    
    from ventanas_admon.ventana_alergias import IngresoAlergias
    
    abrir_ventana_alergia = IngresoAlergias(parent_window=parent_window)
    
    mostrar_ventana_alergia = abrir_ventana_alergia.obtener_ventana()
    mostrar_ventana_alergia.grab_set()
   
    mostrar_ventana_alergia.deiconify()
    mostrar_ventana_alergia.lift()

def abrir_ventana_aislamiento(parent_window=None):
    
    from ventanas_admon.ventana_aislamientos import IngresoAislamientos
    
    abrir_ventana_aislamiento1 = IngresoAislamientos(parent_window=parent_window)
    
    mostrar_ventana_aislamiento = abrir_ventana_aislamiento1.obtener_ventana()
    mostrar_ventana_aislamiento.grab_set()
    
    mostrar_ventana_aislamiento.deiconify()

def abrir_ventana_rango_edad(parent_window=None):
    
    from ventanas_admon.ventana_rango_edades import IngresoRangoEdades
    
    abrir_ventana_rangoedad = IngresoRangoEdades(parent_window=parent_window)
    
    mostrar_ventana_rangoedad = abrir_ventana_rangoedad.obtener_ventana()
    mostrar_ventana_rangoedad.grab_set()
    
    mostrar_ventana_rangoedad.deiconify()

def abrir_ventana_estudio_ordenado(parent_window=None):
    
    from ventanas_admon.ventana_estudios_ordenados import IngresoEstudiosOrdenados
    
    abrir_ventana_estudiosordenados = IngresoEstudiosOrdenados(parent_window=parent_window)
    
    mostrar_ventana_estudiosordenados = abrir_ventana_estudiosordenados.obtener_ventana()
    mostrar_ventana_estudiosordenados.grab_set()
    
    mostrar_ventana_estudiosordenados.deiconify()
    
def abrir_ventana_estados(parent_window=None):
    
    from ventanas_admon.ventana_estados import IngresoEstados
    
    abrir_ventana_estado = IngresoEstados(parent_window=parent_window)
    
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    mostrar_ventana_estado.grab_set()
    
    mostrar_ventana_estado.deiconify()
    
def abrir_ventana_sedes(parent_window=None):
    
    from ventanas_admon.ventana_sedes import IngresoSedes
    
    abrir_ventana_estado = IngresoSedes(parent_window=parent_window)
    
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    mostrar_ventana_estado.grab_set()
    
    mostrar_ventana_estado.deiconify()
    
def abrir_ventana_ratrasos(parent_window=None):
    
    from ventanas_admon.ventana_retrasos import IngresoRetrasos
    
    abrir_ventana_estado = IngresoRetrasos(parent_window=parent_window)
    
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    mostrar_ventana_estado.grab_set()
    
    mostrar_ventana_estado.deiconify()
    
def abrir_ventana_cargos(parent_window=None):
    
    from ventanas_admon.ventana_cargos import IngresoCargos
    
    abrir_ventana_estado = IngresoCargos(parent_window=parent_window)
    
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    mostrar_ventana_estado.grab_set()
    
    mostrar_ventana_estado.deiconify()
    
def abrir_ventana_modalidad(parent_window=None):
    
    from ventanas_admon.ventana_modalidades import IngresoModalidades
    
    abrir_ventana_estado = IngresoModalidades(parent_window=parent_window)
    
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    mostrar_ventana_estado.grab_set()
    
    mostrar_ventana_estado.deiconify()  