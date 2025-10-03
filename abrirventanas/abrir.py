import sys
import os

# Agrega el directorio raíz del proyecto al PATH para poder importar módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ventanas.ventanasprograma import VentanaPrincipal

def abrir_ventana_ingreso():
    
    """# Importa las clases necesarias para construir la interfaz
    from frames.frame_base import FrameBase
    from contenidoframes.contenido_frame1 import ContenidoFrame1
    from contenidoframes.contenido_frame2 import ContenidoFrame2
    from contenidoframes.contenido_frame3 import ContenidoFrame3

    # Crea la ventana principal del programa
    ventana_programa = VentanaPrincipal()
    ventana = ventana_programa.obtener_ventana()
    
    # Aplica los ajustes de maximización y redimensionado
    ventana_programa.aplicar_ajustes_a_ventana(ventana)
    
    # Asegura que la ventana se muestre y quede en primer plano
    ventana.deiconify()  # Asegura que la ventana sea visible
    ventana.lift()  # Trae la ventana al frente
    
    # Crea los frames principales de la interfaz
    alto_pantalla_sup = 1
    
    frames = FrameBase(ventana, alto_pantalla_sup)
    frames_dict = frames.obtener_frames()
    
    # Inserta contenido en cada uno de los frames
    contenido_frame1 = ContenidoFrame1(frames_dict["framesup"])
    contenido_frame1.contenidotituloppal()
    contenido_frame1 = ContenidoFrame1(frames_dict["frame1"])
    contenido_frame1.contenidosframe1()
    contenido_frame2 = ContenidoFrame2(frames_dict["frame2"])
    contenido_frame2.contenidosframe2()
    contenido_frame3 = ContenidoFrame3(frames_dict["frame3"])
    contenido_frame3.contenidosframe3()"""
    
    # Importa las clases necesarias para construir la interfaz
    from ventanas.ventana_ingreso_pacientes import IngresarPacientes
    
    # Crea la ventana principal del programa
    ventana = IngresarPacientes()
    mostrar_ventana = ventana.obtener_ventana()
    mostrar_ventana.mainloop()
    
def abrir_ventana_modificar(paciente):  
    
    """# Importa las clases necesarias para construir la interfaz
    from frames.frame_base import FrameBase
    from contenidoframesmodificar.contenido_modificar_frame1 import ContenidoModificarFrame1
    from contenidoframesmodificar.contenido_modificar_frame2 import ContenidoModificarFrame2
    from contenidoframesmodificar.contenido_modificar_frame3 import ContenidoModificarFrame3
    
    # Crea la ventana principal del programa
    ventana_programa_modificar = VentanaPrincipal()
    ventana_modificar = ventana_programa_modificar.obtener_ventana()
    
    # Aplica los ajustes de maximización y redimensionado
    ventana_programa_modificar.aplicar_ajustes_a_ventana(ventana_modificar)
    
    # Asegura que la ventana se muestre y quede en primer plano
    ventana_modificar.deiconify()  # Asegura que la ventana sea visible
    ventana_modificar.lift()  # Trae la ventana al frente
    
    # Crea los frames principales de la interfaz
    alto_pantalla_sup = 1
    
    frames_dict_modificar = FrameBase(ventana_modificar, alto_pantalla_sup)
    frames_dict_modificar = frames_dict_modificar.obtener_frames()
    
    # Inserta contenido en cada uno de los frames
    contenido_frame1_modificar = ContenidoModificarFrame1(frames_dict_modificar["framesup"])
    contenido_frame1_modificar.contenidotituloppalmodificar()
    contenido_frame1_modificar = ContenidoModificarFrame1(frames_dict_modificar["frame1"])
    contenido_frame1_modificar.contenidosframe1modificar()
    contenido_frame2_modificar = ContenidoModificarFrame2(frames_dict_modificar["frame2"])
    contenido_frame2_modificar.contenidosframe2modificar()
    contenido_frame3_modificar = ContenidoModificarFrame3(frames_dict_modificar["frame3"])
    contenido_frame3_modificar.contenidosframe3modificar()"""
    
    # Importa las clases necesarias para construir la interfaz
    from ventanas.ventana_pacientes_modificar import PacientesModificar
    
    # Crea la ventana principal del programa
    ventana = PacientesModificar(paciente)
    mostrar_ventana = ventana.obtener_ventana()
    mostrar_ventana.mainloop()
    
