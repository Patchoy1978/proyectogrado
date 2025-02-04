import mysql.connector


class ConexionDB():
    
    def __init__(self, host, user, password, port):

        self.conexion = mysql.connector.connect(
            
            host = host,
            user = user,
            password = password,
            port = port
            # database = 'entregaturno'
        )

        # print(self.conexion)
        
        self.cursor = self.conexion.cursor()
        
        sql_statements = ["""
        
        CREATE TABLE if NOT EXISTS alergias (
            id_alergia INTEGER auto_increment not null primary key,
            nombre_alergia varchar(30) not null
        )
        """,
        """
        CREATE TABLE if NOT EXISTS aislamientos (
            id_aislamiento INTEGER auto_increment not null primary key,
            nombre_aislamiento varchar(30) not null
        )
        """,
        """
        CREATE TABLE if NOT EXISTS rangosEdades (
            id_rangoedad INTEGER auto_increment not null primary key,
            rango varchar(12) not null
        )
        """,
        """
        CREATE TABLE if NOT EXISTS estudiosOrdenados (
            id_estudio INTEGER auto_increment not null primary key,
            nombre_estudio varchar(30) not null,
            abreviacion varchar(3) not null
        )
        """,
        """
        CREATE TABLE if NOT EXISTS modalidades (
            id_modalidad INTEGER auto_increment not null primary key,
            nombre_modalidad varchar(30) not null,
            abreviacion varchar(3) not null
        )
        """,
        """
        CREATE TABLE if NOT EXISTS estados (
            id_estado INTEGER auto_increment not null primary key,
            nombre_estado varchar(12) not null
        )
        """,
        """
        CREATE TABLE if NOT EXISTS sedes (
            id_sede INTEGER auto_increment not null primary key,
            nombre_sede varchar(30) not null
        )
        """,
        """
        CREATE TABLE if NOT EXISTS retrasos (
            id_retraso INTEGER auto_increment not null primary key,
            causal_retraso varchar(150) not null
        )
        """,
        """
        CREATE TABLE if NOT EXISTS cargos (
            id_cargo INTEGER auto_increment not null primary key,
            nombre_cargo varchar(60) not null
        )
        """,
        """
        CREATE TABLE if NOT EXISTS usuarios (
            id_usuario INTEGER not NULL AUTO_INCREMENT PRIMARY KEY,
            nombre_usuario VARCHAR(60) NOT NULL,
            identificacion INTEGER NOT NULL UNIQUE,
            contrasena varchar(100) not null,
            email varchar(60) not null unique,
            telefono VARCHAR(15) not null,
            ext integer, 
            modalidad integer not null,
            cargo integer not null,
            CONSTRAINT usuarios_modalidad FOREIGN KEY  (modalidad) REFERENCES modalidades (id_modalidad) on delete cascade on update cascade,
            CONSTRAINT usuarios_cargo FOREIGN KEY  (cargo) REFERENCES cargos (id_cargo) on delete cascade on update cascade
        )
        """,
        """
        create TABLE if not EXISTS registrosPacientes (
            id_registro INTEGER not null AUTO_INCREMENT PRIMARY KEY,
            nombre_paciente VARCHAR(60) not null,
            identificacion_paciente INTEGER not NULL UNIQUE,
            edad TINYINT NOT NULL,
            rango_edad INTEGER not NULL,
            fecha_orden DATE NOT NULL,
            fecha_citacion DATE NOT NULL,
            hc INTEGER not NULL UNIQUE,
            ubicacion VARCHAR(12),
            modalidad INTEGER NOT NULL,
            estudios_ordenados INTEGER NOT NULL,
            diagnostico TEXT not NULL,
            ayuno VARCHAR(2) NOT NULL,
            diferido VARCHAR(2) NOT NULL,
            aislamiento VARCHAR(2) NOT NULL,
            tipo_aislamiento INTEGER not null,
            autorizacion VARCHAR(2) not null,
            anestesia VARCHAR(2) not null,
            estado INTEGER not null,
            sede INTEGER not NULL,
            hora_citacion TIME not null,
            hora_realizacion TIME not null,
            causal_retraso INTEGER not null,
            comentarios_tecnologo TEXT not null,
            comentar_radiologo VARCHAR(2) not null,
            comentarios_radiologo TEXT not NULL,
            usuario INTEGER not null,
            CONSTRAINT registrosPacientes_rangoedad FOREIGN KEY  (rango_edad) REFERENCES rangosEdades (id_rangoedad) on delete cascade on update cascade,
            CONSTRAINT registrosPacientes_usuario FOREIGN KEY  (usuario) REFERENCES usuarios (id_usuario) on delete cascade on update cascade
        )
        """, 
        """
        CREATE TABLE IF NOT EXISTS registrosPacientes_alergias (
            id_registro INTEGER NOT NULL,
            id_alergia INTEGER NOT NULL,
            PRIMARY KEY (id_registro, id_alergia),
            CONSTRAINT fk_registrosPacientes FOREIGN KEY (id_registro) REFERENCES registrosPacientes (id_registro) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_alergias FOREIGN KEY (id_alergia) REFERENCES alergias (id_alergia) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS registrosPacientes_aislamientos (
            id_registro INTEGER NOT NULL,
            id_aislamiento INTEGER NOT NULL,
            PRIMARY KEY (id_registro, id_aislamiento),
            CONSTRAINT fk_regPac_aisla FOREIGN KEY (id_registro) REFERENCES registrosPacientes (id_registro) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_aisla FOREIGN KEY (id_aislamiento) REFERENCES aislamientos (id_aislamiento) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS registrosPacientes_retrasos (
            id_registro INTEGER NOT NULL,
            id_retraso INTEGER NOT NULL,
            PRIMARY KEY (id_registro, id_retraso),
            CONSTRAINT fk_regPac_retraso FOREIGN KEY (id_registro) REFERENCES registrosPacientes (id_registro) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_retraso FOREIGN KEY (id_retraso) REFERENCES retrasos (id_retraso) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS registrosPacientes_sedes (
            id_registro INTEGER NOT NULL,
            id_sede INTEGER NOT NULL,
            PRIMARY KEY (id_registro, id_sede),
            CONSTRAINT fk_regPac_sede FOREIGN KEY (id_registro) REFERENCES registrosPacientes (id_registro) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_sede FOREIGN KEY (id_sede) REFERENCES sedes (id_sede) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS registrosPacientes_estudios (
            id_registro INTEGER NOT NULL,
            id_estudio INTEGER NOT NULL,
            PRIMARY KEY (id_registro, id_estudio),
            CONSTRAINT fk_regPac_estudio FOREIGN KEY (id_registro) REFERENCES registrosPacientes (id_registro) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_estudio FOREIGN KEY (id_estudio) REFERENCES estudiosOrdenados (id_estudio) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS registrosPacientes_modalidades (
            id_registro INTEGER NOT NULL,
            id_modalidad INTEGER NOT NULL,
            PRIMARY KEY (id_registro, id_modalidad),
            CONSTRAINT fk_regPac_modalidad FOREIGN KEY (id_registro) REFERENCES registrosPacientes (id_registro) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_modalidad FOREIGN KEY (id_modalidad) REFERENCES modalidades (id_modalidad) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS registrosPacientes_estados (
            id_registro INTEGER NOT NULL,
            id_estado INTEGER NOT NULL,
            PRIMARY KEY (id_registro, id_estado),
            CONSTRAINT fk_regPac_estado FOREIGN KEY (id_registro) REFERENCES registrosPacientes (id_registro) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_estado FOREIGN KEY (id_estado) REFERENCES estados (id_estado) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
        ]
        
        self.cursor.execute('create DATABASE if not EXISTS EntregaTurno')
        self.cursor.execute('use EntregaTurno')
        
        for sql in sql_statements:
            
            self.cursor.execute(sql)
            
        # para insertar
            
        # self.sql_statements1 = """insert into alergias (nombre_alergia) values (%s)"""
        
        # valores = ("Latex",)
        
        # self.cursor.execute(self.sql_statements1, valores)
        
        # para traer datos 
        
        # self.sql_consulta = """select * from alergias"""
        
        # self.cursor.execute(self.sql_consulta)
        
        # datos = self.cursor.fetchall()
        
        # for dato in datos:
            
        #     print(f' dato obtenido: {dato[1]}')
        
        # para borrar datos
        
        # self.sql_borrar = """delete from alergias where nombre_alergia = 'Latex' """
        
        # self.cursor.execute(self.sql_borrar)
            
        # self.cursor.execute('show databases')
        # self.cursor.execute('show tables')
        
        # for db in self.cursor:
            
        #     print(db)
            
        self.conexion.commit()
        
        # print(self.cursor.rowcount, "dato insertado")
        
        self.conexion.close()
       
# host = input("Ingrese el host de la base de datos: ")
# user = input("Ingrese el usuario de la base de datos: ")
# password = input("Ingrese la contraseña de la base de datos: ")
# port = int(input("Ingrese el puerto de la base de datos: "))
 
# ConexionDB(host,user,password, port)