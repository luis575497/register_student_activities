from app import db
from functools import reduce


class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    facultad = db.Column(db.String(50), nullable=False)
    carrera = db.Column(db.String(50), nullable=False)
    curso = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    actividades = db.relationship("Actividad", backref="estudiante")
    total_horas = db.Column(db.Integer(), nullable=False)

    def __repr__(self) -> str:
        return "<Estudiante %r>" % self.nombre

    def __init__(
        self, cedula, email, facultad, carrera, curso, phone, nombre, total_horas
    ) -> None:
        self.cedula = cedula
        self.email = email
        self.facultad = facultad
        self.carrera = carrera
        self.curso = curso
        self.phone = phone
        self.nombre = nombre
        self.total_horas = total_horas

    def horas_trabajadas(self) -> float:
        return reduce(
            lambda inicio, actividad: actividad.cantidad_de_horas + inicio,
            self.actividades,
            0,
        )
