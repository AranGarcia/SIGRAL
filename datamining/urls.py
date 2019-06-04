from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('formulario/<int:form_id>', views.formulario, name='formulario'),
    # AJAX queries
    path('articulos_por_sucursal/', views.articulos_por_sucursal,
         name='articulos_por_sucursal'),
    path('tercer_trimestre/', views.tercer_trimestre, name='tercer_trimestre')
]
