from flask_login import current_user
from flask import render_template, request, flash, redirect, url_for, make_response
from app.forms.forms import BibliotecarioForm, SeleccionarMes
from flask_login import login_required
from app.schemas.actividad import Actividad
from datetime import datetime, timedelta, date
from functools import reduce
import hashlib
import calendar
from sqlalchemy import and_
import pandas as pd
from app import app, db


@app.route("/bibliotecario", methods=["GET"])
@login_required
def bibliotecario():
    fecha_actual = datetime.now()
    actividades = (
        Actividad.query.filter(Actividad.fecha > fecha_actual - timedelta(days=30))
        .filter_by(bibliotecario_id=current_user.id)
        .all()
    )
    context = {
        "actividades": actividades,
        "horas_supervisadas": reduce(
            lambda inicio, actividad: actividad.cantidad_de_horas + inicio,
            actividades,
            0,
        ),
        "bibliotecario": current_user,
        "estudiantes": len({actividad.estudiante_id for actividad in actividades}),
        "hash_name": hashlib.md5(
            current_user.nombre.lower().encode("utf-8")
        ).hexdigest(),
        "form": SeleccionarMes(),
    }
    app.logger.info(context["estudiantes"])
    return render_template("bibliotecario.html", **context)


@app.route("/bibliotecario/update", methods=["GET", "POST"])
@login_required
def update_bibliotecario():
    if request.method == "GET":
        context = {"form": BibliotecarioForm(), "bibliotecario": current_user}
        return render_template("update_bibliotecario.html", **context)

    if request.method == "POST":
        datos = request.form
        bibliotecario = current_user
        bibliotecario.nombre = datos["nombre"]
        bibliotecario.cedula = datos["cedula"]
        bibliotecario.email = datos["email"]
        bibliotecario.puesto = datos["puesto"]
        bibliotecario.campus = datos["campus"]
        db.session.commit()
        flash("Usuario actualizado exitosamente", "success")
        app.logger.info(f"Usuario actualizado exitosamente - {current_user.email}")
        return redirect(url_for("bibliotecario"))


@login_required
@app.route("/bibliotecario/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        context = {
            "form": BibliotecarioForm(),
        }
        return render_template("password.html", **context)
    if request.method == "POST":
        datos = request.form
        bibliotecario = current_user
        bibliotecario.password = datos["password"]
        db.session.commit()
        flash("Contraseña actualizada exitosamente", "success")
        return redirect(url_for("logout"))


@login_required
@app.route("/bibliotecario/informe", methods=["POST"])
def informe():
    if request.method == "POST":
        month = int(request.form["mes"])
        year = datetime.now().year
        num_days = calendar.monthrange(year, month)[1]
        start_date = date(year, month, 1)
        end_date = date(year, month, num_days)
        query = Actividad.query.filter(
            and_(Actividad.fecha >= start_date, Actividad.fecha <= end_date)
        ).filter_by(bibliotecario_id=current_user.id)
        df = pd.read_sql(query.statement, query.session.bind)
        resp = make_response(df.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=Informe.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
