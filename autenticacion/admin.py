from ast import Or
from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_filter=["org", "tipoUser"]
    search_fields=['usuario__username','organizacion__name_org','usuario__first_name', 'usuario__last_name', 'tipoUser']
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(UserAdmin, self).__init__(model, admin_site)

class SedeAdmin(admin.ModelAdmin):
    list_filter=["name_sede", "ubicacion"]
    search_fields=['name_sede', "ubicacion"]

    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(SedeAdmin, self).__init__(model, admin_site)

admin.site.register(Sede, SedeAdmin)
admin.site.register(Organizacion)
admin.site.register(Colaborador, UserAdmin)