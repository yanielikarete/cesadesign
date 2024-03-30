# -*- encoding: utf-8 -*-
import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404

from bancos.forms import MovimientoForm
from login.lib.tools_view import ObjectListView, ObjectDetailView, eliminarView, eliminarByPkView
from django.http import HttpResponse
from .forms import *
from .tables import *
from .filters import *
from decimal import Decimal
from django.template import loader
from django.db import connection
import simplejson as json

from .models import *
from bancos.models import *
from inventario.models import *
from reunion.models import *
from config.models import *
from clientes.models import *
from ambiente.models import *
from contabilidad.models import *
from transacciones.models import *
from proforma.models import *
from retenciones.models import *
from django.utils.encoding import smart_str
from django.contrib import messages
from django.shortcuts import resolve_url, get_object_or_404
from django.db import transaction, DatabaseError
from django.template.loader import render_to_string
from django import template

import cgi
import logging

# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
now = datetime.now()
register = template.Library()


@register.filter
def to_and(value):
    return value.replace(",", ".")


# =========================Proforma============================#

"""
Funcion:        transacciones-register-proforma
Autor:          Jose Velez Gomez
Descripcion:    Esta funcion registra una proforma
Estado:         TERMINADA
"""


@login_required()
def transacciones_register_proforma(request):
    if request.method == 'POST':
        proforma_register_form = RegistrarProforma(request.POST)

        if proforma_register_form.is_valid():
            opts = {
                'request': request,
            }
            proforma_register_form.save(**opts)
            # messages.success(request, 'La proforma se creo con exito')
            return HttpResponseRedirect('/proforma/proformafactura')
        else:
            form_errors = proforma_register_form.errors
            print form_errors, len(form_errors)
    else:
        proforma_register_form = RegistrarProforma()

    clientes = Cliente.objects.all()
    bodegas = Bodega.objects.all()
    productos = Producto.objects.filter(tipo_producto=2)
    centro_costos = CentroCosto.objects.all()
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    formas_pago = FormaPago.objects.all()

    return render_to_response('proformas/trans_registrar_proforma.html',
                              {'proforma_register_form': proforma_register_form,
                               'bodegas': bodegas,
                               'productos': productos,
                               'centro_costos': centro_costos,
                               'clientes': clientes,
                               'cuentas': cuentas,
                               'formas_pago': formas_pago}, RequestContext(request))


"""
Funcion:        transacciones_consult_proforma
Autor:          Jose Velez Gomez
Descripcion:    Esta funcion registra una proforma
Estado:         TERMINADA
"""


@login_required()
def transacciones_consult_proforma(request):
    print "nuevo"
    if request.method == 'POST':
        proformas = Proforma.objects.all()
        return render_to_response('proformas/trans_consultar_proforma.html', {'proformas': proformas},
                                  RequestContext(request))
    else:
        proformas = Proforma.objects.all()
        return render_to_response('proformas/trans_consultar_proforma.html', {'proformas': proformas},
                                  RequestContext(request))


"""
Funcion:        transacciones_update_proforma
Autor:          Jose Velez Gomez
Descripcion:    Esta funcion registra una proforma
Estado:         En proceso
"""


# @login_required()
# def transacciones_update_proforma(request, id_proforma):
#     print "Jose", id_proforma
#     proforma = Proforma.objects.get(pk=id_proforma)
#     # proforma = get_object_or_404(Proforma, pk = id_proforma)
#     detalles = ProformaDetalle.objects.filter(proforma_id=id_proforma)
#     bodega_select = Bodega.objects.get(pk=proforma.bodega_id)
#     fila = len(detalles) - 1
#
#     if request.method == 'POST':
#         POST = request.POST.copy()
#         proforma_register_form = EditarProforma(POST, instance=proforma)
#
#         if proforma_register_form.is_valid():
#             print "Actualizando"
#             proforma_register_form.save()
#             return HttpResponseRedirect('/proforma/proformafactura/consultar')
#         else:
#             print "NO Actualizando"
#             form_errors = proforma_register_form.errors
#             print form_errors, len(form_errors)
#     else:
#
#         print  "NOOOOOOOO"
#         proforma_register_form = EditarProforma()
#
#     clientes = Cliente.objects.all()
#     bodegas = Bodega.objects.all()
#     productos = Producto.objects.filter(tipo_producto=2)
#     centro_costos = CentroCosto.objects.all()
#     cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
#     formas_pago = FormaPago.objects.all()
#
#     return render_to_response('proformas/trans_actualizar_proforma.html',
#                               {'proforma_register_form': proforma_register_form,
#                                'bodegas': bodegas,
#                                'productos': productos,
#                                'centro_costos': centro_costos,
#                                'clientes': clientes,
#                                'cuentas': cuentas,
#                                'formas_pago': formas_pago,
#                                'proforma': proforma,
#                                'detalles': detalles,
#                                'fila': fila,
#                                'bodega_select': bodega_select,
#                                'id_proforma': id_proforma}, RequestContext(request))
#
#     def replace_semicolon(value):
#         return value.replace(",", ".")
#
#
# class ProformaListView(ObjectListView):
#     model = Proforma
#     paginate_by = 100
#     template_name = 'proforma/indice.html'
#     table_class = ProformaTable
#     filter_class = ProformaFilter
#
#     def get_context_data(self, **kwargs):
#         context = super(ProformaListView, self).get_context_data(**kwargs)
#         context['url_delete'] = reverse_lazy('proforma-delete')
#         return context
#
#
# class ProformaDetailView(ObjectDetailView):
#     model = Proforma
#     template_name = 'proforma/detail.html'
#
#
# def ProformaCreateView(request):
#     if request.method == 'POST':
#         proforma_form = ProformaForm(request.POST)
#         cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
#         centros = CentroCosto.objects.all()
#         productos = Producto.objects.all()
#         retiva = TipoRetencion.objects.filter(impuesto="iva")
#         retir = TipoRetencion.objects.filter(impuesto="ir")
#         if proforma_form.is_valid():
#             new_proforma = proforma_form.save(commit=False)
#             new_proforma.created_by = request.user.get_full_name()
#             new_proforma.updated_by = request.user.get_full_name()
#             new_proforma.created_at = datetime.now()
#             new_proforma.updated_at = datetime.now()
#             new_proforma.subtotal12 = request.POST["subtotal12"]
#             new_proforma.subtotal0 = request.POST["subtotal0"]
#             new_proforma.descuento = request.POST["descuento"]
#             new_proforma.iva = request.POST["iva"]
#             new_proforma.total = request.POST["total"]
#             new_proforma.save()
#             try:
#                 secuencial = Secuenciales.objects.get(modulo='proformac')
#                 secuencial.secuencial = secuencial.secuencial + 1
#                 secuencial.created_by = request.user.get_full_name()
#                 secuencial.updated_by = request.user.get_full_name()
#                 secuencial.created_at = datetime.now()
#                 secuencial.updated_at = datetime.now()
#                 secuencial.save()
#             except Secuenciales.DoesNotExist:
#                 secuencial = None
#
#             contador = request.POST["columnas_receta"]
#             print contador
#             i = 0
#             while int(i) <= int(contador):
#                 i += 1
#                 if int(i) > int(contador):
#                     print('entrosd')
#                     break
#                 else:
#                     if 'id_producto_kits' + str(i) in request.POST:
#                         proformadetalle = ProformaDetalle()
#                         proformadetalle.proforma = new_proforma
#                         proformadetalle.tipo = ProformaDetalle.PRODUCTO
#                         proformadetalle.cantidad = request.POST["cantidad_kits" + str(i)]
#                         proformadetalle.producto = Producto.objects.get(pk=request.POST["id_producto_kits" + str(i)])
#                         proformadetalle.centro = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])
#                         proformadetalle.valor = request.POST["precio_kits" + str(i)]
#                         if request.POST['id_retir_kits' + str(i)] != "":
#                             proformadetalle.retencion_ir = TipoRetencion.objects.get(
#                                 pk=request.POST["id_retir_kits" + str(i)])
#                         # if request.POST['id_retiva_kits'+str(i) != "":
#                         #	proformadetalle.retencion_iva = TipoRetencion.objects.get(pk=request.POST["id_retiva_kits"+str(i)])
#                         proformadetalle.desc = request.POST["descuento_kits" + str(i)]
#                         proformadetalle.subtotal = request.POST["subtotal_kits" + str(i)]
#                         proformadetalle.save()
#
#                 print(i)
#                 print('contadorsd prueba' + str(contador))
#
#             contador = request.POST["columnas_cuenta"]
#             i = 0
#             while int(i) <= int(contador):
#                 i += 1
#                 if int(i) > int(contador):
#                     print('entrosd')
#                     break
#                 else:
#                     if 'id_cuenta_cuenta' + str(i) in request.POST:
#                         proformadetalle = ProformaDetalle()
#                         proformadetalle.proforma = new_proforma
#                         proformadetalle.tipo = ProformaDetalle.CUENTA
#                         proformadetalle.cantidad = request.POST["cantidad_cuenta" + str(i)]
#                         proformadetalle.cuenta = PlanDeCuentas.objects.get(pk=request.POST["id_cuenta_cuenta" + str(i)])
#                         proformadetalle.centro = CentroCosto.objects.get(pk=request.POST["id_centro_cuenta" + str(i)])
#                         proformadetalle.valor = request.POST["precio_cuenta" + str(i)]
#                         # if request.POST['id_retir_cuenta'+str(i)] != ""
#                         #	proformadetalle.retencion_ir = TipoRetencion.objects.get(pk=request.POST["id_retir_cuenta"+str(i)])
#                         # if request.POST['id_retiva_cuenta'+str(i)] != "":
#                         #	proformadetalle.retencion_iva = TipoRetencion.objects.get(pk=request.POST["id_retiva_cuenta"+str(i)])
#                         proformadetalle.desc = request.POST["descuento_cuenta" + str(i)]
#                         proformadetalle.subtotal = request.POST["subtotal_cuenta" + str(i)]
#                         proformadetalle.saldo = Decimal('0')
#                         proformadetalle.saldo_cobrar = Decimal('0')
#                         proformadetalle.save()
#                 print(i)
#                 print('contadorsd prueba' + str(contador))
#
#             return HttpResponseRedirect('/transacciones/proforma')
#         else:
#             print 'error'
#             print proforma_form.errors, len(proforma_form.errors)
#     else:
#         proforma_form = ProformaForm
#         cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
#         centros = CentroCosto.objects.all()
#         productos = Producto.objects.all()
#         retiva = TipoRetencion.objects.filter(impuesto="iva")
#         retir = TipoRetencion.objects.filter(impuesto="ir")
#     return render_to_response('proforma/crear.html',
#                               {'proforma_form': proforma_form, 'cuentas': cuentas, 'centros': centros,
#                                'productos': productos, 'retir': retir, 'retiva': retiva}, RequestContext(request))
#
#
# def ProformaUpdateView(request, pk):
#     if request.method == 'POST':
#         proforma = Proforma.objects.get(proforma_id=pk)
#         proforma_form = ProformaForm(request.POST, request.FILES, instance=proforma)
#         print proforma_form.is_valid(), proforma_form.errors, type(proforma_form.errors)
#
#         if proforma_form.is_valid():
#             proforma = proforma_form.save()
#
#             return HttpResponseRedirect('/transacciones/proforma')
#         else:
#
#             proforma_form = ProformaForm(request.POST)
#             detalle = ProformaDetalle.objects.filter(proforma=proforma.proforma_id)
#
#             context = {
#                 'section_title': 'Actualizar Proforma',
#                 'button_text': 'Actualizar',
#                 'proforma_form': proforma_form,
#                 'detalle': detalle}
#
#         return render_to_response(
#             'proforma/detalle.html',
#             context,
#             context_instance=RequestContext(request))
#     else:
#         proforma = Proforma.objects.get(proforma_id=pk)
#         proforma_form = ProformaForm(instance=proforma)
#         detalle = ProformaDetalle.objects.filter(proforma=proforma)
#
#         context = {
#             'section_title': 'Actualizar Proforma',
#             'button_text': 'Actualizar',
#             'proforma_form': proforma_form,
#             'detalle': detalle}
#
#         return render_to_response(
#             'proforma/detalle.html',
#             context,
#             context_instance=RequestContext(request))
#
#
# @login_required()
# def proformaEliminarView(request):
#     return eliminarView(request, Proforma, 'proforma-list')
#
#
# @login_required()
# def proformaEliminarByPkView(request, pk):
#     return eliminarByPkView(request, pk, Proforma)


