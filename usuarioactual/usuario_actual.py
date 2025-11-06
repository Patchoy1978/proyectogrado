class UsuarioActual:

    usuario = None       # Email del usuario
    nombre = None       # Nombre del usuario
    cargo = None         # Cargo del usuario
    id_usuario = None   # ID en la base de datos
        
    @classmethod
    def set_usuario(cls, email, nombre, cargo, id_usuario):
        cls.usuario = email
        cls.nombre = nombre
        cls.cargo = cargo
        cls.id_usuario = id_usuario

    @classmethod
    def limpiar_usuario(cls):
        cls.usuario = None
        cls.nombre = None
        cls.cargo = None
        cls.id_usuario = None