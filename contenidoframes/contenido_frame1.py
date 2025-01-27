import sys
import os

# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
import customtkinter as ctk
# from tkinter import ttk
# from tkinter.ttk import Combobox

class ContenidoFrame1():
       
    def __init__(self, frame):

        self.frame = frame

        self.frame.grid_rowconfigure(list(range(19)), weight=1)

        self.frame.grid_columnconfigure(list(range(4)), weight=1)


        self.fonts = {

            "title": ("Verdana", 30, 'bold'),

            "title_frame": ("Verdana", 24, 'bold'),

            "label": ("Verdana", 12, 'bold')

        }
            
    def contenidotituloppal(self):
        
        titulo = tk.Label(self.frame, text='Ingreso Del Paciente', font=self.fonts['title'], bg='white', width=200)
        titulo.grid(row=0, column=0, columnspan=3, sticky="nsew") 
    
    def contenidosframe1(self):
        
        titulo_frame = tk.Label(self.frame, text='Datos Del Paciente', font=self.fonts['title_frame'], bg='white', width=10)
        titulo_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        lab_identificacion = tk.Label(self.frame, text='Identificación Del Paciente', font=self.fonts['label'], bg='white', width=30)
        lab_identificacion.grid(row=1, column=0, pady= 10, sticky='nsew')
        
        entry_identificacion_paciente = ctk.CTkEntry(self.frame, 
                                                     font=self.fonts['label'],
                                                     width= 293,
                                                     height= 26,
                                                     fg_color='lightblue',
                                                     corner_radius=10,
                                                     text_color='black')
        entry_identificacion_paciente.grid(row=2, column=0, padx= 15, pady= 10, sticky='nsew')
        
        lab_nombre = tk.Label(self.frame, text='Nombre Del Paciente', font=self.fonts['label'], bg='white', width=20)
        lab_nombre.grid(row=3, column=0, pady= 10, sticky='nsew')
        
        entry_nombre_paciente = ctk.CTkEntry(self.frame, 
                                             font=self.fonts['label'],
                                             width= 600,
                                             height= 26,
                                             fg_color='lightblue',
                                             corner_radius=10,
                                             text_color='black')
        entry_nombre_paciente.grid(row=4, column=0, padx= 15, pady= 10, columnspan=2, sticky='nsew')
        
        lab_edad = tk.Label(self.frame, text='Edad', font=self.fonts['label'], bg='white', width=20)
        lab_edad.grid(row=5, column=0, pady= 10, sticky='nsew')
        
        entry_edad_paciente = ctk.CTkEntry(self.frame, 
                                           font=self.fonts['label'],
                                           width= 293,
                                           height= 26,
                                           fg_color='lightblue',
                                           corner_radius=10,
                                           text_color='black')
        entry_edad_paciente.grid(row=6, column=0, padx= 15, pady= 10, sticky='nsew')
        
        lab_rango_edad = tk.Label(self.frame, text='Rango Edad', font=self.fonts['label'], bg='white', width=20)
        lab_rango_edad.grid(row=5, column=1, pady= 10, sticky='nsew')
        
        entry_rango_edad_paciente = ctk.CTkComboBox(self.frame,
                                                    font=self.fonts['label'],
                                                    state="normal",
                                                    width= 285,
                                                    height= 26,
                                                    fg_color='lightblue',
                                                    corner_radius=10,
                                                    text_color='black',
                                                    values=['Selecione un Rango'],
                                                    button_color="lightblue",
                                                    button_hover_color='lightgreen',
                                                    border_color='black')
        entry_rango_edad_paciente.grid(row=6, column=1, sticky='nsew', padx= 15, pady= 10)
        
        lab_historia_clin = tk.Label(self.frame, text='Historia Clinica', font=self.fonts['label'], bg='white', width=20)
        lab_historia_clin.grid(row=7, column=0, pady= 10, sticky='nsew')
        
        entry_historia_clin_paciente = ctk.CTkEntry(self.frame, 
                                                    font=self.fonts['label'],
                                                    width= 293,
                                                    height= 26,
                                                    fg_color='lightblue',
                                                    corner_radius=10,
                                                    text_color='black')
        entry_historia_clin_paciente.grid(row=8, column=0, padx= 15, pady= 10, sticky='nsew')
        
        lab_ubicacion = tk.Label(self.frame, text='Ubicación Paciente', font=self.fonts['label'], bg='white', width=20)
        lab_ubicacion.grid(row=9, column=0, pady= 5, sticky='nsew')
        
        entry_ubicacion_paciente = ctk.CTkEntry(self.frame, 
                                                font=self.fonts['label'],
                                                width= 293,
                                                height= 26,
                                                fg_color='lightblue',
                                                corner_radius=10,
                                                text_color='black')
        entry_ubicacion_paciente.grid(row=10, column=0, padx= 15, pady= 10, sticky='nsew')
        
        lab_sede = tk.Label(self.frame, text='Sede', font=self.fonts['label'], bg='white', width=20)
        lab_sede.grid(row=11, column=0, pady= 8, sticky='nsew')
        
        entry_sede_paciente = ctk.CTkComboBox(self.frame,
                                              font=self.fonts['label'],
                                              state="normal",
                                              width= 285,
                                              height= 26,
                                              fg_color='lightblue',
                                              corner_radius=10,
                                              text_color='black',
                                              values=['Selecione una Sede'],
                                              button_color="lightblue",
                                              button_hover_color='lightgreen',
                                              border_color='black')
        entry_sede_paciente.grid(row=12, column=0, padx= 15, pady= 10, sticky='nsew')
        
        lab_alergias_paciente = tk.Label(self.frame, text='Alergias', font=self.fonts['label'], bg='white', width=20)
        lab_alergias_paciente.grid(row=13, column=0, pady= 10, sticky='nsew')
        
        var_alergias = tk.IntVar(value=2)  # Valor predeterminado es 0

        # Botón de opción 1
        radio_alergias1 = tk.Radiobutton(self.frame,
                                         text="Sí",
                                         variable = var_alergias,
                                         value=1,
                                         font=self.fonts['label'],
                                         bg= 'white')
        radio_alergias1.grid(row=14, column=0, padx= 15, pady= 10, sticky='w')

        # Botón de opción 2
        radio_alergias2 = tk.Radiobutton(self.frame,
                                         text="No",
                                         variable = var_alergias,
                                         value=2,
                                         font=self.fonts['label'],
                                         bg= 'white')
        radio_alergias2.grid(row=14, column=0, padx=80, sticky='w')
        
        lab_tipo_alergia = tk.Label(self.frame, text='Tipo De Alergia', font=self.fonts['label'], bg='white', width=20)
        lab_tipo_alergia.grid(row=13, column= 1, pady= 10, sticky='nsew')
        
        entry_tipo_alergia_paciente = ctk.CTkComboBox(self.frame,
                                                      font=self.fonts['label'],
                                                      state="normal",
                                                      width= 285,
                                                      height= 26,
                                                      fg_color='lightblue',
                                                      corner_radius=10,
                                                      text_color='black',
                                                      values=['Selecione un Tipo de Alergia'],
                                                      button_color="lightblue",
                                                      button_hover_color='lightgreen',
                                                      border_color='black')
        entry_tipo_alergia_paciente.grid(row=14, column= 1, padx= 15, pady= 10, sticky='nsew')
        
        lab_aislamiento_paciente = tk.Label(self.frame, text='Aislamiento', font=self.fonts['label'], bg='white', width=20)
        lab_aislamiento_paciente.grid(row=15, column=0, pady= 10, sticky='nsew')
        
        var_aislamiento = tk.IntVar(value=2)  # Valor predeterminado es 0

        # Botón de opción 1
        radio_aislamiento1 = tk.Radiobutton(self.frame,
                                            text="Sí",
                                            variable = var_aislamiento,
                                            value=1,
                                            font=self.fonts['label'],
                                            bg= 'white')
        radio_aislamiento1.grid(row=16, column=0, padx= 15, pady= 10, sticky='w')

        # Botón de opción 2
        radio_aislamiento2 = tk.Radiobutton(self.frame,
                                            text="No",
                                            variable = var_aislamiento,
                                            value=2,
                                            font=self.fonts['label'],
                                            bg= 'white')
        radio_aislamiento2.grid(row=16, column=0, padx=80, sticky='w')
        
        lab_tipo_aislamiento = tk.Label(self.frame, text='Tipo De Aislamiento', font=self.fonts['label'], bg='white', width=20)
        lab_tipo_aislamiento.grid(row=15, column= 1, pady= 10, sticky='nsew')
        
        entry_tipo_aislamiento_paciente = ctk.CTkComboBox(self.frame,
                                                          font=self.fonts['label'],
                                                          state="normal",
                                                          width= 285,
                                                          height= 26,
                                                          fg_color='lightblue',
                                                          corner_radius=10,
                                                          text_color='black',
                                                          values=['Selecione un Tipo de Aislamiento'],
                                                          button_color="lightblue",
                                                          button_hover_color='lightgreen',
                                                          border_color='black')
        entry_tipo_aislamiento_paciente.grid(row=16, column= 1, padx= 15, pady= 10, sticky='nsew')
        
        lab_estado = tk.Label(self.frame, text='Estado', font=self.fonts['label'], bg='white', width=20)
        lab_estado.grid(row=17, column= 0, pady=8, sticky='nsew')
        
        entry_estado_paciente = ctk.CTkComboBox(self.frame,
                                                font=self.fonts['label'],
                                                state="normal",
                                                width= 285,
                                                height= 26,
                                                fg_color='lightblue',
                                                corner_radius=10,
                                                text_color='black',
                                                values=['Selecione un Estado'],
                                                button_color="lightblue",
                                                button_hover_color='lightgreen',
                                                border_color='black')
        entry_estado_paciente.grid(row=18, column= 0, padx= 15, pady= 10, sticky='nsew')
        