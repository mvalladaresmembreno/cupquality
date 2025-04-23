from django.urls import path
from . import views as v

urlpatterns=[
    path("get_municipio/<idDpto>", v.get_municipio, name="get_municipio"),
    path("get_municipios/<idDpto>", v.get_municipios, name="get_municipios"),
    path("get_comunidad/<idMun>", v.get_comunidad, name="get_comunidad"),
    path("get_finca/<idProd>", v.get_finca, name="get_finca"),
    path("get_lote/<idFinca>", v.get_lote, name="get_lote"),
    path("get_muestra/<idMuestra>", v.get_muestra, name="get_muestra"),
    path("get_sensorial/<idMuestra>", v.get_sensorial, name="get_sensorial"),
    path("getFincaUnidad/<idFinca>", v.getFincaUnidad, name="getFincaUnidad"),
    path("getOT/<OT>", v.OTexists, name="OTexists"),
    path("downloadPerfil/",v.getxlsMuestras, name="perfilMuestrasXLS"),
]