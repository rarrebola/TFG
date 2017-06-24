from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from socialrouteapp import forms
from socialrouteapp import models
from random import SystemRandom
from django.core.mail import EmailMultiAlternatives

# Create your views here.

def init(request):

    if "usuario" in request.session:
        return HttpResponseRedirect('/inicio/')
    else:
        if request.method == "POST":
            form = forms.RegistroForm(request.POST)
            if form.is_valid():
                # Rescatamos al usuario de la BD
                try:
                        usuarios = models.Usuario.objects.filter(alias=request.POST["alias"])[::1]
                        usuario = usuarios[0]

                        if request.POST["password"] != usuario.password:
                            # AQUÍ FALTARÍA ENVIAR MENSAJES AL FORM INFORMANDO DEL ERROR
                            error = 'Usuario o contraseña no válido(s)'
                            form = forms.RegistroForm()
                            return render(request, 'login.html', {'form': form,
                                                                  'error': error})
                        else:
                            request.session["usuario"] = usuario.alias
                        return HttpResponseRedirect('/inicio/')
                except IndexError:
                    error = 'Usuario o contraseña no válido(s)'
                    form = forms.RegistroForm()
                    return render(request, 'login.html', {'form': form,
                                                          'error': error})
        else:
            form = forms.RegistroForm()
        return render(request, 'login.html', {'form': form})


def registro(request):
    if "usuario" in request.session:
        return HttpResponseRedirect('/inicio/')
    else:
        if request.method == "POST":
            form = forms.UsuarioForm(request.POST)
            # Validación de datos recibidos del formulario
            if form.is_valid():
                error = ""
                fecha_actual = timezone.now()
                # Se comprueba si el usuario existe:
                usuarios_alias = models.Usuario.objects.filter(alias=request.POST["alias"])[::1]
                usuarios_email = models.Usuario.objects.filter(email=request.POST["email"])[::1]
                if usuarios_alias:
                    error = "Ya existe un perfil con ese alias"
                    form = forms.UsuarioForm()
                    return render(request, 'registro.html', {'form': form,
                                                             'error': error})
                elif usuarios_email:
                    error = "El e-mail que ha introducido ya está en uso"
                    form = forms.UsuarioForm()
                    return render(request, 'registro.html', {'form': form,
                                                             'error': error})
                else:
                        # Creación del usuario
                        usuario = models.Usuario(alias=request.POST["alias"],
                                                 email=request.POST["email"],
                                                 password=request.POST["password"],
                                                 fechaIngreso=fecha_actual
                                                 )
                        # Guardado del usuario en la BD
                        usuario.save()
                        # Se almacena el nombre de usuario en la sesión
                        request.session["usuario"] = usuario.alias
                        return HttpResponseRedirect('/inicio/')
        else:
            form = forms.UsuarioForm()
        return render(request, 'registro.html', {'form': form})


def inicio(request):
    # Variable para almacenar el usuario que se rescata de la sesión
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        rutas_creadas = models.Ruta.objects.filter(creador=usuario)
        logs = []
        logs_aux = models.Log.objects.all().order_by("-fecha")

        seguidos = usuario.seguidos.all()
        rutas_seguidas = usuario.ruta_set.all()
        for log in logs_aux:
            if log.usuario in seguidos or log.ruta in rutas_seguidas:
                if log not in logs:
                    logs.append(log)
        return render(request, 'inicio.html', {'usuario': usuario,
                                               'logs': logs,
                                               'rutas_creadas': rutas_creadas,
                                               'rutas_seguidas': rutas_seguidas})
    else:
        return HttpResponseRedirect('/')


def logout(request):
    # Se elimina la variable de sesión que almacena el nombre de usuario
    if "usuario" in request.session:
        del request.session['usuario']
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def miPerfil(request):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            rutas_creadas = models.Ruta.objects.filter(creador=usuario)
            rutas_seguidas = usuario.ruta_set.all()
            usuarios_seguidos = usuario.seguidos.all()
            return render(request, 'perfil.html', {'usuario': usuario,
                                                   'perfil': usuario,
                                                   'rutas_creadas': rutas_creadas,
                                                   'rutas_seguidas': rutas_seguidas,
                                                   'usuarios_seguidos': usuarios_seguidos})
    else:
        return HttpResponseRedirect('/')


def editarPerfil(request):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            form = forms.EditarPerfilForm(request.POST or None,
                                          initial={'alias': usuario.alias,
                                                   'password': usuario.password,
                                                   'email': usuario.email})
            if form.is_valid():
                if request.POST['password'] == usuario.password:
                    alias_anterior = usuario.alias
                    email_anterior = usuario.email
                    if request.POST['alias']:
                        usuario.alias = request.POST['alias']
                    if request.POST['nuevaPassword']:
                        usuario.password = request.POST['nuevaPassword']
                    if request.POST['email']:
                        usuario.email = request.POST['email']
                    try:
                        usuario_aux = models.Usuario.objects.filter(alias = usuario.alias)[0]
                        if usuario_aux != None and alias_anterior != usuario_aux.alias:
                            error = 'Ya existe un usuario con ese alias, introduzca otro'
                            return render(request, 'editarPerfil.html', {'usuario': usuario,
                                                                         'form':form,
                                                                         'error':error})
                        else:
                            usuario_aux = models.Usuario.objects.filter(email = usuario.email)[0]
                            if usuario_aux != None and email_anterior != usuario_aux.email:
                                error = 'El email que desea usar ya está siendo usado, introduzca otro'
                                return render(request, 'editarPerfil.html', {'usuario': usuario,
                                                                             'form':form,
                                                                             'error':error})
                            else:
                                request.session["usuario"] = usuario.alias
                                usuario.save()

                                return HttpResponseRedirect('/miPerfil/')
                    except IndexError:
                        usuario.save()
                        request.session["usuario"] = usuario.alias
                        return HttpResponseRedirect('/miPerfil/')
                else:
                    error = 'La contraseña introducida no es válida'
                    return render(request, 'editarPerfil.html', {'usuario': usuario,
                                                                 'form': form,
                                                                 'error': error})
            else:
                return render(request, 'editarPerfil.html', {'usuario': usuario,
                                                             'form': form})
    else:
        return HttpResponseRedirect('/')


