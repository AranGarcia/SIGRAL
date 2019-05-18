"""
Módulo para acceso al modelo multidimensional en la base de datos.

El archivo db.config proporciona la configuración necesaria para la
conexión a la base de datos.
"""

import configparser
import os

__config_file = os.path.join(os.path.dirname(__file__), 'db.config')

dbconfig = configparser.ConfigParser()
dbconfig.read(__config_file)
