from app import db
from app.schemas.bibliotecario import Bibliotecario
from werkzeug.security import generate_password_hash


@db.event.listens_for(Bibliotecario.password, "set", retval=True)
@db.event.listens_for(Bibliotecario.password, "modified", retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    """
    Cuando se detecta una modificación en el campo password de la tabla bibliotecario, se
    realiza automaticamente un hash del valor asignado y este remplaza al valor en la tabla
    """
    if value != oldvalue:
        return generate_password_hash(value)
    return value
