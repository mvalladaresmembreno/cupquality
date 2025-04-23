from django import template
from analisis.models import *

register = template.Library()

@register.filter
def get_tamizado_peso(fisico, criba):
    t=FisicoTamizado.objects.get(fkFisico_id=fisico, fkTamizado__idTamizado=criba)
    if t:
        return t.pesoGranos
    else:
        return 0

@register.filter
def get_tamizado_por(fisico, criba):
    t=FisicoTamizado.objects.get(fkFisico_id=fisico, fkTamizado__idTamizado=criba)
    if t:
        return t.porGranos
    else:
        return 0