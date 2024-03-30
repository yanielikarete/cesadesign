# coding: utf-8
import django_filters
from .models import *
from config.models import *
#from login.middlewares import ThreadLocal


class ProformaFilter(django_filters.FilterSet):
   
    class Meta:
        model = Proforma
        fields = ['codigo','fecha',]

class CotizacionProformaFilter(django_filters.FilterSet):
   
    class Meta:
        model = CotizacionProforma
        fields = ['codigo','fecha',]