"""
Submódulo de Bibliotecario (routes)
=================================

Este módulo contiene todas las rutas definidas para trabajar con los errores que se
generen en la aplicación:

- Error 401
- Error 404
- Error 405
"""


from app import app
from flask import redirect, url_for, render_template
from typing import Type
from werkzeug.exceptions import NotFound
from werkzeug.wrappers import Response


@app.errorhandler(401)
def status_401(error: Type[NotFound]) -> Response:
    """
    Error 401

    Si un usuario no se encuentra autentificado lo redirige hacia la página de
    login

    Parameters
    ----------
    error : Type[NotFound]
        Error generado definido en el módulo ``werkzeug.exceptions``

    Returns
    -------
    Response
       Redirección hacia la ruta vinculada con la función ``login``

    Notes
    -----
    Se registra el error en la aplicación mediante el decorador ``errorhandler``
    """
    return redirect(url_for("login"))


@app.errorhandler(404)
def status_404(error: Type[NotFound]) -> str:
    """
    Error 404

    Manejo personalizado de error 404.

    Parameters
    ----------
    error : Type[NotFound]
        Error generado definido en el módulo ``werkzeug.exceptions``

    Returns
    -------
    str
       Renderizado de la plantilla ``error.html`` con los datos obtenidos previamente

    Notes
    -----
    Se registra el error en la aplicación mediante el decorador ``errorhandler``
    """
    context = {
        "title": "Página no encontrada",
        "type_error": "404",
        "img_path": "img/pac-404.png",
        "message": "La pagina que buscaba no se encuentra disponible, por favor regrese al inicio",
    }
    return render_template("error.html", **context)


@app.errorhandler(405)
def status_405(error: Type[NotFound]) -> str:
    """
    Error 405

    Manejo personalizado de error 405.

    Parameters
    ----------
    error : Type[NotFound]
        Error generado definido en el módulo ``werkzeug.exceptions``

    Returns
    -------
    str
       Renderizado de la plantilla ``error.html`` con los datos obtenidos previamente

    Notes
    -----
    Se registra el error en la aplicación mediante el decorador ``errorhandler``
    """
    context = {
        "title": "Método no permitido",
        "type_error": "405",
        "img_path": "img/pac-404.png",
        "message": "Esta ruta no permite el método HTTP solicitado",
    }
    return render_template("error.html", **context)
