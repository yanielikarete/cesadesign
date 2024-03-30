# coding: utf-8
import django_filters
from .models import *

class GuiaRemisionFilter(django_filters.FilterSet):
    nro_guia = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = GuiaRemision
        fields = ['nro_guia', 'cliente', 'chofer', 'fecha_inicio', 'fecha_fin', ]

# class FacturaFilter(django_filters.FilterSet):
#     nro_guia = django_filters.CharFilter(lookup_type='icontains')
#    
#     class Meta:
#         model = Factura
#         fields = ['nro_factura', 'cliente', 'vendedor', ]
# 
# class NotaCreditoFilter(django_filters.FilterSet):
#     nro_guia = django_filters.CharFilter(lookup_type='icontains')
#    
#     class Meta:
#         model = NotaCredito
#         fields = ['nro_nota_credito', 'cliente', 'vendedor', ]