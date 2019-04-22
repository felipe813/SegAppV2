from django.utils.safestring import mark_safe
from mapa.dbcontroller import Dbcontroller

def mapa(request):
    dbcontroller = Dbcontroller()
    barrios = dbcontroller.obtener_datos_barrio()
    denuncias = dbcontroller.obtener_denuncias_por_barrio()
    ctx = {"barrios": mark_safe(barrios), "denuncias": mark_safe(denuncias)}
    return ctx
