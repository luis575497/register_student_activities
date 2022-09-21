from app import db


class Actividad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("estudiante.id"))
    bibliotecario_id = db.Column(db.Integer, db.ForeignKey("bibliotecario.id"))
    fecha = db.Column(db.Date)
    hora_inicio = db.Column(db.String(50), nullable=False)
    hora_fin = db.Column(db.String(50), nullable=False)
    cantidad_de_horas = db.Column(db.Float(), nullable=False)
    nombre_actividad = db.Column(db.String(50), nullable=False)
