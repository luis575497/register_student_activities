# Registro de actividades

# Requisitos
- mysql 

# Instalación 
Para instalar todas las dependencias del proyecto cree un entrorno virtual en la carpeta del proyecto
```bash
pip venv venv
```
y mediante el archivo `requeriments.txt` instale todas las librerías necesarias para el proyecto.
```bash
pip install -r requeriments.txt
```
# Configuración
Antes de ejecutar el proyecto deberá configurar la conexión con la base de datos en el archivo `config.py` y modificar la propiedad `SQLALCHEMY_DATABASE_URI` en donde:
- `mysql+pymysql` : es el conector de python para mysql
- `root:admin`: es el usuario y la contraseña  respectivamente
- `@localhost/estudiantes`: es el host y el nombre de la base de datos
La base de datos indicada deberá no contener ninguna tabla

# Uso

# Contribución