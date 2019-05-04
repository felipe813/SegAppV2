from mapa.models import Coordenadas_Poligono
from django.db import models
from mapa.models import Barrio
from mapa.models import Denuncia
from mapa.models import Sectores_Barrio
from mapa.models import Indice

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
        anio_busqueda = 2017
        barrios = Barrio.objects.all()
        denuncias_ciudad = self.obtener_denuncias_totales()#Debería filtrarse por ciudad
        datos = {}
        i = 1
        indice_maximo = 0
        indice_minimo = 1
        existe_indices = self.existe_indices_anio(anio_busqueda)
        if not existe_indices:
            print("Se calculan los indices, no existian")
        else:
            print("Ya existian los indices, solo se buscan")
        for barrio in barrios:
            datos_barrio = {}
            datos_barrio[0] = barrio.id_bario
            datos_barrio[1] = barrio.nom_barrio
            datos_barrio[2] = self.obtener_denuncias_barrio(barrio)

            if not existe_indices:
                datos_barrio[3] = self.obtener_indice_barrio(barrio,denuncias_ciudad)
                if indice_maximo < datos_barrio[3]:
                    indice_maximo = datos_barrio[3]
                if indice_minimo > datos_barrio[3]:
                    indice_minimo = datos_barrio[3]
            else:
                indice = Indice.objects.filter(anio=anio_busqueda,id_barrio = barrio.id_bario).first()
                datos_barrio[3] = float(indice.indice_criminalidad)
                datos_barrio[4] = float(indice.indice_color)
                #print(datos_barrio[3],"  -  ",datos_barrio[4])

            datos[i] = datos_barrio
            i=i+1
        print("El indice minimo es: "+str(indice_minimo))
        print("El indice maximo es: "+str(indice_maximo))
        if not existe_indices:
            print("Se guardan los indices")
            i = 1
            if indice_maximo>indice_minimo:#Siempre debería entrar
                for barrio in barrios:
                    datos[i][4] = (datos[i][3] - indice_minimo)/(indice_maximo - indice_minimo)
                    indice_nuevo = Indice(id_barrio = barrio ,indice_criminalidad = datos[i][3] ,indice_color = datos[i][4],anio = anio_busqueda)
                    indice_nuevo.save()
                    i=i+1

        datos[0] = barrios.count()
        print(datos[0])
        return datos

    

    def existe_indices_anio(self,anio_buscado):
        cant_indices = Indice.objects.filter(anio=anio_buscado).count()
        cant_barrios = Barrio.objects.all().count()
        print(cant_indices)
        print(cant_barrios)
        return cant_barrios==cant_indices

    def obtener_indice_barrio(self,barrio,denuncias_ciudad):
        sectores_barrio = self.obtener_sectores_barrio(barrio)
        denuncias_sector = self.obtener_denuncias_sector(sectores_barrio)
        denuncias_barrio = self.obtener_denuncias_barrio(barrio)
        if(denuncias_barrio==0):
            indice_barrio = denuncias_sector/denuncias_ciudad
        else:
            indice_barrio = 0.25*(denuncias_barrio)/(denuncias_sector+denuncias_barrio) + 0.75*(denuncias_sector+denuncias_barrio)/(denuncias_ciudad)
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