def abrir_ventana_visualizar_datos_ppal():

    # Importa las clases necesarias para construir la interfaz
    from frames.frame_base_visualizacion import FrameBaseVisualizacion
    from ventanas.visualizar_datos_ppal import PanelPrincipalVisualizacion
    
    # Crea la ventana principal del programa
    ventana_visualizar_datos = VentanaPrincipal()
    ventana_visualizar = ventana_visualizar_datos.obtener_ventana()
    
    # Aplica los ajustes de maximización y redimensionado
    ventana_visualizar_datos.aplicar_ajustes_a_ventana(ventana_visualizar)
    
    # Asegura que la ventana se muestre y quede en primer plano
    ventana_visualizar.deiconify()  # Asegura que la ventana sea visible
    ventana_visualizar.lift()  # Trae la ventana al frente
    
    # Crea los frames principales de la interfaz
    alto_pantalla_sup = 1
    
    frames_dict = FrameBaseVisualizacion(ventana_visualizar, alto_pantalla_sup).obtener_frames()

    # Crea una sola instancia pasando ambos frames al constructor
    panel = PanelPrincipalVisualizacion(frames_dict['framesup'], frames_dict['frame1'])
    
    # Llama métodos para llenar cada frame
    panel.visual_principal_titulo()  # Se asume que maneja 'framesup'
    panel.visual_principal_datos()   # Se asume que maneja 'frame1'

def abrir_ventana_visualizar_datos_ppal_diferidos():

    # Importa las clases necesarias para construir la interfaz
    from frames.frame_base_visualizacion import FrameBaseVisualizacion
    from ventanas.visualizar_datos_diferidos import PanelPrincipalVisualizacionDiferidos
    
    # Crea la ventana principal del programa
    ventana_visualizar_datos = VentanaPrincipal()
    ventana_visualizar = ventana_visualizar_datos.obtener_ventana()
    
    # Aplica los ajustes de maximización y redimensionado
    ventana_visualizar_datos.aplicar_ajustes_a_ventana(ventana_visualizar)
    
    # Asegura que la ventana se muestre y quede en primer plano
    ventana_visualizar.deiconify()  # Asegura que la ventana sea visible
    ventana_visualizar.lift()  # Trae la ventana al frente}
    
    # Crea los frames principales de la interfaz
    alto_pantalla_sup = 1
    
    frames_dict = FrameBaseVisualizacion(ventana_visualizar, alto_pantalla_sup).obtener_frames()

    # Crea una sola instancia pasando ambos frames al constructor
    panel = PanelPrincipalVisualizacionDiferidos(frames_dict['framesup'], frames_dict['frame1'])
    
    # Llama métodos para llenar cada frame
    panel.visual_principal_titulo()  # Se asume que maneja 'framesup'
    panel.visual_principal_datos()   # Se asume que maneja 'frame1'

def abrir_ventana_visualizar_datos_ppal_realizados():

    # Importa las clases necesarias para construir la interfaz
    from frames.frame_base_visualizacion import FrameBaseVisualizacion
    from ventanas.visualizar_datos_realizados import PanelPrincipalVisualizacionRealizados
    
    # Crea la ventana principal del programa
    ventana_visualizar_datos = VentanaPrincipal()
    ventana_visualizar = ventana_visualizar_datos.obtener_ventana()
    
    # Aplica los ajustes de maximización y redimensionado
    ventana_visualizar_datos.aplicar_ajustes_a_ventana(ventana_visualizar)
    
    # Asegura que la ventana se muestre y quede en primer plano
    ventana_visualizar.deiconify()  # Asegura que la ventana sea visible
    ventana_visualizar.lift()  # Trae la ventana al frente
    
    # Crea los frames principales de la interfaz
    alto_pantalla_sup = 1
    
    frames_dict = FrameBaseVisualizacion(ventana_visualizar, alto_pantalla_sup).obtener_frames()

    # Crea una sola instancia pasando ambos frames al constructor
    panel = PanelPrincipalVisualizacionRealizados(frames_dict['framesup'], frames_dict['frame1'])
    
    # Llama métodos para llenar cada frame
    panel.visual_principal_titulo()  # Se asume que maneja 'framesup'
    panel.visual_principal_datos()   # Se asume que maneja 'frame1'