# =========================RegistroDocumento============================#

class RegistroDocumentoListView(ObjectListView):
    model = RegistroDocumento
    paginate_by = 100
    template_name = 'registrodocumento/indice.html'
    table_class = RegistroDocumentoTable
    filter_class = RegistroDocumentoFilter

    def get_context_data(self, **kwargs):
        context = super(RegistroDocumentoListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('registroDocumento-delete')
        return context


class RegistroDocumentoDetailView(ObjectDetailView):
    model = RegistroDocumento
    template_name = 'registrodocumento/detail.html'


def RegistroDocumentoCreateView(request):
    if request.method == 'POST':
        registroDocumento_form = RegistroDocumentoForm(request.POST)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.all()
        if registroDocumento_form.is_valid():
            new_registroDocumento = registroDocumento_form.save()
            new_registroDocumento.created_by = request.user.get_full_name()
            new_registroDocumento.updated_by = request.user.get_full_name()
            new_registroDocumento.created_at = datetime.now()
            new_registroDocumento.updated_at = datetime.now()
            new_registroDocumento.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='registroDocumentoc')
                secuencial.secuencial = secuencial.secuencial + 1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            contador = request.POST["columnas_receta"]
            print contador
            i = 0
            while int(i) <= int(contador):
                i += 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_producto_kits' + str(i) in request.POST:
                        registroDocumentodetalle = RegistroDocumentoDetalle()
                        registroDocumentodetalle.registroDocumento = new_registroDocumento
                        registroDocumentodetalle.tipo = RegistroDocumentoDetalle.PRODUCTO
                        registroDocumentodetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                        registroDocumentodetalle.producto = Producto.objects.get(
                            pk=request.POST["id_producto_kits" + str(i)])
                        registroDocumentodetalle.centro = CentroCosto.objects.get(
                            pk=request.POST["id_centro_kits" + str(i)])
                        registroDocumentodetalle.valor = request.POST["precio_kits" + str(i)]
                        registroDocumentodetalle.retencion_ir = TipoRetencion.objects.get(
                            pk=request.POST["id_retir_kits" + str(i)])
                        registroDocumentodetalle.retencion_iva = TipoRetencion.objects.get(
                            pk=request.POST["id_retiva_kits" + str(i)])
                        registroDocumentodetalle.desc = request.POST["descuento_kits" + str(i)]
                        registroDocumentodetalle.subtotal = request.POST["subtotal_kits" + str(i)]
                        registroDocumentodetalle.save()

                print(i)
                print('contadorsd prueba' + str(contador))

            contador = request.POST["columnas_cuenta"]
            i = 0
            while int(i) <= int(contador):
                i += 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_cuenta_cuenta' + str(i) in request.POST:
                        registroDocumentodetalle = RegistroDocumentoDetalle()
                        registroDocumentodetalle.registroDocumento = new_registroDocumento
                        registroDocumentodetalle.tipo = RegistroDocumentoDetalle.CUENTA
                        registroDocumentodetalle.cantidad = request.POST["cantidad_cuenta" + str(i)]
                        registroDocumentodetalle.cuenta = PlanDeCuentas.objects.get(
                            pk=request.POST["id_cuenta_cuenta" + str(i)])
                        registroDocumentodetalle.centro = CentroCosto.objects.get(
                            pk=request.POST["id_centro_cuenta" + str(i)])
                        registroDocumentodetalle.valor = request.POST["precio_cuenta" + str(i)]
                        registroDocumentodetalle.retencion_ir = TipoRetencion.objects.get(
                            pk=request.POST["id_retir_cuenta" + str(i)])
                        registroDocumentodetalle.retencion_iva = TipoRetencion.objects.get(
                            pk=request.POST["id_retiva_cuenta" + str(i)])
                        registroDocumentodetalle.desc = request.POST["descuento_cuenta" + str(i)]
                        registroDocumentodetalle.subtotal = request.POST["subtotal_cuenta" + str(i)]
                        registroDocumentodetalle.save()
                print(i)
                print('contadorsd prueba' + str(contador))

            return HttpResponseRedirect('/transacciones/registroDocumento')
        else:
            print 'error'
            print registroDocumento_form.errors, len(registroDocumento_form.errors)
    else:
        registroDocumento_form = RegistroDocumentoForm
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.all()
        productos = Producto.objects.all()
        retiva = TipoRetencion.objects.filter(impuesto="iva")
        retir = TipoRetencion.objects.filter(impuesto="ir")
    return render_to_response('registrodocumento/crear.html',
                              {'registroDocumento_form': registroDocumento_form, 'cuentas': cuentas, 'centros': centros,
                               'productos': productos, 'retir': retir, 'retiva': retiva}, RequestContext(request))


