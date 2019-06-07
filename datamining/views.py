import base64
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from multidimensional import mdx_query, mdx_plot

# Create your views here.


def index(request):
    return render(request, 'datamining/index.html')


def formulario(request, form_id):
    if form_id == 1:
        return __cargar_formulario1(request)
    elif form_id == 2:
        return __cargar_formulario2(request)
    elif form_id == 3:
        return __cargar_formulario3(request)
    elif form_id == 4:
        return __cargar_formulario4(request)
    elif form_id == 5:
        return __cargar_formulario5(request)
    else:
        # TODO: 404 reponse
        pass


#############################
# Vistas para consultas MDX #
#############################
def articulos_por_sucursal(request):
    lanio = request.GET['lanio']
    ranio = request.GET['ranio']
    id_sucursal = request.GET['sucursal']
    if 'por_categoria' in request.GET and request.GET['por_categoria'] == 'on':
        por_categoria = True
    else:
        por_categoria = False

    if lanio == ranio:
        anio = lanio
    else:
        anio = '{}-{}'.format(lanio, ranio)

    img_path = mdx_plot.grafica_productos_por_sucursal(
        mdx_query.articulos_por_sucursal(id_sucursal, anio, por_categoria))

    with open(img_path, 'rb') as f:
        img_data = f.read()

    return HttpResponse(base64.b64encode(img_data))


def cuarto_trimestre(request):
    img_path = mdx_plot.grafica_sucursales_cuarto_trimestre(
        mdx_query.pedidos_suc_cuarto_trim())

    with open(img_path, 'rb') as f:
        img_data = f.read()

    return HttpResponse(base64.b64encode(img_data))


def tercer_trimestre(request):
    img_path = mdx_plot.grafica_productos_menos_vendidos(
        mdx_query.productos_menos_vendidos_vacaciones())

    with open(img_path, 'rb') as f:
        img_data = f.read()

    return HttpResponse(base64.b64encode(img_data))


def proveedores_antiguedad(request):
    df = mdx_query.proveedores_por_antiguedad()
    tiempo = sorted([po for po in set(df['primera_orden'])])

    lista_antiguedades = []
    for t in tiempo:
        subdf = df[df['primera_orden'] == t]
        proveedores = ', '.join(map(str, subdf['Nombre']))

        t_cadena = str(t)
        anio = t_cadena[:4]
        mes = t_cadena[4:6]
        dia = t_cadena[6:]
        t_llave = '{}-{}-{}'.format(anio, mes, dia)

        lista_antiguedades.append(
            {
                'fecha': t_llave,
                'proveedor': proveedores
            }
        )

    return JsonResponse(
        {
            'antiguedades': lista_antiguedades
        },
        content_type='application/json;charset=UTF-8'
    )


def demanda_productos(request):
    params = request.GET

    # mes | trimestre | anio
    periodo = params['periodo']
    # mas_demanda | menos_demanda
    tipo = params['tipo']

    menos = False if tipo == 'menos_demanda' else True

    res = mdx_query.productos_por_cantidad(10, menos_vendidos=menos)
    return HttpResponse(
        json.dumps(res),
        content_type='application/json;charset=UTF-8'
    )


def __cargar_formulario1(request):
    anios = mdx_query.obtener_anios()
    sucursales = mdx_query.obtener_sucursales()
    ctx = {
        'anios': anios,
        'sucursales': sucursales
    }

    return render(request, 'datamining/formularios/1.html', ctx)


def __cargar_formulario2(request):
    ctx = {
        'sucursales': mdx_query.obtener_sucursales()
    }

    return render(request, 'datamining/formularios/2.html', ctx)


def __cargar_formulario3(request):
    return render(request, 'datamining/formularios/3.html')


def __cargar_formulario4(request):
    return render(request, 'datamining/formularios/4.html')


def __cargar_formulario5(request):
    return render(request, 'datamining/formularios/5.html')
