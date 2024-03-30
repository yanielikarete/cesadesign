# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import *
from models import *
from os import path
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import *
from django.core.validators import RegexValidator

from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template import loader
import urllib
import urllib2
import json
import socket
from datetime import datetime


# class ProformaForm(ModelForm):
#     class Meta:
#         model = Proforma
#         exclude = ("proforma_id", "created_at", "updated_at", "created_by", "updated_by")


class RegistroDocumentoForm(ModelForm):
    class Meta:
        model = RegistroDocumento
        exclude = ("registrodoc_id", "created_at", "updated_at", "created_by", "updated_by")


class DocumentoCompraForm(ModelForm):
    class Meta:
        model = DocumentoCompra
        exclude = ("created_at", "updated_at", "created_by", "updated_by")


class DocumentosRetencionCompraForm(ModelForm):
    class Meta:
        model = DocumentosRetencionCompra


class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito


# class RegistrarProforma(forms.ModelForm):
#     numero_documento = forms.CharField(
#         required=True,
#         max_length=10,
#         min_length=1,
#         widget=forms.TextInput(
#             attrs={'min': '0', 'type': 'number', 'class': 'form-control', 'placeholder': 'Número del documento'}),
#         error_messages={
#             'min_length': "Asegúrese de que este valor tenga menos de 1 digito.",
#             'required': "Debe ingresar al menos un digito.",
#         }
#     )
#     vencimiento = forms.CharField(
#         required=False,
#         max_length=10,
#         min_length=1,
#         widget=forms.TextInput(attrs={'value': '0', 'min': '0', 'type': 'number', 'class': 'form-control',
#                                       'placeholder': 'Días de vencimiento'}),
#         error_messages={
#             'min_length': "Asegúrese de que este valor tenga menos de 1 digito.",
#         }
#     )
#
#     class Meta:
#         model = Proforma
#         fields = ('fecha', 'cliente', 'anulada', 'tipo_registro_documento', 'tipo_documento', 'vendedor', 'referencia',
#                   'vencimiento', 'proyecto', 'forma_de_pago', 'atencion', 'garantia')
#         exclude = ("proforma_id", "created_at", "updated_at", "created_by", "updated_by")
#
#     """docstring for RegistrarProforma"""
#
#     def __init__(self, *args, **kwargs):
#         super(RegistrarProforma, self).__init__(*args, **kwargs)
#         self.fields['tipo_registro_documento'].widget.attrs.update({
#             'class': 'form-control'})
#
#         self.fields['tipo_documento'].widget.attrs.update({
#             'class': 'form-control'})
#
#         self.fields['numero_documento'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su número de documento'})
#
#         self.fields['referencia'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su referencia'})
#
#         self.fields['vencimiento'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su vencimiento'})
#
#         self.fields['vendedor'].widget.attrs.update({
#             'class': 'form-control'})
#         self.fields['vendedor'].required = False
#
#         self.fields['proyecto'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su proyecto'})
#
#         self.fields['atencion'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su atención'})
#
#         self.fields['forma_de_pago'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su forma de pago'})
#
#         self.fields['garantia'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su garantia'})
#
#     def save(self, commit=True, request=None):
#         print "Entro a guardar"
#
#         # ================== PROFORMA ==================#
#         proforma = Proforma()
#         proforma.created_by = request.user.get_full_name()
#         proforma.updated_by = request.user.get_full_name()
#         proforma.created_at = datetime.now()
#         proforma.updated_at = datetime.now()
#
#         proforma.tipo_registro_documento = request.POST["tipo_registro_documento"]
#         proforma.tipo_documento = request.POST["tipo_documento"]
#
#
#         fecha = request.POST["fecha_hoy"]
#         print "Fecha: ", fecha
#         fecha = fecha.split('/')
#         print fecha
#         dia = fecha[0]
#         mes = fecha[1]
#         anio = fecha[2]
#         proforma.fecha = str(anio) + '-' + str(mes) + '-' + str(dia)
#         if proforma.tipo_registro_documento == '1':  # Cliente
#             proforma.vendedor = request.POST["vendedor"]
#
#         elif proforma.tipo_registro_documento == '2':  # Proveedor:
#             proforma.numero_documento = request.POST["numero_documento"]
#
#         id_cliente = request.POST["cliente"]
#         proforma.cliente = Cliente.objects.all().get(pk=id_cliente)
#         proforma.referencia = request.POST["referencia"]
#         proforma.vencimiento = request.POST["vencimiento"]
#         proforma.proyecto = request.POST["proyecto"]
#         proforma.atencion = request.POST["atencion"]
#         proforma.forma_de_pago = request.POST["forma_de_pago"]
#         proforma.garantia = request.POST["garantia"]
#         proforma.anulada = request.POST.get("anulada", None)
#         proforma.porcentaje_iva = str(14)  # Porcentaje del IVA
#         proforma.subtotal12 = request.POST["subtotal_14_producto"]
#         proforma.subtotal0 = request.POST["subtotal_0_producto"]
#         proforma.descuento = request.POST["descuento_final_producto"]
#         proforma.iva = request.POST["iva_final_producto"]
#         proforma.total = request.POST["total_final_producto"]
#         proforma.descripcion = request.POST["descripcion"]
#         id_bodega = request.POST["bodega_cesa"]
#         proforma.bodega = Bodega.objects.all().get(pk=id_bodega)
#         proforma.save()
#
#         # ================== PROFORMA DETALLE ==================#
#         contador = int(request.POST["columnas_productos"]) + 1
#
#         for fila in range(0, contador):
#             # ==============  Guardar Productos  ==============#
#             if 'cantidad_producto' + str(fila) in request.POST:
#                 proforma_detalle = ProformaDetalle()
#                 proforma_detalle.created_by = request.user.get_full_name()
#                 proforma_detalle.updated_by = request.user.get_full_name()
#                 proforma_detalle.created_at = datetime.now()
#                 proforma_detalle.updated_at = datetime.now()
#
#                 proforma_detalle.proforma = proforma
#                 proforma_detalle.cantidad = request.POST["cantidad_producto" + str(fila)]
#                 proforma_detalle.tipo = 1
#                 id_producto = request.POST["producto_hidden" + str(fila)]
#                 producto = Producto.objects.get(pk=int(id_producto))
#                 proforma_detalle.producto = producto
#                 proforma_detalle.nombre = request.POST["producto" + str(fila)]
#                 proforma_detalle.detalle = request.POST["producto" + str(fila)]
#                 proforma_detalle.precio_compra = request.POST["precio_unitario_producto" + str(fila)]
#                 proforma_detalle.descto_pciento = request.POST["porc_descuento_producto" + str(fila)]
#                 proforma_detalle.desc = request.POST["descuento_producto" + str(fila)]
#                 proforma_detalle.subtotal = request.POST["subtotal_producto" + str(fila)]
#                 proforma_detalle.save()
#                 print "Guardando cada producto"
#
#         if commit:
#             print "Guardar"
#
#
# class EditarProforma(forms.ModelForm):
#     numero_documento = forms.CharField(
#         required=True,
#         max_length=10,
#         min_length=1,
#         widget=forms.TextInput(
#             attrs={'min': '0', 'type': 'number', 'class': 'form-control', 'placeholder': 'Número del documento'}),
#         error_messages={
#             'min_length': "Asegúrese de que este valor tenga menos de 1 digito.",
#             'required': "Debe ingresar al menos un digito.",
#         }
#     )
#     vencimiento = forms.CharField(
#         required=False,
#         max_length=10,
#         min_length=1,
#         widget=forms.TextInput(attrs={'value': '0', 'min': '0', 'type': 'number', 'class': 'form-control',
#                                       'placeholder': 'Días de vencimiento'}),
#         error_messages={
#             'min_length': "Asegúrese de que este valor tenga menos de 1 digito.",
#         }
#     )
#
#     class Meta:
#         model = Proforma
#         fields = (
#             'cliente', 'anulada', 'tipo_registro_documento', 'tipo_documento', 'vendedor', 'referencia', 'vencimiento',
#             'proyecto', 'forma_de_pago', 'atencion', 'garantia')
#         exclude = ("proforma_id", "created_at", "updated_at", "created_by", "updated_by")
#
#     """docstring for RegistrarProforma"""
#
#     def __init__(self, *args, **kwargs):
#         super(EditarProforma, self).__init__(*args, **kwargs)
#
#         self.fields['tipo_registro_documento'].widget.attrs.update({
#             'class': 'form-control'})
#
#         self.fields['tipo_documento'].widget.attrs.update({
#             'class': 'form-control'})
#
#         self.fields['numero_documento'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su número de documento'})
#
#         self.fields['referencia'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su referencia'})
#
#         self.fields['vencimiento'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su vencimiento'})
#
#         self.fields['vendedor'].widget.attrs.update({
#             'class': 'form-control'})
#         self.fields['vendedor'].required = False
#
#         self.fields['proyecto'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su proyecto'})
#
#         self.fields['atencion'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su atención'})
#
#         self.fields['forma_de_pago'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su forma de pago'})
#
#         self.fields['garantia'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Ingrese su garantia'})
#
#     def clean(self):
#         return self.cleaned_data
#

class DocumentoVentaForm(ModelForm):
    class Meta:
        model = DocumentoVenta
        exclude = ("created_at", "updated_at", "created_by", "updated_by", "retenido")


class DocumentoRetencionVentaForm(ModelForm):
    class Meta:
        model = DocumentoRetencionVenta

