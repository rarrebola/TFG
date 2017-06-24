from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from socialrouteapp import forms
from socialrouteapp import models
from socialrouteapp import views_dia
import decimal

def crearLugarInteres(request):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            if request.method == "POST":
                form = forms.CrearLugarInteresForm(request.POST)
                if form.is_valid():
                    lugar_interes_aux = models.LugarInteres.objects.filter(nombre = request.POST["nombre"],
                                                                           localidad=request.POST["localidad"])
                    if lugar_interes_aux:
                        error = "El lugar de interés ya existe"
                        form = forms.CrearLugarInteresForm()
                        return render(request, 'crearLugarInteres.html', {'usuario': usuario,
                                                                          'form': form,
                                                                          'error': error})
                    else:
                        lugar_interes = models.LugarInteres(nombre = request.POST["nombre"],
                                                            direccion = request.POST["direccion"],
                                                            localidad = request.POST["localidad"],
                                                            descripcion = request.POST["descripcion"],
                                                            horario = request.POST["horario"],
                                                            precio = request.POST["precio"],
                                                            puntuacion = 0.0)
                        lugar_interes.save()
                        return HttpResponseRedirect('/inicio/')
            else:
                form = forms.CrearLugarInteresForm()
        return render(request, 'crearLugarInteres.html', {'usuario': usuario,
                                                          'form':form})
    else:
        return HttpResponseRedirect('/')

def lugarInteres(request, id_lugarInteres):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            lugar_interes = get_object_or_404(models.LugarInteres, pk=id_lugarInteres)
            request.session['lugar_interes'] = lugar_interes.pk
            form = forms.ValoracionForm()
            valoraciones = models.ValoracionLugarInteres.valoraciones_lugar_interes(lugar_interes)

            return render(request, 'lugarInteres.html', {'lugar_interes': lugar_interes,
                                                         'form':form,
                                                         'valoraciones':valoraciones,
                                                         'usuario': usuario})
    else:
        return HttpResponseRedirect('/')

def editarLugarInteres(request, id_lugarInteres):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            lugar_interes = get_object_or_404(models.LugarInteres, pk=id_lugarInteres)
            form = forms.EditarLugarInteresForm(request.POST or None,
                                      initial={'descripcion': lugar_interes.descripcion,
                                               'horario': lugar_interes.horario,
                                               'precio': lugar_interes.precio})
            if form.is_valid():
                    if request.POST["descripcion"]:
                        lugar_interes.descripcion = request.POST["descripcion"]
                    if request.POST["horario"]:
                        lugar_interes.horario = request.POST["horario"]
                    if request.POST["precio"]:
                        lugar_interes.precio = request.POST["precio"]
                    lugar_interes.save()
                    return HttpResponseRedirect('/inicio/')
            else:
                return render(request, 'crearLugarInteres.html', {'usuario': usuario,
                                                                  'form': form,
                                                                  'lugar_interes': lugar_interes})
    else:
        return HttpResponseRedirect('/')

def buscar_lugares_interes(request):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            if 'dia' in request.session:
                if request.session['dia']:
                    dia = get_object_or_404(models.Dia, pk=request.session['dia'])
                    if 'consulta' in request.POST:
                        if request.POST['consulta']:
                            consulta = request.POST['consulta']
                            consulta_lugares_interes = []
                            lugares_interes_aux = models.LugarInteres.objects.filter(localidad__iexact = consulta)
                            lugares_interes = dia.lugarinteres_set.all()
                            for lugar_interes in lugares_interes_aux:
                                if lugar_interes not in consulta_lugares_interes and lugar_interes not in lugares_interes:
                                    consulta_lugares_interes.append(lugar_interes)
                            return render(request, 'dia.html', {'dia': dia,
                                                                'usuario': usuario,
                                                                'consulta_lugares_interes': consulta_lugares_interes,
                                                                'lugares_interes': lugares_interes,
                                                                'buscado': True})
                        else:
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    else:
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/')