def RegistroDocumentoUpdateView(request, pk):
    if request.method == 'POST':
        registroDocumento = RegistroDocumento.objects.get(registroDocumento_id=pk)
        registroDocumento_form = RegistroDocumentoForm(request.POST, request.FILES, instance=registroDocumento)
        print registroDocumento_form.is_valid(), registroDocumento_form.errors, type(registroDocumento_form.errors)

        if registroDocumento_form.is_valid():
            registroDocumento = registroDocumento_form.save()

            return HttpResponseRedirect('/transacciones/registroDocumento')
        else:

            registroDocumento_form = RegistroDocumentoForm(request.POST)
            detalle = RegistroDocumentoDetalle.objects.filter(registroDocumento=registroDocumento.registroDocumento_id)

            context = {
                'section_title': 'Actualizar RegistroDocumento',
                'button_text': 'Actualizar',
                'registroDocumento_form': registroDocumento_form,
                'detalle': detalle}

        return render_to_response(
            'registrodocumento/detalle.html',
            context,
            context_instance=RequestContext(request))
    else:
        registroDocumento = RegistroDocumento.objects.get(registroDocumento_id=pk)
        registroDocumento_form = RegistroDocumentoForm(instance=registroDocumento)
        detalle = RegistroDocumentoDetalle.objects.filter(registroDocumento=registroDocumento)

        context = {
            'section_title': 'Actualizar RegistroDocumento',
            'button_text': 'Actualizar',
            'registroDocumento_form': registroDocumento_form,
            'detalle': detalle}

        return render_to_response(
            'registrodocumento/detalle.html',
            context,
            context_instance=RequestContext(request))


@login_required()
def registroDocumentoEliminarView(request):
    return eliminarView(request, RegistroDocumento, 'registrodocumento-list')


@login_required()
def registroDocumentoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, RegistroDocumento)


# =========================Deposito============================#


@login_required()
def deposito_list_view(request):
    movimientos = Movimiento.objects.all()
    template = loader.get_template('deposito/index.html')
    context = RequestContext(request, {'movimientos': movimientos})
    return HttpResponse(template.render(context))


@login_required()
def deposito_nuevo_view(request):
    bancos = Banco.objects.all()
    form = DepositoForm
    template = loader.get_template('deposito/create.html')
    context = RequestContext(request, {'form': form, 'bancos': bancos})
    return HttpResponse(template.render(context))


@login_required()
def deposito_crear_view(request):
    if request.method == 'POST':
        form = DepositoForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            deposito = Deposito()
            deposito.fecha_corte = cleaned_data.get('fecha_corte')
            deposito.fecha = cleaned_data.get('fecha')
            deposito.banco_id = int(cleaned_data.get('banco').id)
            deposito.numero_comprobante = cleaned_data.get('numero_comprobante')
            deposito.total = cleaned_data.get('total')
            deposito.descripcion = cleaned_data.get('descripcion')
            deposito.save()
        return HttpResponseRedirect('/transacciones/deposito')


@login_required()
def deposito_edit_view(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.all()
    bancos = Banco.objects.all()
    clientes = Cliente.objects.all()
    template = loader.get_template('movimientos/edit.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos,
                                       'tipo_documentos': tipo_documentos, 'clientes': clientes, 'bancos': bancos})
    return HttpResponse(template.render(context))


@login_required()
def deposito_update_view(request, pk):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            movimiento = Movimiento.objects.get(pk=pk)
            movimiento.tipo_anticipo = cleaned_data.get('tipo_anticipo')
            movimiento.tipo_anticipo_documento = cleaned_data.get('tipo_anticipo_documento')
            movimiento.fecha_emision = cleaned_data.get('fecha_emision')
            movimiento.cuenta_bancaria = int(cleaned_data.get('cuenta_bancaria'))
            movimiento.persona = int(cleaned_data.get('persona'))
            movimiento.paguese_a = cleaned_data.get('paguese_a')
            movimiento.numero_cheque = cleaned_data.get('numero_cheque')
            movimiento.fecha_cheque = cleaned_data.get('fecha_cheque')
            movimiento.descripcion = cleaned_data.get('descripcion')
            movimiento.numero_comprobante = cleaned_data.get('numero_comprobante')
            movimiento.save()
        return HttpResponseRedirect('/bancos/movimiento')


# =========================Documento============================#

# ============Compra=============#
@login_required()
def documento_list_view(request):
    compras = DocumentoCompra.objects.all().order_by('-fecha_emision')
    template = loader.get_template('compra/index.html')
    context = RequestContext(request, {'compras': compras})
    return HttpResponse(template.render(context))


"""
Funcion:        documento_nuevo_view
Autor:          GAPH
Descripcion:    Esta funcion registra una factura de proveedor (compra)
"""


@login_required()
def documento_nuevo_view(request):
    proveedores = Proveedor.objects.filter(activo=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True, categoria="DETALLE")
    sustento = SustentoTributario.objects.all()
    retenciones_fuente = RetencionDetalle.objects.filter(tipo_retencion_id=1)
    retenciones_iva = RetencionDetalle.objects.filter(tipo_retencion_id=2)
    porcentaje_iva = Parametros.objects.get(clave='iva').valor
    formas_pago = SriFormaPago.objects.all()
    centros = CentroCosto.objects.filter(activo=True).exclude(padre_id__isnull=True)
    form = DocumentoCompraForm
    template = loader.get_template('compra/create.html')
    context = RequestContext(request, {'form': form, 'centros': centros, 'proveedores': proveedores,
                                       'sustento': sustento, 'retenciones_iva': retenciones_iva,
                                       'retenciones_fuente': retenciones_fuente,
                                       'cuentas': cuentas, 'formas_pago': formas_pago,
                                       'porcentaje_iva': porcentaje_iva})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def documento_compra_edit_view(request, pk):
    documento = DocumentoCompra.objects.get(id=pk)
    cuentas = PlanDeCuentas.objects.filter(activo=True, categoria="DETALLE")
    sustento = SustentoTributario.objects.all()
    retenciones_fuente = RetencionDetalle.objects.filter(tipo_retencion_id=1)
    retenciones_iva = RetencionDetalle.objects.filter(tipo_retencion_id=2)
    porcentaje_iva = Parametros.objects.get(clave='iva').valor
    formas_pago = SriFormaPago.objects.all()
    centros = CentroCosto.objects.filter(activo=True).exclude(padre_id__isnull=True)
    proveedores = Proveedor.objects.filter(activo=True)
    form = DocumentoCompraForm(request.POST, request.FILES, instance=documento)
    print retenciones_fuente

    template = loader.get_template('compra/edit.html')
    context = RequestContext(request, {'form': form, 'centros': centros, 'proveedores': proveedores,
                                       'sustento': sustento, 'retenciones_iva': retenciones_iva,
                                       'retenciones_fuente': retenciones_fuente,
                                       'cuentas': cuentas, 'formas_pago': formas_pago,
                                       'porcentaje_iva': porcentaje_iva, 'documento': documento})
    return HttpResponse(template.render(context))


