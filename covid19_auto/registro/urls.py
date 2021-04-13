from django.urls import path
#from . import views
from .views import *

urlpatterns=[
    path('',Home.as_view(),name='index'),
    path('RegistroDatos',Register.as_view(),name='RegistroDatos'),
    path('ListaRegistros',ListaRegistros.as_view(),name='ListaRegistros'),
]