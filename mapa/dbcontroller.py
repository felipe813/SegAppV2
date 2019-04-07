from mapa.models import Coordenadas_Poligono
from django.db import models
from mapa.models import Barrio

class Dbcontroller():
    def obtenerDatosBarrio(self):
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
