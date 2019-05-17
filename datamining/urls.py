from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('something', views.something, name='something')
]