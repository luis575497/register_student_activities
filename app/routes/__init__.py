from app import app
from flask import render_template, request
from app.forms.forms import IngresarActividad, Buscador
from app.schemas.estudiante import Estudiante
from functools import reduce
from flask_login import current_user, login_required

@app.route("/", methods=["GET"])
@login_required
def index():
    if request.method == "GET":
        context = {
        "buscador" : Buscador(),
        "lista_estudiantes" : Estudiante.query.order_by(Estudiante.id.desc()).limit(10).all()
        } 
        return render_template("index.html", **context)


@app.route("/view_activities/<int:id>", methods=["GET"])
@login_required
def view_activities(id: int):
    student = Estudiante.query.get(id)
    if request.method == "GET":
        context = {
        "student" : student,
        "actividades" : student.actividades,
        "form_actividades" : IngresarActividad(),
        "horas_realizadas" : student.horas_trabajadas(),
        "total_horas": student.total_horas
        }      
        return render_template("view_activities.html", **context)

from app.routes.estudiante import *
from app.routes.actividades import *
from app.routes.buscador import *
from app.routes.auth import *
from app.routes.certificado import *
from app.routes.bibliotecario import *