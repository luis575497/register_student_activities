from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    SelectField,
    DateField,
    TimeField,
    PasswordField,
)
from wtforms.validators import InputRequired, Email, Length


class RegistrarEstudianteForm(FlaskForm):
    nombre = StringField("Nombre y Apellidos", validators=[InputRequired()])
    cedula = StringField(
        "Cédula",
        validators=[
            InputRequired(),
            Length(min=10, max=10, message="La cédula debe tener 10 dígitos"),
        ],
    )
    email = StringField(
        "Email", validators=[InputRequired(), Email(message="Correo incorrecto")]
    )
    facultad = StringField("Facultad", validators=[InputRequired()])
    carrera = StringField("Carrera", validators=[InputRequired()])
    curso = StringField("Curso", validators=[InputRequired()])
    phone = StringField(
        "Teléfono", validators=[InputRequired(), Length(min=10, max=10)]
    )
    total_horas = IntegerField("Numero de horas", validators=[InputRequired()])


class IngresarActividad(FlaskForm):
    nombre = SelectField(
        "Actividades",
        choices=[
            ("Arreglo de estantes", "Arreglo de estantes"),
            ("Digitalización", "Digitalización de material bibliográfico"),
            ("Arreglo de Vitrinas", "Arreglo de Vitrinas"),
            ("Búsqueda de libros", "Búsqueda de libros"),
            (
                "Colocación de señaléticas en estantes",
                "Colocación de señaléticas en estantes",
            ),
            ("Control de Sala", "Control de Sala"),
            ("Constatación de inventario", "Constatación de inventario"),
            ("Traslado de documentos", "Traslado de documentos"),
            ("Elaboración de listado de libros", "Elaboración de listado de libros"),
            (
                "Elaboración de inventario de libros",
                "Elaboración de inventario de libros",
            ),
        ],
        validators=[InputRequired()],
    )
    fecha = DateField("Fecha", format="%d-%m-%Y", validators=[InputRequired()])
    hora_entrada = TimeField("Hora entrada", validators=[InputRequired()])
    hora_salida = TimeField("Hora salida", validators=[InputRequired()])


class Buscador(FlaskForm):
    cedula = StringField(
        "Cédula",
        validators=[
            InputRequired(),
            Length(min=10, max=10, message="La cédula debe tener 10 dígitos"),
        ],
    )


class Login(FlaskForm):
    cedula = StringField(
        "Cédula",
        validators=[
            InputRequired(),
            Length(min=10, max=10, message="La cédula debe tener 10 dígitos"),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            InputRequired(),
        ],
    )


class BibliotecarioForm(FlaskForm):
    nombre = StringField("Nombre y Apellidos", validators=[InputRequired()])
    cedula = StringField(
        "Cédula",
        validators=[
            InputRequired(),
            Length(min=10, max=10, message="La cédula debe tener 10 dígitos"),
        ],
    )
    email = StringField(
        "Email", validators=[InputRequired(), Email(message="Correo incorrecto")]
    )
    campus = StringField("Campus", validators=[InputRequired()])
    puesto = StringField("Puesto", validators=[InputRequired()])
    password = PasswordField("Password")


class SeleccionarMes(FlaskForm):
    mes = SelectField(
        "Actividades",
        choices=[
            ("01", "Enero"),
            ("02", "Febrero"),
            ("03", "Marzo"),
            ("04", "Abril"),
            ("05", "Mayo"),
            ("06", "Junio"),
            ("07", "Julio"),
            ("08", "Agosto"),
            ("09", "Septiembre"),
            ("10", "Octubre"),
            ("11", "Noviembre"),
            ("12", "Diciembre"),
        ],
        validators=[InputRequired()],
    )
