"""
Submódulo de Utilidades (routes)
=================================

Este módulo contiene diferentes rutas para diversas utilidades):

- Buscador de estudiantes
- Creación de certificados
"""

from app import app
from flask import redirect, url_for, request, flash, send_file
from flask_login import login_required
from app.schemas.estudiante import Estudiante
from app.schemas.estudiante import Estudiante
from app.utils.certificado import generar_certificado
from werkzeug.wrappers import Response

# Buscar Estudiantes
@app.route("/search", methods=["POST"])
@login_required
def search() -> Response:
    """
    Datos bibliotecario

    Cuando se envía una petición GET hacia la ruta ``/bibliotecario>/`` se envían los
    datos necesarios para generar el dashboard del bibliotecario.

    Returns
    -------
    str
        Renderizado de la plantilla ``bibliotecario.html`` con los datos obtenidos previamente

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema
    """
    cedula = request.form["cedula"]
    estudiante = Estudiante.query.filter_by(cedula=cedula).first()
    if estudiante is not None:
        return redirect(url_for("view_activities", id=estudiante.id))
    else:
        flash("No existe el número de cédula ingresado", "error")
        return redirect(url_for("index"))


@app.route("/certificado/<int:id>")
def crear_certificado(id: int):
    certificado = [generar_certificado(id, app.root_path)]
    certificado[0].seek(0)
    return send_file(certificado[0], as_attachment=True, download_name="60_horas.docx")
