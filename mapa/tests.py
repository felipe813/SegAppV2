from django.test import TestCase

from mapa.models import Pais

class TestPais(TestCase):
    def test_constructor(self):
        pais_nuevo = Pais.objects.create(id_pais = 1, nom_pais = "Colombia")
        pais_nuevo.save()
        self.assertEqual(pais_nuevo.id_pais,1,"No tienen el mismo id")
        self.assertEqual(pais_nuevo.nom_pais,"Colombia","No tienen el mismo nombre")
        pais_nuevo.nombre = "Argentina"
        self.assertEqual(pais_nuevo.nom_pais,"Colombia","Se cambiaron los atributos sin setter, no debe ser posible")
        self.assertTrue(isinstance(pais_nuevo,Pais),"No es un ejemplar de Pais")
        self.assertEqual(pais_nuevo._unicode_(),pais_nuevo.nom_pais,"El unicode nos es el nombre del país")
        pais_consulta = Pais.objects.filter(id_pais=1).first()
        self.assertEqual(pais_nuevo,pais_consulta,"No se encontró en base de datos")
