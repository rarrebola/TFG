from django import forms
from django.forms import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

# Definiciones de métodos para las validaciones
def long_minima_8(value):
    if len(value) < 8:
        raise ValidationError(_('Este campo debe tener al menos %(long)s caracteres'),
                              params = {'long': '8'})

def validacion_email(value):
    if '@' not in value or '.' not in value:
        raise ValidationError(_('Introduzca un e-mail válido'))


class RegistroForm(forms.Form):
    alias = forms.CharField(required=True, max_length=20, label=_("Nombre de usuario:"))
    password = forms.CharField(required=True, label=_("Contraseña:"), widget=forms.PasswordInput())


class UsuarioForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    #Esto se ha sacado de aquí: http://stackoverflow.com/questions/17165147/how-can-i-make-a-django-form-field-contain-only-alphanumeric-characters
    alfanumerico = RegexValidator(r'^[0-9a-zA-Z]*$', _('Solo se permiten caracteres alfanuméricos'))

    alias = forms.CharField(label=_("Nombre de usuario:"),max_length=20,validators=[alfanumerico])
    password = forms.CharField(widget=forms.PasswordInput(), label=_("Contraseña:"), validators=[long_minima_8])
    confirmacionPassword = forms.CharField(widget=forms.PasswordInput(), label=_("Confirmación de la contraseña:"), validators=[long_minima_8])
    email = forms.CharField(max_length=50, label=_("Email:"), validators=[validacion_email])
    confirmacionEmail = forms.CharField(max_length=50,label=_("Confirmación del email:"), validators=[validacion_email])


    def clean(self):
        if (self.cleaned_data.get('password') !=
            self.cleaned_data.get('confirmacionPassword')):
                msg = _('Las contraseñas no coinciden')
                self.add_error('confirmacionPassword', msg)

        if (self.cleaned_data.get('email') !=
            self.cleaned_data.get('confirmacionEmail')):
                msg = _('Los emails no coinciden')
                self.add_error('confirmacionEmail', msg)



class RutaForm(forms.Form):
    titulo = forms.CharField(max_length=100, label=_("Título de la ruta:"))
    descripcion = forms.CharField(max_length=1000, widget=forms.Textarea, label=_("Descripción:"))


class DiaForm(forms.Form):
    titulo = forms.CharField(max_length=100, label=_("Título:"))
    descripcion = forms.CharField(max_length=1000, widget=forms.Textarea, label=_("Descripción:"))

class EditarPerfilForm(forms.Form):
    alfanumerico = RegexValidator(r'^[0-9a-zA-Z]*$', _('Solo se permiten caracteres alfanuméricos'))

    alias = forms.CharField(label="Nombre de usuario:", max_length=20, validators=[alfanumerico])
    password = forms.CharField(widget=forms.PasswordInput(), label=_("Antigua contraseña:"), validators=[long_minima_8])
    nuevaPassword = forms.CharField(widget=forms.PasswordInput(), label=_("Nueva contraseña:"),
                                    validators=[long_minima_8])
    confirmacionPassword = forms.CharField(widget=forms.PasswordInput(), label=_("Confirmación de la contraseña:"),
                                           validators=[long_minima_8])
    email = forms.CharField(max_length=50, label=_("Email:"), validators=[validacion_email])
    confirmacionEmail = forms.CharField(max_length=50, label=_("Confirmación del email:"), validators=[validacion_email])


    def clean(self):
        if (self.cleaned_data.get('nuevaPassword') !=
            self.cleaned_data.get('confirmacionPassword')):
                msg = _('Las contraseñas no coinciden')
                self.add_error('confirmacionPassword', msg)

        if (self.cleaned_data.get('email') !=
            self.cleaned_data.get('confirmacionEmail')):
                msg = _('Los emails no coinciden')
                self.add_error('confirmacionEmail', msg)

class RecuperarPasswordForm(forms.Form):
    email = forms.EmailField(max_length=50, label=_("Email:"), validators=[validacion_email])

class CrearLugarInteresForm(forms.Form):
    nombre = forms.CharField(max_length=100, label=_("Nombre"))
    direccion = forms.CharField(max_length=100, label=_("Dirección"))
    localidad = forms.CharField(max_length=30, label=_("Localidad"))
    descripcion = forms.CharField(max_length=1000, label=_("Descripción"), widget=forms.Textarea)
    horario = forms.CharField(max_length=500, label=_("Horario"), widget=forms.Textarea)
    precio = forms.DecimalField(max_digits=8, label= _("Precio"), decimal_places=2)

class EditarLugarInteresForm(forms.Form):
    descripcion = forms.CharField(max_length=1000, label=_("Descripción"), widget=forms.Textarea)
    horario = forms.CharField(max_length=500, label=_("Horario"), widget=forms.Textarea)
    precio = forms.DecimalField(max_digits=8, decimal_places=2)

class ValoracionForm(forms.Form):
    puntuacion = forms.DecimalField(decimal_places=1, max_value=10.0, label=_('Puntuación'))
    comentario = forms.CharField(max_length=1000, widget=forms.Textarea, label=_('Comentario'))