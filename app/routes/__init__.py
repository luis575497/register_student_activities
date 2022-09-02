from app import app
from flask import render_template, request
from app.forms.forms import Buscador
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


from app.routes.estudiante import *
from app.routes.actividades import *
from app.routes.buscador import *
from app.routes.auth import *
from app.routes.certificado import *
from app.routes.bibliotecario import *