from mapa.models import Coordenadas_Poligono
from django.db import models
from mapa.models import Barrio
from mapa.models import Denuncia
from mapa.models import Sectores_Barrio

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
        denuncias_ciudad = self.obtener_denuncias_totales()#Debería filtrarse por ciudad
        datos = {}
        i = 1
        for barrio in barrios:
            datos_barrio = {}
            datos_barrio[0] = barrio.id_bario
            datos_barrio[1] = barrio.nom_barrio
            datos_barrio[2] = self.obtener_denuncias_barrio(barrio)
            datos_barrio[3] = self.obtener_indice_barrio(barrio,denuncias_ciudad)
            datos[i] = datos_barrio
            i=i+1
        datos[0] = barrios.count()
        return datos

    def obtener_indice_barrio(self,barrio,denuncias_ciudad):
        sectores_barrio = self.obtener_sectores_barrio(barrio)
        denuncias_sector = self.obtener_denuncias_sector(sectores_barrio)
        denuncias_barrio = self.obtener_denuncias_barrio(barrio)
        if((denuncias_sector+denuncias_barrio)==0):
            return 0
        else:
            indice_barrio = (denuncias_barrio/(denuncias_sector+denuncias_barrio) + (denuncias_sector+denuncias_barrio)/denuncias_ciudad)/2
            return indice_barrio

    def obtener_denuncias_totales(self):
        denuncias_totales = Denuncia.objects.all()
        return denuncias_totales.count()

    def obtener_denuncias_sector(self, sectores):
        denuncias_sector = 0
        for sector in sectores:
            denuncias_barrio = self.obtener_denuncias_barrio(sector.segundo)
            denuncias_sector = denuncias_sector + denuncias_barrio
        return denuncias_sector

    def obtener_sectores_barrio(self, barrio):
        sectores_barrio = Sectores_Barrio.objects.filter(foco = barrio.id_bario)
        return sectores_barrio

    def obtener_denuncias_barrio(self, barrio):
        denuncias_barrio = Denuncia.objects.filter(id_barrio = barrio.id_bario)
        return denuncias_barrio.count()
