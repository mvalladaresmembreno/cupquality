from django import template
from analisis.models import *

register = template.Library()

@register.simple_tag
def get_sabor_checkbox(**kwargs):
    sabor=kwargs['sabor']
    sabores=list()
    if kwargs['sabores']:
        for s in kwargs['sabores'].values('idSabor'):
            sabores.append(s['idSabor'])
        if sabores:
            if sabor in sabores:
                print(sabor)
                return 'selected'

@register.simple_tag
def get_aroma_checkbox(**kwargs):
    aroma=kwargs['aroma']
    aromas=list()
    if kwargs['aromas']:
        for a in kwargs['aromas'].values('idAroma'):
            aromas.append(a['idAroma'])
        if aromas:
            if aroma in aromas:
                print(aroma)
                return 'selected'
