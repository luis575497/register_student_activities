from flask import render_template, redirect, url_for, request, flash, session, g
from app import login_manager
from app.schemas.bibliotecario import Bibliotecario
from app import app
from app.forms.forms import Login
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.wrappers import Response

@login_manager.user_loader
def load_user(user_id):
    return Bibliotecario.query.get(user_id)

@app.route("/login", methods = ['GET', 'POST'])
def login() -> Response:
    if request.method == "GET":
        login_form = Login()
        return render_template("login.html", form=login_form)
    if request.method == "POST":
        datos = request.form
        bibliotecario = Bibliotecario.query.filter_by(cedula = datos["cedula"]).first()
        if bibliotecario:
            if check_password_hash(bibliotecario.password, datos["password"]):
                login_user(bibliotecario, remember=True)
                session.permanent = True
                app.logger.info(f"{current_user.email} - Usuario logueado correctamente")
                return redirect(url_for("index"))
            else:
                flash("Contraseña incorrecta","error")
                app.logger.info(f"Contraseña incorrecta")
                return redirect(url_for("login"))
        else:
            flash("NO existe un usuario con el número de cédula ingresado","error")
            app.logger.info(f"NO existe un usuario con el número de cédula ingresado")
            return redirect(url_for("login"))

@app.route("/logout", methods = ['GET'])
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for("login"))
