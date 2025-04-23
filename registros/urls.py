from django.contrib import admin
from django.urls import path
from . import views as v

urlpatterns=[
    path('', v.index, name='HomeRegistro'),
    path('productor/', v.addProd, name="addProd"),
    path('rmProd/', v.rmProd, name="rmProd"),
    path('updateProd/', v.updateProd, name="updateProd"),
    path('finca/', v.addFinca, name="addFinca"),
    path('rmFinca/', v.rmFinca, name="rmFinca"),
    path('updateFinca/', v.updateFinca, name="updateFinca"),
    path('lote/', v.addLote, name="addLote"),
    path('rmLote/', v.rmLote, name="rmLote"),
    path('updateLote/', v.updateLote, name="updateLote"),
    path('filtros/', v.filtros, name="Filtros"),
    path('perfilMuestras/', v.perfilMuestras, name="perfilMuestras"),
    path('getPerfilMuestras/', v.getPerfilMuestras, name="getPerfilMuestras"),
]