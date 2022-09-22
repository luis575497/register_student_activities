"""
Submódulo de Actividades (routes)
=================================

Este módulo contiene todas las rutas definidas para realizar con una actividad:
- Agregar una nueva activiadad
- Eliminar una actividad existente
- Obtener los datos de una actividad existente
- Editar una actividad existente
"""

from datetime import datetime
from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms.forms import IngresarActividad
from app.schemas.estudiante import Estudiante
from app.schemas.actividad import Actividad
from flask_login import current_user, login_required
from werkzeug.wrappers import Response


@app.route("/actividad/<int:id_est>/", methods=["POST"])
@login_required
def add_activity(id_est: int) -> Response:
    """
    Agregar una actividad

    Cuando se envía una petición POST hacia la ruta ``/actividad/<int:id_est>/`` se agrega
    una actividad realizada por un estudiante a la base de datos con los datos del
    formulario enviado y toma como bibliotecario al usuario que se encuentra logueado.

    Parameters
    ----------
    id_est : int
        Identificador único del estudiante en la base de datos

    Returns
    -------
    Response
        Redirección hacia la ruta vinculada con la función ``view_activities``

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema
    """

    # Obtener todos los datos de la actividad
    datos_actividades = request.form
    estudiante = Estudiante.query.get(id_est)
    bibliotecario = current_user
    hora_entrada = datetime.strptime(datos_actividades["hora_entrada"], "%H:%M")
    hora_salida = datetime.strptime(datos_actividades["hora_salida"], "%H:%M")
    total_horas = round((hora_salida - hora_entrada).seconds / 3600, 2)

    # Agregar la actividad a la Base de datos si mla hora de entrada es menor  a la hora de salida
    if hora_salida < hora_entrada:
        app.logger.error(
            f"{current_user.email} - La hora de entrada debe ser menor a la hora de salida"
        )
        flash("La hora de entrada debe ser menor a la hora de salida", "error")
        return redirect(url_for("view_activities", id=id_est))

    else:
        new_activitie = Actividad(
            estudiante=estudiante,
            bibliotecario=bibliotecario,
            fecha=datos_actividades["fecha"],
            cantidad_de_horas=total_horas,
            nombre_actividad=datos_actividades["nombre"],
            hora_inicio=hora_entrada.time(),
            hora_fin=hora_salida.time(),
        )
        db.session.add(new_activitie)
        db.session.commit()
        app.logger.info(f"{current_user.email} - Actividad agregada correctamente")
        flash("Actividad agregada correctamente", "success")
        return redirect(url_for("view_activities", id=id_est))


@app.route("/activity/<int:id_est>/<int:id_activity>/remove")
@login_required
def remove_activity(id_est: int, id_activity: int) -> Response:
    """
    Eliminar una actividad

    Cuando se envía una petición POST hacia la ruta ``/activity/<int:id_est>/<int:id_activity>/remove``
    se elimina la actividad identificada de la base de datos y se envía una notificación al usuario.

    Parameters
    ----------
    id_est : int
        Identificador único del estudiante en la base de datos
    id_activity : int
        Identificador único de la actividad en la base de datos

    Returns
    -------
    Response
        Redirección hacia la ruta vinculada con la función ``view_activities``

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema
    """

    db.session.delete(Actividad.query.get(id_activity))
    db.session.commit()
    app.logger.info(f"{current_user.email} - Actividad Eliminada Correctamente")
    flash("Actividad Eliminada Correctamente", "success")
    return redirect(url_for("view_activities", id=id_est))


@app.route("/activity/<int:id_est>/<int:id_activity>/view", methods=["GET"])
@login_required
def view_activity(id_est: int, id_activity: int) -> str:
    """
    Visualizar los datos de una actividad

    Cuando se envía una petición GET hacia la ruta ``/activity/<int:id_est>/<int:id_activity>/view``
    se recopilan los datos vinculados a la actividad señalada y se renderiza la plantilla Jinja2
    ``activity.html``.

    Parameters
    ----------
    id_est : int
        Identificador único del estudiante en la base de datos
    id_activity : int
        Identificador único de la actividad en la base de datos

    Returns
    -------
    str
        Renderizado de la plantilla ``activity.html`` con los datos obtenidos previamente

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema
    """
    if request.method == "GET":
        context = {
            "form_actividades": IngresarActividad(),
            "actividad": Actividad.query.get(id_activity),
            "id_est": id_est,
        }
        return render_template("activity.html", **context)


@app.route("/activity/<int:id_est>/<int:id_activity>/edit", methods=["POST", "GET"])
@login_required
def edit_activity(id_est: int, id_activity: int) -> Response:
    """
    Actualizar una actividad existente

    Cuando se envía una petición POST hacia la ruta ``/activity/<int:id_est>/<int:id_activity>/edit``
    se obtienen los datos enviados en el formulario, se realizan las comprobaciones en cuanto a la
    hora de salida y hora de entrada y se actualizan los datos de la actividad señalada en la base
    de datos.

    Parameters
    ----------
    id_est : int
        Identificador único del estudiante en la base de datos
    id_activity : int
        Identificador único de la actividad en la base de datos

    Returns
    -------
    Response
        Redirección hacia la ruta vinculada con la función ``view_activities`` con el parámetro de
        ``id`` del estudiante

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema
    """
    if request.method == "POST":
        actividades = request.form
        entrada = datetime.strptime(f'{actividades["hora_entrada"]}', "%H:%M")
        salida = datetime.strptime(f'{actividades["hora_salida"]}', "%H:%M")
        total_horas = round((salida - entrada).seconds / 3600, 2)
        bibliotecario = current_user

        if salida < entrada:
            app.logger.info(
                f"{current_user.email} - La hora de entrada debe ser menor a la hora de salida"
            )
            flash("La hora de entrada debe ser menor a la hora de salida", "error")
            return redirect(
                url_for("edit_activity", id_est=id_est, id_activity=id_activity)
            )
        else:
            # Actualizar los datos de la Actividad
            actividad = Actividad.query.get(id_activity)
            actividad.nombre_actividad = actividades["nombre"]
            actividad.fecha = actividades["fecha"]
            actividad.hora_inicio = entrada.time()
            actividad.hora_fin = salida.time()
            actividad.cantidad_de_horas = total_horas
            actividad.bibliotecario = bibliotecario

            db.session.commit()
            app.logger.info(
                f"{current_user.email} - Actividad actualizada correctamente"
            )
            flash("Actividad actualizada correctamente", "success")

            return redirect(url_for("view_activities", id=id_est))