def add_lugar_interes(request):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            if request.session['dia']:
                dia = get_object_or_404(models.Dia, pk=request.session['dia'])
                if request.POST['lugares_interes']:
                    lugares_interes_nuevos = request.POST.getlist('lugares_interes')
                    for lugar_interes_aux in lugares_interes_nuevos:
                        lugar_interes = models.LugarInteres.objects.filter(pk=lugar_interes_aux)[0]
                        lugar_interes.dias.add(dia)
                        lugar_interes.save()
                    lugares_interes = dia.lugarinteres_set.all()
                    views_dia.calcular_precio_dia(dia, lugares_interes)
                    return render(request, 'dia.html', {'dia': dia,
                                                        'usuario': usuario,
                                                        'lugares_interes': lugares_interes})
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
                    lugar_interes = get_object_or_404(models.LugarInteres, pk=request.session['lugar_interes'])
                    valoracion = models.ValoracionLugarInteres(fechaCreacion = timezone.now(),
                                                       valoracion = request.POST['puntuacion'],
                                                       comentario =  request.POST['comentario'],
                                                       usuario = usuario,
                                                       lugarInteres = lugar_interes)
                    valoracion.save()
                    form = forms.ValoracionForm()
                    valoraciones = models.ValoracionLugarInteres.valoraciones_lugar_interes(lugar_interes)
                    calcular_valoraciones_lugar_interes(lugar_interes, valoraciones)
                    return render(request, 'lugarInteres.html', {'lugar_interes': lugar_interes,
                                                         'form':form,
                                                         'valoraciones':valoraciones,
                                                         'usuario': usuario})
                else:
                    lugar_interes = get_object_or_404(models.LugarInteres, pk=request.session['lugar_interes'])
                    form = forms.ValoracionForm()
                    valoraciones = models.ValoracionLugarInteres.valoraciones_lugar_interes(lugar_interes)
                    return render(request, 'lugarInteres.html', {'lugar_interes': lugar_interes,
                                                                 'form': form,
                                                                 'valoraciones': valoraciones,
                                                                 'usuario': usuario})
    else:
        return HttpResponseRedirect('/')

def borrarValoracion(request, id_valoracion):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias = request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
           valoracion = get_object_or_404(models.ValoracionLugarInteres, pk=id_valoracion)
           lugar_interes = valoracion.lugarInteres
           valoracion.delete()
           request.session['lugar_interes'] = lugar_interes.pk
           form = forms.ValoracionForm()
           valoraciones = models.ValoracionLugarInteres.valoraciones_lugar_interes(lugar_interes)
           calcular_valoraciones_lugar_interes(lugar_interes, valoraciones)

           return render(request, 'lugarInteres.html', {'lugar_interes': lugar_interes,
                                                        'form': form,
                                                        'valoraciones': valoraciones,
                                                        'usuario': usuario})
    else:
        return HttpResponseRedirect('/')

def removeLugarInteresEnDia(request, id_lugarInteres):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            lugar_interes = get_object_or_404(models.LugarInteres, pk=id_lugarInteres)
            dia = get_object_or_404(models.Dia, pk=request.session['dia'])
            lugar_interes.dias.remove(dia)
            lugar_interes.save()
            lugares_interes = dia.lugarinteres_set.all()
            views_dia.calcular_precio_dia(dia, lugares_interes)
            return render(request, 'dia.html', {'dia': dia,
                                                'usuario': usuario,
                                                'lugares_interes': lugares_interes})
    else:
        return HttpResponseRedirect('/')

#método para calcular la puntuación de un lugar de interés
def calcular_valoraciones_lugar_interes(lugar_interes, valoraciones):
    num_valoraciones = len(valoraciones)
    puntuacion_li = decimal.Decimal(0.0)
    for val in valoraciones:
        puntuacion_li = puntuacion_li + val.valoracion

    if num_valoraciones > 0:
        lugar_interes.puntuacion = puntuacion_li / num_valoraciones
    else:
        lugar_interes.puntuacion = decimal.Decimal(0.0)

    lugar_interes.save()
