"""
Submódulo de Estudiantes (routes)
=====================================

Este módulo contiene todas las rutas definidas para manejar las operaciones con
estudiantes. Contiene funciones para

- Añadir estudiantes a la base de datos
- Editar estudiantes de la base de datos
- Eliminar estudiantes de la base de datos
- Mostrar dashboard del estudiante
"""

from app import app
from flask import render_template, redirect, url_for, request, flash
from app.forms.forms import RegistrarEstudianteForm, IngresarActividad
from app import db
from app.schemas.estudiante import Estudiante
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.wrappers import Response


@app.route("/estudiante/add", methods=["POST"])
def add_student() -> Response:
    """
    Agregar estudiante

    Se agrega un estudiante a la base de datos con los datos obtenidos del formulario
    enviado por un usuario.

    Returns
    -------
    Response
        Una vez agregado el usuario se redirige hacia la página asociada con la función ``index``

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema
    """
    form_new_student = request.form
    try:
        new_Student = Estudiante(
            nombre=form_new_student["nombre"],
            cedula=form_new_student["cedula"],
            email=form_new_student["email"].lower(),
            facultad=form_new_student["facultad"],
            carrera=form_new_student["carrera"],
            curso=form_new_student["curso"],
            phone=form_new_student["phone"],
            total_horas=form_new_student["total_horas"],
        )
        db.session.add(new_Student)
        db.session.commit()

        flash("Estudiante agregado correctamente", "success")
        app.logger.info(f"{current_user.email} - Estudiante agregado correctamente")
        return redirect(url_for("index"))

    except IntegrityError:
        flash(
            f"El estudiante ya se encuentra en la base de datos, por favor relice una búsqueda por el número de cédula",
            "error",
        )
        return redirect(url_for("student_form"))


@app.route("/estudiante/<id>", methods=["GET"])
@login_required
def estudiante(id: int):
    """
    Formulario de usuario

    Al realizar una solicitud GET a la ruta ``/estudiante/<id>`` se envía el formulario de usuario y se enviarán
    los datos a la plantilla, de no tener un resultado válido para la consulta se renderizará un formulario vacío.

    Parameters
    ----------
    id : int
        Identificador único del estudiante en la base de datos

    Returns
    -------
    str
        Renderizado de la plantilla ``estudiante_form.html`` con los datos obtenidos previamente

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema
    """
    context = {
        "estudiante": Estudiante.query.get(id),
        "form": RegistrarEstudianteForm(),
        "bibliotecario": current_user,
    }
    return render_template("estudiante_form.html", **context)


@app.route("/estudiante/<int:id>/actualizar", methods=["POST"])
@login_required
def edit_estudiante(id: int) -> Response:
    """
    Editar datos del usuario

    Al realizar una solicitud POST a la ruta ``/estudiante/<id>/actualizar`` se actualizan los
    datos del usuario enviados en el formulario por el usuario.

    Parameters
    ----------
    id : int
        Identificador único del estudiante en la base de datos

    Returns
    -------
    Response
        Redirección hacia la ruta asociada con la función ``view_activities``

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema
    """
    # Actualizar los datos del Estudiante
    datos_actualizados = request.form
    estudiante = Estudiante.query.get(id)
    estudiante.nombre = datos_actualizados["nombre"]
    estudiante.cedula = datos_actualizados["cedula"]
    estudiante.facultad = datos_actualizados["facultad"]
    estudiante.carrera = datos_actualizados["carrera"]
    estudiante.email = datos_actualizados["email"].lower()
    estudiante.phone = datos_actualizados["phone"]
    estudiante.curso = datos_actualizados["curso"]
    estudiante.total_horas = datos_actualizados["total_horas"]

    db.session.commit()
    flash("Estudiante actualizado correctamente", "success")
    app.logger.info(f"{current_user.email} - Estudiante actualizado correctamente")
    return redirect(url_for("view_activities", id=estudiante.id))


@app.route("/view_activities/<int:id>", methods=["GET"])
@login_required
def view_activities(id: int):
    """
    Visualizar las actividades del usuario

    Al realizar una solicitud GET a la ruta ``/view_activities/<int:id>`` sen enviarán los
    datos del usuario, formulario de actividad y horas totales hacia una plantilla Jinja2.

    Parameters
    ----------
    id : int
        Identificador único del estudiante en la base de datos

    Returns
    -------
    Response
        Redirección hacia la ruta asociada con la función ``view_activities``

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema
    """
    student = Estudiante.query.get(id)
    context = {
        "student": student,
        "actividades": student.actividades,
        "form_actividades": IngresarActividad(),
        "horas_realizadas": student.horas_trabajadas(),
        "total_horas": student.total_horas,
    }
    return render_template("view_activities.html", **context)
