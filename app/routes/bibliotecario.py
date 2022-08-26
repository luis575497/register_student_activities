from contextlib import redirect_stderr
from app import app, db
from flask_login import current_user
from flask import render_template, request, flash, redirect, url_for
from app.forms.forms import BibliotecarioForm
from flask_login import login_required

@login_required
@app.route("/bibliotecario", methods=["GET"])
def bibliotecario():
    return render_template("bibliotecario.html", bibliotecario=current_user)

@login_required
@app.route("/bibliotecario/update", methods=["GET","POST"])
def update_bibliotecario():
    if request.method == 'GET':
        context = {
        "form": BibliotecarioForm(),
        "bibliotecario": current_user
        }
        return render_template("update_bibliotecario.html", **context)
    
    if request.method == 'POST':
        datos = request.form
        bibliotecario = current_user
        bibliotecario.nombre =datos["nombre"]
        bibliotecario.cedula =datos["cedula"]
        bibliotecario.email =datos["email"]
        bibliotecario.puesto =datos["puesto"]
        bibliotecario.campus =datos["campus"]
        db.session.commit()
        flash("Usuario actualizado exitosamente","success")
        return redirect(url_for("bibliotecario"))

@login_required
@app.route("/bibliotecario/reset_password", methods=["GET","POST"])
def reset_password():
    if request.method == 'GET':
        context = {
            "form" : BibliotecarioForm(),
        }
        return render_template("password.html", **context)
    if request.method == 'POST':
        datos = request.form
        bibliotecario = current_user
        bibliotecario.password =datos["password"]
        db.session.commit()
        flash("Contraseña actualizada exitosamente","success")
        return redirect(url_for("logout"))