from django.contrib import admin
from django.urls import path
from . import views as v

urlpatterns=[
    path('login/', v.iniciar_sesion, name='login'),
    path('logout/', v.cerrar_sesion, name='logout'),
    path('sign_up', v.crear_usuario, name='signup'),
    path('perfil', v.ver_usuario, name='user'),
    path('perfilAdmin', v.userAdmin, name='userAdmin'),
    path('delete', v.userAdminDelete, name='userAdminDelete'),
    path('edit', v.userAdminEdit, name='userAdminEdit'),
    path('activate', v.userAdminActivate, name='userAdminActivate'),
    path('newfirma', v.firma, name='firma'),
]