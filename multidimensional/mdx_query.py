"""
Módulo para el acceso a la base de datos multidimensional
"""

import mysql.connector
import pandas as pd

from . import dbconfig
from . import constants


class MySQLConnectionFactory:
    __instance = None

    def __init__(self):
        if MySQLConnectionFactory.__instance is not None:
            raise Exception('MySQLConnectionFactory is singleton.')

        MySQLConnectionFactory.__instance = self
        self.con = None

    @staticmethod
    def obtener_instancia():
        if MySQLConnectionFactory.__instance is None:
            MySQLConnectionFactory()

        return MySQLConnectionFactory.__instance

    def abrir_conexion(self):
        self.con = mysql.connector.connect(
            host=dbconfig['conexion']['host'],
            database=dbconfig['conexion']['nombredb'],
            user=dbconfig['conexion']['usuario'],
            password=dbconfig['conexion']['contrasena']
        )

        if not self.con.is_connected():
            return Exception('Unable to make connection to database.')

    def cerrar_conexion(self):
        if self.con is not None:
            self.con.close()

    def ejecutar(self, query):
        if self.con is None:
            raise Exception('no se ha abierto la conexion.')
        cursor = self.con.cursor()
        cursor.execute(query)

        return pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)


def envios_por_anio(anios=None, categoria='t', meses=None, conj_cat=None):
    """
    Consulta todos los envíos realizados en la tabla de hechos de ordenes.

    Los parámetros que especifican la búsqueda son:

    - anios: Cadena con formato 'YYYY-YYYY' que establece el intervalo de
        búsqueda. Por defecto, None busca todos los años
    - Categoría: Determina el detalle de los envíos por categoria. Los
        valores posibles son:
        - 't': Considera el total de los envíos
        - 'c': Desglosa envíos por categoría
        - 's': Lista de constantes con los identificadores de las
            categorías que se desean consultar.
    """
    # Clausulas de restriccion:
    select_clause = ['tiempo.anio']
    joins_clause = ['inner join tiempo on tiempo.IdTiempo = orden.idTiempo']
    where_clause = []
    group_clause = ['tiempo.anio']

    rango_anios = [t for t in anios.split('-') if t] if anios else []
    rango_meses = [m for m in meses.split('-') if m] if meses else []

    # Detalle de tiempo
    if len(rango_anios) == 1:
        anio = int(rango_anios[0])
        select_clause.append('tiempo.mes')
        where_clause.append('tiempo.anio = %d' % anio)

        if len(rango_meses) == 2:
            where_clause.append('tiempo.mes >= %d' % int(rango_meses[0]))
            where_clause.append('tiempo.mes <= %d' % int(rango_meses[1]))
        elif len(rango_meses) == 1:
            where_clause.append('tiempo.mes = %d' % int(rango_meses[0]))
        group_clause.append('tiempo.mes')
    elif len(rango_anios) == 2:
        where_clause.append('tiempo.anio >= %d' % int(rango_anios[0]))
        where_clause.append('tiempo.anio <= %d' % int(rango_anios[1]))
    elif len(rango_anios) != 0:
        raise ValueError(
            'el intervalo del tiempo solo requiere dos parámetros: %s' % str(rango_anios))

    # Detalle de categoria:
    if categoria == 'c' or categoria == 's':
        select_clause.append('categoria.Nombre')
        joins_clause.append(
            'inner join categoria on categoria.IdCategoria = orden.idCategoria')
        group_clause.append('categoria.Nombre')

        if categoria == 's':
            if conj_cat is None:
                raise ValueError(
                    'se debe especificar el conjunto de categorias.')
            where_clause.append(
                'categoria.IdCategoria in ({})'.format(
                    ', '.join([str(c) for c in conj_cat]))
            )
    elif categoria != 't':
        raise ValueError(
            'argumento inválido para categoria: ' + str(categoria))

    select_clause.append('count(*) as total_envios')

    query = 'select {} from {} {}{} group by {}'.format(
        ', '.join(select_clause),
        constants.Tables.ORDEN.value,
        ' '.join(joins_clause),
        ' where {}'.format(' and '.join(where_clause)) if where_clause else '',
        ', '.join(group_clause)
    )

    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    res = conn.ejecutar(query)
    conn.cerrar_conexion()

    return res


def categorias_por_sucursal(tiempo=None, sepcat=False):
    select_clause = ['tiempo.anio', 'sucursal.NombreSucursal']
    joins_clause = ['inner join tiempo on tiempo.IdTiempo = orden.idTiempo',
                    'inner join sucursal on sucursal.IdSucursal = orden.idSucursal']
    where_clause = []
    group_clause = ['tiempo.anio', 'sucursal.IdSucursal']

    if tiempo:
        rango_anios = [t for t in anios.split('-') if t] if anios else []
        # Detalle del tiempo
        if len(rango_anios) == 1:
            anio = int(rango_anios[0])
            where_clause.append('tiempo.anio = %d' % anio)
        elif len(rango_anios) == 2:
            where_clause.append('tiempo.anio >= %d' % int(rango_anios[0]))
            where_clause.append('tiempo.anio <= %d' % int(rango_anios[1]))

    # Detalle de categorías
    if sepcat:
        select_clause.append('categoria.Nombre')
        joins_clause.append(
            'inner join categoria on categoria.IdCategoria = orden.idCategoria')
        group_clause.append('categoria.IdCategoria')

    select_clause.append('sum(orden.cantidad)')
    query = 'select {} from {} {}{} group by {}'.format(
        ', '.join(select_clause),
        constants.Tables.ORDEN.value,
        ' '.join(joins_clause),
        ' where {}'.format(' and '.join(where_clause)) if where_clause else '',
        ', '.join(group_clause)
    )

    print(query)
    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    res = conn.ejecutar(query)
    conn.cerrar_conexion()

    return res


def proveedores_por_antiguedad(cant_prov=0):
    query = '''
    select proveedor.Nombre, min(tiempo.IdTiempo) as primera_orden from orden
    inner join proveedor on proveedor.IdProveedor = orden.idProveedor
    inner join tiempo on tiempo.IdTiempo = orden.idTiempo
    group by proveedor.IdProveedor
    order by primera_orden asc;'''

    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    res = conn.ejecutar(query)
    conn.cerrar_conexion()

    anios = set(res['primera_orden'])
    antiguos = sorted(anios)[:cant_prov]
    print('Imprimiendo de años', antiguos)
    return res[res['primera_orden'].isin(antiguos)]


def productos_por_cantidad(limite=-1, menos_vendidos=False):
    query = '''
    select producto.IdProducto, producto.NombreProducto as nombre, sum(orden.cantidad) as cantidad from orden
    inner join producto on producto.IdProducto = orden.idProducto
    group by producto.IdProducto
    order by sum(orden.cantidad) {}{}'''

    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    res = conn.ejecutar(query.format(
            'asc' if menos_vendidos else 'desc',
            ' limit %d' % limite if limite > 0 else ''
        )
    )
    conn.cerrar_conexion()

    return res
