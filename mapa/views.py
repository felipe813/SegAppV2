from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from mapa.dbcontroller import Dbcontroller

def index(request):
    dbcontroller = Dbcontroller()
    barrios = dbcontroller.obtenerDatosBarrio()
    denuncias = dbcontroller.obtenerDenunciasPorBarrio()
    ctx = {"barrios": mark_safe(barrios), "denuncias": mark_safe(denuncias)}
    return render(request,'mapa.html',ctx)
