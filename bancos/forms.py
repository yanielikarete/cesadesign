# -*- coding: utf-8 -*-
from django import forms
from clientes.models import *
from .models import *

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        exclude = ("id","created_at", "updated_at", "created_by", "updated_by","estado")


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento


class ChequePrestadoForm(forms.ModelForm):
    class Meta:
        model = ChequesProtestados


class ConciliacionForm(forms.ModelForm):
    class Meta:
        model = Conciliacion

    def __init__(self, *args, **kwargs):
        super(ConciliacionForm, self).__init__(*args, **kwargs)


class ChequesNoCobradosForm(forms.ModelForm):
    class Meta:
        model = ChequesNoCobrados

