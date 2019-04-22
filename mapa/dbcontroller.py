from mapa.models import Coordenadas_Poligono
from django.db import models
from mapa.models import Barrio
from mapa.models import Denuncia

class Dbcontroller():
    def obtener_datos_barrio(self):
        barrios = Barrio.objects.all()
        datos = {}
        j=1
        for barrio in barrios:
            datos_barrio = {}
            coordenadas = Coordenadas_Poligono.objects.filter(id_barrio=barrio.id_bario)
            i=2
            #print(barrio.nom_barrio)
            for list in coordenadas:
                datos_barrio[i]=[float(list.latitud),float(list.longitud)]
                i=i+1
            datos_barrio[0]=coordenadas.count()
            datos_barrio[1] = float(barrio.id_bario)
            datos[j]=datos_barrio
            j=j+1
        datos[0]=barrios.count()
        return datos

    #-- Obtiene la cantidad de denuncias por barrio --#
    #-- Retorna un arreglo de la siguiente forma --#
    #-- Posición 0: Cantidad total de barrios (n) --#
    #-- Posición 1 a n: Por cada barrio se tiene un arreglo con
    #-- el id del barrio, el nombre del barrio y la cantidad de denuncias por barrio --#
    def obtener_denuncias_por_barrio(self):
        barrios = Barrio.objects.all()
        datos = {}
        i = 1
        for barrio in barrios:
            denuncias_por_barrio = Denuncia.objects.filter(id_barrio = barrio.id_bario)
            datos_barrio = {}
            datos_barrio[0] = barrio.id_bario
            datos_barrio[1] = barrio.nom_barrio
            datos_barrio[2] = denuncias_por_barrio.count()
            datos[i] = datos_barrio
            i=i+1
        datos[0] = barrios.count()
        return datos
