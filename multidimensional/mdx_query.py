"""
Módulo para el acceso a la base de datos multidimensional
"""

import mysql.connector
import pandas as pd

from . import dbconfig


# TODO: Considerar una abstract factory?
class MySQLConnectionFactory:
    __instance = None

    def __init__(self):
        if MySQLConnectionFactory.__instance is not None:
            raise Exception('MySQLConnectionFactory is singleton.')

        MySQLConnectionFactory.__instance = self

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
        self.con.close()

    def ejecutar(self, query):
        cursor = self.con.cursor()
        cursor.execute(query)

        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        print(df)


"""
select tiempo.anio, count(*) from orden
inner join tiempo on tiempo.IdTiempo = orden.idTiempo
group by tiempo.anio
order by anio;
"""

def consultar_envios(anios=None, categoria='t', meses=None, conj_cat=None):

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
        joins_clause.append('inner join categoria on categoria.IdCategoria = orden.idCategoria')
        group_clause.append('categoria.Nombre')

        if categoria == 's':
            where_clause.append('categoria.IdCategoria in (1,2,3,4,5)')
    elif categoria != 't':
        raise ValueError(
            'argumento inválido para categoria: ' + str(categoria))

    select_clause.append('count(*) as total_envios')

    query = 'select {} from orden {}{} group by {}'.format(
        ', '.join(select_clause),
        ' '.join(joins_clause),
        ' where {}'.format(' and '.join(where_clause)) if where_clause else '',
        ', '.join(group_clause)
    )

    conn = MySQLConnectionFactory.obtener_instancia()
    conn.abrir_conexion()
    conn.ejecutar(query)
    conn.cerrar_conexion()
