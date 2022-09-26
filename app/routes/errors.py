from app import app
from flask import redirect, url_for, render_template


@app.errorhandler(401)
def status_401(error):
    return redirect(url_for("login"))


@app.errorhandler(404)
def status_404(error):
    context = {
        "title": "Página no encontrada",
        "type_error": "404",
        "img_path": "img/pac-404.png",
        "message": "La pagina que buscaba no se encuentra disponible, por favor regrese al inicio",
    }
    return render_template("error.html", **context)


@app.errorhandler(405)
def status_405(error):
    context = {
        "title": "Método no permitido",
        "type_error": "405",
        "img_path": "img/pac-404.png",
        "message": "Esta ruta no permite el método HTTP solicitado",
    }
    return render_template("error.html", **context)
