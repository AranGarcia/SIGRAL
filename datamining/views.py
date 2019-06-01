from django.http import HttpResponse
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

    mdx_plot.grafica_productos_por_sucursal(
        mdx_query.articulos_por_sucursal(id_sucursal, anio, por_categoria))

    return HttpResponse(content_type='image/png')


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
