.. Register Students Activities documentation master file, created by
   sphinx-quickstart on Thu Sep 22 11:10:21 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Register Students Activities documentation!
========================================================

Configuración
-------------------------
Antes de ejecutar el proyecto deberá configurar la conexión con la base de datos en el archivo `config.py` y modificar la propiedad `SQLALCHEMY_DATABASE_URI` en donde:

- `mysql+pymysql` : es el conector de python para mysql.
- `root:admin`: es el usuario y la contraseña  respectivamente.
- `@localhost/estudiantes`: es el host y el nombre de la base de datos.

La base de datos indicada deberá no contener ninguna tabla

.. admonition:: Ejemplo

   Ejemplo de configuración del archivo `config.py`

   .. code-block:: python

    class Config(object):
         DEBUG = False
         SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/estudiantes"
         SQLALCHEMY_TRACK_MODIFICATIONS = False
         TESTING = True
         DEBUG = True
         FLASK_DEBUG = "development"
         SECRET_KEY = "sdfksdj156165gnsdfnsdonfs"
         TEMPLATES_FOLDER = "templates"
         PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)

Instalación
--------------------------
Este proyecto sutiliza `Poetry <https://python-poetry.org/>`_ para manejar las dependencias, por lo que para instalar el proyecto debera tenerlo instalado. Una vez instalado en la carpeta del proyecto
ejecute el siguiente comando

.. code-block:: bash

   poetry install


Admin-tools
-------------------------
Se debe crear un usuario mediante la ruta `/admin` y agregar un nuevo bibliotecario. El bibliotecario ingresará con su número de cédula y la contraseña creada.
Se podrá crear y modificar estudiantes, además de poder agregar, modificar y eliminar las actividades realizadas


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   routes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
