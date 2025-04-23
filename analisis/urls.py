from django.urls import path
from . import views as v

urlpatterns=[
    path("", v.index, name="MuestraHome"),
    path("addMuestra", v.addMuestra, name="addMuestra"),
    path("editMuestra/<int:idMuestra>", v.editMuestra, name="editMuestra"),
    path("analize", v.analizeMuestra, name="analizeM"),
    path("saveFisico", v.saveFisico, name="saveFisico"),
    path("saveSensorial", v.saveSensorial, name="saveSensorial"),
    path("completados", v.completados, name="analisisCompletados"),
    path("verMuestras", v.verMuestras, name="verMuestras"),
    path("completarAnalisis", v.completarAnalisis, name="cAnalisis"),
    path("verPuntaje/<idMuestra>", v.verPuntaje, name="verPuntaje"),
    path("conciliar/<muestra>", v.conciliar, name="conciliar"),
    path("homeConciliacion", v.pendientesConciliacion, name="homeConciliacion"),
    path("imprimir/<idMuestra>", v.impresion, name="imprimir"),
    path("impresionProd/<idMuestra>", v.impresionProd, name="impresionProd"),
    path('delete/<idMuestra>', v.rmMuestra, name='deleteMuestra'),
]