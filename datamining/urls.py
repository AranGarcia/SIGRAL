from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('formulario/<int:form_id>', views.formulario, name='formulario'),
    # AJAX queries
    path('articulos_por_sucursal/', views.articulos_por_sucursal,
         name='articulos_por_sucursal'),
    path('cuarto_trimestre/', views.cuarto_trimestre, name='cuarto_trimestre'),
    path('tercer_trimestre/', views.tercer_trimestre, name='tercer_trimestre'),
    path('proveedores_antiguedad/', views.proveedores_antiguedad,
         name='proveedores_antiguedad')
]
