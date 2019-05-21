from enum import Enum

class Tables(Enum):
    CATEGORIA = 'categoria'
    ORDEN = 'orden'
    PRODUCTO = 'producto'
    SUCURSAL = 'sucursal'
    TIEMPO = 'tiempo'

class Categorias(Enum):
    ELECTRODOM = 1
    ARTICHOGAR = 2
    DOMESTICOS = 3
    LINEABLANCA = 4
    AUDIOVIDEO = 5
    COMPUTO = 6