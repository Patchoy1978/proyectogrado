import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import customtkinter as ctk

from tkinter import messagebox

def abrir_ventana_conn_exito():

    messagebox.showinfo("Éxito", "Conexión a la Base de Datos Exitosa")

def abrir_ventana_conn_fallida():

    messagebox.showerror("Error", "No se ha podido conectar a la Base de Datos")
    
def archivo_creado():

    messagebox.showinfo("Creado", "Archivo creado con éxito")
    
def mostrar_inicio():

    messagebox.showinfo("Bienvenido", "Como administrador que eres\nlo primero que debes hacer es\nconfigurar los datos necesarios para\nconectarse a la Base de Datos")
    
def archivo_fallido():

    messagebox.showerror("Creación Fallida", "El Archivo no se ha creado correctamente")

def email_incorrecto():

    messagebox.showwarning("Email Incorrecto", "El Email no es correcto")

def email_no_esta():

    messagebox.showwarning("Email No Esta ", "El Email no esta Registrado")

def email_formato():

    messagebox.showwarning("Email Formato", "El Email no tiene el Formato Correcto")

def email_validado():

    messagebox.showwarning("Email Validado", "El Email ha sido Validado con éxito")

def email_no_validado():

    messagebox.showwarning("Email No Validado", "El Email no ha sido Validado con éxito")

def contrasena_incorrecta():

    messagebox.showwarning("Contraseña Incorrecta", "La Contraseña no es Correcta")

def contrasena_coincide():

    messagebox.showwarning("Contraseña Coincide", "Las Contraseñas no coinciden")

def contrasena_guardada():

    messagebox.showwarning("Contraseña Coincide", "Las Contraseña\nSe Ha Guardado con Exito")

def contrasena_no_guardada():

    messagebox.showwarning("Contraseña Coincide", "Las Contraseña\nNo Se Ha Podido guardar")

def contrasena_formato():

    messagebox.showwarning("Contraseña Formato", "La contraseña debe tener entre 8 y 20 caracteres,\nincluir una mayúscula, una minúscula,\nun número y un carácter especial.")
    
def usuario_ingresado():

    messagebox.showinfo("Usuario Agregado", "El Usuario se ha agregado con éxito")
    
def usuario_no_ingresado():

    messagebox.showerror("Usuario Agregado", "El Usuario no se ha agregado")

def campos_requeridos():

    messagebox.showwarning("Campos Requeridos", "Todos Los Campos Deben Estar Diligenciados")

def telefono_extension():

    messagebox.showwarning("Telefono y Extensión", "El teléfono y la extensión deben contener solo números.")

def modalidad_cargo():

    messagebox.showwarning("Modalidad y Cargo", "Modalidad o cargo seleccionados no válidos.")

def usuario_existe():

    messagebox.showwarning("Modalidad y Cargo", "El usuario ya existe en la base de datos.")

def cerrar_conexion():

    messagebox.showwarning("Cerrar Conexión", "La conexion con la base de datos\nse ha cerrado con éxito.")

def confirmacion_codigo():

    messagebox.showinfo("Código Enviado", "Con el Codigo\nYa Estas Autorizado para ingresar tu nueva contraseña")
    
def validacion_cuenta():

    messagebox.showerror("Error", "No se pudo validar tu cuenta para actualizar la contraseña")

def validacion_completa():

    messagebox.showerror("Error", "Primero valida tu correo.")

def codigo_no_esta():

    messagebox.showwarning("Código No Esta ", "El email Ingresado\nNo Tiene codigo de Autorización")

def ingresar_aislamiento():
    
    messagebox.showwarning("Ingreso Aislamiento","Debe ingresar un aislamiento.")
    
def aislamiento_existe():
    
    messagebox.showinfo("Aislamiento Existente","El aislamiento ya existe en la base de datos.")
    
def debes_hacer_primero():
    
    messagebox.showinfo("Primer Paso","Si no hay pacientes para visualizar\n\nDebes Ingresar Pacientes y Despues\n\nDebes seleccionar una sede\n\npara visualizar los pacientes,\n\nSi quieres observar por un día en especifico\n\ntambién selecciona una fecha.")
    
def admon_debes_hacer_primero():
    
    messagebox.showinfo("Primer Paso","Debes Ingresar Una Modalidad\n\nDebes Ingresar Un Cargo,\n\nDebes Salir De Esta Ventana\n\nDebes Registrarte Para Poder Ingresar\n\nComo el Administrador.")
    
def modificacion_realizada():
    
    messagebox.showinfo("Confirmación Modificación","Los Datos Se Han Actualizado Correctamente")

def si_la_db_esta_vacia():
    
    messagebox.showinfo("Aviso", f"No hay pacientes en base de datos para mostrar.")
    
def paciente_cancelado():
    
    return messagebox.askyesno("Cancelación de Paciente", "¿Deseas cancelar este paciente?")
    
def paciente_diferido():
    
    return messagebox.askyesno("Diferir el Paciente", "¿Deseas diferir este paciente?")

def paciente_realizado():
    
    return messagebox.askyesno("Realizado el Paciente", "¿Este paciente ya esta Realizado?")

def paciente_comentado():
    
    return messagebox.askyesno("Comentado el Paciente", "¿Deseas Comentar Este Paciente?")

def datos_ingresados():
    
    messagebox.showinfo("Datos Ingresados", "Los Datos Se Han Ingresado Exitosamente")

def edad_incorrecta(parent=None):
    
    messagebox.showwarning("Datos Ingresados", "La edad debe ser un número", parent=parent)
    
def tamano_edad_incorrecta(parent=None):
    
    messagebox.showwarning("Datos Ingresados", "La edad no puede tener más de 3 dígitos", parent=parent)
    
def edad_fuera_rango(parent=None):
    
    messagebox.showwarning("Datos Ingresados", "La edad esta por fuera del rango", parent=parent)
