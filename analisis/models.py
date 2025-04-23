from django.db import models
from registros.models import *
from autenticacion.models import *
from multiselectfield import MultiSelectField
# Create your models here.
PESOS=[
    ("100", "100"),
    ("300", "300"),
    ("350", "350"),
    ("500", "500"),
]

NIVELES=[
    (1, "Nivel 1"),
    (2, "Nivel 2"),
    (3, "Nivel 3"),
    (4, "Nivel 4"),
]

TUESTE=[(3,"Alto"),(2, "Medio"),(1, "Bajo"),]
MOLIENDA=[(3,"Alto"),(2, "Medio"),(1, "Bajo"),]
INTENSIDAD=[(3,"Alto"),(2, "Medio"),(1, "Bajo"),]
oAnalisis=[(1,"Seguimiento Cooperativa"),(2, "Concurso"),(3, "Solicitud del Productor"),(4, "Solicitud del Comprador"),]
TipoMuestra=[(1,"Cafe Pergamino"),(2, "Cafe Oro")]
Caracteristicas=[(1,"Derrame"),(2, "Olor no característico"),(3, "Empaque roto"),(4, "Buen estado"),] ##RESOLVER ESTE PROBLEMA PRONTO
Procesado=[(1,"Lavado"),(2, "Natural"),(3, "Honey"),]
Procesos=[(1,"Fisico"),(2, "Sensorial"), (3, "Ambos")]
Ciclo=[(1,"2019-2020"),(2,"2020-2021"),(3,"2021-2022")]

class Estado(models.IntegerChoices):
    COMPLETADA=1, "Completado"
    PENDIENTEAMBOS=2, "Pendiente Ambos"
    PENDIENTEFISICO=3, "Pendiente Fisico"
    PENDIENTESENSORIAL=4, "Pendiente Sensorial"
    PENDIENTECONCILIACION=5, "Pendiente Conciliacion"
    CONCILIADA=6, "Conciliada"
    CANCELADA=7, "Cancelada"
    PENDIENTE=8, "Pendiente"
    RECHAZADA=9, "Rechazada"
    FISICOLISTO=10, "Fisico Listo"
    SENSORIALLISTO=11, "Sensorial Listo"
    AMBOSLISTO=12, "Ambos Listo"

class Muestra(TimeStamped):
    idMuestra=models.BigAutoField(primary_key=True, verbose_name="Lote", auto_created=True)
    fkLote=models.ForeignKey(Lote, blank=False, related_name="Muestras", verbose_name="Lote", on_delete=models.CASCADE)
    fechaEntrega=models.DateField(null=False)
    peso=models.CharField(max_length=4, choices=PESOS, default="100")
    tipo=models.IntegerField(choices=TipoMuestra, verbose_name="Tipo de Muestra", blank=False)
    caracteristicas=MultiSelectField(choices=Caracteristicas, verbose_name="Caracteristicas", blank=False)
    rMuestra=models.IntegerField(blank=False, default=0)
    procesos=models.IntegerField(blank=False, choices=Procesos, verbose_name="Procesos a aplicar")
    procesado=models.IntegerField(choices=Procesado, verbose_name="Procesado", blank=False, default=2)
    ciclo=models.IntegerField(choices=Ciclo, verbose_name="Ciclo", blank=True, null=True)
    observaciones=models.TextField(max_length=254, blank=True, verbose_name="Observaciones")
    estado=models.IntegerField(choices=Estado.choices, default=2)
    repetir=models.BooleanField(default=False)
    fkOrg=models.ForeignKey(Organizacion, blank=True, null=True, related_name="OrgMuestra", verbose_name="Organización", on_delete=models.CASCADE)
    sedeRecepcion=models.ForeignKey(Sede, blank=True, null=True, related_name="SedeMuestra", verbose_name="Sede de Recepción", on_delete=models.CASCADE)
    sedeAnalisis=models.ForeignKey(Sede, blank=True, null=True, related_name="SedeAnalisis", verbose_name="Sede de Analisis", on_delete=models.CASCADE)