def abrir_ventana_visualizar_datos_ppal_cancelados(): 

    # Importa las clases necesarias para construir la interfaz
    from frames.frame_base_visualizacion import FrameBaseVisualizacion
    from ventanas.visualizar_datos_cancelados import PanelPrincipalVisualizacionCancelados
    
    # Crea la ventana principal del programa
    ventana_visualizar_datos = VentanaPrincipal()
    ventana_visualizar = ventana_visualizar_datos.obtener_ventana()
    
    # Aplica los ajustes de maximización y redimensionado
    ventana_visualizar_datos.aplicar_ajustes_a_ventana(ventana_visualizar)
    
    # Asegura que la ventana se muestre y quede en primer plano
    ventana_visualizar.deiconify()  # Asegura que la ventana sea visible
    ventana_visualizar.lift()  # Trae la ventana al frente
    
    # Crea los frames principales de la interfaz
    alto_pantalla_sup = 1
    
    frames_dict = FrameBaseVisualizacion(ventana_visualizar, alto_pantalla_sup).obtener_frames()

    # Crea una sola instancia pasando ambos frames al constructor
    panel = PanelPrincipalVisualizacionCancelados(frames_dict['framesup'], frames_dict['frame1'])
    
    # Llama métodos para llenar cada frame
    panel.visual_principal_titulo()  # Se asume que maneja 'framesup'
    panel.visual_principal_datos()   # Se asume que maneja 'frame1'

def abrir_ventana_visualizar_datos_ppal_radiologo():

    # Importa las clases necesarias para construir la interfaz
    from frames.frame_base_visualizacion import FrameBaseVisualizacion
    from ventanas.visualizar_datos_ppal_radiologo import PanelPrincipalVisualizacionRadiologo
    
    # Crea la ventana principal del programa
    ventana_visualizar_datos = VentanaPrincipal()
    ventana_visualizar = ventana_visualizar_datos.obtener_ventana()
    
    # Aplica los ajustes de maximización y redimensionado
    ventana_visualizar_datos.aplicar_ajustes_a_ventana(ventana_visualizar)
    
    # Asegura que la ventana se muestre y quede en primer plano
    ventana_visualizar.deiconify()  # Asegura que la ventana sea visible
    ventana_visualizar.lift()  # Trae la ventana al frente
    
    # Crea los frames principales de la interfaz
    alto_pantalla_sup = 1
    
    frames_dict = FrameBaseVisualizacion(ventana_visualizar, alto_pantalla_sup).obtener_frames()

    # Crea una sola instancia pasando ambos frames al constructor
    panel = PanelPrincipalVisualizacionRadiologo(frames_dict['framesup'], frames_dict['frame1'])
    
    # Llama métodos para llenar cada frame
    panel.visual_principal_titulo()  # Se asume que maneja 'framesup'
    panel.visual_principal_datos()   # Se asume que maneja 'frame1'

def abrir_ventana_registro_usuario(parent_window=None):
    
    # Importa las clases necesarias para construir la interfaz
    from ventanas.ventana_registro_usuario import VentanaRegistroUsuario
    
    # Crea la ventana principal del programa
    ventana_registro_usuario = VentanaRegistroUsuario(parent_window=parent_window)
    ventana_registro_usuario =ventana_registro_usuario.obtener_ventana()
    
    # Bloquea la interacción con otras ventanas hasta que se cierre esta (ventana modal)
    ventana_registro_usuario.grab_set()
    
    # Asegura que la ventana de registro se muestre (por si estaba oculta)
    ventana_registro_usuario.deiconify()
    
def abrir_ventana_recuperacion_contrasena(parent_window=None):
    
    # Importa las clases necesarias para construir la interfaz
    from ventanas.ventana_recuperacion_contrasena import RecuperacionContrasena
    
    # Crea la ventana principal del programa
    abrir_ventana_recuperacion = RecuperacionContrasena(parent_window=parent_window)
    
    abrir_recuperacion_contrasena = abrir_ventana_recuperacion.obtener_ventana()
    
    # Bloquea la interacción con otras ventanas hasta que se cierre esta (ventana modal)
    abrir_recuperacion_contrasena.grab_set()
    
    # Asegura que la ventana de registro se muestre (por si estaba oculta)
    abrir_recuperacion_contrasena.deiconify()

