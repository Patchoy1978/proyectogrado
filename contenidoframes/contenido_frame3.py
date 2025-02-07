import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import customtkinter as ctk
import tkinter as tk

class ContenidoFrame3 ():
    
    
    def __init__(self, frame):
        
        self.frame = frame
        self.frame.grid_rowconfigure(list(range(14)), weight=1)
        self.frame.grid_columnconfigure(list(range(4)), weight=1)
        
        # Tamaños base para cada tipo de widget
        self.fonts = {

            "title": ("Verdana", 30, 'bold'),

            "title_frame": ("Verdana", 24, 'bold'),

            "label": ("Verdana", 12, 'bold')

        }

    def contenidosframe3 (self):
        
        from abrirventanas.abrir import abrir_ventana_visualizar_datos_ppal, cerrar_ppal
        
        titulo = tk.Label(self.frame, text='Realización Del Estudio', bg='white', font=self.fonts['title_frame'], width=30)
        titulo.grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        lab_hora_citacion = tk.Label(self.frame, font=self.fonts['label'], bg= 'white', text='Hora De La Cita')
        lab_hora_citacion.grid(row = 1, column = 0, sticky='w', pady=8)
        
        horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 5)]  # Intervalos de 5 minutos
        entry_combobox_hora_citacion = ctk.CTkComboBox(self.frame,
                                                    font=self.fonts['label'],
                                                    state="normal",
                                                    width= 285,
                                                    height= 26,
                                                    fg_color='lightblue',
                                                    corner_radius=10,
                                                    text_color='black',
                                                    button_color="lightblue",
                                                    button_hover_color='lightgreen',
                                                    border_color='black',
                                                    values=['Seleccione Una Hora'] + horas)
        entry_combobox_hora_citacion.grid(row=2, column=0, pady=8, padx=15, sticky='nsew')
        
        lab_hora_realizacion = tk.Label(self.frame, font=self.fonts['label'], bg= 'white', text='Hora Realización Estudio')
        lab_hora_realizacion.grid(row = 3, column = 0, sticky='w', pady=8)
        
        # horas1 = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 5)]  # Intervalos de 5 minutos
        entry_combobox_hora_realizacion = ctk.CTkComboBox(self.frame,
                                                    font=self.fonts['label'],
                                                    state="normal",
                                                    width= 285,
                                                    height= 26,
                                                    fg_color='lightblue',
                                                    corner_radius=10,
                                                    text_color='black',
                                                    button_color="lightblue",
                                                    button_hover_color='lightgreen',
                                                    border_color='black',
                                                    values=['Seleccione Una Hora'] + horas)
        entry_combobox_hora_realizacion.grid(row=4, column=0, pady=8, padx=15, sticky='nsew')
        
        lab_causal_retraso = tk.Label(self.frame, font=self.fonts['label'], bg= 'white', text='Causal Del Retraso')
        lab_causal_retraso.grid(row = 5, column = 0, sticky = 'w', pady=8)
        
        entry_list_caus_retraso = ctk.CTkComboBox(self.frame,
                                                font=self.fonts['label'],
                                                state="normal",
                                                width= 610,
                                                height= 26,
                                                fg_color='lightblue',
                                                corner_radius=10,
                                                text_color='black',
                                                values=['Selecione una Causal de Retraso'],
                                                button_color="lightblue",
                                                button_hover_color='lightgreen',
                                                border_color='black')
        entry_list_caus_retraso.grid(row=6, column=0, pady=8, padx=15, sticky='nsew')
        
        lab_coment_tecnologo = tk.Label(self.frame, text='Comentarios Tecnólogo', font=self.fonts['label'], bg='white')
        lab_coment_tecnologo.grid(row=7, column=0, pady = 8, sticky='w')
        
        entry_texto_coment_tecnologo = ctk.CTkTextbox(self.frame,
                                                    wrap=tk.WORD,
                                                    height=100,
                                                    width=610,
                                                    fg_color="lightblue",
                                                    corner_radius= 10,
                                                    font=self.fonts['label'],
                                                    text_color='black',
                                                    border_color='black',
                                                    border_width=2)
        entry_texto_coment_tecnologo.grid(row=8, column=0, pady=10, padx= 15, sticky='nsew')
        
        lab_coment_al_radiologo = tk.Label(self.frame, font=self.fonts['label'], bg= 'white', text='Comentar Estudio Con Radiólogo')
        lab_coment_al_radiologo.grid(row = 9, column = 0, sticky = 'w', pady=8)
        
        var_coment_al_rad = tk.IntVar(value=2)  # Valor predeterminado es No

        # Botón de opción 1
        radio_coment_radiologo1 = tk.Radiobutton(self.frame, text="Sí", variable = var_coment_al_rad, value=1, font=self.fonts['label'], bg= 'white')
        radio_coment_radiologo1.grid(row=10, column=0, padx=12, sticky='w')

        # Botón de opción 2
        radio_coment_radiologo2 = tk.Radiobutton(self.frame, text="No", variable = var_coment_al_rad, value=2, font=self.fonts['label'], bg= 'white')
        radio_coment_radiologo2.grid(row=10, column=0, padx=80, sticky='w')
        
        # frame_coment_radiologo = tk.Frame(self.frame, bg= 'white')
        # frame_coment_radiologo.grid(row=9, column=0, pady=10, sticky='nsew')
        
        lab_coment_radiologo = tk.Label(self.frame, text='Comentarios Radiólogo', font=self.fonts['label'], bg='white')
        lab_coment_radiologo.grid(row=11, column=0, pady = 8, sticky='w')
        
        entry_texto_coment_radiologo = ctk.CTkTextbox(self.frame,
                                                    wrap=tk.WORD,
                                                    height=100,
                                                    width=610,
                                                    fg_color="lightblue",
                                                    corner_radius= 10,
                                                    font=self.fonts['label'],
                                                    text_color='black',
                                                    border_color='black',
                                                    border_width=2)
        entry_texto_coment_radiologo.configure(state = 'disable')
        entry_texto_coment_radiologo.grid(row=12, column=0, pady=10, padx= 15, sticky='nsew')
        
        frame_buttons = ctk.CTkFrame(self.frame,
                                     width=610,
                                     height=230,
                                     fg_color='white')
        frame_buttons.grid(row= 13, column=0, sticky='nsew', padx= 15, pady= 8)
        
        # Configura las columnas dentro de frame_buttons para que se expandan
        frame_buttons.grid_columnconfigure(list(range(3)), weight=1)

        frame_buttons.grid_rowconfigure(0, weight=1)
        
        btn_nuevo = ctk.CTkButton(frame_buttons,
                                  text='Nuevo Ingreso',
                                  text_color='black',
                                  font=self.fonts['label'],
                                  width=20,
                                  height=50,
                                  corner_radius=20,
                                  fg_color='lightblue',
                                  hover_color = 'lightgreen',
                                  anchor='center')
        
        btn_nuevo.grid(row= 0, column= 0, padx= 8, pady= 70, sticky='nsew')
        
        btn_limpiar = ctk.CTkButton(frame_buttons,
                                  text='Limpiar Pantalla',
                                  text_color='black',
                                  font=self.fonts['label'],
                                  width=20,
                                  height=50,
                                  corner_radius=20,
                                  fg_color='lightblue',
                                  hover_color = 'lightgreen',
                                  anchor='center')
        
        btn_limpiar.grid(row= 0, column= 1, padx= 8, pady= 70, sticky='nsew')
        
        btn_atras = ctk.CTkButton(frame_buttons,
                                  text='Regresar',
                                  text_color='black',
                                  font=self.fonts['label'],
                                  width=20,
                                  height=50,
                                  corner_radius=20,
                                  fg_color='lightblue',
                                  hover_color = 'lightgreen',
                                  anchor='center',
                                  command= lambda:(abrir_ventana_visualizar_datos_ppal(), cerrar_ppal(self.frame.winfo_toplevel()))
                                  )
        
        btn_atras.grid(row= 0, column= 2, padx= 8, pady= 70, sticky='nsew')
