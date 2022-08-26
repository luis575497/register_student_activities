from app import db, UserMixin

class Bibliotecario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cedula = db.Column(db.String(10),unique=True, nullable=False )
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    campus = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(250), nullable=False) 
    actividades = db.relationship("Actividad", backref="bibliotecario")

    def __repr__(self) -> str:
        return '<Bibliotecario %r>' % self.nombre

    def __init__(self, cedula, nombre, email, campus, password):
        self.cedula = cedula
        self.nombre = nombre
        self.email = email
        self.campus = campus
        self.password = password