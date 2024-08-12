from app import db

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    equipos = db.relationship('Equipo', backref='marca', lazy=True)

    def __str__(self) -> str:
        return self.nombre

class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    pais_origen = db.Column(db.String(100), nullable=False)

    modelos = db.relationship('Modelo', backref='fabricante', lazy=True)

    def __str__(self) -> str:
        return self.nombre

class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)

    equipos = db.relationship('Equipo', backref='modelo', lazy=True)
    caracteristicas = db.relationship('Caracteristica', backref='modelo', lazy=True)
    accesorios = db.relationship('Accesorio', backref='modelo', lazy=True)

    def __str__(self) -> str:
        return self.nombre

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    equipos = db.relationship('Equipo', backref='categoria', lazy=True)

    def __str__(self) -> str:
        return self.nombre

class Caracteristica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)

    equipos = db.relationship('Equipo', backref='caracteristica', lazy=True)

    def __str__(self) -> str:
        return self.tipo

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    disponible = db.Column(db.Boolean, default=True) 

    equipo = db.relationship('Equipo', back_populates='stocks') 

    def __str__(self) -> str:
        return str(self.id)

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)

    inventarios = db.relationship('Inventario', back_populates='proveedor')

    def __str__(self) -> str:
        return self.nombre

class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)

    equipos = db.relationship('Equipo', backref='accesorio', lazy=True)

    def __str__(self) -> str:
        return self.tipo

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    caracteristica_id = db.Column(db.Integer, db.ForeignKey('caracteristica.id'), nullable=False)
    accesorio_id = db.Column(db.Integer, db.ForeignKey('accesorio.id'), nullable=True)

    stocks = db.relationship('Stock', back_populates='equipo') 

    def __str__(self) -> str:
        return str(self.id)

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    proveedor = db.relationship('Proveedor', back_populates='inventarios')

    def __str__(self) -> str:
        return str(self.id)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    ventas = db.relationship('Venta', backref='cliente', lazy=True)

    def __str__(self) -> str:
        return self.nombre

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())

    equipo = db.relationship('Equipo', backref='ventas')

    def __str__(self) -> str:
        return str(self.id)

