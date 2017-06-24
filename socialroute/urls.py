"""socialroute URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from socialrouteapp import views_usuario
from socialrouteapp import views_ruta
from socialrouteapp import views_dia
from socialrouteapp import views_lugar_interes


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views_usuario.init),
    url(r'^registro/', views_usuario.registro, name='registro'),
    url(r'^inicio/', views_usuario.inicio, name='inicio'),
    url(r'^crearRuta/', views_ruta.crearRuta, name='crearRuta'),
    url(r'(?P<id_ruta>[0-9]+)/ruta/$', views_ruta.ruta, name='ruta'),
    url(r'(?P<id_ruta>[0-9]+)/borrarRuta/$', views_ruta.borrarRuta, name='borrarRuta'),
    url(r'(?P<id_ruta>[0-9]+)/editarRuta/$', views_ruta.editarRuta, name='editarRuta'),
    url(r'(?P<id_ruta>[0-9]+)/anadirDia/$', views_dia.anadirDia, name='anadirDia'),
    url(r'(?P<id_dia>[0-9]+)/dia/$', views_dia.dia, name='dia'),
    url(r'(?P<id_dia>[0-9]+)/borrarDia/$', views_dia.borrarDia, name='borrarDia'),
    url(r'(?P<id_dia>[0-9]+)/editarDia/$', views_dia.editarDia, name='editarDia'),
    url(r'^logout/$', views_usuario.logout, name='logout'),
    url(r'^busqueda/$', views_ruta.busqueda, name='busqueda'),
    url(r'^(?P<id_ruta>[0-9]+)/seguirRuta/$', views_ruta.seguirRuta, name='seguirRuta'),
    url(r'^(?P<id_ruta>[0-9]+)/dejarDeSeguirRuta/$', views_ruta.dejarDeSeguirRuta, name='dejarDeSeguirRuta'),
    url(r'^miPerfil/', views_usuario.miPerfil, name='miPerfil'),
    url(r'^editarPerfil/', views_usuario.editarPerfil, name='editarPerfil'),
    url(r'^borrarPerfil/', views_usuario.borrarPerfil, name='borrarPerfil'),
    url(r'(?P<id_usuario>[0-9]+)/usuario/$', views_usuario.perfil, name='usuario'),
    url(r'^(?P<id_usuario>[0-9]+)/seguirUsuario/$', views_usuario.seguirUsuario, name='seguirUsuario'),
    url(r'^(?P<id_usuario>[0-9]+)/dejarDeSeguirUsuario/$', views_usuario.dejarDeSeguirUsuario, name='dejarDeSeguirUsuario'),
    url(r'^recuperarPassword/', views_usuario.recuperarPassword, name="recuperarPassword"),
    url(r'^crearLugarInteres/', views_lugar_interes.crearLugarInteres, name='crearLugarInteres'),
    url(r'^(?P<id_lugarInteres>[0-9]+)/lugarInteres/$', views_lugar_interes.lugarInteres, name='lugarInteres'),
    url(r'^(?P<id_lugarInteres>[0-9]+)/editarLugarInteres/$', views_lugar_interes.editarLugarInteres, name='editarLugarInteres'),
    url(r'^busqueda_li/$', views_lugar_interes.buscar_lugares_interes, name="busqueda_li"),
    url(r'^add_lugar_interes/$', views_lugar_interes.add_lugar_interes, name="add_lugar_interes"),
    url(r'^addValoracion/$', views_ruta.addValoracion, name="addValoracion"),
    url(r'^(?P<id_valoracion>[0-9]+)/borrarValoracionRuta/$', views_ruta.borrarValoracion, name="borrarValoracionRuta"),
    url(r'^addValoracionLugarInteres/$', views_lugar_interes.addValoracion, name="addValoracionLugarInteres"),
    url(r'^(?P<id_valoracion>[0-9]+)/borrarValoracionLugarInteres/$', views_lugar_interes.borrarValoracion, name="borrarValoracionLugarInteres"),
    url(r'^(?P<id_lugarInteres>[0-9]+)/quitarLugarInteres/$', views_lugar_interes.removeLugarInteresEnDia, name="quitarLugarInteres"),
]


