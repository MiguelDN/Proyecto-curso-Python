import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class Categorias(db.Base):
    """Categorías de los artículos"""
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    articulos = relationship("Inventario", cascade="all, delete-orphan",
                             backref="Categorias", lazy='dynamic')

    def __init__(self, nombre):
        self.nombre = nombre



class Inventario(db.Base):
    __tablename__ = "inventario"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, default=0)
    iva = Column(Integer, default=21)
    descripcion = Column(String(255))
    image = Column(String(255))
    stock = Column(Integer, default=0)
    capacidad_stock = Column(Integer, default=0)
    ubicacion = Column(String, default=0)
    Proveedorid = Column(Integer, ForeignKey('proveedores.id'), nullable=False)
    CategoriaId = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    activo = Column(Boolean, default=True)
    categoria = relationship("Categorias", backref="Articulos")
    proveedor = relationship("Proveedores", backref="Proveedor")


    def precio_final(self):
        return round(self.precio + (self.precio * self.iva / 100), 2)

    def porcentaje_stock(self):
        return round(self.stock * 100 / self.capacidad_stock, 1)



class Proveedores(db.Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    cif = Column(String, nullable=False)
    descuento = Column(Float, default=0)
    direccion = Column(String(255))
    telefono = Column(String(15))
    activo = Column(Boolean, default=True)
    proveedor = relationship("Inventario", cascade="all, delete-orphan",
                             backref="Proveedores", lazy='dynamic')
    proveedorUsu = relationship("Usuarios", cascade="all, delete-orphan",
                                backref="Proveedores", lazy='dynamic')




class Usuarios(db.Base):
    """Usuarios"""
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(128), nullable=False)
    nombre = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    admin = Column(Boolean, default=False)
    proveedor = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    usuProveedorId = Column(Integer, ForeignKey("proveedores.id"), default=0)
    usuProveedor = relationship("Proveedores", backref="ProveedorUsu")


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def is_admin(self):
        return self.admin

    def is_proveedor(self):
        return self.proveedor


class Ventas(db.Base):
    """Ventas"""
    __tablename__ = 'ventas'
    id = Column(Integer, primary_key=True)
    idProducto = Column(Integer, ForeignKey("inventario.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    idUsuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    idProveedor = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
