# Registro de actividades

# Requisitos
- mysql

# Instalación

# Configuración
Antes de ejecutar el proyecto deberá configurar la conexión con la base de datos en el archivo `config.py` y modificar la propiedad `SQLALCHEMY_DATABASE_URI` en donde:
- `mysql+pymysql` : es el conector de python para mysql
- `root:admin`: es el usuario y la contraseña  respectivamente
- `@localhost/estudiantes`: es el host y el nombre de la base de datos
La base de datos indicada deberá no contener ninguna tabla

# Uso
Se debe crear un usuario mediante la ruta `/admin` y agregar un nuevo bibliotecario
El bibliotecario ingresará con su número de cédula y la contraseña creada.
Se podrá crear y modificar estudiantes, además de poder agregar, modificar y eliminar las actividades realizadas
