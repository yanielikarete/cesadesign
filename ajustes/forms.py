# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Textarea
from .models import *
from models import *
from proveedores.models import *
from os import path
from django.views.generic import TemplateView
from django.core.exceptions import NON_FIELD_ERRORS
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from .models import *
from django.shortcuts import render_to_response


class AjustesForm(forms.ModelForm):
    class Meta:
        model = Ajustes
        fields = ("fecha","codigo","bodega","comentario","created_at","updated_at","created_by","updated_by","concepto_ajustes")
        widgets = {
            'comentario': Textarea(attrs={'cols': 100, 'rows': 8}),
        }
class AjustesDetalleForm(forms.ModelForm):
    class Meta:
        model = AjustesDetalle
        #compra_id,proveedor y fecha se guarda automaticamente de la orden de compra
        exclude = ("ajustes_id","fecha","bodega","created_at","updated_at","created_by","updated_by")


#class IngresoOrdenIngresoForm(forms.ModelForm):
#    class Meta:
#        model = IngresoOrdenIngreso
#        fields = ("codigo","fecha","orden_ingreso","comentario","created_at","updated_at","created_by","updated_by","total")
#        widgets = {
#            'comentario': Textarea(attrs={'cols': 100, 'rows': 8}),
#        }

class ConceptoAjustesForm(ModelForm):
    class Meta:
        model = ConceptoAjustes
        exclude = ("created_at","updated_at","created_by","updated_by")