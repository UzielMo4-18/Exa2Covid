from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.

def homePageView(request):
    return HttpResponse('Prueba del servidor')

'''
class Home(View):
    def get(self,request):
        return render(request,'index.html',{})
        '''