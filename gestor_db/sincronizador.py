import re
import mysql.connector
        
class SincronizadorDB:
    """
    Sincroniza la base de datos: crea tablas nuevas y agrega columnas faltantes
    sin perder datos existentes.
    """

    def __init__(self, cursor, conexion, sql_aux, sql_principal):
        self.cursor = cursor
        self.conexion = conexion
        self.sql_aux = sql_aux
        self.sql_principal = sql_principal

    def tabla_existe(self, nombre_tabla):
        self.cursor.execute(f"SHOW TABLES LIKE '{nombre_tabla}';")
        existe = self.cursor.fetchone() is not None
        return existe

    def columnas_existentes(self, nombre_tabla):
        self.cursor.execute(f"SHOW COLUMNS FROM {nombre_tabla};")
        columnas = [col[0] for col in self.cursor.fetchall()]
        return columnas
    
    def agregar_columnas_faltantes(self, nombre_tabla, sql_create):
        columnas_actuales = self.columnas_existentes(nombre_tabla)
        definicion = sql_create[sql_create.find("(")+1 : sql_create.rfind(")")]
        
        for linea in definicion.splitlines():
            linea = linea.strip().rstrip(",")
            if not linea:
                continue
            
            # Ignorar constraints generales
            if any(k in linea.upper() for k in ["PRIMARY", "FOREIGN", "CONSTRAINT", "UNIQUE", "KEY", "CHECK"]):
                continue
            
            # Limpiar referencias de foreign keys inline
            if "REFERENCES" in linea.upper():
                # Tomamos solo la parte antes de REFERENCES
                linea = linea[:linea.upper().find("REFERENCES")].strip()
            if "ON DELETE" in linea.upper():
                linea = linea[:linea.upper().find("ON DELETE")].strip()
            if "ON UPDATE" in linea.upper():
                linea = linea[:linea.upper().find("ON UPDATE")].strip()

            # Extraer nombre y tipo de columna
            parts = linea.split()
            if not parts:
                continue
            col_name = parts[0].strip("`")
            col_tipo = " ".join(parts[1:])
            
            # Agregar solo si no existe
            if col_name not in columnas_actuales:
                try:
                    self.cursor.execute(f"ALTER TABLE {nombre_tabla} ADD COLUMN {col_name} {col_tipo}")
                except Exception as e:
                    print(f"{e}")
    
    def sincronizar(self):

        # Tablas auxiliares
        for sql in self.sql_aux:
            nombre_tabla = sql.split("CREATE TABLE IF NOT EXISTS")[1].split("(")[0].strip()
            if not self.tabla_existe(nombre_tabla):
                self.cursor.execute(sql)
            else:
                self.agregar_columnas_faltantes(nombre_tabla, sql)

        # Tablas principales
        for nombre_tabla, sql in self.sql_principal.items():
            if not self.tabla_existe(nombre_tabla):
                self.cursor.execute(sql)
            else:
                self.agregar_columnas_faltantes(nombre_tabla, sql)

        self.conexion.commit()