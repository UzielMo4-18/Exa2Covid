from django.shortcuts import render,redirect
from django.views import View
from .models import Usuario
from .forms import *
import datetime,requests

# Create your views here.

class Home(View):
    def get(self,request):
        dia=datetime.date.today()
        NewURL="https://api.covid19tracking.narrativa.com/api/"+str(dia)
        NewURL=NewURL+"/country/mexico"
        list_response=requests.get(NewURL)
        json_response_list=list_response.json()

        resultados=json_response_list['total']
        confirmados=json_response_list['total']['today_confirmed']
        recuperados=json_response_list['total']['today_recovered']
        muertos=json_response_list['total']['today_deaths']
        context={'confirmados':confirmados,'recuperados':recuperados,'muertos':muertos}
        print(confirmados)
        print(context)
        return render(request,'index.html',context)

class Register(View):
    def get(self,request):
        form=FormUsuario()
        context={'form':form}
        return render(request,'Registrar.html',context)

    def post(self,request):
        form=FormUsuario(request.POST)
        if form.is_valid():
            registro=form.save(commit=False)
            usuarios=Usuario.objects.filter(correo=registro.correo,timestamp__gte=datetime.date.today())
            print(usuarios)
            if usuarios: print("Ya realizó su registro diario, vuelva mañana")
            else:
                print("Datos registrados exitosamente")
                if registro.temperatura>37.5 or registro.oxigenacion<90:
                    registro.positivo=True
                    registro.save()
                    return redirect('Aviso')
                else:
                    registro.save()
                    return redirect('index')
        else:
            context={'form':form}
            return render(request,'Registrar.html',context)

class ListaRegistros(View):
    def get(self,request):
        usuarios=Usuario.objects.all()
        context={'usuarios':usuarios}
        return render(request,'Lista.html',context)

class MsgAviso(View):
    def get(self,request):
        return render(request,'Aviso.html',{})