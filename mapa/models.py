from django.db import models


class Pais(models.Model):
    id_pais = models.IntegerField(primary_key=True)
    nom_pais = models.CharField(max_length=30)
   
    def _unicode_(self):
        return self.nom_pais

class Departamento(models.Model):
    id_dpto = models.CharField(max_length=10, primary_key=True)
    nom_dpto = models.CharField(max_length=50)
    id_pais = models.IntegerField()
    '''id_pais = models.ForeignKey(Pais, on_delete=models.PROTECT)'''
   
    def _unicode_(self):
        return self.nom_dpto

class Municipio(models.Model):
    id_muni = models.CharField(max_length=10, primary_key=True)
    nom_muni = models.CharField(max_length=50)
    id_dpto = models.ForeignKey(Departamento, on_delete=models.PROTECT)
   
    def _unicode_(self):
        return self.nom_muni


class Zona(models.Model):
    id_zona = models.IntegerField( primary_key=True)
    nom_zona = models.CharField(max_length=10)
   
    def _unicode_(self):
        return self.nom_zona

class Barrio(models.Model):
    id_bario = models.CharField(max_length=10, primary_key=True)
    nom_barrio = models.CharField(max_length=50)
    id_zona = models.ForeignKey(Zona, on_delete=models.PROTECT)
    id_municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
   
    def _unicode_(self):
        return self.nom_barrio


class Arma(models.Model):
    id_arma = models.IntegerField( primary_key=True)
    nom_arma = models.CharField(max_length=30)
   
    def _unicode_(self):
        return self.nom_arma



class Movil(models.Model):
    id_movil = models.IntegerField( primary_key=True)
    nom_movil = models.CharField(max_length=30)
   
    def _unicode_(self):
        return self.nom_movil

class Estado_Civil(models.Model):
    id_est_civ = models.IntegerField( primary_key=True)
    nom_est_civ = models.CharField(max_length=20)
   
    def _unicode_(self):
        return self.nom_est_civ

class Pais(models.Model):
    id_pais = models.IntegerField( primary_key=True)
    nom_pais = models.CharField(max_length=30)
   
    def _unicode_(self):
        return self.nom_pais

class Empleado(models.Model):
    id_empleado = models.IntegerField( primary_key=True)
    nom_empleado = models.CharField(max_length=30)
   
    def _unicode_(self):
        return self.nom_empleado

class Profesion(models.Model):
    id_profesion = models.IntegerField( primary_key=True)
    nom_profesion = models.CharField(max_length=30)
   
    def _unicode_(self):
        return self.nom_profesion

class Escolaridad(models.Model):
    id_escolaridad = models.IntegerField( primary_key=True)
    nom_escolaridad = models.CharField(max_length=30)
   
    def _unicode_(self):
        return self.nom_escolaridad

class Sitio(models.Model):
    id_sitio = models.IntegerField( primary_key=True)
    nom_sitio = models.CharField(max_length=50)
   
    def _unicode_(self):
        return self.nom_sitio

class Coordenadas_Poligono(models.Model):
    id_barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT)
    latitud = models.CharField(max_length=20)
    longitud = models.CharField(max_length=20)
    id_coor_poli = models.BigIntegerField(primary_key=True)

    def _unicode_(self):
        return self.latitud + " - " +self.longitud
 
class Denuncia(models.Model):
    fecha_den = models.DateField()
    hora_den = models.TimeField()
    id_barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT)
    id_sitio = models.ForeignKey(Sitio, on_delete=models.PROTECT)
    id_arma = models.ForeignKey(Arma, on_delete=models.PROTECT)
    id_mov_agr = models.ForeignKey(Movil, on_delete=models.PROTECT,related_name='movil_agresor')
    id_mov_vic = models.ForeignKey(Movil, on_delete=models.PROTECT,related_name='movil_victima')
    edad = models.IntegerField()
    sexo_vic = models.CharField(max_length=10)
    id_est_civ = models.ForeignKey(Estado_Civil, on_delete=models.PROTECT)
    id_pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    id_empleado_vic = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    id_profesion = models.ForeignKey(Profesion, on_delete=models.PROTECT)
    id_escolaridad = models.ForeignKey(Escolaridad, on_delete=models.PROTECT)
    cantdiad_vic = models.IntegerField() 
    

    
    