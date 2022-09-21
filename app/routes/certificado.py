from app import app
from flask import send_file
from app.forms.forms import IngresarActividad
from app.schemas.estudiante import Estudiante
from app.utils.certificado import generar_certificado


@app.route("/certificado/<int:id>")
def crear_certificado(id: int):
    certificado = [generar_certificado(id, app.root_path)]
    certificado[0].seek(0)
    return send_file(certificado[0], as_attachment=True, download_name="60_horas.docx")
