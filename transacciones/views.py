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
from django.db.models import Sum

from .models import *
from bancos.models import *
from inventario.models import *
from facturacion.models import *
from ordenproduccion.models import *

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
from django.views.decorators.csrf import csrf_exempt
import cgi
import logging

# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db import connections
import pyodbc
from django.utils.encoding import smart_str, smart_unicode
from django.utils.safestring import mark_safe

from django import template
from django.utils.safestring import mark_safe


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

# ============Liquidacion Compra=============#
# @login_required()
# def lcdocumento_list_view(request):
#     #compras = DocumentoCompra.objects.all().order_by('-fecha_emision')
#     lcompras=''
#     template = loader.get_template('compra/lcindex.html')
#     context = RequestContext(request, {'lcompras': lcompras})
#     return HttpResponse(template.render(context))
#
# @login_required()
# def documento_compra_consultar_liquidaciones(request):
#     if request.method == "POST" and request.is_ajax:
#         proveedor_id = request.POST['id']
#         cursor = connection.cursor()
#         query = 'SELECT id, establecimiento, punto_emision, secuencial, porcentaje_iva, base_iva, base_iva_0, valor_iva' \
#                 ' FROM documento_lcompra' \
#                 ' WHERE proveedor_id = ' + (proveedor_id) + \
#                 ' AND retenido=false;'
#         cursor.execute(query)
#         ro = cursor.fetchall()
#         json_resultados = json.dumps(ro)
#     else:
#         raise Http404
#     return HttpResponse(json_resultados, content_type="application/json")
#
#
# @login_required()
# @csrf_exempt
# def documento_lcompra_api_view(request):
#     if request.method == "GET" and request.is_ajax:
#         _draw = request.GET['draw']
#         _start = int(request.GET['start'])
#         _end = int(request.GET['length'])
#         _search_value = request.GET['search[value]']
#         _order = request.GET['order[0][column]']
#         _order_dir = request.GET['order[0][dir]']
#         cursor = connection.cursor()
#         sql = "select c.id,c.fecha_emision,p.nombre_proveedor,c.establecimiento,c.punto_emision,c.secuencial,o.nro_compra,cl.codigo,c.total,c.descripcion,a.codigo_asiento,c.anulado,c.retenido,c.asiento_id,sum(ab.abono),c.facturacion_eletronica from documento_lcompra c left join contabilidad_asiento a on a.asiento_id=c.asiento_id left join proveedor p on p.proveedor_id=c.proveedor_id left join orden_compra o on o.compra_id=c.orden_compra_id left join compras_locales cl on cl.id=c.compra_id left join documento_abono ab on ab.documento_lcompra_id=c.id and ab.anulado is not True  where 1=1 "
#         if _search_value:
#             sql += " and UPPER(p.nombre_proveedor) like '%" + _search_value + "%' or UPPER(c.establecimiento) like '%" + _search_value.upper() + "%' or UPPER(c.punto_emision) like '%" + _search_value.upper() + "%' or UPPER(c.secuencial) like '%" + _search_value.upper() + "%' or CAST(o.nro_compra as VARCHAR)  like '%" + _search_value.upper() + "%' or CAST(c.total as VARCHAR)  like '%" + _search_value.upper() + "%' or CAST(c.fecha_emision as VARCHAR)  like '%" + _search_value + "%' or UPPER(cl.codigo) like '%" + _search_value.upper() + "%' or UPPER(c.descripcion) like '%" + _search_value.upper() + "%' or UPPER(a.codigo_asiento) like '%" + _search_value.upper() + "%'"
#
#         if _search_value.upper() == 'ANULADO' or _search_value.upper() == 'AN' or _search_value.upper() == 'ANU' or _search_value.upper() == 'ANUL' or _search_value.upper() == 'ANULA' or _search_value.upper() == 'ANULAD':
#             sql += " or c.anulado is True"
#
#         if _search_value.upper() == 'ACTIVO' or _search_value.upper() == 'AC' or _search_value.upper() == 'ACT' or _search_value.upper() == 'ACTI' or _search_value.upper() == 'ACTIV':
#             sql += " or c.anulado is not True"
#
#         # sql +=" order by fecha"
#         sql += " group by c.id,c.fecha_emision,p.nombre_proveedor,c.establecimiento,c.punto_emision,c.secuencial,o.nro_compra,cl.codigo,c.total,c.descripcion,a.codigo_asiento,c.anulado,c.retenido,c.asiento_id"
#         print _order
#         if _order == '0':
#             sql += " order by c.fecha_emision " + _order_dir
#         if _order == '1':
#             sql += " order by p.nombre_proveedor " + _order_dir
#
#         if _order == '2':
#             sql += " order by c.establecimiento,c.punto_emision,c.secuencial " + _order_dir
#         if _order == '3':
#             sql += " order by CAST(o.nro_compra AS Numeric(10,0)) " + _order_dir
#
#         if _order == '4':
#             sql += " order by CAST(cl.codigo  AS Numeric(10,0)) " + _order_dir
#
#         if _order == '5':
#             sql += " order by cl.total " + _order_dir
#         if _order == '6':
#             sql += " order by c.descripcion " + _order_dir
#         if _order == '7':
#             sql += " order by a.codigo_asiento " + _order_dir
#
#         if _order == '8':
#             sql += " order by c.anulado " + _order_dir
#         print sql
#         cursor.execute(sql)
#         compras = cursor.fetchall()
#
#         compras_filtered = compras[_start:_start + _end]
#
#         compras_list = []
#         for o in compras_filtered:
#             mes = o[1].month
#             anio = o[1].year
#             cursor = connection.cursor()
#             query = "select anio_id,mes_id from bloqueo_periodo  where date_part('year',fecha)='" + str(
#                 anio) + "' and date_part('month',fecha)='" + str(mes) + "'"
#             cursor.execute(query)
#             ro = cursor.fetchall()
#
#             compras_obj = []
#             compras_obj.append(o[1].strftime('%Y-%m-%d'))
#             compras_obj.append(o[2])
#             factura = '' + str(o[3]) + '-' + str(o[4]) + '-' + str(o[5])
#             compras_obj.append(factura)
#             compras_obj.append(o[6])
#             compras_obj.append(o[7])
#             compras_obj.append(o[8])
#
#             compras_obj.append(o[9])
#             compras_obj.append(o[10])
#             html = ''
#
#             if o[11]:
#                 compras_obj.append("Anulado")
#                 if o[13]:
#                     html += '<a href="http://' + str(
#                         request.META['HTTP_HOST']) + '/transacciones/documento/compra/asiento/' + str(o[0]) + '/imprimir" style="position: relative;"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-print"></i></button></a>'
#             else:
#                 compras_obj.append("Activo")
#                 if ro:
#                     r = 1
#                 else:
#                     if o[14] < 1:
#                         html += '<a href="http://' + str(
#                             request.META['HTTP_HOST']) + '/transacciones/documento/compra/' + str(o[
#                                                                                                       0]) + '/editar/"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-pencil"></i></button></a>'
#
#                         html += '<a href="http://' + str(
#                             request.META['HTTP_HOST']) + '/transacciones/documento/compra/' + str(o[
#                                                                                                       0]) + '/eliminar" style="" onclick="return confirm(¿Está seguro de anular esta factura?)"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-trash"></i></button></a>'
#                 if o[12]:
#                     html += '<a href="http://' + str(request.META['HTTP_HOST']) + '/transacciones/retencion/' + str(o[
#                                                                                                                         0]) + '/imprimirpdf/"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-list"></i></button></a>'
#
#                 if o[13]:
#                     html += '<a href="http://' + str(
#                         request.META['HTTP_HOST']) + '/transacciones/documento/compra/asiento/' + str(o[
#                                                                                                           0]) + '/imprimir" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-print"></i></button></a>'
#                 if o[15]:
#                     print 'fe'
#                     html += '<a href="http://' + str(
#                         request.META['HTTP_HOST']) + '/transacciones/consultar_datos_retencion_electronica/' + str(o[
#                                                                                                                        0]) + '/" target="_blank"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye"></i>Ver retencion electronica</button></a>'
#                     html += '<a href="http://' + str(
#                         request.META['HTTP_HOST']) + '/transacciones/documento/compra/' + str(o[
#                                                                                                   0]) + '/eliminar" style="" onclick="return confirm(¿Está seguro de anular esta factura?)"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-trash"></i></button></a>'
#
#
#                 else:
#                     fecha_inicio = o[1].strftime('%Y-%m-%d')
#                     if str(o[1].year) == '2017':
#                         print 'f'
#                     else:
#                         html += '<a href="#" onclick="mostrarRetencionElectronica(' + str(o[
#                                                                                               0]) + ')" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye">Retenc. Electronica</i></button></a>'
#
#             html += '<a href="http://' + str(request.META['HTTP_HOST']) + '/transacciones/documento/compra/' + str(o[
#                                                                                                                        0]) + '/consultar" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye"></i></button></a>'
#
#             compras_obj.append(html)
#
#             compras_list.append(compras_obj)
#         response_data = {}
#         response_data['draw'] = _draw
#         response_data['recordsTotal'] = len(compras)
#         response_data['recordsFiltered'] = len(compras)
#         response_data['data'] = compras_list
#     else:
#         raise Http404
#     return HttpResponse(json.dumps(response_data), content_type="application/json")


# ============Compra=============#
@login_required()
def documento_list_view(request):
    #compras = DocumentoCompra.objects.all().order_by('-fecha_emision')
    compras=''
    template = loader.get_template('compra/index.html')
    context = RequestContext(request, {'compras': compras})
    return HttpResponse(template.render(context))