@login_required()
def consultar_documento_asiento_view(request):
    if request.method == "POST" and request.is_ajax:
        asiento_id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT a.*,p.nombre_plan,p.codigo_plan FROM contabilidad_asientodetalle a,contabilidad_plandecuentas p WHERE a.cuenta_id=p.plan_id AND a.asiento_id = ' + (
        asiento_id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def consultar_documento_retencion_view(request):
    if request.method == "POST" and request.is_ajax:
        documento_id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT r.establecimiento, r.punto_emision,r.secuencial,r.autorizacion,r.descripcion, to_char(r.fecha_emision, \'YYYY-MM-DD\') as fecha_emision , d.retencion_detalle_id,o.codigo,o.descripcion,d.base_imponible,d.porcentaje_retencion,d.valor_retenido,o.tipo_retencion_id,o.cuenta_id' \
                ' FROM documento_retencion_compra r,documento_retencion_detalle_compra d,retencion_detalle o ' \
                'WHERE d.documento_retencion_compra_id=r.id AND o.id=d.retencion_detalle_id AND r.documento_compra_id = ' + (
                documento_id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
@transaction.atomic()
def documento_compra_crear_view(request):
    if request.method == 'POST':
        form = DocumentoCompraForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    cleaned_data = form.cleaned_data
                    documento = DocumentoCompra()
                    documento.created_by = request.user.get_full_name()
                    documento.updated_by = request.user.get_full_name()
                    documento.created_at = datetime.now()
                    documento.updated_at = datetime.now()
                    documento.fecha_emision = cleaned_data.get('fecha_emision')
                    documento.fecha_vencimiento = cleaned_data.get('fecha_vencimiento')
                    documento.proveedor = cleaned_data.get('proveedor')
                    documento.orden_compra = cleaned_data.get('orden_compra')
                    documento.establecimiento = cleaned_data.get('establecimiento')
                    documento.punto_emision = cleaned_data.get('punto_emision')
                    documento.secuencial = cleaned_data.get('secuencial')
                    documento.autorizacion = cleaned_data.get('autorizacion')
                    documento.descripcion = cleaned_data.get('descripcion')
                    documento.base_iva_0 = request.POST['base_iva_0_factura']
                    documento.base_iva = request.POST['base_iva_factura']
                    documento.valor_iva = request.POST['valor_iva_factura']
                    documento.porcentaje_iva = cleaned_data.get('porcentaje_iva')
                    documento.base_ice = cleaned_data.get('base_ice')
                    documento.valor_ice = cleaned_data.get('valor_ice')
                    documento.porcentaje_ice = cleaned_data.get('porcentaje_ice')
                    documento.descuento = cleaned_data.get('descuento')
                    documento.total = request.POST['total_factura']
                    documento.tipo_provision = cleaned_data.get('tipo_provision')
                    documento.pagado = False
                    documento.sustento_tributario = cleaned_data.get('sustento_tributario')
                    documento.sri_forma_pago_id = request.POST['forma_pago']
                    documento.save()

                    asientos = json.loads(request.POST['arreglo_asientos'])
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        asiento = Asiento()
                        asiento.codigo_asiento = "P" + str(now.year) + "000" + str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'FACTURA COMPRAS ' + str(documento.proveedor.nombre_proveedor.encode('utf8')) + str(
                            documento.establecimiento) + '-' + str(documento.punto_emision) + '-' + str(
                            documento.secuencial)
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe = request.POST['asiento-total-debe']
                        total_haber = request.POST['asiento-total-haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.save()

                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)

                        for item_asiento in asientos:
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            if int(item_asiento['centro_id']) != 0:
                                asiento_detalle.centro_costo_id = item_asiento['centro_id']
                            asiento_detalle.save()

                        documento.asiento = asiento
                        documento.save()

                    retenciones = json.loads(request.POST['arreglo_retenciones'])
                    if len(retenciones) > 0:
                        documento_retencion_compra = DocumentosRetencionCompra()
                        documento_retencion_compra.documento_compra_id = int(documento.id)
                        documento_retencion_compra.fecha_emision = request.POST['retencion-fecha-emision']
                        documento_retencion_compra.establecimiento = request.POST['retencion-establecimiento']
                        documento_retencion_compra.punto_emision = request.POST['retencion-punto']
                        documento_retencion_compra.secuencial = request.POST['retencion-secuencial']
                        documento_retencion_compra.autorizacion = request.POST['retencion-autorizacion']
                        documento_retencion_compra.descripcion = request.POST['retencion-descripcion']
                        documento_retencion_compra.save()
                        for retencion in retenciones:
                            documento_retencion_detalle_compra = DocumentosRetencionDetalleCompra()
                            documento_retencion_detalle_compra.documento_retencion_compra_id = documento_retencion_compra.id
                            documento_retencion_detalle_compra.retencion_detalle_id = retencion['id']
                            documento_retencion_detalle_compra.base_imponible = retencion['base']
                            documento_retencion_detalle_compra.porcentaje_retencion = retencion['porcentaje']
                            documento_retencion_detalle_compra.valor_retenido = retencion['valor_retenido']
                            documento_retencion_detalle_compra.save()

                        retencion_secuencial = Secuenciales.objects.get(modulo='retencion')
                        retencion_secuencial.secuencial = int(request.POST['retencion-secuencial'])
                        retencion_secuencial.save()
                        documento.retenido = True
                        documento.save()
                    
                    if request.POST['retencion_total_retenido']:
                        valor_ret=request.POST['retencion_total_retenido']
                    print ("Prueba de hoy")
                    print (valor_ret)
                    total=request.POST['total_factura']
                    print ("Prueba de hoy")
                    print (total)
                    total_pagar=float(total)-float(valor_ret)
                    print ("Prueba de hoy")
                    print (total_pagar)
                    documento.total_pagar = total_pagar
                    documento.valor_retenido=request.POST['retencion_total_retenido']
                    documento.save()
            except Exception as e:
                print (e.args)
        else:
            form_errors = form.errors
            print form.errors

        response_data = {}
        response_data['result'] = 'ok'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
@transaction.atomic()
def documento_compra_update_view(request, pk):
    if request.method == 'POST':
        documento = DocumentoCompra.objects.get(id=pk)
        form = DocumentoCompraForm(request.POST)
        valor_ret=0

        if form.is_valid():

            try:
                with transaction.atomic():
                    cleaned_data = form.cleaned_data
                    documento.updated_by = request.user.get_full_name()
                    documento.updated_at = datetime.now()
                    documento.fecha_emision = cleaned_data.get('fecha_emision')
                    documento.fecha_vencimiento = cleaned_data.get('fecha_vencimiento')
                    documento.proveedor = cleaned_data.get('proveedor')
                    documento.establecimiento = cleaned_data.get('establecimiento')
                    documento.punto_emision = cleaned_data.get('punto_emision')
                    documento.secuencial = cleaned_data.get('secuencial')
                    documento.autorizacion = cleaned_data.get('autorizacion')
                    documento.descripcion = request.POST['descripcion']
                    documento.base_iva_0 = request.POST['base_iva_0_factura']
                    documento.base_iva = request.POST['base_iva_factura']
                    documento.valor_iva = request.POST['valor_iva_factura']
                    documento.porcentaje_iva = request.POST['porcentaje_iva_factura']
                    documento.base_ice = cleaned_data.get('base_ice')
                    documento.valor_ice = cleaned_data.get('valor_ice')
                    documento.porcentaje_ice = cleaned_data.get('porcentaje_ice')
                    documento.descuento = cleaned_data.get('descuento')
                    documento.total = request.POST['total_factura']
                    documento.tipo_provision = cleaned_data.get('tipo_provision')
                    documento.pagado = False
                    documento.sustento_tributario = cleaned_data.get('sustento_tributario')
                    documento.sri_forma_pago_id = request.POST['forma_pago']
                    documento.generada = False
                    
                    documento.save()

                    asientos = json.loads(request.POST['arreglo_asientos'])
                    if len(asientos) > 0:
                        if documento.asiento_id:
                            asiento = Asiento.objects.get(asiento_id=documento.asiento_id)
                            asiento.glosa = 'FACTURA COMPRAS ' + str(documento.proveedor.nombre_proveedor.encode('utf8')) + str(
                                documento.establecimiento) + '-' + str(documento.punto_emision) + '-' + str(
                                documento.secuencial)
                            asiento.save()
                            items = AsientoDetalle.objects.filter(asiento_id=asiento.asiento_id).delete()

                            for item_asiento in asientos:
                                asiento_detalle = AsientoDetalle()
                                asiento_detalle.asiento_id = int(asiento.asiento_id)
                                asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                                asiento_detalle.debe = item_asiento['debe']
                                asiento_detalle.haber = item_asiento['haber']
                                asiento_detalle.concepto = item_asiento['concepto']
                                if item_asiento['centro_id'] != 'null':
                                    asiento_detalle.centro_costo_id = item_asiento['centro_id']
                            
                                asiento_detalle.save()
                        else:
                            codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                            secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                            asiento = Asiento()
                            asiento.codigo_asiento = "P" + str(now.year) + "000" + str(codigo_asiento)
                            asiento.fecha = cleaned_data.get('fecha_emision')
                            asiento.glosa = 'FACTURA COMPRAS ' + str(documento.proveedor.nombre_proveedor.encode('utf8')) + str(
                                documento.establecimiento) + '-' + str(documento.punto_emision) + '-' + str(
                                documento.secuencial)
                            asiento.gasto_no_deducible = False
                            asiento.secuencia_asiento = codigo_asiento
                            total_debe = request.POST['asiento-total-debe']
                            total_haber = request.POST['asiento-total-haber']
                            asiento.total_debe = total_debe
                            asiento.total_haber = total_haber
                            asiento.save()
                            Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                            documento.asiento = asiento
                            documento.save()

                            for item_asiento in asientos:
                                asiento_detalle = AsientoDetalle()
                                asiento_detalle.asiento_id = int(asiento.asiento_id)
                                asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                                asiento_detalle.debe = item_asiento['debe']
                                asiento_detalle.haber = item_asiento['haber']
                                asiento_detalle.concepto = item_asiento['concepto']
                                if item_asiento['centro_id'] != 'null':
                                    asiento_detalle.centro_costo_id = item_asiento['centro_id']
                            
                                asiento_detalle.save()

                    retenciones = json.loads(request.POST['arreglo_retenciones'])
                    if len(retenciones) > 0:
                        if documento.retenido:
                            documento_retencion_compra = DocumentosRetencionCompra.objects.get(
                                documento_compra_id=documento.id)

                            documento_retencion_compra.fecha_emision = request.POST['retencion-fecha-emision']
                            documento_retencion_compra.establecimiento = request.POST['retencion-establecimiento']
                            documento_retencion_compra.punto_emision = request.POST['retencion-punto']
                            documento_retencion_compra.secuencial = request.POST['retencion-secuencial']
                            documento_retencion_compra.autorizacion = request.POST['retencion-autorizacion']
                            documento_retencion_compra.descripcion = request.POST['retencion-descripcion']
                            documento_retencion_compra.save()

                            items = DocumentosRetencionDetalleCompra.objects.filter(
                                documento_retencion_compra_id=documento_retencion_compra.id).delete()

                            for retencion in retenciones:
                                documento_retencion_detalle_compra = DocumentosRetencionDetalleCompra()
                                documento_retencion_detalle_compra.documento_retencion_compra_id = documento_retencion_compra.id
                                documento_retencion_detalle_compra.retencion_detalle_id = retencion['id']
                                documento_retencion_detalle_compra.base_imponible = retencion['base']
                                documento_retencion_detalle_compra.porcentaje_retencion = retencion['porcentaje']
                                documento_retencion_detalle_compra.valor_retenido = retencion['valor_retenido']
                                documento_retencion_detalle_compra.save()

                        else:

                            documento_retencion_compra = DocumentosRetencionCompra()
                            documento_retencion_compra.documento_compra_id = int(documento.id)
                            documento_retencion_compra.fecha_emision = request.POST['retencion-fecha-emision']
                            documento_retencion_compra.establecimiento = request.POST['retencion-establecimiento']
                            documento_retencion_compra.punto_emision = request.POST['retencion-punto']
                            documento_retencion_compra.secuencial = request.POST['retencion-secuencial']
                            documento_retencion_compra.autorizacion = request.POST['retencion-autorizacion']
                            documento_retencion_compra.descripcion = request.POST['retencion-descripcion']
                            documento_retencion_compra.save()
                            for retencion in retenciones:
                                documento_retencion_detalle_compra = DocumentosRetencionDetalleCompra()
                                documento_retencion_detalle_compra.documento_retencion_compra_id = documento_retencion_compra.id
                                documento_retencion_detalle_compra.retencion_detalle_id = retencion['id']
                                documento_retencion_detalle_compra.base_imponible = retencion['base']
                                documento_retencion_detalle_compra.porcentaje_retencion = retencion['porcentaje']
                                documento_retencion_detalle_compra.valor_retenido = retencion['valor_retenido']
                                documento_retencion_detalle_compra.save()

                            retencion_secuencial = Secuenciales.objects.get(modulo='retencion')
                            retencion_secuencial.secuencial = int(request.POST['retencion-secuencial'])
                            retencion_secuencial.save()
                            documento.retenido = True
                            documento.save()

                    if request.POST['retencion_total_retenido']:
                        valor_ret=request.POST['retencion_total_retenido']
                    print ("Prueba de hoy")
                    print (valor_ret)
                    total=request.POST['total_factura']
                    print ("Prueba de hoy")
                    print (total)
                    total_pagar=float(total)-float(valor_ret)
                    print ("Prueba de hoy")
                    print (total_pagar)
                    documento.total_pagar = total_pagar
                    documento.valor_retenido=request.POST['retencion_total_retenido']
                    documento.save()
            except Exception as e:
                print (e.args)
        else:
            form_errors = form.errors
            print form.errors

        response_data = {}
        response_data['result'] = 'ok'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def imprimir_retencion_compra_view(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    documento = DocumentoCompra.objects.get(id=pk)
    retencion = DocumentosRetencionCompra.objects.get(documento_compra_id=pk)
    detalle = DocumentosRetencionDetalleCompra.objects.filter(documento_retencion_compra_id=retencion.id)
    total = sum(d.valor_retenido for d in detalle)
    rango = 4 - len(detalle)
    now = datetime.now()

    html = render_to_string('compra/retencion_imprimir.html',
                            {'pagesize': 'A4', 'documento': documento, 'retencion': retencion, 'detalle': detalle,
                             'fecha': now, 'total': total, 'rango': range(rango)},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


@login_required()
def imprimir_asiento_compra_view(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    documento = DocumentoCompra.objects.get(id=pk)
    asiento = Asiento.objects.get(asiento_id=documento.asiento_id)
    detalle = AsientoDetalle.objects.filter(asiento_id=documento.asiento_id)
    total_haber = sum(d.haber for d in detalle)
    total_debe = sum(d.debe for d in detalle)

    now = datetime.now()

    html = loader.get_template('compra/asiento_imprimir.html')
    context = RequestContext(request, {'documento': documento, 'aiento': asiento, 'detalle': detalle,
                             'fecha': now, 'total_debe': total_debe, 'total_haber': total_haber})
    return HttpResponse(html.render(context))



def generar_pdf(html):
    # Funci?n para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))



@login_required()
@transaction.atomic()
def documento_compra_retencion_crear_view(request):
    if request.method == 'POST':
        form = DocumentosRetencionCompraForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Cabezera retencion
                    cleaned_data = form.cleaned_data
                    documento = DocumentosRetencionCompra()
                    compra_compra_id = cleaned_data.get('documento_compra')
                    DocumentoCompra.objects.filter(id=compra_compra_id).update(retenido=True)
                    documento.documento_compra = cleaned_data.get('documento_compra')
                    documento.fecha_emision = cleaned_data.get('fecha_emision')
                    documento.establecimiento = cleaned_data.get('establecimiento')
                    documento.punto_emision = cleaned_data.get('punto_emision')
                    documento.secuencial = cleaned_data.get('secuencial')
                    documento.autorizacion = cleaned_data.get('autorizacion')
                    documento.descripcion = cleaned_data.get('descripcion')
                    documento.save()
                    # Detalle retencion
                    retenciones = json.loads(request.POST['arreglo_retenciones'])
                    if len(retenciones) > 0:
                        for retencion in retenciones:
                            documento_retencion_compra = DocumentosRetencionDetalleCompra()
                            documento_retencion_compra.documento_retencion_compra_id = int(documento.id)
                            documento_retencion_compra.retencion_detalle_id = retencion['id']
                            documento_retencion_compra.base_imponible = retencion['base']
                            documento_retencion_compra.porcentaje_retencion = retencion['porcentaje']
                            documento_retencion_compra.valor_retenido = retencion['valor_retenido']
                            documento_retencion_compra.save()

                    asientos = json.loads(request.POST['arreglo_asientos'])
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        asiento = Asiento()
                        asiento.codigo_asiento = int(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = ''
                        asiento.gasto_no_deducible = False
                        asiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=secuenciales_id + 1)
                        for item_asiento in asientos:
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.save()

            except Exception as e:
                print (e.message)
        else:
            form_errors = form.errors
    return HttpResponseRedirect('documento/venta/retencion')


@login_required()
def documento_edit_view(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.all()
    bancos = Banco.objects.all()
    clientes = Cliente.objects.all()
    template = loader.get_template('movimientos/edit.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos,
                                       'tipo_documentos': tipo_documentos, 'clientes': clientes, 'bancos': bancos})
    return HttpResponse(template.render(context))


@login_required()
def compra_consultar_cuenta(request):
    if request.method == "POST" and request.is_ajax:
        plan_cuenta_id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT plan_id, codigo_plan, nombre_plan FROM contabilidad_plandecuentas WHERE plan_id = ' + (
            plan_cuenta_id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def documento_compra_consultar_facturas(request):
    if request.method == "POST" and request.is_ajax:
        proveedor_id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT id, establecimiento, punto_emision, secuencial, porcentaje_iva, base_iva, base_iva_0, valor_iva' \
                ' FROM documento_compra' \
                ' WHERE proveedor_id = ' + (proveedor_id) + \
                ' AND retenido=false;'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def documento_update_view(request, pk):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            movimiento = Movimiento.objects.get(pk=pk)
            movimiento.tipo_anticipo = cleaned_data.get('tipo_anticipo')
            movimiento.tipo_anticipo_documento = cleaned_data.get('tipo_anticipo_documento')
            movimiento.fecha_emision = cleaned_data.get('fecha_emision')
            movimiento.cuenta_bancaria = int(cleaned_data.get('cuenta_bancaria'))
            movimiento.persona = int(cleaned_data.get('persona'))
            movimiento.paguese_a = cleaned_data.get('paguese_a')
            movimiento.numero_cheque = cleaned_data.get('numero_cheque')
            movimiento.fecha_cheque = cleaned_data.get('fecha_cheque')
            movimiento.descripcion = cleaned_data.get('descripcion')
            movimiento.numero_comprobante = cleaned_data.get('numero_comprobante')
            movimiento.save()
        return HttpResponseRedirect('/bancos/movimiento')


@login_required()
def consultar_orden_compra(request):
    if request.method == "POST" and request.is_ajax:
        proveedor = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT compra_id,nro_compra,total FROM orden_compra AS oc WHERE oc.proveedor_id = ' + (proveedor) + ';'
        cursor.execute(query)

        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def consultar_items_orden(request):
    if request.method == "POST" and request.is_ajax:
        orden_compra = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT cd.compras_detalle_id, cd.compra_id, cd.producto_id, cd.cantidad, p.descripcion_producto, cd.precio_compra, cd.total ' \
                'FROM compras_detalle AS cd ' \
                'INNER JOIN producto AS p ' \
                'ON cd.producto_id = p.producto_id ' \
                'WHERE compra_id =' + orden_compra + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def documento_nuevo_retencion_view(request):
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    documentos = TransaccionTipoDocuemento.objects.all()
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    bodegas = Bodega.objects.all()
    productos = Producto.objects.all()
    retenciones_fuente = RetencionDetalle.objects.filter(tipo_retencion_id=1)
    retenciones_iva = RetencionDetalle.objects.filter(tipo_retencion_id=2)
    formas_pago = SriFormaPago.objects.all()
    bancos = Banco.objects.all()
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.all()
    form = MovimientoForm
    template = loader.get_template('compra/retencion.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos,
                                       'tipo_documentos': tipo_documentos, 'bancos': bancos, 'proveedores': proveedores,
                                       'bodegas': bodegas, 'documentos': documentos, 'productos': productos,
                                       'retenciones_iva': retenciones_iva, 'retenciones_fuente': retenciones_fuente,
                                       'cuentas': cuentas, 'formas_pago': formas_pago})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def documento_compra_retencion_crear_view(request):
    if request.method == 'POST':
        form = DocumentosRetencionCompraForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Cabezera retencion
                    cleaned_data = form.cleaned_data
                    documento = DocumentosRetencionCompra()
                    compra_compra_id = int(cleaned_data.get('documento_compra').id)
                    DocumentoCompra.objects.filter(id=compra_compra_id).update(retenido=True)
                    documento.documento_compra = cleaned_data.get('documento_compra')
                    documento.fecha_emision = cleaned_data.get('fecha_emision')
                    documento.establecimiento = cleaned_data.get('establecimiento')
                    documento.punto_emision = cleaned_data.get('punto_emision')
                    documento.secuencial = cleaned_data.get('secuencial')
                    documento.autorizacion = cleaned_data.get('autorizacion')
                    documento.descripcion = cleaned_data.get('descripcion')
                    documento.save()
                    # Detalle retencion
                    retenciones = json.loads(request.POST['arreglo_retenciones'])
                    if len(retenciones) > 0:
                        for retencion in retenciones:
                            documento_retencion_compra = DocumentosRetencionDetalleCompra()
                            documento_retencion_compra.documento_retencion_compra_id = int(documento.id)
                            documento_retencion_compra.retencion_detalle_id = retencion['id']
                            documento_retencion_compra.base_imponible = retencion['base']
                            documento_retencion_compra.porcentaje_retencion = retencion['porcentaje']
                            documento_retencion_compra.valor_retenido = retencion['valor_retenido']
                            documento_retencion_compra.save()

                    asientos = json.loads(request.POST['arreglo_asientos'])
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        asiento = Asiento()
                        asiento.codigo_asiento = int(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = ''
                        asiento.gasto_no_deducible = False
                        asiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=secuenciales_id + 1)
                        for item_asiento in asientos:
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.save()

            except Exception as e:
                print (e.message)
        else:
            form_errors = form.errors
    return HttpResponseRedirect('documento/compra/nuevo')


@login_required()
def documento_nuevo_retencion_venta_view(request):
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    documentos = TransaccionTipoDocuemento.objects.all()
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    bodegas = Bodega.objects.all()
    productos = Producto.objects.all()
    retenciones_fuente = RetencionDetalle.objects.filter(tipo_retencion_id=1)
    retenciones_iva = RetencionDetalle.objects.filter(tipo_retencion_id=2)
    formas_pago = SriFormaPago.objects.all()
    bancos = Banco.objects.all()
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.all()
    form = MovimientoForm
    template = loader.get_template('venta/retencion.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos,
                                       'tipo_documentos': tipo_documentos, 'bancos': bancos, 'proveedores': proveedores,
                                       'bodegas': bodegas, 'documentos': documentos, 'productos': productos,
                                       'retenciones_iva': retenciones_iva, 'retenciones_fuente': retenciones_fuente,
                                       'cuentas': cuentas, 'formas_pago': formas_pago})
    return HttpResponse(template.render(context))


"""
Modulo:        DOCUMENTO VENTA
Autor:          GAPH
Descripcion:    Esta modulo registra una factura de cliente (venta)
"""


@login_required()
def documento_venta_list_view(request):
    ventas = DocumentoVenta.objects.all()
    template = loader.get_template('venta/index.html')
    context = RequestContext(request, {'ventas': ventas})
    return HttpResponse(template.render(context))

@login_required()
def documentoVentaEliminarByPkView(request, pk):
    obj = DocumentoVenta.objects.get(id=pk)

    if obj:
        obj.activo = False
        obj.save()

    return HttpResponseRedirect('/transacciones/documento/venta')

@login_required()
def documento_venta_nuevo_view(request):

    clientes = Cliente.objects.filter(activo=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True, categoria="DETALLE")
    retenciones_fuente = RetencionDetalle.objects.filter(tipo_retencion_id=1)
    retenciones_iva = RetencionDetalle.objects.filter(tipo_retencion_id=2)
    porcentaje_iva = Parametros.objects.get(clave='iva').valor
    formas_pago = SriFormaPago.objects.all()
    centros = CentroCosto.objects.filter(activo=True).exclude(padre_id__isnull=True)
    vendedores = Vendedor.objects.all()
    puntos = PuntosVenta.objects.filter(activo=True)
    form = DocumentoVentaForm
    template = loader.get_template('venta/create.html')
    context = RequestContext(request, {'form': form, 'centros': centros, 'clientes': clientes,
                                       'retenciones_iva': retenciones_iva,'vendedores':vendedores,
                                       'retenciones_fuente': retenciones_fuente,'puntos':puntos,
                                       'cuentas': cuentas, 'formas_pago': formas_pago,
                                       'porcentaje_iva': porcentaje_iva})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def documento_venta_crear_view(request):
    if request.method == 'POST':
        form = DocumentoVentaForm(request.POST)
        msg = ""
        if form.is_valid():
            try:
                with transaction.atomic():
                    cleaned_data = form.cleaned_data
                    documento = DocumentoVenta()
                    documento.created_by = request.user.get_full_name()
                    documento.updated_by = request.user.get_full_name()
                    documento.created_at = datetime.now()
                    documento.updated_at = datetime.now()
                    documento.fecha_emision = cleaned_data.get('fecha_emision')
                    documento.cliente = cleaned_data.get('cliente')
                    documento.proforma_id = request.POST['cliente_proforma']
                    documento.establecimiento = cleaned_data.get('establecimiento')
                    documento.punto_emision = cleaned_data.get('punto_emision')
                    documento.secuencial = cleaned_data.get('secuencial')
                    documento.autorizacion = cleaned_data.get('autorizacion')
                    documento.descripcion = cleaned_data.get('descripcion')
                    documento.base_iva_0 = cleaned_data.get('base_iva_0')
                    documento.valor_iva_0 = cleaned_data.get('valor_iva_0')
                    documento.base_iva = cleaned_data.get('subtotal')
                    documento.subtotal = cleaned_data.get('subtotal')
                    documento.valor_iva = cleaned_data.get('valor_iva')
                    documento.porcentaje_iva = cleaned_data.get('porcentaje_iva')
                    documento.descuento = cleaned_data.get('descuento')
                    documento.total = cleaned_data.get('total')
                    documento.total_en_letras = cleaned_data.get('total_en_letras')
                    documento.razon_social_id = request.POST['razon_social']
                    documento.punto_venta_id = request.POST['punto_venta']
                    documento.vendedor = cleaned_data.get('vendedor')
                    documento.ruc = request.POST['cliente_ruc']
                    documento.direccion = request.POST['cliente_direccion']
                    documento.telefono = request.POST['cliente_telefono']
                    documento.retenido = False
                    documento.save()

                    if request.POST['punto_venta'] > 0:
                        punto = PuntosVenta.objects.get(id=documento.punto_venta_id)
                        punto.secuencial = int(request.POST['secuencial'])
                        punto.save()
                    else:
                        factura_secuencial = Secuenciales.objects.get(modulo='factura')
                        factura_secuencial.secuencial = int(request.POST['secuencial'])
                        factura_secuencial.save()

                    productos = json.loads(request.POST['arreglo_detalle'])
                    if len(productos) > 0:
                        for producto in productos:
                            documento_detalle = DocumentosVentaDetalle()
                            documento_detalle.documento_venta_id = int(documento.id)
                            documento_detalle.descripcion = producto['descripcion']
                            documento_detalle.base_iva_0 = 0
                            documento_detalle.valor_iva_0 = 0
                            documento_detalle.base_iva = producto['precio']
                            documento_detalle.valor_iva = (Decimal(producto['precio']) * Decimal(request.POST['porcentaje_iva'])) / 100
                            documento_detalle.porcentaje_iva = request.POST['porcentaje_iva']
                            documento_detalle.base_ice = 0
                            documento_detalle.valor_ice = 0
                            documento_detalle.porcentaje_ice = 0
                            documento_detalle.descuento = 0
                            documento_detalle.cantidad = producto['cantidad']
                            documento_detalle.subtotal = producto['total']
                            documento_detalle.save()


                    asientos = json.loads(request.POST['arreglo_asientos'])
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        asiento = Asiento()
                        asiento.codigo_asiento = "C" + str(now.year) + "000" + str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'FACTURA VENTAS ' + smart_str(documento.cliente.nombre_cliente) +' '+ str(
                            documento.establecimiento) + '-' + str(documento.punto_emision) + '-' + str(
                            documento.secuencial)
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe = request.POST['asiento-total-debe']
                        total_haber = request.POST['asiento-total-haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.save()

                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)

                        for item_asiento in asientos:
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.save()

                        documento.asiento = asiento
                        documento.save()
                    #
                    # retenciones = json.loads(request.POST['arreglo_retenciones'])
                    # if len(retenciones) > 0:
                    #     # Cabezera retencion
                    #     cleaned_data = form.cleaned_data
                    #     documento_retencion = DocumentoRetencionVenta()
                    #     compra_venta_id = cleaned_data.get('documento_venta')
                    #     DocumentoVenta.objects.filter(id=compra_venta_id).update(retenido=True)
                    #     documento_retencion.documento_venta_id = int(documento.id)
                    #     fecha_emision = request.POST['retencion-fecha-emision']
                    #     fecha_emision = fecha_emision.split('/')
                    #     documento_retencion.fecha_emision = str(fecha_emision[2]) + '-' + str(
                    #         fecha_emision[1]) + '-' + str(fecha_emision[0])
                    #     documento_retencion.establecimiento = request.POST['retencion-establecimiento']
                    #     documento_retencion.punto_emision = request.POST['retencion-punto']
                    #     documento_retencion.secuencial = request.POST['retencion-secuencial']
                    #     documento_retencion.autorizacion = request.POST['retencion-autorizacion']
                    #     documento_retencion.descripcion = request.POST['retencion-descripcion']
                    #     documento_retencion.save()
                    #     # Detalle retencion
                    #     for retencion in retenciones:
                    #         documento_retencion_detalle = DocumentoRetencionDetalleVenta()
                    #         documento_retencion_detalle.documento_retencion_venta_id = int(documento_retencion.id)
                    #         documento_retencion_detalle.retencion_detalle_id = retencion['id']
                    #         documento_retencion_detalle.base_imponible = retencion['base']
                    #         documento_retencion_detalle.porcentaje_retencion = retencion['porcentaje']
                    #         documento_retencion_detalle.valor_retenido = retencion['valor_retenido']
                    #         documento_retencion_detalle.save()

                    msg = "ok"
            except Exception as e:
                print (e.args)
        else:
            msg = form.errors

    response_data = {}
    response_data['result'] = msg
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
@transaction.atomic()
def documento_venta_edit_view(request, pk):

    documento = DocumentoVenta.objects.get(id=pk)
    detalle = DocumentosVentaDetalle.objects.filter(documento_venta_id=pk)
    cuentas = PlanDeCuentas.objects.filter(activo=True, categoria="DETALLE")
    retenciones_fuente = RetencionDetalle.objects.filter(tipo_retencion_id=1)
    retenciones_iva = RetencionDetalle.objects.filter(tipo_retencion_id=2)
    porcentaje_iva = Parametros.objects.get(clave='iva').valor
    centros = CentroCosto.objects.filter(activo=True).exclude(padre_id__isnull=True)
    clientes = Cliente.objects.filter(activo=True)
    vendedores = Vendedor.objects.all()


    form = DocumentoVentaForm(request.POST, request.FILES, instance=documento)
    template = loader.get_template('venta/edit.html')
    context = RequestContext(request, {'form': form, 'centros': centros, 'clientes': clientes,
                                       'vendedores': vendedores, 'retenciones_iva': retenciones_iva,
                                       'retenciones_fuente': retenciones_fuente,
                                       'cuentas': cuentas, 'detalle': detalle,
                                       'porcentaje_iva': porcentaje_iva, 'documento': documento})
    return HttpResponse(template.render(context))


@login_required()
def documento_venta_consultar_facturas(request):
    if request.method == "POST" and request.is_ajax:
        cliente_id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT id, to_char(fecha_emision, \'DD/MM/YYYY\') as fecha, establecimiento, punto_emision, secuencial, porcentaje_iva, base_iva, base_iva_0, valor_iva' \
                ' FROM documento_venta' \
                ' WHERE cliente_id = ' + (cliente_id) + \
                ' AND retenido=false;'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
@transaction.atomic()
def documento_venta_retencion_crear_view(request):
    if request.method == 'POST':
        form = DocumentoRetencionVentaForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Cabezera retencion
                    cleaned_data = form.cleaned_data
                    documento_retencion = DocumentoRetencionVenta()
                    documento_retencion.documento_venta = cleaned_data.get('documento_venta')
                    documento_retencion.fecha_emision = cleaned_data.get('fecha_emision')
                    documento_retencion.establecimiento = cleaned_data.get('establecimiento')
                    documento_retencion.punto_emision = cleaned_data.get('punto_emision')
                    documento_retencion.secuencial = cleaned_data.get('secuencial')
                    documento_retencion.autorizacion = cleaned_data.get('autorizacion')
                    documento_retencion.descripcion = cleaned_data.get('descripcion')
                    documento_retencion.save()
                    # Detalle retencion
                    retenciones = json.loads(request.POST['arreglo_retenciones'])
                    if len(retenciones) > 0:
                        for retencion in retenciones:
                            documento_retencion_detalle = DocumentoRetencionDetalleVenta()
                            documento_retencion_detalle.documento_retencion_venta_id = int(documento_retencion.id)
                            documento_retencion_detalle.retencion_detalle_id = retencion['id']
                            documento_retencion_detalle.base_imponible = retencion['base']
                            documento_retencion_detalle.porcentaje_retencion = retencion['porcentaje']
                            documento_retencion_detalle.valor_retenido = retencion['valor_retenido']
                            documento_retencion_detalle.save()

                    asientos = json.loads(request.POST['arreglo_asientos'])
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        asiento = Asiento()
                        asiento.codigo_asiento = int(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = ''
                        asiento.gasto_no_deducible = False
                        asiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=secuenciales_id + 1)
                        for item_asiento in asientos:
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.save()
                    '''Actualizamos el registro de venta para saber que ya se aplico una retencion'''
                    documento_venta = cleaned_data.get('documento_venta')
                    DocumentoVenta.objects.filter(id=documento_venta.id).update(retenido=True)

            except Exception as e:
                print (e.message)
        else:
            form_errors = form.errors
    return HttpResponseRedirect('documento/venta/retencion')


@login_required()
def documento_consultar_proforma(request):
    if request.method == "POST" and request.is_ajax:
        cliente_id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT id, codigo, subtotal, iva, total FROM proforma WHERE cliente_id = ' + (cliente_id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def documento_consultar_proforma_detalle(request):
    if request.method == "POST" and request.is_ajax:
        proforma_id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT pd.id, pd.proforma_id, pd.producto_id, pd.cantidad, pd.nombre, pd.precio_compra , pd.total  ' \
                'FROM proforma_detalle AS pd ' \
                'INNER JOIN producto AS p ' \
                'ON pd.producto_id = p.producto_id ' \
                'WHERE pd.proforma_id = ' + proforma_id + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def consultar_cuenta_contable(request):
    if request.method == "POST" and request.is_ajax:
        plan_id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT plan_id, codigo_plan, nombre_plan FROM contabilidad_plandecuentas WHERE plan_id = ' + (
            plan_id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def documento_retencion_list_view(request):
    rentenciones = DocumentosRetencionCompra.objects.all()
    template = loader.get_template('compra/retencion_index.html')
    context = RequestContext(request, {'rentenciones': rentenciones})
    return HttpResponse(template.render(context))


@login_required()
def documento_venta_retencion_list_view(request):
    rentenciones = DocumentoRetencionVenta.objects.all()
    template = loader.get_template('venta/retencion_index.html')
    context = RequestContext(request, {'rentenciones': rentenciones})
    return HttpResponse(template.render(context))


@login_required()
def consultar_retencion(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT * FROM retencion_detalle WHERE id = ' + (id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")

@login_required()
def consultar_razon_social(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT a.id, a.nombre FROM razon_social a, razon_social_clientes b WHERE a.id = b.razon_social_id AND b.cliente_id = ' + (id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")

@login_required()
def consultar_proforma_cliente(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT id,codigo,to_char(fecha, \'YYYY-MM-DD\') as fecha,total,descuento FROM proforma  WHERE aprobada = TRUE AND cliente_id = ' + (id) + ' ORDER BY fecha DESC;'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")

@login_required()
def consultar_proforma_detalle_cliente(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT id,nombre,producto_id,cantidad,precio_compra,total FROM proforma_detalle  WHERE no_producir <> TRUE AND proforma_id = ' + (id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")

@login_required()
def imprimir_factura_venta_view(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    documento = DocumentoVenta.objects.get(id=pk)
    detalle = DocumentosVentaDetalle.objects.filter(documento_venta_id=pk)
    #total_haber = sum(d.haber for d in detalle)
    #total_debe = sum(d.debe for d in detalle)
    rango = 10 - len(detalle)
    now = datetime.now()
    html = loader.get_template('venta/factura_imprimir.html')
    context = RequestContext(request,
                             { 'documento': documento, 'detalle': detalle,'fecha': now,'rango':range(rango)})
    return HttpResponse(html.render(context))

@login_required()
def consultar_cuenta_contable_by_codigo(request):
    if request.method == "POST" and request.is_ajax:
        plan_cuenta_id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT plan_id, codigo_plan, nombre_plan FROM contabilidad_plandecuentas WHERE codigo_plan = ' + (
            plan_cuenta_id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def imprimir_factura_venta_pdf_view(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    documento = DocumentoVenta.objects.get(id=pk)
    detalle = DocumentosVentaDetalle.objects.filter(documento_venta_id=pk)
    #total_haber = sum(d.haber for d in detalle)
    #total_debe = sum(d.debe for d in detalle)
    rango = 26 - len(detalle)
    now = datetime.now()

    html = render_to_string('venta/fatura_imprimir_pdf.html',
                            {'pagesize': 'A4', 'documento': documento, 'detalle': detalle, 'fecha': now,
                             'rango': range(rango)},
                            context_instance=RequestContext(request))
    return generar_pdf(html)



def index(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    documento = DocumentoVenta.objects.get(id=pk)
    detalle = DocumentosVentaDetalle.objects.filter(documento_venta_id=pk)
    #total_haber = sum(d.haber for d in detalle)
    #total_debe = sum(d.debe for d in detalle)
    rango = 22- len(detalle)
    now = datetime.now()
    r=range(rango)
        
    html = render_to_string('venta/fatura_imprimir_pdf.html', {'pagesize':'A4','documento':documento,'detalle':detalle,'fecha':now,'rango': r}, context_instance=RequestContext(request))
    return generar_pdf(html)




@login_required()
def consultar_razon_social_id(request):
    if request.method == "POST":
        id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT * FROM razon_social WHERE id = ' + (id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")



@login_required()
def AsientoEliminarDetalleView(request):
    pk=request.POST["id"]
    objetos = AsientoDetalle.objects.get(detalle_id=pk)
    objetos.delete()
    mensaje="Eliminado con exito"

    return HttpResponse(

    )


@login_required()
def consultar_plan_cuentas_retencion_detalle_view(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT p.plan_id,p.codigo_plan,p.nombre_plan FROM retencion_detalle a,contabilidad_plandecuentas p WHERE a.cuenta_id=p.plan_id AND a.id = ' + (
        id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")

@login_required()
def documentoCompraEliminarByPkView(request, pk):
    obj = DocumentoCompra.objects.get(id=pk)

    if obj:
        obj.anulado = True
        obj.activo = False
        obj.save()
        try:
            asiento = Asiento.objects.filter(asiento_id=obj.asiento_id)
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            for a in asiento:
                a.anulado= True
                a.save()

    return HttpResponseRedirect('/transacciones/documento/compra')

@login_required()
def imprimir_retencion_venta_view(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    documento = DocumentoVenta.objects.get(id=pk)
    retencion = DocumentoRetencionVenta.objects.get(documento_venta_id=pk)
    detalle = DocumentoRetencionDetalleVenta.objects.filter(documento_retencion_venta_id=retencion.id)
    total = sum(d.valor_retenido for d in detalle)
    rango = 4 - len(detalle)
    now = datetime.now()
    usuario=request.user.get_full_name()

    html = render_to_string('venta/retencion_venta_imprimir.html',
                            {'pagesize': 'A4', 'documento': documento, 'retencion': retencion, 'detalle': detalle,
                             'fecha': now, 'total': total, 'rango': range(rango),'usuario': usuario,},
                            context_instance=RequestContext(request))
    return generar_pdf(html)

@login_required()
def export_to_excel_factura(request,pk):


    # your excel html format
    template_name = "factura.html"
    documento = DocumentoVenta.objects.get(id=pk)
    detalle = DocumentosVentaDetalle.objects.filter(documento_venta_id=pk)
    rango = int(10 - len(detalle))
    lista = []
    for i in range(0,rango):
        lista.append(i)
    print rango
    now = datetime.now()
    


    response = render_to_response('venta/factura_imprimir_excel.html', {'documento':documento,'lista':lista,'detalle':detalle})

    # this is the output file
    nombre='FACTURA_'+documento.establecimiento+'-'+documento.punto_emision+'-'+documento.secuencial
    filename = nombre+'.xls'

    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
    return response
