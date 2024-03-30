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

class ConceptoOrdenEgresoForm(ModelForm):
    class Meta:
        model = ConceptoOrdenEgreso
        exclude = ("created_at","updated_at","created_by","updated_by")


class OrdenEgresoForm(forms.ModelForm):
    class Meta:
        model = OrdenEgreso
        fields = ("notas","fecha","codigo","proveedor","bodega","comentario","created_at","updated_at","created_by","updated_by","nro_fact_proveedor","total","orden_produccion_codigo","subtotal","aprobada","anulado","concepto_orden_egreso")
        widgets = {
            'comentario': Textarea(attrs={'cols': 100, 'rows': 8}),
        }
class OrdenEgresoDetalleForm(forms.ModelForm):
    class Meta:
        model = OrdenEgresoDetalle
        #compra_id,proveedor y fecha se guarda automaticamente de la orden de compra
        exclude = ("orden_egreso_id","fecha","proveedor","bodega","recibido","impto2_pciento","impto2_monto","tipo_cambio","moneda","created_at","updated_at","created_by","updated_by")


class EgresoOrdenEgresoForm(forms.ModelForm):
    class Meta:
        model = EgresoOrdenEgreso
        fields = ("codigo","fecha","orden_egreso","comentario","created_at","updated_at","created_by","updated_by","total","proveedor")
        widgets = {
            'comentario': Textarea(attrs={'cols': 100, 'rows': 8}),
        }


