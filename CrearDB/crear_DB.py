import mysql.connector


class ConexionDB():
    
    def __init__(self, host, user, password, port):

        self.conexion = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            port = port
        )
        
        self.cursor = self.conexion.cursor()
        
        # ------------------------
        # Tablas auxiliares
        # ------------------------
        sql_aux = [
            # Tabla de alergias
            """CREATE TABLE IF NOT EXISTS alergias (
                id_alergia INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
                nombre_alergia VARCHAR(30) NOT NULL
            )""",
            # Tabla de aislamientos
            """CREATE TABLE IF NOT EXISTS aislamientos (
                id_aislamiento INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
                nombre_aislamiento VARCHAR(30) NOT NULL
            )""",
            # Tabla de rangos de edad
            """CREATE TABLE IF NOT EXISTS rangosedades (
                id_rangoedad INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
                rango VARCHAR(12) NOT NULL
            )""",
            # Lista de estudios
            """CREATE TABLE IF NOT EXISTS listaEstudios (
                id_estudio INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
                nombre_estudio VARCHAR(255) NOT NULL,
                abreviacion VARCHAR(3) NOT NULL
            )""",
            # Modalidades
            """CREATE TABLE IF NOT EXISTS modalidades (
                id_modalidad INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
                nombre_modalidad VARCHAR(255) NOT NULL,
                abreviacion VARCHAR(3) NOT NULL
            )""",
            # Estados
            """CREATE TABLE IF NOT EXISTS estados (
                id_estado INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
                nombre_estado VARCHAR(12) NOT NULL
            )""",
            # Sedes
            """CREATE TABLE IF NOT EXISTS sedes (
                id_sede INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
                nombre_sede VARCHAR(30) NOT NULL
            )""",
            # Retrasos
            """CREATE TABLE IF NOT EXISTS retrasos (
                id_retraso INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
                causal_retraso VARCHAR(150) NOT NULL
            )""",
            # Cargos
            """CREATE TABLE IF NOT EXISTS cargos (
                id_cargo INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
                nombre_cargo VARCHAR(60) NOT NULL
            )""",
            # Usuarios
            """CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nombre_usuario VARCHAR(60) NOT NULL,
                identificacion BIGINT NOT NULL UNIQUE,
                contrasena VARCHAR(100) NOT NULL,
                email VARCHAR(60) NOT NULL UNIQUE,
                telefono VARCHAR(15) NOT NULL,
                ext INTEGER,
                modalidad INTEGER NOT NULL,
                cargo INTEGER NOT NULL,
                codigo INTEGER,
                CONSTRAINT usuarios_modalidad FOREIGN KEY (modalidad) REFERENCES modalidades(id_modalidad) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT usuarios_cargo FOREIGN KEY (cargo) REFERENCES cargos(id_cargo) ON DELETE CASCADE ON UPDATE CASCADE
            )"""
        ]

        # ------------------------
        # Tablas principales
        # ------------------------
        tablas_principales = [
            "registrosPacientes",
            "registrosPacientesDiferidos",
            "registrosPacientesRealizados",
            "registrosPacientesCancelados",
            "registrosPacientesModificados"
        ]

        sql_principal = {}
        for tabla in tablas_principales:
            sql_principal[tabla] = f"""
            CREATE TABLE IF NOT EXISTS {tabla} (
                id_registro INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY UNIQUE,
                nombre_paciente VARCHAR(60) NOT NULL,
                identificacion_paciente BIGINT NOT NULL,
                edad TINYINT NOT NULL,
                rango_edad INTEGER NOT NULL,
                fecha_orden DATE NOT NULL,
                fecha_citacion DATE NOT NULL,
                hc VARCHAR(12) NOT NULL,
                ubicacion VARCHAR(30) NOT NULL,
                modalidad INTEGER NOT NULL,
                estudios_ordenados_paciente TEXT NOT NULL,
                diagnostico TEXT NOT NULL,
                ayuno VARCHAR(2) NOT NULL,
                diferido VARCHAR(2) NOT NULL,
                alergia VARCHAR(2) NOT NULL,
                tipo_alergia TEXT NOT NULL,
                aislamiento VARCHAR(2) NOT NULL,
                tipo_aislamiento TEXT NOT NULL,
                autorizacion VARCHAR(2) NOT NULL,
                anestesia VARCHAR(2) NOT NULL,
                estado INTEGER NOT NULL,
                sede INTEGER NOT NULL,
                hora_citacion TIME NOT NULL,
                hora_realizacion TIME NOT NULL,
                causal_retraso INTEGER NOT NULL,
                comentarios_tecnologo TEXT NOT NULL,
                comentar_radiologo VARCHAR(2) NOT NULL,
                comentarios_radiologo TEXT NULL,
                usuario INTEGER NOT NULL,
                bloqueado_por VARCHAR(60) DEFAULT 'Libre',
                CONSTRAINT fk_{tabla}_rangoedad FOREIGN KEY (rango_edad)
                REFERENCES rangosedades(id_rangoedad)
                ON DELETE CASCADE ON UPDATE CASCADE
            )
            """
            
        # Relaciones automáticas
        relaciones = ["retrasos", "sedes", "modalidades", "estados", "usuarios", "aislamientos", "listaEstudios", "alergias"]
        
        # ------------------------
        # Crear base de datos
        # ------------------------
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS entregaturno")
        self.cursor.execute("USE entregaturno")

        # ------------------------
        # Crear tablas auxiliares
        # ------------------------
        for sql in sql_aux:
            self.cursor.execute(sql)
            self.conexion.commit()

        # ------------------------
        # Crear tablas principales y relaciones
        # ------------------------
        for tabla, sql in sql_principal.items():
            # Crear tabla principal
            self.cursor.execute(sql)
            self.conexion.commit()

            # Crear tablas de relación automáticamente
            for rel in relaciones:
                tabla_rel = f"{tabla}_{rel}"

                if rel == "retrasos":
                    fk_rel = f"fk_{tabla}_rel"
                    fk_id = "id_retraso"
                    ref_tabla = "retrasos"
                elif rel == "sedes":
                    fk_rel = f"fk_{tabla}_sed"
                    fk_id = "id_sede"
                    ref_tabla = "sedes"
                elif rel == "modalidades":
                    fk_rel = f"fk_{tabla}_mod"
                    fk_id = "id_modalidad"
                    ref_tabla = "modalidades"
                elif rel == "estados":
                    fk_rel = f"fk_{tabla}_estado"
                    fk_id = "id_estado"
                    ref_tabla = "estados"
                elif rel == "usuarios":
                    fk_rel = f"fk_{tabla}_usu"
                    fk_id = "id_usuario"
                    ref_tabla = "usuarios"
                elif rel == "aislamientos":
                    fk_rel = f"fk_{tabla}_ais"
                    fk_id = "id_aislamiento"
                    ref_tabla = "aislamientos"
                elif rel == "listaEstudios":
                    fk_rel = f"fk_{tabla}_est"
                    fk_id = "id_estudio"
                    ref_tabla = "listaEstudios"
                elif rel == "alergias":
                    fk_rel = f"fk_{tabla}_ale"
                    fk_id = "id_alergia"
                    ref_tabla = "alergias"

                sql_rel = f"""
                CREATE TABLE IF NOT EXISTS {tabla_rel} (
                    id_registro INTEGER NOT NULL,
                    {fk_id} INTEGER NOT NULL,
                    PRIMARY KEY (id_registro, {fk_id}),
                    CONSTRAINT fk_{tabla_rel} FOREIGN KEY (id_registro) REFERENCES {tabla}(id_registro) ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT {fk_rel} FOREIGN KEY ({fk_id}) REFERENCES {ref_tabla}({fk_id}) ON DELETE CASCADE ON UPDATE CASCADE
                )
                """
                self.cursor.execute(sql_rel)
                self.conexion.commit()

        # Cerrar conexión
        self.conexion.close()