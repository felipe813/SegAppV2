from mapa.models import CoordenadasPoligono
from django.db import models
from mapa.models import Barrio
from mapa.models import Denuncia
from mapa.models import SectoresBarrio
from mapa.models import Indice
from mapa.models import Delito
from mapa.models import Comentario

class Dbcontroller(object):

    instance = None

    def __new__(cls):
        if not Dbcontroller.instance:
            Dbcontroller.instance = Dbcontroller.__Dbcontroller()
        return Dbcontroller.instance

    def __getattr__(self, __barrios):
        return getattr(self.instance, __barrios)

    def __setattr__(self, __barrios, valor):
        return setattr(self.instance, __barrios, valor)

    class __Dbcontroller:
        def __init__(self):
            self.__barrios = None
            self.__denuncias = {}
            self.__anio_busqueda = 0

        def obtener_datos_barrio(self):
            datos = {}
            j=1
            barrios = self.get_barrios()
            for barrio in barrios:
                datos_barrio = {}
                coordenadas = CoordenadasPoligono.objects.filter(id_barrio=barrio.id_bario)
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
        def obtener_denuncias_por_barrio(self, anio_busqueda):
            self.__anio_busqueda = anio_busqueda
            if self.__anio_busqueda in self.__denuncias:
                return self.__denuncias[self.__anio_busqueda]
            denuncias_ciudad = self.obtener_denuncias_totales()#Debería filtrarse por ciudad
            datos = {}
            existe_indices = self.existe_indices_anio(self.__anio_busqueda)
            if not existe_indices:
                print("Se calculan los indices, no existian")
                datos = self.obtener_denuncias_con_calculo_indices(self.__anio_busqueda, denuncias_ciudad)
            else:
                print("Ya existian los indices, solo se buscan")
                datos = self.obtener_denuncias_sin_calculo_indices()
            datos[0] = self.get_barrios().count()
            self.__denuncias[self.__anio_busqueda] = datos
            print(datos[0])
            return datos

        def obtener_denuncias_con_calculo_indices(self, anio_busqueda, denuncias_ciudad):
            i = 1
            indice_maximo = 0
            indice_minimo = 1
            datos = {}
            barrios = self.get_barrios()
            for barrio in barrios:
                datos_barrio = {}
                datos_barrio[0] = barrio.id_bario
                datos_barrio[1] = barrio.nom_barrio
                datos_barrio[2] = self.obtener_denuncias_barrio(barrio)
                datos_barrio[3] = self.obtener_indice_barrio(barrio, denuncias_ciudad)

                datos_barrio[5] = self.obtener_denuncias_barrio_delito(barrio,1)
                datos_barrio[6] = self.obtener_denuncias_barrio_delito(barrio,2)
                datos_barrio[7] = self.obtener_denuncias_barrio_delito(barrio,3)
                datos_barrio[8] = self.obtener_denuncias_barrio_delito(barrio,5)

                if indice_maximo < datos_barrio[3]:
                    indice_maximo = datos_barrio[3]
                if indice_minimo > datos_barrio[3]:
                    indice_minimo = datos_barrio[3]
                datos[i] = datos_barrio
                i=i+1
            print("El indice minimo es: "+str(indice_minimo))
            print("El indice maximo es: "+str(indice_maximo))
            if indice_maximo>indice_minimo:#Siempre debería entrar
                rango = [indice_minimo, indice_maximo]
                datos = self.calcular_indices(anio_busqueda, datos, rango)
            return datos

        def calcular_indices(self, anio_busqueda, datos, rango):
            i = 1
            indice_minimo = rango[0]
            indice_maximo = rango[1]
            barrios = self.get_barrios()
            for barrio in barrios:
                datos[i][4] = (datos[i][3] - indice_minimo)/(indice_maximo - indice_minimo)
                barrio = Barrio.objects.filter(id_bario=datos[i][0]).first()
                indice_nuevo = Indice(id_barrio = barrio, indice_criminalidad = datos[i][3], indice_color = datos[i][4], anio = anio_busqueda)
                indice_nuevo.save()
                i=i+1
            return datos

        def obtener_denuncias_sin_calculo_indices(self):
            i = 1
            datos = {}
            barrios = self.get_barrios()
            for barrio in barrios:
                datos_barrio = {}
                datos_barrio[0] = barrio.id_bario
                datos_barrio[1] = barrio.nom_barrio
                datos_barrio[2] = self.obtener_denuncias_barrio(barrio)
                indice = Indice.objects.filter(anio=self.__anio_busqueda,id_barrio = barrio.id_bario).first()
                datos_barrio[3] = float(indice.indice_criminalidad)
                datos_barrio[4] = float(indice.indice_color)

                datos_barrio[5] = self.obtener_denuncias_barrio_delito(barrio,Delito.objects.filter(id_delito = 1).first())
                datos_barrio[6] = self.obtener_denuncias_barrio_delito(barrio,Delito.objects.filter(id_delito = 2).first())
                datos_barrio[7] = self.obtener_denuncias_barrio_delito(barrio,Delito.objects.filter(id_delito = 3).first())
                datos_barrio[8] = self.obtener_denuncias_barrio_delito(barrio,Delito.objects.filter(id_delito = 5).first())

                datos[i] = datos_barrio
                i=i+1
            return datos


        def existe_indices_anio(self,anio_buscado):
            cant_indices = Indice.objects.filter(anio=anio_buscado).count()
            cant_barrios = self.get_barrios().count()
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
            rango_fechas = self.__obtener_rango_fechas(self.__anio_busqueda)
            denuncias_totales = Denuncia.objects.filter(fecha_den__range = rango_fechas)
            return denuncias_totales.count()

        def obtener_denuncias_sector(self, sectores):
            denuncias_sector = 0
            for sector in sectores:
                denuncias_barrio = self.obtener_denuncias_barrio(sector.segundo)
                denuncias_sector = denuncias_sector + denuncias_barrio
            return denuncias_sector

        def obtener_sectores_barrio(self, barrio):
            sectores_barrio = SectoresBarrio.objects.filter(foco = barrio.id_bario)
            return sectores_barrio

        def obtener_denuncias_barrio(self, barrio):
            rango_fechas = self.__obtener_rango_fechas(self.__anio_busqueda)
            denuncias_barrio = Denuncia.objects.filter(id_barrio = barrio.id_bario, fecha_den__range = rango_fechas)
            #print("Para el barrio "+barrio.nom_barrio+" se tienen "+ str(denuncias_barrio.count()) +" denuncias\n")
            return denuncias_barrio.count()

        def obtener_denuncias_barrio_delito(self, barrio, delito):
            rango_fechas = self.__obtener_rango_fechas(self.__anio_busqueda)
            denuncias_barrio = Denuncia.objects.filter(id_barrio = barrio.id_bario, fecha_den__range = rango_fechas, id_delito = delito.id_delito)
            return denuncias_barrio.count()

        def get_barrios(self):
            if self.__barrios == None:
                self.__barrios = Barrio.objects.all()
            return self.__barrios

        def ingresar_comentario(self, fecha_comentario, usuario, nombre_barrio, comentario):
            try:
                print("Barrio: "+nombre_barrio)
                barrio = Barrio.objects.filter(nom_barrio=nombre_barrio).first()
                print("ID Barrio: "+barrio.id_bario)
                comentario_nuevo = Comentario(fecha_comentario = fecha_comentario, id_user = usuario, id_barrio = barrio, comentario = comentario)
                comentario_nuevo.save()
                return True
            except:
                print("Error ingresando el usuario")
                return False

        def obtener_comentarios_barrio(self, nombre_barrio):
            try:
                barrio = Barrio.objects.filter(nom_barrio=nombre_barrio).first()
                print("ID Barrio: "+barrio.id_bario)
                comentarios = Comentario.objects.filter(id_barrio = barrio.id_bario)
                datos = {'cantidad':comentarios.count()}
                print("Cantidad de comentarios: "+str(datos['cantidad']))
                i = 0
                for comentario in comentarios:
                    datos[str(i)]={'Fecha':str(comentario.fecha_comentario), 'Usuario':str(comentario.id_user), 'Comentario':str(comentario.comentario)}
                    i = i+1
                return datos
            except:
                return None

        def __obtener_rango_fechas(self, anio_busqueda):
            fecha_min = str(anio_busqueda)+'-01-01'
            fecha_max = str(anio_busqueda)+'-12-31'
            return (fecha_min, fecha_max)
