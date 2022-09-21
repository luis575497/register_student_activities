from app import app
from flask import render_template, redirect, url_for, request, flash
from app.schemas.estudiante import Estudiante
from werkzeug.wrappers import Response

# Buscar Estudiantes
@app.route("/search", methods=["POST"])
def search() -> Response:
    cedula = request.form["cedula"]
    estudiante = Estudiante.query.filter_by(cedula=cedula).first()
    if estudiante is not None:
        return redirect(url_for("view_activities", id=estudiante.id))
    else:
        flash("No existe el número de cédula ingresado", "error")
        return redirect(url_for("index"))
