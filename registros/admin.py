from itertools import product
from django.contrib import admin
from .models import *
# Register your models here.

class ProductorAdmin(admin.ModelAdmin):
    list_filter=["firstnameProd","lastnameProd","fkMun__nameMun", "fechaNac"]
    search_fields=["idProd","firstnameProd","lastnameProd","fkMun__nameMun", "fechaNac"]
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(ProductorAdmin, self).__init__(model, admin_site)

class FincaAdmin(admin.ModelAdmin):
    list_filter=["nameFinca","fkProd__firstnameProd","fkProd__lastnameProd","fkCom__nameCom", "fkCom__fkMun__nameMun", "area"]
    search_fields=["idFinca","nameFinca","fkProd__firstnameProd","fkProd__lastnameProd","fkMun__nameMun", "area"]

    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(FincaAdmin, self).__init__(model, admin_site)
class LoteAdmin(admin.ModelAdmin):
    list_filter=["nameLote", "fkVar__nameVariedad", "fkCert__nameCert", "area", "altitud"]
    search_fields=["idLote","nameLote", "fkVar__nameVariedad", "fkCert__nameCert", "area", "altitud"]
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(LoteAdmin, self).__init__(model, admin_site)

class DepartamentoAdmin(admin.ModelAdmin):
    list_filter=["fkPais__namePais", "nameDpto"]
    search_fields=["idDpto","fkPais__namePais", "nameDpto"]
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(DepartamentoAdmin, self).__init__(model, admin_site)

class MunicipioAdmin(admin.ModelAdmin):
    list_filter=["fkdpto__nameDpto", "nameMun"]
    search_fields=["idMun","fkdpto__nameDpto", "nameMun"]
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(MunicipioAdmin, self).__init__(model, admin_site)

class ComunidadAdmin(admin.ModelAdmin):
    list_filter=["fkMun__fkdpto__nameDpto","fkMun__nameMun", "nameCom"]
    search_fields=["idCom","fkMun__fkdpto__nameDpto","fkMun__nameMun", "nameCom"]
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(ComunidadAdmin, self).__init__(model, admin_site)

admin.site.register(Pais)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Comunidad, ComunidadAdmin)
admin.site.register(Productor, ProductorAdmin)
admin.site.register(Finca, FincaAdmin)
admin.site.register(Variedad)
admin.site.register(Certificacion)
admin.site.register(Lote, LoteAdmin)