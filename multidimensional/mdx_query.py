"""
Módulo para el acceso a la base de datos multidimensional
"""

import datetime
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


def articulos_por_sucursal(sucursal, anios=None, por_cagtegorias=False):
    select_clause = [
        'tiempo.anio', 'sucursal.NombreSucursal as sucursal', 'sum(cantidad) as cantidad']
    joins_clause = [
        'inner join tiempo on tiempo.IdTiempo = orden.idTiempo',
        'inner join sucursal on sucursal.IdSucursal = orden.idSucursal']
    where_clause = ['sucursal.IdSucursal = {}'.format(sucursal)]
    group_clause = ['tiempo.anio']

    rango_anios = [t for t in anios.split('-') if t] if anios else []

    if len(rango_anios) == 1:
        where_clause.append('tiempo.anio = {}'. format(rango_anios[0]))
    elif len(rango_anios) == 2:
        where_clause.append('tiempo.anio >= {} and tiempo.anio <= {}'. format(
            rango_anios[0], rango_anios[1]))

    if por_cagtegorias:
        select_clause.insert(1, 'categoria.Nombre as categoria')
        joins_clause.append(
            'inner join categoria on categoria.IdCategoria = orden.idCategoria')
        group_clause.append('orden.idCategoria')

    query = 'select {} from orden {}{} group by {} order by tiempo.anio asc'.format(
        ', '.join(select_clause),
        ' '.join(joins_clause),
        ' where {}'.format(' and '.join(where_clause)) if where_clause else '',
        ', '.join(group_clause)
    )

    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    res = conn.ejecutar(query)
    conn.cerrar_conexion()

    return res


def pedidos_suc_cuarto_trim(limite=3):
    query = '''
    select orden.idSucursal, sucursal.NombreSucursal, tiempo.anio,
        sum(cantidad) as cantidad_enviada from orden
    inner join tiempo on tiempo.IdTiempo = orden.idTiempo
    inner join sucursal on sucursal.IdSucursal = orden.idSucursal
    where tiempo.trimestre = 4
    group by orden.idSucursal, tiempo.anio
    '''

    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    res = conn.ejecutar(query)
    conn.cerrar_conexion()

    anios = set(res['anio'])
    ultimos_anios = sorted([a for a in anios], reverse=True)[:limite]

    indices = []
    for ua in ultimos_anios:
        cantidad_maxima = max(res[res['anio'] == ua]['cantidad_enviada'])
        indices.extend(res[(res['anio'] == ua) & (
            res['cantidad_enviada'] == cantidad_maxima)].index)

    return res.iloc[indices]


def productos_menos_vendidos_vacaciones(limite=10):
    query = '''
    select tiempo.anio, producto.IdProducto as id, producto.NombreProducto as nombre, sum(orden.cantidad) as cantidad_enviada  from orden
    inner join tiempo on tiempo.IdTiempo = orden.idTiempo
    inner join producto on producto.idCategoria = orden.idCategoria
    where tiempo.trimestre = 3
    group by tiempo.anio, producto.IdProducto'''

    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    res = conn.ejecutar(query)
    conn.cerrar_conexion()

    anios = set(res['anio'])
    ultimos_anios = sorted([i for i in anios])[:limite]

    indices = []
    for a in ultimos_anios:
        cantidad_minima = min(res[res['anio'] == a]['cantidad_enviada'])
        indices.extend(res[(res['anio'] == a) & (
            res['cantidad_enviada'] == cantidad_minima)].index)
    return res.iloc[indices]


def proveedores_por_antiguedad(cant_prov=10):
    query = '''
    select proveedor.IdProveedor, proveedor.Nombre, min(tiempo.IdTiempo)
        as primera_orden from orden
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
    return res[res['primera_orden'].isin(antiguos)]


def productos_por_cantidad(limite=10, periodo='a', menos_vendidos=False):
    query = '''
    select producto.NombreProducto as nombre, tiempo.anio, tiempo.IdTiempo,
        tiempo.mes, tiempo.trimestre, cantidad from orden
    inner join producto on producto.IdProducto = orden.idProducto
    inner join tiempo on tiempo.IdTiempo = orden.idTiempo
    group by producto.IdProducto
    '''

    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    res = conn.ejecutar(query)
    conn.cerrar_conexion()

    fecha = datetime.datetime.now()
    anio = max(res['anio']) - 5

    subdf = res[res['anio'] >= anio]
    nombres = set(subdf['nombre'])
    nombre_cantidad = []
    for n in nombres:
        nombre_cantidad.append(
            (n, sum(subdf[subdf['nombre'] == n]['cantidad'])))

    def l(x): return x[1]
    nombre_cantidad.sort(key=l, reverse=menos_vendidos)
    return nombre_cantidad[:limite]
#
#  CONSULTAS PARA FORMULARIOS
#


def obtener_anios():
    '''Devuelve todos los años disponibles en la BD.'''

    query = 'select distinct anio from tiempo order by anio asc'

    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    res = conn.ejecutar(query)
    conn.cerrar_conexion()

    return [a for a in res['anio']]


def obtener_sucursales():
    '''Devuelve todos las sucrusales disponibles en la BD.'''

    query = 'select IdSucursal, NombreSucursal from sucursal'

    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    res = conn.ejecutar(query)
    conn.cerrar_conexion()

    return [tup for tup in zip(res['IdSucursal'], res['NombreSucursal'])]
