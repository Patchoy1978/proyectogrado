import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import tkinter as tk
import customtkinter as ctk
# from tkinter import ttk
# from tkinter.ttk import Combobox
from tkcalendar import DateEntry

class ContenidoModificarFrame2 ():
    
    def __init__(self, frame):
        
        self.frame = frame
        
        self.frame.grid_rowconfigure(list(range(17)), weight=1)

        self.frame.grid_columnconfigure(list(range(3)), weight=1)


        self.fonts = {

            "title": ("Verdana", 30, 'bold'),

            "title_frame": ("Verdana", 24, 'bold'),

            "label": ("Verdana", 12, 'bold')

        }
        
    def contenidosframe2modificar (self):
        
        titulo = tk.Label(self.frame, text='Datos Del Estudio', font= self.fonts['title_frame'], bg='white')
        titulo.grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        lab_fecha_orden = tk.Label(self.frame, font= self.fonts['label'], bg= 'white', text='Fecha De La Orden', width=20)
        lab_fecha_orden.grid(row= 1, column= 0, sticky= 'nsew', pady= 8)
        
        entry_fecha_orden = DateEntry(self.frame,
                                    width=20,
                                    background='lightblue',
                                    foreground='white',
                                    borderwidth=2,
                                    date_pattern= 'dd/MM/yyyy',
                                    font=('verdana', 12, 'bold'),
                                    locale = 'es')
        entry_fecha_orden.grid(row=2, column=0, pady=8, padx=15, sticky='nsew')
        
        lab_fecha_citacion = tk.Label(self.frame, font= self.fonts['label'], bg= 'white', text='Fecha De La Cita', width=20)
        lab_fecha_citacion.grid(row= 3, column= 0, sticky= 'nsew', pady= 8)
        
        entry_fecha_cita = DateEntry(self.frame,
                                   width=20,
                                   background='lightblue',
                                   foreground='white',
                                   borderwidth=2,
                                   date_pattern= 'dd/MM/yyyy',
                                   font= self.fonts['label'],
                                   locale = 'es')
        entry_fecha_cita.grid(row=4, column=0, pady=8, padx=15, sticky='nsew')
        
        lab_modalidad = tk.Label(self.frame, text='Modalidad', font= self.fonts['label'], bg='white', width=20)
        lab_modalidad.grid(row=5, column=0, pady = 8, sticky='nsew')
        
        entry_modalidad = ctk.CTkComboBox(self.frame,
                                        font= self.fonts['label'],
                                        state="normal",
                                        width= 275,
                                        height= 26,
                                        fg_color='lightblue',
                                        corner_radius=10,
                                        text_color='black',
                                        values=['Selecione una Modalidad'],
                                        button_color="lightblue",
                                        button_hover_color='lightgreen',
                                        border_color='black')
        entry_modalidad.grid(row=6, column=0, sticky='nsew', padx= 15, pady= 8)
        
        lab_estud_ordenados = tk.Label(self.frame, text='Estudios Ordenados', font= self.fonts['label'], bg='white', width=20)
        lab_estud_ordenados.grid(row=7, column=0, pady = 8, sticky='nsew')
        
        entry_texto_est_ord = ctk.CTkTextbox(self.frame,
                                    wrap=tk.WORD,
                                    height=100,
                                    width=560,
                                    fg_color="lightblue",
                                    corner_radius= 10,
                                    font= self.fonts['label'],
                                    text_color='black',
                                    border_color='black',
                                    border_width=2)
        entry_texto_est_ord.configure(state="disable")
        entry_texto_est_ord.grid(row=8, column=0, columnspan= 2, pady=8, padx= 15, sticky='nsew')
        
        entry_list_estud_ordenados = ctk.CTkTextbox(self.frame,
                                                    wrap=tk.WORD,
                                                    height=150,
                                                    width=560,
                                                    fg_color="lightblue",
                                                    corner_radius= 10,
                                                    font= self.fonts['label'],
                                                    text_color='black',
                                                    border_color='black',
                                                    border_width=2)
        entry_list_estud_ordenados.configure(state= 'disable')
        entry_list_estud_ordenados.grid(row=9, column=0, columnspan= 2, pady=8, padx= 15, sticky='nsew')
        
        entry_busqueda = ctk.CTkEntry(self.frame,
                                    font= self.fonts['label'],
                                      width= 275,
                                      height= 20,
                                      fg_color='lightblue',
                                      corner_radius=10,
                                      text_color='black')
        entry_busqueda.grid (row=10, column=0, pady=10, padx= 15, sticky='nsew')
        
        lab_ayuno_paciente = tk.Label(self.frame, text='Ayuno', font= self.fonts['label'], bg='white', width=20)
        lab_ayuno_paciente.grid(row=11, column=0, pady = 8, sticky='nsew')
        
        var_ayuno = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        radio_ayuno1 = tk.Radiobutton(self.frame,
                                      text="Sí",
                                      variable = var_ayuno,
                                      value=1,
                                      font= self.fonts['label'],
                                      bg= 'white')
        radio_ayuno1.grid(row=12, column=0, padx=12, sticky='w')

        # Botón de opción 2
        radio_ayuno2 = tk.Radiobutton(self.frame,
                                      text="No",
                                      variable = var_ayuno,
                                      value=2,
                                      font= self.fonts['label'],
                                      bg= 'white')
        radio_ayuno2.grid(row=12, column=0, padx=80, sticky='w')
        
        lab_diferido_paciente = tk.Label(self.frame, text='Diferido', font= self.fonts['label'], bg='white', width=20)
        lab_diferido_paciente.grid(row=11, column=1, pady = 8, sticky='nsew')
        
        var_diferido = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        radio_diferido1 = tk.Radiobutton(self.frame,
                                         text="Sí",
                                         variable = var_diferido,
                                         value=1,
                                         font= self.fonts['label'],
                                         bg= 'white')
        radio_diferido1.grid(row=12, column=1, padx=12, sticky='w')

        # Botón de opción 2
        radio_diferido2 = tk.Radiobutton(self.frame,
                                         text="No",
                                         variable = var_diferido,
                                         value=2,
                                         font= self.fonts['label'],
                                         bg= 'white')
        radio_diferido2.grid(row=12, column=1, padx=80, sticky='w')
        
        lab_autorizacion_paciente = tk.Label(self.frame, text='Autorización', font= self.fonts['label'], bg='white', width=20)
        lab_autorizacion_paciente.grid(row=13, column=0, pady = 8, sticky='nsew')
        
        var_autorizacion = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        radio_autorizacion1 = tk.Radiobutton(self.frame,
                                             text="Sí",
                                             variable = var_autorizacion,
                                             value=1,
                                             font= self.fonts['label'],
                                             bg= 'white')
        radio_autorizacion1.grid(row=14, column=0, padx=12, sticky='w')

        # Botón de opción 2
        radio_autorizacion2 = tk.Radiobutton(self.frame,
                                             text="No",
                                             variable = var_autorizacion,
                                             value=2,
                                             font= self.fonts['label'],
                                             bg= 'white')
        radio_autorizacion2.grid(row=14, column=0, padx=80, sticky='w')
        
        lab_anestesia_paciente = tk.Label(self.frame, text='Anestesia', font= self.fonts['label'], bg='white', width=20)
        lab_anestesia_paciente.grid(row=13, column=1, pady = 8, sticky='nsew')
        
        var_anestesia = tk.IntVar(value=0)  # Valor predeterminado es 0

        # Botón de opción 1
        radio_anestesia1 = tk.Radiobutton(self.frame,
                                          text="Sí",
                                          variable = var_anestesia,
                                          value=1,
                                          font= self.fonts['label'],
                                          bg= 'white')
        radio_anestesia1.grid(row=14, column=1, padx=12, sticky='w')

        # Botón de opción 2
        radio_anestesia2 = tk.Radiobutton(self.frame,
                                          text="No",
                                          variable = var_anestesia,
                                          value=2,
                                          font= self.fonts['label'],
                                          bg= 'white')
        radio_anestesia2.grid(row=14, column=1, padx=80, sticky='w')
        
        lab_diagnostico = tk.Label(self.frame, text='Diagnóstico', font= self.fonts['label'], bg='white', width=20)
        lab_diagnostico.grid(row=15, column=0, pady = 8, sticky='nsew')
        
        entry_texto_diagnostico = ctk.CTkTextbox(self.frame,
                                        wrap=tk.WORD,
                                        height=100,
                                        width=560,
                                        fg_color="lightblue",
                                        corner_radius= 10,
                                        font= self.fonts['label'],
                                        text_color='black',
                                        border_color='black',
                                        border_width=2)
        entry_texto_diagnostico.grid(row=16, column=0, columnspan= 2, pady=10, padx= 15, sticky='nsew')
        
        # scroll_entry_diagnostico = tk.Scrollbar(frame_diagnostico, command=entry_texto_diagnostico.yview)
        # entry_texto_diagnostico.configure(yscrollcommand=scroll_entry_diagnostico.set)
        # scroll_entry_diagnostico.grid(row=1, column=1, sticky='ns', pady=3)

