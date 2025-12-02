import sys
import os

import customtkinter as ctk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexion_DB.conexionDB import Conexion_DB

from abrirventanasemergentes.abrir_ventanas import (datos_ingresados,
                                                    campos_requeridos,
                                                    datos_existen,
                                                    eliminacion_realizada,
                                                    modificacion_realizada,
                                                    selecionar_datos,
                                                    abrir_ventana_conn_exito,
                                                    abrir_ventana_conn_fallida,
                                                    id_no_esta
                                                    )

class IngresoEstudiosOrdenados():
    
    def __init__(self, parent_window=None):
        
        self.parent_window = parent_window  # Guardamos la referencia del padre
        
        ancho_ventana_nueva = 600
        alto_ventana_nueva = 420
        
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        self.root = ctk.CTkToplevel()
        
        self.root.protocol("WM_DELETE_WINDOW", lambda:None)
        
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.title('Estudios')
        
        self.root.resizable(False,False)
        
        self.fonts = {
            
            'title': ('verdana', 26, 'bold'),
            'label_title': ('verdana', 14, 'bold'),
            'label': ('verdana', 12 ),
            'boton': ('verdana', 14, 'bold')
        }
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        self.frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame.grid(row= 0, column= 0, sticky='nsew')
        
        self.frame1 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame1.grid(row= 1, column= 0, sticky='nsew')
        
        self.frame2 = ctk.CTkFrame(self.root, fg_color='transparent')
        self.frame2.grid(row= 2, column= 0, sticky='nsew')
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame2.grid_rowconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.grid_columnconfigure(2, weight=1)
        
        try:
            
            self.db = Conexion_DB()
            self.db.conectar() 
            abrir_ventana_conn_exito()
        
        except:
            
            abrir_ventana_conn_fallida()
        
        self.estudio_id_seleccionado = None
        
        # Diccionarios para guardar variables y widgets entry
        self.vars = {}
        self.entries = {}
        
        self.alergia_id_seleccionada = None
        
        self.ingreso_datos()
        
        self.root.bind_all("<Return>", self.insertar_estudio)
        
    def obtener_ventana(self):
        
        return self.root
        
    def ingreso_datos(self):
        
        campos = [
            
            {'label': 'Ingreso Datos'}
        ]
        
        campos1 = [
            
            {'clave': 'estudio', 'label': 'Estudio', 'placeholder': 'Ingrese el Estudio','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'abreviacion','label': 'Abreviación', 'placeholder': 'Ingrese la Abreviación','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'busqueda','label': 'Resultado de la Busqueda', 'placeholder': 'Busqueda','ancho': 100, 'alto': 26, 'tipo':'textbox'}

        ]
        
        campos2 = [
            
            {'label': 'Ingresar', 'ancho': 100, 'alto': 30, 'color':'#00155c', 'command': self.insertar_estudio},
            {'label': 'Eliminar', 'ancho': 100, 'alto': 30, 'color':'#00155c', 'command': self.eliminar_estudio},
            {'label': 'Modificar', 'ancho': 100, 'alto': 30, 'color':'#00155c', 'command': self.modificar_estudio},
            {'label': 'Salir', 'ancho': 100, 'alto': 30, 'color':'#00155c', 'command': self.salir},
        ]
        
        
        for i, campo in enumerate(campos):
        
            self.crear_label(self.frame, text=campo['label'], font=self.fonts['title'], fila=0, columna=0)
            
        for i, campo1 in enumerate(campos1):
            # Se coloca la etiqueta de cada campo
            self.crear_label(self.frame1, text=campo1['label'], font=self.fonts['label_title'], fila=i*2+1, columna=0)
            
            if campo1['tipo'] == 'entry':
                # Creamos la variable de control para el entry y lo guardamos en el diccionario
                self.vars[campo1['clave']] = ctk.StringVar()
                # Si deseas, puedes agregar trace para modificar el texto a Title (por ejemplo en el entry "estudio")
                if campo1['clave'] == 'estudio':
                    self.vars[campo1['clave']].trace_add("write", self.actualizar_a_title)
                    self.vars[campo1['clave']].trace_add("write", self.buscar_estudio)
                    # Además puedes agregar otro trace para buscar mientras se escribe:
                else:
                    
                    self.vars[campo1['clave']].trace_add("write", self.actualizar_a_title)
                    self.vars[campo1['clave']].trace_add("write", self.buscar_estudio)
                
                # Se crea el entry y se almacena en el diccionario
                self.entries[campo1['clave']] = self.crear_entry(
                    self.frame1,
                    font=self.fonts['label'],
                    fila=i*2+2,
                    columna=0,
                    ancho_widget=campo1['ancho'],
                    alto_widget=campo1['alto'],
                    placeholder=campo1['placeholder'],
                    textvariable=self.vars[campo1['clave']]
                )
            elif campo1['tipo'] == 'textbox':
                # Se crea el textbox y se asigna a un atributo específico
                self.textbox_resultados = self.crear_textbox(
                    self.frame1,
                    font=self.fonts['label'],
                    fila=i*2+2,
                    columna=0,
                    alto=campo1['alto'],
                    ancho=campo1['ancho']
                )

        for i, campo2 in enumerate(campos2):
        
            self.crear_boton(self.frame2, 
                            font=self.fonts['boton'], 
                            texto= campo2['label'], 
                            color_fondo= campo2['color'], 
                            fila=0, 
                            columna= i+1, 
                            ancho=campo1['ancho'], 
                            alto= campo1['alto'], 
                            command = campo2['command']
                            )
            
        # para insertar
            
        self.sql_statement = """insert into estudiosordenados (nombre_estudio, abreviacion) values (%s, %s)"""
    
    def actualizar_a_title(self, *args):
        """
        Callback que actualiza el contenido de la variable a formato Title.
        """
        
        # Actualizar el entry de 'estudio'
        texto_estudio = self.vars['estudio'].get()
        texto_title_estudio = texto_estudio.title()
        
        if texto_estudio != texto_title_estudio:
            self.vars['estudio'].set(texto_title_estudio)
            
        texto_abreviacion = self.vars['abreviacion'].get()
        texto_title_abreviacion = texto_abreviacion.upper()
        
        if texto_abreviacion != texto_title_abreviacion:
            self.vars['abreviacion'].set(texto_title_abreviacion)
    
    def insertar_estudio(self, event = None):
        
        # Obtener los valores de los entries usando las claves del diccionario
        
        estudio = self.entries['estudio'].get().strip()
        abreviacion = self.entries['abreviacion'].get().strip()
        
        if not estudio or not abreviacion:
            campos_requeridos()
            return
        
        # Consultar si el estudio ya existe en la base de datos (ajusta la consulta según corresponda)
        consulta_existencia = "SELECT COUNT(*) FROM listaestudios WHERE nombre_estudio = %s AND abreviacion = %s"
        self.db.cursor.execute(consulta_existencia, (estudio, abreviacion))
        resultado = self.db.cursor.fetchone()  # Usamos fetchone para un solo resultado

        if resultado[0] > 0:
            datos_existen()
            return  # No inserta si ya existe

        sql_insert = "INSERT INTO listaestudios (nombre_estudio, abreviacion) VALUES (%s, %s)"
        self.db.cursor.execute(sql_insert, (estudio, abreviacion))
        self.db.conexion.commit()
        datos_ingresados()
        # Limpiar los entries luego de la inserción
        self.vars['estudio'].set("")
        self.vars['abreviacion'].set("")
        
    def eliminar_estudio(self):
        
        estudio = self.entries['estudio'].get().strip()
        abreviacion = self.entries['abreviacion'].get().strip()
        
        if not estudio or not abreviacion:
            selecionar_datos()
            return
        
        sql_delete = "DELETE FROM listaestudios WHERE nombre_estudio = %s AND abreviacion = %s"
        self.db.cursor.execute(sql_delete, (estudio, abreviacion))
        self.db.conexion.commit()
        eliminacion_realizada()
        self.vars['estudio'].set("")
        self.vars['abreviacion'].set("")
    
    def buscar_estudio(self, *args):
        
        estudio = self.vars['estudio'].get().strip()

        # Limpiar el textbox de resultados
        self.textbox_resultados.configure(state="normal")
        self.textbox_resultados.delete("1.0", "end")

        if not estudio:
            self.textbox_resultados.configure(state="disabled")
            return

        sql_buscar_estudio = "SELECT id_estudio, nombre_estudio, abreviacion FROM listaestudios WHERE nombre_estudio LIKE %s"
        self.db.cursor.execute(sql_buscar_estudio, (f"%{estudio}%",))
        resultados = self.db.cursor.fetchall()

        if resultados:
            for resultado in resultados:
                id_estudio, nombre, abreviacion = resultado
                self.textbox_resultados.insert("end", f"{id_estudio}: {nombre} - {abreviacion}\n")
        else:
            self.textbox_resultados.insert("end", "No hay coincidencias")

        self.textbox_resultados.configure(state="disabled")
        self.textbox_resultados.bind("<ButtonRelease-1>", self.seleccionar_estudio)
    
    def modificar_estudio(self):
        
        estudio_nuevo = self.entries['estudio'].get().strip()
        abreviacion_nueva = self.entries['abreviacion'].get().strip()

        if not estudio_nuevo or not abreviacion_nueva:
            selecionar_datos()
            return

        # Verificar si se ha seleccionado una modalidad
        if not self.estudio_id_seleccionado:
            id_no_esta()
            return

        sql_modificar_estudio = "UPDATE listaestudios SET nombre_estudio = %s, abreviacion = %s WHERE id_estudio = %s"
        self.db.cursor.execute(sql_modificar_estudio, (estudio_nuevo, abreviacion_nueva, self.estudio_id_seleccionado))
        self.db.conexion.commit()
        modificacion_realizada()

        # Limpiar los campos
        self.textbox_resultados.configure(state="normal")
        self.textbox_resultados.delete("1.0", "end")
        self.vars['estudio'].set("")
        self.vars['abreviacion'].set("")
        self.estudio_id_seleccionado = None  # Resetear la selección
        self.textbox_resultados.configure(state="disabled")
    
    def obtener_resultados_busqueda(self, estudio):
        
        # Realiza la búsqueda en la base de datos y devuelve los resultados
        sql_buscar_estudio = "SELECT id_estudio, nombre_estudio, abreviacion FROM listaestudios WHERE nombre_estudio LIKE %s"
        self.db.cursor.execute(sql_buscar_estudio, (f"%{estudio}%",))
        resultados = self.db.cursor.fetchall()
        
        # Crear un diccionario con los resultados, {id_alergia: nombre_alergia}
        estudio_dict = {}
        for resultado in resultados:
            estudio_dict[resultado[0]] = resultado[1]  # {id_alergia: nombre_alergia}
        
        return estudio_dict
    
    def seleccionar_estudio(self, event):
        
        # Obtener la línea donde se hizo clic
        widget = event.widget
        index = widget.index("@%d,%d linestart" % (event.x, event.y))  # Obtiene el índice de la línea
        seleccion = widget.get(index, "%s lineend" % index).strip()  # Obtiene el contenido de la línea

        # Verificar que la línea no esté vacía
        if not seleccion:
            return

        # Extraer el ID (número antes de ":")
        id_estudio, datos = seleccion.split(":", 1)
        id_estudio = id_estudio.strip()
        nombre_estudio, abreviacion = datos.split(" - ")

        # Guardar ID en la variable para modificar/eliminar
        self.estudio_id_seleccionado = id_estudio

        # Colocar los datos en los Entry
        self.vars['estudio'].set(nombre_estudio.strip())
        self.vars['abreviacion'].set(abreviacion.strip())
    
    def obtener_id_estudio_seleccionado(self, estudio_nombre):
        
        sql_buscar_id = "SELECT id_estudio FROM listaestudios WHERE nombre_estudio = %s"
        self.db.cursor.execute(sql_buscar_id, (estudio_nombre,))
        resultado = self.db.cursor.fetchone()  # Obtener solo un resultado
        return resultado[0] if resultado else None

    def crear_label(self, parent, text, font, fila, columna, ancho= 1, alto= 1):
        
        label = ctk.CTkLabel(parent,
                            text=text,
                            font=font,
                            text_color= '#484a4b'
                            )
        label.grid(row= fila, column= columna, sticky='nsew', columnspan= ancho, rowspan= alto)
        
        return label
    
    def crear_entry(self,parent, font, fila, columna, placeholder, ancho=1, alto=1, ancho_widget=150, alto_widget=26, textvariable =None):
        
        entry = ctk.CTkEntry(parent,
                            font = font,
                            text_color='black',
                            corner_radius=10,
                            width=ancho_widget,
                            height=alto_widget,
                            fg_color='lightgray',
                            placeholder_text=placeholder,
                            placeholder_text_color= 'gray',
                            textvariable=textvariable
                            )
        entry.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto, padx=5, sticky='ew')
                
        return entry
        
    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, ancho=70, alto=70, command=None):
        
        boton = ctk.CTkButton(
                                parent,
                                font=font,
                                text=texto,
                                fg_color=color_fondo,
                                text_color='white',
                                height=alto,
                                width= ancho,
                                command=command,
                                corner_radius=10,
                                hover_color= "lightgreen"
                            )
        boton.grid(row=fila, column=columna, rowspan=alto, padx=15, pady= 15, sticky='nsew')
        return boton

    def crear_textbox(self, parent, font, fila, columna, alto, ancho):
        
        entry_textbox = ctk.CTkTextbox(parent,
                                    wrap=ctk.WORD,
                                    height=100,
                                    width=560,
                                    fg_color="lightgray",
                                    corner_radius=10,
                                    font=font,
                                    text_color='black',
                                    scrollbar_button_color= "lightgreen"
                                    )
    
        # Usamos grid después de crear el widget
        entry_textbox.grid(row=fila, column=columna, pady=5, padx=5, sticky='nsew')
        
        return entry_textbox

    def salir(self):
            """Método personalizado para el botón Salir.
            Cierra la ventana de alergias y restablece la ventana de administración."""
            
            if self.db:
                
                self.db.cerrar_conexion()  # Llamamos al método de cerrar conexión
            
            self.root.destroy()  # Cierra la ventana de alergias
            
            if self.parent_window:
                
                self.parent_window.deiconify()
                self.parent_window.lift()
