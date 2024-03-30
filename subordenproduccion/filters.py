# coding: utf-8
import django_filters
from .models import *
from muedirsa.models import *
#from login.middlewares import ThreadLocal


class ProductoFilter(django_filters.FilterSet):
    descripcion_producto = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Producto
        fields = ['codigo_producto','descripcion_producto',]

class CategoriaProductoFilter(django_filters.FilterSet):
    descripcion_categoria = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = CategoriaProducto
        fields = ['codigo_categoria','descripcion_categoria','predeterminado',]

class BodegaFilter(django_filters.FilterSet):
    nombre= django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Bodega
        fields = ['codigo_bodega','nombre',]

class SubCategoriaProductoFilter(django_filters.FilterSet):
    descripcion_sub_categ = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = SubCategoriaProducto
        fields = ['codigo_sub_categ','descripcion_sub_categ',]

class KardexFilter(django_filters.FilterSet):
    nombre= django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Kardex
        fields = ['nro_documento','producto',]

class LoteFilter(django_filters.FilterSet):
    descripcion_sub_categ = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Lote
        fields = ['nro_lote','descripcion_lote',]

class SerialesFilter(django_filters.FilterSet):
    nombre= django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Seriales
        fields = ['nro_serial','producto',]

class UnidadesFilter(django_filters.FilterSet):
    nombre= django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Unidades
        fields = ['abreviatura','descripcion_unidad',]

class TipoProductoFilter(django_filters.FilterSet):
   
    class Meta:
        model = TipoProducto
        fields = ['codigo','descripcion',]

class LineaFilter(django_filters.FilterSet):
   
    class Meta:
        model = Linea
        fields = ['codigo','descripcion',]