@login_required()
@csrf_exempt
def documento_list_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        if _search_value:
            compras = DocumentoCompra.objects.all().order_by('-fecha_emision').filter(proveedor__nombre_proveedor__contains=_search_value)
        else:
            compras = DocumentoCompra.objects.all().order_by('-fecha_emision')
        compras_filtered = compras[_start:_start + _end]

        compra_list = []
        for compra in compras_filtered:
            compra_obj = []

            compra_obj.append(compra.fecha_emision.strftime('%Y-%m-%d'))
            compra_obj.append(compra.proveedor.nombre_proveedor)
            compra_obj.append(compra.establecimiento+"-"+compra.punto_emision+"-"+compra.secuencial)

            if compra.orden_compra:
                compra_obj.append(str(compra.orden_compra.nro_compra))
            else:
                compra_obj.append("")

            if compra.compra:
                compra_obj.append(compra.compra.codigo)
            else:
                compra_obj.append("")

            compra_obj.append(compra.total)
            compra_obj.append(compra.descripcion)

            if compra.asiento:
                compra_obj.append(compra.asiento.codigo_asiento)

            else:
                compra_obj.append("")

            if compra.anulado:
                compra_obj.append("Anulado")

            else:
                compra_obj.append("Activo")

            compra_obj.append(compra.id)

            compra_list.append(compra_obj)
        response_data = {}
        response_data['draw'] = _draw
        response_data['recordsTotal'] = len(compras)
        response_data['recordsFiltered'] = len(compras)
        response_data['data'] = compra_list
    else:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")

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
    centros = CentroCosto.objects.filter(activo=True)
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    form = DocumentoCompraForm
    puntos_venta = PuntosVenta.objects.all().order_by('id')
    ordenes = OrdenProduccion.objects.filter(aprobada=True)
    template = loader.get_template('compra/create.html')
    context = RequestContext(request, {'form': form, 'centros': centros, 'proveedores': proveedores, 'ordenes': ordenes,
                                       'sustento': sustento, 'retenciones_iva': retenciones_iva,
                                       'retenciones_fuente': retenciones_fuente,'puntos_venta': puntos_venta,
                                       'cuentas': cuentas, 'formas_pago': formas_pago,'centros_defecto':centros_defecto,
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
    puntos_venta = PuntosVenta.objects.all().order_by('id')
    formas_pago = SriFormaPago.objects.all()
    centros = CentroCosto.objects.filter(activo=True)
    proveedores = Proveedor.objects.filter(activo=True)
    form = DocumentoCompraForm(request.POST, request.FILES, instance=documento)
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    ordenes = OrdenProduccion.objects.filter(aprobada=True)
    costeo = CosteoFabricacionFacturas.objects.filter(documento_compra_id=pk)

    print retenciones_fuente

    template = loader.get_template('compra/edit.html')
    context = RequestContext(request, {'form': form, 'centros': centros, 'proveedores': proveedores,'ordenes': ordenes,
                                       'sustento': sustento, 'retenciones_iva': retenciones_iva,'costeo':costeo,
                                       'retenciones_fuente': retenciones_fuente,'centros_defecto':centros_defecto,
                                       'cuentas': cuentas, 'formas_pago': formas_pago,'puntos_venta': puntos_venta,
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
                    documento.base_no_iva_factura = request.POST['base_no_iva_factura']
                    documento.base_rise_factura = request.POST['base_rise_factura']
                    documento.puntos_venta_id = request.POST['puntos_venta']
                    
                    contador=request.POST["columnas_costeo"]
                    print 'contador'
                    print contador
                    
                    i=0
                    while int(i) <= int(contador):
                        i+= 1
                        if int(i) > int(contador):
                            print('entrosd')
                            break
                        else:
                            if 'total_kits'+str(i) in request.POST:
                                print 'entro a costeo'
                                
                                comprasdetalle=CosteoFabricacionFacturas()
                                comprasdetalle.updated_by = request.user.get_full_name()
                                comprasdetalle.created_by = request.user.get_full_name()
                                comprasdetalle.documento_compra_id =documento.id
                                comprasdetalle.fecha=documento.fecha_emision
                                comprasdetalle.porcentaje=request.POST["porcentaje_kits"+str(i)]
                                comprasdetalle.total=request.POST["total_kits"+str(i)]
                                comprasdetalle.tipo=request.POST["tipo_costeo_kits"+str(i)]
                                comprasdetalle.rubro=request.POST["rubro_kits"+str(i)]
                                comprasdetalle.created_at = datetime.now()
                                comprasdetalle.updated_at = datetime.now()
                                op=request.POST["op_kits"+str(i)]
                                if int(op) != 0:
                                    print 'entro op'
                                    comprasdetalle.orden_produccion_id=request.POST["op_kits"+str(i)]
                                comprasdetalle.save()
                                
                                documento.afecta_produccion =True
                                documento.save()

                    asientos = json.loads(request.POST['arreglo_asientos'])
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        asiento = Asiento()
                        asiento.codigo_asiento = "P" + str(now.year) + "00" + str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'FACTURA COMPRAS ' + str(documento.proveedor.nombre_proveedor.encode('utf8')) + str(
                            documento.establecimiento) + '-' + str(documento.punto_emision) + '-' + str(
                            documento.secuencial)
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe = request.POST['asiento-total-debe']
                        total_haber = request.POST['asiento-total-haber']
                        asiento.modulo = 'Transacciones-FACTURA COMPRAS '
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
                    else:
                        documento_retencion = DocumentosRetencionCompra()
                        documento_retencion.documento_compra_id= int(documento.id)
                        documento_retencion.fecha_emision=documento.fecha_emision
                        #documento_retencion.establecimiento=documento.establecimiento
                        #documento_retencion.punto_emision=documento.punto_emision
                        documento_retencion.establecimiento="000"
                        documento_retencion.punto_emision="000"
                        documento_retencion.secuencial="00000000"
                        documento_retencion.autorizacion="11192754445"
                        documento_retencion.descripcion=documento.descripcion
                        documento_retencion.valor_retenido=0
                        documento_retencion.migrado=True
                        documento_retencion.save()
                        
                        documento_retencion_detalle=DocumentosRetencionDetalleCompra()
                        documento_retencion_detalle.retencion_detalle_id=14
                        documento_retencion_detalle.base_imponible=documento.base_iva
                        documento_retencion_detalle.porcentaje_retencion=0
                        documento_retencion_detalle.valor_retenido=0
                        documento_retencion_detalle.documento_retencion_compra_id=documento_retencion.id
                        documento_retencion_detalle.migrado=True
                        documento_retencion_detalle.save()
                        
                       
                        documento.retenido = True
                        documento.save()
                        
                    
                    if request.POST['retencion_total_retenido']:
                        valor_ret=request.POST['retencion_total_retenido']
                    #print ("Prueba de hoy")
                    #print (valor_ret)
                    total=request.POST['total_factura']
                    #print ("Prueba de hoy")
                    #print (total)
                    total_pagar=float(total)-float(valor_ret)
                    #print ("Prueba de hoy")
                    #print (total_pagar)
                    documento.total_pagar = total_pagar
                    documento.valor_retenido=request.POST['retencion_total_retenido']
                    documento.save()
                    
                    try:
                        punto_venta = PuntosVenta.objects.get(id=documento.puntos_venta_id)
                    except PuntosVenta.DoesNotExist:
                        punto_venta = None
                    if punto_venta:
                        sec=punto_venta.secuencial_retencion_electronica+1
                        punto_venta.secuencial_retencion_electronica=sec
                        punto_venta.save()
                        
                        
                        
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
                    documento.no_afecta=False
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
                    documento.base_no_iva_factura = request.POST['base_no_iva_factura']
                    documento.base_rise_factura = request.POST['base_rise_factura']
                    documento.generada = False
                    documento.puntos_venta_id = request.POST['puntos_venta']
                    
                    documento.save()
                    contador=request.POST["columnas_costeo"]
                    
                    i=0
                    while int(i) <= int(contador):
                        i+= 1
                        if int(i) > int(contador):
                            print('entrosd')
                            break
                        else:
                            if 'total_kits'+str(i) in request.POST:
                                if 'id_costeo'+str(i) in request.POST:
                                    detalle_id=request.POST["id_costeo"+str(i)]
                                    detallecompra = CosteoFabricacionFacturas.objects.get(id=detalle_id)
                                    detallecompra.updated_by = request.user.get_full_name()
                                    detallecompra.documento_compra_id =documento.id
                                    detallecompra.fecha=documento.fecha_emision
                                    detallecompra.porcentaje=request.POST["porcentaje_kits"+str(i)]
                                    detallecompra.total=request.POST["total_kits"+str(i)]
                                    detallecompra.tipo=request.POST["tipo_costeo_kits"+str(i)]
                                    detallecompra.rubro=request.POST["rubro_kits"+str(i)]
                                    detallecompra.updated_at = datetime.now()
                                    op=request.POST["op_kits"+str(i)]
                                    if int(op) != 0:
                                        print 'entro op'
                                        detallecompra.orden_produccion_id=request.POST["op_kits"+str(i)]
                                   
                                    detallecompra.save()
                    
                                    print('Tiene detalle'+str(i))
                                else:
                                    comprasdetalle=CosteoFabricacionFacturas()
                                    comprasdetalle.updated_by = request.user.get_full_name()
                                    comprasdetalle.created_by = request.user.get_full_name()
                                    comprasdetalle.created_at = datetime.now()
                                    comprasdetalle.updated_at = datetime.now()
                                    comprasdetalle.documento_compra_id =documento.id
                                    comprasdetalle.fecha=documento.fecha_emision
                                    comprasdetalle.porcentaje=request.POST["porcentaje_kits"+str(i)]
                                    comprasdetalle.total=request.POST["total_kits"+str(i)]
                                    comprasdetalle.tipo=request.POST["tipo_costeo_kits"+str(i)]
                                    comprasdetalle.rubro=request.POST["rubro_kits"+str(i)]
                                    op=request.POST["op_kits"+str(i)]
                                    if int(op) != 0:
                                        print 'entro op'
                                        comprasdetalle.orden_produccion_id=request.POST["op_kits"+str(i)]
                                    comprasdetalle.save()
                                documento.afecta_produccion =True
                                documento.save()              
                    # 


                    asientos = json.loads(request.POST['arreglo_asientos'])
                    if len(asientos) > 0:
                        if documento.asiento_id:
                            asiento = Asiento.objects.get(asiento_id=documento.asiento_id)
                            asiento.glosa = 'FACTURA COMPRAS ' + str(documento.proveedor.nombre_proveedor.encode('utf8')) + str(
                                documento.establecimiento) + '-' + str(documento.punto_emision) + '-' + str(
                                documento.secuencial)
                            asiento.modulo = 'Transacciones-FACTURA COMPRAS '
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
                            asiento.codigo_asiento = "P" + str(now.year) + "00" + str(codigo_asiento)
                            asiento.fecha = cleaned_data.get('fecha_emision')
                            asiento.modulo = 'Transacciones-FACTURA COMPRAS '
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
                            
                            try:
                                punto_venta = PuntosVenta.objects.get(id=documento.puntos_venta_id)
                            except PuntosVenta.DoesNotExist:
                                punto_venta = None
                            if punto_venta:
                                sec=punto_venta.secuencial_retencion_electronica+1
                                punto_venta.secuencial_retencion_electronica=sec
                                punto_venta.save()

                    else:
                        documento_retencion = DocumentosRetencionCompra()
                        documento_retencion.documento_compra_id= int(documento.id)
                        documento_retencion.fecha_emision=documento.fecha_emision
                        documento_retencion.establecimiento=documento.establecimiento
                        documento_retencion.punto_emision=documento.punto_emision
                        documento_retencion.secuencial="00000000"
                        documento_retencion.autorizacion="11192754445"
                        documento_retencion.descripcion=documento.descripcion
                        documento_retencion.valor_retenido=0
                        documento_retencion.migrado=True
                        documento_retencion.save()
                        
                        documento_retencion_detalle=DocumentosRetencionDetalleCompra()
                        documento_retencion_detalle.retencion_detalle_id=14
                        documento_retencion_detalle.base_imponible=documento.base_iva
                        documento_retencion_detalle.porcentaje_retencion=0
                        documento_retencion_detalle.valor_retenido=0
                        documento_retencion_detalle.documento_retencion_compra_id=documento_retencion.id
                        documento_retencion_detalle.migrado=True
                        documento_retencion_detalle.save()
                        
                       
                        documento.retenido = True
                        documento.save()
                        try:
                            punto_venta = PuntosVenta.objects.get(id=documento.puntos_venta_id)
                        except PuntosVenta.DoesNotExist:
                            punto_venta = None
                        if punto_venta:
                            sec=punto_venta.secuencial_retencion_electronica+1
                            punto_venta.secuencial_retencion_electronica=sec
                            punto_venta.save()
                            
                            
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
                        asiento.modulo = 'Transacciones-RETENCION COMPRAS '
                        asiento.codigo_asiento = "RP" + str(now.year) + "00" + str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'RETENCION COMPRAS'
                        asiento.gasto_no_deducible = False
                        asiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
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
def compra_consultar_cuenta_by_codigo(request):
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
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    form = MovimientoForm
    template = loader.get_template('compra/retencion.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos,'centros_defecto':centros_defecto,
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
                        asiento.codigo_asiento = "RP" + str(now.year) + "00" + str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.modulo = 'Transacciones-Retencion Compras'
                        asiento.glosa = 'Transacciones-Retencion Compras'
                        asiento.gasto_no_deducible = False
                        asiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)

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

#-------------------------->
@login_required()
def documento_nuevo_cruces_view(request):
    clientes = Cliente.objects.all()
    documentos = TransaccionTipoDocuemento.objects.all()
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    bodegas = Bodega.objects.all()
    productos = Producto.objects.all()
    tipo_documentos = TipoDocumento.objects.all()
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    centros= CentroCosto.objects.all()
    form = DocumentoCrucesForm
    template = loader.get_template('venta/cruces.html')

    context = RequestContext(request, {'form': form, 'clientes': clientes,
                                       'centros_defecto':centros_defecto,
                                       'tipo_documentos': tipo_documentos,
                                       'centros':centros,
                                       'bodegas': bodegas, 'documentos': documentos, 'productos': productos,
                                       'cuentas': cuentas
                                       })


    return HttpResponse(template.render(context))

@login_required()
@transaction.atomic()
def documento_nuevo_cruces_crear_view(request):
     if request.method == 'POST':
        #print("post")
        cruce_form = DocumentoCrucesForm(request.POST)
        msg = ""
        if cruce_form.is_valid():
            #print ("paso")
            try:
                with transaction.atomic():
                    retenciones = json.loads(request.POST['arreglo_retenciones'])
                    if len(retenciones) > 0:
                        for retencion in retenciones:
                            vfactura = retencion['base']
                            nfactura = retencion['descripcion']
                            sfactura = retencion['valor_retenido']
                            tfactura = retencion['porcentaje']
                            snumfact = retencion['id']
                            sCliente = int(request.POST['cliente-id'])
                            snummovi = int(request.POST['factura-descripcion'])
                            Anticipo = float(request.POST['base_cero'])
                            MontoOri = float(request.POST['base_anticipo'])
                            SaldoAnt = Anticipo - float(vfactura)

                            objClien = Cliente.objects.get(id_cliente=sCliente)
                            objMovim = Movimiento.objects.get(id=snummovi)
                            objFactu = DocumentoVenta.objects.get(id=snumfact)

                            cleaned_data = cruce_form.cleaned_data
                            documento = Cruces()
                            documento.fecha = request.POST['fecha_emision']
                            documento.created_by = request.user.get_full_name()
                            documento.updated_by = request.user.get_full_name()
                            documento.created_at = datetime.now()
                            documento.updated_at = datetime.now()
                            documento.estado = True
                            documento.anulado = False
                            documento.descripcion = cleaned_data.get('descripcion')
                            documento.valor_cruce = vfactura
                            documento.comprobante = request.POST['autorizacion']
                            documento.valor_factura = tfactura
                            documento.saldo_factura = SaldoAnt
                            documento.factura = nfactura
                            documento.cliente = objClien
                            documento.documento_venta = objFactu
                            documento.movimiento = objMovim
                            documento.save()

                            detalle = CrucesDetalle()
                            detalle.movimiento = objMovim
                            detalle.documento_venta = objFactu
                            detalle.cliente = objClien
                            detalle.valor_cruce = vfactura
                            detalle.comprobante = request.POST['autorizacion']
                            detalle.save()
                            #vNulo = None
                            #objDocAV = DocumentoAbonoVenta.objects.get(documento_venta_id__isnull=N)

                            objDocAV = DocumentoAbonoVenta.objects.get(movimiento_id = snummovi, documento_venta_id=None)

                            objDocAV.documento_venta = objFactu
                            objDocAV.abono = vfactura
                            objDocAV.diferencia = SaldoAnt
                            objDocAV.cantidad_anterior_abonada = 0
                            objDocAV.updated_at = datetime.now()
                            objDocAV.updated_by = request.user.get_full_name()
                            objDocAV.save()

                            if (SaldoAnt > 0):
                                objMovim.cruce = False
                                objMovim.saldo = sfactura
                                objMovim.tipo_documento = 13

                                objMovim.save()

                                newDocAV = DocumentoAbonoVenta()
                                newDocAV.movimiento = objMovim
                                newDocAV.abono = MontoOri
                                newDocAV.created_by = request.user.get_full_name()
                                newDocAV.updated_by = request.user.get_full_name()
                                newDocAV.created_at = datetime.now()
                                newDocAV.updated_at = datetime.now()
                                newDocAV.cantidad_anterior_abonada = 0
                                newDocAV.diferencia = SaldoAnt
                                newDocAV.anulado = False
                                newDocAV.abono_inicial = 0
                                newDocAV.save()

                            else:
                                objMovim.cruce = True
                                objMovim.saldo = sfactura
                                objMovim.tipo_documento = 13
                                objMovim.save()

                        asientos = json.loads(request.POST['arreglo_asientos'])
                        if len(asientos) > 0:
                            codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                            secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                            asiento = Asiento()
                            asiento.codigo_asiento = "CR" + str(now.year) + "00" + str(codigo_asiento)
                            asiento.fecha = request.POST['fecha_emision']
                            asiento.modulo = 'Cruces-Cuentas x Cobrar'
                            asiento.glosa = 'REG CRUCE ANTICIPO ' + request.POST['autorizacion'] + ' CONTRA FACTURA ' + nfactura
                            asiento.total_debe = vfactura
                            asiento.total_haber = vfactura
                            asiento.gasto_no_deducible = False
                            asiento.save()
                            Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)

                            for item_asiento in asientos:
                                asiento_detalle = AsientoDetalle()
                                asiento_detalle.asiento_id = int(asiento.asiento_id)
                                asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                                asiento_detalle.concepto =  'REG CRUCE ANTICIPO ' + request.POST['autorizacion'] + ' CONTRA FACTURA ' + nfactura
                                asiento_detalle.debe = item_asiento['debe']
                                asiento_detalle.haber = item_asiento['haber']
                                asiento_detalle.save()

                        msg = "ok"
                        #print ("ok")
            except Exception as e:
                print (e.args)
        else:
            form_errors = cruce_form.errors
            #print ("no paso")
     else:
         cruce_form = DocumentoCrucesForm()
         #print("no post")

     response_data = {}
     response_data['result'] = msg
     return HttpResponse(json.dumps(response_data), content_type="application/json")
     #return HttpResponse('documento/venta/cruces')


#--------------------
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
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    centros= CentroCosto.objects.all()
    form = MovimientoForm
    template = loader.get_template('venta/retencion.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos,'centros_defecto':centros_defecto,
                                       'tipo_documentos': tipo_documentos, 'bancos': bancos, 'proveedores': proveedores,'centros':centros,
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
    #ventas = DocumentoVenta.objects.all()
    ventas=''
    template = loader.get_template('venta/index.html')
    context = RequestContext(request, {'ventas': ventas})
    return HttpResponse(template.render(context))

@login_required()
def documentoVentaEliminarByPkView(request, pk):
    obj = DocumentoVenta.objects.get(id=pk)

  
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
        try:
            retencion = DocumentoRetencionVenta.objects.filter(documento_venta_id=pk)
        except DocumentoRetencionVenta.DoesNotExist:
            retencion = None
        if retencion:
            for r in retencion:
                try:
                    asientor = Asiento.objects.filter(asiento_id=r.asiento_id)
                except Asiento.DoesNotExist:
                    asientor = None
                if asientor:
                    for ar in asientor:
                        ar.anulado= True
                        ar.save()
               
            

        

    return HttpResponseRedirect('/transacciones/documento/venta')

@login_required()
def documento_venta_nuevo_view(request):

    clientes = Cliente.objects.filter(activo=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True, categoria="DETALLE")
    retenciones_fuente = RetencionDetalle.objects.filter(tipo_retencion_id=1)
    retenciones_iva = RetencionDetalle.objects.filter(tipo_retencion_id=2)
    porcentaje_iva = Parametros.objects.get(clave='iva').valor
    formas_pago = SriFormaPago.objects.all()
    centros = CentroCosto.objects.filter(activo=True)
    vendedores = Vendedor.objects.all()
    puntos = PuntosVenta.objects.filter(activo=True)
    form = DocumentoVentaForm
    cuenta_iva_ventas_valor = Parametros.objects.get(clave='cuenta_iva_ventas').valor
    cuenta_ventas_valor = Parametros.objects.get(clave='cuenta_ventas').valor
    cuenta_descuento_ventas_valor = Parametros.objects.get(clave='cuenta_descuento_ventas').valor
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    if cuenta_iva_ventas_valor:
        try:
            cuenta_iva_ventas=PlanDeCuentas.objects.get(codigo_plan=cuenta_iva_ventas_valor).plan_id
        except PlanDeCuentas.DoesNotExist:
            cuenta_iva_ventas = None
       
    if cuenta_ventas_valor:
        try:
            cuenta_ventas=PlanDeCuentas.objects.get(codigo_plan=cuenta_ventas_valor).plan_id
        except PlanDeCuentas.DoesNotExist:
            cuenta_ventas = None
    
    if cuenta_descuento_ventas_valor:
        try:
            cuenta_descuento_ventas=PlanDeCuentas.objects.get(codigo_plan=cuenta_descuento_ventas_valor).plan_id
        except PlanDeCuentas.DoesNotExist:
            cuenta_descuento_ventas = None
        
        
    formas_pago_ventas = FormaPagoVentas.objects.all()
    tipo_comprobante_ventas = TipoComprobanteVentas.objects.all()
    template = loader.get_template('venta/create.html')
    context = RequestContext(request, {'form': form, 'centros': centros, 'clientes': clientes,'centros_defecto':centros_defecto,
                                       'retenciones_iva': retenciones_iva,'vendedores':vendedores,
                                       'retenciones_fuente': retenciones_fuente,'puntos':puntos,
                                       'cuentas': cuentas, 'formas_pago': formas_pago,'formas_pago_ventas':formas_pago_ventas,'tipo_comprobante_ventas':tipo_comprobante_ventas,
                                       'porcentaje_iva': porcentaje_iva,'cuenta_iva_ventas': cuenta_iva_ventas,'cuenta_ventas': cuenta_ventas,'cuenta_descuento_ventas': cuenta_descuento_ventas})
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
                    documento.guia_remision_id = request.POST['guia_remision']
                    documento.tipo_comprobante_ventas_id = request.POST['tipo_comprobante_ventas']
                    documento.save()

                    if request.POST['punto_venta'] > 0:
                        punto = PuntosVenta.objects.get(id=documento.punto_venta_id)
                        sec=punto.secuencial_factura_electronica+1
                        punto.secuencial_factura_electronica = int(sec)
                        punto.save()
                    else:
                        factura_secuencial = Secuenciales.objects.get(modulo='factura')
                        factura_secuencial.secuencial = int(request.POST['secuencial'])
                        factura_secuencial.save()
                    
                    
                    forma_pagos_ventas2=request.POST.getlist('forma_pago_ventas')
                    print forma_pagos_ventas2
                    
                    
                    if len(forma_pagos_ventas2) > 0:
                        for f in forma_pagos_ventas2:
                            IdPago = int(f[0])
                            documentov_forma_pago = DocumentoVentaFormaPago()
                            documentov_forma_pago.documento_venta_id = int(documento.id)
                            documentov_forma_pago.forma_pago_ventas_id = IdPago #int(f[0])
                            documentov_forma_pago.save()
                            

                    productos = json.loads(request.POST['arreglo_detalle'])
                    if len(productos) > 0:
                        idx = 0
                        for producto in productos:
                            idx = idx + 1
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
                            documento_detalle.descuento = producto['descuento']
                            documento_detalle.cantidad = producto['cantidad']
                            documento_detalle.subtotal = producto['total']
                            documento_detalle.producto_id = idx
                            documento_detalle.save()


                    asientos = json.loads(request.POST['arreglo_asientos'])
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        asiento = Asiento()
                        asiento.codigo_asiento = "C" + str(now.year) + "00" + str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'FACTURA VENTAS ' + smart_str(documento.cliente.nombre_cliente) +' '+ str(
                            documento.establecimiento) + '-' + str(documento.punto_emision) + '-' + str(
                            documento.secuencial)
                        asiento.gasto_no_deducible = False
                        asiento.modulo = 'Transacciones-FACTURA VENTAS '
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
    centros = CentroCosto.objects.filter(activo=True)
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

#---------------------------------->
@login_required()
def documento_venta_consultar_anticipos(request):
    if request.method == "POST" and request.is_ajax:
        cliente_id = request.POST['id']
        cursor = connection.cursor()

        query = "SELECT A.id, to_char(A.fecha_emision, 'DD/MM/YYYY') as fecha, A.tipo_anticipo_id, A.tipo_documento_id, A.numero_comprobante, "
        query += " A.porcentaje_iva, A.subtotal, A.subtotal_0, A.monto, coalesce(C.pagos, 0) pagos "
        query += " FROM movimiento A "
        query += " LEFT JOIN documento_abono_venta B ON A.id = B.movimiento_id "
        query += " LEFT JOIN anticipos_detalles C ON A.cliente_id = C.cliente_id AND A.numero_comprobante = C.numero_comprobante "
        query += " WHERE A.cliente_id = " + cliente_id
        query += " AND A.cruce is False "
        query += " AND A.activo is not False "
        query += " AND B.documento_venta_id is null "

        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")

@login_required()
def documento_venta_consultar_deudas(request):
    if request.method == "POST" and request.is_ajax:
        cliente_id = request.POST['id']
        cliente_id = request.POST['id']
        cursor = connection.cursor()
        #, total, concat(establecimiento, '-', punto_emision, '-', secuencial) as seriedoc
        query = "SELECT A.id, to_char(A.fecha_emision, 'DD/MM/YYYY') as fecha, A.establecimiento, A.punto_emision, A.secuencial, A.porcentaje_iva, A.base_iva, A.valor_iva, A.total, "
        query += "coalesce(B.abonos, 0) abonos, coalesce(C.retenciones, 0) retenciones "
        query += " FROM documento_venta A "
        query += " LEFT JOIN documento_venta_abonos B ON A.id = B.documento_venta_id "
        query += " LEFT JOIN documento_venta_retenciones C ON A.id = C.documento_venta_id "
        query += " WHERE cliente_id = " + cliente_id
        query += " AND A.activo is not False;"
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")

#-----------------------------------
@login_required()
def documento_venta_consultar_facturas(request):
    if request.method == "POST" and request.is_ajax:
        cliente_id = request.POST['id']
        cursor = connection.cursor()
        #, total, concat(establecimiento, '-', punto_emision, '-', secuencial) as seriedoc
        query = "SELECT id, to_char(fecha_emision, 'DD/MM/YYYY') as fecha, establecimiento, punto_emision, secuencial, porcentaje_iva, base_iva, base_iva_0, valor_iva, total "
        query += " FROM documento_venta "
        query += " WHERE cliente_id = " + (cliente_id)
        query += " AND retenido=false and activo is not False;"
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
                    #print cleaned_data
                    documento_retencion = DocumentoRetencionVenta()
                    documento_retencion.documento_venta = cleaned_data.get('documento_venta')
                    documento_retencion.fecha_emision = cleaned_data.get('fecha_emision')
                    documento_retencion.establecimiento = cleaned_data.get('establecimiento')
                    documento_retencion.punto_emision = cleaned_data.get('punto_emision')
                    documento_retencion.secuencial = cleaned_data.get('secuencial')
                    documento_retencion.autorizacion = cleaned_data.get('autorizacion')
                    ruc_tcredito=request.POST['ruc_con_tarjeta_credito']
                    retencion_con_tarjeta_de_credito=request.POST['retencion_con_tarjeta_credito']
                    print "Detalle de RUC tc"
                    print ruc_tcredito
                    print retencion_con_tarjeta_de_credito
                    
                    
                    documento_retencion.ruc_compania_tcredito = ruc_tcredito
                    if retencion_con_tarjeta_de_credito == 'true':
                        documento_retencion.retencion_con_tarjeta_de_credito = True
                        print retencion_con_tarjeta_de_credito
                    else:
                        documento_retencion.retencion_con_tarjeta_de_credito = False
                    documento_retencion.descripcion = cleaned_data.get('descripcion')
                    documento_retencion.save()
                    # Detalle retencion
                    
                    retenciones = json.loads(request.POST['arreglo_retenciones'])
                    print (retenciones)
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
                    print(asientos)
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        asiento = Asiento()
                        asiento.codigo_asiento = "RC" + str(now.year) + "00" + str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.modulo='Transacciones-RETENCION VENTA'
                        asiento.glosa = 'RT '+str(documento_retencion.establecimiento)+'- '+str(documento_retencion.punto_emision)+ '- '+str(documento_retencion.secuencial)+' de factura de cliente '+str(documento_retencion.documento_venta.establecimiento)+'- '+str(documento_retencion.documento_venta.punto_emision)+ '- '+str(documento_retencion.documento_venta.secuencial)
                        asiento.gasto_no_deducible = False
                        asiento.save()
                        documento_retencion.asiento=asiento
                        documento_retencion.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        for item_asiento in asientos:
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.centro_costo_id = item_asiento['centro']
                            asiento_detalle.concepto=documento_retencion.descripcion 
                            asiento_detalle.save()
                    documento_venta = cleaned_data.get('documento_venta')
                    DocumentoVenta.objects.filter(id=documento_venta.id).update(retenido=True)

            except Exception as e:
                print (e.message)
                print (e.args)
        else:
            form_errors = form.errors
            print (form_errors)
    else:
        print("ENTRO EN GET")
    #return HttpResponseRedirect('documento/venta/retencion')


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

#--------------------Cruces ------------->
@login_required()
def cruces_list_view(request):
    rentenciones = DocumentoRetencionVenta.objects.all()
    cursor = connection.cursor()

    query = "SELECT "
    query += "A.id, to_char(A.fecha, 'DD/MM/YYYY'), A.movimiento_id, A.documento_venta_id, A.cliente_id, B.nombre_cliente, A.factura, "
    query += "A.valor_factura, A.saldo_factura, A.valor_cruce, A.comprobante, A.estado, (A.valor_factura - A.valor_cruce) saldo "
    query += "from cruces A "
    query += "left join cliente B on A.cliente_id = B.id_cliente "
    query += "where A.estado is Not False and B.activo is True "

    cursor.execute(query)
    ro = cursor.fetchall()
    template = loader.get_template('venta/cruces_index.html')
    context = RequestContext(request, {'rentenciones': rentenciones,'cruces_actual': ro})
    return HttpResponse(template.render(context))




#----------------------------------------
@login_required()
def documento_venta_retencion_list_view(request):
    rentenciones = DocumentoRetencionVenta.objects.all()
    cursor = connection.cursor()
    #query="select drv.id,drv.fecha_emision,c.nombre_cliente,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,drv.descripcion,dv.establecimiento,dv.punto_emision,dv.secuencial,sum(dvd.valor_retenido),dv.id,drv.anulado from documento_retencion_venta drv,documento_retencion_detalle_venta dvd,documento_venta dv,cliente c where dvd.documento_retencion_venta_id=drv.id and dv.id=drv.documento_venta_id and dv.cliente_id=c.id_cliente group by drv.id,dv.establecimiento,dv.punto_emision,dv.secuencial,c.nombre_cliente,dv.id "
    #query="select drv.id,drv.fecha_emision,c.nombre_cliente,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,drv.descripcion,dv.establecimiento,dv.punto_emision,dv.secuencial,sum(dvd.valor_retenido),dv.id,drv.anulado,periodos from documento_retencion_venta drv,documento_retencion_detalle_venta dvd,documento_venta dv,cliente c,(SELECT b.id as periodos,p.id FROM documento_retencion_venta  p LEFT JOIN bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM p.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from p.fecha_emision)) G where G.id= drv.id and dvd.documento_retencion_venta_id=drv.id and dv.id=drv.documento_venta_id and dv.cliente_id=c.id_cliente group by drv.id,dv.establecimiento,dv.punto_emision,dv.secuencial,c.nombre_cliente,dv.id,G.periodos"
    #query="select drv.id,drv.fecha_emision,c.nombre_cliente,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,drv.descripcion,dv.establecimiento,dv.punto_emision,dv.secuencial,sum(dvd.valor_retenido),dv.id,drv.anulado,periodos,a.codigo_asiento from documento_retencion_venta drv,documento_retencion_detalle_venta dvd,documento_venta dv,cliente c,contabilidad_asiento a,(SELECT b.id as periodos,p.id FROM documento_retencion_venta  p LEFT JOIN bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM p.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from p.fecha_emision)) G where G.id= drv.id and dvd.documento_retencion_venta_id=drv.id and dv.id=drv.documento_venta_id and dv.cliente_id=c.id_cliente  and a.asiento_id=drv.asiento_id group by drv.id,dv.establecimiento,dv.punto_emision,dv.secuencial,c.nombre_cliente,dv.id,G.periodos,a.codigo_asiento"
    query="select drv.id,to_char(drv.fecha_emision, \'YYYY-MM-DD\'),c.nombre_cliente,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,drv.descripcion,dv.establecimiento,dv.punto_emision,dv.secuencial,sum(dvd.valor_retenido),dv.id,drv.anulado,b.id,a.codigo_asiento from documento_retencion_venta drv left join documento_retencion_detalle_venta dvd on dvd.documento_retencion_venta_id=drv.id left join documento_venta dv on  dv.id=drv.documento_venta_id left join cliente c on dv.cliente_id=c.id_cliente left join contabilidad_asiento a  on a.asiento_id=drv.asiento_id left join bloqueo_periodo b on date_part('year',b.fecha)=EXTRACT(YEAR FROM drv.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from drv.fecha_emision) where  1=1 group by drv.id,dv.establecimiento,dv.punto_emision,dv.secuencial,c.nombre_cliente,dv.id,a.codigo_asiento,b.id order by drv.id"
    cursor.execute(query)
    ro = cursor.fetchall()
    template = loader.get_template('venta/retencion_index.html')
    context = RequestContext(request, {'rentenciones': rentenciones,'retenciones_actual': ro})
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
        #query = 'SELECT id,codigo,to_char(fecha, \'YYYY-MM-DD\') as fecha,total,descuento FROM proforma  WHERE aprobada = TRUE AND cliente_id = ' + (id) + ' ORDER BY fecha DESC;'
        query='SELECT proforma.id,proforma.codigo,to_char(proforma.fecha, \'YYYY-MM-DD\'),proforma.total,proforma.descuento, sum(documento_venta.total) FROM proforma  left join documento_venta  on documento_venta.proforma_id=proforma.id and documento_venta.activo is True  WHERE proforma.aprobada = TRUE AND proforma.cliente_id = ' + (id) + ' group by proforma.id,proforma.codigo,proforma.fecha,proforma.total,proforma.descuento ORDER BY proforma.fecha DESC'
        print query
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
        query = 'SELECT pd.id,pd.nombre,pd.producto_id,pd.cantidad,pd.precio_compra,pd.total,p.iva,p.total FROM proforma_detalle pd,proforma p  WHERE pd.proforma_id=p.id and pd.no_producir <> TRUE AND pd.proforma_id = ' + (id) + ';'
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
    detalle = DocumentosVentaDetalle.objects.filter(documento_venta_id=pk).order_by('id')
    #total_haber = sum(d.haber for d in detalle)
    #total_debe = sum(d.debe for d in detalle)
    rango = 10 - len(detalle)
    now = datetime.now()
    total_letras1=''
    total_letras2=''
    if len(documento.total_en_letras)>45:
        total_letras1=documento.total_en_letras[0:45]
        total_letras2=documento.total_en_letras[45:]
    else:
        total_letras1=documento.total_en_letras
    html = loader.get_template('venta/factura_imprimir.html')
    context = RequestContext(request,
                             { 'documento': documento, 'detalle': detalle,'fecha': now,'rango':range(rango),'total_letras1':total_letras1,'total_letras2':total_letras2})
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
    rango = 36 - len(detalle)
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
    rango = 18- len(detalle)
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
    
    retencion = DocumentoRetencionVenta.objects.get(id=pk)
    documento = DocumentoVenta.objects.get(id=retencion.documento_venta_id)
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
    rango = int(20 - len(detalle))
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



@login_required()
def export_to_pdf_factura(request,pk):


    # your excel html format
    template_name = "fatura_imprimir_pdf.html"
    documento = DocumentoVenta.objects.get(id=pk)
    detalle = DocumentosVentaDetalle.objects.filter(documento_venta_id=pk)
    rango = int(20 - len(detalle))
    lista = []
    for i in range(0,rango):
        lista.append(i)
    print rango
    now = datetime.now()
    


    response = render_to_response('venta/fatura_imprimir_pdf.html', {'documento':documento,'lista':lista,'detalle':detalle})

    # this is the output file
    nombre='FACTURA_'+documento.establecimiento+'-'+documento.punto_emision+'-'+documento.secuencial
    filename = nombre+'.xls'

    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/pdf; charset=utf-16'
    return response



@login_required()
@csrf_exempt
def validarFactura(request):
    if request.method == 'POST':
      establecimiento = request.POST.get('establecimiento')
      punto = request.POST.get('punto')
      secuencial = request.POST.get('secuencial')
      tipo= request.POST.get('tipo')
      proveedor= request.POST.get('proveedor')
      id = request.POST.get('id')
      #objetos = Proveedor.objects.get(ruc = ruc)
      #modulo_secuencial = objetos.proveedor_id
      
      cursor = connection.cursor()
      if id == '0':
            query = "select id,descripcion from documento_compra where establecimiento='" + (establecimiento) + "' and punto_emision='" + (punto) + "' and secuencial='" + (secuencial) + "' and tipo_provision='" + (tipo) + "' and anulado is not True"
            
      else:
             query = "select id,descripcion from documento_compra where establecimiento='" + (establecimiento) + "' and punto_emision='" + (punto) + "' and secuencial='" + (secuencial) + "' and tipo_provision='" + (tipo)+ "' and id!="+ (id) +" and anulado is not True"
      if proveedor:
             query+=" and proveedor_id=" + (proveedor) 
      print query
      cursor.execute(query)
      ro = cursor.fetchall()
      json_resultados = json.dumps(ro)
      return HttpResponse(json_resultados, content_type="application/json")


    else:
        raise Http404
    
    
    
    

def imprimir_pdf_retencion_view(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    documento = DocumentoCompra.objects.get(id=pk)
    retencion = DocumentosRetencionCompra.objects.get(documento_compra_id=pk)
    detalle = DocumentosRetencionDetalleCompra.objects.filter(documento_retencion_compra_id=retencion.id)
    total = sum(d.valor_retenido for d in detalle)
    rango = 4 - len(detalle)
    now = datetime.now()
    html = loader.get_template('compra/retencion_imprimir_pdf.html')
    context = RequestContext(request, {'documento': documento, 'retencion': retencion, 'detalle': detalle,
                             'fecha': now, 'total': total, 'rango': range(rango)})
    return HttpResponse(html.render(context))

@login_required()
def retencionVentaEliminarByPkView(request, pk):
    try:
        obj = DocumentoRetencionVenta.objects.get(id=pk)
    except DocumentoRetencionVenta.DoesNotExist:
        obj=None
   

    if obj:
        obj.anulado = True
        obj.save()
        
        try:
            asiento = Asiento.objects.filter(asiento_id=obj.asiento_id)
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            for a in asiento:
                a.anulado= True
                a.save()
        try:
            ob = DocumentoVenta.objects.get(id=obj.documento_venta_id)
        except DocumentoVenta.DoesNotExist:
            ob=None
        if ob:
            ob.retenido=False
            ob.save()

    return HttpResponseRedirect('/transacciones/documento/venta/retencion')


@login_required()
@transaction.atomic()
def retencion_venta_consultar_view(request, pk):

    retencion = DocumentoRetencionVenta.objects.get(id=pk)
    detalle = DocumentoRetencionDetalleVenta.objects.filter(documento_retencion_venta_id=pk)
    asientos = AsientoDetalle.objects.filter(asiento_id=retencion.asiento_id)
    
    template = loader.get_template('venta/retencion_consultar.html')
    context = RequestContext(request, {'retencion': retencion, 'detalle': detalle, 'asientos': asientos})
    return HttpResponse(template.render(context))

@login_required()
def impresion_factura_venta_prueba_view(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    documento = DocumentoVenta.objects.get(id=pk)
    detalle = DocumentosVentaDetalle.objects.filter(documento_venta_id=pk)
    #total_haber = sum(d.haber for d in detalle)
    #total_debe = sum(d.debe for d in detalle)
    rango = 10 - len(detalle)
    now = datetime.now()
    html = loader.get_template('venta/factura_imprimir_prueba.html')
    context = RequestContext(request,
                             { 'documento': documento, 'detalle': detalle,'fecha': now,'rango':range(rango)})
    return HttpResponse(html.render(context))


@login_required()
@csrf_exempt
def documento_compra_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order=request.GET['order[0][column]']
        _order_dir=request.GET['order[0][dir]']
        cursor = connection.cursor()
        sql="select c.id,c.fecha_emision,p.nombre_proveedor,c.establecimiento,c.punto_emision,c.secuencial,o.nro_compra,cl.codigo,c.total,c.descripcion,a.codigo_asiento,c.anulado,c.retenido,c.asiento_id,sum(ab.abono),c.facturacion_eletronica from documento_compra c left join contabilidad_asiento a on a.asiento_id=c.asiento_id left join proveedor p on p.proveedor_id=c.proveedor_id left join orden_compra o on o.compra_id=c.orden_compra_id left join compras_locales cl on cl.id=c.compra_id left join documento_abono ab on ab.documento_compra_id=c.id and ab.anulado is not True  where 1=1 "
        if _search_value:
            sql+=" and UPPER(p.nombre_proveedor) like '%"+_search_value+"%' or UPPER(c.establecimiento) like '%"+_search_value.upper()+"%' or UPPER(c.punto_emision) like '%"+_search_value.upper()+"%' or UPPER(c.secuencial) like '%"+_search_value.upper()+"%' or CAST(o.nro_compra as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(c.total as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(c.fecha_emision as VARCHAR)  like '%"+_search_value+"%' or UPPER(cl.codigo) like '%"+_search_value.upper()+"%' or UPPER(c.descripcion) like '%"+_search_value.upper()+"%' or UPPER(a.codigo_asiento) like '%"+_search_value.upper()+"%'"
        
        if _search_value.upper()=='ANULADO'  or _search_value.upper()=='AN' or _search_value.upper()=='ANU' or _search_value.upper()=='ANUL'  or _search_value.upper()=='ANULA' or _search_value.upper()=='ANULAD':
            sql+=" or c.anulado is True"
        
        if _search_value.upper()=='ACTIVO' or _search_value.upper()=='AC' or _search_value.upper()=='ACT' or _search_value.upper()=='ACTI' or _search_value.upper()=='ACTIV':
            sql+=" or c.anulado is not True"
           
    
        #sql +=" order by fecha"
        sql +=" group by c.id,c.fecha_emision,p.nombre_proveedor,c.establecimiento,c.punto_emision,c.secuencial,o.nro_compra,cl.codigo,c.total,c.descripcion,a.codigo_asiento,c.anulado,c.retenido,c.asiento_id"
        print _order
        if _order == '0':
            sql +=" order by c.fecha_emision "+_order_dir
        if _order == '1':
            sql +=" order by p.nombre_proveedor "+_order_dir
            
        if _order == '2':
            sql +=" order by c.establecimiento,c.punto_emision,c.secuencial "+_order_dir
        if _order == '3':
            sql +=" order by CAST(o.nro_compra AS Numeric(10,0)) "+_order_dir
        
        if _order == '4':
            sql +=" order by CAST(cl.codigo  AS Numeric(10,0)) "+_order_dir
        
        if _order == '5':
            sql +=" order by cl.total "+_order_dir
        if _order == '6':
            sql +=" order by c.descripcion "+_order_dir
        if _order == '7':
            sql +=" order by a.codigo_asiento "+_order_dir
        
        if _order == '8':
            sql +=" order by c.anulado "+_order_dir
        print sql
        cursor.execute(sql)
        compras = cursor.fetchall()
            
        compras_filtered = compras[_start:_start + _end]

        compras_list = []
        for o in compras_filtered:
            mes=o[1].month
            anio=o[1].year
            cursor = connection.cursor()
            query="select anio_id,mes_id from bloqueo_periodo  where date_part('year',fecha)='"+str(anio)+"' and date_part('month',fecha)='"+str(mes)+"'"
            cursor.execute(query)
            ro = cursor.fetchall()
            
            compras_obj = []
            compras_obj.append(o[1].strftime('%Y-%m-%d'))
            compras_obj.append(o[2])
            factura=''+str(o[3])+'-'+str(o[4])+'-'+str(o[5])
            compras_obj.append(factura)
            compras_obj.append(o[6])
            compras_obj.append(o[7])
            compras_obj.append(o[8])
            
            compras_obj.append(o[9])
            compras_obj.append(o[10])
            html=''

            if o[11]:
                compras_obj.append("Anulado")
                if o[13]:
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/transacciones/documento/compra/asiento/'+str(o[0])+'/imprimir" style="position: relative;"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-print"></i></button></a>'
                

            else:
                compras_obj.append("Activo")
                if ro:
                    r=1
                else:
                    if o[14] < 1:
                        html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/transacciones/documento/compra/'+str(o[0])+'/editar/"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-pencil"></i></button></a>'
                    
                        html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/transacciones/documento/compra/'+str(o[0])+'/eliminar" style="" onclick="return confirm(¿Está seguro de anular esta factura?)"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-trash"></i></button></a>'
                if o[12]:
                    
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/transacciones/retencion/'+str(o[0])+'/imprimirpdf/"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-list"></i></button></a>'
                    
                    
                if o[13]:

                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/transacciones/documento/compra/asiento/'+str(o[0])+'/imprimir" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-print"></i></button></a>'
                if o[15]:
                    print 'fe'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/transacciones/consultar_datos_retencion_electronica/'+str(o[0])+'/" target="_blank"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye"></i>Ver retencion electronica</button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/transacciones/documento/compra/'+str(o[0])+'/eliminar" style="" onclick="return confirm(¿Está seguro de anular esta factura?)"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-trash"></i></button></a>'

                    
                else:
                    fecha_inicio = o[1].strftime('%Y-%m-%d')
                    if str(o[1].year) == '2017':
                        print 'f'
                    else:
                        html+='<a href="#" onclick="mostrarRetencionElectronica('+str(o[0])+')" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye">Retenc. Electronica</i></button></a>'
                    
                
            
            html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/transacciones/documento/compra/'+str(o[0])+'/consultar" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye"></i></button></a>'

            
           
            
            

            compras_obj.append(html)

            compras_list.append(compras_obj)
        response_data = {}
        response_data['draw'] = _draw
        response_data['recordsTotal'] = len(compras)
        response_data['recordsFiltered'] = len(compras)
        response_data['data'] = compras_list
    else:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def documento_venta_api_view(request):
    if request.method == "POST" and request.is_ajax:
        cursor = connection.cursor()
        sql="select c.id,to_char(c.fecha_emision, \'YYYY/MM/DD\') as fecha,p.nombre_cliente,c.establecimiento,c.punto_emision,c.secuencial,o.nombre,c.base_iva,c.valor_iva,c.total,c.descripcion,a.codigo_asiento,c.activo,c.asiento_id,b.id,c.facturacion_eletronica,c.id_facturacion_eletronica from documento_venta c left join contabilidad_asiento a on a.asiento_id=c.asiento_id left join cliente p on p.id_cliente=c.cliente_id left join puntos_venta o on o.id=c.punto_venta_id left join bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM c.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from c.fecha_emision) where 1=1  order by c.fecha_emision desc"
        print sql
        cursor.execute(sql)
    
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")

@login_required()
def consultar_factura_venta_view(request,pk):
    
    factura = DocumentoVenta.objects.get(pk=pk)
    facturas = DocumentosVentaDetalle.objects.filter(documento_venta_id=pk)
  
    try:
        asientos = Asiento.objects.get(asiento_id=factura.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=factura.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None
    total_asientos_debe1=AsientoDetalle.objects.filter(asiento_id=factura.asiento_id).aggregate(Sum('debe'))
    total_asientos_haber1=AsientoDetalle.objects.filter(asiento_id=factura.asiento_id).aggregate(Sum('haber'))
    total_asientos_debe=0
    total_asientos_haber=0
    if total_asientos_debe1['debe__sum']:
        total_asientos_debe=total_asientos_debe1['debe__sum']
    else:
        total_asientos_debe1=0
    
    if total_asientos_haber1['haber__sum']:
        total_asientos_haber=total_asientos_haber1['haber__sum']
    else:
        total_asientos_haber1=0



    template = loader.get_template('venta/factura_consultar.html')
    context = RequestContext(request, {'factura': factura, 'facturas': facturas,'asientos': asientos,'detalle_asientos':detalle_asientos,'total_asientos_debe':total_asientos_debe,'total_asientos_haber':total_asientos_haber})
    return HttpResponse(template.render(context))




@login_required()
@transaction.atomic()
def documento_compra_consultar_view(request, pk):
    documento = DocumentoCompra.objects.get(id=pk)
    cuentas = PlanDeCuentas.objects.filter(activo=True, categoria="DETALLE")
    total_valor_retenido=0
    try:
        documento_retencion = DocumentosRetencionCompra.objects.get(documento_compra_id=pk)
    except DocumentosRetencionCompra.DoesNotExist:
        documento_retencion = None
    if documento_retencion:
        try:
            documento_retencion_detalle = DocumentosRetencionDetalleCompra.objects.filter(documento_retencion_compra_id=documento_retencion.id)
        except DocumentosRetencionDetalleCompra.DoesNotExist:
            documento_retencion_detalle = None
        
        total_valor_ret=DocumentosRetencionDetalleCompra.objects.filter(documento_retencion_compra_id=documento_retencion.id).aggregate(Sum('valor_retenido'))
        if total_valor_ret['valor_retenido__sum']:
            total_valor_retenido=total_valor_ret['valor_retenido__sum']
        else:
            total_valor_retenido=0
        
            
    else:
        documento_retencion_detalle = None
    
    

        
        
        
    try:
        asientos = Asiento.objects.get(asiento_id=documento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=documento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None
    total_asientos_debe1=AsientoDetalle.objects.filter(asiento_id=documento.asiento_id).aggregate(Sum('debe'))
    total_asientos_haber1=AsientoDetalle.objects.filter(asiento_id=documento.asiento_id).aggregate(Sum('haber'))
    if total_asientos_debe1['debe__sum']:
        total_asientos_debe=total_asientos_debe1['debe__sum']
    else:
        total_asientos_debe1=0
        total_asientos_debe=0
    
    if total_asientos_haber1['haber__sum']:
        total_asientos_haber=total_asientos_haber1['haber__sum']
    else:
        total_asientos_haber1=0
        total_asientos_haber=0
        

    
    porcentaje_iva = Parametros.objects.get(clave='iva').valor
    formas_pago = SriFormaPago.objects.all()
    form = DocumentoCompraForm(request.POST, request.FILES, instance=documento)

    template = loader.get_template('compra/consultar.html')
    context = RequestContext(request, {'form': form,  'asientos': asientos,'detalle_asientos':detalle_asientos,
                                       'total_asientos_debe':total_asientos_debe,'total_asientos_haber':total_asientos_haber,
                                       'cuentas': cuentas, 'formas_pago': formas_pago,
                                       'documento_retencion':documento_retencion,'total_valor_retenido':total_valor_retenido,
                                       'documento_retencion_detalle':documento_retencion_detalle,
                                       'porcentaje_iva': porcentaje_iva, 'documento': documento})
    return HttpResponse(template.render(context))

@login_required()
def consultar_guias_remision_cliente(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        cursor = connection.cursor()
        #query = 'SELECT id,codigo,to_char(fecha, \'YYYY-MM-DD\') as fecha,total,descuento FROM proforma  WHERE aprobada = TRUE AND cliente_id = ' + (id) + ' ORDER BY fecha DESC;'
        query='SELECT guia.guia_id,guia.nro_guia,to_char(guia.fecha_inicio, \'YYYY-MM-DD\'), tg.descripcion FROM facturacion_guiaremision guia  left join tipo_guia tg  on tg.id=guia.tipo_guia_id WHERE guia.activo is True and  guia.aprobada is True  AND guia.cliente_id = ' + (id) + '  ORDER BY guia.nro_guia DESC'
        print query
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
@transaction.atomic
def consultar_facturacion_electronica(request):
    #db = MySQLdb.connect(host="104.192.6.75, user="sa",passwd="U7BKm3eayFCn9cTx", db="FacturaNotaCreditoYDebito")
    with transaction.atomic():
        id = request.POST['id']
        try:
            factura = DocumentoVenta.objects.get(id=id)
        except DocumentoVenta.DoesNotExist:
            factura = None
        
        ambiente=''
        tipoEmision=''
        razonSocial=''
        nombreComercial=''
        dirMatriz=''
        contribuyenteEspecial=''
        obligadoContabilidad='SI'
        moneda=''
        
        
        valor_ambiente = Parametros.objects.get(clave='fe_ambiente').valor
        ambiente=valor_ambiente
        
        tipoEmision='1'
        valor_razonSocial=Parametros.objects.get(clave='fe_razonSocial').valor
        razonSocial=valor_razonSocial
        
        valor_nombreComercial=Parametros.objects.get(clave='fe_nombreComercial').valor
        nombreComercial=valor_nombreComercial
        
        valor_dirMatriz=Parametros.objects.get(clave='fe_direccion').valor
        dirMatriz=valor_dirMatriz
        
        valor_contribuyenteEspecial=Parametros.objects.get(clave='fe_contribuyenteEspecial').valor
        contribuyenteEspecial=valor_contribuyenteEspecial
        
        valor_moneda=Parametros.objects.get(clave='fe_moneda').valor
        moneda=valor_moneda
        
        dirEstablecimiento=Parametros.objects.get(clave='fe_direccion').valor
        ruc=Parametros.objects.get(clave='fe_ruc').valor
        iva=Parametros.objects.get(clave='iva').valor
        id_f=Parametros.objects.get(clave='fe_factura_nota_credito').valor
        #CASO DE NOTA DE CREDITO O DEBITO
        codDocModificado=''
        numDocModificado=''
        fechaEmisionDocSustento=''
        valorModificacion=0
        #FIN DE NOTA DE CREDITO O DEBITO
        
        
        tipoIdentificacionComprador=''
        guiaRemision=''
        razonSocialComprador=''
        identificacionComprador=''
        totalSinImpuestos=0
        totalDescuento=0
        importeTotal=0
        
        motivo=''
        direccion=''
        telefono=''
        email=''
        codigoPorcentajeICE=0
        tarifaICE=0
        baseICE=0
        valorICE=0
        baseIVA0=0
        valorIVA0=0
        baseIVA12=0
        valorIVA12=0
        direccionComprador=''
        propina=0
        
        baseIVA14=0
        valorIVA14=0
    
        if factura:
            if factura.id_facturacion_eletronica:
                print 'ya existe el id'
                html= 'Ya existe esa factura en el sistema'
                return HttpResponse(html)
            else:
                
                if factura.razon_social_id:
                    razonSocialComprador=factura.razon_social.nombre
                    identificacionComprador=factura.razon_social.ruc
                    direccionComprador=factura.razon_social.direccion1
                    email=factura.razon_social.email1
                    #ruc=factura.razon_social.ruc
                    if len(factura.razon_social.ruc)>10:
                        tipoIdentificacionComprador='04'
                        
                    else:
                        tipoIdentificacionComprador='05'
                    
                    
                else:
                    razonSocialComprador=factura.cliente.nombre_cliente
                    email=factura.cliente.email1
                    
                    direccionComprador=factura.cliente.direccion1
                    ruc=factura.cliente.ruc.replace(' ', '')
                    
                    if len(ruc)>10:
                        identificacionComprador=factura.cliente.ruc
                        tipoIdentificacionComprador='04'
                        #ruc=factura.cliente.ruc
                    else:
                        identificacionComprador=factura.cliente.cedula
                        tipoIdentificacionComprador='05'
                        #ruc=factura.cliente.cedula
                        
                    
                    
                if factura.guia_remision_id:
                    guiaRemision=factura.guia_remision.nro_guia
                    
                
                
                
                motivo=factura.descripcion
                direccion=smart_str(factura.direccion)
                telefono=factura.telefono
                direccionComprador=smart_str(factura.direccion)
                
                
                subtotal=float(factura.subtotal)-float(factura.descuento)
                totalSinImpuestos=subtotal
                totalDescuento=factura.descuento
                importeTotal=factura.total
                codigoPorcentajeICE=0
                tarifaICE=0
                baseICE=0
                valorICE=0
                if factura.base_iva_0:
                    baseIVA0=factura.base_iva_0
                    
                valorIVA0=factura.valor_iva_0
                #baseIVA12=factura.base_iva
                baseIVA12=subtotal
                valorIVA12=factura.valor_iva
                
                secuencialTransaccion=''
                tipoDocTransaccion=''
                
                if factura.valor_iva == 0:
                    baseIVA0=subtotal
                    baseIVA12=0.00
                    valorIVA12=0.00
                #print 'CONEXION'
                fecha=factura.fecha_emision.strftime('%Y-%m-%d')
                
                
                if direccion == '' or telefono =='' or email =='':
                    html='Revise los datos del proveedor Direccion,telefono o email'
                else:
            
                    conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
                    cursor = conn.cursor()
                    sqlCommanf="INSERT INTO infoDocumentoCliente (id,ambiente,tipoEmision,razonSocial,nombreComercial,ruc,codDoc,estab,ptoEmi,secuencial,secuencialTransaccion,tipoDocTransaccion,dirMatriz,fechaEmision,dirEstablecimiento,contribuyenteEspecial,obligadoContabilidad,codDocModificado,numDocModificado,fechaEmisionDocSustento,valorModificacion,tipoIdentificacionComprador,guiaRemision,razonSocialComprador,identificacionComprador,totalSinImpuestos,totalDescuento,propina,importeTotal,moneda,motivo,direccion,telefono,email,codigoPorcentajeICE,tarifaICE,baseICE,valorICE,baseIVA0,valorIVA0,baseIVA12,valorIVA12,direccionComprador,baseIVA14,valorIVA14) values ("+str(id_f)+",'"+str(ambiente)+"','"+str(tipoEmision)+"','"+str(razonSocial)+"','"+str(nombreComercial)+"','"+str(ruc)+"','01','"+str(factura.establecimiento)+"','"+str(factura.punto_emision)+"','"+str(factura.secuencial)+"','"+str(secuencialTransaccion)+"','"+str(tipoDocTransaccion)+"','"+str(dirMatriz)+"','"+str(fecha)+"','"+str(dirEstablecimiento)+"','"+str(contribuyenteEspecial)+"','"+str(obligadoContabilidad)+"','"+str(codDocModificado)+"','"+str(numDocModificado)+"',NULL,"+str(valorModificacion)+",'"+str(tipoIdentificacionComprador)+"','"+str(guiaRemision)+"','"+str(razonSocialComprador.encode('utf8'))+"','"+str(identificacionComprador)+"',"+str(totalSinImpuestos)+","+str(totalDescuento)+","+str(propina)+","+str(importeTotal)+",'"+str(moneda)+"','"+str(motivo.encode('utf8'))+"','"+str(direccion)+"','"+str(telefono)+"','"+str(email)+"','"+str(codigoPorcentajeICE)+"',"+str(tarifaICE)+","+str(baseICE)+","+str(valorICE)+","+str(baseIVA0)+","+str(valorIVA0)+","+str(baseIVA12)+","+str(valorIVA12)+",'"+str(direccionComprador)+"',"+str(baseIVA14)+","+str(valorIVA14)+")"
                    print sqlCommanf
                    cursor.execute(sqlCommanf)
                    conn.commit()
                    
                    #post_id = cursor.lastrowid
                    #post_id = factura.id
                    post_id =id_f
                    print post_id
            
                    
                    secuencia=1
                    
                    codigoPrincipal=''
                    codigoAuxiliar=''
                    fdescripcion=''
                    precioUnitario=0
                    cantidad=0
                    
                    try:
                        factura_detalle = DocumentosVentaDetalle.objects.filter(documento_venta_id=factura.id)
                    except DocumentosVentaDetalle.DoesNotExist:
                        factura_detalle = None
                    if  factura_detalle:
                        for f in factura_detalle:
                            codigoPrincipal='0000000'
                            codigoAuxiliar='0000000'
                            fdescripcion=smart_str(f.descripcion)
                            
                            
                            if iva=='12':
                                fuprecio_iva=f.base_iva*0.12
                            
                            
                            fsin_impuesto=float(f.base_iva)-float(fuprecio_iva)
                                
                            precioUnitario=f.base_iva
                            cantidad=f.cantidad
                            fdescuento=f.descuento
                            subtotal_detalle=float(f.subtotal)-float(f.descuento)
                            #fprecioTotalSinImpuesto=f.subtotal
                            fprecioTotalSinImpuesto=subtotal_detalle
                            fcodigoPorcentajeICE=0
                            ftarifaICE=0
                            fbaseICE=0
                            fvalorICE=0
                            fbaseIVA0=0
                            fvalorIVA0=0
                            
                            fbaseIVA12=subtotal_detalle
                            valorfIVA12=subtotal_detalle*0.12
                            
                            fvalorIVA12=valorfIVA12
                            funidadMedida=''
                            fcodigoPorcentajeIVA=''
                            
                            if factura.valor_iva== 0:
                                fbaseIVA0=subtotal_detalle
                                fvalorIVA0=0
                                
                                fbaseIVA12=0
                                valorfIVA12=0
                                fvalorIVA12=0
                                
                            
                            if iva=='12':
                                fcodigoPorcentajeIVA='02'
                            else:
                                if iva=='14':
                                    fcodigoPorcentajeIVA='03'
                                else:
                                    fcodigoPorcentajeIVA='0'
                                
                            
                            sqlComman1="INSERT INTO detalleInfoDocumentoCliente (id,secuencia,codigoPrincipal,codigoAuxiliar,descripcion,cantidad,precioUnitario,descuento,precioTotalSinImpuesto,codigoPorcentajeICE,tarifaICE,baseICE,valorICE,baseIVA0,valorIVA0,baseIVA12,valorIVA12,unidadMedida,codigoPorcentajeIVA) values ("+str(post_id)+","+str(secuencia)+",'"+str(codigoPrincipal)+"','"+str(codigoAuxiliar)+"','"+str(fdescripcion)+"',"+str(cantidad)+","+str(precioUnitario)+","+str(fdescuento)+","+str(fprecioTotalSinImpuesto)+","+str(fcodigoPorcentajeICE)+","+str(ftarifaICE)+","+str(fbaseICE)+","+str(fvalorICE)+","+str(fbaseIVA0)+","+str(fvalorIVA0)+","+str(fbaseIVA12)+","+str(fvalorIVA12)+",'"+str(funidadMedida)+"','"+str(fcodigoPorcentajeIVA)+"')"
                            #print sqlComman1
                            cursor.execute(sqlComman1)
                            conn.commit()
                            secuencia=secuencia+1
                    
                    
                    
                    try:
                        factura_fpago = DocumentoVentaFormaPago.objects.filter(documento_venta_id=factura.id)
                    except DocumentoVentaFormaPago.DoesNotExist:
                        factura_fpago = None
                    
                    secuenciafpago=1
                    if factura_fpago:
                        for fp in factura_fpago:
                            formaPago=fp.forma_pago_ventas.codigo
                            fptotal=fp.documento_venta.total
                            try:
                                v_plazo = Parametros.objects.get(clave='fe_dias_plazo').valor
                            except Parametros.DoesNotExist:
                                v_plazo = 15
                            
                                
                                
                            #v_plazo=Parametros.objects.get(clave='fe_dias_plazo').valor
                            fpplazo=v_plazo
                            fpunidadTiempo='dias'
                            sqlComman2="INSERT INTO infoFormaPago (id,secuencia,formaPago,total,plazo,unidadTiempo) values ("+str(post_id)+","+str(secuenciafpago)+",'"+str(formaPago)+"',"+str(fptotal)+",'"+str(fpplazo)+"','"+str(fpunidadTiempo)+"')"
                            #print sqlComman2
                            cursor.execute(sqlComman2)
                            conn.commit()
                        
                        
                            secuenciafpago=secuenciafpago+1
        
        
                    html='Se ingreso la factura electronicamente'
                    factura.facturacion_eletronica=True
                    factura.id_facturacion_eletronica=int(post_id)
                    factura.save()
                    try:
                        param = Parametros.objects.get(clave='fe_factura_nota_credito')
                    except Parametros.DoesNotExist:
                        param = None
                    if param:
                        valor_f=int(post_id)+1
                        param.valor= valor_f
                        param.save()
                
                return HttpResponse(html)
    
        else:
            raise Http404    
        
        
        
@login_required()
@transaction.atomic
def consultar_retencion_electronica(request):
    #db = MySQLdb.connect(host="104.192.6.75, user="sa",passwd="U7BKm3eayFCn9cTx", db="FacturaNotaCreditoYDebito")
    with transaction.atomic():
        fid = request.POST['id']
        try:
            factura = DocumentosRetencionCompra.objects.get(documento_compra_id=fid)
        except DocumentosRetencionCompra.DoesNotExist:
            factura = None
        
        ambiente=''
        tipoEmision=''
        razonSocial=''
        nombreComercial=''
        dirMatriz=''
        contribuyenteEspecial=''
        obligadoContabilidad='SI'
        moneda=''
        
        
        valor_ambiente = Parametros.objects.get(clave='fe_ambiente').valor
        ambiente=valor_ambiente
        
        tipoEmision='1'
        valor_razonSocial=Parametros.objects.get(clave='fe_razonSocial').valor
        razonSocial=valor_razonSocial
        
        valor_nombreComercial=Parametros.objects.get(clave='fe_nombreComercial').valor
        nombreComercial=valor_nombreComercial
        
        valor_dirMatriz=Parametros.objects.get(clave='fe_direccion').valor
        dirMatriz=valor_dirMatriz
        
        valor_contribuyenteEspecial=Parametros.objects.get(clave='fe_contribuyenteEspecial').valor
        contribuyenteEspecial=valor_contribuyenteEspecial
        
        valor_moneda=Parametros.objects.get(clave='fe_moneda').valor
        moneda=valor_moneda
        
        dirEstablecimiento=Parametros.objects.get(clave='fe_direccion').valor
        iva=Parametros.objects.get(clave='iva').valor
        
        #FIN DE NOTA DE CREDITO O DEBITO
        
        
        tipoIdentificacionSujetoRetenido=''
        razonSocialSujetoRetenido=''
        identificacionSujetoRetenido=''
        periodoFiscal=''
        direccion=''
        telefono=''
        email=''
        ruc=Parametros.objects.get(clave='fe_ruc').valor
        
    
        if factura:
            razonSocialSujetoRetenido=factura.documento_compra.proveedor.nombre_proveedor
            
            if factura.documento_compra.proveedor.ruc:
                identificacionSujetoRetenido=factura.documento_compra.proveedor.ruc
                tipoIdentificacionSujetoRetenido='04'
            else:
                identificacionSujetoRetenido=factura.documento_compra.proveedor.cedula
                tipoIdentificacionSujetoRetenido='05'
            
            direccion=factura.documento_compra.proveedor.direccion1
            telefono=factura.documento_compra.proveedor.telefono1
            email=factura.documento_compra.proveedor.e_mail1
            periodoFiscal=factura.fecha_emision
            id=factura.id
            
                
                
                
            secuencialTransaccion=''
            tipoDocTransaccion=''
            logn_secuencia=len(str(factura.secuencial))
            if logn_secuencia<9:
                secuencialRet=str(factura.secuencial).zfill(9) 
            else:
                secuencialRet=factura.secuencial
            
            print 'CONEXION'
            r1=razonSocialSujetoRetenido.encode('utf-8')
            r2=razonSocialSujetoRetenido.encode('ascii', 'ignore')
        
            conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
            print 'inicio de conexion'
            #conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=FEDemo")
            cursor = conn.cursor()
            sqlCommanf="INSERT INTO infoCompRetencion (dirMatriz,id,ambiente,tipoEmision,razonSocial,nombreComercial,ruc,codDoc,estab,ptoEmi,secuencial,secuencialTransaccion,tipoDocTransaccion,fechaEmision,dirEstablecimiento,contribuyenteEspecial,obligadoContabilidad,tipoIdentificacionSujetoRetenido,razonSocialSujetoRetenido,identificacionSujetoRetenido,periodoFiscal,direccion,telefono,email) values ('"+str(dirMatriz)+"',"+str(id)+",'"+str(ambiente)+"','"+str(tipoEmision)+"','"+str(razonSocial)+"','"+str(nombreComercial)+"','"+str(ruc)+"','07','"+str(factura.establecimiento)+"','"+str(factura.punto_emision)+"','"+str(secuencialRet)+"','"+str(secuencialTransaccion)+"','"+str(tipoDocTransaccion)+"','"+str(factura.fecha_emision)+"','"+str(dirEstablecimiento)+"','"+str(contribuyenteEspecial)+"','"+str(obligadoContabilidad)+"','"+str(tipoIdentificacionSujetoRetenido)+"','"+str(razonSocialSujetoRetenido.encode('utf8'))+"','"+str(identificacionSujetoRetenido)+"','"+str(periodoFiscal)+"','"+str(direccion.encode('utf8'))+"','"+str(telefono)+"','"+str(email)+"')"
            print sqlCommanf
            cursor.execute(sqlCommanf)
            conn.commit()
            
            #post_id = cursor.lastrowid
            post_id = factura.id
            print post_id
    
            
            secuencia=1
            codigo=''
            codigoRetencion=''
            baseImponible=0
            porcentajeRetener=0
            valorRetenido=0
            codDocSustento=''
            numDocSustento=''
            fechaEmisionDocSustento=''

            
            try:
                factura_detalle = DocumentosRetencionDetalleCompra.objects.filter(documento_retencion_compra_id=id)
            except DocumentosRetencionDetalleCompra.DoesNotExist:
                factura_detalle = None
                
            if  factura_detalle:
                for f in factura_detalle:
                    iva_rf=f.retencion_detalle.tipo_retencion_id
                    if iva_rf== 1:
                        codigo='1'
                    else:
                        codigo='2'
                        
                        
                    
                    #codigoRetencion=f.retencion_detalle.codigo
                    codigoRetencion=f.retencion_detalle.codigo_facturacion_electronica
                    baseImponible=f.base_imponible
                    porcentajeRetener=f.porcentaje_retencion
                    valorRetenido=f.valor_retenido
                    codDocSustento='01'
                    numDocSustento=factura.documento_compra.establecimiento+''+factura.documento_compra.punto_emision+''+factura.documento_compra.secuencial
                    fechaEmisionDocSustento=factura.documento_compra.fecha_emision
                    
                    
                    
                        
                    
                    sqlComman1="INSERT INTO impuestoInfoCompRetencion (id,secuencia,codigo,codigoRetencion,baseImponible,porcentajeRetener,valorRetenido,codDocSustento,numDocSustento,fechaEmisionDocSustento) values ("+str(id)+","+str(secuencia)+",'"+str(codigo)+"','"+str(codigoRetencion)+"',"+str(baseImponible)+","+str(porcentajeRetener)+","+str(valorRetenido)+",'"+str(codDocSustento)+"','"+str(numDocSustento)+"','"+str(fechaEmisionDocSustento)+"')"
                    print sqlComman1
                    cursor.execute(sqlComman1)
                    conn.commit()
                    secuencia=secuencia+1
            
            
            
            

            html='Se ingreso la retencion electronicamente'
            try:
                dc = DocumentoCompra.objects.get(id=fid)
            except DocumentoCompra.DoesNotExist:
                dc = None
            if dc:
                dc.facturacion_eletronica=True
                dc.save()
            
            return HttpResponse(html)
    
        else:
            raise Http404    
        
@login_required()
@transaction.atomic
def consultar_retencion_electronica_actual(request):
    #db = MySQLdb.connect(host="104.192.6.75, user="sa",passwd="U7BKm3eayFCn9cTx", db="FacturaNotaCreditoYDebito")
    with transaction.atomic():
        fid = request.POST['id']
        try:
            factura = DocumentosRetencionCompra.objects.get(documento_compra_id=fid)
        except DocumentosRetencionCompra.DoesNotExist:
            factura = None
        
        ambiente=''
        tipoEmision=''
        razonSocial=''
        nombreComercial=''
        dirMatriz=''
        contribuyenteEspecial=''
        obligadoContabilidad='SI'
        moneda=''
        
        
        valor_ambiente = Parametros.objects.get(clave='fe_ambiente').valor
        ambiente=valor_ambiente
        
        tipoEmision='1'
        valor_razonSocial=Parametros.objects.get(clave='fe_razonSocial').valor
        razonSocial=valor_razonSocial
        
        valor_nombreComercial=Parametros.objects.get(clave='fe_nombreComercial').valor
        nombreComercial=valor_nombreComercial
        
        valor_dirMatriz=Parametros.objects.get(clave='fe_direccion').valor
        dirMatriz=valor_dirMatriz
        
        valor_contribuyenteEspecial=Parametros.objects.get(clave='fe_contribuyenteEspecial').valor
        contribuyenteEspecial=valor_contribuyenteEspecial
        
        valor_moneda=Parametros.objects.get(clave='fe_moneda').valor
        moneda=valor_moneda
        
        dirEstablecimiento=Parametros.objects.get(clave='fe_direccion').valor
        iva=Parametros.objects.get(clave='iva').valor
        
        #FIN DE NOTA DE CREDITO O DEBITO
        
        
        tipoIdentificacionSujetoRetenido=''
        razonSocialSujetoRetenido=''
        identificacionSujetoRetenido=''
        periodoFiscal=''
        direccion=''
        telefono=''
        email=''
        ruc=Parametros.objects.get(clave='fe_ruc').valor
        
    
        if factura:
            razonSocialSujetoRetenido=factura.documento_compra.proveedor.nombre_proveedor
            
            if factura.documento_compra.proveedor.ruc !='':
                identificacionSujetoRetenido=factura.documento_compra.proveedor.ruc
                
            else:
                identificacionSujetoRetenido=factura.documento_compra.proveedor.cedula
                
                
            if len(identificacionSujetoRetenido)>10:
                tipoIdentificacionSujetoRetenido='04'
            else:
                tipoIdentificacionSujetoRetenido='05'
                
            
            direccion=factura.documento_compra.proveedor.direccion1
            telefono=factura.documento_compra.proveedor.telefono1
            email=factura.documento_compra.proveedor.e_mail1
            periodoFiscal=factura.fecha_emision
            id=factura.id
            
                
                
                
            secuencialTransaccion=''
            tipoDocTransaccion=''
            logn_secuencia=len(str(factura.secuencial))
            if logn_secuencia<9:
                secuencialRet=str(factura.secuencial).zfill(9) 
            else:
                secuencialRet=factura.secuencial
            
            print 'CONEXION'
            r1=razonSocialSujetoRetenido.encode('utf-8')
            r2=razonSocialSujetoRetenido.encode('ascii', 'ignore')
            
            if direccion == '' or telefono =='' or email =='':
                html='Revise los datos del proveedor Direccion,telefono o email'
            else:
        
                conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
                print 'inicio de conexion'
                #conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=FEDemo")
                cursor = conn.cursor()
                sqlCommanf="INSERT INTO infoCompRetencion (dirMatriz,id,ambiente,tipoEmision,razonSocial,nombreComercial,ruc,codDoc,estab,ptoEmi,secuencial,secuencialTransaccion,tipoDocTransaccion,fechaEmision,dirEstablecimiento,contribuyenteEspecial,obligadoContabilidad,tipoIdentificacionSujetoRetenido,razonSocialSujetoRetenido,identificacionSujetoRetenido,periodoFiscal,direccion,telefono,email) values ('"+str(dirMatriz)+"',"+str(id)+",'"+str(ambiente)+"','"+str(tipoEmision)+"','"+str(razonSocial)+"','"+str(nombreComercial)+"','"+str(ruc)+"','07','"+str(factura.establecimiento)+"','"+str(factura.punto_emision)+"','"+str(secuencialRet)+"','"+str(secuencialTransaccion)+"','"+str(tipoDocTransaccion)+"','"+str(factura.fecha_emision)+"','"+str(dirEstablecimiento)+"','"+str(contribuyenteEspecial)+"','"+str(obligadoContabilidad)+"','"+str(tipoIdentificacionSujetoRetenido)+"','"+str(razonSocialSujetoRetenido.encode('utf8'))+"','"+str(identificacionSujetoRetenido)+"','"+str(periodoFiscal)+"','"+str(direccion.encode('utf8'))+"','"+str(telefono)+"','"+str(email)+"')"
                print sqlCommanf
                cursor.execute(sqlCommanf)
                conn.commit()
                
                #post_id = cursor.lastrowid
                post_id = factura.id
                print post_id
        
                
                secuencia=1
                codigo=''
                codigoRetencion=''
                baseImponible=0
                porcentajeRetener=0
                valorRetenido=0
                codDocSustento=''
                numDocSustento=''
                fechaEmisionDocSustento=''
    
                
                try:
                    factura_detalle = DocumentosRetencionDetalleCompra.objects.filter(documento_retencion_compra_id=id)
                except DocumentosRetencionDetalleCompra.DoesNotExist:
                    factura_detalle = None
                    
                if  factura_detalle:
                    for f in factura_detalle:
                        iva_rf=f.retencion_detalle.tipo_retencion_id
                        if iva_rf== 1:
                            codigo='1'
                        else:
                            codigo='2'
                            
                            
                        
                        #codigoRetencion=f.retencion_detalle.codigo
                        codigoRetencion=f.retencion_detalle.codigo_facturacion_electronica
                        baseImponible=f.base_imponible
                        porcentajeRetener=f.porcentaje_retencion
                        valorRetenido=f.valor_retenido
                        codDocSustento='01'
                        numDocSustento=factura.documento_compra.establecimiento+''+factura.documento_compra.punto_emision+''+factura.documento_compra.secuencial
                        fechaEmisionDocSustento=factura.documento_compra.fecha_emision
                        
                        
                        
                            
                        
                        sqlComman1="INSERT INTO impuestoInfoCompRetencion (id,secuencia,codigo,codigoRetencion,baseImponible,porcentajeRetener,valorRetenido,codDocSustento,numDocSustento,fechaEmisionDocSustento) values ("+str(id)+","+str(secuencia)+",'"+str(codigo)+"','"+str(codigoRetencion)+"',"+str(baseImponible)+","+str(porcentajeRetener)+","+str(valorRetenido)+",'"+str(codDocSustento)+"','"+str(numDocSustento)+"','"+str(fechaEmisionDocSustento)+"')"
                        print sqlComman1
                        cursor.execute(sqlComman1)
                        conn.commit()
                        secuencia=secuencia+1
                
                
                
                
    
                html='Se ingreso la retencion electronicamente'
                try:
                    dc = DocumentoCompra.objects.get(id=fid)
                except DocumentoCompra.DoesNotExist:
                    dc = None
                if dc:
                    dc.facturacion_eletronica=True
                    dc.ats=True
                    dc.save()
            
            return HttpResponse(html)
    
        else:
            raise Http404
        
        
        
@login_required()
@transaction.atomic
def consultar_datos_facturacion_electronica(request,pk):
    #db = MySQLdb.connect(host="104.192.6.75, user="sa",passwd="U7BKm3eayFCn9cTx", db="FacturaNotaCreditoYDebito")
    with transaction.atomic():
        id = pk
        try:
            factura = DocumentoVenta.objects.get(id=id)
        except DocumentoVenta.DoesNotExist:
            factura = None
        
        if factura:
            if factura.id_facturacion_eletronica:
                conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
                cursor = conn.cursor()
                sqlCommanf="select claveAcceso,estado,numeroAutorizacion,fechaAutorizacion,msjeSRI,estadoCorreo,msjeCorreo,estadoPdf,msjePdf,secuencial  from infoDocumentoCliente where id="+str(factura.id_facturacion_eletronica)+";"
                print sqlCommanf
                cursor.execute(sqlCommanf)
                row = cursor.fetchall()
                conn.commit()
                
                
                return render_to_response('venta/consultar_facturacion_electronica.html', {'row': row}, RequestContext(request))
    
        else:
            raise Http404

@transaction.atomic
def consultar_datos_retencion_electronica(request,pk):
    #db = MySQLdb.connect(host="104.192.6.75, user="sa",passwd="U7BKm3eayFCn9cTx", db="FacturaNotaCreditoYDebito")
    with transaction.atomic():
        id = pk
        try:
            factura_c = DocumentoCompra.objects.get(id=id)
        except DocumentoCompra.DoesNotExist:
            factura_c = None
        
        if factura_c:
            try:
                factura = DocumentosRetencionCompra.objects.get(documento_compra_id=id)
            except DocumentosRetencionCompra.DoesNotExist:
                factura = None
            if factura:
            
                if factura.id:
                    conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
                    cursor = conn.cursor()
                    sqlCommanf="select claveAcceso,estado,numeroAutorizacion,fechaAutorizacion,msjeSRI,estadoCorreo,msjeCorreo,estadoPdf,msjePdf,secuencial  from infoCompRetencion where id="+str(factura.id)+";"
                    cursor.execute(sqlCommanf)
                    row = cursor.fetchall()
                    conn.commit()
                    for p2 in row:
                    
                        mensajeSri=p2[4].decode('utf8','replace')
                        estado=p2[1]
                    
                    
                    return render_to_response('compra/retencion_electronica.html', {'row': row,'mensajeSri':mensajeSri,'id': id,'estado': estado}, RequestContext(request))
    
        else:
            raise Http404   
        
        
@transaction.atomic
def listado_retencion_electronica(request):
    #db = MySQLdb.connect(host="104.192.6.75, user="sa",passwd="U7BKm3eayFCn9cTx", db="FacturaNotaCreditoYDebito")
    with transaction.atomic():
        conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
        cursor = conn.cursor()
        sqlCommanf="select fechaEmision,ambiente,ptoEmi,estab,secuencial,Direccion,Telefono,Email,razonSocialSujetoRetenido,identificacionSujetoRetenido,tipoIdentificacionSujetoRetenido,Estado,claveAcceso,numeroAutorizacion,fechaAutorizacion,msjeSRI,estadoCorreo,msjeCorreo,estadoPdf,msjePdf,secuencial from infoCompRetencion "
        cursor.execute(sqlCommanf)
        row = cursor.fetchall()
        conn.commit()
        return render_to_response('compra/listado_retencion_electronica.html', {'row': row}, RequestContext(request))
    
        
 


