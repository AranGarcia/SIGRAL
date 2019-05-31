from django.shortcuts import render

from multidimensional import mdx_query

# Create your views here.


def index(request):
    return render(request, 'datamining/index.html')


def dashboard(request):
    return render(request, 'datamining/dashboard.html')


def formulario(request, form_id):
    if form_id == 1:
        return __cargar_formulario1(request)


def __cargar_formulario1(request):
    anios = mdx_query.obtener_anios()
    sucursales = mdx_query.obtener_sucursales()
    ctx = {
        'anios': anios,
        'sucursales': sucursales
    }

    return render(request, 'datamining/formularios/1.html', ctx)
