# -*- coding: utf-8 -*-
"""
Módulo de rutas (routes)
===========================

Este módulo contiene todas las rutas definidas en la aplicación y se separan en
diferentes archivos de acuerdo al objeto sobre el cual se le estan realizando
las accciones
"""

from app import app
from flask import render_template, request
from app.forms.forms import Buscador
from app.schemas.estudiante import Estudiante
from flask_login import login_required
from app.routes.estudiante import *
from app.routes.actividades import *
from app.routes.buscador import *
from app.routes.auth import *
from app.routes.certificado import *
from app.routes.bibliotecario import *


@app.route("/", methods=["GET"])
@login_required
def index() -> str:
    """
    Renderizado del template index

    Cuando se envía una petición POST hacia la ruta raiz ``/`` se buscan los datos sobre formulario
    del buscado y un listado de los últimos 10 estudiantes ingresados en la base de datos y posteriormente
    se renderiza el template ``index.html``.

    Returns
    -------
    str
        Renderizado del template ``index.html`` mediante platillas Jinja2

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema

    """
    if request.method == "GET":
        context = {
            "buscador": Buscador(),
            "lista_estudiantes": Estudiante.query.order_by(Estudiante.id.desc())
            .limit(10)
            .all(),
        }
        return render_template("index.html", **context)
