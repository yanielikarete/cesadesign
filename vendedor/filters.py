# coding: utf-8
import django_filters
from .models import *
from muedirsa.models import *
#from login.middlewares import ThreadLocal


class VendedoresFilter(django_filters.FilterSet):
   
    class Meta:
        model = Vendedor
        fields = ['codigo','nombre']