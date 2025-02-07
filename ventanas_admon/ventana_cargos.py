import sys
import os

import customtkinter as ctk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexion_DB.conexionDB import Conexion_DB

class IngresoCargos():
    
    def __init__(self, parent_window=None):
        
        self.parent_window = parent_window  # Guardamos la referencia del padre
        
        ancho_ventana_nueva = 600
        alto_ventana_nueva = 350
        
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        
        self.root = ctk.CTkToplevel()
        
        self.root.protocol("WM_DELETE_WINDOW", lambda:None)
        
        x = (self.root.winfo_screenwidth() // 2) - (ancho_ventana_nueva // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto_ventana_nueva // 2)
        
        self.root.geometry(f'{ancho_ventana_nueva}x{alto_ventana_nueva}+{x}+{y}')
        
        self.root.title('Ingreso Cargos')
        
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
        
        # Crear la variable de control para el Entry
        self.cargo_var = ctk.StringVar()
        # Asociar el trace para que cada vez que cambie se actualice en formato title
        self.cargo_var.trace_add("write", self.actualizar_a_title)
        self.cargo_var.trace_add("write", self.buscar_cargo)
        
        self.cargo_id_seleccionado = None
        
        self.ingreso_datos()
        
    def obtener_ventana(self):
        
        return self.root
        
    def ingreso_datos(self):
        
        campos = [
            
            {'label': 'Ingreso\nDatos'}
        ]
        
        campos1 = [
            
            {'label': 'Cargo', 'placeholder': 'Ingrese El Cargo','ancho': 100, 'alto': 26, 'tipo':'entry'},
            {'label': 'Resultado de la Busqueda', 'placeholder': 'Busqueda','ancho': 100, 'alto': 26, 'tipo':'textbox'}

        ]
        
        campos2 = [
            
            {'label': 'Ingresar', 'ancho': 100, 'alto': 30, 'color':'Lightblue', 'command': self.insertar_cargo},
            {'label': 'Eliminar', 'ancho': 100, 'alto': 30, 'color':'Lightblue', 'command': self.eliminar_cargo},
            {'label': 'Modificar', 'ancho': 100, 'alto': 30, 'color':'Lightblue', 'command': self.modificar_cargo},
            {'label': 'Salir', 'ancho': 100, 'alto': 30, 'color':'red', 'command': self.salir},
        ]
        
        
        for i, campo in enumerate(campos):
        
            self.crear_label(self.frame, text=campo['label'], font=self.fonts['title'], fila=0, columna=0)
            
        for i, campo1 in enumerate(campos1):
    
            self.crear_label(self.frame1, text=campo1['label'], font=self.fonts['label'], fila=i*2+1, columna=0)
        
            self.entry_cargo = self.crear_entry(self.frame1, 
                             font=self.fonts['label'], 
                             fila=i*2+2, 
                             columna= 0, 
                             ancho_widget=campo1['ancho'], 
                             alto_widget= campo1['alto'], 
                             placeholder =campo1['placeholder'],
                             textvariable = self.cargo_var
                             )
            
            if campo1['tipo'] == 'textbox':
            
                self.textbox_resultados = self.crear_textbox(self.frame1,
                                                             font=self.fonts['label'],
                                                             fila=i*2+2,
                                                             columna=0,
                                                             alto= campo1['alto'],
                                                             ancho=campo1['ancho'],
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
            
        self.sql_statement = """insert into cargos (nombre_cargo) values (%s)"""
    
    def actualizar_a_title(self, *args):
        """
        Callback que actualiza el contenido de la variable a formato Title.
        """
        
        texto_actual = self.cargo_var.get()
        
        texto_title = texto_actual.title()  # Convierte a title case
        
        if texto_actual != texto_title:
            
            # Actualizamos la variable, lo que actualizará el Entry
            self.cargo_var.set(texto_title)
    
    def insertar_cargo(self):
        
        # Obtener el valor del entry
        cargo = self.entry_cargo.get().strip()
        
        if not cargo:
            print("Debe ingresar un Cargo.")
            return
        
        # 🔹 Consultar si el cargo ya existe en la base de datos
        consulta_existencia = "SELECT COUNT(*) FROM cargos WHERE nombre_cargo = %s"
        
        self.db.cursor.execute(consulta_existencia, (cargo,))
        
        resultado = self.db.cursor.fetchone()

        if resultado[0] > 0:
            print(f"El cargo '{cargo}' ya existe en la base de datos.")
            return  # No inserta si ya existe

        # try:
        sql_insert = "INSERT INTO cargos (nombre_cargo) VALUES (%s)"
        self.db.cursor.execute(sql_insert, (cargo,)) 
        self.db.conexion.commit()  # Confirmar cambios en la base de datos
        self.cargo_var.set("")
        #     print(f"Alergia '{alergia}' insertada correctamente.")
        # except Exception as e:
        #     print("Error al insertar en la base de datos:", e)
        
    def eliminar_cargo(self):
        
        cargo = self.entry_cargo.get()
        
        if not cargo:
            
            return
        
        sql_delete = "DELETE FROM cargos WHERE nombre_cargo = %s"
        self.db.cursor.execute(sql_delete, (cargo,))
        self.db.conexion.commit()  # Confirmar cambios en la base de datos
        self.cargo_var.set("")
    
    def buscar_cargo(self, *args):
        
        cargo = self.cargo_var.get().strip()
        
        # Limpiar el textbox si no hay entrada
        if not cargo:
            self.textbox_resultados.configure(state="normal")
            self.textbox_resultados.delete("1.0", "end")
            self.textbox_resultados.configure(state="disabled")
            return
        
        # Buscar en la base de datos solo lo que empieza con la entrada del usuario
        sql_buscar_cargo = "SELECT nombre_cargo FROM cargos WHERE nombre_cargo LIKE %s"
        self.db.cursor.execute(sql_buscar_cargo, (f"%{cargo}%",))
        resultados = self.db.cursor.fetchall()
        
        # Limpiar y actualizar el textbox con los resultados
        self.textbox_resultados.configure(state="normal")
        self.textbox_resultados.delete("1.0", "end")

        if resultados:
            for resultado in resultados:
                self.textbox_resultados.insert("end", resultado[0] + "\n")
        else:
            self.textbox_resultados.insert("end", "No hay coincidencias")
        
        self.textbox_resultados.configure(state="disabled")

        # Hacer que el textbox permita clics para seleccionar un valor
        self.textbox_resultados.bind("<ButtonRelease-1>", self.seleccionar_cargo)
    
    def modificar_cargo(self):
        
        # Obtener el valor del Entry
        cargo_nuevo = self.cargo_var.get().strip()
        
        # Verificar si el valor está vacío
        if not cargo_nuevo:
            # Si está vacío, muestra un mensaje o realiza alguna acción
            return
        
        # Usar el ID de la alergia seleccionada previamente
        cargo_id = self.cargo_id_seleccionado if hasattr(self, 'cargo_id_seleccionado') else None

        if not cargo_id:
            print("No se ha seleccionado un cargo para modificar.")
            return
        
        # Realizar la actualización en la base de datos
        sql_modificar_alergia = "UPDATE cargos SET nombre_cargo = %s WHERE id_cargo = %s"
        self.db.cursor.execute(sql_modificar_alergia, (cargo_nuevo, cargo_id))
        self.db.conexion.commit()

        # Limpiar el Textbox y actualizarlo con el nuevo valor
        self.textbox_resultados.configure(state="normal")
        self.textbox_resultados.delete("1.0", "end")
        self.cargo_var.set("")
        # self.textbox_resultados.insert("end", f"Alergia modificada: {alergia_nueva}\n")
        self.textbox_resultados.configure(state="disabled")


        # Hacer que el textbox permita clics para seleccionar un valor
        self.textbox_resultados.bind("<ButtonRelease-1>", self.seleccionar_cargo)
    
    def obtener_resultados_busqueda(self, cargo):
        
        # Realiza la búsqueda en la base de datos y devuelve los resultados
        sql_buscar_cargo = "SELECT id_cargo, nombre_cargo FROM cargos WHERE nombre_cargo LIKE %s"
        self.db.cursor.execute(sql_buscar_cargo, (f"%{cargo}%",))
        resultados = self.db.cursor.fetchall()
        
        # Crear un diccionario con los resultados, {id_alergia: nombre_alergia}
        cargo_dict = {}
        
        for resultado in resultados:
            
            cargo_dict[resultado[0]] = resultado[1]  # {id_alergia: nombre_alergia}
        
        return cargo_dict
    
    def seleccionar_cargo(self, event):
        
        seleccion = self.textbox_resultados.get("insert linestart", "insert lineend").strip()
        if seleccion and seleccion != "No hay coincidencias":
            self.cargo_var.set(seleccion)
            
            # almacenar el ID de la alergia seleccionada
            cargo_id = self.obtener_id_cargo_seleccionado(seleccion)
            if cargo_id:
                self.cargo_id_seleccionado = cargo_id  # Almacenar el ID para futuras modificaciones
    
    def obtener_id_cargo_seleccionado(self, cargo_nombre):
        
        sql_buscar_id = "SELECT id_cargo FROM cargos WHERE nombre_cargo = %s"
        self.db.cursor.execute(sql_buscar_id, (cargo_nombre,))
        resultado = self.db.cursor.fetchone()

        if resultado:
            return resultado[0]  # Devuelve el ID de la alergia
        else:
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
        boton.grid(row=fila, column=columna, rowspan=alto, padx=15, pady= 15, sticky='ew')
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
            Cierra la ventana de cargos y restablece la ventana de administración."""
            
            if self.db:
                
                self.db.cerrar_conexion()  # Llamamos al método de cerrar conexión
            
            self.root.destroy()  # Cierra la ventana de cargos
            
            if self.parent_window:
                
                self.parent_window.deiconify()
                self.parent_window.lift()

# a= IngresoCargos()
# g= a.obtener_ventana()
# g.mainloop()