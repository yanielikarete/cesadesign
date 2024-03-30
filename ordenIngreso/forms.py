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


class OrdenIngresoForm(forms.ModelForm):
    class Meta:
        model = OrdenIngreso
        fields = ("notas","fecha","codigo","bodega","comentario","created_at","updated_at","created_by","updated_by","orden_produccion_codigo","cliente","imagen","concepto_orden_ingreso")
        widgets = {
            'comentario': Textarea(attrs={'cols': 100, 'rows': 8}),
        }
class OrdenIngresoDetalleForm(forms.ModelForm):
    class Meta:
        model = OrdenIngresoDetalle
        #compra_id,proveedor y fecha se guarda automaticamente de la orden de compra
        exclude = ("orden_ingreso_id","fecha","bodega","recibido","impto2_pciento","impto2_monto","tipo_cambio","moneda","created_at","updated_at","created_by","updated_by")


class IngresoOrdenIngresoForm(forms.ModelForm):
    class Meta:
        model = IngresoOrdenIngreso
        fields = ("codigo","fecha","orden_ingreso","comentario","created_at","updated_at","created_by","updated_by","total")
        widgets = {
            'comentario': Textarea(attrs={'cols': 100, 'rows': 8}),
        }
class ConceptoOrdenIngresoForm(ModelForm):
    class Meta:
        model = ConceptoOrdenIngreso
        exclude = ("created_at","updated_at","created_by","updated_by")