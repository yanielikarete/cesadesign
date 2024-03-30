# coding: utf-8
import django_filters
from clientes.models import *

class ClienteFilter(django_filters.FilterSet):
    nombre_cliente = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Cliente
        fields = ['codigo_cliente', 'nombre_cliente', ]


class RazonSocialFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = RazonSocial
        fields = ['codigo_razon_social', 'nombre', ]