def abrir_ventana_envio_codigo(parent_window=None):
    
    # Importa las clases necesarias para construir la interfaz
    from ventanas.ventana_generacion_codigo import EnvioRecuperacionContrasena
    
    # Crea la ventana principal del programa
    abrir_ventana_recuperacion = EnvioRecuperacionContrasena(parent_window=parent_window)
    
    abrir_recuperacion_contrasena = abrir_ventana_recuperacion.obtener_ventana()
    
    # Bloquea la interacción con otras ventanas hasta que se cierre esta (ventana modal)
    abrir_recuperacion_contrasena.grab_set()
    
    # Asegura que la ventana de registro se muestre (por si estaba oculta)
    abrir_recuperacion_contrasena.deiconify()
    
def abrir_ventana_admon():
    
    # Importa las clases necesarias para construir la interfaz
    from ventanas.ventana_admon import VentanaAdmon
    
    # Crea la ventana principal del programa
    abrir_ventana_administrador = VentanaAdmon()
    
    # Habilitar todos los botones en esa misma instancia
    #abrir_ventana_administrador.set_botones_estado('normal')
    
    mostrar_ventana_admon = abrir_ventana_administrador.obtener_ventana()
    
    # Asegura que la ventana de registro se muestre (por si estaba oculta)
    mostrar_ventana_admon.deiconify()
    
    # Retorna la llamada a la función que abre la ventana del administrador
    return abrir_ventana_administrador

def abrir_ventana_inicio():
    
    # Importa las clases necesarias para construir la interfaz
    from ventanas.ventana_inicio import VentanaInicioPrograma
    
    # Crea la ventana principal del programa
    ventana_inicio = VentanaInicioPrograma().obtener_ventana()
    
    ventana_inicio.deiconify()

def cerrar_ppal(venta_principal):
    
    # Oculta la ventana principal sin destruirla (se puede volver a mostrar con deiconify)
    venta_principal.withdraw()

def cerrar_ppal_entrada(venta_principal, ventana_ingreso):
    
    # Cierra y destruye completamente la ventana principal
    venta_principal.destroy()
    
    # Cierra y destruye también la ventana de ingreso
    ventana_ingreso.destroy()
    
# ventanas del admon