def borrarPerfil(request):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            usuario.delete()
            del request.session['usuario']
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def perfil(request, id_usuario):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            perfil = get_object_or_404(models.Usuario, pk=id_usuario)
            rutas_creadas = models.Ruta.objects.filter(creador=perfil)
            rutas_seguidas = models.Ruta.objects.filter(seguidores=perfil)
            usuarios_seguidos = perfil.seguidos.all()
            perfil_seguido = False
            for u in usuario.seguidos.all():
                if u.id == perfil.id:
                    perfil_seguido = True
                    break
            return render(request, 'perfil.html', {'usuario': usuario,
                                                   'perfil': perfil,
                                                   'rutas_creadas': rutas_creadas,
                                                   'rutas_seguidas':rutas_seguidas,
                                                   'usuario_seguido': perfil_seguido,
                                                   'usuarios_seguidos': usuarios_seguidos})
    else:
        return HttpResponseRedirect('/')

def seguirUsuario(request, id_usuario):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            perfil = get_object_or_404(models.Usuario, pk=id_usuario)
            if usuario != perfil:
                usuario.seguidos.add(perfil)
                rutas_creadas = models.Ruta.objects.filter(creador=perfil)
                rutas_seguidas = models.Ruta.objects.filter(seguidores=perfil)
                usuarios_seguidos = perfil.seguidos.all()
                return render(request, 'perfil.html', {'usuario': usuario,
                                                       'perfil': perfil,
                                                       'rutas_creadas': rutas_creadas,
                                                       'rutas_seguidas': rutas_seguidas,
                                                       'usuario_seguido':True,
                                                       'usuarios_seguidos':usuarios_seguidos})
            else:

                return HttpResponseRedirect('/'+id_usuario+'/usuario/')
    else:
        return HttpResponseRedirect('/')

def dejarDeSeguirUsuario(request, id_usuario):
    if "usuario" in request.session:
        usuario = models.Usuario.objects.filter(alias=request.session["usuario"])[0]
        if usuario == None:
            return HttpResponseRedirect('/')
        else:
            perfil = get_object_or_404(models.Usuario, pk=id_usuario)
            if usuario != perfil:
                usuario.seguidos.remove(perfil)
                rutas_creadas = models.Ruta.objects.filter(creador=perfil)
                rutas_seguidas = models.Ruta.objects.filter(seguidores=perfil)
                usuarios_seguidos = perfil.seguidos.all()
                return render(request, 'perfil.html', {'usuario': usuario,
                                                       'perfil': perfil,
                                                       'rutas_creadas': rutas_creadas,
                                                       'rutas_seguidas': rutas_seguidas,
                                                       'usuario_seguido':False,
                                                       'usuarios_seguidos':usuarios_seguidos})
    else:
        return HttpResponseRedirect('/')

def recuperarPassword(request):
    if "usuario" in request.session:
        return HttpResponseRedirect('/inicio/')
    else:
        if request.method == "POST":
            form = forms.RecuperarPasswordForm(request.POST)
            # Validación de datos recibidos del formulario
            if form.is_valid():
                try:
                    usuario = models.Usuario.objects.filter(email=request.POST["email"])[0]

                    #Generación de contraseña aleatoria
                    longitud = 10
                    valores = "0123456789abcdefghijklmnopqrstuvwxyz"
                    random = SystemRandom()
                    password = ""

                    while longitud > 0:
                        password = password + random.choice(valores)
                        longitud = longitud - 1

                    usuario.password = password
                    usuario.save()

                    #Envío del email
                    asunto = 'Social Route - envío de contraseñas'
                    contenido = 'Usted ha solicitado un cambio de contraseña. Su contraseña es la siguiente: '+password+ \
                                ' Para cambiar la contraseña, acceda a su perfil y seleccione \'Editar perfil\'.' \
                                'Este mensaje ha sido autogenerado, por favor, NO RESPONDA.'
                    origen='"Social Route" <socialrouteservices@gmail.com>'
                    destino=request.POST["email"]
                    mensaje=EmailMultiAlternatives(asunto, contenido, origen, [destino])
                    mensaje.send()
                    return HttpResponseRedirect('/')
                except IndexError:
                    error = 'No existen usuarios con el email indicado'
                    return render(request, 'recuperarPassword.html', {'form': form,
                                                                      'error': error})

        else:
            form  = forms.RecuperarPasswordForm()
        return render(request, 'recuperarPassword.html', {'form': form})
