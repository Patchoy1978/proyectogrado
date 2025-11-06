import sys
import os

import customtkinter as ctk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'img'))

from conexion_DB.conexionDB import Conexion_DB

from tkinter import messagebox

from PIL import Image

class IngresoPacientesAdmon():
    
    def __init__(self, parent_window=None):
        
        self.parent_window = parent_window  # Guardamos la referencia del padre
        
        ancho_ventana_nueva = 1200
        alto_ventana_nueva = 1050
        
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        self.root = ctk.CTkToplevel()
        
        self.root.protocol("WM_DELETE_WINDOW", lambda:None)
        
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.title('Usuarios')
        
        self.root.iconbitmap('img/documento.ico')
        
        self.root.resizable(False,False)
        
        self.fonts = {
            
            'title': ('verdana', 26, 'bold'),
            'label_title': ('verdana', 14, 'bold'),
            'label': ('verdana', 12 ),
            'boton': ('verdana', 14, 'bold')
        }
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        #self.root.grid_rowconfigure(1, weight=1)
        #self.root.grid_rowconfigure(2, weight=1)
        
        self.frame = ctk.CTkScrollableFrame(self.root, fg_color='transparent')
        self.frame.grid(row= 0, column= 0, columnspan = 2, sticky='nsew')
        
        self.frame_titulo = ctk.CTkFrame(self.frame, fg_color='transparent')
        self.frame_titulo.grid(row= 0, column= 0, columnspan = 2, sticky='ew')
        
        self.frame1 = ctk.CTkFrame(self.frame, fg_color='transparent')
        self.frame1.grid(row= 1, column= 0, sticky='nsew')
        
        self.frame2 = ctk.CTkFrame(self.frame, fg_color='transparent')
        self.frame2.grid(row= 1, column= 1, sticky='nsew')
        
        self.frame3 = ctk.CTkFrame(self.frame, fg_color='transparent')
        self.frame3.grid(row= 2, column= 0, columnspan = 2, sticky='ns')
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame_titulo.grid_columnconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame3.grid_columnconfigure(0, weight=1)
        #self.frame3.grid_rowconfigure(0, weight=1)
        
        
        
        self.db = Conexion_DB()
        self.db.conectar()  
        
        self.atras = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, 'atras.png')).resize((35,35)), size= (35,35))
        self.adelante = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base, 'adelante.png')).resize((35,35)), size= (35,35))
        
        # Diccionarios para guardar variables y widgets entry
        self.vars = {}
        self.entries = {}
        self.textbox = {}
        self.botones = {}
        self.acciones = {
                        'identificacion_paciente': self.buscar_paciente
                    }

        self.usuario_id_seleccionado = None
        
        self.buscando = False
        #self.root.bind_all("<Return>",)
        
        self.ingreso_datos()
        
    def obtener_ventana(self):
        
        return self.root
        
    def ingreso_datos(self):
        
        campos = [
            
            {'label': 'Eliminar Pacientes'}
        ]
        
        campos1 = [
            
            {'clave': 'identificacion_paciente','label': 'Identificación', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'nombre_paciente', 'label': 'Nombre Paciente', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'edad','label': 'Edad', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'rango_edad','label': 'Rango Edad', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'fecha_orden','label': 'Fecha Orden', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'fecha_citacion','label': 'Fecha Citación', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'hc','label': 'Historia Clínica', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'ubicacion','label': 'Ubicación', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'modalidad','label': 'Modalidad', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'estudios_ordenados_paciente','label': 'Estudios Ordenados Paciente', 'ancho': 100, 'alto': 26, 'tipo':'textbox'},
            {'clave': 'diagnostico','label': 'Diagnóstico', 'ancho': 100, 'alto': 26, 'tipo':'textbox'},
            {'clave': 'ayuno','label': 'Ayuno', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'diferido','label': 'Diferido', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'alergia','label': 'Alergia', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            

        ]
        
        campos2 = [
            
            {'clave': 'tipo_alergia','label': 'Tipo Alergia', 'ancho': 100, 'alto': 26, 'tipo':'textbox'},
            {'clave': 'aislamiento', 'label': 'Aislamiento', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'tipo_aislamiento','label': 'Tipo Aislamiento', 'ancho': 100, 'alto': 26, 'tipo':'textbox'},
            {'clave': 'autorizacion','label': 'Autorización', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'anestesia','label': 'Anestesia', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'estado','label': 'Estado', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'sede','label': 'Sede', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'hora_citacion','label': 'Hora Citación', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'hora_realizacion','label': 'Hora Realización', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'causal_retraso','label': 'Causal De Retraso', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'comentarios_tecnologo','label': 'Comentarios Del Tecnólogo', 'ancho': 100, 'alto': 26, 'tipo':'textbox'},
            {'clave': 'comentar_radiologo','label': 'Comentar Con El Radiólogo', 'ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'comentarios_radiologo','label': 'Comentarios Del Radiólogo', 'ancho': 100, 'alto': 26, 'tipo':'textbox'},

        ]
        
        campos3 = [

            {'clave' : 'anterior', 'label': "", 'ancho': 20, 'alto': 20, 'color':'transparent', 'command': self.paciente_anterior, 'image': self.atras, 'tipo':'boton', 'state' : 'normal'},
            {'clave': 'contador','label': None, 'ancho': 80, 'alto': 26, 'tipo':'entry'},
            {'clave' : 'siguiente', 'label': "", 'ancho': 20, 'alto': 20, 'color':'transparent', 'command': self.paciente_siguiente, 'image': self.adelante, 'tipo':'boton', 'state' : 'normal'},
            {'clave' : 'eliminar', 'label': 'Eliminar', 'ancho': 100, 'alto': 30, 'color':'#00155c', 'command': self.eliminar_paciente, 'image': None, 'tipo':'boton'},
            {'clave' : 'limpiar_campos', 'label': 'Limpiar Pantalla', 'ancho': 100, 'alto': 30, 'color':'#00155c', 'command': self.limpiar_campos, 'image': None, 'tipo':'boton', 'state' : 'normal'},
            {'clave' : 'salir', 'label': 'Salir', 'ancho': 100, 'alto': 30, 'color':'#00155c', 'command': self.salir, 'image': None, 'tipo':'boton', 'state' : 'normal'},
        ]
        
        
        for i, campo in enumerate(campos):
        
            self.crear_label(self.frame_titulo, text=campo['label'], font=self.fonts['title'], fila=0, columna=0)
            
        for i, campo1 in enumerate(campos1):
            # Se coloca la etiqueta de cada campo
            self.crear_label(self.frame1, text=campo1['label'], font=self.fonts['label_title'], fila=i*2+1, columna=0)
            
            if campo1['tipo'] == 'entry':
                # Creamos la variable de control para el entry y lo guardamos en el diccionario
                self.vars[campo1['clave']] = ctk.StringVar()
                
                # Solo asignamos la función a la traza si la clave está en el diccionario
                if campo1['clave'] in self.acciones:
                    self.vars[campo1['clave']].trace_add("write", self.acciones[campo1['clave']])
                
                # Se crea el entry y se almacena en el diccionario
                entry = self.crear_entry(
                    self.frame1,
                    font=self.fonts['label'],
                    fila=i*2+2,
                    columna=0,
                    ancho_widget=campo1['ancho'],
                    alto_widget=campo1['alto'],
                    textvariable=self.vars[campo1['clave']]
                )
                
                self.entries[campo1['clave']] = entry
                
            elif campo1['tipo'] == 'textbox':
                
                # Creamos la variable de control para el entry y lo guardamos en el diccionario
                self.vars[campo1['clave']] = ctk.StringVar()
                
                # Solo asignamos la función a la traza si la clave está en el diccionario
                if campo1['clave'] in self.acciones:
                    self.vars[campo1['clave']].trace_add("write", self.acciones[campo1['clave']])
                
                # Se crea el textbox y se asigna a un atributo específico
                self.textbox_resultados = self.crear_textbox(
                    self.frame1,
                    font=self.fonts['label'],
                    fila=i*2+2,
                    columna=0,
                    alto=campo1['alto'],
                    ancho=campo1['ancho']
                )
                
                self.textbox[campo1['clave']] = self.textbox_resultados
                
        for i, campo2 in enumerate(campos2):
            
            # Se coloca la etiqueta de cada campo
            self.crear_label(self.frame2, text=campo2['label'], font=self.fonts['label_title'], fila=i*2+1, columna=0)
        
            if campo2['tipo'] == 'entry':
                # Creamos la variable de control para el entry y lo guardamos en el diccionario
                self.vars[campo2['clave']] = ctk.StringVar()
                
                # Solo asignamos la función a la traza si la clave está en el diccionario
                if campo2['clave'] in self.acciones:
                    self.vars[campo2['clave']].trace_add("write", self.acciones[campo2['clave']])
                
                # Se crea el entry y se almacena en el diccionario
                entry = self.crear_entry(
                    self.frame2,
                    font=self.fonts['label'],
                    fila=i*2+2,
                    columna=0,
                    ancho_widget=campo2['ancho'],
                    alto_widget=campo2['alto'],
                    textvariable=self.vars[campo2['clave']]
                )
                
                self.entries[campo2['clave']] = entry
                
            elif campo2['tipo'] == 'textbox':
                
                # Creamos la variable de control para el entry y lo guardamos en el diccionario
                self.vars[campo2['clave']] = ctk.StringVar()
                
                # Solo asignamos la función a la traza si la clave está en el diccionario
                if campo2['clave'] in self.acciones:
                    self.vars[campo2['clave']].trace_add("write", self.acciones[campo2['clave']])
                
                # Se crea el textbox y se asigna a un atributo específico
                self.textbox_resultados = self.crear_textbox(
                    self.frame2,
                    font=self.fonts['label'],
                    fila=i*2+2,
                    columna=0,
                    alto=campo2['alto'],
                    ancho=campo2['ancho']
                )
                
                self.textbox[campo2['clave']] = self.textbox_resultados

        for i, campo3 in enumerate(campos3):
            
            if campo3['tipo'] == 'entry':
                # Creamos la variable de control para el entry y lo guardamos en el diccionario
                self.vars[campo3['clave']] = ctk.StringVar()
                
                # Solo asignamos la función a la traza si la clave está en el diccionario
                if campo3['clave'] in self.acciones:
                    self.vars[campo3['clave']].trace_add("write", self.acciones[campo3['clave']])
                
                # Se crea el entry y se almacena en el diccionario
                contador_p = self.crear_entry(
                    self.frame3,
                    font=self.fonts['label'],
                    fila=0,
                    columna=i+1,
                    ancho_widget=campo3['ancho'],
                    alto_widget=campo3['alto'],
                    textvariable=self.vars[campo3['clave']]
                )
                contador_p.grid(pady=20, padx = 0)
                self.entries[campo3['clave']] = contador_p
                
            elif campo3['tipo'] == 'boton':
                
                boton = self.crear_boton(self.frame3, 
                            font=self.fonts['boton'], 
                            texto= campo3['label'], 
                            color_fondo= campo3['color'], 
                            fila=0, 
                            columna= i+1, 
                            ancho=campo3['ancho'], 
                            alto= campo3['alto'], 
                            command = campo3['command'],
                            image=campo3['image'],
                            state='disabled' if campo3['clave'] in ['anterior', 'siguiente'] else 'normal'
                            )
                
                self.botones[campo3['clave']] = boton
        
    def eliminar_paciente(self):
        
        if not self.pacientes_encontrados:  # aseguramos que la lista no está vacía
            
            messagebox.showinfo("Pacientes Encontrados", "No hay pacientes cargados para eliminar.")
            
            return

        # Obtenemos el registro actual
        registro_actual = self.pacientes_encontrados[self.indice_actual]
        id_registro = registro_actual.get("id_registro")

        if not id_registro:  # valida None o vacío
            
            messagebox.showinfo("Registro para Eliminar", "No hay registros cargados para eliminar.")
            
            return
        
        respuesta = messagebox.askyesno("Registro para Eliminar", "Estas Seguro De Eliminar Este Paciente?.")
        
        if not respuesta:
            
            return

        # Consulta para eliminar el usuario
        sql_delete = "DELETE FROM registrospacientes WHERE id_registro = %s"
        self.db.cursor.execute(sql_delete, (id_registro,))
        self.db.conexion.commit()

        nombre_paciente = registro_actual.get("nombre_paciente", "Desconocido")
        
        messagebox.showinfo("Registro Eliminado", f"Paciente con nombre {nombre_paciente} fue eliminado de la base de datos.")


        # Eliminar en memoria
        self.pacientes_encontrados.pop(self.indice_actual)

        # Ajustar índice
        if self.indice_actual >= len(self.pacientes_encontrados):
            self.indice_actual = max(0, len(self.pacientes_encontrados) - 1)

        # Mostrar siguiente paciente o limpiar campos si no hay más
        if self.pacientes_encontrados:
            self.mostrar_paciente(self.indice_actual)
        else:
            # Limpiar todos los Entry
            for var in self.vars.values():
                var.set("")
            # Limpiar todos los Text
            for tb in self.textbox.values():
                tb.delete("0.0", "end")
            messagebox.showinfo("Paciente en lista", "No hay más pacientes.")
    
    def buscar_paciente(self, *args):
        
        self.pacientes_encontrados = []
    
        user_identification = self.entries['identificacion_paciente'].get().strip()
        if not user_identification:
            
            return

        sql_buscar_usuario = "SELECT * FROM registrospacientes WHERE identificacion_paciente LIKE %s"
        self.db.cursor.execute(sql_buscar_usuario, (user_identification,))
        
        columnas = self.db.cursor.column_names
        filas = self.db.cursor.fetchall()
        
        resultado = [dict(zip(columnas, fila)) for fila in filas]
        self.pacientes_encontrados.extend(resultado)
        
        # Inicializar índice y total solo si no existen o la lista estaba vacía
        if not hasattr(self, 'indice_actual') or not hasattr(self, 'total_pacientes') or len(self.pacientes_encontrados) == 0:
            self.indice_actual = 0

        self.total_pacientes = len(self.pacientes_encontrados)

        if self.total_pacientes == 0:
            
            return

        # Mostrar el paciente actual según el índice actual
        self.mostrar_paciente(self.indice_actual)
        
    # Función interna para mostrar un paciente según el índice
    def mostrar_paciente(self,indice):
        
        val = self.pacientes_encontrados[indice]

        # Obtener modalidad y rango de edad
        nombre_modalidad = self.obtener_nombre_modalidad(val['modalidad'])
        rango_edad = self.obtener_rango_edad(val['rango_edad'])
        estado = self.obtener_estado(val['estado'])
        sede = self.obtener_sede(val['sede'])
        retraso = self.obtener_causal_retraso(val['causal_retraso'])

        # Diccionario con valores a mostrar
        datos = {
            'nombre_paciente': val['nombre_paciente'],
            'identificacion_paciente': val['identificacion_paciente'],
            'edad': val['edad'],
            'rango_edad': rango_edad,
            'fecha_orden': val['fecha_orden'],
            'fecha_citacion': val['fecha_citacion'],
            'hc': val['hc'],
            'ubicacion': val['ubicacion'],
            'modalidad': nombre_modalidad,
            'estudios_ordenados_paciente': val['estudios_ordenados_paciente'],
            'diagnostico': val['diagnostico'],
            'ayuno': val['ayuno'],
            'diferido': val['diferido'],
            'alergia': val['alergia'],
            'tipo_alergia': val['tipo_alergia'],
            'aislamiento': val['aislamiento'],
            'tipo_aislamiento': val['tipo_aislamiento'],
            'autorizacion': val['autorizacion'],
            'anestesia': val['anestesia'],
            'estado': estado,
            'sede': sede,
            'hora_citacion': val['hora_citacion'],
            'hora_realizacion': val['hora_realizacion'],
            'causal_retraso': retraso,
            'comentarios_tecnologo': val['comentarios_tecnologo'],
            'comentar_radiologo': val['comentar_radiologo'],
            'comentarios_radiologo': val['comentarios_radiologo'],
        }

        # Rellenar widgets
        for clave, valor in datos.items():
            if clave in self.textbox:  # Si es un Textbox
                widget = self.textbox[clave]
                widget.delete("0.0", "end")
                widget.insert("0.0", str(valor) if valor else "")
            elif clave in self.vars:  # Si es un Entry
                self.vars[clave].set(str(valor) if valor else "")

        # Actualizar contador
        self.vars['contador'].set(f"{indice+1} / {self.total_pacientes}")

        # Habilitar o deshabilitar botones
        if self.total_pacientes > 1:
            self.botones['anterior'].configure(state='normal' if indice > 0 else 'disabled')
            self.botones['siguiente'].configure(state='normal' if indice < self.total_pacientes-1 else 'disabled')
        else:
            self.botones['anterior'].configure(state='disabled')
            self.botones['siguiente'].configure(state='disabled')

    def crear_label(self, parent, text, font, fila, columna, ancho= 1, alto= 1):
        
        label = ctk.CTkLabel(parent,
                            text=text,
                            font=font,
                            text_color= '#484a4b'
                            )
        label.grid(row= fila, column= columna, sticky='nsew', columnspan= ancho, rowspan= alto)
        
        return label
    
    def crear_entry(self,parent, font, fila, columna, ancho=1, alto=1, ancho_widget=150, alto_widget=26, textvariable =None):
        
        entry = ctk.CTkEntry(parent,
                            font = font,
                            text_color='black',
                            corner_radius=10,
                            width=ancho_widget,
                            height=alto_widget,
                            fg_color='lightgray',
                            textvariable=textvariable
                            )
        entry.grid(row=fila, column=columna, columnspan=ancho, rowspan=alto, padx=5, sticky='ew')
                
        return entry
        
    def crear_boton(self, parent, font, texto, color_fondo, fila, columna, ancho=70, alto=70, command=None, image = None, state = 'normal'):
        
        boton = ctk.CTkButton(
                                parent,
                                font=font,
                                text=texto,
                                fg_color=color_fondo,
                                text_color='white',
                                height=alto,
                                width= ancho,
                                command=command,
                                image=image,
                                corner_radius=10,
                                hover_color= "lightgreen"
                            )
        boton.grid(row=fila, column=columna, rowspan=alto, padx=15, pady= 15, sticky='nsew')
        return boton

    def crear_textbox(self, parent, font, fila, columna, alto, ancho):
        
        entry_textbox = ctk.CTkTextbox(parent,
                                    wrap=ctk.WORD,
                                    height=70,
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

    def crear_combobox (self, parent, font, fila, columna, textvariable, opciones):
        
        entry_combobox = ctk.CTkOptionMenu(parent,
                                        font= font,
                                        values= opciones,
                                        variable = textvariable,
                                        button_color= "lightgray",
                                        button_hover_color= "lightgreen"
                                        )
        
        entry_combobox.grid(row= fila, column= columna, padx=5, pady=5, sticky='ew')
        
        return entry_combobox

    def obtener_rango_edad(self, id_rango):
        
        """Obtiene los nombres de los cargos desde la base de datos."""

        sql = "SELECT rango FROM rangosedades WHERE id_rangoedad = %s"
        
        self.db.cursor.execute(sql, (id_rango, )) 
    
        resultado = self.db.cursor.fetchone()  # Lista de tuplas (id_cargo, nombre_cargo)

        # Retornar solo los nombres de los cargos para el combobox
        return resultado[0]

    def obtener_estado(self, id_estado):
        
        sql = "SELECT nombre_estado FROM estados WHERE id_estado = %s"
        
        self.db.cursor.execute(sql, (id_estado, ))
        
        resultado = self.db.cursor.fetchone()
        
        return resultado[0]
    
    def obtener_sede(self, id_sede):
        
        sql = "SELECT nombre_sede FROM sedes WHERE id_sede = %s"
        
        self.db.cursor.execute(sql, (id_sede, ))
        
        resultado = self.db.cursor.fetchone()
        
        return resultado[0]
    
    def obtener_causal_retraso(self, id_retraso):
        
        sql = "SELECT causal_retraso FROM retrasos WHERE id_retraso = %s"
        
        self.db.cursor.execute(sql, (id_retraso, ))
        
        resultado = self.db.cursor.fetchone()
        
        return resultado[0]

    def obtener_modalidades(self):
        
        """Obtiene los nombres de las modalidades desde la base de datos."""
        
        self.db.cursor.execute("SELECT id_modalidad, nombre_modalidad, abreviacion FROM modalidades")  
        modalidades = self.db.cursor.fetchall()  # Lista de tuplas (id, nombre, abreviación)
        # conexion.close()
        self.opciones = {f'{nombre_modalidad} ({abreviacion})': id_modalidad for id_modalidad, nombre_modalidad, abreviacion in modalidades}  # Lista con formato "id:nombre (abreviación)"

        return list(self.opciones.keys())
    
    def obtener_nombre_modalidad(self, id_modalidad):
        """Obtiene el nombre de la modalidad desde la base de datos usando su ID."""
        sql = "SELECT nombre_modalidad FROM modalidades WHERE id_modalidad = %s"
        self.db.cursor.execute(sql, (id_modalidad,))
        resultado = self.db.cursor.fetchone()
        return resultado[0] if resultado else None

    def obtener_id_modalidad(self, nombre_modalidad):
        """Obtiene el ID de modalidad basado en el nombre de la modalidad."""
        # La modalidad está en formato 'nombre (abreviación)', por lo que solo tomamos el nombre
        nombre_modalidad = nombre_modalidad.split(' (')[0]
        
        sql = "SELECT id_modalidad FROM modalidades WHERE nombre_modalidad = %s"
        self.db.cursor.execute(sql, (nombre_modalidad,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None

    def obtener_id_cargo(self, nombre_cargo):
        """Obtiene el ID de cargo basado en el nombre del cargo."""
        sql = "SELECT id_cargo FROM cargos WHERE nombre_cargo = %s"
        self.db.cursor.execute(sql, (nombre_cargo,))
        resultado = self.db.cursor.fetchone()
        
        # Retornar el ID si lo encuentra, de lo contrario None
        return resultado[0] if resultado else None

    def paciente_siguiente(self):
        if self.indice_actual + 1 < self.total_pacientes:
            self.indice_actual += 1
            self.mostrar_paciente(self.indice_actual)

    def paciente_anterior(self):
        if self.indice_actual - 1 >= 0:
            self.indice_actual -= 1
            self.mostrar_paciente(self.indice_actual)

    def limpiar_campos(self):
        
        """Limpia todos los campos de entrada."""
        self.vars['identificacion_paciente'].set("")
        self.vars['nombre_paciente'].set("")
        self.vars['edad'].set("")
        self.vars['rango_edad'].set("")
        self.vars['fecha_orden'].set("")
        self.vars['fecha_citacion'].set("")
        self.vars['hc'].set("")
        self.vars['ubicacion'].set("")
        self.vars['modalidad'].set("")
        self.textbox['estudios_ordenados_paciente'].delete("0.0", "end")
        self.textbox['diagnostico'].delete("0.0", "end")
        self.vars['ayuno'].set("")
        self.vars['diferido'].set("")
        self.vars['alergia'].set("")
        self.textbox['tipo_alergia'].delete("0.0", "end")
        self.vars['aislamiento'].set("")
        self.textbox['tipo_aislamiento'].delete("0.0", "end")
        self.vars['autorizacion'].set("")
        self.vars['anestesia'].set("")
        self.vars['estado'].set("")
        self.vars['sede'].set("")
        self.vars['hora_citacion'].set("")
        self.vars['hora_realizacion'].set("")
        self.vars['causal_retraso'].set("")
        self.textbox['comentarios_tecnologo'].delete("0.0", "end")
        self.vars['comentar_radiologo'].set("")
        self.textbox['comentarios_radiologo'].delete("0.0", "end")
    
    def salir(self):
            """Método personalizado para el botón Salir.
            Cierra la ventana de alergias y restablece la ventana de administración."""
            
            if self.db:
                
                self.db.cerrar_conexion()  # Llamamos al método de cerrar conexión
            
            self.root.destroy()  # Cierra la ventana de alergias
            
            if self.parent_window:
                
                self.parent_window.deiconify()
                self.parent_window.lift()
# a= IngresoUsuariosAdmon()
# g= a.obtener_ventana()
# g.mainloop()