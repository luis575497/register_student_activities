from app import app
from flask import render_template, redirect, url_for, request, flash
from app.forms.forms import RegistrarEstudianteForm, IngresarActividad
from app import db
from app.schemas.estudiante import Estudiante
from flask_login import login_required, current_user
from werkzeug.wrappers import Response

@app.route("/estudiante", methods=["POST", "GET"])
def add_student():
    if request.method == "POST":
        form_new_student = request.form
        estudiante_cedula = Estudiante.query.filter_by(cedula = form_new_student["cedula"]).first()
        estudiante_email  = Estudiante.query.filter_by(email = form_new_student["email"]).first()
        
        if (estudiante_cedula is None) and (estudiante_email is None):
            new_Student = Estudiante(
                nombre = form_new_student["nombre"],
                cedula = form_new_student["cedula"],
                email = form_new_student["email"],
                facultad = form_new_student["facultad"],
                carrera = form_new_student["carrera"],
                curso = form_new_student["curso"],
                phone = form_new_student["phone"],
                total_horas = form_new_student["total_horas"],
                )
            db.session.add(new_Student)
            db.session.commit()
            
            flash('Estudiante agregado correctamente',"success")
            return redirect(url_for("index"))

        else:
            try:
                flash(f"El estudiante ya se encuentra en la base de datos, por favor relice una búsqueda por el número de cédula: {estudiante_cedula.cedula}","error")
            except Exception:
                flash(f"El estudiante ya se encuentra en la base de datos, por favor relice una búsqueda por el número de cédula: {estudiante_email.cedula}","error")
            finally:
                return redirect(url_for("index"))
    
    if request.method == 'GET':
        estudiante_form = RegistrarEstudianteForm()
        return render_template("new_student.html", form = estudiante_form)


@app.route("/estudiante/<int:id>", methods=["GET","POST"])
@login_required
def estudiante(id: int):
    if request.method == "GET":
        context = {
        "estudiante" : Estudiante.query.get(id),
        "form" : RegistrarEstudianteForm(),
        "bibliotecario": current_user
        }
        return render_template("estudiante.html", **context)
    

@app.route("/estudiante/<int:id>/actualizar", methods=["POST"])
@login_required
def edit_estudiante(id: int) -> Response:
    if request.method == "POST":
        # Actualizar los datos del Estudiante
        datos_actualizados = request.form
        estudiante = Estudiante.query.get(id)
        estudiante.nombre = datos_actualizados["nombre"]
        estudiante.cedula = datos_actualizados["cedula"]
        estudiante.facultad = datos_actualizados["facultad"]
        estudiante.carrera = datos_actualizados["carrera"]
        estudiante.email = datos_actualizados["email"]
        estudiante.phone = datos_actualizados["phone"]
        estudiante.curso = datos_actualizados["curso"]
        estudiante.total_horas = datos_actualizados["total_horas"]

        db.session.commit()
        flash("Estudiante actualizado correctamente","success")
        return redirect(url_for("view_activities", id=estudiante.id))



@app.route("/view_activities/<int:id>", methods=["GET"])
@login_required
def view_activities(id: int):
    student = Estudiante.query.get(id)
    if request.method == "GET":
        context = {
        "student" : student,
        "actividades" : student.actividades,
        "form_actividades" : IngresarActividad(),
        "horas_realizadas" : student.horas_trabajadas(),
        "total_horas": student.total_horas
        }      
        return render_template("view_activities.html", **context)