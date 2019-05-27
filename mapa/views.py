from django.utils.safestring import mark_safe
from mapa.dbcontroller import Dbcontroller
import json
import datetime
from django.utils.timezone import utc

from django.http import HttpResponse



class Views():
    barrios = None
    denuncias = {'2016':None,'2017':None,'2018':None,'2019':None}
    def __init__(self):
        self.__dbcontroller = Dbcontroller()


    def mapa(self, request):
        print('Entro a mapa' + request.method)
        if request.method == 'POST':
            operacion=request.POST.get('operacion')
            if operacion == 'ingresarComentario':
                comentario =request.POST.get('comentario')
                barrio = request.POST.get('barrio')
                usuario = request.user
                fecha_comentario = datetime.datetime.utcnow().replace(tzinfo=utc)
                #fecha_comentario = datetime.strptime(fecha_comentario, "%a, %d %b %Y %H:%M:%S %z")
                print("Se guardara el comentario "+ comentario+ " del barrio "+ barrio)
                # AQUI SE DEBE GUARDAR EL COMENTARIO EN LA BASE DE DATOS
                resultado = self.__dbcontroller.ingresar_comentario(fecha_comentario, usuario, barrio, comentario)
                salida = "Error al ingresar el comentario"
                if(resultado):
                    salida = "Comentario ingresado correctamente"
                ctx = {"Tipo": operacion,"Datos": resultado}
                return ctx
            if operacion == 'obtenerComentarios':
                barrio = request.POST.get('barrio')
                print("Se obtendran los comentarios del barrio "+ barrio)
                # AQUI SE DEBE CONSULTAR LA LISTA DE COMENTARIOS Y GUARDARLOS EN UNA LISTA
                comentarios = self.__dbcontroller.obtener_comentarios_barrio(barrio)
                ##comentarios = {'cantidad':2,'0':{'Fecha':"13 de abril2",'Usuario':"asanchez2",'Comentario':"Roban celulares y atracan personas en la calle2"},'1':{'Fecha':"13 de abril",'Usuario':"asanchez",'Comentario':"Roban celulares y atracan personas en la calle"}}
                ctx = {"Tipo": operacion,"Datos": comentarios}
                return ctx
        if self.barrios == None:
            self.barrios = self.__dbcontroller.obtener_datos_barrio()
        anio =request.GET.get('anio')
        
        if anio==None:
            anio='2018'
        print('El año de busqueda es '+str(anio))
        if self.denuncias[anio] == None:
            print("Entra a buscar")
            self.denuncias[anio] = self.__dbcontroller.obtener_denuncias_por_barrio(anio)
        print(self.denuncias[anio])
        ctx = {"Tipo":"CargueInicial","Datos":{"barrios": mark_safe(self.barrios), "denuncias": mark_safe(self.denuncias[anio])}}
        print("Sale")
        return ctx
