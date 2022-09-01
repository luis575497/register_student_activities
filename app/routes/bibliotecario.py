from calendar import month
from contextlib import redirect_stderr
from app import app, db
from flask_login import current_user
from flask import render_template, request, flash, redirect, url_for
from app.forms.forms import BibliotecarioForm, SeleccionarMes
from flask_login import login_required
from app.schemas.actividad import Actividad
from datetime import datetime, timedelta
from functools import reduce
import hashlib

@app.route("/bibliotecario", methods=["GET"])
@login_required
def bibliotecario():
    fecha_actual = datetime.now()
    actividades = Actividad.query.filter(Actividad.fecha > fecha_actual - timedelta(days=30)).filter_by(bibliotecario_id = current_user.id).all()
    context = {
    "actividades" : actividades,
    "horas_supervisadas": reduce(lambda inicio, actividad: actividad.cantidad_de_horas + inicio, actividades, 0),
    "bibliotecario": current_user,
    "estudiantes": len({actividad.estudiante_id for actividad in actividades}),
    "hash_name":  hashlib.md5(current_user.nombre.lower().encode('utf-8')).hexdigest(),
    "form": SeleccionarMes(),
    }
    app.logger.info(context["estudiantes"])
    return render_template("bibliotecario.html", **context)


@app.route("/bibliotecario/update", methods=["GET","POST"])
@login_required
def update_bibliotecario():
    if request.method == 'GET':
        context = {
        "form": BibliotecarioForm(),
        "bibliotecario": current_user
        }
        return render_template("update_bibliotecario.html", **context)
    
    if request.method == 'POST':
        datos = request.form
        bibliotecario = current_user
        bibliotecario.nombre =datos["nombre"]
        bibliotecario.cedula =datos["cedula"]
        bibliotecario.email =datos["email"]
        bibliotecario.puesto =datos["puesto"]
        bibliotecario.campus =datos["campus"]
        db.session.commit()
        flash("Usuario actualizado exitosamente","success")
        return redirect(url_for("bibliotecario"))

@login_required
@app.route("/bibliotecario/reset_password", methods=["GET","POST"])
def reset_password():
    if request.method == 'GET':
        context = {
            "form" : BibliotecarioForm(),
        }
        return render_template("password.html", **context)
    if request.method == 'POST':
        datos = request.form
        bibliotecario = current_user
        bibliotecario.password =datos["password"]
        db.session.commit()
        flash("Contraseña actualizada exitosamente","success")
        return redirect(url_for("logout"))

@login_required
@app.route("/bibliotecario/informe", methods=["POST"])
def informe():
    if request.method == "POST":
        mes = request.form["mes"]
        return f"Mes: {mes}"