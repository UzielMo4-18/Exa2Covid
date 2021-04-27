from django.shortcuts import render,redirect
from django.views import View
from .models import Usuario
from .forms import *
import datetime,requests

# Create your views here.

class estado(object):
    """docstring for estado"""
    def __init__(self, nombre, ncasos, nrecuperados, nmuertos):
        self.nombre = nombre
        self.ncasos = ncasos
        self.nrecuperados = nrecuperados
        self.nmuertos = nmuertos

class Home(View):
    def get(self,request):
        dia=datetime.date.today()
        NewURL="https://api.covid19tracking.narrativa.com/api/"+str(dia)
        NewURL=NewURL+"/country/mexico"
        list_response=requests.get(NewURL)
        json_response_list=list_response.json()

        estados=json_response_list['dates'][str(dia)]['countries']['Mexico']['regions']
        confirmadosT=json_response_list['total']['today_confirmed']
        recuperadosT=json_response_list['total']['today_recovered']
        muertosT=json_response_list['total']['today_deaths']

        nombresE=[]
        casosE=[]
        recuperadosE=[]
        muertesE=[]
        for states in estados:
            nombresE.append(states['name'])
            casosE.append(states['today_confirmed'])
            try: recuperadosE.append(states['today_recovered'])
            except: recuperadosE.append(0)
            muertesE.append(states['today_deaths'])

        estados.clear()
        for i in range(0,len(casosE)):
            estados.append(estado(nombresE[i],casosE[i],recuperadosE[i],muertesE[i]))

        nombresE.clear()
        casosE.clear()
        recuperadosE.clear()
        muertesE.clear()
        estados.sort(key=lambda st:st.ncasos, reverse=True)
        for st in range(0,10):
            nombresE.append(estados[st].nombre)
            casosE.append(estados[st].ncasos)

        context={'confirmadosT':confirmadosT,'recuperadosT':recuperadosT,'muertosT':muertosT,
            'nombresE':nombresE,'casosE':casosE,'estados':estados}
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