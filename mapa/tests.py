from django.test import TestCase

from mapa.models import Pais, Departamento, Municipio, Zona, Barrio, Indice, Arma, Movil
from mapa.dbcontroller import Dbcontroller

class TestModelos(TestCase):
    def test_crear_pais(self):
        pais_nuevo = Pais.objects.create(id_pais = 1, nom_pais = "Colombia")
        pais_nuevo.save()
        self.assertEqual(pais_nuevo.id_pais,1,"No tienen el mismo id")
        self.assertEqual(pais_nuevo.nom_pais,"Colombia","No tienen el mismo nombre")
        pais_nuevo.nom_pais = "Argentina"
        self.assertEqual(pais_nuevo.nom_pais,"Argentina","No se cambiaron los atributos")
        self.assertTrue(isinstance(pais_nuevo,Pais),"No es un ejemplar de Pais")
        self.assertEqual(pais_nuevo._unicode_(),pais_nuevo.nom_pais,"El unicode no es el nombre del país")
        pais_consulta = Pais.objects.filter(id_pais=1).first()
        self.assertEqual(pais_nuevo,pais_consulta,"No se encontró en base de datos")
        return pais_nuevo

    def test_crear_dpto(self):
        pais_nuevo = self.test_crear_pais()
        dpto_nuevo = Departamento.objects.create(id_dpto = 1, nom_dpto = "Tolima", id_pais = pais_nuevo.id_pais)
        dpto_nuevo.save()
        self.assertEqual(dpto_nuevo.id_pais,pais_nuevo.id_pais,"No tiene el mismo id del país")
        self.assertEqual(dpto_nuevo.nom_dpto,"Tolima","No tienen el mismo nombre")
        dpto_nuevo.nom_dpto = "Cundinamarca"
        self.assertEqual(dpto_nuevo.nom_dpto,"Cundinamarca","No se cambiaron los atributos")
        self.assertTrue(isinstance(dpto_nuevo,Departamento),"No es un ejemplar de Departamento")
        self.assertEqual(dpto_nuevo._unicode_(),dpto_nuevo.nom_dpto,"El unicode no es el nombre del departamento")
        return dpto_nuevo

    def test_crear_municipio(self):
        dpto_nuevo = self.test_crear_dpto()
        municipio_nuevo = Municipio.objects.create(id_muni = 1, nom_muni = "Ibagué", id_dpto = dpto_nuevo)
        municipio_nuevo.save()
        self.assertEqual(municipio_nuevo.id_dpto,dpto_nuevo,"No tiene el mismo id del departamento")
        self.assertEqual(municipio_nuevo.nom_muni,"Ibagué","No tienen el mismo nombre")
        municipio_nuevo.nom_muni = "Bogotá"
        self.assertEqual(municipio_nuevo.nom_muni,"Bogotá","No se cambiaron los atributos")
        self.assertTrue(isinstance(municipio_nuevo,Municipio),"No es un ejemplar de Municipio")
        self.assertEqual(municipio_nuevo._unicode_(),municipio_nuevo.nom_muni,"El unicode no es el nombre del municipio")
        return municipio_nuevo

    def test_crear_zona(self):
        zona = Zona.objects.create(id_zona = 1, nom_zona = "Zona")
        zona.save()
        self.assertEqual(zona.nom_zona,"Zona","No tienen el mismo nombre")
        zona.nom_zona = "Zona2"
        self.assertEqual(zona.nom_zona,"Zona2","No se cambiaron los atributos")
        self.assertTrue(isinstance(zona,Zona),"No es un ejemplar de la clase Zona")
        self.assertEqual(zona._unicode_(),zona.nom_zona,"El unicode no es el nombre")
        return zona

    def test_crear_barrio(self):
        zona = self.test_crear_zona()
        municipio = self.test_crear_municipio()
        barrio = Barrio.objects.create(id_bario = '1', nom_barrio = "Quirigua", id_zona = zona, id_municipio = municipio)
        barrio.save()
        self.assertEqual(barrio.nom_barrio,"Quirigua","No tienen el mismo nombre")
        barrio.nom_barrio = "Galán"
        self.assertEqual(barrio.nom_barrio,"Galán","No se cambiaron los atributos")
        self.assertTrue(isinstance(barrio,Barrio),"No es un ejemplar de la clase Barrio")
        self.assertEqual(barrio._unicode_(),barrio.nom_barrio,"El unicode no es el nombre")
        return barrio

    def test_crear_indice(self):
        barrio = self.test_crear_barrio()
        indice = Indice.objects.create(id_barrio = barrio, indice_criminalidad = 0.27, indice_color = 1, anio = 2017)
        indice.save()
        self.assertEqual(indice.indice_criminalidad,0.27,"No tienen el mismo indice")
        indice.indice_criminalidad = 0
        self.assertEqual(indice.indice_criminalidad,0,"No se cambiaron los atributos")
        self.assertTrue(isinstance(indice,Indice),"No es un ejemplar de la clase Indice")
        self.assertEqual(indice._unicode_(),indice.indice_criminalidad,"El unicode no es el índice de criminalidad")
        return indice

    def test_crear_arma(self):
        arma = Arma.objects.create(id_arma = 1, nom_arma = "Arma1")
        arma.save()
        self.assertEqual(arma.nom_arma,"Arma1","No tienen el mismo nombre")
        arma.nom_arma = "Arma2"
        self.assertEqual(arma.nom_arma,"Arma2","No se cambiaron los atributos")
        self.assertTrue(isinstance(arma,Arma),"No es un ejemplar de la clase Arma")
        self.assertEqual(arma._unicode_(),arma.nom_arma,"El unicode no es el nombre")
        return arma

    def test_crear_movil(self):
        movil = Movil.objects.create(id_movil = 1, nom_movil = "Movil1")
        movil.save()
        self.assertEqual(movil.nom_movil,"Movil1","No tienen el mismo nombre")
        movil.nom_movil = "Movil2"
        self.assertEqual(movil.nom_movil,"Movil2","No se cambiaron los atributos")
        self.assertTrue(isinstance(movil,Movil),"No es un ejemplar de la clase Movil")
        self.assertEqual(movil._unicode_(),movil.nom_movil,"El unicode no es el nombre")
        return movil

class TestBdController(TestCase):
    def test_crear_controlador(self):
        dbcontroller = Dbcontroller()
        #self.assertTrue(isinstance(dbcontroller,Dbcontroller.__dbcontroller),"No es un ejemplar de la clase Dbcontroller")
        t = TestModelos()
        t.test_crear_indice()
        dbcontroller.obtener_datos_barrio()
        dbcontroller.get_barrios()
        dbcontroller2 = Dbcontroller()
        self.assertEqual(dbcontroller,dbcontroller2,"Hay dos ejemplares distintos de Dbcontroller")
    def test_obtener_denuncias_por_barrio():
        dbcontroller = Dbcontroller()
        t = TestModelos()
        t.test_crear_indice()
        denuncias_sin_indices = dbcontroller.obtener_denuncias_por_barrio()
        denuncias_con_indices = dbcontroller.obtener_denuncias_por_barrio()
        self.assertEqual(denuncias_sin_indices,denuncias_con_indices,"Los resultados son distintos al no haber índices")
    def test_obtener_barrios():
        dbcontroller = Dbcontroller()
        t = TestModelos()
        barrio = t.test_crear_barrio()
        barrios = dbcontroller.get_barrios()
        self.assertTrue(barrio in barrios,"No es un ejemplar de la clase Dbcontroller")
