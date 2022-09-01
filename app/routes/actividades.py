from app import app
from flask import render_template, redirect, url_for, request, flash
from app.forms.forms import IngresarActividad
from app import db
from app.schemas.estudiante import Estudiante
from app.schemas.bibliotecario import Bibliotecario
from app.schemas.actividad import Actividad
from datetime import datetime
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

@app.route("/actividad/<int:id_est>/", methods=["POST"])
@login_required
def add_activity(id_est: int) -> Response:
    """
    Agregar una actividad realizada por un estudiante, tiene como parámetro de entrada la 
    id del estudiante, obtiene los datos del formulario enviado y toma como bibliotecario
    al usuario que se encuentra logueado
    """

    #Obtener todos los datos de la actividad
    datos_actividades = request.form
    estudiante = Estudiante.query.get(id_est)
    bibliotecario = current_user
    hora_entrada = datetime.strptime(datos_actividades["hora_entrada"], '%H:%M')
    hora_salida = datetime.strptime(datos_actividades["hora_salida"], '%H:%M')
    total_horas = round((hora_salida - hora_entrada).seconds / 3600, 2)

    # Agregar la actividad a la Base de datos si mla hora de entrada es menor  a la hora de salida
    if hora_salida < hora_entrada:
        app.logger.error(f"{current_user.email} - La hora de entrada debe ser menor a la hora de salida")
        flash("La hora de entrada debe ser menor a la hora de salida", "error")
        return redirect(url_for("view_activities", id=id_est))
    
    else:
        new_activitie = Actividad(
            estudiante = estudiante,
            bibliotecario = bibliotecario,
            fecha = datos_actividades["fecha"] ,
            cantidad_de_horas = total_horas,
            nombre_actividad = datos_actividades["nombre"],
            hora_inicio = hora_entrada.time(),
            hora_fin = hora_salida.time(),
            )
        db.session.add(new_activitie)
        db.session.commit()
        app.logger.info(f"{current_user.email} - Actividad agregada correctamente")
        flash("Actividad agregada correctamente","success")
        return redirect(url_for("view_activities", id=id_est))


@app.route("/activity/<int:id_est>/<int:id_activity>/remove")
@login_required
def remove_activity(id_est: int, id_activity: int) -> Response:
    """
    Elimina una actividad de a base de datos tomando como entrada la id de la actividad y del estudiante.
    Regresa a la página de actividades del estudiante
    """
    db.session.delete(Actividad.query.get(id_activity))
    db.session.commit()
    app.logger.info(f"{current_user.email} - Actividad Eliminada Correctamente")
    flash("Actividad Eliminada Correctamente","success")
    return redirect(url_for("view_activities", id=id_est))



@app.route("/activity/<int:id_est>/<int:id_activity>/edit", methods=["POST","GET"])
@login_required
def edit_activity(id_est: int, id_activity: int)  -> Response: 
    """"
    POST - Recibe los datos del formulario enviado y actualiza con los nuevos datos la actividad
    GET -  Envía el formulario de actividades y los datos de actividad a editar
    """
    if request.method == "POST":
        actividades = request.form
        entrada = datetime.strptime(f'{actividades["hora_entrada"]}', '%H:%M')
        salida  = datetime.strptime(f'{actividades["hora_salida"]}' , '%H:%M')
        total_horas = round((salida - entrada).seconds / 3600, 2)
        bibliotecario = current_user

        if salida < entrada:
            app.logger.info(f"{current_user.email} - La hora de entrada debe ser menor a la hora de salida")
            flash("La hora de entrada debe ser menor a la hora de salida", "error")
            return redirect(url_for("edit_activity", id_est=id_est, id_activity=id_activity))
        else:
            # Actualizar los datos de la Actividad
            actividad =  Actividad.query.get(id_activity)
            actividad.nombre_actividad = actividades["nombre"]
            actividad.fecha = actividades["fecha"]
            actividad.hora_inicio = entrada.time()
            actividad.hora_fin = salida.time()
            actividad.cantidad_de_horas = total_horas
            actividad.bibliotecario = bibliotecario

            db.session.commit()
            app.logger.info(f"{current_user.email} - Actividad actualizada correctamente")
            flash("Actividad actualizada correctamente", "success")
            
            return redirect(url_for("view_activities", id=id_est ))
    
    if request.method == "GET":
        context = {
            "form_actividades" : IngresarActividad(),
            "actividad" :Actividad.query.get(id_activity),
            "id_est" : id_est,
        }
        return render_template("activity.html", **context)