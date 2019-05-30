"""
Módulo para acceso al modelo multidimensional en la base de datos.

El archivo db.config proporciona la configuración necesaria para la
conexión a la base de datos.
"""

import configparser
import os

CUR_DIR = os.path.dirname(__file__)

__config_file = os.path.join(CUR_DIR, 'db.config')

# Configuración de base de datos
dbconfig = configparser.ConfigParser()
dbconfig.read(__config_file)

# Configuración de directorio para las gráficas
PLOT_DIR = os.path.join(CUR_DIR + os.path.sep +  '..', 'plots')
if not os.path.exists(PLOT_DIR):
    os.mkdir(PLOT_DIR)