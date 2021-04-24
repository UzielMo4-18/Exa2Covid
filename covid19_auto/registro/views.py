from django.shortcuts import render,redirect
from django.views import View
from .models import Usuario
from .forms import *
import datetime,requests

# Create your views here.

class estado(object):
    """docstring for estado"""
    def __init__(self, nombre, ncasos):#, nrecuperados, nmuertos):
        self.nombre = nombre
        self.ncasos = ncasos
        #self.nrecuperados = nrecuperados
        #self.nmuertos = nmuertos

    def info_estado(self):
        print("Nombre del estado:",self.nombre)
        print("Casos totales a la fecha:",self.ncasos,"\n")

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
        states_array=[]
        for states in estados:
            if states['name']: nombresE.append(states['name'])
            if states['today_confirmed']: casosE.append(states['today_confirmed'])
            #if states['today_deaths']: muertesE.append(states['today_deaths'])
            #if states['today_recovered']: recuperadosE.append(states['today_recovered'])

        for i in range(0,len(casosE)):
            est=estado(nombresE[i],casosE[i])#,recuperadosE[i],muertesE[i])
            states_array.append(est)

        nombresE.clear()
        casosE.clear()
        states_array.sort(key=lambda st:st.ncasos, reverse=True)
        for st in range(0,10):
            nombresE.append(states_array[st].nombre)
            casosE.append(states_array[st].ncasos)
            #recuperadosE.append(states_array[st].nrecuperados)
            #muertesE.append(states_array[st].nmuertos)
        #print("Top 10 estados con más casos\n")
        #print(nombres)
        #print(casos)
        #for st in range(0,10):
            #print("Nombre del estado:",nombres[st])
            #print("Casos del estado:",casos[st],"\n")

        context={'confirmadosT':confirmadosT,'recuperadosT':recuperadosT,
            'muertosT':muertosT,'nombresE':nombresE,'casosE':casosE}#,'recuperadosE':recuperadosE,
            #'muertesE':muertesE}
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