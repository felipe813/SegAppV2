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
            operacion=request.POST.get('operacion')
            if operacion == 'ingresarComentario':
                comentario =request.POST.get('comentario')
                barrio = request.POST.get('barrio')
                print("Se guardara el comentario "+ comentario+ " del barrio "+ barrio)
                # AQUI SE DEBE GUARDAR EL COMENTARIO EN LA BASE DE DATOS
                ctx = {"Tipo": operacion,"Datos": "Se ingreso correctamente"}
                return ctx
            if operacion == 'obtenerComentarios':
                barrio = request.POST.get('barrio')
                print("Se obtendran los comentarios del barrio "+ barrio)
                # AQUI SE DEBE CONSULTAR LA LISTA DE COMENTARIOS Y GUARDARLOS EN UNA LISTA
                comentarios = {'cantidad':2,'0':{'Fecha':"13 de abril2",'Usuario':"asanchez2",'Comentario':"Roban celulares y atracan personas en la calle2"},'1':{'Fecha':"13 de abril",'Usuario':"asanchez",'Comentario':"Roban celulares y atracan personas en la calle"}}
                ctx = {"Tipo": operacion,"Datos": comentarios}
                return ctx
        if self.barrios == None:
            self.barrios = self.__dbcontroller.obtener_datos_barrio()
        if self.denuncias == None:
            print("Entra")
            self.denuncias = self.__dbcontroller.obtener_denuncias_por_barrio()
            #print(self.denuncias)
        print(self.denuncias)
        ctx = {"Tipo":"CargueInicial","Datos":{"barrios": mark_safe(self.barrios), "denuncias": mark_safe(self.denuncias)}}
        print("Sale")
        return ctx