class Sabor(TimeStamped):
    idSabor = models.CharField(primary_key=True, max_length=64, verbose_name="Identificador")
    nameSabor = models.CharField(max_length=64, verbose_name="Sabor", blank=False)
    nivelSabor= models.IntegerField(choices=NIVELES, default=1)
    pI=models.ForeignKey("self", verbose_name="Padre Nivel I", blank=True, on_delete=models.CASCADE, related_name="IPSabor", null=True)
    pII=models.ForeignKey("self", verbose_name="Padre Nivel II", blank=True, on_delete=models.CASCADE, related_name="IIPSabor", null=True)

class Aroma(TimeStamped):
    idAroma = models.CharField(primary_key=True, max_length=64, verbose_name="Identificador")
    nameAroma = models.CharField(max_length=64, verbose_name="Aroma", blank=False)
    nivelAroma= models.IntegerField( choices=NIVELES, default=1)    
    pI=models.ForeignKey("self", verbose_name="Padre Nivel I", blank=True, on_delete=models.CASCADE, related_name="IPAroma", null=True)
    pII=models.ForeignKey("self", verbose_name="Padre Nivel II", blank=True, on_delete=models.CASCADE, related_name="IIPAroma", null=True)
    pIII=models.ForeignKey("self", verbose_name="Padre Nivel III", blank=True, on_delete=models.CASCADE, related_name="IIIPAroma", null=True)

class DefectoT1(TimeStamped):
    idDefecto = models.CharField(primary_key=True ,max_length=10 ,verbose_name="Identificador")
    nameDefecto = models.CharField(max_length=64 ,verbose_name="Defecto", blank=False)
    granosNecesarios=models.IntegerField(verbose_name="Granos Necesarios", blank=False)

class DefectoT2(TimeStamped):
    idDefecto = models.CharField(primary_key=True ,max_length=10 ,verbose_name="Identificador")
    nameDefecto = models.CharField(max_length=64 ,verbose_name="Defecto", blank=False)
    granosNecesarios=models.IntegerField(verbose_name="Granos Necesarios", blank=False)

class Tamizado(TimeStamped):
    idTamizado = models.CharField(primary_key=True ,max_length=10 ,verbose_name="Identificador")
    nameTamizado = models.CharField(max_length=64 ,verbose_name="Tamizado", blank=False)

class Fisico(TimeStamped):
    fkCatador=models.ForeignKey(Colaborador, blank=False, related_name="CatadorFisico", verbose_name="CatadorFisico", on_delete=models.CASCADE)
    fkMuestra= models.ForeignKey(Muestra, blank=False, related_name="Fsico", verbose_name="Muestra", on_delete=models.CASCADE)
    pDefectos = models.FloatField(null=False, blank=True, default=0.0)
    porDefectos=models.FloatField(null=False, blank=True, default=0.0)
    temp=models.FloatField(null=False, blank=True, default=0.0)
    humedad=models.FloatField(null=False, blank=True, default=0.0)
    rendimiento=models.FloatField(null=False, blank=True, default=0.0)
    fechaFisico=models.DateField(null=False, auto_now_add=True)
    pesoTamiz=models.FloatField(null=False, blank=True, default=0.0)
    pesoTotalTamiz=models.FloatField(null=False, blank=True, default=0.0)
    porTotalTamiz=models.FloatField(null=False, blank=True, default=0.0)

class FisicoDefectoTI(TimeStamped):
    fkFisico=models.ForeignKey(Fisico, blank=False, related_name="FisicoDefectoTI", verbose_name="Fisico", on_delete=models.CASCADE)
    fkDefecto=models.ForeignKey(DefectoT1, blank=False, related_name="DefectoT1", verbose_name="Defecto", on_delete=models.CASCADE)
    encontrados=models.FloatField(blank=False, default=0)
    defectos=models.FloatField(blank=False, default=0)
    pesoDefecto=models.FloatField(null=False, blank=True, default=0.0)
    porDefecto=models.FloatField(null=False, blank=True, default=0.0)

class FisicoDefectoTII(TimeStamped):
    fkFisico=models.ForeignKey(Fisico, blank=False, related_name="FisicoDefectoTII", verbose_name="Fisico", on_delete=models.CASCADE)
    fkDefecto=models.ForeignKey(DefectoT2, blank=False, related_name="DefectoT2", verbose_name="Defecto", on_delete=models.CASCADE)
    encontrados=models.FloatField(blank=False, default=0)
    defectos=models.FloatField(blank=False, default=0)
    pesoDefecto=models.FloatField(null=False, blank=True, default=0.0)
    porDefecto=models.FloatField(null=False, blank=True, default=0.0)

