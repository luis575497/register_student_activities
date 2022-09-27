"""
Submódulo de Autenticación (routes)
=====================================

Este módulo contiene todas las rutas definidas y configuraciones necesaria para
manejar la autenticación del usuario.

- Cargar el usuario
- Loggin
- Logout
"""

from flask import render_template, redirect, url_for, request, flash, session
from app import login_manager
from app.schemas.bibliotecario import Bibliotecario
from app import app
from app.forms.forms import Login
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.wrappers import Response


@login_manager.user_loader
def load_user(user_id) -> Bibliotecario:
    """
    Cargar Usuario

    Cargar los datos del usuario mediante una búsqueda por el id en la base de datos.
    Se utiliza el decorador de ``login_manager`` para registar al usuario.

    Parameters
    ----------
    user_id : int
        Identificador único del bibliotecario en la base de datos

    Returns
    -------
    Bibliotecario
        Instancia de un modelo de bibliotecario del ORM SQLAlchemy

    """
    return Bibliotecario.query.get(user_id)


@app.route("/login", methods=["GET"])
def login() -> str:
    """
    Inicio de sesión

    Cuando se envía una petición GET hacia la ruta ``/login`` se envían los datos
    del formulario de login.

    Returns
    -------
    str
        Renderizado del template ``login.html`` mediante platillas Jinja2

    """
    if request.method == "GET":
        login_form = Login()
        return render_template("login.html", form=login_form)


@app.route("/login/validate_user", methods=["POST"])
def validate_user() -> Response:
    """
    Validar usuarios

    Cuando se envía una petición POST hacia la ruta ``/login/validate_user`` se envían los datos
    del formulario de login.

    Returns
    -------
    Response
        Redirección hacia la página ``index.html`` si se valida correctamente al usuario,
        en caso contrario lo redirige hacia la ruta ``/login/``.

    """
    if request.method == "POST":
        datos = request.form
        bibliotecario = Bibliotecario.query.filter_by(cedula=datos["cedula"]).first()
        if bibliotecario:
            if check_password_hash(bibliotecario.password, datos["password"]):
                login_user(bibliotecario, remember=True)
                session.permanent = True
                app.logger.info(
                    f"{current_user.email} - Usuario logueado correctamente"
                )
                return redirect(url_for("index"))
            else:
                flash("Contraseña incorrecta", "error")
                app.logger.info(f"Contraseña incorrecta")
                return redirect(url_for("login"))
        else:
            flash("NO existe un usuario con el número de cédula ingresado", "error")
            app.logger.info(f"NO existe un usuario con el número de cédula ingresado")
            return redirect(url_for("login"))


@app.route("/logout", methods=["GET"])
@login_required
def logout() -> Response:
    """
    Cerrar Sesión

    Cuando se envía una petición POST hacia la ruta ``/logout`` se ejecuta la función
    ``logout_user()`` de la librería ``Flask-login`` para cerrar la sesión del usuario.

    Returns
    -------
    Response
        Redirección hacia la ruta ``/login/``.

    """
    logout_user()
    return redirect(url_for("login"))
