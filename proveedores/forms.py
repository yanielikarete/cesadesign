# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import *
from models import *
from os import path
from contabilidad.models import *


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        exclude = ( "activo", )

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        self.fields['retencion_fuente'].queryset = RetencionDetalle.objects.filter(tipo_retencion_id=1)
        self.fields['retencion_iva'].queryset = RetencionDetalle.objects.filter(tipo_retencion_id=2)
        self.fields['cuenta_gasto'].queryset = PlanDeCuentas.objects.filter(categoria="DETALLE",activo=True)
        self.fields['cuenta_anticipo'].queryset = PlanDeCuentas.objects.filter(categoria="DETALLE",activo=True)
        self.fields['cuenta_contable_compra'].queryset = PlanDeCuentas.objects.filter(categoria="DETALLE",activo=True)
