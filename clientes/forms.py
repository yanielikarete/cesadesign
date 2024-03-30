# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import *
from models import *
from clientes.models import *
from os import path


class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        exclude = ("created_at", "updated_at", "created_by", "direccion3", "balance", "giro_id", "interes_anual",
                   "termino_id", "aplica_2do_impto", "aplica_reten_ica", "segundo_impto", "monto_ult_transac", "fecha_ult_transac",
                   "descri_ult_transac", "aplica_2do_impto", "updated_by", "creado", "registro_empresarial", "registro_tributario",
                   "reten_impto", "reten_ica", "facturar_con", "campo1", "campo2", "campo3", "aplica_reten_impto", "aplica_reten_fuente",
                   "reten_fuente", "aplica_impto", "impto", "impto_incluido","activo")

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['ruc'].label = "RUC o cedula"
        self.fields['retencion_fuente'].queryset = RetencionDetalle.objects.filter(tipo_retencion_id=1)
        self.fields['retencion_iva'].queryset = RetencionDetalle.objects.filter(tipo_retencion_id=2)

class RazonSocialForm(ModelForm):

    class Meta:
        model = RazonSocial
        exclude = ("created_at","updated_at","created_by","direccion3","balance","giro_id","interes_anual","termino_id","aplica_2do_impto","aplica_reten_ica","segundo_impto","monto_ult_transac","fecha_ult_transac","descri_ult_transac","aplica_2do_impto","updated_by","categoria_cliente_id","vendedor_id","creado","registro_empresarial","registro_tributario","reten_impto","reten_ica","facturar_con","campo1","campo2","campo3","aplica_reten_impto","aplica_reten_fuente","reten_fuente","aplica_impto","impto","impto_incluido")

    def __init__(self, *args, **kwargs):
        super(RazonSocialForm, self).__init__(*args, **kwargs)
        self.fields['ruc'].label = "RUC o cedula"
