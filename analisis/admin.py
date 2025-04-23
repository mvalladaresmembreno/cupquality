from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Muestra)
admin.site.register(DefectoT1)
admin.site.register(DefectoT2)
admin.site.register(Fisico)
admin.site.register(Sabor)
admin.site.register(Aroma)
admin.site.register(Tamizado)
admin.site.register(FisicoDefectoTI)
admin.site.register(FisicoDefectoTII)
admin.site.register(FisicoTamizado)
admin.site.register(Sensorial)
admin.site.register(Conciliacion)
""" 
admin.site.register(Analisis)
 """