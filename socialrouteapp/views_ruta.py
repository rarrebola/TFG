from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from socialrouteapp import forms
from socialrouteapp import models
from django.utils import timezone
import decimal

def crearRuta(request):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            if request.method == "POST":
                form = forms.RutaForm(request.POST)
                if form.is_valid():
                    ruta = models.Ruta(titulo = request.POST["titulo"],
                               descripcion = request.POST["descripcion"],
                               precio = 0.0,
                               puntuacion = 0.0,
                               creador = usuario)
                    ruta.save()
                    log = models.Log(usuario = usuario,
                                     ruta = ruta,
                                     fecha = timezone.now(),
                                     log = 'creado')
                    log.save()
                    return HttpResponseRedirect('/inicio/')
            else:
                form = forms.RutaForm()
        return render(request, 'crearRuta.html', {'usuario': usuario,
                                                  'form':form})
    else:
        return HttpResponseRedirect('/')

def ruta(request, id_ruta):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            ruta = get_object_or_404(models.Ruta, pk=id_ruta)
            request.session['ruta'] = ruta.pk
            #Recuperamos los días pertenecientes a la ruta:
            dias = models.Dia.dias_ruta(ruta)
            precio_ruta = decimal.Decimal(0.0)
            for dia in dias:
                ruta.precio = precio_ruta + dia.precio
            ruta.save()
            ruta_seguida = (ruta in usuario.ruta_set.filter(pk=id_ruta))
            form = forms.ValoracionForm()
            valoraciones = models.ValoracionRuta.valoraciones_ruta(ruta)
            lugares_interes = []
            for dia in dias:
                lugares_interes_aux = dia.lugarinteres_set.all()
                for lugar_interes in lugares_interes_aux:
                    lugares_interes.append(lugar_interes)
            calcular_precio_ruta(ruta, dias)
            return render(request, 'ruta.html', {'ruta': ruta,
                                                         'usuario': usuario,
                                                         'dias': dias,
                                                         'ruta_seguida': ruta_seguida,
                                                         'form': form,
                                                         'valoraciones':valoraciones,
                                                         'lugares_interes': lugares_interes})
    else:
        return HttpResponseRedirect('/')

def borrarRuta(request, id_ruta):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            ruta = get_object_or_404(models.Ruta, pk=id_ruta)
            if usuario == ruta.creador:
                ruta.delete()
            return HttpResponseRedirect('/inicio/')
    else:
        return HttpResponseRedirect('/')

def editarRuta(request, id_ruta):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            ruta = get_object_or_404(models.Ruta, pk=id_ruta)
            if ruta and ruta.creador==usuario:
                form = forms.RutaForm(request.POST or None,
                                     initial = {'usuario': usuario,
                                                'titulo':ruta.titulo,
                                                'descripcion':ruta.descripcion})
                if form.is_valid():
                    if request.POST["titulo"]:
                       ruta.titulo=request.POST["titulo"]
                    if request.POST["descripcion"]:
                        ruta.descripcion=request.POST["descripcion"]
                    ruta.save()
                    log = models.Log(usuario=usuario,
                                     ruta=ruta,
                                     fecha=timezone.now(),
                                     log='modificado')
                    log.save()
                    return HttpResponseRedirect('/inicio/')
                else:
                    return render(request, 'crearRuta.html', {'usuario': usuario,
                                                              'form': form})
            else:
                return HttpResponseRedirect('/inicio/')
    else:
        return HttpResponseRedirect('/')

def busqueda(request):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            if 'consulta' in request.GET:
                if request.GET['consulta']:
                    consulta = request.GET['consulta']
                    #Búsqueda de rutas cuyo título contenga la consulta
                    rutas = []
                    rutas_aux = models.Ruta.objects.filter(titulo__icontains=consulta)
                    for ruta in rutas_aux:
                        if ruta not in rutas:
                            rutas.append(ruta)
                    #Búsqueda de rutas cuya descripción contenga la consulta
                    rutas_aux = models.Ruta.objects.filter(descripcion__icontains=consulta)
                    for ruta in rutas_aux:
                        if ruta not in rutas:
                            rutas.append(ruta)
                    #Búsqueda de rutas cuyo día contenga la consulta
                    dias = models.Dia.objects.all()
                    for dia in dias:
                        if dia.titulo in consulta:
                            if dia.ruta not in rutas:
                                rutas.append(dia.ruta)
                        if  dia.descripcion in consulta:
                            if dia.ruta not in rutas:
                                rutas.append(dia.ruta)
                    #Búsqueda de rutas cuyo creador contenga la consulta
                    rutas_aux = models.Ruta.objects.all()
                    for ruta in rutas_aux:
                        if consulta in ruta.creador.alias and ruta not in rutas:
                            rutas.append(ruta)
                    #Búsqueda de usuarios cuyo alias contenga la consulta
                    usuarios = models.Usuario.objects.filter(alias__icontains=consulta)
                    #Búsqueda de lugares de interés cuyo nombre contenga la consulta
                    lugares_interes = []
                    lugares_interes_aux = models.LugarInteres.objects.filter(nombre__icontains=consulta)
                    for lugar_interes in lugares_interes_aux:
                        if lugar_interes not in lugares_interes:
                            lugares_interes.append(lugar_interes)
                    #Búsqueda de lugares de interés cuya localidad contenga la consulta
                    lugares_interes_aux = models.LugarInteres.objects.filter(localidad__icontains=consulta)
                    for lugar_interes in lugares_interes_aux:
                        if lugar_interes not in lugares_interes:
                            lugares_interes.append(lugar_interes)

                    return render(request, 'busqueda.html',{'usuario': usuario,
                                                            'titulo':consulta,
                                                           'rutas':rutas,
                                                           'usuarios':usuarios,
                                                           'lugares_interes': lugares_interes})
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        HttpResponseRedirect('/')

