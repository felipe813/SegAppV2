from django.utils.safestring import mark_safe
from mapa.dbcontroller import Dbcontroller

class Views():
    def __init__(self):
        self.__dbcontroller = Dbcontroller()

    def mapa(self, request):
        barrios = self.__dbcontroller.obtener_datos_barrio()
        denuncias = self.__dbcontroller.obtener_denuncias_por_barrio()
        ctx = {"barrios": mark_safe(barrios), "denuncias": mark_safe(denuncias)}
        return ctx

#class Views():
#    def __init__(self):
#        self.__dbcontroller = Dbcontroller()
#        self.__ctx_mapa = None

#    def mapa(self, request):
#        if(self.__ctx_mapa == None):
#            barrios = self.__dbcontroller.obtener_datos_barrio()
#            denuncias = self.__dbcontroller.obtener_denuncias_por_barrio()
#            self.__ctx_mapa = {"barrios": mark_safe(barrios), "denuncias": mark_safe(denuncias)}
#        return self.__ctx_mapa