def abrir_ventana_alergias(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de alergias
    from ventanas_admon.ventana_alergias import IngresoAlergias
    
    # Crea la instancia de la ventana de alergias, recibiendo como parámetro la ventana padre
    abrir_ventana_alergia = IngresoAlergias(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_alergia = abrir_ventana_alergia.obtener_ventana()
    
    # Hace que la ventana de alergias sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_alergia.grab_set()
    
    # Trae la ventana al frente y asegura que se muestre
    mostrar_ventana_alergia.lift()
    mostrar_ventana_alergia.deiconify()

def abrir_ventana_aislamiento(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de aislamientos
    from ventanas_admon.ventana_aislamientos import IngresoAislamientos
    
    # Crea la instancia de la ventana de aislamientos, pasando como parámetro la ventana padre
    abrir_ventana_aislamiento1 = IngresoAislamientos(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_aislamiento = abrir_ventana_aislamiento1.obtener_ventana()
    
    # Hace que la ventana sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_aislamiento.grab_set()
    
    # Asegura que la ventana se muestre (por si estaba oculta)
    mostrar_ventana_aislamiento.deiconify()

def abrir_ventana_rango_edad(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de rangos de edad
    from ventanas_admon.ventana_rango_edades import IngresoRangoEdades
    
    # Crea la instancia de la ventana de rangos de edad, recibiendo como parámetro la ventana padre
    abrir_ventana_rangoedad = IngresoRangoEdades(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_rangoedad = abrir_ventana_rangoedad.obtener_ventana()
    
    # Hace que la ventana sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_rangoedad.grab_set()
    
    # Asegura que la ventana se muestre (por si estaba oculta)
    mostrar_ventana_rangoedad.deiconify()

def abrir_ventana_estudio_ordenado(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de estudios ordenados
    from ventanas_admon.ventana_estudios_ordenados import IngresoEstudiosOrdenados
    
    # Crea la instancia de la ventana de estudios ordenados, pasando como parámetro la ventana padre
    abrir_ventana_estudiosordenados = IngresoEstudiosOrdenados(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_estudiosordenados = abrir_ventana_estudiosordenados.obtener_ventana()
    
    # Hace que la ventana sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_estudiosordenados.grab_set()
    
    # Asegura que la ventana se muestre (por si estaba oculta)
    mostrar_ventana_estudiosordenados.deiconify()
    
def abrir_ventana_estados(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de estados
    from ventanas_admon.ventana_estados import IngresoEstados
    
    # Crea la instancia de la ventana de estados, recibiendo como parámetro la ventana padre
    abrir_ventana_estado = IngresoEstados(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    
    # Hace que la ventana sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_estado.grab_set()
    
    # Asegura que la ventana se muestre (por si estaba oculta)
    mostrar_ventana_estado.deiconify()
    
def abrir_ventana_sedes(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de sedes
    from ventanas_admon.ventana_sedes import IngresoSedes
    
    # Crea la instancia de la ventana de sedes, recibiendo como parámetro la ventana padre
    abrir_ventana_estado = IngresoSedes(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    
    # Hace que la ventana sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_estado.grab_set()
    
    # Asegura que la ventana se muestre (por si estaba oculta)
    mostrar_ventana_estado.deiconify()
    
def abrir_ventana_ratrasos(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de retrasos
    from ventanas_admon.ventana_retrasos import IngresoRetrasos
    
    # Crea la instancia de la ventana de retrasos, recibiendo como parámetro la ventana padre
    abrir_ventana_estado = IngresoRetrasos(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    
    # Hace que la ventana sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_estado.grab_set()
    
    # Asegura que la ventana se muestre (por si estaba oculta)
    mostrar_ventana_estado.deiconify()
    
def abrir_ventana_cargos(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de cargos
    from ventanas_admon.ventana_cargos import IngresoCargos
    
    # Crea la instancia de la ventana de cargos, recibiendo como parámetro la ventana padre
    abrir_ventana_estado = IngresoCargos(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    
    # Hace que la ventana sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_estado.grab_set()
    
    # Asegura que la ventana se muestre (por si estaba oculta)
    mostrar_ventana_estado.deiconify()
    
def abrir_ventana_modalidad(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de modalidades
    from ventanas_admon.ventana_modalidades import IngresoModalidades
    
    # Crea la instancia de la ventana de modalidades, recibiendo como parámetro la ventana padre
    abrir_ventana_estado = IngresoModalidades(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    
    # Hace que la ventana sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_estado.grab_set()
    
    # Asegura que la ventana se muestre (por si estaba oculta)
    mostrar_ventana_estado.deiconify()  
    
def abrir_ventana_usuarios_admon(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de usuarios administrativos
    from ventanas_admon.ventana_usuarios import IngresoUsuariosAdmon
    
    # Crea la instancia de la ventana de usuarios administrativos, recibiendo como parámetro la ventana padre
    abrir_ventana_estado = IngresoUsuariosAdmon(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    
    # Hace que la ventana sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_estado.grab_set()
    
    # Asegura que la ventana se muestre (por si estaba oculta)
    mostrar_ventana_estado.deiconify()  
    
def abrir_ventana_pacientes_admon(parent_window=None):
    
    # Importa la clase que define la ventana de ingreso de pacientes administrativos
    from ventanas_admon.ventana_pacientes import IngresoPacientesAdmon
    
    # Crea la instancia de la ventana de pacientes administrativos, recibiendo como parámetro la ventana padre
    abrir_ventana_estado = IngresoPacientesAdmon(parent_window=parent_window)
    
    # Obtiene el objeto de la ventana creada
    mostrar_ventana_estado = abrir_ventana_estado.obtener_ventana()
    
    # Hace que la ventana sea modal (bloquea interacción con otras ventanas hasta cerrarla)
    mostrar_ventana_estado.grab_set()
    
    # Asegura que la ventana se muestre (por si estaba oculta)
    mostrar_ventana_estado.deiconify()