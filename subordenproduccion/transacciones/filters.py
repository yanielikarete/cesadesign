# coding: utf-8
import django_filters
from .models import *


# class ProformaFilter(django_filters.FilterSet):
#     class Meta:
#         model = Proforma
#         fields = ['fecha', 'cliente', 'referencia', ]
#

class RegistroDocumentoFilter(django_filters.FilterSet):
    class Meta:
        model = RegistroDocumento
        fields = ['fecha', 'cliente' ]