def seguirRuta(request, id_ruta):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            ruta = get_object_or_404(models.Ruta, pk=id_ruta)
            dias = models.Dia.dias_ruta(ruta)
            form = forms.ValoracionForm()
            valoraciones = models.ValoracionRuta.valoraciones_ruta(ruta)
            lugares_interes = []
            for dia in dias:
                lugares_interes_aux = dia.lugarinteres_set.all()
                for lugar_interes in lugares_interes_aux:
                    lugares_interes.append(lugar_interes)
            rutas_seguidas = usuario.ruta_set.all()
            rutas_creadas = models.Ruta.objects.filter(creador=usuario)
            if not (ruta in rutas_seguidas or ruta in rutas_creadas):
                ruta.seguidores.add(usuario)
            return render(request, 'ruta.html', {'ruta': ruta,
                                                         'usuario': usuario,
                                                         'dias': dias,
                                                         'ruta_seguida': True,
                                                         'form': form,
                                                         'valoraciones':valoraciones,
                                                         'lugares_interes': lugares_interes})
    else:
        return HttpResponseRedirect('/')

def dejarDeSeguirRuta(request, id_ruta):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            ruta = get_object_or_404(models.Ruta, pk=id_ruta)
            dias = models.Dia.dias_ruta(ruta)
            form = forms.ValoracionForm()
            valoraciones = models.ValoracionRuta.valoraciones_ruta(ruta)
            lugares_interes = []
            for dia in dias:
                lugares_interes_aux = dia.lugarinteres_set.all()
                for lugar_interes in lugares_interes_aux:
                    lugares_interes.append(lugar_interes)
            rutas_seguidas = usuario.ruta_set.all()
            rutas_creadas = models.Ruta.objects.filter(creador=usuario)
            if not (ruta not in rutas_seguidas or ruta in rutas_creadas):
                ruta.seguidores.remove(usuario)
            return render(request, 'ruta.html', {'ruta': ruta,
                                                     'usuario': usuario,
                                                     'dias': dias,
                                                     'ruta_seguida': False,
                                                     'form': form,
                                                     'valoraciones': valoraciones,
                                                     'lugares_interes': lugares_interes})

    else:
        return HttpResponseRedirect('/')
def addValoracion(request):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            if request.method == "POST":
                form  = forms.ValoracionForm(request.POST)
                if form.is_valid():
                    ruta = get_object_or_404(models.Ruta, pk=request.session['ruta'])
                    valoracion = models.ValoracionRuta(fechaCreacion = timezone.now(),
                                                       valoracion = request.POST['puntuacion'],
                                                       comentario =  request.POST['comentario'],
                                                       usuario = usuario,
                                                       ruta = ruta)
                    valoracion.save()
                    dias = models.Dia.dias_ruta(ruta)
                    ruta_seguida = (ruta in usuario.ruta_set.all())
                    form = forms.ValoracionForm()
                    valoraciones = models.ValoracionRuta.valoraciones_ruta(ruta)
                    calcular_valoraciones_ruta(ruta, valoraciones)
                    return render(request, 'ruta.html', {'ruta': ruta,
                                                         'usuario': usuario,
                                                         'dias': dias,
                                                         'ruta_seguida': ruta_seguida,
                                                         'form': form,
                                                         'valoraciones':valoraciones})
                else:
                    ruta = models.Ruta.objects.filter(pk=request.session['ruta'])
                    dias = models.Dia.dias_ruta(ruta)
                    ruta_seguida = (ruta in usuario.ruta_set.all())
                    form = forms.ValoracionForm()
                    valoraciones = models.ValoracionRuta.valoraciones_ruta(ruta)
                    return render(request, 'ruta.html', {'ruta': ruta,
                                                         'usuario': usuario,
                                                         'dias': dias,
                                                         'ruta_seguida': ruta_seguida,
                                                         'form': form,
                                                         'valoraciones':valoraciones})
    else:
        return HttpResponseRedirect('/')

def borrarValoracion(request, id_valoracion):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
           valoracion =  get_object_or_404(models.ValoracionRuta, pk=id_valoracion)
           ruta = valoracion.ruta
           valoracion.delete()
           valoraciones = models.ValoracionRuta.valoraciones_ruta(ruta)
           calcular_valoraciones_ruta(ruta, valoraciones)
           dias = models.Dia.dias_ruta(ruta)
           ruta_seguida = (ruta in usuario.ruta_set.all())
           form = forms.ValoracionForm()
           return render(request, 'ruta.html', {'ruta': ruta,
                                                'usuario': usuario,
                                                'dias': dias,
                                                'ruta_seguida': ruta_seguida,
                                                'form': form,
                                                'valoraciones': valoraciones})
    else:
        return HttpResponseRedirect('/')

def calcular_valoraciones_ruta(ruta, valoraciones):
    num_valoraciones = len(valoraciones)
    puntuacion_ruta = decimal.Decimal(0.0)
    for val in valoraciones:
        puntuacion_ruta = puntuacion_ruta + val.valoracion

    if num_valoraciones > 0:
        ruta.puntuacion = puntuacion_ruta / num_valoraciones
    else:
        ruta.puntuacion = decimal.Decimal(0.0)

    ruta.save()

def calcular_precio_ruta(ruta, dias):
    precio_ruta = decimal.Decimal(0.0)
    for dia in dias:
            precio_ruta = precio_ruta + dia.precio
    ruta.precio = precio_ruta
    ruta.save()