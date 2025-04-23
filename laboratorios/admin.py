from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Muestra)
admin.site.register(Sabor)
admin.site.register(Aroma)
admin.site.register(DefectoT1)
admin.site.register(DefectoT2)
admin.site.register(Tamizado)
admin.site.register(Fisico)
admin.site.register(FisicoDefectoTI)
admin.site.register(FisicoDefectoTII)
admin.site.register(FisicoTamizado)
admin.site.register(Sensorial)
admin.site.register(Analisis)
admin.site.register(Conciliacion)