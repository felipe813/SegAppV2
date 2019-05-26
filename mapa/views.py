from django.utils.safestring import mark_safe
from mapa.dbcontroller import Dbcontroller
import json
from django.http import HttpResponse



class Views():
    barrios = None
    denuncias = None
    def __init__(self):
        self.__dbcontroller = Dbcontroller()

    
    def mapa(self, request):
        if request.method == 'POST':
            print("POST")
            print(request)
            ctx = {"barrios": "ejemplo"}
            return ctx
            #return HttpResponse(json.dumps('your_data'))
        if self.barrios == None:
            self.barrios = self.__dbcontroller.obtener_datos_barrio()
        if self.denuncias == None:
            print("Entra")
            self.denuncias = self.__dbcontroller.obtener_denuncias_por_barrio()
            #print(self.denuncias)
        ctx = {"barrios": mark_safe(self.barrios), "denuncias": mark_safe(self.denuncias)}
        print("Sale")
        return ctx
