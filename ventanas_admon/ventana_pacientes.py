import sys
import os

import customtkinter as ctk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexion_DB.conexionDB import Conexion_DB

class IngresoUsuariosAdmon():
    
    def __init__(self, parent_window=None):
        
        self.parent_window = parent_window  # Guardamos la referencia del padre
        
        ancho_ventana_nueva = 500
        alto_ventana_nueva = 600
        
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
            
            'title': ('verdana', 26,  'bold'),
            'label': ('verdana', 12,  'bold'),
            'boton': ('verdana', 18,  'bold')
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
        
        
        self.db = Conexion_DB()
        self.db.conectar()  
        
        # Diccionarios para guardar variables y widgets entry
        self.vars = {}
        self.entries = {}
        self.combobox = {}
        self.acciones = {
                        'identificacion': self.buscar_usuario,
                        'nombreusuario': self.actualizar_a_title,
                        'contrasena': self.actualizar_a_title,
                        'email': self.actualizar_a_title,
                        'telefono': self.actualizar_a_title,
                        'extension': self.actualizar_a_title
                    }
       
        self.usuario_id_seleccionado = None
        
        self.buscando = False
        
        #self.root.bind_all("<Return>",)
        
        self.ingreso_datos()
        
    def obtener_ventana(self):
        
        return self.root
        
    def ingreso_datos(self):
        
        campos = [
            
            {'label': 'Administrar\nUsuarios'}
        ]
        
        campos1 = [
            
            {'clave': 'identificacion','label': 'Identificación', 'placeholder': 'Ingrese la Identificación','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'nombreusuario', 'label': 'Nombre Usuario', 'placeholder': 'Ingrese el Nombre','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'contrasena','label': 'Contraseña', 'placeholder': 'Ingrese la Contraseña','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'email','label': 'Email', 'placeholder': 'Ingrese el Email','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'telefono','label': 'Telefono', 'placeholder': 'Ingrese el Telefono','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'extension','label': 'Extensión', 'placeholder': 'Ingrese el Extensión','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'modalidad','label': 'Modalidad', 'placeholder': 'Ingrese la Modalidad','ancho': 100, 'alto': 26, 'tipo':'combobox', 'textvariable':'', 'opciones': self.obtener_modalidades()},
            {'clave': 'cargo','label': 'Cargo', 'placeholder': 'Ingrese el Cargo','ancho': 100, 'alto': 26, 'tipo':'combobox', 'textvariable':'', 'opciones': self.obtener_cargos()},

        ]
        
        campos2 = [

            {'label': 'Eliminar', 'ancho': 100, 'alto': 30, 'color':'Lightblue', 'command': self.eliminar_usuario},
            {'label': 'Modificar', 'ancho': 100, 'alto': 30, 'color':'Lightblue', 'command': self.modificar_usuario},
            {'label': 'Salir', 'ancho': 100, 'alto': 30, 'color':'lightblue', 'command': self.salir},
        ]
        
        
        for i, campo in enumerate(campos):
        
            self.crear_label(self.frame, text=campo['label'], font=self.fonts['title'], fila=0, columna=0)
            
        for i, campo1 in enumerate(campos1):
            # Se coloca la etiqueta de cada campo
            self.crear_label(self.frame1, text=campo1['label'], font=self.fonts['label'], fila=i*2+1, columna=0)
            
            if campo1['tipo'] == 'entry':
                # Creamos la variable de control para el entry y lo guardamos en el diccionario
                self.vars[campo1['clave']] = ctk.StringVar()
                
                # Solo asignamos la función a la traza si la clave está en el diccionario
                if campo1['clave'] in self.acciones:
                    self.vars[campo1['clave']].trace_add("write", self.acciones[campo1['clave']])
                
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
            
            elif campo1['tipo'] == 'combobox':
                # Crear una variable de control
                self.vars[campo1['clave']] = ctk.StringVar()
                
                # Crear el combobox con opciones obtenidas desde la base de datos
                self.combobox[campo1['clave']] = self.crear_combobox(
                    self.frame1,
                    font=self.fonts['label'],
                    fila=i*2+2,
                    columna=0,
                    textvariable=self.vars[campo1['clave']],
                    opciones=campo1['opciones']
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
            
        self.sql_statement = """insert into usuarios (nombre_usuario, identificacion, contrasena, email, telefono, ext, modalidad, cargo) values (%s, %s, %s, %s, %s, %s, %s, %s)"""
    
    def actualizar_a_title(self, *args):
        """
        Callback que actualiza el contenido de la variable a formato Title.
        """
        # Actualizar el entry de 'nombre Usuario'
        texto_nombreusuario = self.vars['nombreusuario'].get()
        texto_title_nombreusuario = texto_nombreusuario.title()
        
        if texto_nombreusuario != texto_title_nombreusuario:
            self.vars['nombreusuario'].set(texto_title_nombreusuario)
        
    def eliminar_usuario(self):
        
        nombreusuario = self.entries['nombreusuario'].get().strip()
        identificacion = self.entries['identificacion'].get().strip()
        contrasena = self.entries['contrasena'].get().strip()
        email = self.entries['email'].get().strip()
        telefono = self.entries['telefono'].get().strip()
        extension = self.entries['extension'].get().strip()
        modalidad = self.combobox['modalidad'].get().strip()  # Esto devuelve nombre + abreviación
        cargo = self.combobox['cargo'].get().strip()  # Esto devuelve solo nombre del cargo

        if not nombreusuario or not identificacion or not contrasena or not email or not telefono or not extension or not modalidad or not cargo:
            print("Debe seleccionar un Usuario para eliminar.")
            return
        
        # Obtener los IDs de modalidad y cargo usando las funciones creadas
        id_modalidad = self.obtener_id_modalidad(modalidad)
        id_cargo = self.obtener_id_cargo(cargo)
        
        # Verificar si los IDs son válidos
        if not id_modalidad or not id_cargo:
            print("Modalidad o Cargo no válidos.")
            return
        
        # Consulta para eliminar el usuario usando los IDs de modalidad y cargo
        sql_delete = """
        DELETE FROM usuarios 
        WHERE nombre_usuario = %s 
        AND identificacion = %s 
        AND contrasena = %s 
        AND email = %s 
        AND telefono = %s 
        AND ext = %s 
        AND modalidad = %s 
        AND cargo = %s
        """
        
        # Ejecutar la consulta pasando los valores adecuados
        self.db.cursor.execute(sql_delete, (nombreusuario, identificacion, contrasena, email, telefono, extension, id_modalidad, id_cargo))
        self.db.conexion.commit()
        
        # Limpiar las variables después de eliminar el usuario
        self.vars['nombreusuario'].set("")
        self.vars['identificacion'].set("")
        self.vars['contrasena'].set("")
        self.vars['email'].set("")
        self.vars['telefono'].set("")
        self.vars['extension'].set("")
        self.vars['modalidad'].set("")
        self.vars['cargo'].set("")
    
    def buscar_usuario(self, *args):
        
        user_identification = self.vars['identificacion'].get().strip()

        if not user_identification:
            self.limpiar_campos()
            return  # Si no hay identificación, no buscar
        
        # Obtener el ID del usuario
        self.usuario_id_seleccionado = self.obtener_id_usuario_seleccionado(user_identification)
        
        if self.usuario_id_seleccionado is None:
            # print("No se encontró el usuario con esa identificación.")
            return

        sql_buscar_usuario = """
            SELECT nombre_usuario, identificacion, contrasena, email, telefono, ext, modalidad, cargo 
            FROM usuarios 
            WHERE identificacion LIKE %s
        """
        self.db.cursor.execute(sql_buscar_usuario, (f"{user_identification}",))
        resultado = self.db.cursor.fetchone()  # Obtener solo un resultado
        
        #Si hay resultados
        if resultado:
            # for resultado in resultado:
            nombre_usuario, identificacion, contrasena, email, telefono, ext, modalidad_id, cargo_id = resultado
            
            # Obtener el nombre de modalidad y cargo
            nombre_modalidad = self.obtener_nombre_modalidad(modalidad_id)
            nombre_cargo = self.obtener_nombre_cargo(cargo_id)

            # Llenar los campos correspondientes con los datos de la base de datos
            self.vars['nombreusuario'].set(nombre_usuario)
            self.vars['identificacion'].set(identificacion)
            self.vars['contrasena'].set(contrasena)
            self.vars['email'].set(email)
            self.vars['telefono'].set(telefono)
            self.vars['extension'].set(ext)
            self.vars['modalidad'].set(nombre_modalidad)
            self.vars['cargo'].set(nombre_cargo)
            
            # Hacer que el campo de contraseña sea de solo lectura
            if  'contrasena' in self.entries:
                
                self.entries['contrasena'].configure(state="readonly")
    
    def modificar_usuario(self):
        
        # # Activamos la bandera de que estamos modificando
        self.buscando = True

        nombreusuario = self.vars['nombreusuario']
        identificacion = self.vars['identificacion']
        contrasena = self.vars['contrasena']
        email = self.vars['email']
        telefono = self.vars['telefono']
        extension = self.vars['extension']
        modalidad_nombre = self.vars['modalidad'].get()
        cargo_nombre = self.vars['cargo'].get()
        
        if not self.usuario_id_seleccionado:
            # print("No se ha seleccionado un usuario para modificar.")
            return

        if not nombreusuario.get().strip() or not identificacion.get().strip() or not contrasena.get().strip() or not email.get().strip() or not telefono.get().strip() or not extension.get().strip() or not modalidad_nombre.strip() or not cargo_nombre.strip():
            print("Debe ingresar todos los datos.")
            return

        # Obtener los ID correspondientes de modalidad y cargo
        modalidad_id = self.obtener_id_modalidad(modalidad_nombre)
        cargo_id = self.obtener_id_cargo(cargo_nombre)

        if not modalidad_id or not cargo_id:
            # print("Modalidad o cargo no válidos.")
            return

        sql_modificar_usuario = """
            UPDATE usuarios 
            SET nombre_usuario = %s, identificacion = %s, contrasena = %s, email = %s, telefono = %s, ext = %s, modalidad = %s, cargo = %s 
            WHERE id_usuario = %s
        """

        self.db.cursor.execute(sql_modificar_usuario, (
            nombreusuario.get().strip(),
            identificacion.get().strip(),
            contrasena.get().strip(),
            email.get().strip(),
            telefono.get().strip(),
            extension.get().strip(),
            modalidad_id,  # Pasar el ID de modalidad
            cargo_id,      # Pasar el ID de cargo
            self.usuario_id_seleccionado  # Asegúrate de pasar el ID de usuario
        ))
        
        self.db.conexion.commit()

        # Limpiar campos y restablecer la bandera de búsqueda
        self.buscando = False
        
        # Limpiar campos y restablecer la bandera de búsqueda
        self.buscando = False
        self.usuario_id_seleccionado = None  # Resetear la selección

        # Limpiar los campos de entrada después de la modificación
        self.vars['nombreusuario'].set("")
        self.vars['identificacion'].set("")
        self.vars['contrasena'].set("")
        self.vars['email'].set("")
        self.vars['telefono'].set("")
        self.vars['extension'].set("")
        self.vars['modalidad'].set("")
        self.vars['cargo'].set("")
        
        self.usuario_id_seleccionado = None  # Resetear la selección

    def obtener_resultados_busqueda(self, identificacion):
        
        # Realiza la búsqueda en la base de datos y devuelve los resultados
        sql_buscar_identificacion = "SELECT nombre_usuario, identificacion, contrasena, email, telefono, ext, modalidad, cargo FROM usuarios WHERE nombre_usuario LIKE %s"
        self.db.cursor.execute(sql_buscar_identificacion, (f"{identificacion}%",))
        resultados = self.db.cursor.fetchall()
        
        # Crear un diccionario con los resultados, {id_alergia: nombre_alergia}
        usuario_dict = {}
        for resultado in resultados:
            usuario_dict[resultado[0]] = resultado[1]  # {id_alergia: nombre_alergia}
        
        return usuario_dict
    
    # def seleccionar_usuario(self, event):
        
        # Obtener la línea donde se hizo clic
        widget = event.widget
        index = widget.index("@%d,%d linestart" % (event.x, event.y))  # Obtiene el índice de la línea
        seleccion = widget.get(index, "%s lineend" % index).strip()  # Obtiene el contenido de la línea

        # Verificar que la línea no esté vacía
        if not seleccion:
            return

        # Extraer el ID (número antes de ":")
        id_usuario, datos = seleccion.split(":", 1)
        id_usuario = id_usuario.strip()
        nombre_usuario, identificacion, contrasena, email, telefono, ext, modalidad, cargo = datos.split(" - ")

        # Guardar ID en la variable para modificar/eliminar
        self.usuario_id_seleccionado = id_usuario

        # Colocar los datos en los Entry
        self.vars['nombreusuario'].set("")
        self.vars['identificacion'].set("")
        self.vars['contrasena'].set("")
        self.vars['email'].set("")
        self.vars['telefono'].set("")
        self.vars['extension'].set("")
        self.vars['modalidad'].set("")
        self.vars['cargo'].set("")
    
    def obtener_id_usuario_seleccionado(self, identificacion):
        
        sql_buscar_id = "SELECT id_usuario FROM usuarios WHERE identificacion = %s"
        self.db.cursor.execute(sql_buscar_id, (identificacion,))
        resultado = self.db.cursor.fetchone()  # Obtener solo un resultado
        
        if resultado:
            return resultado[0]
        else:
            # print(f"Usuario con identificación {identificacion} no encontrado.")
            return None

    def crear_label(self, parent, text, font, fila, columna, ancho= 1, alto= 1):
        
        label = ctk.CTkLabel(parent,
                            text=text,
                            font=font,
                            text_color= 'black'
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
                            placeholder_text_color= 'black',
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
                                text_color='black',
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
                                    border_color='black',
                                    border_width=2
                                    )
    
        # Usamos grid después de crear el widget
        entry_textbox.grid(row=fila, column=columna, pady=5, padx=5, sticky='nsew')
        
        return entry_textbox

    def crear_combobox (self, parent, font, fila, columna, textvariable, opciones):
        
        entry_combobox = ctk.CTkComboBox(parent,
                                        font= font,
                                        values= opciones,
                                        variable = textvariable,
                                        button_color= "lightgray",
                                        button_hover_color= "lightgreen"
                                        )
        
        entry_combobox.grid(row= fila, column= columna, padx=5, pady=5, sticky='ew')
        
        return entry_combobox

    def salir(self):
            """Método personalizado para el botón Salir.
            Cierra la ventana de alergias y restablece la ventana de administración."""
            
            if self.db:
                
                self.db.cerrar_conexion()  # Llamamos al método de cerrar conexión
            
            self.root.destroy()  # Cierra la ventana de alergias
            
            if self.parent_window:
                
                self.parent_window.deiconify()
                self.parent_window.lift()

    def obtener_cargos(self):
        
        """Obtiene los nombres de los cargos desde la base de datos."""
    
        self.db.cursor.execute("SELECT id_cargo, nombre_cargo FROM cargos") 
        cargos = self.db.cursor.fetchall()  # Lista de tuplas (id_cargo, nombre_cargo)

        # Diccionario para mapear nombres a IDs
        self.mapeo_cargos = {nombre: id_cargo for id_cargo, nombre in cargos}

        # Retornar solo los nombres de los cargos para el combobox
        return list(self.mapeo_cargos.keys())

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

    def obtener_nombre_cargo(self, id_cargo):
        """Obtiene el nombre del cargo desde la base de datos usando su ID."""
        sql = "SELECT nombre_cargo FROM cargos WHERE id_cargo = %s"
        self.db.cursor.execute(sql, (id_cargo,))
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

    def limpiar_campos(self):
        """Limpia todos los campos de entrada."""
        self.vars['nombreusuario'].set("")
        self.vars['identificacion'].set("")
        self.vars['contrasena'].set("")
        self.vars['email'].set("")
        self.vars['telefono'].set("")
        self.vars['extension'].set("")
        self.vars['modalidad'].set("")
        self.vars['cargo'].set("")

# a= IngresoUsuariosAdmon()
# g= a.obtener_ventana()
# g.mainloop()