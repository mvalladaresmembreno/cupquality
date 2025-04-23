from django.urls import path
from . import views as v
urlpatterns=[
    path("", v.index, name="LabHome" ), #estadisticas
    path("addMuestra", v.addMuestra, name="addMuestraLab"), #agregar muestra
    path("verMuestras", v.verMuestras, name="verMuestrasLab"), #ver muestra
    path("editMuestra/<int:idMuestra>", v.editMuestra, name="editMuestraLab"),#editar muestra
    path("analize", v.analizeMuestra, name="analizeMLab"), #analizar muestra
    path("saveFisico", v.saveFisico, name="saveFisicoLab"), #guardar analisis fisico
    path("saveSensorial", v.saveSensorial, name="saveFisicoLab"), #guardar analsis sensorial
    path("imprimir/<idMuestra>", v.impresion, name="imprimirLab"), #imprimir
    path("verResultados/", v.verResultado, name="verResultadosMuestraLab"), #ver resultados de una muestra
    path("completados", v.completados, name="completadosLab"), #ver muestras completadas
    path('filtros/', v.filtros, name="FiltrosLab"),
    path('delete/<idMuestra>', v.rmMuestra, name='deleteMuestraLab'),
]