class FisicoTamizado(TimeStamped):
    fkFisico=models.ForeignKey(Fisico, blank=False, related_name="FisicoTamizado", verbose_name="Fisico", on_delete=models.CASCADE)
    fkTamizado=models.ForeignKey(Tamizado, blank=False, related_name="Tamizado", verbose_name="Tamizado", on_delete=models.CASCADE)
    pesoGranos=models.FloatField(null=False, blank=True, default=0.0)
    porGranos=models.FloatField(null=False, blank=True, default=0.0)

class Sensorial(TimeStamped):
    fkCatador=models.ForeignKey(Colaborador, blank=False, related_name="CatadorSensorial", verbose_name="CatadorSensorial", on_delete=models.CASCADE)
    fkMuestra= models.ForeignKey(Muestra, blank=False, related_name="Sensorial", verbose_name="Muestra", on_delete=models.CASCADE)
    cAgua= models.FloatField(null=False, blank=True, default=0.0)
    nTueste=models.IntegerField(choices=TUESTE, default=1)
    fragancia=models.FloatField(null=False, blank=True, default=0.0)
    aroma=models.ManyToManyField(Aroma, blank=True, related_name="AAroma", verbose_name="Aromas")
    seco=models.IntegerField(choices=TUESTE, default=1)
    espuma=models.IntegerField(choices=TUESTE, default=1)
    pSabor=models.FloatField(null=False, blank=True, default=0.0)
    sabor=models.ManyToManyField(Sabor, blank=True, related_name="ASabor", verbose_name="Sabores")
    remanente=models.FloatField(null=False, blank=True, default=0.0)
    pUniformidad=models.FloatField(null=False, blank=True, default=0.0)
    cUniformidad=models.IntegerField(default=0)
    pTLimpia=models.FloatField(null=False, blank=True, default=0.0)
    cTLimpia=models.IntegerField(default=0)
    pDulzor=models.FloatField(null=False, blank=True, default=0.0)
    cDulzor=models.IntegerField(default=0)
    acidez=models.FloatField(null=False, blank=True, default=0.0)
    iAcidez=models.IntegerField(choices=INTENSIDAD ,default=2)
    cuerpo=models.FloatField(null=False, blank=True, default=0.0)
    iCuerpo=models.IntegerField(choices=INTENSIDAD ,default=2)
    balance=models.FloatField(null=False, blank=True, default=0.0)
    comentario=models.TextField(max_length=254, blank=True, verbose_name="Observaciones")
    pCatador=models.FloatField(null=False, blank=True, default=0.0)
    castigo=models.FloatField(null=False, blank=True, default=0.0)
    pFinal=models.FloatField(null=False, blank=True, default=0.0)
    fechaSensorial=models.DateField(null=False, auto_now_add=True)

    def total(self):
        if self.iCuerpo == 1 or self.iCuerpo == 2:
            castigo=(2*(5-self.cTLimpia))
            self.pFinal=(self.fragancia+self.balance+self.pSabor+self.pTLimpia+self.remanente+self.acidez+self.cuerpo+self.pUniformidad +self.pCatador +self.pDulzor) - castigo
        elif self.iCuerpo == 3:
            castigo=(4*(5-self.cTLimpia))
            self.pFinal=(self.fragancia+self.balance+self.pSabor+self.pTLimpia+self.remanente+self.acidez+self.cuerpo+self.pUniformidad +self.pCatador +self.pDulzor) -  castigo
        self.save()

    def getIntensidad(self):
        return self.get_iCuerpo_display()
    
    def getTueste(self):
        return self.get_nTueste_display()

class Conciliacion(TimeStamped):
    fkCSensorial=models.ForeignKey(Sensorial, null=True, blank=True, related_name="CSensorial", verbose_name="Sensorial" , on_delete=models.CASCADE)
    fechaConciliacion=models.DateField(null=True, blank=True, auto_now_add=True)
    estado=models.IntegerField(choices=Estado.choices, default=2)