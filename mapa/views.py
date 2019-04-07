from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from mapa.dbcontroller import Dbcontroller

def index(request):
    dbcontroller = Dbcontroller()
    datos = dbcontroller.obtenerDatosBarrio()
    ctx = {"datos": datos}
    return render(request,'mapa.html',ctx)
