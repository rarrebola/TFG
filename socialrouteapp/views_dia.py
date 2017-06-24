from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from socialrouteapp import forms
from socialrouteapp import models
from socialrouteapp import views_ruta
from django.utils import timezone
import decimal

# Create your views here.

def anadirDia(request, id_ruta):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            ruta_d = get_object_or_404(models.Ruta, pk=id_ruta)
            if ruta_d and usuario == ruta_d.creador:
                form = forms.DiaForm(request.POST)
                if form.is_valid():
                    dia = models.Dia(titulo = request.POST["titulo"],
                             descripcion = request.POST["descripcion"],
                             precio = 0.0,
                             ruta = ruta_d,
                             creador = usuario)
                    dia.save()
                    dias = models.Dia.dias_ruta(ruta_d)
                    log = models.Log(usuario=usuario,
                                     ruta=ruta_d,
                                     fecha=timezone.now(),
                                     log='modificado')
                    log.save()
                    lugares_interes = []
                    for dia in dias:
                        lugares_interes_aux = dia.lugarinteres_set.all()
                        for lugar_interes in lugares_interes_aux:
                            lugares_interes.append(lugar_interes)
                    return HttpResponseRedirect('/%s/ruta/' % ruta_d.id)
                else:
                    form = forms.DiaForm()
                    return render(request, 'crearDia.html', {'form': form})
            else:
                return HttpResponseRedirect('/inicio/')
    else:
        return HttpResponseRedirect('/')

def dia(request, id_dia):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            dia = get_object_or_404(models.Dia, pk=id_dia)
            request.session['dia'] = id_dia
            lugares_interes = dia.lugarinteres_set.all()
            calcular_precio_dia(dia, lugares_interes)
            return render(request, 'dia.html', {'dia': dia,
                                                'usuario': usuario,
                                                'lugares_interes': lugares_interes})
    else:
        return HttpResponseRedirect('/')

def borrarDia(request, id_dia):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            dia = get_object_or_404(models.Dia, pk=id_dia)
            ruta = dia.ruta
            if dia.creador == usuario:
                dia.delete()
        dias = models.Dia.dias_ruta(ruta)
        ruta_seguida = (ruta in usuario.ruta_set.all())
        form = forms.ValoracionForm()
        valoraciones = models.ValoracionRuta.valoraciones_ruta(ruta)
        views_ruta.calcular_precio_ruta(ruta, dias)
        lugares_interes = []
        for dia in dias:
            lugares_interes_aux = dia.lugarinteres_set.all()
            for lugar_interes in lugares_interes_aux:
                lugares_interes.append(lugar_interes)
        log = models.Log(usuario=usuario,
                         ruta=ruta,
                         fecha=timezone.now(),
                         log='modificado')
        log.save()
        return render(request, 'ruta.html', {'ruta': ruta,
                                                         'usuario': usuario,
                                                         'dias': dias,
                                                         'ruta_seguida': ruta_seguida,
                                                         'form': form,
                                                         'valoraciones':valoraciones,
                                                         'lugares_interes': lugares_interes})
    else:
        return HttpResponseRedirect('/')

def editarDia(request, id_dia):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            dia = get_object_or_404(models.Dia, pk=id_dia)
            if dia and dia.creador == usuario:
                form = forms.RutaForm(request.POST or None,
                                    initial = {'titulo':dia.titulo,
                                                'descripcion':dia.descripcion})
                if form.is_valid():
                    if request.POST["titulo"]:
                        dia.titulo=request.POST["titulo"]
                    if request.POST["descripcion"]:
                        dia.descripcion=request.POST["descripcion"]
                    dia.save()
                    ruta = dia.ruta
                    dias = models.Dia.dias_ruta(ruta)
                    ruta_seguida = (ruta in usuario.ruta_set.all())
                    views_ruta.calcular_precio_ruta(ruta, dias)
                    form = forms.ValoracionForm()
                    valoraciones = models.ValoracionRuta.valoraciones_ruta(ruta)
                    lugares_interes = []
                    for dia in dias:
                        lugares_interes_aux = dia.lugarinteres_set.all()
                        for lugar_interes in lugares_interes_aux:
                            lugares_interes.append(lugar_interes)
                    log = models.Log(usuario=usuario,
                                     ruta=ruta,
                                     fecha=timezone.now(),
                                     log='modificado')
                    log.save()
                    return render(request, 'ruta.html', {'ruta': ruta,
                                                         'usuario': usuario,
                                                         'dias': dias,
                                                         'ruta_seguida': ruta_seguida,
                                                         'form': form,
                                                         'valoraciones':valoraciones,
                                                         'lugares_interes': lugares_interes})
                else:
                    return render(request, 'crearDia.html', {'form': form})
            else:
                return HttpResponseRedirect('/inicio/')
    else:
        return HttpResponseRedirect('/')

def calcular_precio_dia(dia, lugares_interes):
    precio_dia = decimal.Decimal(0.0)
    for lugar_interes in lugares_interes:
        precio_dia = precio_dia + lugar_interes.precio
    dia.precio = precio_dia
    dia.save()

