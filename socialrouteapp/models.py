from django.db import models

# Create your models here.
class Usuario(models.Model):
    alias = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    fechaIngreso = models.DateField()
    seguidos = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return self.alias


class Ruta(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000)
    precio = models.DecimalField(blank=True, decimal_places=2, max_digits=8)
    puntuacion = models.DecimalField(blank=True, decimal_places=2, max_digits=4)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='creador')
    seguidores = models.ManyToManyField(Usuario)

    def __str__(self):
        return self.titulo

class Dia(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000)
    precio = models.DecimalField(blank=True, decimal_places=2, max_digits=6)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    #Esta función se usa para recuperar los días pertenecientes a una ruta
    def dias_ruta(ruta):
        dias = []
        for dia in Dia.objects.all():
            if dia.ruta == ruta:
                dias.append(dia)
        return dias

    def __str__(self):
        return self.titulo+", "+self.ruta.titulo

class LugarInteres(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    localidad = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=1000)
    horario = models.CharField(max_length=500)
    precio = models.DecimalField(decimal_places=2, max_digits=6)
    puntuacion = models.DecimalField(blank=True, decimal_places=2, max_digits=4)
    dias = models.ManyToManyField(Dia)

    def __str__(self):
        return self.nombre

    class Meta:
        unique_together = ('nombre', 'localidad')

class Valoracion(models.Model):
    fechaCreacion = models.DateField()
    valoracion = models.DecimalField(decimal_places=2, max_digits=4)
    comentario = models.CharField(max_length=1000)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.valoracion)

class ValoracionRuta(Valoracion):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)

    def valoraciones_ruta(ruta):
        valoraciones = []
        for valoracion in ValoracionRuta.objects.all():
            if valoracion.ruta == ruta:
                valoraciones.append(valoracion)
        return valoraciones

class ValoracionLugarInteres(Valoracion):
    lugarInteres = models.ForeignKey(LugarInteres, on_delete=models.CASCADE)

    def valoraciones_lugar_interes(lugar_interes):
        valoraciones = []
        for valoracion in ValoracionLugarInteres.objects.all():
            if valoracion.lugarInteres == lugar_interes:
                valoraciones.append(valoracion)
        return valoraciones

class Log(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    log = models.CharField(max_length=10)

    def __str__(self):
        return self.usuario + " " + self.ruta + " " +self.fecha