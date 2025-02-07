import sys
import os

import customtkinter as ctk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexion_DB.conexionDB import Conexion_DB

class IngresoModalidades():
    
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
        
        self.root.title('Ingreso Estudios')
        
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
       
        self.modalidad_id_seleccionada = None
        
        self.ingreso_datos()
        
    def obtener_ventana(self):
        
        return self.root
        
    def ingreso_datos(self):
        
        campos = [
            
            {'label': 'Ingreso\nDatos'}
        ]
        
        campos1 = [
            
            {'clave': 'modalidad', 'label': 'Modalidad', 'placeholder': 'Ingrese la Modalidad','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'abreviacion','label': 'Abreviación', 'placeholder': 'Ingrese la Abreviación','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'clave': 'busqueda','label': 'Resultado de la Busqueda', 'placeholder': 'Busqueda','ancho': 100, 'alto': 26, 'tipo':'textbox'}

        ]
        
        campos2 = [
            
            {'label': 'Ingresar', 'ancho': 100, 'alto': 30, 'color':'Lightblue', 'command': self.insertar_modalidad},
            {'label': 'Eliminar', 'ancho': 100, 'alto': 30, 'color':'Lightblue', 'command': self.eliminar_modalidad},
            {'label': 'Modificar', 'ancho': 100, 'alto': 30, 'color':'Lightblue', 'command': self.modificar_modalidad},
            {'label': 'Salir', 'ancho': 100, 'alto': 30, 'color':'red', 'command': self.salir},
        ]
        
        
        for i, campo in enumerate(campos):
        
            self.crear_label(self.frame, text=campo['label'], font=self.fonts['title'], fila=0, columna=0)
            
        for i, campo1 in enumerate(campos1):
            # Se coloca la etiqueta de cada campo
            self.crear_label(self.frame1, text=campo1['label'], font=self.fonts['label'], fila=i*2+1, columna=0)
            
            if campo1['tipo'] == 'entry':
                # Creamos la variable de control para el entry y lo guardamos en el diccionario
                self.vars[campo1['clave']] = ctk.StringVar()
                # Si deseas, puedes agregar trace para modificar el texto a Title (por ejemplo en el entry "estudio")
                if campo1['clave'] == 'modalidad':
                    self.vars[campo1['clave']].trace_add("write", self.actualizar_a_title)
                    self.vars[campo1['clave']].trace_add("write", self.buscar_modalidad)
                    # Además puedes agregar otro trace para buscar mientras se escribe:
                else:
                    
                    self.vars[campo1['clave']].trace_add("write", self.actualizar_a_title)
                    self.vars[campo1['clave']].trace_add("write", self.buscar_modalidad)
                
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
            
        self.sql_statement = """insert into modalidades (nombre_modalidad, abreviacion) values (%s, %s)"""
    
    def actualizar_a_title(self, *args):
        """
        Callback que actualiza el contenido de la variable a formato Title.
        """
        
        # Actualizar el entry de 'modalidad'
        texto_modalidad = self.vars['modalidad'].get()
        texto_title_modalidad = texto_modalidad.title()
        
        if texto_modalidad != texto_title_modalidad:
            self.vars['modalidad'].set(texto_title_modalidad)
            
        texto_abreviacion = self.vars['abreviacion'].get()
        texto_title_abreviacion = texto_abreviacion.upper()
        
        if texto_abreviacion != texto_title_abreviacion:
            self.vars['abreviacion'].set(texto_title_abreviacion)
    
    def insertar_modalidad(self):
        
        # Obtener los valores de los entries usando las claves del diccionario
        
        modalidad = self.entries['modalidad'].get().strip()
        abreviacion = self.entries['abreviacion'].get().strip()
        
        if not modalidad or not abreviacion:
            print("Debe ingresar tanto la Modalidad como la Abreviación.")
            return
        
        # Consultar si el modalidad ya existe en la base de datos (ajusta la consulta según corresponda)
        consulta_existencia = "SELECT COUNT(*) FROM modalidades WHERE nombre_modalidad  = %s AND abreviacion = %s"
        self.db.cursor.execute(consulta_existencia, (modalidad, abreviacion))
        resultado = self.db.cursor.fetchone()  # Usamos fetchone para un solo resultado

        if resultado[0] > 0:
            print(f"El Estudio '{modalidad}' ya existe en la base de datos.")
            return  # No inserta si ya existe

        # try:
        sql_insert = "INSERT INTO modalidades (nombre_modalidad, abreviacion) VALUES (%s, %s)"
        self.db.cursor.execute(sql_insert, (modalidad, abreviacion))
        self.db.conexion.commit()
        # Limpiar los entries luego de la inserción
        self.vars['modalidad'].set("")
        self.vars['abreviacion'].set("")
        #     print(f"Alergia '{alergia}' insertada correctamente.")
        # except Exception as e:
        #     print("Error al insertar en la base de datos:", e)
        
    def eliminar_modalidad(self):
        
        modalidad = self.entries['modalidad'].get().strip()
        abreviacion = self.entries['abreviacion'].get().strip()
        
        if not modalidad or not abreviacion:
            print("Debe seleccionar una Modalidad y su abreviación para eliminar.")
            return
        
        sql_delete = "DELETE FROM modalidades WHERE nombre_modalidad = %s AND abreviacion = %s"
        self.db.cursor.execute(sql_delete, (modalidad, abreviacion))
        self.db.conexion.commit()
        self.vars['modalidad'].set("")
        self.vars['abreviacion'].set("")
    
    def buscar_modalidad(self, *args):
        
        modalidad = self.vars['modalidad'].get().strip()

        # Limpiar el textbox de resultados
        self.textbox_resultados.configure(state="normal")
        self.textbox_resultados.delete("1.0", "end")

        if not modalidad:
            self.textbox_resultados.configure(state="disabled")
            return

        sql_buscar_modalidad = "SELECT id_modalidad, nombre_modalidad, abreviacion FROM modalidades WHERE nombre_modalidad LIKE %s"
        self.db.cursor.execute(sql_buscar_modalidad, (f"%{modalidad}%",))
        resultados = self.db.cursor.fetchall()

        if resultados:
            for resultado in resultados:
                id_modalidad, nombre, abreviacion = resultado
                self.textbox_resultados.insert("end", f"{id_modalidad}: {nombre} - {abreviacion}\n")
        else:
            self.textbox_resultados.insert("end", "No hay coincidencias")

        self.textbox_resultados.configure(state="disabled")
        self.textbox_resultados.bind("<ButtonRelease-1>", self.seleccionar_modalidad)
    
    def modificar_modalidad(self):
        
        modalidad_nueva = self.entries['modalidad'].get().strip()
        abreviacion_nueva = self.entries['abreviacion'].get().strip()

        if not modalidad_nueva or not abreviacion_nueva:
            print("Debe ingresar los datos para modificar.")
            return

        # Verificar si se ha seleccionado una modalidad
        if not self.modalidad_id_seleccionada:
            print("No se ha seleccionado una modalidad para modificar.")
            return

        sql_modificar_modalidad = "UPDATE modalidades SET nombre_modalidad = %s, abreviacion = %s WHERE id_modalidad = %s"
        self.db.cursor.execute(sql_modificar_modalidad, (modalidad_nueva, abreviacion_nueva, self.modalidad_id_seleccionada))
        self.db.conexion.commit()

        # Limpiar los campos
        self.textbox_resultados.configure(state="normal")
        self.textbox_resultados.delete("1.0", "end")
        self.vars['modalidad'].set("")
        self.vars['abreviacion'].set("")
        self.modalidad_id_seleccionada = None  # Resetear la selección
        self.textbox_resultados.configure(state="disabled")
    
    def obtener_resultados_busqueda(self, modalidad):
        
        # Realiza la búsqueda en la base de datos y devuelve los resultados
        sql_buscar_modalidad = "SELECT id_modalidad, nombre_modalidad, abreviacion FROM modalidades WHERE nombre_modalidad LIKE %s"
        self.db.cursor.execute(sql_buscar_modalidad, (f"%{modalidad}%",))
        resultados = self.db.cursor.fetchall()
        
        # Crear un diccionario con los resultados, {id_alergia: nombre_alergia}
        modalidad_dict = {}
        for resultado in resultados:
            modalidad_dict[resultado[0]] = resultado[1]  # {id_alergia: nombre_alergia}
        
        return modalidad_dict
    
    def seleccionar_modalidad(self, event):
        
        # Obtener la línea donde se hizo clic
        widget = event.widget
        index = widget.index("@%d,%d linestart" % (event.x, event.y))  # Obtiene el índice de la línea
        seleccion = widget.get(index, "%s lineend" % index).strip()  # Obtiene el contenido de la línea

        # Verificar que la línea no esté vacía
        if not seleccion:
            return

        # Extraer el ID (número antes de ":")
        id_modalidad, datos = seleccion.split(":", 1)
        id_modalidad = id_modalidad.strip()
        nombre_modalidad, abreviacion = datos.split(" - ")

        # Guardar ID en la variable para modificar/eliminar
        self.modalidad_id_seleccionada = id_modalidad

        # Colocar los datos en los Entry
        self.vars['modalidad'].set(nombre_modalidad.strip())
        self.vars['abreviacion'].set(abreviacion.strip())
    
    def obtener_id_modalidad_seleccionada(self, modalidad_nombre):
        
        sql_buscar_id = "SELECT id_modalidad FROM modalidades WHERE nombre_modalidad = %s"
        self.db.cursor.execute(sql_buscar_id, (modalidad_nombre,))
        resultado = self.db.cursor.fetchone()  # Obtener solo un resultado
        return resultado[0] if resultado else None

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
                             fg_color='lightblue',
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
                                text_color='black',
                                height=alto,
                                width= ancho,
                                command=command,
                                corner_radius=10
                            )
        boton.grid(row=fila, column=columna, rowspan=alto, padx=15, pady= 15, sticky='nsew')
        return boton

    def crear_textbox(self, parent, font, fila, columna, alto, ancho):
        
        entry_textbox = ctk.CTkTextbox(parent,
                                    wrap=ctk.WORD,
                                    height=100,
                                    width=560,
                                    fg_color="lightblue",
                                    corner_radius=10,
                                    font=font,
                                    text_color='black',
                                    border_color='black',
                                    border_width=2
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

# a= IngresoModalidades()
# g= a.obtener_ventana()
# g.mainloop()