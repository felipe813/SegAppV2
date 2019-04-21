from django.utils.safestring import mark_safe
from mapa.dbcontroller import Dbcontroller

def mapa(request):
    dbcontroller = Dbcontroller()
    barrios = dbcontroller.obtenerDatosBarrio()
    denuncias = dbcontroller.obtenerDenunciasPorBarrio()
    ctx = {"barrios": mark_safe(barrios), "denuncias": mark_safe(denuncias)}
    return ctx
