from django.urls import path
#from . import views
from .views import *

urlpatterns=[
    path('',homePageView,name='home')
    #path('',Home.as_view(),name='index'),
]