from django.shortcuts import render,redirect
from django.views import View
from .models import Usuario
from .forms import *

# Create your views here.

class Home(View):
    def get(self,request):
        return render(request,'index.html',{})

class Register(View):
    def get(self,request):
        form=FormUsuario()
        context={'form':form}
        return render(request,'Registrar.html',context)

class ListaRegistros(View):
    def get(self,request):
        return render(request,'Lista.html',{})