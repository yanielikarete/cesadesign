# coding: utf-8
import django_filters
from .models import *
from config.models import *
#from login.middlewares import ThreadLocal


class PedidoFilter(django_filters.FilterSet):
   
    class Meta:
        model = Pedido
        fields = ['codigo','fecha',]