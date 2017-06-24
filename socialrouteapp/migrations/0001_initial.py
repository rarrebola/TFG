# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-24 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=1000)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('log', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='LugarInteres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('localidad', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=1000)),
                ('horario', models.CharField(max_length=500)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('puntuacion', models.DecimalField(blank=True, decimal_places=2, max_digits=4)),
                ('dias', models.ManyToManyField(to='socialrouteapp.Dia')),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=1000)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=8)),
                ('puntuacion', models.DecimalField(blank=True, decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('fechaIngreso', models.DateField()),
                ('seguidos', models.ManyToManyField(to='socialrouteapp.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Valoracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateField()),
                ('valoracion', models.DecimalField(decimal_places=2, max_digits=4)),
                ('comentario', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='ValoracionLugarInteres',
            fields=[
                ('valoracion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='socialrouteapp.Valoracion')),
                ('lugarInteres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialrouteapp.LugarInteres')),
            ],
            bases=('socialrouteapp.valoracion',),
        ),
        migrations.CreateModel(
            name='ValoracionRuta',
            fields=[
                ('valoracion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='socialrouteapp.Valoracion')),
            ],
            bases=('socialrouteapp.valoracion',),
        ),
        migrations.AddField(
            model_name='valoracion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialrouteapp.Usuario'),
        ),
        migrations.AddField(
            model_name='ruta',
            name='creador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creador', to='socialrouteapp.Usuario'),
        ),
        migrations.AddField(
            model_name='ruta',
            name='seguidores',
            field=models.ManyToManyField(to='socialrouteapp.Usuario'),
        ),
        migrations.AddField(
            model_name='log',
            name='ruta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialrouteapp.Ruta'),
        ),
        migrations.AddField(
            model_name='log',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialrouteapp.Usuario'),
        ),
        migrations.AddField(
            model_name='dia',
            name='creador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialrouteapp.Usuario'),
        ),
        migrations.AddField(
            model_name='dia',
            name='ruta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialrouteapp.Ruta'),
        ),
        migrations.AddField(
            model_name='valoracionruta',
            name='ruta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialrouteapp.Ruta'),
        ),
        migrations.AlterUniqueTogether(
            name='lugarinteres',
            unique_together=set([('nombre', 'localidad')]),
        ),
    ]
