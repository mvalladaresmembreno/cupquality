from django import template
from analisis.models import *

register = template.Library()

@register.simple_tag
def get_defecto_checkbox(**kwargs):
    tipo=int(int(kwargs['tipo']))
    defecto=kwargs['defecto']
    value=kwargs['value']
    if tipo == 1 :
        check=FisicoDefectoTI.objects.get(fkFisico__id=value, fkDefecto__idDefecto=defecto)
    else:
        check=FisicoDefectoTII.objects.get(fkFisico__id=value, fkDefecto__idDefecto=defecto)
    if check and (check.encontrados > 0):
        return 'checked'

@register.simple_tag
def get_defecto_encontrados(**kwargs):
    tipo=int(kwargs['tipo'])
    defecto=kwargs['defecto']
    value=kwargs['value']
    if tipo == 1 :
        check=FisicoDefectoTI.objects.get(fkFisico__id=value, fkDefecto__idDefecto=defecto)
    else:
        check=FisicoDefectoTII.objects.get(fkFisico__id=value, fkDefecto__idDefecto=defecto)
    if check.encontrados > 0:
        return check.encontrados
    else: return 0

@register.simple_tag
def get_defecto_defectos(**kwargs):
    tipo=int(kwargs['tipo'])
    defecto=kwargs['defecto']
    value=kwargs['value']
    if tipo == 1 :
        check=FisicoDefectoTI.objects.get(fkFisico__id=value, fkDefecto__idDefecto=defecto)
    else:
        check=FisicoDefectoTII.objects.get(fkFisico__id=value, fkDefecto__idDefecto=defecto)
    if check.defectos > 0:
        return check.defectos
    else: return 0    

@register.simple_tag
def get_defecto_peso(**kwargs):
    tipo=int(kwargs['tipo'])
    defecto=kwargs['defecto']
    value=kwargs['value']
    if tipo == 1 :
        check=FisicoDefectoTI.objects.get(fkFisico__id=value, fkDefecto__idDefecto=defecto)
    else:
        check=FisicoDefectoTII.objects.get(fkFisico__id=value, fkDefecto__idDefecto=defecto)
    if check.pesoDefecto > 0:
        return check.pesoDefecto
    else: return 0

@register.simple_tag
def get_defecto_por(**kwargs):
    tipo=int(kwargs['tipo'])
    defecto=kwargs['defecto']
    value=kwargs['value']
    if tipo == 1 :
        check=FisicoDefectoTI.objects.get(fkFisico__id=value, fkDefecto__idDefecto=defecto)
    else:
        check=FisicoDefectoTII.objects.get(fkFisico__id=value, fkDefecto__idDefecto=defecto)
    if check.porDefecto > 0:
        return check.porDefecto
    else: return 0
