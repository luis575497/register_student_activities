from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin
from flask_avatars import Avatars

app = Flask(__name__)

# Configuración de la aplicación
app.config.from_object("config.DevelopmentConfig")

# Cargar Base de Datos
db = SQLAlchemy(app)
from app.schemas import *

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Font Awesome
fa = FontAwesome(app)

# Avatars
avatars = Avatars(app)

# Vista de Administrador para agregar bibliotecario
admin = Admin(app)
from app.schemas.bibliotecario import Bibliotecario
from app.schemas.estudiante import Estudiante

admin.add_views(ModelView(Bibliotecario, db.session))
admin.add_views(ModelView(Estudiante, db.session))

# cargar los eventos
from app.utils.events import hash_user_password
