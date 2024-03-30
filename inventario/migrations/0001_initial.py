# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import colegio.models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('categoria_id', models.AutoField( serialize=False, auto_created=True, primary_key=True)),
                ('codigo_categoria', models.CharField(max_length=10)),
                ('descripcion_categoria', models.CharField(max_length=255)),
                ('predeterminado', models.IntegerField()),
                ('nro_productos', models.IntegerField()),
                ('imagen_categoria', models.CharField(max_length=255)),
                ('activo', models.BooleanField(default=True, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['codigo_categoria'],
                'verbose_name': 'CategoriaProducto',
                
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubCategoriaProducto',
            fields=[
                ('sub_categoria_producto_id', models.AutoField( serialize=False, auto_created=True, primary_key=True)),
                ('codigo_sub_categ', models.CharField(max_length=10)),
                ('categoria', models.ForeignKey(verbose_name='CategoriaProducto', to='inventario.CategoriaProducto')),
                ('descripcion_sub_categ', models.CharField(max_length=255)),
                ('predeterminado', models.IntegerField()),
                ('nro_productos', models.IntegerField()),
                ('imagen_subcateg', models.CharField(max_length=255)),
                ('activo', models.BooleanField(default=True, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['codigo_sub_categ'],
               
            },
            bases=(models.Model,),
        ),

      
    ]
