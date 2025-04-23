from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from registros.models import Municipio, TimeStamped
from jsignature.fields import JSignatureField
# Create your models here.

TIPOSORG=[
    (1, 'Cooperativa'),
    (2, 'Laboratorio'),
    (3, 'Adminstración'),
]

TIPOSUSER=[
    (1, 'Administrador'),
    (2, 'Jefe de Laboratorio'),
    (3, 'Digitador de Laboratorio'),
    (4, 'Analista de Laboratorio'),
    (5, 'Jefe de Cooperativa'),
    (6, 'Digitador de Cooperativa'),
    (7, 'Analista de Cooperativa'),
    (8, 'Hibrido Cooperativa'),

]
class Sede(TimeStamped):
    id_sede = models.CharField(primary_key=True, max_length=15)
    name_sede= models.CharField(max_length=64, blank=False)
    ubicacion = models.ForeignKey(Municipio, blank=False, related_name="sedeMunicipio", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.id_sede} - {self.name_sede}"
class Organizacion(TimeStamped):
    id_org = models.CharField(primary_key=True, max_length=15)
    name_org= models.CharField(max_length=64, blank=False)
    tipo_org=models.IntegerField(blank=False, choices=TIPOSORG, default=1)
    ubicacion = models.ForeignKey(Municipio, blank=False, related_name="orgMunicipio", on_delete=models.CASCADE, null=True)
    nameLogo=models.CharField(max_length=64, blank=True, null=True, verbose_name="Nombre del logo")
    sedes=models.ManyToManyField(Sede, blank=True, related_name="sedeOrg")

    def __str__(self):
        return f"{self.id_org} - {self.name_org}"

class Colaborador(TimeStamped):
    usuario=models.OneToOneField(settings.AUTH_USER_MODEL, related_name="colaborador", on_delete=models.CASCADE)
    org=models.ForeignKey(Organizacion, blank=False, related_name="organizacionColab", on_delete=models.CASCADE)
    tipoUser=models.IntegerField(blank=False, choices=TIPOSUSER, default=4)
    firma=JSignatureField(blank=True, null=True)

    def is_boss(self):
        u=self
        if User.objects.filter(username=u.usuario.username, groups__name="Jefe").exists():
            return True
        return False
    def is_siteadmin(self):
        u=self
        if User.objects.filter(username=u.usuario.username, groups__name="Administrador").exists():
            return True
        return False      

    def groupname(self):
        u=self
        if User.objects.filter(username=u.usuario.username, groups__name="Tecnico").exists():
            return "Tecnico"
        elif User.objects.filter(username=u.usuario.username, groups__name="Administrador").exists():
            return "Administrador"
        else:
            return "Miembro"
    def __str__(self):
        return f"{self.usuario}-{self.org}"
