from django.db import models
from django.utils import timezone
from psycopg2 import Time

# Create your models here.
UNIDADES=[("Mz", "Mz"),
          ("Ha", "Ha"),]

class TimeStamped(models.Model):
    creation_date = models.DateTimeField(editable=False, verbose_name="Fecha de creación")
    last_modified = models.DateTimeField(editable=False, verbose_name="Última modificación")

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()

        self.last_modified = timezone.now()
        return super(TimeStamped, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Pais(models.Model):
    idPais=models.CharField(primary_key=True, max_length=15, blank=False, null=False, verbose_name="ID Pais")
    namePais=models.CharField(max_length=64, blank=False, verbose_name="Nombre Pais")
    
    def __str__(self):
        return f"{self.idPais} - {self.namePais}"
class Departamento(models.Model):
    idDpto=models.CharField(primary_key=True, max_length=15, blank=False, null=False, verbose_name="ID Dpto")
    fkPais=models.ForeignKey(Pais, blank=False, related_name="paisDpto", verbose_name="Pais", on_delete=models.CASCADE)
    nameDpto=models.CharField(max_length=64, blank=False, verbose_name="Nombre Dpto")

    def __str__(self):
        return f"{self.nameDpto}"

class Municipio(models.Model):
    idMun=models.CharField(primary_key=True, max_length=15, blank=False, null=False, verbose_name="ID_Municipio")
    fkdpto=models.ForeignKey(Departamento, blank=False, related_name="Departamento", verbose_name="ID_Dpto", on_delete=models.CASCADE)
    nameMun=models.CharField(max_length=64, blank=False, verbose_name="Nombre Municipio")
    
    def __str__(self):
        return f"{self.fkdpto.fkPais.namePais} - {self.fkdpto.nameDpto} - {self.nameMun}"

class Comunidad(models.Model):
    idCom=models.CharField(primary_key=True, max_length=15, blank=False, null=False, verbose_name="ID Comunidad")
    fkMun=models.ForeignKey(Municipio,blank=False, related_name="comunidadMunicipio", on_delete=models.CASCADE )
    nameCom=models.CharField(max_length=64, blank=False, verbose_name="Nombre Comunidad")
    def __str__(self):
        return f"{self.fkMun.nameMun} - {self.nameCom}"

class Productor(TimeStamped):
    idProd = models.BigAutoField(primary_key=True, verbose_name="Productor", auto_created=True)
    fkMun= models.ForeignKey(Municipio,blank=False, related_name="prodMunicipio", on_delete=models.CASCADE )
    firstnameProd= models.CharField(max_length=64, blank=False, verbose_name="fnameProductor")
    lastnameProd=models.CharField(max_length=64, blank=False, verbose_name="lnameProductor")
    fechaNac=models.DateField(null=True)
    estado=models.IntegerField(blank=False, default=1)
    organizacion=models.ForeignKey('autenticacion.Organizacion', on_delete=models.CASCADE, null=True, blank=True, related_name="orgProductor")
    codeProd=models.CharField(max_length=64, blank=True, verbose_name="codeProductor")
    genero=models.CharField(max_length=1, choices=[("M", "Masculino"), ("F", "Femenino")], default="M")
    def __str__(self):
        return f"{self.firstnameProd} {self.lastnameProd}"
    
class Finca(TimeStamped):
    idFinca = models.BigAutoField(primary_key=True, verbose_name="Finca", auto_created=True)
    fkProd=models.ForeignKey(Productor, blank=False, related_name="fincaProductor", on_delete=models.CASCADE)
    fkCom=models.ForeignKey(Comunidad, blank=False, related_name="fincaComunidad", on_delete=models.CASCADE)
    nameFinca=models.CharField(max_length=64, blank=False, verbose_name="nameFinca")
    area=models.FloatField(null=False, blank=False, default=0.0)
    unidad=models.CharField(max_length=4, choices=UNIDADES, default="Mz")
    estado=models.IntegerField(blank=False, default=1)
    def __str__(self):
        return f"{self.fkProd.firstnameProd} {self.fkProd.lastnameProd} - {self.nameFinca} - {self.area}m2."

class Variedad(models.Model):
    nameVariedad=models.CharField(max_length=64, blank=False, verbose_name="TipoCafe")
    def __str__(self):
        return f"{self.nameVariedad}"
class Certificacion(models.Model):
    nameCert=models.CharField(max_length=64, blank=False, verbose_name="Certificación")
    nameImg=models.CharField(max_length=64, blank=False, verbose_name="Imagen")
    def __str__(self):
        return f"{self.nameCert}"
class Lote(TimeStamped):
    idLote = models.BigAutoField(primary_key=True, verbose_name="Lote", auto_created=True)
    nameLote=models.CharField(max_length=64, verbose_name="nameLote")
    fkVar=models.ManyToManyField(Variedad, blank=True, related_name="Variedades")
    fkCert=models.ManyToManyField(Certificacion, blank=True, related_name="Certificaciones")
    fkFinca=models.ForeignKey(Finca,null=True, blank=True, related_name="LoteFinca", verbose_name="Finca", on_delete=models.CASCADE)
    area=models.FloatField(null=False, blank=False, default=0.0)
    unidad=models.CharField(max_length=4, choices=UNIDADES, default="Mz")
    altitud=models.FloatField(null=False, blank=False, default=0.0)
    estado=models.IntegerField(blank=False, default=1)
    
    def __str__(self):
        return f"{self.nameLote} - {self.area} - {self.altitud}"
