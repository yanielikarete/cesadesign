# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from bancos.forms import *
from contabilidad.models import *
from transacciones.models import DocumentoCompra,DocumentoAbono,DocumentoVenta,DocumentoAbonoVenta,MovimientoNotaCredito,DocumentosVentaDetalle,DocumentoVentaFormaPago
from decimal import *
from django.db import transaction, connection
import simplejson as json
from django.utils import timezone
from proveedores.models import *
from bancos.models import Banco
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import Http404
import datetime
# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import DateFormat
from django.core.serializers.json import DjangoJSONEncoder

import pyodbc
now = datetime.datetime.now()

@login_required()
def banco_list_view(request):
    bancos = Banco.objects.filter(estado=True)
    template = loader.get_template('bancos/index.html')
    context = RequestContext(request, {'bancos': bancos})
    return HttpResponse(template.render(context))


@login_required()
def BancoCreateView(request):
    if request.method == 'POST':
        banco_form = BancoForm(request.POST)

        if banco_form.is_valid():
            new_orden = banco_form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = now
            new_orden.updated_at = now
            new_orden.estado = True
            new_orden.save()

            return HttpResponseRedirect('/bancos/bancos')
        else:
            print 'error'
            print banco_form.errors, len(banco_form.errors)
    else:
        banco_form = BancoForm

    return render_to_response('bancos/create-new.html', {'form': banco_form,}, RequestContext(request))

@login_required()
def BancoUpdateView(request, pk):
    if request.method == 'POST':
        banco = Banco.objects.get(id=pk)
        banco_form = BancoForm(request.POST, request.FILES, instance=banco)
        print banco_form.is_valid(), banco_form.errors, type(banco_form.errors)

        if banco_form.is_valid():
            banco_form.cleaned_data['estado'] = True
            banco = banco_form.save()
            banco.updated_by = request.user.get_full_name()
            banco.updated_at = now
            banco.save()
            return HttpResponseRedirect('/bancos/bancos')
        else:

            banco_form = BancoForm(request.POST)

            context = {
                'section_title': 'Actualizar Asiento',
                'button_text': 'Actualizar',
                'form': banco_form}

        return render_to_response(
            'bancos/update.html',
            context,
            context_instance=RequestContext(request))
    else:
        banco = Banco.objects.get(id=pk)
        banco_form = BancoForm(instance=banco)

        context = {
            'section_title': 'Actualizar Asiento',
            'button_text': 'Actualizar',
            'form': banco_form}

        return render_to_response(
            'bancos/update.html',
            context,
            context_instance=RequestContext(request))

@login_required()
def BancoEliminarByPkView(request, pk):
    obj = Banco.objects.get(id = pk)

    if obj:
        obj.estado = False
        obj.save()

    return HttpResponseRedirect('/bancos/bancos')

@login_required()
def movimiento_list_view(request):
    #movimientos = Movimiento.objects.filter(tipo_anticipo=1).filter(tipo_documento_id=1).exclude(tipo_documento_id=10).order_by('-id')
    movimientos=''
    template = loader.get_template('movimientos/index.html')
    context = RequestContext(request, {'movimientos': movimientos})
    return HttpResponse(template.render(context))


@login_required()
def movimiento_nuevo_view(request):
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    bancos = Banco.objects.filter(estado=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    tipo_anticipos = TipoAnticipo.objects.all().exclude(id = 2)
    tipo_documentos = TipoDocumento.objects.filter(proveedor = True).filter(id = 1)
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    centros = CentroCosto.objects.all()
    form = MovimientoForm
    template = loader.get_template('movimientos/create.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos,'centros_defecto':centros_defecto,
                                       'centros':centros,
                                       'tipo_documentos': tipo_documentos, 'bancos': bancos, 'cuentas': cuentas,
                                       'proveedores': proveedores})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def movimiento_crear_view(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():

                with transaction.atomic():
                    print "ingresa a crear el movimiento un formulario válido"
                    cleaned_data = form.cleaned_data
                    movimiento = Movimiento()
                    movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
                    movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    movimiento.banco_id = int(cleaned_data.get('banco').id)
                    if movimiento.tipo_anticipo_id == 2:
                        movimiento.cliente_id = int(request.POST['persona_id'])
                    else:
                        movimiento.proveedor_id = int(request.POST['persona_id'])
                    movimiento.paguese_a = cleaned_data.get('paguese_a')
                    movimiento.numero_cheque = cleaned_data.get('numero_cheque')
                    movimiento.fecha_cheque = cleaned_data.get('fecha_emision')
                    desp=cleaned_data.get('descripcion')
                    movimiento.descripcion = desp.replace("\n", " ")
                    movimiento.monto = cleaned_data.get('monto')
                    movimiento.monto_cheque = request.POST['monto_cheque']
                    abon=cleaned_data.get('abono_saldo_inicial')
                    print abon
                    if abon == True:
                        movimiento.abono_saldo_inicial = True
                    else:
                        movimiento.abono_saldo_inicial = False
                    movimiento.save()
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.created_at = now
                    movimiento.updated_at = now
                    movimiento.numero_comprobante = 'M'+str(now.year)+'000'+str(movimiento.id)
                    movimiento.save()
                    print "Entro a cheque"
                    print request.POST['monto_cheque']

                    #ACTUALIZACION SECUENCIAL CHEQUE
                    if movimiento.tipo_documento_id == 1:
                        Banco.objects.filter(pk=movimiento.banco_id).update(secuencia=movimiento.numero_cheque + 1)

                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        asiento = Asiento()
                        asiento.codigo_asiento = "B"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE BANCOS - ' + movimiento.numero_comprobante
                        asiento.modulo='Bancos-CHEQUE'
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.created_by = request.user.get_full_name()
                        asiento.updated_by = request.user.get_full_name()
                        asiento.created_at = now
                        asiento.updated_at = now
                        
                        asiento.save()
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            print item_asiento['id_plancuenta']
                            print item_asiento['debe']
                            print item_asiento['haber']
                            print asiento.asiento_id
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.centro_costo_id = item_asiento['centro']

                            asiento_detalle.save()
                    facturas = json.loads(request.POST['arreglo_facturas'])
                    if len(facturas) > 0:
                        for item_factura in facturas:
                            if item_factura['check']:
                                if movimiento.tipo_anticipo_id == 2:
                                    fact = DocumentoVenta.objects.get(id=item_factura['id'])
                                    fact.pagado = True
                                    fact.movimiento_id = movimiento.id
                                    fact.save()
                                    abono = DocumentoAbonoVenta()
                                    abono.documento_venta_id = item_factura['id']
                                    abono.movimiento_id = movimiento.id
                                    abono.abono = item_factura['abono']
                                    abono.cantidad_anterior_abonada = item_factura['anterior']
                                    abono.diferencia = item_factura['diferencia']
                                    abono.created_by = request.user.get_full_name()
                                    abono.updated_by = request.user.get_full_name()
                                    abono.created_at = now
                                    abono.updated_at = now
                                    abono.save()
                                else:

                                    fact = DocumentoCompra.objects.get(id=item_factura['id'])
                                    fact.pagado=True
                                    fact.movimiento_id=movimiento.id
                                    fact.save()
                                    abono=DocumentoAbono()
                                    abono.documento_compra_id=item_factura['id']
                                    abono.movimiento_id = movimiento.id
                                    abono.abono=item_factura['abono']
                                    abono.cantidad_anterior_abonada = item_factura['anterior']
                                    abono.diferencia = item_factura['diferencia']
                                    abono.created_by = request.user.get_full_name()
                                    abono.updated_by = request.user.get_full_name()
                                    abono.created_at = now
                                    abono.updated_at = now
                                    abono.save()

            else:
                form_errors = form.errors
                print form_errors
        except Exception as e:
            print (e.message)
        
        
        item = {
            'id': movimiento.id,
            'documento': movimiento.tipo_documento_id,
        }
        json_resultados = json.dumps(item)
   
        return HttpResponse(json_resultados, content_type="application/json")

        #return HttpResponseRedirect('/bancos/movimiento')


@login_required()
def movimiento_edit_view(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(proveedor = True)
    bancos = Banco.objects.filter(estado=True)
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    facturas=DocumentoCompra.objects.filter(movimiento_id=pk)
    cursor = connection.cursor()
    if movimiento.tipo_anticipo_id==1:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_compra f,documento_abono da where da.movimiento_id = ' + (
    pk) + ' and f.id=da.documento_compra_id;'
    else:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_venta f,documento_abono_venta da where da.movimiento_id = ' + (
            pk) + ' and f.id=da.documento_venta_id;'
    cursor.execute(query)
    facturas = cursor.fetchall()
    total_facturas=DocumentoAbono.objects.filter(movimiento_id=pk).aggregate(Sum('abono'))
    if total_facturas['abono__sum']:
        total_f=total_facturas['abono__sum']
    else:
        total_f=0
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None



    template = loader.get_template('movimientos/update.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos, 'facturas': facturas,'asientos': asientos,'detalle_asientos':detalle_asientos,
                                       'tipo_documentos': tipo_documentos, 'clientes': clientes, 'bancos': bancos, 'cuentas': cuentas,
                                       'proveedores': proveedores,'total_f':total_f})
    return HttpResponse(template.render(context))



@login_required()
def consultar_facturas(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        tipo = request.POST['tipo']

        cursor = connection.cursor()
        if(tipo == 'proveedor'):
            query = 'select dc.id, to_char(dc.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,SUM(da.abono),dc.punto_emision,dc.secuencial,dc.valor_retenido,SUM(m.total) as nc from documento_compra dc LEFT JOIN documento_abono da  ON (da.documento_compra_id = dc.id) AND da.anulado=FALSE LEFT JOIN movimiento_nota_credito m  ON (m.documento_compra_id = dc.id) AND m.anulado is not True where dc.proveedor_id = ' + (id) + ' GROUP BY dc.id, dc.fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,dc.valor_retenido;'
        else:
            query = 'select dv.id, to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento, dv.base_iva, dv.valor_iva, dv.total,SUM(da.abono),dv.punto_emision,dv.secuencial,SUM(n.total) from documento_venta dv LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = dv.id) LEFT JOIN movimiento_nota_credito n  ON (n.documento_venta_id = dv.id and n.anulado is not True) where dv.cliente_id = ' + (id) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento, dv.base_iva, dv.valor_iva, dv.total;'
            print(query)
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")

@login_required()
def movimiento_update_view(request, pk):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():


            cleaned_data = form.cleaned_data
            movimiento = Movimiento.objects.get(pk=pk)
            movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
            movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
            movimiento.fecha_emision = cleaned_data.get('fecha_emision')
            movimiento.banco_id = int(cleaned_data.get('banco').id)
            if movimiento.tipo_anticipo_id == 2:
                movimiento.cliente_id = int(request.POST['persona_id'])
            else:
                movimiento.proveedor_id = int(request.POST['persona_id'])
            movimiento.paguese_a = cleaned_data.get('paguese_a')
            movimiento.numero_cheque = cleaned_data.get('numero_cheque')
            movimiento.fecha_cheque = cleaned_data.get('fecha_cheque')
            desp=cleaned_data.get('descripcion')
            movimiento.descripcion = desp.rstrip('\n')
            movimiento.monto = cleaned_data.get('monto')
            movimiento.numero_comprobante = cleaned_data.get('numero_comprobante')
            movimiento.updated_by = request.user.get_full_name()
            movimiento.updated_at = now
            movimiento.save()
            try:
                asiento = Asiento.objects.get(asiento_id=movimiento.asiento_id)
            except Asiento.DoesNotExist:
                asiento = None
            if asiento:
                asiento.fecha= movimiento.fecha_emision
                asiento.updated_by = request.user.get_full_name()
                asiento.updated_at = now
                asiento.save()
        return HttpResponseRedirect('/bancos/movimiento')


@login_required()
def consultar_secuencia_cheque(request):
    if request.method == "POST":
        banco_id = request.POST['id']
        cursor = connection.cursor()
        query = 'select id, secuencia, nombre from banco where id = ' + banco_id + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def movimiento_otros_nuevo_view(request):
    tipo_movimientos = Catalogo.objects.filter(data=5)
    tipo_anticipo_documentos = Catalogo.objects.filter(data=4)
    form = MovimientoForm
    template = loader.get_template('movimientos/otros_create.html')
    context = RequestContext(request, {'form': form, 'tipo_movimientos': tipo_movimientos,
                                       'tipo_anticipo_documentos': tipo_anticipo_documentos})
    return HttpResponse(template.render(context))


@login_required()
def cheques_prestados_list_view(request):
    cheques_prestados = ChequesProtestados.objects.all()
    template = loader.get_template('chequesprotestados/index.html')
    context = RequestContext(request, {'cheques_prestados': cheques_prestados})
    return HttpResponse(template.render(context))


@login_required()
def cheques_prestados_nuevo_view(request):
    clientes = Cliente.objects.all()
    bancos = Banco.objects.filter(estado=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    form = MovimientoForm
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    centros= CentroCosto.objects.all()
    template = loader.get_template('chequesprotestados/create.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'bancos': bancos,'centros_defecto':centros_defecto,'centros':centros,
                                       'cuentas': cuentas})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def cheques_prestados_crear_view(request):
    if request.method == 'POST':
        form = ChequePrestadoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    cleaned_data = form.cleaned_data
                    cheque_protestado = ChequesProtestados()
                    cheque_protestado.fecha_emision = cleaned_data.get('fecha_emision')
                    cheque_protestado.banco_id = int(cleaned_data.get('banco').id)
                    cheque_protestado.cliente_id = int(cleaned_data.get('cliente').id_cliente)
                    cheque_protestado.numero_cheque = cleaned_data.get('numero_cheque')
                    if request.POST['movimiento_id']:
                        cheque_protestado.movimiento_id = request.POST['movimiento_id']
                    cheque_protestado.fecha_cheque = cleaned_data.get('fecha_cheque')
                    cheque_protestado.valor_cheque = cleaned_data.get('valor_cheque')
                    cheque_protestado.valor_multa = cleaned_data.get('valor_multa')
                    cheque_protestado.comprobante_debito = cleaned_data.get('comprobante_debito')
                    cheque_protestado.descripcion = cleaned_data.get('descripcion')
                    cheque_protestado.save()
                    
                    movimiento_valor = Movimiento()
                    movimiento_valor.tipo_anticipo_id = cheque_protestado.movimiento.tipo_anticipo_id
                    movimiento_valor.tipo_documento_id = 2
                    movimiento_valor.fecha_emision = cleaned_data.get('fecha_emision')
                    movimiento_valor.banco_id = int(cleaned_data.get('banco').id)
                    movimiento_valor.cliente_id = cheque_protestado.movimiento.cliente_id
                    movimiento_valor.paguese_a = cheque_protestado.movimiento.paguese_a
                    movimiento_valor.numero_cheque = cleaned_data.get('numero_cheque')
                    movimiento_valor.descripcion = "NOTA DE DEBITO DE CHEQUE PROTESTADO NO."+str(cheque_protestado.numero_cheque)+"/"+cheque_protestado.descripcion
                    movimiento_valor.monto = cleaned_data.get('valor_cheque')
                    movimiento_valor.asociado_cheques_protestados=True
                    movimiento_valor.created_by = request.user.get_full_name()
                    movimiento_valor.created_at = now
                    movimiento_valor.updated_by = request.user.get_full_name()
                    movimiento_valor.updated_at = now
                    
                    movimiento_valor.save()
                    movimiento_valor.numero_comprobante = 'ND'+str(now.year)+'000'+str(movimiento_valor.id)
                    movimiento_valor.save()
                    
                    
                    movimiento_multa = Movimiento()
                    movimiento_multa.tipo_anticipo_id = cheque_protestado.movimiento.tipo_anticipo_id
                    movimiento_multa.tipo_documento_id = 2
                    movimiento_multa.fecha_emision = cleaned_data.get('fecha_emision')
                    movimiento_multa.banco_id = int(cleaned_data.get('banco').id)
                    movimiento_multa.cliente_id = cheque_protestado.movimiento.cliente_id
                    movimiento_multa.paguese_a = cheque_protestado.movimiento.paguese_a
                    movimiento_multa.numero_cheque = cleaned_data.get('numero_cheque')
                    movimiento_multa.descripcion = "NOTA DE DEBITO DE MULTA CHEQUE PROTESTADO NO."+str(cheque_protestado.numero_cheque)+"/"+cheque_protestado.descripcion
                    movimiento_multa.monto = cheque_protestado.valor_multa
                    movimiento_multa.asociado_cheques_protestados=True
                    movimiento_multa.save()
                    movimiento_multa.numero_comprobante = 'ND'+str(now.year)+'000'+str(movimiento_multa.id)
                    movimiento_multa.created_by = request.user.get_full_name()
                    movimiento_multa.created_at = now
                    movimiento_multa.updated_by = request.user.get_full_name()
                    movimiento_multa.updated_at = now
                    movimiento_multa.save()
                    
                    cheque_protestado.movimiento_valor_cheque_id=movimiento_valor.id
                    cheque_protestado.movimiento_multa_id=movimiento_multa.id
                    cheque_protestado.save()

                    asientos = json.loads(request.POST['arreglo_asientos'])
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        asiento = Asiento()
                        asiento.codigo_asiento = "CHPROT"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.modulo = "Bancos-CHEQUES PROTESTADOS"
                        
                        try:
                            movimiento = Movimiento.objects.get(id=cheque_protestado.movimiento_id)
                        except Movimiento.DoesNotExist:
                            movimiento = None
                        if movimiento:
                            print 'entro1'
                            asiento.glosa = 'CHEQUE PROTESTADO '+str(movimiento.descripcion)
                        else:
                            print 'entro2'
                            asiento.glosa = 'CHEQUE PROTESTADO '
                            
                        asiento.gasto_no_deducible = False
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.created_by = request.user.get_full_name()
                        asiento.created_at = now
                        asiento.updated_by = request.user.get_full_name()
                        asiento.updated_at = now
                        asiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        for item_asiento in asientos:
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.centro_costo_id = item_asiento['centro']
                            asiento_detalle.save()
                        cheque_protestado.asiento_id=asiento.asiento_id
                        cheque_protestado.save()

            except Exception as e:
                print (e.message)
        else:
            form_errors = form.errors
        return HttpResponseRedirect('/bancos/cheques_protestados')


@login_required()
def cheques_prestados_edit_view(request, pk):
    cheque_prestado = ChequesProtestados.objects.get(pk=pk)
    clientes = Cliente.objects.all()
    bancos = Banco.objects.filter(estado=True)
    asiento_detalle = AsientoDetalle.objects.filter(asiento_id=cheque_prestado.asiento_id)
    asientos = Asiento.objects.get(asiento_id=cheque_prestado.asiento_id)
    template = loader.get_template('chequesprotestados/edit.html')
    context = RequestContext(request, {'cheque_prestado': cheque_prestado, 'clientes': clientes, 'bancos': bancos,'asientos': asientos, 'detalle_asientos': asiento_detalle})
    return HttpResponse(template.render(context))


@login_required()
def cheques_prestados_update_view(request, pk):
    if request.method == 'POST':
        form = ChequePrestadoForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cheque_protestado = ChequesProtestados.objects.get(pk=pk)
            cheque_protestado.fecha_emision = cleaned_data.get('fecha_emision')
            cheque_protestado.banco_id = int(cleaned_data.get('banco').id)
            cheque_protestado.cliente_id = int(cleaned_data.get('cliente').id_cliente)
            cheque_protestado.numero_cheque = cleaned_data.get('numero_cheque')
            cheque_protestado.fecha_cheque = cleaned_data.get('fecha_cheque')
            cheque_protestado.valor_cheque = cleaned_data.get('valor_cheque')
            cheque_protestado.valor_multa = cleaned_data.get('valor_multa')
            cheque_protestado.comprobante_debito = cleaned_data.get('comprobante_debito')
            cheque_protestado.descripcion = cleaned_data.get('descripcion')
            cheque_protestado.save()
            
            try:
                movimiento_valor = Movimiento.objects.get(id=cheque_protestado.movimiento_valor_cheque_id)
            except Movimiento.DoesNotExist:
                movimiento_valor = None
            if movimiento_valor:
                movimiento_valor.descripcion="NOTA DE DEBITO DE CHEQUE PROTESTADO NO."+str(cheque_protestado.numero_cheque)+"/"+cheque_protestado.descripcion
                movimiento_valor.monto = cleaned_data.get('valor_cheque')
                movimiento_valor.numero_cheque = cleaned_data.get('numero_cheque')
                movimiento_valor.save()
            else:
                movimiento_valor = Movimiento()
                movimiento_valor.tipo_anticipo_id = cheque_protestado.movimiento.tipo_anticipo_id
                movimiento_valor.tipo_documento_id = 2
                movimiento_valor.fecha_emision = cleaned_data.get('fecha_emision')
                movimiento_valor.banco_id = int(cleaned_data.get('banco').id)
                movimiento_valor.cliente_id = cheque_protestado.movimiento.cliente_id
                movimiento_valor.paguese_a = cheque_protestado.movimiento.paguese_a
                movimiento_valor.numero_cheque = cleaned_data.get('numero_cheque')
                movimiento_valor.descripcion = "NOTA DE DEBITO DE CHEQUE PROTESTADO NO."+str(cheque_protestado.numero_cheque)+"/"+cheque_protestado.descripcion
                movimiento_valor.monto = cleaned_data.get('valor_cheque')
                movimiento_valor.asociado_cheques_protestados=True
                movimiento_valor.save()
                movimiento_valor.numero_comprobante = 'ND'+str(now.year)+'000'+str(movimiento_valor.id)
                movimiento_valor.created_by = request.user.get_full_name()
                movimiento_valor.created_at = now
                movimiento_valor.updated_by = request.user.get_full_name()
                movimiento_valor.updated_at = now
                movimiento_valor.save()
            
            try:
                movimiento_multa = Movimiento.objects.get(id=cheque_protestado.movimiento_multa_id)
            except Movimiento.DoesNotExist:
                movimiento_multa = None
            if movimiento_multa:
                movimiento_multa.numero_cheque = cleaned_data.get('numero_cheque')
                movimiento_multa.descripcion = "NOTA DE DEBITO DE MULTA CHEQUE PROTESTADO NO."+str(cheque_protestado.numero_cheque)+"/"+cheque_protestado.descripcion
                movimiento_multa.monto = cheque_protestado.valor_multa
                movimiento_multa.save()
            else:
                movimiento_multa = Movimiento()
                movimiento_multa.tipo_anticipo_id = cheque_protestado.movimiento.tipo_anticipo_id
                movimiento_multa.tipo_documento_id = 2
                movimiento_multa.fecha_emision = cleaned_data.get('fecha_emision')
                movimiento_multa.banco_id = int(cleaned_data.get('banco').id)
                movimiento_multa.cliente_id = cheque_protestado.movimiento.cliente_id
                movimiento_multa.paguese_a = cheque_protestado.movimiento.paguese_a
                movimiento_multa.numero_cheque = cleaned_data.get('numero_cheque')
                movimiento_multa.descripcion = "NOTA DE DEBITO DE MULTA CHEQUE PROTESTADO NO."+str(cheque_protestado.numero_cheque)+"/"+cheque_protestado.descripcion
                movimiento_multa.monto = cheque_protestado.valor_multa
                movimiento_multa.asociado_cheques_protestados=True
                movimiento_multa.save()
                movimiento_multa.numero_comprobante = 'ND'+str(now.year)+'000'+str(movimiento_multa.id)
                movimiento_multa.created_by = request.user.get_full_name()
                movimiento_multa.created_at = now
                movimiento_multa.updated_by = request.user.get_full_name()
                movimiento_multa.updated_at = now
                movimiento_multa.save()
            cheque_protestado.movimiento_valor_cheque_id=movimiento_valor.id
            cheque_protestado.movimiento_multa_id=movimiento_multa.id
            cheque_protestado.save()

                
                
        return HttpResponseRedirect('/bancos/cheques_protestados')


@login_required()
def consultar_cheques_clientes(request):
    if request.method == "POST" and request.is_ajax:
        cliente_id = request.POST['id']
        cursor = connection.cursor()
        query = 'SELECT m.id, to_char(m.fecha_emision, \'YYYY-MM-DD\') as fecha_emision , b.nombre, m.numero_cheque,m.descripcion,m.monto' \
                ' FROM movimiento as m' \
                ' INNER JOIN banco as b' \
                ' ON m.banco_id = b.id' \
                ' WHERE m.tipo_anticipo_id = 2 and m.tipo_documento_id = 4  and m.activo is True and m.cliente_id = ' + (cliente_id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def conciliaciones_list_view(request):
    conciliaciones = Conciliacion.objects.order_by('fecha_corte')
    template = loader.get_template('conciliaciones/index.html')
    context = RequestContext(request, {'conciliaciones': conciliaciones})
    return HttpResponse(template.render(context))


@login_required()
def conciliaciones_nuevo_view(request):
    cuentas_bancos = Banco.objects.filter(estado=True)
    template = loader.get_template('conciliaciones/create.html')
    context = RequestContext(request, {'cuentas_bancos': cuentas_bancos})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()

def conciliaciones_crear_view(request):
    if request.method == 'POST':
        
        form = ConciliacionForm(request.POST)
        try:
            if form.is_valid():
                with transaction.atomic():
                    cleaned_data = form.cleaned_data
                    conciliacion = Conciliacion()
                    conciliacion.fecha_corte = cleaned_data.get('fecha_corte')
                    conciliacion.cuenta_banco_id = cleaned_data.get('cuenta_banco').id
                    conciliacion.descripcion = cleaned_data.get('descripcion')
                    conciliacion.saldo_estado_cuenta = cleaned_data.get('saldo_estado_cuenta')
                    conciliacion.estado = cleaned_data.get('estado')
                    estado=cleaned_data.get('estado')
                    print estado
                    if estado=='1' or estado==True:
                        conciliacion.descripcion_estado = "CONCLUIDA"
                    else:
                        conciliacion.descripcion_estado = "PENDIENTE"
                    #conciliacion.total = cleaned_data.get('total')
                    conciliacion.save()
                    facturas = json.loads(request.POST['arreglo_facturas'])
                    if len(facturas) > 0:
                        for item_factura in facturas:
                            if item_factura['check']:
                                id=item_factura['id']
                                try:
                                    movimiento = Movimiento.objects.get(id=id)
                                except Movimiento.DoesNotExist:
                                    movimiento = None
                                if movimiento:
                                    movimiento.conciliacion=conciliacion
                                    movimiento.save()
                                    
            else:
                form_errors = form.errors
                print form_errors
        except Exception as e:
            print (e.message)
                
                            


        return HttpResponseRedirect('/bancos/conciliaciones')


@login_required()
def conciliaciones_edit_view(request, pk):
    conciliacion = Conciliacion.objects.get(pk=pk)
    detalle = Movimiento.objects.filter(conciliacion_id=pk)
    cuentas_bancos = Banco.objects.filter(estado=True)
    id = conciliacion.cuenta_banco_id
    fecha = conciliacion.fecha_corte
    cursor = connection.cursor()
    
    #query = "select m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,m.conciliacion_id from movimiento m, tipo_documento td where td.id=m.tipo_documento_id and m.activo is True and m.banco_id= " + str(id) + " and m.fecha_emision<='"+str(fecha)+"' and (m.conciliacion_id=" + str(pk) + " or m.conciliacion_id is NULL)   order by m.fecha_emision";
    try:
        bancos = Banco.objects.get(id=id)
        cuenta_id=bancos.cuenta_contable_id
            
    except Banco.DoesNotExist:
        bancos = None
        cuenta_id=0
        
    query = "select m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,m.conciliacion_id,da.asiento_id,sum(da.debe),sum(da.haber),m.asociado_cheques_protestados from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON (co.id=m.conciliacion_id)  LEFT JOIN contabilidad_asientodetalle da  ON (da.asiento_id = m.asiento_id)  and da.cuenta_id="+str(cuenta_id)+" where   m.activo is True and m.tipo_documento_id!=5 and m.tipo_documento_id!=7 and m.tipo_documento_id!=8  and m.tipo_documento_id!=10 and m.tipo_documento_id!=11 and m.banco_id= "+str(id)+" and m.fecha_emision<='"+str(fecha)+"' and (co.fecha_corte>'"+str(fecha)+"' or  co.fecha_corte is null or co.id="+str(pk)+") group by m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,m.fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id order by m.fecha_emision" 
 
 
    print query
    cursor.execute(query)
    ro = cursor.fetchall()
    conciliacion_id=pk
    
    template = loader.get_template('conciliaciones/edit.html')
    context = RequestContext(request, {'conciliacion': conciliacion, 'cuentas_bancos': cuentas_bancos,'detalle': detalle,'detalle_conciliaciones':ro,'conciliacion_id':conciliacion_id})
    return HttpResponse(template.render(context))


@login_required()
def conciliaciones_update_view(request, pk):
    if request.method == 'POST':
        form = ConciliacionForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            conciliacion = Conciliacion.objects.get(pk=pk)
            conciliacion.fecha_corte = cleaned_data.get('fecha_corte')
            conciliacion.cuenta_banco_id = cleaned_data.get('cuenta_banco').id
            conciliacion.descripcion = cleaned_data.get('descripcion')
            conciliacion.saldo_estado_cuenta = cleaned_data.get('saldo_estado_cuenta')
            
            estado=request.POST['estado']
            print estado
            if estado=='1' or estado==True:
                conciliacion.descripcion_estado = "CONCLUIDA"
                conciliacion.estado = True
                print "entro1"
            else:
                conciliacion.descripcion_estado = "PENDIENTE"
                conciliacion.estado = False
                print "entro0"
                    
            conciliacion.save()
            detalle = Movimiento.objects.filter(conciliacion_id=pk)
            if detalle:
                for d in detalle:
                    d.conciliacion=None
                    d.save()
                            
                    
            facturas = json.loads(request.POST['arreglo_facturas'])
            
            if len(facturas) > 0:
                for item_factura in facturas:
                    if item_factura['check']:
                        id=item_factura['id']
                        try:
                            movimiento = Movimiento.objects.get(id=id)
                        except Movimiento.DoesNotExist:
                            movimiento = None
                        if movimiento:
                            movimiento.conciliacion=conciliacion
                            movimiento.save()
                            
                            
                        
                    
        return HttpResponseRedirect('/bancos/conciliaciones')


@login_required()
def estado_cuenta_list_view(request):
    bancos = Banco.objects.filter(estado=True)
    template = loader.get_template('estadocuenta/index.html')
    context = RequestContext(request, {'bancos': bancos})
    return HttpResponse(template.render(context))



@login_required()
def consultar_plan_cuentas_personas_bancos(request):
    if request.method == "POST" :
        banco = request.POST['banco']
        tipo = request.POST['tipo']
        persona = request.POST['persona']
        cursor = connection.cursor()
        print "tipo"
        print tipo
        if(tipo == '1'):
            query = 'select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp, proveedor p where p.proveedor_id = ' + (
                persona) + ' and cp.plan_id=p.cuenta_contable_compra_id;'

        else:
            if (tipo == '2'):
                query = 'select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp, cliente p where p.id_cliente = ' + (
                persona) + ' and cp.plan_id=p.cuenta_cobrar_id;'
                print(query)

            else:
                if (tipo == '3'):
                    query = 'select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp, cliente p where p.id_cliente = ' + (
                        persona) + ' and cp.plan_id=p.cuenta_contable_venta_id;'
                    print(query)

                else:
                    query = 'select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp, banco p where p.id = ' + (
                    banco) + ' and cp.plan_id=p.cuenta_contable_id;'



        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


def imprimir_cheque(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    movimiento = Movimiento.objects.get(id=pk)
    paguese=movimiento.paguese_a
    beneficiario=paguese[0:50]
    html = loader.get_template('movimientos/imprimir.html')
    context = RequestContext(request, {'movimiento': movimiento,'beneficiario': beneficiario})
    return HttpResponse(html.render(context))

@login_required()
def movimientoEliminarByPkView(request, pk):
    obj = Movimiento.objects.get(id=pk)

    if obj:
        obj.activo = False
        obj.save()
        try:
            abonos = DocumentoAbono.objects.filter(movimiento_id=obj.id)
        except DocumentoAbono.DoesNotExist:
            abonos = None
        if abonos:
            for a in abonos:
                a.anulado= True
                a.save()
        try:
            asiento = Asiento.objects.filter(asiento_id=obj.asiento_id)
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            for a in asiento:
                a.anulado= True
                a.save()
        try:
            nota_credito = MovimientoNotaCredito.objects.filter(movimiento_id=obj.id)
        except MovimientoNotaCredito.DoesNotExist:
            nota_credito = None
            
        print obj.id
        if nota_credito:
            for nc in nota_credito:
                nc.anulado= True
                nc.save()
                print "id:"
                print nc.id
        
                try:
                    dc = DocumentoCompra.objects.filter(id=nc.documento_compra_id)
                except DocumentoCompra.DoesNotExist:
                    dc = None
                if dc:
                    for d in dc:
                        d.nota_credito= False
                        d.save()
                            

    return HttpResponseRedirect('/bancos/movimiento')

@login_required()
def imprimir_comprobante_egreso(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    movimiento = Movimiento.objects.get(id=pk)
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle= AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle = None


    #html = render_to_string('movimientos/imprimir_orden_egreso.html', {'pagesize':'A4','movimiento':movimiento,'detalle':detalle,'asiento':asientos}, context_instance=RequestContext(request))
    #return generar_pdf(html)
    html = loader.get_template('movimientos/imprimir_orden_egreso.html')
    context = RequestContext(request, {'movimiento':movimiento,'detalle':detalle,'asiento':asientos})
    return HttpResponse(html.render(context))

def generar_pdf(html):
    # Funci?n para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


#reportes
@login_required()
def estadoCuentaProveedorView(request):
    cursor = connection.cursor();
    cursor.execute("SELECT proveedor_id,codigo_proveedor,nombre_proveedor from proveedor order by CAST(codigo_proveedor AS Numeric(10,0))" );
    row = cursor.fetchall();

    proveedores = Proveedor.objects.filter(activo=True).order_by('codigo_proveedor')
    return render_to_response('reportes/estado_cuenta_proveedor_actual.html',RequestContext(request, {'proveedores': row}))

# @login_required()
# def consultaCuentaProveedorView(request):
#     if request.method == 'POST':
#         fechainicial = request.POST.get('fechainicial')
#         fechafin = request.POST.get('fechafin')
#         proveedor = request.POST.get('proveedor')
#         total_debito=0
#         total_facturas=0
#         proveedor_s=Proveedor.objects.get(proveedor_id=proveedor)
#         if proveedor_s:
#             nombre_proveedor=proveedor_s.nombre_proveedor
#             saldo_inicial=proveedor_s.saldo_factura
#             total_debito=float(saldo_inicial)
#         else:
#             nombre_proveedor=''
#             saldo_inicial=0
#         qle="SELECT  distinct dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0,dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_proveedor,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,c.codigo_proveedor,c.ruc,drv.id,dv.anulado,dv.proveedor_id FROM documento_compra dv LEFT JOIN proveedor c ON c.proveedor_id=dv.proveedor_id LEFT JOIN documento_retencion_compra drv ON drv.documento_compra_id=dv.id  where dv.anulado is not True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' and dv.proveedor_id="+proveedor
#         print qle
# 
#         cursor = connection.cursor();
#         cursor.execute("SELECT  distinct dv.id,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0,dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_proveedor,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,c.codigo_proveedor,c.ruc,drv.id,dv.anulado,dv.id FROM documento_compra dv LEFT JOIN proveedor c ON c.proveedor_id=dv.proveedor_id LEFT JOIN documento_retencion_compra drv ON drv.documento_compra_id=dv.id  where dv.anulado is not True and dv.no_afecta is not True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' and dv.proveedor_id="+proveedor);
#         row = cursor.fetchall();
#         total = 0
#         subtotal = 0
#         iva = 0
#         
#         total_credito=0
#         total_saldo=0
#         
#         # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
#         html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info">'
#         html+='<thead>'
#         html+='<tr><td colspan="7" style="text-align:center"><b>REPORTE DE ESTADO DE CUENTA DEL PROVEEDOR '+str(nombre_proveedor.encode('utf8'))+'</b></td></tr>'
#         html+='<tr><td colspan="2"><b>DESDE</b></td><td colspan="2">'+str(fechainicial)+'</td><td colspan="2"><b>HASTA</b></td><td colspan="1">'+str(fechafin)+'</td></tr>'
#         html+='<tr><th>TIPO</th>'
#         #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
#         html+='<th>Numero</th>'
#         html+= '<th>Fecha</th>'
#         html+='<th>Debito</th><th>Credito</th><th>Saldo</th><th>Concepto</th></tr></thead>'
#         html+='<tbody><tr>'
#         html+='<tr><td><b>SALDO INICIAL</b></td><td style="text-align:center"></td>'
#         html+='<td style="text-align:center"><b></b></td>'
#         html+='<td style="text-align:right"><b>'+str("%2.2f" % saldo_inicial).replace('.', ',')+'</b></td><td style="text-align:right">0,00</td>'
#         html+='<td style="text-align:right"><b>'+str("%2.2f" % saldo_inicial).replace('.', ',')+'</b></td><td></td></tr>'
#         html+='<tr>'
#         cursor = connection.cursor()
#         #sql_i="select m.id,m.monto_cheque,da.abono,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion from movimiento m LEFT JOIN documento_abono da ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and m.abono_saldo_inicial is True and m.proveedor_id="+str(proveedor)+" group by m.id, m.monto_cheque,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion order by m.fecha_emision"
#         sql_i="select m.id,da.abono,da.abono,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion from documento_abono da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.saldo_inicial is True and da.proveedor_id="+str(proveedor)+" order by m.fecha_emision"
#         print sql_i
#         cursor.execute(sql_i);
#         row_i= cursor.fetchall()
#         sub_saldo=0
#         saldo_total_movi=0
#         saldo_final_inicial=0
#         for pi in row_i:
#             html += '<tr>'
#             html += '<td>'+str(pi[12].encode('utf8'))+'</td>'
#             html += '<td>'+str(pi[8])+'</td>'
#             html += '<td>'+str(pi[3])+'</td>'
#             html += '<td style="text-align:right">0,00</td>'
#             if pi[1]:
#                 saldo_i_monto=float(pi[1])
#             else:
#                 saldo_i_monto=0
#             
#             saldo_mov_inicial=float(saldo_i_monto)
#             saldo_total_movi=saldo_total_movi+saldo_mov_inicial
#             #credito
#             
#             html += '<td style="text-align:right">'+str("%2.2f" % saldo_mov_inicial).replace('.', ',')+'</td>'
#             saldo_final_inicial=float(saldo_inicial)-float(saldo_total_movi)
#             html += '<td style="text-align:right">'+str("%2.2f" % saldo_final_inicial).replace('.', ',')+'</td>'
#             html += '<td >'+str(pi[7].encode('utf8'))+'</td>'
#             html += '</tr>'
#         total_facturas=total_facturas+saldo_final_inicial
#         total_credito=total_credito+saldo_total_movi
#             
# 
#                     
#         
#         
#         
#         for p in row:
#             html += '<td><b>FACTURA</b></td>'
#                 
#            
#          
#             factura=''
#             if p[2]:
#                 factura+=''+str(p[2]) +'-'
#             else:
#                 factura+='-'
#             
#             if p[3]:
#                 factura+=''+str(p[3]) +'-'
#             else:
#                 factura+='-'
#             
#             if p[4]:
#                 factura+=''+str(p[4]) 
#             else:
#                 factura+=''
#             html += '<td style="text-align:center"><b>' + str(factura) + '</b></td>'
# 
#             if p[1]:
#                 html += '<td style="text-align:center"><b>' + str(p[1]) +'</b></td>'
#             else:
#                 html += '<td></td>'
#             
#            
#             
#             if p[14]:
#                 #html += '<td style="text-align:center">' + str(p[14]) + '</td>'
#                 totalf=p[14]
#             else:
#                 #html += '<td></td>'
#                 totalf=0
#             
#             total_debito=total_debito+totalf
#             html += '<td style="text-align:right"><b>' + str("%2.2f" % totalf).replace('.', ',') + '</b></td>'
#             html += '<td style="text-align:right">0,00</td>'
#             html += '<td style="text-align:right"><b>' + str("%2.2f" % totalf).replace('.', ',')  + '</b></td>'
#             html += '<td><b>'+str(p[6].encode('utf8'))+'</b></td>'
#              
#             html += '</tr>'
#             #RETENCIONES SUMA
#               
#             if p[0]:
#                 
#                 saldo=0
#                 cursor = connection.cursor()
#                 sqlr3="select sum(drdv.valor_retenido),drv.id,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id from documento_retencion_compra drv,documento_retencion_detalle_compra drdv where drv.id=drdv.documento_retencion_compra_id and drv.documento_compra_id="+ str(p[0])+" group by drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id"
#                 print sqlr3
#                 cursor.execute(sqlr3);
#                 rowr3 = cursor.fetchall()
#                 retencion=0
#                 retencion1=0
#                 for pr2 in rowr3:
#                     
#                     retencion_cod=''
#                     if pr2[2]:
#                         retencion_cod+=''+str(pr2[2]) +'-'
#                     else:
#                         retencion_cod+='-'
#                     
#                     if pr2[3]:
#                         retencion_cod+=''+str(pr2[3]) +'-'
#                     else:
#                         retencion_cod+='-'
#                     
#                     if pr2[4]:
#                         retencion_cod+=''+str(pr2[4]) 
#                     else:
#                         retencion_cod+=''
#                     
#                     html += '<tr>'
#                     html += '<td>RETENCIONES</td>'
#                     
#                     html+='<td style="text-align:center">'+str(retencion_cod)+'</td>'
#                     html+='<td style="text-align:center">'+str(pr2[5])+'</td>'
#                     html+='<td style="text-align:right" >0,00</td>'
#                     
#                     
#                     if pr2[0]:
#                         saldo=Decimal(saldo)+Decimal(pr2[0])
#                         ret1=pr2[0]
#                     else:
#                         ret1=0
#                         
#                     
#                     total_a=float(totalf)-float(saldo)
#                     total_credito=total_credito+float(ret1)
#                     html+='<td style="text-align:right">'+str("%2.2f" % ret1).replace('.', ',') +'</td>'
#                     html+='<td style="text-align:right">'+str("%2.2f" % total_a).replace('.', ',')+'</td>'
#                     html+='<td style="text-align:center">'+str(pr2[6].encode('utf8'))+'</td>'
# 
#                     html += '</tr>'
#                 #ABONO DE MOVIMIENTOS
#                 cursor = connection.cursor();
#                 sql3="select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion from documento_abono da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.documento_compra_id="+ str(p[0])+" order by m.fecha_emision"
#                 print sql3
#                 cursor.execute(sql3);
#                 row3 = cursor.fetchall()
#                 
#                 for p3 in row3:
#                     html += '<tr>'
#                     html += '<td>'+str(p3[13].encode('utf8'))+'</td>'
#                     
#                     #html += '<td></td>'
#                     #html += '<td>'+str(p3[13])+'</td>'
#                     html += '<td>'+str(p3[9])+'</td>'
#                     html += '<td>'+str(p3[4])+'</td>'
#                     #html += '<td></td>'
#                     html += '<td style="text-align:right">0,00</td>'
#                     #credito
#                     html += '<td style="text-align:right">'+str("%2.2f" % p3[0]).replace('.', ',')+'</td>'
#                     total_a=0
#                     
#                     if p[11]==True:
#                         html += '<td></td>'
#                         estadof='ANULADO'
#                         
#                     else:                        
#                         saldo=saldo+p3[0]
#                         total_a=float(totalf)-float(saldo)
#                         html += '<td style="text-align:right">'+str("%2.2f" % total_a).replace('.', ',')+'</td>'
#                         estadof='ACTIVO'
#                         total_credito=total_credito+float(p3[0])
#                     
#                         
#                         
#                     
#                     html += '<td>'+str(p3[8].encode('utf8'))+'</td>'
#                     
#                     html += '</tr>'
#                     
#                     print 'hrl'
#                 
#                 
#                 #NOTAS DE CREDITO
#                 cursor = connection.cursor();
#                 sql4="select da.total,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion from movimiento_nota_credito da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.documento_compra_id="+ str(p[0])+" order by m.fecha_emision"
#                 print sql4
#                 cursor.execute(sql4);
#                 row4 = cursor.fetchall()
#                 
#                 for p4 in row4:
#                     html += '<tr>'
#                     html += '<td>'+str(p4[13].encode('utf8'))+'</td>'
#                     
#                     #html += '<td></td>'
#                     #html += '<td>'+str(p3[13])+'</td>'
#                     html += '<td>'+str(p4[9])+'</td>'
#                     html += '<td>'+str(p4[4])+'</td>'
#                     #html += '<td></td>'
#                     html += '<td style="text-align:right">0,00</td>'
#                     #credito
#                     html += '<td style="text-align:right">'+str("%2.2f" % p4[0]).replace('.', ',')+'</td>'
#                     total_a=0
#                     
#                     if p[11]==True:
#                         html += '<td></td>'
#                         estadof='ANULADO'
#                         
#                     else:                        
#                         saldo=saldo+p4[0]
#                         total_a=float(totalf)-float(saldo)
#                         html += '<td style="text-align:right">'+str("%2.2f" % total_a).replace('.', ',')+'</td>'
#                         estadof='ACTIVO'
#                         total_credito=total_credito+float(p4[0])
#                     
#                         
#                         
#                     
#                     html += '<td>'+str(p4[8].encode('utf8'))+'</td>'
#                     
#                     html += '</tr>'
#                     
#                     print 'hrl'
#                 
#                 total_facturas=total_facturas+total_a
#         html+='</tbody>'
#         html+='<tfoot><tr><td></td><td></td><td></td><td style="text-align:right">'+str("%2.2f" % total_debito).replace('.', ',')+'</td><td style="text-align:right">'+str("%2.2f" % total_credito).replace('.', ',')+'</td><td></td><td></td></tr>'
#         html+='<tr><td colspan="4" style="text-align:right"><b>TOTAL DE PAGAR PROVEEDOR</b></td><td style="text-align:right">'+str("%2.2f" % total_facturas).replace('.', ',')+'</td><td></td><td></td></tr></tfoot>'
#         html+='</table>'
# 
#         return HttpResponse(
#             html
#         )
#     else:
#         raise Http404
# 
#     

@login_required()
def consultaCuentaProveedorView(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        proveedor = request.POST.get('proveedor')
        proveedor_hasta0 = request.POST.get('proveedor_hasta')
        total_debito=0
        total_facturas=0
        proveedor_s=Proveedor.objects.get(proveedor_id=proveedor)
        if proveedor_s:
            nombre_proveedor=proveedor_s.nombre_proveedor
            codigo_proveedor=proveedor_s.codigo_proveedor
            saldo_inicial=proveedor_s.saldo_factura
            total_debito=float(saldo_inicial)
        else:
            nombre_proveedor=''
            saldo_inicial=0
            
        proveedor_h=Proveedor.objects.get(proveedor_id=proveedor_hasta0)
        if proveedor_h:
            nombre_proveedor_h=proveedor_h.nombre_proveedor
            codigo_proveedor_h=proveedor_h.codigo_proveedor
        else:
            nombre_proveedor_h=''
            
            
        

        
        
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info">'
        html+='<thead>'
        html+='<tr><td colspan="7" style="text-align:center"><b>REPORTE DE ESTADO DE CUENTA DEL PROVEEDOR <br > DESDE '+str(codigo_proveedor.encode('utf8'))+' '+str(nombre_proveedor.encode('utf8'))+' HASTA '+str(codigo_proveedor_h.encode('utf8'))+' '+str(nombre_proveedor_h.encode('utf8'))+'</b></td></tr>'
        html+='<tr><td colspan="2"><b>DESDE</b></td><td colspan="2">'+str(fechainicial)+'</td><td colspan="2"><b>HASTA</b></td><td colspan="1">'+str(fechafin)+'</td></tr>'
        # html+='<tr><th>TIPO</th>'
        # #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        # html+='<th>Numero</th>'
        # html+= '<th>Fecha</th>'
        # html+='<th>Debito</th><th>Credito</th><th>Saldo</th><th>Concepto</th></tr></thead>'
        html+='</thead>'
        
        cursor = connection.cursor()
        cursor.execute('select proveedor_id,codigo_proveedor,nombre_proveedor,saldo_factura from proveedor '
            ' where codigo_proveedor::int>=%s '
            'and  codigo_proveedor::int<=%s '
            'order by codigo_proveedor ', (int(codigo_proveedor),int(codigo_proveedor_h)))
        rowc = cursor.fetchall()
        html+='<tbody>'
        for pc in rowc:
            proveedor=pc[0]
            cursor = connection.cursor();
            cursor.execute("SELECT  distinct dv.id,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0,dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_proveedor,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,c.codigo_proveedor,c.ruc,drv.id,dv.anulado,dv.id FROM documento_compra dv LEFT JOIN proveedor c ON c.proveedor_id=dv.proveedor_id LEFT JOIN documento_retencion_compra drv ON drv.documento_compra_id=dv.id  where dv.anulado is not True and dv.no_afecta is not True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' and dv.proveedor_id="+str(proveedor)+" order by dv.fecha_emision")
            row = cursor.fetchall();
            total = 0
            subtotal = 0
            iva = 0
            total_facturas=0
            total_credito=0
            total_debito=0
            total_saldo=0
            saldo_inicial=0
            if pc[3]:
                saldo_inicial=pc[3]
            
            cursor = connection.cursor()
            sql_i="select distinct m.id,da.abono,da.abono,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion from documento_abono da LEFT JOIN movimiento m ON m.id=da.movimiento_id and m.fecha_emision>='" + fechainicial + "' and m.fecha_emision<='" + fechafin + "'  LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.saldo_inicial is True and da.proveedor_id="+str(proveedor)+" and m.id is not Null order by m.fecha_emision"
            #print sql_i
            cursor.execute(sql_i);
            row_i= cursor.fetchall()
            
            if saldo_inicial>0 or len(row_i)>0 or len(row)>0:
                if pc[2]:
                    html+='<tr><td colspan="7"><h5><b>'+str(pc[1])+'-'+str(pc[2].encode('utf8'))+'</b></h5></td></tr>'
                else:
                    html+='<tr><td colspan="7"><h5><b>'+str(pc[1])+'</b></h5></td></tr>'
                    
                html+='<tr style="border:solid 1px black"><td><b>TIPO</b></td>'
                html+='<td style="width:150px ;"><b>Numero</b></td>'
                html+= '<td style="width:81px ;"><b>Fecha</b></td>'
                html+='<td><b>Debito</b></td><td><b>Credito</b></td><td><b>Saldo</b></td><td><b>Concepto</b></td></tr>'
                html+='<tr>'
                html+='<tr><td><b>SALDO INICIAL</b></td><td style="text-align:center"></td>'
                html+='<td style="text-align:center"><b></b></td><td style="text-align:right">0,00</td><td style="text-align:right">0,00</td>'
                #html+='<td style="text-align:right"><b>'+str("%2.2f" % saldo_inicial).replace('.', ',')+'</b></td>'
                html+='<td style="text-align:right"><b>'+str("%2.2f" % saldo_inicial).replace('.', ',')+'</b></td><td></td></tr>'
                html+='<tr>'
                
                sub_saldo=0
                saldo_total_movi=0
                saldo_final_inicial=0
                if row_i:
                    for pi in row_i:
                        html += '<tr>'
                        if pi[12]:
                            html += '<td>'+str(pi[12].encode('utf8'))+'</td>'
                        else:
                            html += '<td></td>'
                        html += '<td>'+str(pi[8])+'</td>'
                        html += '<td>'+str(pi[3])+'</td>'
                        
                        if pi[1]:
                            saldo_i_monto=float(pi[1])
                        else:
                            saldo_i_monto=0
                        
                        saldo_mov_inicial=float(saldo_i_monto)
                        saldo_total_movi=saldo_total_movi+saldo_mov_inicial
                        #credito
                        
                        html += '<td style="text-align:right">'+str("%2.2f" % saldo_mov_inicial).replace('.', ',')+'</td>'
                        saldo_final_inicial=float(saldo_inicial)-float(saldo_total_movi)
                        html += '<td style="text-align:right">0,00</td>'
                        html += '<td style="text-align:right">'+str("%2.2f" % saldo_final_inicial).replace('.', ',')+'</td>'
                        if pi[7]:
                            html += '<td >'+str(pi[7].encode('utf8'))+'</td>'
                        else:
                            html += '<td ></td>'
                        html += '</tr>'
                else:
                    saldo_final_inicial=float(saldo_inicial)
                total_facturas=total_facturas+saldo_final_inicial
                total_credito=total_credito+saldo_total_movi
     
                for p in row:
                    html += '<td><b>FACTURA</b></td>'
                    factura=''
                    if p[2]:
                        factura+=''+str(p[2]) +'-'
                    else:
                        factura+='-'
                    
                    if p[3]:
                        factura+=''+str(p[3]) +'-'
                    else:
                        factura+='-'
                    
                    if p[4]:
                        factura+=''+str(p[4]) 
                    else:
                        factura+=''
                    html += '<td style="text-align:center"><b>' + str(factura) + '</b></td>'
        
                    if p[1]:
                        html += '<td style="text-align:center"><b>' + str(p[1]) +'</b></td>'
                    else:
                        html += '<td></td>'
                    
                   
                    
                    if p[14]:
                        #html += '<td style="text-align:center">' + str(p[14]) + '</td>'
                        totalf=p[14]
                    else:
                        #html += '<td></td>'
                        totalf=0
                    
                    total_debito=total_debito+totalf
                    
                    html += '<td style="text-align:right">0,00</td>'
                    html += '<td style="text-align:right"><b>' + str("%2.2f" % totalf).replace('.', ',') + '</b></td>'
                    html += '<td style="text-align:right"><b>' + str("%2.2f" % totalf).replace('.', ',')  + '</b></td>'
                    if p[6]:
                        html += '<td><b>'+str(p[6].encode('utf8'))+'</b></td>'
                    else:
                        html += '<td></td>'
                     
                    html += '</tr>'
                    #RETENCIONES SUMA
                      
                    if p[0]:
                        
                        saldo=0
                        cursor = connection.cursor()
                        sqlr3="select sum(drdv.valor_retenido),drv.id,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id from documento_retencion_compra drv,documento_retencion_detalle_compra drdv where drv.id=drdv.documento_retencion_compra_id and drv.documento_compra_id="+ str(p[0])+" group by drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id"
                        #print sqlr3
                        cursor.execute(sqlr3);
                        rowr21 = cursor.fetchall()
                        retencion=0
                        retencion1=0
                        for pr2 in rowr21:
                            
                            retencion_cod=''
                            if pr2[2]:
                                retencion_cod+=''+str(pr2[2]) +'-'
                            else:
                                retencion_cod+='-'
                            
                            if pr2[3]:
                                retencion_cod+=''+str(pr2[3]) +'-'
                            else:
                                retencion_cod+='-'
                            
                            if pr2[4]:
                                retencion_cod+=''+str(pr2[4]) 
                            else:
                                retencion_cod+=''
                            
                            html += '<tr>'
                            html += '<td>RETENCIONES</td>'
                            
                            html+='<td style="text-align:center">'+str(retencion_cod)+'</td>'
                            html+='<td style="text-align:center">'+str(pr2[5])+'</td>'
                            
                            
                            
                            if pr2[0]:
                                saldo=Decimal(saldo)+Decimal(pr2[0])
                                ret1=pr2[0]
                            else:
                                ret1=0
                                
                            
                            total_a=float(totalf)-float(saldo)
                            total_credito=total_credito+float(ret1)
                            html+='<td style="text-align:right">'+str("%2.2f" % ret1).replace('.', ',') +'</td>'
                            html+='<td style="text-align:right" >0,00</td>'
                            html+='<td style="text-align:right">'+str("%2.2f" % total_a).replace('.', ',')+'</td>'
                            if pr2[6]:
                                html+='<td style="text-align:center">'+str(pr2[6].encode('utf8'))+'</td>'
                            else:
                                html+='<td style="text-align:center"></td>'
        
                            html += '</tr>'
                        #ABONO DE MOVIMIENTOS
                        cursor = connection.cursor();
                        sql3="select distinct da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,da.observacion,da.id from documento_abono da LEFT JOIN movimiento m ON m.id=da.movimiento_id and m.fecha_emision>='" + fechainicial + "' and m.fecha_emision<='" + fechafin + "' and m.activo is True LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.documento_compra_id="+ str(p[0])+" order by m.fecha_emision"
                        print sql3
                        cursor.execute(sql3);
                        row3 = cursor.fetchall()
                        
                        for p3 in row3:
                            if p3[13]:
                                html += '<tr>'
                                if p3[13]:
                                    html += '<td>'+str(p3[13].encode('utf8'))+'</td>'
                                else:
                                    html += '<td></td>'
                               
                                
                                
                                #html += '<td></td>'
                                #html += '<td>'+str(p3[13])+'</td>'
                                html += '<td>'+str(p3[9])+'</td>'
                                html += '<td>'+str(p3[4])+'</td>'
                                #html += '<td></td>'
                                
                                #credito
                                html += '<td style="text-align:right">'+str("%2.2f" % p3[0]).replace('.', ',')+'</td>'
                                html += '<td style="text-align:right">0,00</td>'
                                total_a=0
                                
                                if p[11]==True:
                                    html += '<td></td>'
                                    estadof='ANULADO'
                                    
                                else:                        
                                    saldo=saldo+p3[0]
                                    total_a=float(totalf)-float(saldo)
                                    html += '<td style="text-align:right">'+str("%2.2f" % total_a).replace('.', ',')+'</td>'
                                    estadof='ACTIVO'
                                    total_credito=total_credito+float(p3[0])
                                
                                    
                                if p3[8]:
                                    html += '<td>'+str(p3[8].encode('utf8'))+'</td>'
                                else:
                                    html += '<td></td>'    
                                
                                
                                
                                html += '</tr>'
                            
                            
                        
                        
                        #NOTAS DE CREDITO
                        cursor = connection.cursor();
                        sql4="select distinct da.total,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion from movimiento_nota_credito da LEFT JOIN movimiento m ON m.id=da.movimiento_id and m.activo is True LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.documento_compra_id="+ str(p[0])+" order by m.fecha_emision"
                        #print sql4
                        cursor.execute(sql4);
                        row4 = cursor.fetchall()
                        
                        for p4 in row4:
                            html += '<tr>'
                            if p4[13]:
                                html += '<td>'+str(p4[13].encode('utf8'))+'</td>'
                            else:
                                html += '<td></td>'
                            
                            #html += '<td></td>'
                            #html += '<td>'+str(p3[13])+'</td>'
                            html += '<td>'+str(p4[9])+'</td>'
                            html += '<td>'+str(p4[4])+'</td>'
                            #html += '<td></td>'
                            
                            #credito
                            html += '<td style="text-align:right">'+str("%2.2f" % p4[0]).replace('.', ',')+'</td>'
                            html += '<td style="text-align:right">0,00</td>'
                            total_a=0
                            
                            if p[11]==True:
                                html += '<td></td>'
                                estadof='ANULADO'
                                
                            else:                        
                                saldo=saldo+p4[0]
                                total_a=float(totalf)-float(saldo)
                                html += '<td style="text-align:right">'+str("%2.2f" % total_a).replace('.', ',')+'</td>'
                                estadof='ACTIVO'
                                total_credito=total_credito+float(p4[0])
                            
                                
                                
                            if p4[8]:
                                html += '<td>'+str(p4[8].encode('utf8'))+'</td>'
                            else:
                                html += '<td></td>'
                            
                            html += '</tr>'
                            
                            #print 'hrl'
                        
                        total_facturas=total_facturas+total_a
                
                html+='<tr><td></td><td></td><td></td><td style="text-align:right">'+str("%2.2f" % total_credito).replace('.', ',')+'</td><td style="text-align:right">'+str("%2.2f" % total_debito).replace('.', ',')+'</td><td></td><td></td></tr>'
                html+='<tr><td colspan="4" style="text-align:right"><b>TOTAL DE PAGAR PROVEEDOR</b></td><td style="text-align:right">'+str("%2.2f" % total_facturas).replace('.', ',')+'</td><td></td><td></td></tr>'
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404

   
@login_required()
def movimiento_list_proforma_view(request):
    movimientos = Movimiento.objects.filter(proforma=True).order_by('-id')
    template = loader.get_template('movimientos/index_proforma.html')
    context = RequestContext(request, {'movimientos': movimientos})
    return HttpResponse(template.render(context))

@login_required()
def movimiento_nuevo_proforma_view(request):
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    bancos = Banco.objects.filter(estado=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.all()
    form = MovimientoForm
    template = loader.get_template('movimientos/create_proforma.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos,
                                       'tipo_documentos': tipo_documentos, 'bancos': bancos, 'cuentas': cuentas,
                                       'proveedores': proveedores})
    return HttpResponse(template.render(context))



@login_required()
def consultar_proformas_abonar(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        tipo = request.POST['tipo']

        cursor = connection.cursor()
        query = 'select dv.id, to_char(dv.fecha, \'DD/MM/YYYY\') as fecha,  dv.puntos_venta_id,v.nombre as vendedor,pv.nombre as punto,dv.abreviatura_codigo, dv.codigo, dv.total,SUM(da.abono) from proforma dv INNER JOIN  puntos_venta pv ON (dv.puntos_venta_id= pv.id) INNER JOIN  vendedor v ON (dv.vendedor_id= v.id) LEFT JOIN documento_abono_venta da  ON (da.proforma_id = dv.id) where da.documento_venta_id is NULL and dv.aprobada=True and dv.anulada!= True and v.id=dv.vendedor_id and pv.id=dv.puntos_venta_id and  dv.cliente_id = ' + (id) + ' GROUP BY dv.id, dv.fecha, dv.puntos_venta_id,dv.abreviatura_codigo, dv.codigo,v.nombre,pv.nombre, dv.total;'
        print(query)
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404

    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
@transaction.atomic()
def movimiento_crear_proforma_view(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():

                with transaction.atomic():
                    print "ingresa a crear el movimiento un formulario válido"
                    cleaned_data = form.cleaned_data
                    movimiento = Movimiento()
                    movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
                    movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    movimiento.banco_id = int(cleaned_data.get('banco').id)
                    if movimiento.tipo_anticipo_id == 2:
                        movimiento.cliente_id = int(request.POST['persona_id'])
                    else:
                        movimiento.proveedor_id = int(request.POST['persona_id'])
                    movimiento.paguese_a = cleaned_data.get('paguese_a')
                    movimiento.numero_cheque = cleaned_data.get('numero_cheque')
                    movimiento.fecha_cheque = cleaned_data.get('fecha_cheque')
                    movimiento.descripcion = cleaned_data.get('descripcion')
                    movimiento.monto = cleaned_data.get('monto')
                    movimiento.proforma=True
                    movimiento.save()
                    movimiento.numero_comprobante = 'M'+str(now.year)+'000'+str(movimiento.id)
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.created_at = now
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.updated_at = now
                    movimiento.save()

                    #ACTUALIZACION SECUENCIAL CHEQUE
                    Banco.objects.filter(pk=movimiento.banco_id).update(secuencia=movimiento.numero_cheque + 1)

                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        asiento = Asiento()
                        asiento.codigo_asiento = "B"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE BANCOS ANTICIPO - ' + movimiento.numero_comprobante
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.created_by = request.user.get_full_name()
                        asiento.created_at = now
                        asiento.updated_by = request.user.get_full_name()
                        asiento.updated_at = now
                        asiento.save()
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            print item_asiento['id_plancuenta']
                            print item_asiento['debe']
                            print item_asiento['haber']
                            print asiento.asiento_id
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']

                            asiento_detalle.save()
                    facturas = json.loads(request.POST['arreglo_facturas'])
                    if len(facturas) > 0:
                        for item_factura in facturas:
                            if item_factura['check']:
                                if movimiento.tipo_anticipo_id == 2:

                                    abono = DocumentoAbonoVenta()
                                    abono.proforma_id = item_factura['id']
                                    abono.movimiento_id = movimiento.id
                                    abono.abono = item_factura['abono']
                                    abono.cantidad_anterior_abonada = item_factura['anterior']
                                    abono.diferencia = item_factura['diferencia']
                                    abono.created_by = request.user.get_full_name()
                                    abono.updated_by = request.user.get_full_name()
                                    abono.created_at = now
                                    abono.updated_at = now
                                    abono.save()


            else:
                form_errors = form.errors
                print form_errors
        except Exception as e:
            print (e.message)

        return HttpResponseRedirect('/bancos/movimiento_proforma')

@login_required()
def movimiento_edit_proforma_view(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.all()
    bancos = Banco.objects.filter(estado=True)
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    facturas=DocumentoCompra.objects.filter(movimiento_id=pk)
    cursor = connection.cursor()
    query = 'select dv.id, to_char(dv.fecha, \'DD/MM/YYYY\') as fecha,  dv.puntos_venta_id,v.nombre as vendedor,pv.nombre as punto,dv.abreviatura_codigo, dv.codigo, dv.total,da.abono,da.cantidad_anterior_abonada,da.diferencia from proforma dv INNER JOIN  puntos_venta pv ON (dv.puntos_venta_id= pv.id) INNER JOIN  vendedor v ON (dv.vendedor_id= v.id) LEFT JOIN documento_abono_venta da  ON (da.proforma_id = dv.id) where da.documento_venta_id is NULL and dv.aprobada=True and dv.anulada!= True and v.id=dv.vendedor_id and pv.id=dv.puntos_venta_id and  dv.cliente_id = ' + str(movimiento.cliente_id) + ';'
    cursor.execute(query)
    facturas = cursor.fetchall()
    total_facturas=DocumentoAbonoVenta.objects.filter(movimiento_id=pk).aggregate(Sum('abono'))
    if total_facturas['abono__sum']:
        total_f=total_facturas['abono__sum']
    else:
        total_f=0
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None



    template = loader.get_template('movimientos/edit_proforma.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos, 'facturas': facturas,'asientos': asientos,'detalle_asientos':detalle_asientos,
                                       'tipo_documentos': tipo_documentos, 'clientes': clientes, 'bancos': bancos, 'cuentas': cuentas,
                                       'proveedores': proveedores,'total_f':total_f})
    return HttpResponse(template.render(context))



@login_required()
def movimiento_nuevo_cliente_view(request):
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    bancos = Banco.objects.filter(estado=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(cliente=True).exclude(id=9).exclude(id=3)
    tarjeta_credito = TarjetaCredito.objects.all()
    puntos= PuntosVenta.objects.order_by('id')
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    centros= CentroCosto.objects.all()

    form = MovimientoForm
    template = loader.get_template('movimientos/create_cliente.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos, 'puntos': puntos,'centros_defecto':centros_defecto,'centros':centros,
                                       'tipo_documentos': tipo_documentos, 'bancos': bancos, 'cuentas': cuentas,'tarjeta_credito':tarjeta_credito,
                                       'proveedores': proveedores})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def movimiento_crear_cliente_view(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():

                with transaction.atomic():
                    print "ingresa a crear el movimiento un formulario valido43"
                    cleaned_data = form.cleaned_data
                    movimiento = Movimiento()
                    movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
                    movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    movimiento.banco_id = int(cleaned_data.get('banco').id)
                    if movimiento.tipo_anticipo_id == 2:
                        movimiento.cliente_id = int(request.POST['persona_id'])
                    else:
                        movimiento.proveedor_id = int(request.POST['persona_id'])
                    movimiento.paguese_a = cleaned_data.get('paguese_a')
                    movimiento.numero_cheque = cleaned_data.get('numero_cheque')
                    movimiento.fecha_cheque = cleaned_data.get('fecha_cheque')
                    movimiento.descripcion = cleaned_data.get('descripcion')
                    movimiento.monto = cleaned_data.get('monto')
                    if movimiento.tipo_documento_id== 5:
                        print 'entro a tarjeta'
                        print request.POST['tarjeta_credito']
                        print request.POST['punto_venta']
                        movimiento.tarjeta_credito_id =  request.POST['tarjeta_credito']
                        movimiento.puntos_venta_id = request.POST['punto_venta']
                    movimiento.numero_lote = cleaned_data.get('numero_lote')
                    movimiento.save()
                    movimiento.numero_comprobante = 'M'+str(now.year)+'000'+str(movimiento.id)
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.created_at = now
                    movimiento.updated_at = now
                    movimiento.save()
                    try:
                        secuencial = Secuenciales.objects.get(modulo='documento_ingreso_movimiento')
                        movimiento.numero_ingreso=secuencial.secuencial
                        movimiento.save()
                        secuencial.secuencial=secuencial.secuencial+1
                        secuencial.created_by = request.user.get_full_name()
                        secuencial.updated_by = request.user.get_full_name()
                        secuencial.created_at = now
                        secuencial.updated_at = now
                        secuencial.save()
                    except Secuenciales.DoesNotExist:
                        secuencial = None
                    

                    
                    #ACTUALIZACION SECUENCIAL CHEQUE
                    #Banco.objects.filter(pk=movimiento.banco_id).update(secuencia=movimiento.numero_cheque + 1)
                    contador = request.POST["columnas_receta"]
                    print contador
                    i = 0
                    while int(i) <= int(contador):
                        i += 1
                        print('entro comoqw' + str(i))
                        if int(i) > int(contador):
                            print('entrosd')
                            break
                        else:
                            if 'id_kits' + str(i) in request.POST:
                                print 'entro fact'
                                tipo_mov=request.POST["tipo_kits"+str(i)]
                                if tipo_mov == "FA":
                                    idf=request.POST["id_kits"+str(i)]
                                    fact = DocumentoVenta.objects.get(id=idf)
                                    fact.pagado = True
                                    fact.movimiento_id = movimiento.id
                                    fact.save()
                                    abono = DocumentoAbonoVenta()
                                    abono.documento_venta_id = request.POST["id_kits"+str(i)]
                                    abono.movimiento_id = movimiento.id
                                    abono.abono = request.POST["abono_kits"+str(i)]
                                    abono.cantidad_anterior_abonada =request.POST["cantidad_kits"+str(i)]
                                    abono.diferencia = request.POST["diferencia_kits"+str(i)]
                                    abono.created_by = request.user.get_full_name()
                                    abono.updated_by = request.user.get_full_name()
                                    abono.created_at = now
                                    abono.updated_at = now
                                    abono.save()
                                else:

                                    abono = DocumentoAbonoVenta()
                                    abono.proforma_id = request.POST["id_kits"+str(i)]
                                    abono.movimiento_id = movimiento.id
                                    abono.abono = request.POST["abono_kits" + str(i)]
                                    abono.cantidad_anterior_abonada = request.POST["cantidad_kits" + str(i)]
                                    abono.diferencia = request.POST["diferencia_kits" + str(i)]
                                    abono.created_by = request.user.get_full_name()
                                    abono.updated_by = request.user.get_full_name()
                                    abono.created_at = now
                                    abono.updated_at = now
                                    abono.save()
                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        asiento = Asiento()
                        asiento.codigo_asiento = "B"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE BANCOS - ' + movimiento.numero_comprobante
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        asiento.modulo='Bancos-DEPOSITO CLIENTES'
                        
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.created_by = request.user.get_full_name()
                        asiento.created_at = now
                        asiento.updated_by = request.user.get_full_name()
                        asiento.updated_at = now
                        asiento.save()
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            print item_asiento['id_plancuenta']
                            print item_asiento['debe']
                            print item_asiento['haber']
                            print asiento.asiento_id
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.tipo=item_asiento['tipo']
                            asiento_detalle.subtipo=item_asiento['subtipo']
                            asiento_detalle.centro_costo_id = item_asiento['centro']
                            asiento_detalle.save()
                    # facturas = json.loads(request.POST['arreglo_facturas'])
                    # if len(facturas) > 0:
                    #     for item_factura in facturas:
                    #         if item_factura['check']:

            else:
                form_errors = form.errors
                print form.is_valid(), form.errors, type(form.errors)
        except Exception as e:
            print (e.message)

        return HttpResponseRedirect('/bancos/movimiento_cliente')

@login_required()
def movimiento_cliente_list_view(request):
    #movimientos = Movimiento.objects.filter(tipo_anticipo=2).filter(proforma=False).exclude(tipo_documento_id=9).exclude(tipo_documento_id=3).exclude(tipo_documento_id=2).order_by('-id')
    cursor = connection.cursor()
    query = " select m.id,m.tipo_anticipo_id,ta.descripcion,m.numero_comprobante,td.descripcion,to_char(m.fecha_emision, \'YYYY/MM/DD\') as fecha_emision,m.paguese_a,m.descripcion,c.nombre_cliente,p.nombre_proveedor,ba.nombre, m.activo,m.monto,td.id,m.conciliacion_id,m.asociado_cheques_protestados,b.id,m.numero_cheque,pu.nombre from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN puntos_venta pu  ON pu.id = m.puntos_venta_id LEFT JOIN conciliacion co  ON co.id = m.conciliacion_id LEFT JOIN tipo_anticipo ta  ON ta.id = m.tipo_anticipo_id LEFT JOIN cliente c  ON c.id_cliente = m.cliente_id LEFT JOIN proveedor p  ON p.proveedor_id = m.proveedor_id LEFT JOIN banco ba  ON ba.id = m.banco_id  left join bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM m.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from m.fecha_emision) where 1=1 and m.tipo_documento_id!=9 and m.tipo_documento_id!=3 and m.tipo_documento_id!=2 and m.tipo_anticipo_id=2  and m.proforma is False order by m.fecha_emision"
    cursor.execute(query)
    ro = cursor.fetchall()
    template = loader.get_template('movimientos/index_cliente.html')
    context = RequestContext(request, {'movimientos': ro})
    return HttpResponse(template.render(context))



@login_required()
def movimiento_edit_cliente_view(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(cliente=True)
    bancos = Banco.objects.filter(estado=True)
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    facturas=DocumentoCompra.objects.filter(movimiento_id=pk)
    cursor = connection.cursor()
    if movimiento.tipo_anticipo_id==1:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_compra f,documento_abono da where da.movimiento_id = ' + (
    pk) + ' and f.id=da.documento_compra_id;'
    else:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_venta f,documento_abono_venta da where da.movimiento_id = ' + (
            pk) + ' and f.id=da.documento_venta_id;'
    cursor.execute(query)
    facturas = cursor.fetchall()
    total_facturas=DocumentoAbono.objects.filter(movimiento_id=pk).aggregate(Sum('abono'))
    if total_facturas['abono__sum']:
        total_f=total_facturas['abono__sum']
    else:
        total_f=0
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None



    template = loader.get_template('movimientos/edit_cliente.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos, 'facturas': facturas,'asientos': asientos,'detalle_asientos':detalle_asientos,
                                       'tipo_documentos': tipo_documentos, 'clientes': clientes, 'bancos': bancos, 'cuentas': cuentas,
                                       'proveedores': proveedores,'total_f':total_f})
    return HttpResponse(template.render(context))



def consultar_plan_cobrar_cliente(request):
    if request.method == "POST" and request.is_ajax:
        banco = request.POST['banco']
        tipo = request.POST['tipo_documento']
        persona = request.POST['persona']
        cursor = connection.cursor()
        if(tipo == '5'):
            valor = Parametros.objects.get(clave='cuenta_cobrar_tarjeta_credito')
            query = "select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp where cp.codigo_plan ='"+ str(
                valor.valor) + "';"


        else:
            if (tipo == '6'):
                valor = Parametros.objects.get(clave='cuenta_cobrar_retencion_iva')
                query = "select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp where cp.codigo_plan ='" + str(
                    valor.valor) + "';"

            else:
                if (tipo == '7'):
                    valor = Parametros.objects.get(clave='cuenta_cobrar_facturas_no_cobrar')
                    query = "select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp where cp.codigo_plan ='" + str(
                        valor.valor) + "';"
                else:
                    if (tipo == '8'):
                        valor = Parametros.objects.get(clave='cuenta_anticipos')
                        query = "select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp where cp.codigo_plan ='" + str(
                            valor.valor) + "';"
                    else:
                        query = 'select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp, banco p where p.id = ' + str(
                        banco) + ' and cp.plan_id=p.cuenta_contable_id;'

        if (tipo == 'ir'):
            valor = Parametros.objects.get(clave='cuenta_cobrar_impuesto_renta')
            query = "select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp where cp.codigo_plan ='" + str(
                valor.valor) + "';"
        if (tipo == 'cheque_posfechado'):
            valor = Parametros.objects.get(clave='cuenta_cobrar_cheques_posfechados')
            query = "select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp where cp.codigo_plan ='" + str(
                valor.valor) + "';"


        print(query)
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")



@login_required()
def cheques_no_cobrados_list_view(request):
    cheques= ChequesNoCobrados.objects.all()
    template = loader.get_template('cheques_no_cobrados/index.html')
    context = RequestContext(request, {'cheques': cheques})
    return HttpResponse(template.render(context))


@login_required()
def cheques_no_cobrados_nuevo_view(request):

    bancos = Banco.objects.filter(estado=True)
    form = ChequesNoCobradosForm
    template = loader.get_template('cheques_no_cobrados/create.html')
    context = RequestContext(request, {'form': form, 'bancos': bancos})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def cheques_no_cobrados_crear_view(request):
    if request.method == 'POST':
        form = ChequesNoCobradosForm(request.POST)
        print("entro")
        if form.is_valid():
            print("entro2")
            try:
                with transaction.atomic():
                    cleaned_data = form.cleaned_data
                    cheque_protestado = ChequesNoCobrados()
                    cheque_protestado.fecha_emision = cleaned_data.get('fecha_emision')
                    cheque_protestado.banco_id = int(cleaned_data.get('banco').id)
                    cheque_protestado.nombre_proveedor = cleaned_data.get('nombre_proveedor')
                    cheque_protestado.numero_cheque = cleaned_data.get('numero_cheque')
                    cheque_protestado.valor_cheque = cleaned_data.get('valor_cheque')
                    cheque_protestado.descripcion = cleaned_data.get('descripcion')
                    cheque_protestado.save()


            except Exception as e:
                print("entro3")
                print (e.message)
        else:
            print("entro4")
            form_errors = form.errors
            print (form.errors)
        return HttpResponseRedirect('/bancos/cheques_no_cobrados')


@login_required()
def cheques_no_cobrados_edit_view(request, pk):
    cheque_prestado = ChequesNoCobrados.objects.get(pk=pk)
    bancos = Banco.objects.filter(estado=True)
    template = loader.get_template('cheques_no_cobrados/edit.html')
    context = RequestContext(request, {'cheque_prestado': cheque_prestado,  'bancos': bancos})
    return HttpResponse(template.render(context))


@login_required()
def cheques_no_cobrados_update_view(request, pk):
    if request.method == 'POST':
        form = ChequesNoCobradosForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cheque_protestado = ChequesNoCobrados.objects.get(pk=pk)
            cheque_protestado.fecha_emision = cleaned_data.get('fecha_emision')
            cheque_protestado.banco_id = int(cleaned_data.get('banco').id)
            cheque_protestado.cliente_id = int(cleaned_data.get('cliente').id_cliente)
            cheque_protestado.numero_cheque = cleaned_data.get('numero_cheque')
            cheque_protestado.fecha_cheque = cleaned_data.get('fecha_cheque')
            cheque_protestado.valor_cheque = cleaned_data.get('valor_cheque')
            cheque_protestado.valor_multa = cleaned_data.get('valor_multa')
            cheque_protestado.comprobante_debito = cleaned_data.get('comprobante_debito')
            cheque_protestado.descripcion = cleaned_data.get('descripcion')
            cheque_protestado.save()
        else:
            print("entro4")
            form_errors = form.errors
            print (form.errors)
        return HttpResponseRedirect('/bancos/cheques_no_cobrados')



@login_required()
def consultar_factura_proforma(request):
    if request.method == "POST":

        tipo = request.POST['tipo']
        fila = request.POST['fila']
        persona= request.POST['persona']

        cursor = connection.cursor()
        if tipo == 'PR':
            query = 'select dv.id, to_char(dv.fecha, \'DD/MM/YYYY\') as fecha, dv.abreviatura_codigo,dv.codigo, dv.iva,dv.porcentaje_iva, dv.total,SUM(da.abono),pv.nombre as punto , dv.puntos_venta_id,v.nombre as vendedor,(SELECT SUM(n.total) as total FROM movimiento_nota_credito n where 1=1 and n.proforma_id = dv.id and n.anulado is not True) C  from proforma dv INNER JOIN  puntos_venta pv ON (dv.puntos_venta_id= pv.id) INNER JOIN  vendedor v ON (dv.vendedor_id= v.id) LEFT JOIN documento_abono_venta da  ON (da.proforma_id = dv.id)  and da.documento_venta_id is NULL and da.anulado IS NOT True where  dv.aprobada=True and dv.anulada!= True and v.id=dv.vendedor_id and pv.id=dv.puntos_venta_id and  dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha, dv.puntos_venta_id,dv.abreviatura_codigo, dv.codigo,v.nombre,pv.nombre, dv.total;'
        else:
            
            #query = 'select dv.id, to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva, dv.valor_iva, dv.total,SUM(da.abono),dv.punto_emision,dr.id,sum(drd.valor_retenido) as retencion,dv.total-sum(drd.valor_retenido) from documento_venta dv LEFT JOIN documento_retencion_venta dr  ON (dr.documento_venta_id = dv.id ) LEFT JOIN documento_retencion_detalle_venta drd  ON (drd.documento_retencion_venta_id = dr.id ) LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = dv.id or da.proforma_id=dv.proforma_id) and da.anulado is not True where dv.activo is True  and dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento, dv.base_iva, dv.valor_iva, dv.total,dr.id;'
            query = 'select dv.id, to_char(dv.fecha_emision,  \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva, dv.valor_iva, dv.total,SUM(da.abono),dv.punto_emision,dr.id,dr.retenciones as retencion,dv.total-dr.retenciones,(SELECT SUM(n.total) as total FROM movimiento_nota_credito n where 1=1 and n.documento_venta_id = dv.id and n.anulado is not True) C from documento_venta dv LEFT JOIN documento_venta_retenciones dr ON dr.documento_venta_id=dv.id LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = dv.id or da.proforma_id=dv.proforma_id) and da.anulado is not True where dv.activo is True  and dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento,dr.retenciones,dv.base_iva, dv.valor_iva, dv.total,dr.id;'
        
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('movimientos/mostrar_facturas_proformas.html',
                                  {'ro': ro, 'tipo': tipo, 'persona': persona,'fila': fila,},RequestContext(request))

    else:
        tipo = request.POST['tipo']
        fila = request.POST['fila']
        persona = request.POST['persona']

        cursor = connection.cursor()
        if tipo == 'PR':
            #query = 'select dv.id, to_char(dv.fecha, \'DD/MM/YYYY\') as fecha, dv.abreviatura_codigo,dv.codigo, dv.iva,dv.porcentaje_iva, dv.total,SUM(da.abono),pv.nombre as punto , dv.puntos_venta_id,v.nombre as vendedor from proforma dv INNER JOIN  puntos_venta pv ON (dv.puntos_venta_id= pv.id) INNER JOIN  vendedor v ON (dv.vendedor_id= v.id) LEFT JOIN documento_abono_venta da  ON (da.proforma_id = dv.id)  and da.documento_venta_id is NULL and da.anulado IS NOT True where  dv.aprobada=True and dv.anulada!= True and v.id=dv.vendedor_id and pv.id=dv.puntos_venta_id and  dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha, dv.puntos_venta_id,dv.abreviatura_codigo, dv.codigo,v.nombre,pv.nombre, dv.total;'
            query = 'select dv.id, to_char(dv.fecha, \'DD/MM/YYYY\') as fecha, dv.abreviatura_codigo,dv.codigo, dv.iva,dv.porcentaje_iva, dv.total,SUM(da.abono),pv.nombre as punto , dv.puntos_venta_id,v.nombre as vendedor,(SELECT SUM(n.total) as total FROM movimiento_nota_credito n where 1=1 and n.proforma_id = dv.id and n.anulado is not True) C  from proforma dv INNER JOIN  puntos_venta pv ON (dv.puntos_venta_id= pv.id) INNER JOIN  vendedor v ON (dv.vendedor_id= v.id) LEFT JOIN documento_abono_venta da  ON (da.proforma_id = dv.id)  and da.documento_venta_id is NULL and da.anulado IS NOT True where  dv.aprobada=True and dv.anulada!= True and v.id=dv.vendedor_id and pv.id=dv.puntos_venta_id and  dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha, dv.puntos_venta_id,dv.abreviatura_codigo, dv.codigo,v.nombre,pv.nombre, dv.total;'
            
        else:
            #query = 'select dv.id, to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.subtotal,dv.base_iva, dv.valor_iva, dv.total,SUM(da.abono),dv.punto_emision from documento_venta dv LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = dv.id) and da.anulado is not True where dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento, dv.base_iva, dv.valor_iva, dv.total;'
            #query = 'select dv.id, to_char(dv.fecha_emision,  \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva, dv.valor_iva, dv.total,SUM(da.abono),dv.punto_emision,dr.id,dr.retenciones as retencion,dv.total-dr.retenciones from documento_venta dv LEFT JOIN documento_venta_retenciones dr ON dr.documento_venta_id=dv.id LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = dv.id or da.proforma_id=dv.proforma_id) and da.anulado is not True where dv.activo is True  and dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento,dr.retenciones,dv.base_iva, dv.valor_iva, dv.total,dr.id;'
            query = 'select dv.id, to_char(dv.fecha_emision,  \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva, dv.valor_iva, dv.total,SUM(da.abono),dv.punto_emision,dr.id,dr.retenciones as retencion,dv.total-dr.retenciones,(SELECT SUM(n.total) as total FROM movimiento_nota_credito n where 1=1 and n.documento_venta_id = dv.id and n.anulado is not True) C from documento_venta dv LEFT JOIN documento_venta_retenciones dr ON dr.documento_venta_id=dv.id LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = dv.id or da.proforma_id=dv.proforma_id) and da.anulado is not True where dv.activo is True  and dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento,dr.retenciones,dv.base_iva, dv.valor_iva, dv.total,dr.id;'
        print(query)
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('movimientos/mostrar_facturas_proformas.html',
                                  {'ro': ro, 'tipo': tipo, 'persona': persona,'fila': fila},
                                   RequestContext(request))

@login_required()
def MovimientoClienteUpdateView(request, pk):
    if request.method == "POST":
        movimiento = Movimiento.objects.get(id=pk)
        asiento_id=movimiento.asiento_id
        form = MovimientoForm(request.POST,request.FILES,instance=movimiento)
        p_id=pk
        print(p_id)
        print form.is_valid(), form.errors, type(form.errors)
        

        if form.is_valid() :

            new_orden=form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.asiento_id=asiento_id
            new_orden.updated_at = now
            new_orden.save()
            contador=request.POST["columnas_receta"]

            i=0
            while int(i) <= int(contador):
                i+= 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits'+str(i) in request.POST:
                        
                        if 'id_detalle'+str(i) in request.POST:
                            detalle_id=request.POST["id_detalle"+str(i)]
                            detallecompra=DocumentoAbonoVenta.objects.get(id=detalle_id)
                            tipo_mov=request.POST["tipo_kits"+str(i)]
                            if tipo_mov == "FA":
                                detallecompra.documento_venta_id = request.POST["id_kits" + str(i)]
                                detallecompra.movimiento_id = movimiento.id
                                detallecompra.abono = request.POST["abono_kits" + str(i)]
                                detallecompra.cantidad_anterior_abonada = request.POST["cantidad_kits" + str(i)]
                                detallecompra.diferencia = request.POST["diferencia_kits" + str(i)]
                                detallecompra.updated_by = request.user.get_full_name()
                                detallecompra.updated_at = now
                                detallecompra.save()
                            else:

                                detallecompra.proforma_id = request.POST["id_kits" + str(i)]
                                detallecompra.movimiento_id = movimiento.id
                                detallecompra.abono = request.POST["abono_kits" + str(i)]
                                detallecompra.cantidad_anterior_abonada = request.POST["cantidad_kits" + str(i)]
                                detallecompra.diferencia = request.POST["diferencia_kits" + str(i)]
                                detallecompra.updated_by = request.user.get_full_name()
                                detallecompra.updated_at = now
                                detallecompra.save()

                            
                            
                        else:
                            tipo_mov=request.POST["tipo_kits"+str(i)]
                            if tipo_mov == "FA":
                                it=request.POST["id_kits" + str(i)]
                                fact = DocumentoVenta.objects.get(id=it)
                                fact.pagado = True
                                fact.movimiento_id = movimiento.id
                                fact.save()
                                abono = DocumentoAbonoVenta()
                                abono.documento_venta_id = request.POST["id_kits"+str(i)]
                                abono.movimiento_id = movimiento.id
                                abono.abono = request.POST["abono_kits"+str(i)]
                                abono.cantidad_anterior_abonada =request.POST["cantidad_kits"+str(i)]
                                abono.diferencia = request.POST["diferencia_kits"+str(i)]
                                abono.created_by = request.user.get_full_name()
                                abono.updated_by = request.user.get_full_name()
                                abono.created_at = now
                                abono.updated_at = now
                                abono.save()
                            else:
                                abono = DocumentoAbonoVenta()
                                abono.proforma_id = request.POST["id_kits"+str(i)]
                                abono.movimiento_id = movimiento.id
                                abono.abono = request.POST["abono_kits" + str(i)]
                                abono.cantidad_anterior_abonada = request.POST["cantidad_kits" + str(i)]
                                abono.diferencia = request.POST["diferencia_kits" + str(i)]
                                abono.created_by = request.user.get_full_name()
                                abono.updated_by = request.user.get_full_name()
                                abono.created_at = now
                                abono.updated_at = now
                                abono.save()
                                
            #ordencompra_form=OrdenCompraForm(request.POST)
            movimiento = Movimiento.objects.get(id=pk)
            #asientos = Asiento.objects.filter(asiento_id=movimiento.asiento_id)
            facturas= DocumentoAbonoVenta.objects.filter(movimiento_id=movimiento.id)
            sum_fact = DocumentoAbonoVenta.objects.filter(movimiento_id=movimiento.id).aggregate(Sum('abono'))

            form=MovimientoForm(instance=movimiento)
            asientos = json.loads(request.POST['arreglo_asientos'])
            if len(asientos) > 0:
                        for item_asiento in asientos:
                            detalle_id=item_asiento['ida']
                            asiento_detalle = AsientoDetalle.objects.get(detalle_id=detalle_id)
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.tipo=item_asiento['tipo']
                            asiento_detalle.subtipo=item_asiento['subtipo']
                            asiento_detalle.save()
            try:
                asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
            except Asiento.DoesNotExist:
                asientos = None

            try:
                detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
            except AsientoDetalle.DoesNotExist:
                detalle_asientos = None
            
            
            if sum_fact['abono__sum']:
                sum_fact=sum_fact['abono__sum']
            else:
                sum_fact=0
        

            context = {
            'section_title':'Movimeinto',
            'detalle_asientos':detalle_asientos,
            'form':form,
            'asientos':asientos,
            'facturas':facturas,
                'sum_fact': sum_fact,
            'movimiento':movimiento
            }


            

            return render_to_response(
            'movimientos/edit_cliente.html', context,context_instance=RequestContext(request))

        else:

            movimiento = Movimiento.objects.get(id=pk)
            #asientos = Asiento.objects.filter(asiento_id=movimiento.asiento_id)
            facturas= DocumentoAbonoVenta.objects.filter(movimiento_id=movimiento.id)
            form=MovimientoForm(instance=movimiento)
            sum_fact = DocumentoAbonoVenta.objects.filter(movimiento_id=movimiento.id).aggregate(Sum('abono'))
            try:
                asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
            except Asiento.DoesNotExist:
                asientos = None

            try:
                detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
            except AsientoDetalle.DoesNotExist:
                detalle_asientos = None

            if sum_fact['abono__sum']:
                sum_fact=sum_fact['abono__sum']
            else:
                sum_fact=0

            context = {
            'section_title':'Movimeinto',
           'detalle_asientos':detalle_asientos,
            'form':form,
            'asientos':asientos,
            'facturas':facturas,
                'sum_fact': sum_fact,
            'movimiento':movimiento
            }


            

            return render_to_response(
            'movimientos/edit_cliente.html', context,context_instance=RequestContext(request))
    else:

        movimiento = Movimiento.objects.get(id=pk)
        try:
            asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
        except Asiento.DoesNotExist:
            asientos = None

        try:
            detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
        except AsientoDetalle.DoesNotExist:
            detalle_asientos = None
        
        facturas= DocumentoAbonoVenta.objects.filter(movimiento_id=movimiento.id)
        sum_fact = DocumentoAbonoVenta.objects.filter(movimiento_id=movimiento.id).aggregate(Sum('abono'))

        if sum_fact['abono__sum']:
            sum_fact = sum_fact['abono__sum']
        else:
            sum_fact = 0
        form=MovimientoForm(instance=movimiento)
        

        context = {
        'section_title':'Movimeinto',
      'detalle_asientos':detalle_asientos,
        'form':form,
        'asientos':asientos,
        'facturas':facturas,
            'sum_fact':sum_fact,
        'movimiento':movimiento
        }

        return render_to_response('movimientos/edit_cliente.html', context,context_instance=RequestContext(request))


@login_required()
def imprimir_chequePDF(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    movimiento = Movimiento.objects.get(id=pk)

    html = render_to_string('movimientos/imprimirPdf.html', {'pagesize':'A4','movimiento':movimiento,}, context_instance=RequestContext(request))
    return generar_pdf(html)
    

@login_required()
def consultar_plan_cuentas_parametros(request):
    if request.method == "POST" and request.is_ajax:
        clave = request.POST.get('clave')
        objetos = Parametros.objects.get(clave = clave)
        valor = objetos.valor
        cursor = connection.cursor()
        query = "select cp.plan_id,cp.codigo_plan, cp.nombre_plan,cp.tipo_cuenta_id from contabilidad_plandecuentas cp where cp.codigo_plan = '" + str(
                valor) + "';"

        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")


@login_required()
def movimiento_proveedor_nota_credito_view(request):
    if request.method == "POST":
        form = MovimientoForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():

                with transaction.atomic():
                    print "ingresa a crear el movimiento un formulario válido"
                    cleaned_data = form.cleaned_data
                    movimiento = Movimiento()
                    movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
                    movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    #movimiento.banco_id = int(cleaned_data.get('banco').id)
                    movimiento.proveedor_id = int(request.POST['persona_id'])
                    movimiento.paguese_a = cleaned_data.get('paguese_a')
                    movimiento.numero_cheque = 0
                    movimiento.fecha_cheque = cleaned_data.get('fecha_cheque')
                    movimiento.descripcion = cleaned_data.get('descripcion')
                    movimiento.nc_establecimiento = request.POST['establecimiento']
                    movimiento.nc_punto_emision =request.POST['punto']
                    movimiento.nc_secuencial = request.POST['secuencial']
                    movimiento.nc_autorizacion = request.POST['autorizacion']
                    movimiento.subtotal = request.POST['subtotal']
                    movimiento.subtotal_0 = request.POST['subtotal0']
                    movimiento.rise = request.POST['base_rise_factura']
                    movimiento.porcentaje_iva = request.POST['porcentaje_iva']
                    movimiento.monto = cleaned_data.get('monto')
                    movimiento.save()
                    movimiento.numero_comprobante = 'M'+str(now.year)+'000'+str(movimiento.id)
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.created_at = now
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.updated_at = now
                    movimiento.save()
                    
                    fat=int(request.POST['factura'])
                    
                    print 'factura= %s' %(fat)
                    
                    
                    nc= MovimientoNotaCredito()
                    nc.movimiento= movimiento
                    nc.fecha = cleaned_data.get('fecha_emision')
                    nc.documento_compra_id = fat
                    c_id=int(request.POST['factura'])
                    documentoc= DocumentoCompra.objects.get(id=fat)
                    documentoc.nota_credito=True
                    documentoc.save()
                    
                    nc.proveedor = True
                    nc.descripcion = cleaned_data.get('descripcion')
                    nc.total = cleaned_data.get('monto')
                    monto= cleaned_data.get('monto')
                    if monto:
                        #iva vlor
                        iva_p = Parametros.objects.get(clave='iva')
                        iva_por=Decimal(iva_p.valor)
                        print "IVA DE HOY"
                        print iva_por
                        iva=monto*(iva_por/100)
                        subtotal=monto-iva
                        nc.iva = iva
                        nc.subtotal = subtotal
                    nc.created_by = request.user.get_full_name()
                    nc.updated_by = request.user.get_full_name()
                    nc.created_at = now
                    nc.updated_at = now
                    nc.save()
                    
                    
                    
                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        asiento = Asiento()
                        asiento.codigo_asiento = "B"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE NC-PROVEEDOR - ' + movimiento.numero_comprobante
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe=request.POST['total-debe-asiento']
                        total_haber=request.POST['total-haber-asiento']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.modulo='Bancos-NC PROVEEDOR'
                        asiento.created_by = request.user.get_full_name()
                        asiento.created_at = now
                        asiento.updated_by = request.user.get_full_name()
                        asiento.updated_at = now
                        asiento.save()
                        
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            print item_asiento['id_plancuenta']
                            print item_asiento['debe']
                            print item_asiento['haber']
                            print asiento.asiento_id
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.centro_costo_id=item_asiento['centro']

                            asiento_detalle.save()

                    #ACTUALIZACION SECUENCIAL CHEQUE

                     
            else:
                form_errors = form.errors
                print form_errors
        except Exception as e:
            print (e.message)

        return HttpResponseRedirect('/bancos/movimiento')
    else:

        
        proveedores = Proveedor.objects.all()
        bancos = Banco.objects.filter(estado=True)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        tipo_anticipos = TipoAnticipo.objects.filter(id = 1)
        tipo_documentos = TipoDocumento.objects.filter(proveedor = True).filter(id=3)
        iva = Parametros.objects.get(clave='iva')
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
        centros = CentroCosto.objects.all()


        form = MovimientoForm
        template = loader.get_template('movimientos/create_nota_credito_proveedor.html')
        context = RequestContext(request, {'form': form,'tipo_anticipos': tipo_anticipos,'centros_defecto':centros_defecto,
                                           'tipo_documentos': tipo_documentos, 'bancos': bancos, 'cuentas': cuentas,
                                           'proveedores': proveedores,'iva': iva,'centros':centros})
        return HttpResponse(template.render(context))

    


@login_required()
def consultar_factura_pagadas_proveedor(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        cursor = connection.cursor()
        query = 'select dc.id,dc.establecimiento,dc.punto_emision,dc.secuencial,dc.autorizacion,dc.descripcion,dc.total,dc.pagado,dc.total_pagar,dc.asiento_id,p.cuenta_contable_compra_id from documento_compra  dc, proveedor p where p.proveedor_id=dc.proveedor_id and dc.nota_credito is not True and p.proveedor_id = ' + (id) + ';'
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")

@login_required()
def movimiento_list_nota_credito_proveedor_view(request):
    movimientos = Movimiento.objects.filter(tipo_anticipo=1).filter(tipo_documento_id=3).order_by('-id')
    cursor = connection.cursor()
    query = " select m.id,m.tipo_anticipo_id,ta.descripcion,td.descripcion,to_char(m.fecha_emision, \'YYYY/MM/DD\') as fecha_emision,m.paguese_a,m.descripcion,c.nombre_proveedor, m.activo,m.numero_comprobante,m.monto,m.monto_cheque,td.id,m.conciliacion_id,b.id from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON co.id = m.conciliacion_id LEFT JOIN tipo_anticipo ta  ON ta.id = m.tipo_anticipo_id LEFT JOIN proveedor c  ON c.proveedor_id = m.proveedor_id left join bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM m.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from m.fecha_emision) where 1=1  and m.tipo_anticipo_id=1 and m.tipo_documento_id=3 order by m.fecha_emision"
    
    #select m.id,m.tipo_anticipo_id,td.descripcion,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.monto,m.monto_cheque,td.id,da.asiento_id,m.conciliacion_id,b.id from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON (co.id = m.conciliacion_id)  left join bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM m.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from m.fecha_emision) where 1=1  and m.tipo_anticipo_id=1 and m.tipo_documento_id=3 order by m.fecha_emision"
    #print query
    cursor.execute(query)
    ro = cursor.fetchall()
    
    template = loader.get_template('movimientos/nc_proveedor_index.html')
    context = RequestContext(request, {'movimientos': ro})
    return HttpResponse(template.render(context))

@login_required()
def imprimir_comprobante_nc_proveedor(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    movimiento = Movimiento.objects.get(id=pk)
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle= AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle = None

    html = loader.get_template('movimientos/imprimir_nc_proveedor.html')
    context = RequestContext(request, {'movimiento':movimiento,'detalle':detalle,'asiento':asientos})
    return HttpResponse(html.render(context))
@login_required()
def movimiento_list_nc_cliente_bancaria_view(request):
    #movimientos = Movimiento.objects.filter(tipo_anticipo=2).filter(tipo_documento_id=3).order_by('-id')
    cursor = connection.cursor()
    query = " select m.id,m.tipo_anticipo_id,ta.descripcion,m.numero_comprobante,td.descripcion,to_char(m.fecha_emision, \'YYYY/MM/DD\') as fecha_emision,m.paguese_a,m.descripcion,c.nombre_cliente,p.nombre_proveedor,ba.nombre, m.activo,m.monto,td.id,m.conciliacion_id,m.asociado_cheques_protestados,b.id from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON co.id = m.conciliacion_id LEFT JOIN tipo_anticipo ta  ON ta.id = m.tipo_anticipo_id LEFT JOIN cliente c  ON c.id_cliente = m.cliente_id LEFT JOIN proveedor p  ON p.proveedor_id = m.proveedor_id LEFT JOIN banco ba  ON ba.id = m.banco_id  left join bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM m.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from m.fecha_emision) where 1=1 and m.tipo_documento_id=3 and m.tipo_anticipo_id=2 order by m.fecha_emision"
    print query
    cursor.execute(query)
    ro = cursor.fetchall()
    
    template = loader.get_template('movimientos/nc_cliente_bancaria_index.html')
    context = RequestContext(request, {'movimientos': ro})
    return HttpResponse(template.render(context))


@login_required()
def movimiento_nuevo_nc_bancaria_cliente_view(request):
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    bancos = Banco.objects.filter(estado=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(cliente=True).filter(id=3)
    tarjeta_credito = TarjetaCredito.objects.all()
    form = MovimientoForm
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    centros = CentroCosto.objects.all()
    template = loader.get_template('movimientos/nc_bancaria_cliente.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos,'centros':centros,'centros_defecto':centros_defecto,
                                       'tipo_documentos': tipo_documentos, 'bancos': bancos, 'cuentas': cuentas,'tarjeta_credito':tarjeta_credito,
                                       'proveedores': proveedores})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def movimiento_crear_nc_bancaria_cliente_view(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():

                with transaction.atomic():
                    print "ingresa a crear el movimiento un formulario valido43"
                    cleaned_data = form.cleaned_data
                    movimiento = Movimiento()
                    movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
                    movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    movimiento.banco_id = int(cleaned_data.get('banco').id)
                    if 'persona_id' in request.POST:
                        persona_id=request.POST['persona_id']
                        if persona_id:
                            if movimiento.tipo_anticipo_id == 2:
                                movimiento.cliente_id = int(request.POST['persona_id'])
                            else:
                                movimiento.proveedor_id = int(request.POST['persona_id'])
                        else:
                            movimiento.nc_sin_persona=True
                    movimiento.paguese_a = cleaned_data.get('paguese_a')
                    movimiento.descripcion = cleaned_data.get('descripcion')
                    movimiento.monto = cleaned_data.get('monto')
                    m=cleaned_data.get('monto')
                    print "Monto"
                    print m
                    movimiento.save()
                    movimiento.numero_comprobante = 'M'+str(now.year)+'000'+str(movimiento.id)
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.created_at = now
                    movimiento.updated_at = now
                    movimiento.save()
                    try:
                        secuencial = Secuenciales.objects.get(modulo='nc_bancaria_cliente')
                        movimiento.numero_ingreso=secuencial.secuencial
                        movimiento.save()
                        secuencial.secuencial=secuencial.secuencial+1
                        secuencial.created_by = request.user.get_full_name()
                        secuencial.updated_by = request.user.get_full_name()
                        secuencial.created_at = now
                        secuencial.updated_at = now
                        secuencial.save()
                    except Secuenciales.DoesNotExist:
                        secuencial = None
                    

                    
                    #ACTUALIZACION SECUENCIAL CHEQUE
                    #Banco.objects.filter(pk=movimiento.banco_id).update(secuencia=movimiento.numero_cheque + 1)
                    contador = request.POST["columnas_receta"]
                    print contador
                    i = 0
                    while int(i) <= int(contador):
                        i += 1
                        print('entro comoqw' + str(i))
                        if int(i) > int(contador):
                            print('entrosd')
                            break
                        else:
                            if 'id_kits' + str(i) in request.POST:
                                tipo_mov=request.POST["tipo_kits"+str(i)]
                                if tipo_mov == "FA":
                                    idf=request.POST["id_kits"+str(i)]
                                    if idf:
                                        fact = DocumentoVenta.objects.get(id=idf)
                                        fact.nota_credito=True
                                        fact.save()
                                        nc= MovimientoNotaCredito()
                                        nc.movimiento= movimiento
                                        nc.fecha = cleaned_data.get('fecha_emision')
                                        nc.documento_venta_id = request.POST["id_kits"+str(i)]
                                        nc.proveedor = False
                                        nc.descripcion = cleaned_data.get('descripcion')
                                        nc.total = cleaned_data.get('monto')
                                        monto= cleaned_data.get('monto')
                                        if monto:
                                            iva_p = Parametros.objects.get(clave='iva')
                                            iva_por=Decimal(iva_p.valor)
                                            print "IVA DE HOY"
                                            print iva_por
                                            iva=monto*(iva_por/100)
                                            
                                            subtotal=monto-iva
                                            nc.iva = iva
                                            nc.subtotal = subtotal
                                        nc.created_by = request.user.get_full_name()
                                        nc.updated_by = request.user.get_full_name()
                                        nc.created_at = now
                                        nc.updated_at = now
                                        nc.save()
                                else:
                                    idf=request.POST["id_kits"+str(i)]
                                    if idf:
                                        nc= MovimientoNotaCredito()
                                        nc.movimiento= movimiento
                                        nc.fecha = cleaned_data.get('fecha_emision')
                                        nc.proforma_id = request.POST["id_kits"+str(i)]
                                        nc.proveedor = False
                                        nc.descripcion = cleaned_data.get('descripcion')
                                        nc.total = cleaned_data.get('monto')
                                        nc.es_proforma=True
                                        monto= cleaned_data.get('monto')
                                        if monto:
                                            iva_p = Parametros.objects.get(clave='iva')
                                            iva_por=Decimal(iva_p.valor)
                                            iva=monto*(iva_por/100)
                                            
                                            subtotal=monto-iva
                                            nc.iva = iva
                                            nc.subtotal = subtotal
                                        nc.created_by = request.user.get_full_name()
                                        nc.updated_by = request.user.get_full_name()
                                        nc.created_at = now
                                        nc.updated_at = now
                                        nc.save()
                                    
                                
                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        asiento = Asiento()
                        asiento.codigo_asiento = "B"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO NOTA DE CREDITO BANCARIA  CLIENTE- ' + movimiento.numero_comprobante
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        asiento.modulo='Bancos-NC BANCARIA CLIENTE'
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.created_by = request.user.get_full_name()
                        asiento.created_at = now
                        asiento.updated_by = request.user.get_full_name()
                        asiento.updated_at = now
                        asiento.save()
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.centro_costo_id = item_asiento['centro']
                            asiento_detalle.concepto = item_asiento['concepto']
                            tip=item_asiento['tipo']
                            if tip=='debe':
                                asiento_detalle.tipo='deb'
                            else:
                                asiento_detalle.tipo='hab'
                            #asiento_detalle.subtipo=item_asiento['subtipo']
                            asiento_detalle.save()
                    # facturas = json.loads(request.POST['arreglo_facturas'])
                    # if len(facturas) > 0:
                    #     for item_factura in facturas:
                    #         if item_factura['check']:


            else:
                form_errors = form.errors
                print form_errors
        except Exception as e:
            print (e.message)

        return HttpResponseRedirect('/bancos/movimiento/nc/bancaria/cliente')




@login_required()
def NotaCreditoComercialListView(request):
    movimientos = Movimiento.objects.filter(tipo_anticipo=2).filter(tipo_documento_id=9).order_by('-id')
    cursor = connection.cursor()
    query = " select m.id,m.nro_nota_credito,m.tipo_anticipo_id,ta.descripcion,td.descripcion,to_char(m.fecha_emision, \'YYYY/MM/DD\') as fecha_emision,m.paguese_a,m.descripcion,c.nombre_cliente,m.subtotal,m.iva, m.activo,m.numero_comprobante,m.monto,td.id,m.conciliacion_id,b.id,m.facturacion_eletronica,EXTRACT(YEAR FROM m.fecha_emision) from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON co.id = m.conciliacion_id LEFT JOIN tipo_anticipo ta  ON ta.id = m.tipo_anticipo_id LEFT JOIN cliente c  ON c.id_cliente = m.cliente_id left join bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM m.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from m.fecha_emision) where 1=1  and m.tipo_anticipo_id=2 and m.tipo_documento_id=9 order by m.fecha_emision"
    
    cursor.execute(query)
    ro = cursor.fetchall()
    template = loader.get_template('movimientos/nc_cliente_comercial_index.html')
    context = RequestContext(request, {'notascredito': ro})
    return HttpResponse(template.render(context))

def NotaCreditoComercialCreateView(request):
    if request.method == 'POST':
        form=MovimientoForm(request.POST)
        
        
        nota=Movimiento()
        nota.cliente_id=request.POST["cliente_descripcion"]
        nota.fecha_emision=request.POST["fecha_vencimiento"]
        nota.razon_social_id=request.POST["razon_social_descripcion"]
        nota.puntos_venta_id=request.POST["puntos_venta"]
        nota.nro_nota_credito=request.POST["nro_nota_credito"]
        nota.descripcion=request.POST["descripcion"]
        nota.direccion=request.POST["cliente_direccion"]
        nota.ruc=request.POST["cliente_ruc"]
        nota.telefono=request.POST["cliente_telefono"]
        nota.monto=request.POST["monto"]
        nota.tipo_anticipo_id=2
        nota.tipo_documento_id=9
        nota.created_by = request.user.get_full_name()
        nota.created_at = now
        nota.updated_by = request.user.get_full_name()
        nota.updated_at = now
        
        nota.save()
        nota.numero_comprobante = 'M'+str(now.year)+'000'+str(nota.id)
        
        nota.save()
        print('GUARDAR NOTA DE CREDITO')
        # try:
        #     secuencial = Secuenciales.objects.get(modulo='nota_credito')
        #     secuencial.secuencial=secuencial.secuencial+1
        #     secuencial.created_by = request.user.get_full_name()
        #     secuencial.updated_by = request.user.get_full_name()
        #     secuencial.created_at = datetime.now()
        #     secuencial.updated_at = datetime.now()
        #     secuencial.save()
        # except Secuenciales.DoesNotExist:
        #     secuencial = None

                
        contador=request.POST["columnas_receta_f"]
        i=0
        while int(i)<=int(contador):
            i+= 1
            if int(i)> int(contador):
                break
            else:
                if 'id_kits'+str(i) in request.POST:
                    nc= MovimientoNotaCredito()
                    nc.movimiento= nota
                    nc.fecha = request.POST["fecha_vencimiento"]
                    nc.documento_venta_id = request.POST["id_kits"+str(i)]
                    v_id=request.POST["id_kits"+str(i)]
                    documentov = DocumentoVenta.objects.get(id=v_id)
                    documentov.nota_credito=True
                    documentov.save()
                    nc.proveedor = False
                    nc.descripcion = request.POST["descripcion"]
                    nc.total = request.POST["monto"]
                    monto= float(nota.monto)
                    lleva_iva= request.POST.get('lleva_iva', False)
                    nc.lleva_iva=lleva_iva
                
                    if monto:
                        #IVA valor
                        if lleva_iva:
                            iva_p = Parametros.objects.get(clave='iva')
                            iva_por=Decimal(iva_p.valor)
                        else:
                            iva_por=0
                       
                        
                        
                        subtotal=Decimal(monto)/(1+(iva_por/100))
                        iva=Decimal(subtotal)*(iva_por/100)
                        nc.iva = Decimal(iva)
                        nc.subtotal =Decimal(subtotal)
                        nota.iva = Decimal(iva)
                        nota.subtotal =Decimal(subtotal)
                        nota.save()
                    nc.created_by = request.user.get_full_name()
                    nc.updated_by = request.user.get_full_name()
                    nc.created_at = now
                    nc.updated_at = now
                    nc.save()
                                    
                     

                print('contadorsd prueba'+str(contador))
        asientos = json.loads(request.POST['arreglo_asientos'])
        if len(asientos) > 0:
            codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
            secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
            asiento = Asiento()
            asiento.codigo_asiento = "NCC" + str(now.year) + "00" + str(codigo_asiento)
            asiento.fecha = nota.fecha_emision
            asiento.glosa = 'NOTA de credito Comercial ' + str(nota.cliente.nombre_cliente.encode('utf8')) + str(nota.nro_nota_credito)+' No. Movimiento'+ str(nota.numero_comprobante)
            asiento.gasto_no_deducible = False
            asiento.modulo = 'Bancos-NC COMERCIAL '
            asiento.secuencia_asiento = codigo_asiento
            total_debe = request.POST['total-debe-asiento']
            total_haber = request.POST['total-haber-asiento']
            asiento.total_debe = total_debe
            asiento.total_haber = total_haber
            asiento.updated_by = request.user.get_full_name()
            asiento.created_by = request.user.get_full_name()
            asiento.created_at = now
            asiento.updated_at = now
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

            nota.asiento_id = asiento.asiento_id
            nota.save()
                        


        return HttpResponseRedirect('/bancos/movimiento/nc/comercial')

                
                
                
            
        
    else:
        form=MovimientoForm
        clientes= Cliente.objects.all()
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
        centros = CentroCosto.objects.all()
        iva_p = Parametros.objects.get(clave='iva')
        iva_por=Decimal(iva_p.valor)
        print(iva_por)
        
        return render_to_response('movimientos/nc_cliente_comercial.html', { 'form': form,'clientes':clientes,'cuentas':cuentas,'centros_defecto':centros_defecto,'centros':centros,'valor_iva': iva_p},  RequestContext(request))

@login_required()
def imprimir_comprobante_nc_comercial(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    movimiento = Movimiento.objects.get(id=pk)
    nc = MovimientoNotaCredito.objects.get(movimiento_id=pk)
    rango = 3
    

    html = render_to_string('movimientos/imprimir_nc_comercial.html',
                            {'pagesize': 'A4', 'documento': movimiento,'nc': nc,'rango': range(rango)},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


@login_required()
def movimiento_list_anticipo_proveedor_view(request):
    movimientos = Movimiento.objects.filter(tipo_anticipo=1).filter(tipo_documento_id=3).order_by('-id')
    template = loader.get_template('movimientos/anticipo_proveedores_list.html')
    context = RequestContext(request, {'movimientos': movimientos})
    return HttpResponse(template.render(context))



@login_required()
def movimiento_anticipo_proveedor_view(request):
    if request.method == "POST":
        form = MovimientoForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():

                with transaction.atomic():
                    print "ingresa a crear el movimiento un formulario válido"
                    cleaned_data = form.cleaned_data
                    movimiento = Movimiento()
                    movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
                    movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    #movimiento.banco_id = int(cleaned_data.get('banco').id)
                    movimiento.proveedor_id = int(request.POST['persona_id'])
                    movimiento.paguese_a = cleaned_data.get('paguese_a')
                    movimiento.numero_cheque = 0
                    movimiento.fecha_cheque = cleaned_data.get('fecha_cheque')
                    movimiento.descripcion = cleaned_data.get('descripcion')
                    movimiento.monto = cleaned_data.get('monto')
                    movimiento.save()
                    movimiento.numero_comprobante = 'M'+str(now.year)+'000'+str(movimiento.id)
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.created_at = now
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.updated_at = now
                    movimiento.save()
                    
                    fat=int(request.POST['factura'])
                    
                    print 'factura= %s' %(fat)
                
                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        asiento = Asiento()
                        asiento.codigo_asiento = "DBA"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE DAR DE BAJA ANTICIPO - ' + movimiento.numero_comprobante
                        asiento.gasto_no_deducible = False
                        asiento.modulo = 'BANCOS-DAR DE BAJA ANTICIPO '
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe=request.POST['total-debe-asiento']
                        total_haber=request.POST['total-haber-asiento']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.created_by = request.user.get_full_name()
                        asiento.created_at = now
                        asiento.updated_by = request.user.get_full_name()
                        asiento.updated_at = now
                        asiento.save()
                        
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            print item_asiento['id_plancuenta']
                            print item_asiento['debe']
                            print item_asiento['haber']
                            print asiento.asiento_id
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']

                            asiento_detalle.save()

                    #ACTUALIZACION SECUENCIAL CHEQUE

                     
            else:
                form_errors = form.errors
                print form_errors
        except Exception as e:
            print (e.message)

        return HttpResponseRedirect('/bancos/movimiento')
    else:

        clientes = Cliente.objects.all()
        proveedores = Proveedor.objects.all()
        bancos = Banco.objects.filter(estado=True)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        tipo_anticipos = TipoAnticipo.objects.filter(id = 1)
        tipo_documentos = TipoDocumento.objects.filter(proveedor = True).filter(id=3)
        form = MovimientoForm
        template = loader.get_template('movimientos/anticipo_proveedores.html')
        context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos,
                                           'tipo_documentos': tipo_documentos, 'bancos': bancos, 'cuentas': cuentas,
                                           'proveedores': proveedores})
        return HttpResponse(template.render(context))

    
@login_required()
def movimientoEliminarClienteByPkView(request, pk):
    obj = Movimiento.objects.get(id=pk)

    if obj:
        obj.activo = False
        obj.save()
        try:
            abonos = DocumentoAbonoVenta.objects.filter(movimiento_id=obj.id)
        except DocumentoAbonoVenta.DoesNotExist:
            abonos = None
        if abonos:
            for a in abonos:
                a.anulado= True
                a.save()
        try:
            asiento = Asiento.objects.filter(asiento_id=obj.asiento_id)
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            for a in asiento:
                a.anulado= True
                a.save()

    return HttpResponseRedirect('/bancos/movimiento_cliente')





@login_required()
def consultar_movimiento_conciliar(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        fecha = request.POST['fecha']
        #conciliacion_ultima=Conciliacion.objects.latest('id')
        try:
            bancos = Banco.objects.get(id=id)
            cuenta_id=bancos.cuenta_contable_id
            print "entro a banco"
            print bancos.id
            print "holl"
            print bancos.cuenta_contable_id
        except Banco.DoesNotExist:
            bancos = None
            cuenta_id=0
        cursor = connection.cursor()
        #query = "select m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id,sum(da.debe),sum(da.haber),m.conciliacion_id, to_char(co.fecha_corte, \'DD/MM/YYYY\') as fecha_corte from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON (co.id = m.conciliacion_id)  LEFT JOIN contabilidad_asientodetalle da  ON (da.asiento_id = m.asiento_id)  and da.cuenta_id="+str(cuenta_id)+" where   m.activo is True and m.banco_id= "+str(id)+" and m.fecha_emision<='"+str(fecha)+"' and (m.conciliacion_id is null or co.fecha_corte>='"+str(fecha)+"') group by m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,m.fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id,co.fecha_corte,m.conciliacion_id order by m.fecha_emision"
        query = "select m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id,sum(da.debe),sum(da.haber),m.conciliacion_id, to_char(co.fecha_corte, \'DD/MM/YYYY\') as fecha_corte,m.asociado_cheques_protestados from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON (co.id = m.conciliacion_id)  LEFT JOIN contabilidad_asientodetalle da  ON (da.asiento_id = m.asiento_id)  and da.cuenta_id="+str(cuenta_id)+" where   m.activo is True and m.banco_id= "+str(id)+" and m.fecha_emision<='"+str(fecha)+"' and (co.fecha_corte>'"+str(fecha)+"' or co.fecha_corte is null)  group by m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,m.fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id,co.fecha_corte,m.conciliacion_id order by m.fecha_emision"
        print query
 
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")



@login_required()
@csrf_exempt
def validarCheque(request):
    if request.method == 'POST':
      numero_cheque = request.POST.get('numero_cheque')
      #objetos = Proveedor.objects.get(ruc = ruc)
      #modulo_secuencial = objetos.proveedor_id
      
      cursor = connection.cursor()
      query = "select id,paguese_a,numero_cheque from movimiento where numero_cheque='" + (numero_cheque) + "' and activo is not False and tipo_documento_id=1;"
      print query
      cursor.execute(query)
      ro = cursor.fetchall()
      json_resultados = json.dumps(ro)
      return HttpResponse(json_resultados, content_type="application/json")


    else:
        raise Http404
    
    
    
    
@login_required()
def movimiento_deposito_view(request):
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    bancos = Banco.objects.filter(estado=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    tipo_anticipos = TipoAnticipo.objects.filter(id = 3)
    tipo_documentos = TipoDocumento.objects.filter(id=4)
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    centros = CentroCosto.objects.all()
    form = MovimientoForm
    template = loader.get_template('movimientos/otros_depositos.html')
    context = RequestContext(request, {'form': form,'tipo_anticipos': tipo_anticipos,'centros_defecto':centros_defecto,'centros':centros,
                                       'tipo_documentos': tipo_documentos, 'bancos': bancos, 'cuentas': cuentas,
                                       'proveedores': proveedores})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def movimiento_crear_deposito_view(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():

                with transaction.atomic():
                    print "ingresa a crear el movimiento un formulario válido"
                    cleaned_data = form.cleaned_data
                    movimiento = Movimiento()
                    movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
                    movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    movimiento.banco_id = int(cleaned_data.get('banco').id)
                    movimiento.paguese_a = cleaned_data.get('paguese_a')
                    movimiento.descripcion = cleaned_data.get('descripcion')
                    movimiento.monto = cleaned_data.get('monto')
                    movimiento.save()
                    movimiento.numero_comprobante = 'M'+str(now.year)+'000'+str(movimiento.id)
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.created_at = now
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.updated_at = now
                    movimiento.save()
                    
                    
                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        asiento = Asiento()
                        asiento.codigo_asiento = "B"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE BANCOS - ' + movimiento.numero_comprobante
                        asiento.modulo = 'Bancos-DEPOSITO '
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.created_by = request.user.get_full_name()
                        asiento.created_at = now
                        asiento.updated_by = request.user.get_full_name()
                        asiento.updated_at = now
                        asiento.save()
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            print item_asiento['id_plancuenta']
                            print item_asiento['debe']
                            print item_asiento['haber']
                            print asiento.asiento_id
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.centro_costo_id = item_asiento['centro']

                            asiento_detalle.save()
                   
            else:
                form_errors = form.errors
                print form_errors
        except Exception as e:
            print (e.message)
        
        
        item = {
            'id': movimiento.id,
            'documento': movimiento.tipo_documento_id,
        }
        json_resultados = json.dumps(item)
   
        return HttpResponse(json_resultados, content_type="application/json")

        #return HttpResponseRedirect('/bancos/movimiento')
@login_required()
def movimiento_list_deposito_view(request):
    #movimientos = Movimiento.objects.filter(tipo_anticipo=3).filter(tipo_documento_id=4).order_by('-id')
    cursor = connection.cursor()
    query = " select m.id,m.tipo_anticipo_id,ta.descripcion,m.numero_comprobante,td.descripcion,to_char(m.fecha_emision, \'YYYY/MM/DD\') as fecha_emision,m.paguese_a,m.descripcion,c.nombre_cliente,p.nombre_proveedor,ba.nombre, m.activo,m.monto,td.id,m.conciliacion_id,m.asociado_cheques_protestados,b.id from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON co.id = m.conciliacion_id LEFT JOIN tipo_anticipo ta  ON ta.id = m.tipo_anticipo_id LEFT JOIN cliente c  ON c.id_cliente = m.cliente_id LEFT JOIN proveedor p  ON p.proveedor_id = m.proveedor_id LEFT JOIN banco ba  ON ba.id = m.banco_id  left join bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM m.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from m.fecha_emision) where 1=1 and m.tipo_documento_id=4 and m.tipo_anticipo_id=3 order by m.fecha_emision"
    cursor.execute(query)
    ro = cursor.fetchall()
    
    template = loader.get_template('movimientos/depositos_list.html')
    context = RequestContext(request, {'movimientos': ro})
    return HttpResponse(template.render(context))

@login_required()
def imprimir_deposito(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    movimiento = Movimiento.objects.get(id=pk)
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle= AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle = None


    #html = render_to_string('movimientos/imprimir_orden_egreso.html', {'pagesize':'A4','movimiento':movimiento,'detalle':detalle,'asiento':asientos}, context_instance=RequestContext(request))
    #return generar_pdf(html)
    html = loader.get_template('movimientos/imprimir_deposito.html')
    context = RequestContext(request, {'movimiento':movimiento,'detalle':detalle,'asiento':asientos})
    return HttpResponse(html.render(context))


@login_required()
def nota_debito_list_view(request):
    #movimientos = Movimiento.objects.filter(tipo_documento_id=2).order_by('-id')
    cursor = connection.cursor()
    query = " select m.id,m.tipo_anticipo_id,ta.descripcion,m.numero_comprobante,td.descripcion,to_char(m.fecha_emision, \'YYYY/MM/DD\') as fecha_emision,m.paguese_a,m.descripcion,c.nombre_cliente,p.nombre_proveedor,ba.nombre, m.activo,m.monto,td.id,m.conciliacion_id,m.asociado_cheques_protestados,b.id from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON co.id = m.conciliacion_id LEFT JOIN tipo_anticipo ta  ON ta.id = m.tipo_anticipo_id LEFT JOIN cliente c  ON c.id_cliente = m.cliente_id LEFT JOIN proveedor p  ON p.proveedor_id = m.proveedor_id LEFT JOIN banco ba  ON ba.id = m.banco_id  left join bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM m.fecha_emision) and date_part('month',b.fecha)=EXTRACT(MONTH from m.fecha_emision) where 1=1 and m.tipo_documento_id=2 order by m.fecha_emision"
    cursor.execute(query)
    ro = cursor.fetchall()
    template = loader.get_template('movimientos/debito_list.html')
    context = RequestContext(request, {'movimientos': ro})
    return HttpResponse(template.render(context))


@login_required()
def nota_debito_nuevo_view(request):
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    bancos = Banco.objects.filter(estado=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    tipo_anticipos = TipoAnticipo.objects.all().exclude(id = 2)
    tipo_documentos = TipoDocumento.objects.filter(proveedor = True).filter(id=2)
    cursor = connection.cursor()
    facturas_sql='select dc.id, to_char(dc.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,SUM(da.abono),dc.punto_emision,dc.secuencial,dc.descripcion,dc.valor_retenido,dc.total_pagar ,SUM(m.total) as nc from documento_compra dc LEFT JOIN documento_abono da  ON (da.documento_compra_id = dc.id)  and da.anulado is not True  LEFT JOIN movimiento_nota_credito m  ON (m.documento_compra_id = dc.id) AND m.anulado is not True where  dc.anulado is not True GROUP BY dc.id, dc.fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,dc.valor_retenido,dc.total_pagar;'
    cursor.execute(facturas_sql)
    ro = cursor.fetchall()
    
    
    form = MovimientoForm
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    centros = CentroCosto.objects.all()

    template = loader.get_template('movimientos/create_debito.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos,'centros_defecto':centros_defecto,'centros':centros,
                                       'tipo_documentos': tipo_documentos, 'bancos': bancos, 'cuentas': cuentas,'facturas_sql': ro,
                                       'proveedores': proveedores})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def nota_debito_crear_view(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():

                with transaction.atomic():
                    print "ingresa a crear el movimiento un formulario válido"
                    cleaned_data = form.cleaned_data
                    movimiento = Movimiento()
                    movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
                    movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    movimiento.banco_id = int(cleaned_data.get('banco').id)
                    if int(cleaned_data.get('tipo_anticipo').id) == 2:
                        if request.POST['persona_id']:
                            movimiento.cliente_id = int(request.POST['persona_id'])
                    else:
                        if int(cleaned_data.get('tipo_anticipo').id)== 1:
                             if request.POST['persona_id']:
                                movimiento.proveedor_id = int(request.POST['persona_id'])
                    movimiento.paguese_a = cleaned_data.get('paguese_a')
                    movimiento.descripcion = cleaned_data.get('descripcion')
                    movimiento.monto = cleaned_data.get('monto')
                    movimiento.save()
                    movimiento.numero_comprobante = 'ND'+str(now.year)+'000'+str(movimiento.id)
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.created_at = now
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.updated_at = now
                    movimiento.save()
                   
                    #ACTUALIZACION SECUENCIAL CHEQUE
                    
                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        asiento = Asiento()
                        asiento.codigo_asiento = "B"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE NOTAS DE DEBITO - ' + movimiento.numero_comprobante
                        asiento.gasto_no_deducible = False
                        asiento.modulo = 'Bancos- NOTA DE DEBITO '
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.updated_by = request.user.get_full_name()
                        asiento.created_by = request.user.get_full_name()
                        asiento.created_at = now
                        asiento.updated_at = now
                        asiento.save()
                        
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            print item_asiento['id_plancuenta']
                            print item_asiento['debe']
                            print item_asiento['haber']
                            print asiento.asiento_id
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.centro_costo_id = item_asiento['centro']

                            asiento_detalle.save()
                    
                    contador = request.POST["columnas_recetaf"]
                    i = 0
                    while int(i) < int(contador):
                        i += 1
                        if 'facturas_kits' + str(i) in request.POST:
                            
                            if 'id_detallef' + str(i) in request.POST:
                                id_detall=request.POST["id_detallef" + str(i)]
                                if id_detall:
                                    print "ID detalle"
                                    print id_detall
                                    asientodetalle=DocumentoAbono.objects.get(id=id_detall)
                                    asientodetalle.abono = request.POST["monto_kits" + str(i)]
                                    asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                                    asientodetalle.activo=True
                                    asientodetalle.anulado=False
                                    asientodetalle.updated_by = request.user.get_full_name()
                                    asientodetalle.updated_at = now
                                    asientodetalle.save()
                                else:
                                    fact=request.POST["facturas_kits" + str(i)]
                                    if fact!='0':
                                        asientodetalle = DocumentoAbono()
                                        asientodetalle.movimiento_id = movimiento.id
                                        asientodetalle.documento_compra_id = request.POST["facturas_kits" + str(i)]
                                        asientodetalle.abono = request.POST["monto_kits" + str(i)]
                                        asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                                        asientodetalle.activo=True
                                        asientodetalle.anulado=False
                                        asientodetalle.updated_by = request.user.get_full_name()
                                        asientodetalle.created_by = request.user.get_full_name()
                                        asientodetalle.created_at = now
                                        asientodetalle.updated_at = now
                                        asientodetalle.save()
                                    
                                
                            else:
                                fact=request.POST["facturas_kits" + str(i)]
                                if fact!='0':
                                    asientodetalle = DocumentoAbono()
                                    asientodetalle.movimiento_id = movimiento.id
                                    asientodetalle.abono = request.POST["monto_kits" + str(i)]
                                    asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                                    asientodetalle.documento_compra_id = request.POST["facturas_kits" + str(i)]
                                    asientodetalle.activo=True
                                    asientodetalle.anulado=False
                                    asientodetalle.updated_by = request.user.get_full_name()
                                    asientodetalle.created_by = request.user.get_full_name()
                                    asientodetalle.created_at = now
                                    asientodetalle.updated_at = now
                                    asientodetalle.save()
                                        
                            

            
            
            else:
                form_errors = form.errors
                print form_errors
        except Exception as e:
            print (e.message)
        
        
        item = {
            'id': movimiento.id,
            'documento': movimiento.tipo_documento_id,
        }
        json_resultados = json.dumps(item)
   
        return HttpResponse(json_resultados, content_type="application/json")

        #return HttpResponseRedirect('/bancos/movimiento')

@login_required()
def imprimir_nd(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    movimiento = Movimiento.objects.get(id=pk)
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle= AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle = None


    #html = render_to_string('movimientos/imprimir_orden_egreso.html', {'pagesize':'A4','movimiento':movimiento,'detalle':detalle,'asiento':asientos}, context_instance=RequestContext(request))
    #return generar_pdf(html)
    html = loader.get_template('movimientos/imprimir_nd.html')
    context = RequestContext(request, {'movimiento':movimiento,'detalle':detalle,'asiento':asientos})
    return HttpResponse(html.render(context))


@login_required()
def movimiento_nuevo_cliente_cheques_posfechados_view(request):
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    bancos = Banco.objects.filter(estado=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documento = TipoDocumento.objects.get(id=11)
    tarjeta_credito = TarjetaCredito.objects.all()
    puntos= PuntosVenta.objects.order_by('id')

    form = MovimientoForm
    template = loader.get_template('movimientos/cheques_posfechados.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos, 'puntos': puntos,
                                       'tipo_documento': tipo_documento, 'bancos': bancos, 'cuentas': cuentas,'tarjeta_credito':tarjeta_credito,
                                       'proveedores': proveedores})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def movimiento_crear_cliente_cheques_posfechados_view(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():

                with transaction.atomic():
                    print "ingresa a crear el movimiento un formulario valido43"
                    cleaned_data = form.cleaned_data
                    movimiento = Movimiento()
                    movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
                    movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    movimiento.banco_id = int(cleaned_data.get('banco').id)
                    if movimiento.tipo_anticipo_id == 2:
                        movimiento.cliente_id = int(request.POST['persona_id'])
                    else:
                        movimiento.proveedor_id = int(request.POST['persona_id'])
                    movimiento.paguese_a = cleaned_data.get('paguese_a')
                    movimiento.numero_cheque = cleaned_data.get('numero_cheque')
                    movimiento.fecha_cheque = cleaned_data.get('fecha_cheque')
                    movimiento.descripcion = cleaned_data.get('descripcion')
                    movimiento.monto = cleaned_data.get('monto')
                    movimiento.puntos_venta_id = request.POST['punto_venta']
                    movimiento.save()
                    movimiento.numero_comprobante = 'M'+str(now.year)+'000'+str(movimiento.id)
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.created_at = now
                    movimiento.updated_at = now
                    movimiento.save()
                    try:
                        secuencial = Secuenciales.objects.get(modulo='documento_ingreso_movimiento')
                        movimiento.numero_ingreso=secuencial.secuencial
                        movimiento.save()
                        secuencial.secuencial=secuencial.secuencial+1
                        secuencial.created_by = request.user.get_full_name()
                        secuencial.updated_by = request.user.get_full_name()
                        secuencial.created_at = now
                        secuencial.updated_at = now
                        secuencial.save()
                    except Secuenciales.DoesNotExist:
                        secuencial = None
                    

                    
                    #ACTUALIZACION SECUENCIAL CHEQUE
                    #Banco.objects.filter(pk=movimiento.banco_id).update(secuencia=movimiento.numero_cheque + 1)
                    contador = request.POST["columnas_receta"]
                    print contador
                    i = 0
                    while int(i) <= int(contador):
                        i += 1
                        print('entro comoqw' + str(i))
                        if int(i) > int(contador):
                            print('entrosd')
                            break
                        else:
                            if 'id_kits' + str(i) in request.POST:
                                print 'entro fact'
                                tipo_mov=request.POST["tipo_kits"+str(i)]
                                if tipo_mov == "FA":
                                    idf=request.POST["id_kits"+str(i)]
                                    fact = DocumentoVenta.objects.get(id=idf)
                                    fact.pagado = True
                                    fact.movimiento_id = movimiento.id
                                    fact.save()
                                    abono = DocumentoAbonoVenta()
                                    abono.documento_venta_id = request.POST["id_kits"+str(i)]
                                    abono.movimiento_id = movimiento.id
                                    abono.abono = request.POST["abono_kits"+str(i)]
                                    abono.cantidad_anterior_abonada =request.POST["cantidad_kits"+str(i)]
                                    abono.diferencia = request.POST["diferencia_kits"+str(i)]
                                    abono.created_by = request.user.get_full_name()
                                    abono.updated_by = request.user.get_full_name()
                                    abono.created_at = now
                                    abono.updated_at = now
                                    abono.save()
                                else:

                                    abono = DocumentoAbonoVenta()
                                    abono.proforma_id = request.POST["id_kits"+str(i)]
                                    abono.movimiento_id = movimiento.id
                                    abono.abono = request.POST["abono_kits" + str(i)]
                                    abono.cantidad_anterior_abonada = request.POST["cantidad_kits" + str(i)]
                                    abono.diferencia = request.POST["diferencia_kits" + str(i)]
                                    abono.created_by = request.user.get_full_name()
                                    abono.updated_by = request.user.get_full_name()
                                    abono.created_at = now
                                    abono.updated_at = now
                                    abono.save()
                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        asiento = Asiento()
                        asiento.codigo_asiento = "B"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE CHEQUES POSFECHADOS - ' + movimiento.numero_comprobante
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        asiento.modulo ='Bancos-CHEQUES POSFECHADOS'
                        
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.created_by = request.user.get_full_name()
                        asiento.created_at = now
                        asiento.updated_by = request.user.get_full_name()
                        asiento.updated_at = now
                        
                        asiento.save()
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            print item_asiento['id_plancuenta']
                            print item_asiento['debe']
                            print item_asiento['haber']
                            print asiento.asiento_id
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.tipo=item_asiento['tipo']
                            asiento_detalle.subtipo=item_asiento['subtipo']
                            asiento_detalle.save()
                    # facturas = json.loads(request.POST['arreglo_facturas'])
                    # if len(facturas) > 0:
                    #     for item_factura in facturas:
                    #         if item_factura['check']:

            else:
                form_errors = form.errors
                print form.is_valid(), form.errors, type(form.errors)
        except Exception as e:
            print (e.message)

        return HttpResponseRedirect('/bancos/movimiento/cheques_posfechados')
@login_required()
def movimiento_cliente_cheques_posfechados(request):
    movimientos = Movimiento.objects.filter(tipo_anticipo=2).filter(proforma=False).filter(tipo_documento_id=11).order_by('-id')
    template = loader.get_template('movimientos/index_cheques_posfechados.html')
    context = RequestContext(request, {'movimientos': movimientos})
    return HttpResponse(template.render(context))

@login_required()
@csrf_exempt
def guardarMovimientoDescripcion(request):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        id = request.POST.get('id')
        print descripcion
        try:
            try:
                movimiento =Movimiento.objects.get(id=id)
            except Movimiento.DoesNotExist:
                movimiento = None
            
            
            if movimiento:
                movimiento.descripcion=descripcion.replace("\n", " ")
                movimiento.updated_by = request.user.get_full_name()
                movimiento.updated_at = now

                
                movimiento.save()
                asientos = json.loads(request.POST['arreglo_asientos'])
                print asientos
                if len(asientos) > 0:
                    for item_asiento in asientos:
                        print item_asiento
                        try:
                            asiento_detalle =AsientoDetalle.objects.get(detalle_id=item_asiento['detalle_id'])
                        except AsientoDetalle.DoesNotExist:
                            asiento_detalle = None
                        if asiento_detalle:
                            print "entro"
                            print item_asiento['detalle_id']
                            
                            asiento_detalle =AsientoDetalle.objects.get(detalle_id=item_asiento['detalle_id'])
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.save()
                
        except Exception as e:
            print (e.message)
        item = {
            'id': movimiento.id,
            'documento': movimiento.tipo_documento_id,
        }
        json_resultados = json.dumps(item)
        return HttpResponse(json_resultados, content_type="application/json")

            
def imprimir_cheque_actual(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    movimiento = Movimiento.objects.get(id=pk)
    paguese=movimiento.paguese_a
    beneficiario=paguese[0:50]
    html = loader.get_template('movimientos/imprimir_cheque_actual.html')
    context = RequestContext(request, {'movimiento': movimiento,'beneficiario': beneficiario})
    return HttpResponse(html.render(context))       


def imprimir_cheque_pdf(request, pk):
    movimiento = Movimiento.objects.get(id=pk)
    paguese=movimiento.paguese_a
    beneficiario=paguese[0:50]

    
    html1 = render_to_string('movimientos/imprimir_cheque_pdf.html', {'pagesize': 'A4', 'movimiento': movimiento,'beneficiario': beneficiario},
                             context_instance=RequestContext(request))
    return generar_pdf(html1)

@login_required()
def chequeProtestadoEliminarByPkView(request, pk):
    obj = ChequesProtestados.objects.get(id=pk)

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
                a.updated_by = request.user.get_full_name()
                a.updated_at = now
                a.save()
          
        try:
            movimiento_valor = Movimiento.objects.filter(id=obj.movimiento_valor_cheque_id)
        except Movimiento.DoesNotExist:
            movimiento_valor = None
        if movimiento_valor:
            for m in movimiento_valor:
                m.activo= False
                m.updated_by = request.user.get_full_name()
                m.updated_at = now
                m.save()
        try:
            movimiento_multa = Movimiento.objects.filter(id=obj.movimiento_multa_id)
        except Movimiento.DoesNotExist:
            movimiento_multa = None
        if movimiento_multa:
            for mm in movimiento_multa:
                mm.activo= False
                mm.updated_by = request.user.get_full_name()
                mm.updated_at = now
                mm.save()
       
                            

    return HttpResponseRedirect('/bancos/cheques_protestados/')



@login_required()
def edit_movimiento_proveedor_nota_credito_view(request,pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(proveedor = True)
    bancos = Banco.objects.filter(estado=True)
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    nota_credito=MovimientoNotaCredito.objects.get(movimiento_id=pk)
    cursor = connection.cursor()
    if movimiento.tipo_anticipo_id==1:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_compra f,documento_abono da where da.movimiento_id = ' + (
    pk) + ' and f.id=da.documento_compra_id;'
    else:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_venta f,documento_abono_venta da where da.movimiento_id = ' + (
            pk) + ' and f.id=da.documento_venta_id;'
    cursor.execute(query)
    facturas = cursor.fetchall()
    total_facturas=DocumentoAbono.objects.filter(movimiento_id=pk).aggregate(Sum('abono'))
    if total_facturas['abono__sum']:
        total_f=total_facturas['abono__sum']
    else:
        total_f=0
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None
    



    template = loader.get_template('movimientos/editar_nota_credito_proveedor.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos, 'nota_credito': nota_credito,'asientos': asientos,'detalle_asientos':detalle_asientos,
                                       'tipo_documentos': tipo_documentos, 'clientes': clientes, 'bancos': bancos, 'cuentas': cuentas,
                                       'proveedores': proveedores,'total_f':total_f})
    return HttpResponse(template.render(context))


@login_required()
def movimiento_edit_deposito_view(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(proveedor = True)
    bancos = Banco.objects.filter(estado=True)
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    facturas=DocumentoCompra.objects.filter(movimiento_id=pk)
    cursor = connection.cursor()
    if movimiento.tipo_anticipo_id==1:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_compra f,documento_abono da where da.movimiento_id = ' + (
    pk) + ' and f.id=da.documento_compra_id;'
    else:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_venta f,documento_abono_venta da where da.movimiento_id = ' + (
            pk) + ' and f.id=da.documento_venta_id;'
    cursor.execute(query)
    facturas = cursor.fetchall()
    total_facturas=DocumentoAbono.objects.filter(movimiento_id=pk).aggregate(Sum('abono'))
    if total_facturas['abono__sum']:
        total_f=total_facturas['abono__sum']
    else:
        total_f=0
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None



    template = loader.get_template('movimientos/edit_deposito.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos, 'facturas': facturas,'asientos': asientos,'detalle_asientos':detalle_asientos,
                                       'tipo_documentos': tipo_documentos, 'clientes': clientes, 'bancos': bancos, 'cuentas': cuentas,
                                       'proveedores': proveedores,'total_f':total_f})
    return HttpResponse(template.render(context))
@login_required()
def movimiento_update_deposito_view(request, pk):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():


            cleaned_data = form.cleaned_data
            movimiento = Movimiento.objects.get(pk=pk)
            movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
            movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
            movimiento.fecha_emision = cleaned_data.get('fecha_emision')
            movimiento.banco_id = int(cleaned_data.get('banco').id)
            if movimiento.tipo_anticipo_id == 2:
                movimiento.cliente_id = int(request.POST['persona_id'])
            else:
                movimiento.proveedor_id = int(request.POST['persona_id'])
            movimiento.paguese_a = cleaned_data.get('paguese_a')
            
            movimiento.descripcion = cleaned_data.get('descripcion')
            movimiento.updated_by = request.user.get_full_name()
            movimiento.updated_at = now
            
            movimiento.save()
            try:
                asiento = Asiento.objects.get(asiento_id=movimiento.asiento_id)
            except Asiento.DoesNotExist:
                asiento = None
            if asiento:
                asiento.fecha= movimiento.fecha_emision
                asiento.updated_by = request.user.get_full_name()
                asiento.updated_at = now
                asiento.save()
        return HttpResponseRedirect('/bancos/movimiento/deposito')


    

def imprimir_pdf_conciliaciones_view(request, pk):
    conciliacion = Conciliacion.objects.get(pk=pk)
    detalle = Movimiento.objects.filter(conciliacion_id=pk)
    cuentas_bancos = Banco.objects.filter(estado=True)
    id = conciliacion.cuenta_banco_id
    fecha = conciliacion.fecha_corte
    cursor = connection.cursor()
    
    try:
        bancos = Banco.objects.get(id=id)
        cuenta_id=bancos.cuenta_contable_id
            
    except Banco.DoesNotExist:
        bancos = None
        cuenta_id=0
        
    query = "select m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,m.conciliacion_id,da.asiento_id,sum(da.debe),sum(da.haber) from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON (co.id=m.conciliacion_id)  LEFT JOIN contabilidad_asientodetalle da  ON (da.asiento_id = m.asiento_id)  and da.cuenta_id="+str(cuenta_id)+" where   m.activo is True and m.tipo_documento_id!=5 and m.tipo_documento_id!=7 and m.tipo_documento_id!=8  and m.tipo_documento_id!=10 and m.tipo_documento_id!=11 and m.banco_id= "+str(id)+" and m.fecha_emision<='"+str(fecha)+"' and (co.fecha_corte>'"+str(fecha)+"' or  co.fecha_corte is null or co.id="+str(pk)+") group by m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,m.fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id order by m.fecha_emision" 
 
 
    print query
    cursor.execute(query)
    ro = cursor.fetchall()
    conciliacion_id=pk
    query2 = "select distinct  extract(month from m.fecha_emision) mes ,extract(year from m.fecha_emision) anio  from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON (co.id=m.conciliacion_id)  LEFT JOIN contabilidad_asientodetalle da  ON (da.asiento_id = m.asiento_id)  and da.cuenta_id="+str(cuenta_id)+" where   m.activo is True and m.tipo_documento_id!=5 and m.tipo_documento_id!=7 and m.tipo_documento_id!=8  and m.tipo_documento_id!=10 and m.tipo_documento_id!=11  and m.banco_id= "+str(id)+" and m.fecha_emision<='"+str(fecha)+"' and (co.fecha_corte>'"+str(fecha)+"' or  co.fecha_corte is null or co.id="+str(pk)+") group by m.fecha_emision order by anio,mes"
    print "QUERY 2 "
 
 
    print query2
    print "---------------------------------------"
    cursor.execute(query2)
    ro2 = cursor.fetchall()
    meses = ['', 'ENERO', 'FEBRERO','MARZO', 'ABRIL','MAYO', 'JUNIO','JULIO', 'AGOSTO', 'SEPTIEMBRE','OCTUBRE', 'NOVIEMBRE','DICIEMBRE']
    
       
    html_ch="<h4>***DETALLE DE CHEQUES GIRADOS Y NO EFECTIVIZADOS****</h4>"
    html_ch+='<table width="100%" id="movimientos_no_conciliados"><thead><tr><td>TP</td><td>Numero</td><td>Fecha</td><td>Referencia</td><td>Valor</td><td>Concepto</td></tr></thead>'
    html_ch+='<tbody>'
    total_no_conciliados=0
    total_ncb_nc=0
    total_cheques_nc=0
    total_de_nc=0
    total_nd_nc=0
    
    for r2 in ro2:
        if r2[0]:
            anio=int(r2[1])
            mes=int(r2[0])
            fecha_inicio_corte=str(anio)+"-"+str(mes)+"-01"
            if mes==1 or mes==3 or mes==5 or mes==7 or mes==8 or mes==10 or mes==12:
                fecha_corte=str(anio)+"-"+str(mes)+"-31"
            else:
                if mes==2:
                    fecha_corte=str(anio)+"-"+str(mes)+"-28"
                else:
                    fecha_corte=str(anio)+"-"+str(mes)+"-30"
                    
                
            query3 = "select m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,m.conciliacion_id,da.asiento_id,sum(da.debe),sum(da.haber),m.asociado_cheques_protestados,m.tipo_documento_id from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON (co.id=m.conciliacion_id)  LEFT JOIN contabilidad_asientodetalle da  ON (da.asiento_id = m.asiento_id)  and da.cuenta_id="+str(cuenta_id)+" where   m.activo is True and m.tipo_documento_id!=5 and m.tipo_documento_id!=7 and m.tipo_documento_id!=8  and m.tipo_documento_id!=10 and m.tipo_documento_id!=11 and m.banco_id= "+str(id)+" and m.fecha_emision>='"+str(fecha_inicio_corte)+"' and m.fecha_emision<='"+str(fecha_corte)+"' and (co.fecha_corte>'"+str(fecha)+"' or  co.fecha_corte is null or co.id>"+str(pk)+") group by m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,m.fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id order by m.fecha_emision"
            cursor.execute(query3)
            print "FECHA CORTE "+str(fecha_inicio_corte)+" FECCHA FIN "+str(fecha_corte)
            print query3
            print "-------------------------------------------"
            ro3 = cursor.fetchall()
            total_mes=0
            for r3 in ro3:
                #cheque
                if r3[12]==1:
                    monto=r3[11]
                    monto1="/v/"+str(r3[11])
                    
                #15 es el debe y 16 es el haber
                else:
                    
                    if r3[15]>0:
                        if r3[17]:
                            monto=r3[10]
                            monto1="/g/"+str(r3[10])
                        else:
                            monto=r3[15]
                            monto1="/f//"+str(r3[15])
                    else:
                        if r3[17]:
                            monto=r3[10]
                            monto1="/e///"+str(r3[10])
                            
                        else:
                            if r3[16]>0:
                                if r3[16]:
                                    monto=r3[16]
                                    monto1="/i////"+str(r3[16])
                                else:
                                    monto=0
                                    monto1="/n/////"+str(r3[16])
                            else:
                                monto=0
                                monto1="/h///////"+str(r3[16])
                                
                    
                if r3[5]:
                    r35=r3[5].encode('utf8')
                else:
                    r35=''
                
                if r3[6]:
                    r36=r3[6].encode('utf8')
                else:
                    r36=''
                
                if r3[2]:
                    r32=r3[2].encode('utf8')
                else:
                    r32=''
                
                #deposito
                html_ch+="<tr><td>"+str(r32)+"</td><td>"+str(r3[9])+"</td><td>"+str(r3[4])+"</td>"
                html_ch+="<td>"+str(r3[8])+"-"+str(r35)+"</td><td>"+str(monto)+"</td><td>"+str(r36)+"</td></tr>"
                if r3[12]==2 or r3[12]==4:
                    total_mes=float(total_mes)-float(monto)
                else:    
                    total_mes=float(total_mes)+float(monto)
                if r3[12]==1:
                    total_cheques_nc=total_cheques_nc+float(monto)
                if r3[12]==2:
                    total_nd_nc=total_nd_nc+float(monto)
                if r3[12]==4:
                    total_de_nc=total_de_nc+float(monto)
                if r3[12]==3:
                    total_ncb_nc=total_ncb_nc+float(monto)
                
            html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right'>TOTAL DE "+str(meses[mes])+"/"+str(anio)+"</td><td>"+str(total_mes)+"</td><td></td></tr>"
            html_ch+="<tr><td colspan='6' style='text-align:right'></td></tr>"
            total_no_conciliados=total_no_conciliados+total_mes
    html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right' >TOTAL DE NO CONCILIADOS</td><td>"+str(total_no_conciliados)+"</td><td></td></tr>"
    html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right' >TOTAL DE NO CONCILIADOS CHEQUES</td><td>"+str(total_cheques_nc)+"</td><td></td></tr>"
    html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right' >TOTAL DE NO CONCILIADOS DEPOSITOS</td><td>"+str(total_de_nc)+"</td><td></td></tr>"
    html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right' >TOTAL DE NO CONCILIADOS NOTAS DE CREDITO</td><td>"+str(total_ncb_nc)+"</td><td></td></tr>"
    html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right' >TOTAL DE NO CONCILIADOS NOTAS DE DEBITO</td><td>"+str(total_nd_nc)+"</td><td></td></tr>"
    html_ch+="</tbody>"
    html_ch+="</table>"
    
    
    
    html_ch+="<h4 style='display:block;page-break-before:always;'>***DETALLE DE MOVIMIENTOS CONCILIADOS****</h4>"
    html_ch+='<table width="100%" id="movimientos_conciliados"><thead><tr><td>TP</td><td>Numero</td><td>Fecha</td><td>Referencia</td><td>Valor</td><td>Concepto</td></tr></thead>'
    html_ch+='<tbody>'
    total_conciliados=0
    total_ncb=0
    total_cheques=0
    total_de=0
    total_nd=0
    for r2 in ro2:
        if r2[0]:
            anio=int(r2[1])
            mes=int(r2[0])
            
            fecha_inicio_corte=str(anio)+"-"+str(mes)+"-01"
            if mes==1 or mes==3 or mes==5 or mes==7 or mes==8 or mes==10 or mes==12:
                fecha_corte=str(anio)+"-"+str(mes)+"-31"
                
            else:
                if mes==2:
                    fecha_corte=str(anio)+"-"+str(mes)+"-28"
                else:
                    fecha_corte=str(anio)+"-"+str(mes)+"-30"
                    
                
            query4 = "select m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,m.conciliacion_id,da.asiento_id,sum(da.debe),sum(da.haber),m.asociado_cheques_protestados from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON (co.id=m.conciliacion_id)  LEFT JOIN contabilidad_asientodetalle da  ON (da.asiento_id = m.asiento_id)  and da.cuenta_id="+str(cuenta_id)+" where   m.activo is True and m.tipo_documento_id!=5 and m.tipo_documento_id!=7 and m.tipo_documento_id!=8  and m.tipo_documento_id!=10 and m.tipo_documento_id!=11 and m.banco_id= "+str(id)+" and m.fecha_emision>='"+str(fecha_inicio_corte)+"' and m.fecha_emision<='"+str(fecha_corte)+"' and (co.id="+str(pk)+") group by m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,m.fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id order by m.fecha_emision"
            cursor.execute(query4)
            ro4 = cursor.fetchall()
            total_mes=0
            for r4 in ro4:
                
                if r4[12]==1:
                    monto=r4[11]
                    monto1='-'+str(monto)
                #15 es el debe y 16 es el haber
                else:
                    if r4[17] :
                         monto=r4[10]
                         monto1='/'+str(monto)
                    else:
                        
                        if r4[15]>0:
                            monto=r4[15]
                            monto1='//'+str(r4[15])
                        else:
                            monto=r4[16]
                            monto1='///'+str(monto)
                if r4[2]:
                    r42=r4[2].encode('utf8')
                else:
                    r42=''
                
                if r4[5]:
                    r45=r4[5].encode('utf8')
                else:
                    r45=''
                
                if r4[6]:
                    r46=r4[6].encode('utf8')
                else:
                    r46=''
                html_ch+="<tr><td>"+str(r42)+"</td><td>"+str(r4[9])+"</td><td>"+str(r4[4])+"</td><td>"+str(r4[8])+"-"+str(r45)+"</td><td>"+str(r4[10])+"</td><td>"+str(r46)+"</td></tr>"
                if r4[12] ==2 or r4[12] == 4:
                    total_mes=float(total_mes)-float(monto)
                else:
                    total_mes=float(total_mes)+float(monto)
                
                if r4[12]==1:
                    total_cheques=total_cheques+float(monto)
                if r4[12]==2:
                    total_nd=total_nd+float(monto)
                if r4[12]==4:
                    total_de=total_de+float(monto)
                if r4[12]==3:
                    total_ncb=total_ncb+float(monto)
                    
            html_ch+="<tr><td colspan='4' style='text-align:right'>TOTAL DE "+str(meses[mes])+"/"+str(anio)+"</td><td>"+str(total_mes)+"</td><td></td></tr>"
            html_ch+="<tr><td colspan='6' style='text-align:right'></td></tr>"
            total_conciliados=total_conciliados+total_mes
    html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right'>TOTAL DE CONCILIADOS</td><td>"+str(total_conciliados)+"</td><td></td></tr>"
    html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right'>TOTAL DE CONCILIADOS CHEQUES</td><td>"+str(total_cheques)+"</td><td></td></tr>"
    html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right'>TOTAL DE CONCILIADOS DEPOSITOS</td><td>"+str(total_de)+"</td><td></td></tr>"
    html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right'>TOTAL DE CONCILIADOS NOTAS DE CREDITO </td><td>"+str(total_ncb)+"</td><td></td></tr>"
    html_ch+="<tr class='resultado'><td colspan='4' style='text-align:right'>TOTAL DE CONCILIADOS NOTAS DE DEBITO</td><td>"+str(total_nd)+"</td><td></td></tr>"
    html_ch+="</tbody>"
    html_ch+="</table>"
    
    user=request.user.get_full_name()
    html = loader.get_template('conciliaciones/conciliaciones_imprimir.html')
    context = RequestContext(request, {'conciliacion': conciliacion, 'cuentas_bancos': cuentas_bancos,'detalle': detalle,'detalle_conciliaciones':ro,'conciliacion_id':conciliacion_id,'fecha':now,'user': user,'html_ch': html_ch})
    return HttpResponse(html.render(context))  



@login_required()
def movimientoNotaCreditoClienteEliminarByPkView(request, pk):
    obj = Movimiento.objects.get(id=pk)

    if obj:
        obj.activo = False
        obj.updated_by = request.user.get_full_name()
        obj.updated_at = now
        obj.save()
        print "entro a mov"
        
        try:
            asiento = Asiento.objects.filter(asiento_id=obj.asiento_id)
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            for a in asiento:
                a.anulado= True
                a.updated_by = request.user.get_full_name()
                a.updated_at = now
                a.save()
        
        
   
                
                
        try:
            nota_credito = MovimientoNotaCredito.objects.filter(movimiento_id=obj.id)
        except MovimientoNotaCredito.DoesNotExist:
            nota_credito = None
            
        print obj.id
        if nota_credito:
            for nc in nota_credito:
                nc.anulado= True
                nc.save()
                print "id:"
                print nc.id
        
                try:
                    dc = DocumentoCompra.objects.filter(id=nc.documento_compra_id)
                except DocumentoCompra.DoesNotExist:
                    dc = None
                if dc:
                    for d in dc:
                        d.nota_credito= False
                        d.save()
                try:
                    dv = DocumentoVenta.objects.filter(id=nc.documento_venta_id)
                except DocumentoVenta.DoesNotExist:
                    dv = None
                if dv:
                    print "entro a dv"
                    for d1 in dv:
                        d1.nota_credito= False
                        d1.save()
                            

    return HttpResponseRedirect('/bancos/movimiento/nc/bancaria/cliente')


@login_required()
def conciliaciones_consultar_view(request, pk):
    conciliacion = Conciliacion.objects.get(pk=pk)
    detalle = Movimiento.objects.filter(conciliacion_id=pk)
    cuentas_bancos = Banco.objects.filter(estado=True)
    id = conciliacion.cuenta_banco_id
    fecha = conciliacion.fecha_corte
    cursor = connection.cursor()
    
    #query = "select m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,m.conciliacion_id from movimiento m, tipo_documento td where td.id=m.tipo_documento_id and m.activo is True and m.banco_id= " + str(id) + " and m.fecha_emision<='"+str(fecha)+"' and (m.conciliacion_id=" + str(pk) + " or m.conciliacion_id is NULL)   order by m.fecha_emision";
    try:
        bancos = Banco.objects.get(id=id)
        cuenta_id=bancos.cuenta_contable_id
            
    except Banco.DoesNotExist:
        bancos = None
        cuenta_id=0
        
    query = "select m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,m.conciliacion_id,da.asiento_id,sum(da.debe),sum(da.haber),m.asociado_cheques_protestados from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON (co.id=m.conciliacion_id)  LEFT JOIN contabilidad_asientodetalle da  ON (da.asiento_id = m.asiento_id)  and da.cuenta_id="+str(cuenta_id)+" where   m.activo is True and m.tipo_documento_id!=5 and m.tipo_documento_id!=7 and m.tipo_documento_id!=8  and m.tipo_documento_id!=10 and m.tipo_documento_id!=11 and m.banco_id= "+str(id)+" and m.fecha_emision<='"+str(fecha)+"' and (co.fecha_corte>'"+str(fecha)+"' or  co.fecha_corte is null or co.id="+str(pk)+") group by m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,m.fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id order by m.fecha_emision" 
 
 
    print query
    cursor.execute(query)
    ro = cursor.fetchall()
    conciliacion_id=pk
    
    template = loader.get_template('conciliaciones/consultar.html')
    context = RequestContext(request, {'conciliacion': conciliacion, 'cuentas_bancos': cuentas_bancos,'detalle': detalle,'detalle_conciliaciones':ro,'conciliacion_id':conciliacion_id})
    return HttpResponse(template.render(context))



@login_required()
def consultar_ch_protestados_conciliar(request):
    if request.method == "POST" and request.is_ajax:
        id = request.POST['id']
        fecha = request.POST['fecha']
        #conciliacion_ultima=Conciliacion.objects.latest('id')
        try:
            bancos = Banco.objects.get(id=id)
            cuenta_id=bancos.cuenta_contable_id
            print "entro a banco"
            print bancos.id
            print "holl"
            print bancos.cuenta_contable_id
        except Banco.DoesNotExist:
            bancos = None
            cuenta_id=0
        cursor = connection.cursor()
        #query = "select m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id,sum(da.debe),sum(da.haber),m.conciliacion_id, to_char(co.fecha_corte, \'DD/MM/YYYY\') as fecha_corte from movimiento m LEFT JOIN tipo_documento td  ON (td.id=m.tipo_documento_id) LEFT JOIN conciliacion co  ON (co.id = m.conciliacion_id)  LEFT JOIN contabilidad_asientodetalle da  ON (da.asiento_id = m.asiento_id)  and da.cuenta_id="+str(cuenta_id)+" where   m.activo is True and m.banco_id= "+str(id)+" and m.fecha_emision<='"+str(fecha)+"' and (m.conciliacion_id is null or co.fecha_corte>='"+str(fecha)+"') group by m.id,m.tipo_anticipo_id,td.descripcion,m.banco_id,m.fecha_emision,m.paguese_a,m.descripcion, m.activo,m.numero_comprobante,m.numero_cheque,m.monto,m.monto_cheque,td.id,da.asiento_id,co.fecha_corte,m.conciliacion_id order by m.fecha_emision"
        query = "select ch.id,m.id,ch.descripcion,ch.banco_id,to_char(ch.fecha_emision, \'DD/MM/YYYY\') as fecha_emision,m.paguese_a,m.descripcion, ch.anulado,ch.comprobante_debito,ch.numero_cheque,ch.valor_cheque,ch.valor_multa,ch.cliente_id,da.asiento_id,sum(da.debe),sum(da.haber),ch.conciliacion_id, to_char(co.fecha_corte, \'DD/MM/YYYY\') as fecha_corte from cheques_protestados ch LEFT JOIN movimiento m  ON (m.id=ch.movimiento_id) LEFT JOIN conciliacion co  ON (co.id = ch.conciliacion_id) LEFT JOIN contabilidad_asientodetalle da  ON (da.asiento_id = ch.asiento_id)  and da.cuenta_id="+str(cuenta_id)+" where   ch.anulado is not  True and ch.banco_id= "+str(id)+" and ch.fecha_emision<='"+str(fecha)+"' and (co.fecha_corte>'"+str(fecha)+"' or co.fecha_corte is null)   group by ch.id,m.id,ch.descripcion,ch.banco_id,ch.fecha_emision,m.paguese_a,m.descripcion, ch.anulado,ch.comprobante_debito,ch.numero_cheque,ch.valor_cheque,ch.valor_multa,ch.cliente_id,da.asiento_id,ch.conciliacion_id, co.fecha_corte"
        print query
 
        cursor.execute(query)
        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)
    else:
        raise Http404
    return HttpResponse(json_resultados, content_type="application/json")



@login_required()
def documento_abono_cheque_list_view(request):
    cursor = connection.cursor()
    query=" select m.id,ch.id,m.fecha_emision,m.tipo_anticipo_id,m.numero_comprobante,c.nombre_cliente,ta.descripcion,td.descripcion,m.numero_cheque,m.descripcion,b.nombre,m.monto,m.activo,m.conciliacion_id,ch.id,bp.id from documento_abono_cheque dch left join cheques_protestados ch on ch.id=dch.cheques_protestados_id left join movimiento m on m.id=dch.movimiento_id left join banco b on b.id=m.banco_id left join tipo_documento td on td.id=m.tipo_documento_id left join cliente c on c.id_cliente=dch.cliente_id left join tipo_anticipo ta on ta.id=m.tipo_anticipo_id left join bloqueo_periodo bp on  date_part('year',bp.fecha)=EXTRACT(YEAR FROM m.fecha_emision) and date_part('month',bp.fecha)=EXTRACT(MONTH from m.fecha_emision)"
    cursor.execute(query)
    ro = cursor.fetchall()
    template = loader.get_template('chequesprotestados/index_abono_cheques.html')
    context = RequestContext(request, {'cheques_protestados': ro})
    return HttpResponse(template.render(context))


@login_required()
def movimiento_nuevo_abono_cheque_view(request):
    clientes = Cliente.objects.all()
    bancos = Banco.objects.filter(estado=True)
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(cliente=True).exclude(id=9).exclude(id=3)
    tarjeta_credito = TarjetaCredito.objects.all()
    puntos= PuntosVenta.objects.order_by('id')
    centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
    centros= CentroCosto.objects.all()

    form = MovimientoForm
    template = loader.get_template('chequesprotestados/abono_cliente.html')
    context = RequestContext(request, {'form': form, 'clientes': clientes, 'tipo_anticipos': tipo_anticipos, 'puntos': puntos,'centros_defecto':centros_defecto,
                                       'centros':centros,
                                       'tipo_documentos': tipo_documentos, 'bancos': bancos, 'cuentas': cuentas,'tarjeta_credito':tarjeta_credito,
                                       })
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic()
def movimiento_crear_abono_cheque_view(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():

                with transaction.atomic():
                    print "ingresa a crear el movimiento un formulario valido43"
                    cleaned_data = form.cleaned_data
                    movimiento = Movimiento()
                    movimiento.tipo_anticipo_id = int(cleaned_data.get('tipo_anticipo').id)
                    movimiento.tipo_documento_id = int(cleaned_data.get('tipo_documento').id)
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    movimiento.banco_id = int(cleaned_data.get('banco').id)
                    if movimiento.tipo_anticipo_id == 2:
                        movimiento.cliente_id = int(request.POST['persona_id'])
                    else:
                        movimiento.proveedor_id = int(request.POST['persona_id'])
                    movimiento.paguese_a = cleaned_data.get('paguese_a')
                    movimiento.numero_cheque = cleaned_data.get('numero_cheque')
                    movimiento.fecha_cheque = cleaned_data.get('fecha_cheque')
                    movimiento.descripcion = cleaned_data.get('descripcion')
                    movimiento.monto = cleaned_data.get('monto')
                    if movimiento.tipo_documento_id== 5:
                        movimiento.tarjeta_credito_id =  request.POST['tarjeta_credito']
                        movimiento.puntos_venta_id = request.POST['punto_venta']
                    movimiento.numero_lote = cleaned_data.get('numero_lote')
                    movimiento.save()
                    movimiento.numero_comprobante = 'M'+str(now.year)+'000'+str(movimiento.id)
                    movimiento.save()
                    try:
                        secuencial = Secuenciales.objects.get(modulo='documento_ingreso_movimiento')
                        movimiento.numero_ingreso=secuencial.secuencial
                        movimiento.save()
                        secuencial.secuencial=secuencial.secuencial+1
                        secuencial.created_by = request.user.get_full_name()
                        secuencial.updated_by = request.user.get_full_name()
                        secuencial.created_at = now
                        secuencial.updated_at = now
                        secuencial.save()
                    except Secuenciales.DoesNotExist:
                        secuencial = None
                    

                    
                    #ACTUALIZACION SECUENCIAL CHEQUE
                    #Banco.objects.filter(pk=movimiento.banco_id).update(secuencia=movimiento.numero_cheque + 1)
                    contador = request.POST["columnas_receta"]
                    print "entro a cheques protestadis"
                    print contador
                    i = 0
                    while int(i) <= int(contador):
                        i += 1
                        if int(i) > int(contador):
                            break
                        else:
                            if 'id_kits' + str(i) in request.POST:
                                
                                idf=request.POST["id_kits"+str(i)]
                                print idf
                                
                                abono = DocumentoAbonoCheque()
                                abono.cheques_protestados_id = request.POST["id_kits"+str(i)]
                                abono.movimiento_id = movimiento.id
                                abono.cliente_id=movimiento.cliente_id
                                abono.abono = request.POST["abono_kits"+str(i)]
                                abono.created_by = request.user.get_full_name()
                                abono.updated_by = request.user.get_full_name()
                                abono.created_at = now
                                abono.updated_at = now
                                abono.save()
                                    
                                
                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        asiento = Asiento()
                        asiento.codigo_asiento = "B"+str(now.year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE BANCOS - ' + movimiento.numero_comprobante
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        asiento.modulo='Bancos-DEPOSITO CHEQUES PROTESTADOS'
                        
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.save()
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                       
                        for item_asiento in asientos:
                            
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.tipo=item_asiento['tipo']
                            asiento_detalle.subtipo=item_asiento['subtipo']
                            asiento_detalle.centro_costo_id = item_asiento['centro']
                            asiento_detalle.save()
                    

            else:
                form_errors = form.errors
                print form.is_valid(), form.errors, type(form.errors)
        except Exception as e:
            print (e.message)

        return HttpResponseRedirect('/bancos/cheques_protestados/abono')



@login_required()
def consultar_abono_cheques_protestados(request):
    if request.method == "POST":

        fila = request.POST['fila']
        persona= request.POST['persona']
        id=persona

        cursor = connection.cursor()
        query='select dv.id, dv.fecha_emision, dv.numero_cheque, dv.valor_cheque, dv.valor_multa,dv.valor_cheque+dv.valor_multa,SUM(da.abono),dv.descripcion,dv.comprobante_debito from cheques_protestados dv LEFT JOIN documento_abono_cheque da  ON (da.cheques_protestados_id = dv.id) where dv.cliente_id =' + (id) + ' and  da.anulado is not True and  dv.anulado is not True GROUP BY dv.id, dv.fecha_emision, dv.numero_cheque, dv.valor_cheque, dv.valor_multa,dv.descripcion,dv.comprobante_debito ;'
        print(query)
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('chequesprotestados/mostrar_cheques_abono.html',
                                  {'ro': ro,  'persona': persona,'fila': fila,},RequestContext(request))

    else:
        fila = request.POST['fila']
        persona= request.POST['persona']
        id=persona

        cursor = connection.cursor()
        query='select dv.id, dv.fecha_emision, dv.numero_cheque, dv.valor_cheque, dv.valor_multa,dv.valor_cheque+dv.valor_multa,SUM(da.abono),dv.descripcion,dv.comprobante_debito from cheques_protestados dv LEFT JOIN documento_abono_cheque da  ON (da.cheques_protestados_id = dv.id) where dv.cliente_id =' + (id) + ' and  da.anulado is  not True GROUP BY dv.id, dv.fecha_emision, dv.numero_cheque, dv.valor_cheque, dv.valor_multa,dv.descripcion,dv.comprobante_debito ;'
        print(query)
        cursor.execute(query)
        ro = cursor.fetchall()
        
        return render_to_response('chequesprotestados/mostrar_cheques_abono.html',
                                  {'ro': ro,  'persona': persona,'fila': fila},
                                   RequestContext(request))
    
    

@login_required()
def movimientoEliminarAbonoChequeByPkView(request, pk):
    obj = Movimiento.objects.get(id=pk)

    if obj:
        obj.activo = False
        obj.save()
        try:
            abonos = DocumentoAbonoCheque.objects.filter(movimiento_id=obj.id)
        except DocumentoAbonoCheque.DoesNotExist:
            abonos = None
        if abonos:
            for a in abonos:
                a.anulado= True
                a.activo=False
                a.save()
        try:
            asiento = Asiento.objects.filter(asiento_id=obj.asiento_id)
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            for a in asiento:
                a.anulado= True
                a.save()

    return HttpResponseRedirect('/bancos/cheques_protestados/abono/')



@login_required()
def debito_consultar_view(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(proveedor = True)
    bancos = Banco.objects.filter(estado=True)
    clientes = Cliente.objects.all()
    proveedores = Proveedor.objects.all()
    cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    facturas=DocumentoCompra.objects.filter(movimiento_id=pk)
    cursor = connection.cursor()
    if movimiento.tipo_anticipo_id==1 or movimiento.tipo_anticipo_id==3:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_compra f,documento_abono da where da.movimiento_id = ' + (
    pk) + ' and f.id=da.documento_compra_id;'
    else:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_venta f,documento_abono_venta da where da.movimiento_id = ' + (
            pk) + ' and f.id=da.documento_venta_id;'
        
    cursor.execute(query)
    facturas = cursor.fetchall()
    total_facturas=DocumentoAbono.objects.filter(movimiento_id=pk).aggregate(Sum('abono'))
    if total_facturas['abono__sum']:
        total_f=total_facturas['abono__sum']
    else:
        total_f=0
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None



    template = loader.get_template('movimientos/consultar_debito.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos, 'facturas': facturas,'asientos': asientos,'detalle_asientos':detalle_asientos,
                                       'tipo_documentos': tipo_documentos, 'clientes': clientes, 'bancos': bancos, 'cuentas': cuentas,
                                       'proveedores': proveedores,'total_f':total_f})
    return HttpResponse(template.render(context))



@login_required()
def proforma_factura_list_view(request):
    cursor = connection.cursor()
    query="select distinct pr.id, pr.abreviatura_codigo, pr.codigo,pr.fecha,c.nombre_cliente,p.nombre,pr.total,periodos from proforma pr,documento_abono_venta da,cliente c,puntos_venta p,documento_venta dv,(SELECT b.id as periodos,pb.id FROM proforma  pb LEFT JOIN bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM pb.fecha) and date_part('month',b.fecha)=EXTRACT(MONTH from pb.fecha)) G where G.id= pr.id and da.proforma_id=pr.id and dv.proforma_id=pr.id and da.documento_venta_id is NULL and c.id_cliente=pr.cliente_id and p.id=pr.puntos_venta_id and da.anulado is not True order by pr.id"
    cursor.execute(query)
    ro = cursor.fetchall()
    template = loader.get_template('reportes/proformas_facturas_abonos.html')
    context = RequestContext(request, {'proformas': ro})
    return HttpResponse(template.render(context))



@login_required()
def proforma_factura_corregir_abono_view(request, pk):
    abonos = DocumentoAbonoVenta.objects.filter(proforma_id=pk).filter(documento_venta_id__isnull=True).filter(anulado=False)
    facturas=DocumentoVenta.objects.filter(proforma_id=pk).filter(activo=True)
    template = loader.get_template('reportes/proformas_facturas_reemplazar_abonos.html')
    context = RequestContext(request, {'abonos': abonos, 'facturas': facturas, 'proforma_id': pk})
    return HttpResponse(template.render(context))

@login_required()
def MostrarProformasFacturasAbonoView(request):
    if request.method == 'POST':
        id = request.POST["id"]
        proforma_id = request.POST["proforma_id"]
        cursor = connection.cursor()
        #query = 'select dv.id, to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva, dv.valor_iva, dv.total,SUM(da.abono),dv.punto_emision,dr.id,sum(drd.valor_retenido) as retencion,dv.total-sum(drd.valor_retenido) as final,dv.total-sum(drd.valor_retenido)-SUM(da.abono),c.nombre_cliente from documento_venta dv LEFT JOIN documento_retencion_venta dr  ON (dr.documento_venta_id = dv.id ) LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id LEFT JOIN documento_retencion_detalle_venta drd  ON (drd.documento_retencion_venta_id = dr.id ) LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = dv.id) and da.anulado is not True where dv.activo is True  and dv.proforma_id = ' + (proforma_id) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento, dv.base_iva, dv.valor_iva, dv.total,dr.id,c.nombre_cliente;'
        #query=' SELECT distinct dv.id,to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva, dv.valor_iva, dv.total,abono,dv.punto_emision,rete_id,retencion,dv.total-retencion as final,dv.total-retencion-abono,cliente FROM documento_venta dv,( SELECT d.id,sum(da.abono) as abono FROM documento_venta d LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = d.id) and da.anulado is not True where d.proforma_id=' + (proforma_id) + '  GROUP BY d.id) A, (SELECT  d.id,dr.id as rete_id,sum (drd.valor_retenido) as retencion from documento_venta d LEFT JOIN documento_retencion_venta dr  ON (dr.documento_venta_id = d.id ) LEFT JOIN documento_retencion_detalle_venta drd  ON (drd.documento_retencion_venta_id = dr.id ) where d.proforma_id=' + (proforma_id) + ' and dr.anulado is not True GROUP BY d.id,dr.id) B ,(SELECT  d.id,c.nombre_cliente as cliente from documento_venta d LEFT JOIN cliente c ON c.id_cliente=d.cliente_id where d.proforma_id=' + (proforma_id) + ' )C where dv.activo is True  and dv.proforma_id =' + (proforma_id)
        query='SELECT dv.id,to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva, dv.valor_iva,dv.total,abono,dv.punto_emision,dvr.id,dvr.retenciones,dv.total-dvr.retenciones as final,dv.total-dvr.retenciones-abono,c.nombre_cliente FROM documento_venta dv left join documento_abono_venta da on da.documento_venta_id = dv.id and da.anulado is not True left join documento_venta_retenciones dvr on dvr.documento_venta_id = dv.id  left join cliente c   ON c.id_cliente=dv.cliente_id where dv.activo is True  and dv.proforma_id =' + str(proforma_id)
        print query
        cursor.execute(query)
        ro = cursor.fetchall()
        facturas=DocumentoVenta.objects.filter(proforma_id=proforma_id).filter(activo=True)
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
        centros = CentroCosto.objects.all()
        abonos = DocumentoAbonoVenta.objects.get(id=id)

        

        return render_to_response('reportes/mostrar_proformas_facturas_abonos.html',
                                  {'facturas': ro, 'abonos': abonos,'proforma_id':proforma_id,'centros_defecto':centros_defecto,'centros':centros}, RequestContext(request))


    else:
        id = request.POST["id"]
        proforma_id = request.POST["proforma_id"]
        facturas=DocumentoVenta.objects.filter(proforma_id=proforma_id).filter(activo=True)
        abonos = DocumentoAbonoVenta.objects.get(id=id)
        

        return render_to_response('reportes/mostrar_proformas_facturas_abonos.html',
                                  {'facturas': facturas, 'abonos': abonos,'proforma_id':proforma_id}, RequestContext(request))



@login_required()
@csrf_exempt
def guardarInversionAbonoProformaFactura(request):
    if request.method == 'POST':
        contador = request.POST["columnas_receta"]
        proforma_id = request.POST["proforma_id"]
        abono_id = request.POST["id"]
        monto = request.POST["id_montoa"]
        fecha=request.POST["fecha_abono"]
        try:
            mov = DocumentoAbonoVenta.objects.get(id=abono_id)
        except DocumentoAbonoVenta.DoesNotExist:
            mov = None
       
        i = 0
        html = "Guardado con exito"
        
        
        
        asientos = json.loads(request.POST['arreglo_asientos'])
        if len(asientos) > 0:
            codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
            secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
            print 'secuencial = %s' % (codigo_asiento)
            asiento = Asiento()
            asiento.codigo_asiento = "ADC"+str(now.year)+"00"+str(codigo_asiento)
            asiento.fecha = fecha
            asiento.glosa = 'MOVIMIENTO MODULO DE AJUSTES DE DE DEP. CLIENTES PROFORMAS-FACTURA- ' + mov.movimiento.numero_comprobante
            asiento.gasto_no_deducible = False
            asiento.secuencia_asiento = codigo_asiento
            asiento.modulo ='Bancos-AJUSTES DE DEP. CLIENTES PROFORMAS-FACTURA'
            total_debe=request.POST['total_debe']
            total_haber=request.POST['total_haber']
            asiento.total_debe = total_debe
            asiento.total_haber = total_haber
            asiento.save()
            
            Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
            
            ajuste = AjusteFacturaAbonoProforma()
            ajuste.proforma_id=proforma_id
            ajuste.fecha=fecha
            ajuste.movimiento_id=mov.movimiento_id
            ajuste.asiento_id=asiento.asiento_id
            ajuste.total=monto
            ajuste.created_by = request.user.get_full_name()
            ajuste.updated_by = request.user.get_full_name()
            ajuste.created_at = now
            ajuste.updated_at = now
            ajuste.save()
           
            for item_asiento in asientos:
                asiento_detalle = AsientoDetalle()
                asiento_detalle.asiento_id = asiento.asiento_id
                asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                asiento_detalle.debe = item_asiento['debe']
                asiento_detalle.haber = item_asiento['haber']
                asiento_detalle.concepto = item_asiento['concepto']
                asiento_detalle.tipo=item_asiento['tipo']
                asiento_detalle.centro_costo_id = item_asiento['centro']
                asiento_detalle.save()
                            
                        
                        
        while int(i) <= int(contador):
            i += 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'factura_kits' + str(i) in request.POST:
                    abono=request.POST["abono_kits" + str(i)]
                    if abono:
                        if abono>0:
                            abono_n = DocumentoAbonoVenta()
                            abono_n.documento_venta_id = request.POST["factura_kits" + str(i)]
                            if mov:
                                abono_n.movimiento_id = mov.movimiento.id
                            abono_n.abono = abono
                            abono_n.created_by = request.user.get_full_name()
                            abono_n.updated_by = request.user.get_full_name()
                            abono_n.created_at = now
                            abono_n.updated_at = now
                            abono_n.ajuste_factura_abono_proforma=ajuste
                            abono_n.save()
                        

               
        if mov:
            total=float(mov.abono)-float(monto)
            if total>0:
                mov.abono=total
                if mov.abono_inicial:
                    if mov.abono_inicial<0:
                        mov.abono_inicial=mov.abono
                else:
                    mov.abono_inicial=mov.abono
                        
                mov.save()
            else:
                mov.anulado=True
                if mov.abono_inicial:
                    if mov.abono_inicial<0:
                        mov.abono_inicial=mov.abono
                else:
                    mov.abono_inicial=mov.abono
                mov.ajuste_factura_abono_proforma=ajuste
                mov.save()
                   

        abonos = DocumentoAbonoVenta.objects.filter(proforma_id=proforma_id).filter(documento_venta_id__isnull=True).filter(anulado=False)
        facturas=DocumentoVenta.objects.filter(proforma_id=proforma_id).filter(activo=True)
        template = loader.get_template('reportes/proformas_facturas_reemplazar_abonos.html')
        context = RequestContext(request, {'abonos': abonos, 'facturas': facturas, 'proforma_id': proforma_id})
        #return HttpResponse(template.render(context))
        item = {
                'id': ajuste.id,
                'documento': asiento.asiento_id,
            }
        json_resultados = json.dumps(item)
   
        return HttpResponse(json_resultados, content_type="application/json")
    else:
        raise Http404


@login_required()
def consultar_actual_factura_proforma(request):
    if request.method == "POST":

        tipo = request.POST['tipo']
        fila = request.POST['fila']
        persona= request.POST['persona']

        cursor = connection.cursor()
        print('entro como tipo' + str(tipo))
        if tipo == 'PR':
            #query='select distinct dv.id, to_char(dv.fecha,  \'DD/MM/YYYY\') as fecha, dv.abreviatura_codigo,dv.codigo, dv.iva,dv.porcentaje_iva,dv.total,A.abono,pv.nombre as punto , dv.puntos_venta_id,v.nombre as vendedor,F.factura from proforma dv,(select proforma_id,sum(f.total) as factura from documento_venta f  where  f.activo is True group by f.proforma_id)F,(select proforma_id,sum(da.abono) as abono  from documento_abono_venta da   where  da.documento_venta_id is NULL and da.anulado IS NOT True group by da.proforma_id)A,puntos_venta pv, vendedor v where  dv.aprobada=True and dv.anulada is not  True and  dv.cliente_id = ' + (persona) + ' and F.proforma_id = dv.id and A.proforma_id = dv.id and dv.vendedor_id= v.id and pv.id=dv.puntos_venta_id'
            query='select distinct dv.id,to_char(dv.fecha, \'DD/MM/YYYY\') as fecha_emision, dv.abreviatura_codigo,dv.codigo, dv.iva,dv.porcentaje_iva,dv.total,sum(da.abono),pv.nombre as punto ,dv.puntos_venta_id,v.nombre as vendedor,sum(f.total),(SELECT SUM(n.total) as total FROM movimiento_nota_credito n where 1=1 and n.proforma_id = dv.id and n.anulado is not True) C from proforma dv left join puntos_venta pv on pv.id=dv.puntos_venta_id left join vendedor v on v.id=dv.vendedor_id left join documento_venta f on f.proforma_id=dv.id and f.activo is True left join documento_abono_venta da on da.proforma_id=dv.id and da.anulado IS NOT True where dv.aprobada=True and dv.anulada is not True and  dv.cliente_id = ' + (persona) + ' group by dv.id,dv.fecha, dv.abreviatura_codigo,dv.codigo, dv.iva,dv.porcentaje_iva,dv.total,pv.nombre,dv.puntos_venta_id,v.nombre'
        else:
            #query = 'select dv.id, to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva, dv.valor_iva, dv.total,SUM(da.abono),dv.punto_emision from documento_venta dv LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = dv.id) and da.anulado is not True where dv.activo is True and dv.nota_credito is not True and dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento, dv.base_iva, dv.valor_iva, dv.total;'
            #query = 'select dv.id, to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva, dv.valor_iva, dv.total,SUM(da.abono),dv.punto_emision,dr.id,sum(drd.valor_retenido) as retencion,dv.total-sum(drd.valor_retenido) from documento_venta dv LEFT JOIN documento_retencion_venta dr  ON (dr.documento_venta_id = dv.id ) LEFT JOIN documento_retencion_detalle_venta drd  ON (drd.documento_retencion_venta_id = dr.id ) LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = dv.id or da.proforma_id=dv.proforma_id) and da.anulado is not True where dv.activo is True  and dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento, dv.base_iva, dv.valor_iva, dv.total,dr.id;'
            query='select dv.id, to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva,dv.valor_iva, dv.total,(SELECT SUM(abono) as abonos FROM documento_abono_venta da where 1=1 and (da.documento_venta_id = dv.id) and da.anulado is not True) B ,dv.punto_emision,dr.id,retenciones,dv.total-retenciones,(SELECT SUM(n.total) as total FROM movimiento_nota_credito n where 1=1 and n.documento_venta_id = dv.id and n.anulado is not True) C from documento_venta dv LEFT JOIN documento_venta_retenciones dr ON dr.documento_venta_id=dv.id where dv.activo is True and dv.cliente_id  = ' + (persona) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento, dv.base_iva, dv.valor_iva, dv.total,dr.id,retenciones'
        print query
    
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('movimientos/mostrar_facturas_proformas.html',
                                  {'ro': ro, 'tipo': tipo, 'persona': persona,'fila': fila},RequestContext(request))
    else:
        tipo = request.POST['tipo']
        fila = request.POST['fila']
        persona = request.POST['persona']
        print('entro como tipo' + str(tipo))

        cursor = connection.cursor()
        if tipo == 'PR':
            #query = 'select dv.id, to_char(dv.fecha, \'DD/MM/YYYY\') as fecha, dv.abreviatura_codigo,dv.codigo, dv.iva,dv.porcentaje_iva, dv.total,SUM(da.abono),pv.nombre as punto , dv.puntos_venta_id,v.nombre as vendedor from proforma dv INNER JOIN  puntos_venta pv ON (dv.puntos_venta_id= pv.id) INNER JOIN  vendedor v ON (dv.vendedor_id= v.id) LEFT JOIN documento_abono_venta da  ON (da.proforma_id = dv.id)  and da.documento_venta_id is NULL and da.anulado IS NOT True where  dv.aprobada=True and dv.anulada!= True and v.id=dv.vendedor_id and pv.id=dv.puntos_venta_id and  dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha, dv.puntos_venta_id,dv.abreviatura_codigo, dv.codigo,v.nombre,pv.nombre, dv.total;'
            query='select distinct dv.id, to_char(dv.fecha,  \'DD/MM/YYYY\') as fecha, dv.abreviatura_codigo,dv.codigo, dv.iva,dv.porcentaje_iva,dv.total,A.abono,pv.nombre as punto , dv.puntos_venta_id,v.nombre as vendedor,F.factura from proforma dv,(select proforma_id,sum(f.total) as factura,(SELECT SUM(n.total) as total FROM movimiento_nota_credito n where 1=1 and n.proforma_id = dv.id and n.anulado is not True) C from documento_venta f  where  f.activo is True group by f.proforma_id)F,(select proforma_id,sum(da.abono) as abono  from documento_abono_venta da   where  da.documento_venta_id is NULL and da.anulado IS NOT True group by da.proforma_id)A,puntos_venta pv, vendedor v where  dv.aprobada=True and dv.anulada is not  True and  dv.cliente_id = ' + (persona) + ' and F.proforma_id = dv.id and A.proforma_id = dv.id and dv.vendedor_id= v.id and pv.id=dv.puntos_venta_id'
            
        else:
            #query = 'select dv.id, to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.subtotal,dv.base_iva, dv.valor_iva, dv.total,SUM(da.abono),dv.punto_emision from documento_venta dv LEFT JOIN documento_abono_venta da  ON (da.documento_venta_id = dv.id) and da.anulado is not True where dv.cliente_id = ' + (persona) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento, dv.base_iva, dv.valor_iva, dv.total;'
            query='select dv.id, to_char(dv.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dv.establecimiento,dv.secuencial, dv.base_iva,dv.valor_iva, dv.total,(SELECT SUM(abono) as abonos FROM documento_abono_venta da where 1=1 and (da.documento_venta_id = dv.id) and da.anulado is not True) B ,dv.punto_emision,dr.id,retenciones,dv.total-retenciones,(SELECT SUM(n.total) as total FROM movimiento_nota_credito n where 1=1 and n.documento_venta_id = dv.id and n.anulado is not True) C from documento_venta dv LEFT JOIN documento_venta_retenciones dr ON dr.documento_venta_id=dv.id where dv.activo is True and dv.cliente_id  = ' + (persona) + ' GROUP BY dv.id, dv.fecha_emision, dv.establecimiento, dv.base_iva, dv.valor_iva, dv.total,dr.id,retenciones'
        print(query)
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('movimientos/mostrar_facturas_proformas.html',
                                  {'ro': ro, 'tipo': tipo, 'persona': persona,'fila': fila},
                                   RequestContext(request))


@login_required()
def movimiento_consultar_cheque_view(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    bancos = Banco.objects.filter(estado=True)
    cursor = connection.cursor()
    if movimiento.tipo_anticipo_id==1:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_compra f,documento_abono da where da.movimiento_id = ' + (
    pk) + ' and f.id=da.documento_compra_id and da.anulado is not True;'
    else:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_venta f,documento_abono_venta da where da.movimiento_id = ' + (
            pk) + ' and f.id=da.documento_venta_id and da.anulado is not True;'
    cursor.execute(query)
    facturas = cursor.fetchall()
    total_facturas=DocumentoAbono.objects.filter(movimiento_id=pk).filter(anulado=False).aggregate(Sum('abono'))
    if total_facturas['abono__sum']:
        total_f=total_facturas['abono__sum']
    else:
        total_f=0
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None
    
    
    abono_sql='select f.proveedor_id,f.nombre_proveedor,dc.abono,m.numero_comprobante from documento_abono dc, movimiento m,proveedor f where m.id=dc.movimiento_id and f.proveedor_id=dc.proveedor_id  and dc.activo is not False and dc.anulado is not True and m.id=' + (pk) +';'
    cursor.execute(abono_sql)
    ro_abono = cursor.fetchall()




    template = loader.get_template('movimientos/consultar.html')
    context = RequestContext(request, {'movimiento': movimiento, 'facturas': facturas,'asientos': asientos,'detalle_asientos':detalle_asientos, 'abonos': ro_abono,
                                       'total_f':total_f})
    return HttpResponse(template.render(context))




@login_required()
def movimiento_prueba_list_view(request):
    movimientos=''
    template = loader.get_template('movimientos/index_prueba.html')
    context = RequestContext(request, {'movimientos': movimientos})
    return HttpResponse(template.render(context))


# @login_required()
# def movimiento_api_view(request):
#     if request.method == "POST" and request.is_ajax:
#         cursor = connection.cursor()
#         sql="  select m.id,t.descripcion,to_char(m.fecha_emision, \'DD/MM/YYYY\') as fecha,m.numero_comprobante,m.paguese_a,p.ruc,td.descripcion,m.numero_cheque,b.nombre,m.monto_cheque,m.monto,m.descripcion,m.activo,m.conciliacion_id from movimiento m left join proveedor p on p.proveedor_id=m.proveedor_id left join tipo_documento td on td.id=m.tipo_documento_id and td.id=1 left join tipo_anticipo t on t.id=m.tipo_anticipo_id and t.id=1 left join banco b on b.id=m.banco_id where m.tipo_anticipo_id=1 and m.tipo_documento_id=1 order by m.fecha_emision"
#     
#         print sql
#         cursor.execute(sql)
#     
#         ro = cursor.fetchall()
#         json_resultados = json.dumps(ro)
#     else:
#         raise Http404
#     return HttpResponse(json_resultados, content_type="application/json")

@login_required()
@csrf_exempt
def movimiento_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order=request.GET['order[0][column]']
        _order_dir=request.GET['order[0][dir]']
        cursor = connection.cursor()
        #sql="  select m.id,t.descripcion,m.fecha_emision,m.numero_comprobante,m.paguese_a,p.ruc,td.descripcion,m.numero_cheque,b.nombre,m.monto_cheque,m.monto,m.descripcion,m.activo,m.conciliacion_id from movimiento m left join proveedor p on p.proveedor_id=m.proveedor_id left join tipo_documento td on td.id=m.tipo_documento_id and td.id=1 left join tipo_anticipo t on t.id=m.tipo_anticipo_id and t.id=1 left join banco b on b.id=m.banco_id where m.tipo_anticipo_id=1 and m.tipo_documento_id=1 "
        sql="select m.id,t.descripcion,m.fecha_emision,m.numero_comprobante,m.paguese_a,p.ruc,td.descripcion,m.numero_cheque,b.nombre,m.monto_cheque,m.monto,m.descripcion,m.activo,m.conciliacion_id from movimiento m left join proveedor p on p.proveedor_id=m.proveedor_id left join tipo_documento td on td.id=m.tipo_documento_id and td.id=1 left join tipo_anticipo t on t.id=m.tipo_anticipo_id and t.id=1 left join banco b on b.id=m.banco_id where m.tipo_anticipo_id=1 and m.tipo_documento_id=1 "
        if _search_value:
            sql+=" and ( UPPER(t.descripcion) like '%"+_search_value+"%' or UPPER(m.numero_comprobante) like '%"+_search_value.upper()+"%'  or CAST(m.monto_cheque as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(m.monto as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(m.fecha_emision as VARCHAR)  like '%"+_search_value+"%' or UPPER(m.paguese_a) like '%"+_search_value.upper()+"%' or UPPER(p.ruc) like '%"+_search_value.upper()+"%' or UPPER(td.descripcion) like '%"+_search_value.upper()+"%' or UPPER(m.numero_cheque) like '%"+_search_value.upper()+"%' or UPPER(b.nombre) like '%"+_search_value.upper()+"%' or UPPER(m.descripcion) like '%"+_search_value.upper()+"%'"
        
        if _search_value.upper()=='ANULADO'  or _search_value.upper()=='AN' or _search_value.upper()=='ANU' or _search_value.upper()=='ANUL'  or _search_value.upper()=='ANULA' or _search_value.upper()=='ANULAD':
            sql+=" or m.activo is not True"
        
        if _search_value.upper()=='ACTIVO' or _search_value.upper()=='ACTIV' or _search_value.upper()=='ACTI' or _search_value.upper()=='ACT' or _search_value.upper()=='ACT' or _search_value.upper()=='AC':
            sql+=" or m.activo is  True"
        if _search_value:
             sql+=" ) "
            
           
    
        #sql +=" order by fecha"
        print _order
        if _order == '1':
            sql +=" order by t.descripcion "+_order_dir
        if _order == '0':
            sql +=" order by m.fecha_emision "+_order_dir
        if _order == '2':
            sql +=" order by m.numero_comprobante "+_order_dir
        
        if _order == '3':
            sql +=" order by m.paguese_a "+_order_dir
        
        if _order == '4':
            sql +=" order by p.ruc "+_order_dir
        if _order == '5':
            sql +=" order by td.descripcion "+_order_dir
        if _order == '6':
            
            sql +=" order by CAST(m.numero_cheque AS Numeric(10,0)) "+_order_dir
        if _order == '7':
            
            sql +=" order by b.nombre "+_order_dir
        
        if _order == '8':
            sql +=" order by m.monto_cheque "+_order_dir
            
        if _order == '9':
            sql +=" order by m.monto "+_order_dir
            
        if _order == '10':
            sql +=" order by m.descripcion "+_order_dir
        if _order == '':
            sql +=" order by m.fecha_emision DESC"
        
        
        
        cursor.execute(sql)
        compras = cursor.fetchall()
            
        compras_filtered = compras[_start:_start + _end]

        compras_list = []
        for o in compras_filtered:
            compras_obj = []
            
            compras_obj.append(o[2].strftime('%Y-%m-%d'))
            compras_obj.append(o[1])
            compras_obj.append(o[3])
            compras_obj.append(o[4])
            compras_obj.append(o[5])
            compras_obj.append(o[6])
            compras_obj.append(o[7])
            compras_obj.append(o[8])
            compras_obj.append(o[9])
            compras_obj.append(o[10])
            compras_obj.append(o[11])
            html=''
            mes=o[2].month
            anio=o[2].year
            cursor = connection.cursor()
            query="select anio_id,mes_id from bloqueo_periodo  where date_part('year',fecha)='"+str(anio)+"' and date_part('month',fecha)='"+str(mes)+"'"
            cursor.execute(query)
            ro = cursor.fetchall()
            
            if o[13]:
                if o[12]:
                    compras_obj.append("Activo")
                    #fecha_inicial=o[2].split('-')
                    #mes=fecha_inicial[1]
                    #anio=fecha_inicial[0]
                   
                    if ro:
                        r=1
                    else:
                        html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/editar" style=""><button type="button" class="btn btn-primary btn-xs"><i class="fa fa-pencil-square-o icon-white"></i></button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/imprimir_cheque_actual" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa fa-money"></i></button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/consultar_cheque" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye"></i></button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/imprimir_orden_egreso" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa fa-file-text-o"></i></button></a>'
                
                else:
                    compras_obj.append("Anulado")
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/imprimir_cheque_actual" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa fa-money"></i></button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/consultar_cheque" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye"></i></button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/imprimir_orden_egreso" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa fa-file-text-o"></i></button></a>'
                    
            else:

                if o[12]:
                    compras_obj.append("Activo")
                    if ro:
                        r=1
                    else:
                        html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/editar" style=""><button type="button" class="btn btn-primary btn-xs"><i class="fa fa-pencil-square-o icon-white"></i></button></a>'
                        html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/eliminar" style=""><button type="button" class="btn btn-danger btn-xs"><i class=" glyphicon glyphicon-trash icon-white"></i></button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/imprimir_cheque_actual" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa fa-money"></i></button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/consultar_cheque" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye"></i></button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/imprimir_orden_egreso" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa fa-file-text-o"></i></button></a>'
                
                else:
                    
                    compras_obj.append("Anulado")
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/imprimir_cheque_actual" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa fa-money"></i></button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/consultar_cheque" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye"></i></button></a>'
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/bancos/movimiento/'+str(o[0])+'/imprimir_orden_egreso" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa fa-file-text-o"></i></button></a>'
                
            
           
            
           
            
            

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
def movimiento_nc_cliente_bancaria_consultar_view(request,pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(proveedor = True)
    
    cursor = connection.cursor()
    query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.total,da.total,da.total,f.punto_emision,f.secuencial  from documento_venta f,movimiento_nota_credito da where da.movimiento_id = ' + (
            pk) + ' and f.id=da.documento_venta_id;'
    cursor.execute(query)
    facturas = cursor.fetchall()
    query2='select dv.id,dv.fecha, dv.abreviatura_codigo, dv.subtotal,dv.iva, dv.total,da.total,da.total,da.total,pv.nombre as punto ,dv.codigo from proforma dv INNER JOIN  puntos_venta pv ON (dv.puntos_venta_id= pv.id) INNER JOIN  movimiento_nota_credito da ON (da.proforma_id= dv.id) where pv.id=dv.puntos_venta_id and  da.movimiento_id = ' + str(pk) + ' and  dv.id=da.proforma_id'
    
    #query2 = 'select f.id,f.fecha_emision,f.abreviatura_codigo,f.c,f.valor_iva,f.total,da.total,da.total,da.total,f.punto_emision,f.secuencial  from documento_venta f,movimiento_nota_credito da where da.movimiento_id = ' + (pk) + ' and f.id=da.documento_venta_id;'
    cursor.execute(query2)
    proformas = cursor.fetchall()
    total_facturas=MovimientoNotaCredito.objects.filter(movimiento_id=pk).aggregate(Sum('total'))
    
    
    
    if total_facturas['total__sum']:
        total_f=total_facturas['total__sum']
    else:
        total_f=0
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None
    
    total_asientos_debe1=AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id).aggregate(Sum('debe'))
    total_asientos_haber1=AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id).aggregate(Sum('haber'))
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
    



    template = loader.get_template('movimientos/nc_bancaria_cliente_consultar.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos, 'facturas': facturas,'asientos': asientos,'detalle_asientos':detalle_asientos,
                                       'tipo_documentos': tipo_documentos, 'total_f':total_f,'total_asientos_debe':total_asientos_debe,'total_asientos_haber':total_asientos_haber,'proformas':proformas})
    return HttpResponse(template.render(context))
    
    
    
@login_required()
def movimiento_deposito_cliente_consultar_view(request,pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(cliente=True).exclude(id=9).exclude(id=3)
    
    cursor = connection.cursor()
    query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.abono,da.abono,f.punto_emision,f.secuencial  from documento_venta f,documento_abono_venta da where da.movimiento_id = ' + (
            pk) + ' and f.id=da.documento_venta_id;'
    cursor.execute(query)
    facturas = cursor.fetchall()
    total_facturas=DocumentoAbonoVenta.objects.filter(movimiento_id=pk).aggregate(Sum('abono'))
    if total_facturas['abono__sum']:
        total_f=total_facturas['abono__sum']
    else:
        total_f=0
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None
    
    total_asientos_debe1=AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id).aggregate(Sum('debe'))
    total_asientos_haber1=AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id).aggregate(Sum('haber'))
    if total_asientos_debe1['debe__sum']:
        total_asientos_debe=total_asientos_debe1['debe__sum']
    else:
        total_asientos_debe1=0
    
    if total_asientos_haber1['haber__sum']:
        total_asientos_haber=total_asientos_haber1['haber__sum']
    else:
        total_asientos_haber1=0
    



    template = loader.get_template('movimientos/consultar_deposito_cliente.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos, 'facturas': facturas,'asientos': asientos,'detalle_asientos':detalle_asientos,
                                       'tipo_documentos': tipo_documentos, 'total_f':total_f,'total_asientos_debe':total_asientos_debe,'total_asientos_haber':total_asientos_haber})
    return HttpResponse(template.render(context))


@login_required()
def movimiento_consultar_deposito_view(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    tipo_anticipos = TipoAnticipo.objects.all()
    tipo_documentos = TipoDocumento.objects.filter(proveedor = True)
    cursor = connection.cursor()
    if movimiento.tipo_anticipo_id==1:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_compra f,documento_abono da where da.movimiento_id = ' + (
    pk) + ' and f.id=da.documento_compra_id;'
    else:
        query = 'select f.id,f.fecha_emision,f.establecimiento,f.base_iva,f.valor_iva,f.total,da.abono,da.cantidad_anterior_abonada,da.diferencia,f.punto_emision,f.secuencial  from documento_venta f,documento_abono_venta da where da.movimiento_id = ' + (
            pk) + ' and f.id=da.documento_venta_id;'
    cursor.execute(query)
    facturas = cursor.fetchall()
    total_facturas=DocumentoAbono.objects.filter(movimiento_id=pk).aggregate(Sum('abono'))
    if total_facturas['abono__sum']:
        total_f=total_facturas['abono__sum']
    else:
        total_f=0
    try:
        asientos = Asiento.objects.get(asiento_id=movimiento.asiento_id)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle_asientos = AsientoDetalle.objects.filter(asiento_id=movimiento.asiento_id)
    except AsientoDetalle.DoesNotExist:
        detalle_asientos = None



    template = loader.get_template('movimientos/consultar_deposito.html')
    context = RequestContext(request, {'movimiento': movimiento, 'tipo_anticipos': tipo_anticipos, 'facturas': facturas,'asientos': asientos,'detalle_asientos':detalle_asientos,
                                       'tipo_documentos': tipo_documentos, 'total_f':total_f})
    return HttpResponse(template.render(context))

@login_required()
@csrf_exempt
def validarBloqueoPeriodo(request):
    if request.method == 'POST':
      fecha = request.POST.get('fecha')
      fecha_inicial=fecha.split('-')
      mes=fecha_inicial[1]
      anio=fecha_inicial[0]
      cursor = connection.cursor()
      query="select anio_id,mes_id from bloqueo_periodo  where date_part('year',fecha)='"+str(anio)+"' and date_part('month',fecha)='"+str(mes)+"'"
      print query
                       
      cursor.execute(query)
      ro = cursor.fetchall()
      json_resultados = json.dumps(ro)
      return HttpResponse(json_resultados, content_type="application/json")

    else:
        raise Http404
    
    

@login_required()
def ReporteTipoMovimientoView(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    centro_costos = CentroCosto.objects.filter(activo=True)
    tipos = TipoDocumento.objects.all()
    return render_to_response('reportes/reporte_por_movimiento.html',
                              RequestContext(request, {'cuentas': plan_ctas,'centro_costos':centro_costos,'tipos':tipos}))


@login_required()
def ConsultaReporteTipoMovimientoView(request):
    if request.method == "POST" and request.is_ajax:
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        cuenta_hasta = request.POST['inputCuentaHasta']
        centroCosto = request.POST['centro_costo']
        tipo = request.POST['tipo']
        try:
            cuenta_cod_desde = PlanDeCuentas.objects.get(plan_id=cuenta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_desde = None
            
        try:
            cuenta_cod_hasta = PlanDeCuentas.objects.get(plan_id=cuenta_hasta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_hasta= None
        
    

        cursor = connection.cursor()
        html=''
        html+='<table class="table table-bordered " id="estado_cuentas">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="8"><b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>DESDE:'+str(fecha_desde)+' HASTA: '+str(fecha_hasta)+'</td></tr>'
        html+='<tr><th style="text-align: center"><b>Fecha</b></th><th style="text-align: center"><b>Tipo de Movimiento</b></th>'
        html+='<th style="text-align: center"><b>No. Movimiento</b></th><th style="text-align: center"><b>Cuenta</b></th>'
        html+='<th style="text-align: center"><b>Debe</b></th><th style="text-align: center"><b>Haber</b></th>'
        html+='<th style="text-align: center"><b>Glosa</b></th>'
        html+='<th style="text-align: center"><b>Centro de Costo</b></th>'
        html+='</tr></thead>'
        html+='<tbody>'
        
        sql2="select m.id,m.tipo_documento_id,m.fecha_emision,t.descripcion,m.numero_comprobante,p.nombre_plan,p.codigo_plan,p.plan_id,sum(ad.debe),sum(ad.haber),a.glosa,ad.centro_costo_id from movimiento m,contabilidad_plandecuentas p,contabilidad_asiento a,contabilidad_asientodetalle ad,tipo_documento t where a.asiento_id=ad.asiento_id and a.anulado is not True and ad.cuenta_id=p.plan_id"
        sql2+=" and t.id=m.tipo_documento_id and m.asiento_id=a.asiento_id and p.codigo_plan::float>= "+str(cuenta_cod_desde.codigo_plan)+" and p.codigo_plan::float<= "+str(cuenta_cod_hasta.codigo_plan)+" and m.fecha_emision >= '"+str(fecha_desde)+"' and m.fecha_emision <= '"+str(fecha_hasta)+"'"
        if centroCosto != "0":
            sql2+=" and ad.centro_costo_id="+str(centroCosto)
        
        if tipo != "0":
            sql2+=" and m.tipo_documento_id="+str(tipo)
        sql2+=" GROUP BY m.id,m.tipo_documento_id,m.fecha_emision,t.descripcion,m.numero_comprobante,p.nombre_plan,p.codigo_plan,p.plan_id,a.glosa,ad.centro_costo_id"
        cursor.execute(sql2)
        rop = cursor.fetchall()
        for cuentas in rop:
            html+='<tr>'
            html+='<td >' + str(cuentas[2])+ '</td>'
            html+='<td >' + str(cuentas[3].encode('utf8'))+ '</td>'
            html+='<td >' + str(cuentas[4])+ '</td>'
            html+='<td>' + str(cuentas[6].encode('utf8'))+ '-' + str(cuentas[5].encode('utf8')) + '</td>'
            html+='<td >' + str("%2.2f" % cuentas[8]).replace('.', ',')+ '</td>'
            html+='<td >' + str("%2.2f" % cuentas[9]).replace('.', ',')+ '</td>'
            html+='<td >' + str(cuentas[10].encode('utf8'))+ '</td>'
            try:
                pb = CentroCosto.objects.filter(centro_id=cuentas[11]).first()
            except CentroCosto.DoesNotExist:
                pb = None
            if pb:
                html+='<td>' + str(pb.nombre_centro.encode('utf8'))+ '</td>'
            else:
                html+='<td></td>'
            html+='</tr>'
                     
            
            
        html+='</tbody>'
    else:
        raise Http404

    return HttpResponse(
            html
        )
    #return HttpResponse(json_resultados, content_type="application/json")
    
@login_required()
def movimientoNotaCreditoComercialEliminarByPkView(request, pk):
    obj = Movimiento.objects.get(id=pk)

    if obj:
        obj.activo = False
        obj.updated_by = request.user.get_full_name()
        obj.updated_at = now
        obj.save()
        print "entro a mov"
        
        try:
            asiento = Asiento.objects.filter(asiento_id=obj.asiento_id)
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            for a in asiento:
                a.anulado= True
                a.updated_by = request.user.get_full_name()
                a.updated_at = now
                a.save()
        
        
   
                
                
        try:
            nota_credito = MovimientoNotaCredito.objects.filter(movimiento_id=obj.id)
        except MovimientoNotaCredito.DoesNotExist:
            nota_credito = None
            
        print obj.id
        if nota_credito:
            for nc in nota_credito:
                nc.anulado= True
                nc.save()
                
        
                
                try:
                    dv = DocumentoVenta.objects.filter(id=nc.documento_venta_id)
                except DocumentoVenta.DoesNotExist:
                    dv = None
                if dv:
                    print "entro a dv"
                    for d1 in dv:
                        d1.nota_credito= False
                        d1.save()
                            

    return HttpResponseRedirect('/bancos/movimiento/nc/comercial')


#reportes
@login_required()
def reporteporChequesView(request):
    cursor = connection.cursor();
    cursor.execute("SELECT proveedor_id,codigo_proveedor,nombre_proveedor from proveedor order by CAST(codigo_proveedor AS Numeric(10,0))" );
    row = cursor.fetchall();
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')

    return render_to_response('reportes/reportes_por_cheque.html',RequestContext(request, {'proveedores': row,'cuentas': plan_ctas,}))


@login_required()
def ConsultaReporteporChequeView(request):
    if request.method == "POST" and request.is_ajax:
        cuenta = request.POST['inputCuentaDesde']
        fecha_desde = request.POST['fechainicial']
        fecha_hasta = request.POST['fechafin']
        cuenta_hasta = request.POST['inputCuentaHasta']
        provedor_desde = request.POST['proveedor']
        provedor_hasta= request.POST['proveedor_hasta']
        conciliado = request.POST['conciliado']
        activo = request.POST['activo']
        
        try:
            cuenta_cod_desde = PlanDeCuentas.objects.get(plan_id=cuenta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_desde = None
            
        try:
            cuenta_cod_hasta = PlanDeCuentas.objects.get(plan_id=cuenta_hasta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_hasta= None
        
    

        cursor = connection.cursor()
        html=''
        html+='<table class="table table-bordered " id="cheques">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="9">'
        #<b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>'
        html+='<b><b>REPORTE DE CHEQUES <br />DESDE:'+str(fecha_desde)+' HASTA: '+str(fecha_hasta)+'</b></td></tr>'
        html+='<tr><th style="text-align: center"><b>No. Movimiento</b></th><th style="text-align: center"><b>Fecha</b></th><th style="text-align: center"><b>Cheque</b></th>'
        html+='<th style="text-align: center"><b>Identificacion</b></th><th style="text-align: center"><b>Proveedor</b></th>'
        html+='<th style="text-align: center"><b>Beneficiario</b></th><th style="text-align: center"><b>Concepto</b></th>'
        html+='<th style="text-align: center"><b>Total</b></th>'
        html+='<th style="text-align: center"><b>Facturas</b></th>'
        html+='</tr></thead>'
        html+='<tbody>'
        
        sql2="select m.id,m.tipo_documento_id,m.fecha_emision,t.descripcion,m.numero_comprobante,m.numero_cheque,pr.ruc,pr.cedula,pr.codigo_proveedor,m.paguese_a,m.descripcion,m.monto_cheque,p.nombre_plan,p.codigo_plan,p.plan_id,sum(ad.debe),sum(ad.haber),a.glosa from movimiento m,contabilidad_plandecuentas p,contabilidad_asiento a,contabilidad_asientodetalle ad,tipo_documento t,proveedor pr where a.asiento_id=ad.asiento_id and ad.cuenta_id=p.plan_id"
        sql2+=" and m.proveedor_id=pr.proveedor_id and t.id=m.tipo_documento_id and m.asiento_id=a.asiento_id"
        sql2+=" and p.codigo_plan::float>= "+str(cuenta_cod_desde.codigo_plan)+" and p.codigo_plan::float<= "+str(cuenta_cod_hasta.codigo_plan)
        if provedor_desde != "0":
            sql2+=" and pr.codigo_proveedor::float>= "+str(provedor_desde)
        if provedor_hasta != "0":
            sql2+=" and pr.codigo_proveedor::float<= "+str(provedor_hasta)
        sql2+=" and m.fecha_emision >= '"+str(fecha_desde)+"' and m.fecha_emision <= '"+str(fecha_hasta)+"'"
        sql2+=" and m.tipo_documento_id=1"
        if conciliado == "1":
            sql2+=" and m.conciliacion_id is not Null"
        if conciliado == "2":
            sql2+=" and m.conciliacion_id is  Null"
        
        if activo == "1":
            sql2+=" and m.activo is True"
        if activo == "2":
            sql2+=" and m.activo is not True"
        
        
        sql2+=" GROUP BY m.id,m.tipo_documento_id,m.fecha_emision,t.descripcion,m.numero_comprobante,p.nombre_plan,p.codigo_plan,p.plan_id,a.glosa,m.numero_cheque,pr.ruc,pr.cedula,pr.codigo_proveedor,m.paguese_a,m.descripcion,m.monto_cheque order by m.numero_cheque"
        print sql2
        cursor.execute(sql2)
        rop = cursor.fetchall()
        for cuentas in rop:
            html+='<tr>'
            html+='<td >' + str(cuentas[4])+ '</td>'
            html+='<td >' + str(cuentas[2])+ '</td>'
            html+='<td >' + str(cuentas[5])+ '</td>'
            html+='<td >' + str(cuentas[6])+ '</td>'
            html+='<td >' + str(cuentas[8])+ '</td>'
            html+='<td >' + str(cuentas[9].encode('utf8'))+ '</td>'
            html+='<td >' + str(cuentas[10].encode('utf8'))+ '</td>'
            html+='<td >' + str("%2.2f" % cuentas[11]).replace('.', ',')+ '</td>'
            html_facturas=''
            try:
                facturas = DocumentoAbono.objects.filter(movimiento_id=cuentas[0])
            except DocumentoAbono.DoesNotExist:
                facturas = None
            if facturas:
                for f in facturas:
                    if f.documento_compra:
                        html_facturas+=f.documento_compra.establecimiento+'-'+f.documento_compra.punto_emision+'-'+f.documento_compra.secuencial+'/ '
            html+='<td >' + str(html_facturas)+ '</td>'
            html+='</tr>'
                     
            
            
        html+='</tbody>'
    else:
        raise Http404

    return HttpResponse(
            html
        )
    #return HttpResponse(json_resultados, content_type="application/json")
    
    
@login_required()
def reporteporDepositoView(request):
    cursor = connection.cursor();
    cursor.execute("SELECT id_cliente,codigo_cliente,nombre_cliente from cliente order by CAST(codigo_cliente AS Numeric(10,0))" );
    row = cursor.fetchall();
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')

    return render_to_response('reportes/reportes_por_deposito.html',RequestContext(request, {'cliente': row,'cuentas': plan_ctas,}))


@login_required()
def ConsultaReporteporDepositoView(request):
    if request.method == "POST" and request.is_ajax:
        cuenta = request.POST['inputCuentaDesde']
        fecha_desde = request.POST['fechainicial']
        fecha_hasta = request.POST['fechafin']
        cuenta_hasta = request.POST['inputCuentaHasta']
        cliente_desde = request.POST['cliente']
        cliente_hasta= request.POST['cliente_hasta']
        conciliado = request.POST['conciliado']
        activo = request.POST['activo']
        
        try:
            cuenta_cod_desde = PlanDeCuentas.objects.get(plan_id=cuenta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_desde = None
            
        try:
            cuenta_cod_hasta = PlanDeCuentas.objects.get(plan_id=cuenta_hasta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_hasta= None
        
    

        cursor = connection.cursor()
        html=''
        html+='<table class="table table-bordered " id="cheques">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="4" style="text-align: center">'
        #<b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>'
        html+='<b>REPORTE DE DEPOSITOS <br />DESDE:'+str(fecha_desde)+' HASTA: '+str(fecha_hasta)+'</b></td></tr>'
        html+='<tr><th style="text-align: center"><b>No. Movimiento</b></th><th style="text-align: center"><b>Fecha</b></th>'
        html+='<th style="text-align: center"><b>Concepto</b></th>'
        html+='<th style="text-align: center"><b>Total</b></th>'
        html+='</tr></thead>'
        html+='<tbody>'
        
        sql2="select pr.id_cliente,pr.codigo_cliente,pr.nombre_cliente from movimiento m,contabilidad_plandecuentas p,contabilidad_asiento a,contabilidad_asientodetalle ad,tipo_documento t,cliente pr where a.asiento_id=ad.asiento_id and ad.cuenta_id=p.plan_id"
        sql2+=" and m.cliente_id=pr.id_cliente and t.id=m.tipo_documento_id and m.asiento_id=a.asiento_id"
        sql2+=" and p.codigo_plan::float>= "+str(cuenta_cod_desde.codigo_plan)+" and p.codigo_plan::float<= "+str(cuenta_cod_hasta.codigo_plan)
        if cliente_desde != "0":
            sql2+=" and pr.codigo_cliente::float>= "+str(cliente_desde)
        if cliente_hasta != "0":
            sql2+=" and pr.codigo_cliente::float<= "+str(cliente_hasta)
        
        sql2+=" and m.fecha_emision >= '"+str(fecha_desde)+"' and m.fecha_emision <= '"+str(fecha_hasta)+"'"
        sql2+=" and m.tipo_documento_id=4"
        
        if conciliado == "1":
            sql2+=" and m.conciliacion_id is not Null"
        if conciliado == "2":
            sql2+=" and m.conciliacion_id is  Null"
        
        if activo == "1":
            sql2+=" and m.activo is True"
        if activo == "2":
            sql2+=" and m.activo is not True"
        
        
        sql2+=" GROUP BY  pr.id_cliente,pr.codigo_cliente,pr.nombre_cliente  order by pr.codigo_cliente"
        print sql2
        cursor.execute(sql2)
        rop = cursor.fetchall()
        total_g=0
        for c in rop:
            html+='<tr>'
            html+='<td colspan="5"><b>' + str(c[1])+ '-'+ str(c[2].encode('utf8'))+ '</b></td>'
            html+='</tr>'
            sql3="select m.id,m.tipo_documento_id,m.fecha_emision,t.descripcion,m.numero_comprobante,m.numero_cheque,pr.ruc,pr.cedula,pr.codigo_cliente,m.paguese_a,m.descripcion,m.monto,p.nombre_plan,p.codigo_plan,p.plan_id,sum(ad.debe),sum(ad.haber),a.glosa from movimiento m,contabilidad_plandecuentas p,contabilidad_asiento a,contabilidad_asientodetalle ad,tipo_documento t,cliente pr where a.asiento_id=ad.asiento_id and ad.cuenta_id=p.plan_id"
            sql3+=" and m.cliente_id=pr.id_cliente and t.id=m.tipo_documento_id and m.asiento_id=a.asiento_id"
            sql3+=" and p.codigo_plan::float>= "+str(cuenta_cod_desde.codigo_plan)+" and p.codigo_plan::float<= "+str(cuenta_cod_hasta.codigo_plan)
            sql3+=" and pr.id_cliente= "+str(c[0])
            sql3+=" and m.fecha_emision >= '"+str(fecha_desde)+"' and m.fecha_emision <= '"+str(fecha_hasta)+"'"
            sql3+=" and m.tipo_documento_id=4"
            
            if conciliado == "1":
                sql3+=" and m.conciliacion_id is not Null"
            if conciliado == "2":
                sql3+=" and m.conciliacion_id is  Null"
            
            if activo == "1":
                sql3+=" and m.activo is True"
            if activo == "2":
                sql3+=" and m.activo is not True"
            
            
            sql3+=" GROUP BY m.id,m.tipo_documento_id,m.fecha_emision,t.descripcion,m.numero_comprobante,p.nombre_plan,p.codigo_plan,p.plan_id,a.glosa,m.numero_cheque,pr.ruc,pr.cedula,pr.codigo_cliente,m.paguese_a,m.descripcion,m.monto order by m.fecha_emision"
            print sql3
            cursor.execute(sql3)
            rop1 = cursor.fetchall()
            total_c=0
            for cuentas in rop1:
                html+='<tr>'
                html+='<td >' + str(cuentas[4])+ '</td>'
                html+='<td >' + str(cuentas[2])+ '</td>'
                html+='<td >' + str(cuentas[10].encode('utf8'))+ '</td>'
                html+='<td >' + str("%2.2f" % cuentas[11]).replace('.', ',')+ '</td>'
                total_c=total_c+cuentas[11]
                
                html+='</tr>'
            
            html+='<tr>'
            html+='<td colspan="3" style="text-align:right"><b>Total</b></td>'
            html+='<td ><b>' + str("%2.2f" % total_c).replace('.', ',')+ '</b></td>'
            html+='</tr>'
            total_g=total_g+total_c
                     
        html+='<tr>'
        html+='<td colspan="3" style="text-align:right"><b>Total General</b></td>'
        html+='<td ><b>' + str("%2.2f" % total_g).replace('.', ',')+ '</b></td>'
        html+='</tr>'    
            
        html+='</tbody>'
    else:
        raise Http404

    return HttpResponse(
            html
        )
    #return HttpResponse(json_resultados, content_type="application/json")
    
    
@login_required()
def reporteporNotadeCreditoView(request):
    cursor = connection.cursor();
    cursor.execute("SELECT id_cliente,codigo_cliente,nombre_cliente from cliente order by CAST(codigo_cliente AS Numeric(10,0))" );
    row = cursor.fetchall();
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')

    return render_to_response('reportes/reportes_por_nota_credito.html',RequestContext(request, {'cliente': row,'cuentas': plan_ctas,}))


@login_required()
def ConsultaReporteporNotadeCreditoView(request):
    if request.method == "POST" and request.is_ajax:
        cuenta = request.POST['inputCuentaDesde']
        fecha_desde = request.POST['fechainicial']
        fecha_hasta = request.POST['fechafin']
        cuenta_hasta = request.POST['inputCuentaHasta']
        cliente_desde = request.POST['cliente']
        cliente_hasta= request.POST['cliente_hasta']
        conciliado = request.POST['conciliado']
        activo = request.POST['activo']
        
        try:
            cuenta_cod_desde = PlanDeCuentas.objects.get(plan_id=cuenta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_desde = None
            
        try:
            cuenta_cod_hasta = PlanDeCuentas.objects.get(plan_id=cuenta_hasta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_hasta= None
        
    

        cursor = connection.cursor()
        html=''
        html+='<table class="table table-bordered " id="cheques">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="4" style="text-align: center">'
        #<b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>'
        html+='<b><b>REPORTE DE NOTAS DE CREDITO <br />DESDE:'+str(fecha_desde)+' HASTA: '+str(fecha_hasta)+'</b></td></tr>'
        html+='<tr><th style="text-align: center"><b>No. Movimiento</b></th><th style="text-align: center"><b>Fecha</b></th>'
        html+='<th style="text-align: center"><b>Concepto</b></th>'
        html+='<th style="text-align: center"><b>Total</b></th>'
        html+='</tr></thead>'
        html+='<tbody>'
        
        sql2="select pr.id_cliente,pr.codigo_cliente,pr.nombre_cliente from movimiento m,contabilidad_plandecuentas p,contabilidad_asiento a,contabilidad_asientodetalle ad,tipo_documento t,cliente pr where a.asiento_id=ad.asiento_id and ad.cuenta_id=p.plan_id"
        sql2+=" and m.cliente_id=pr.id_cliente and t.id=m.tipo_documento_id and m.asiento_id=a.asiento_id"
        sql2+=" and p.codigo_plan::float>= "+str(cuenta_cod_desde.codigo_plan)+" and p.codigo_plan::float<= "+str(cuenta_cod_hasta.codigo_plan)
        if cliente_desde != "0":
            sql2+=" and pr.codigo_cliente::float>= "+str(cliente_desde)
        if cliente_hasta != "0":
            sql2+=" and pr.codigo_cliente::float<= "+str(cliente_hasta)
        sql2+=" and m.fecha_emision >= '"+str(fecha_desde)+"' and m.fecha_emision <= '"+str(fecha_hasta)+"'"
        sql2+=" and m.tipo_documento_id=3"
        
        if conciliado == "1":
            sql2+=" and m.conciliacion_id is not Null"
        if conciliado == "2":
            sql2+=" and m.conciliacion_id is  Null"
        
        if activo == "1":
            sql2+=" and m.activo is True"
        if activo == "2":
            sql2+=" and m.activo is not True"
        
        
        sql2+=" GROUP BY  pr.id_cliente,pr.codigo_cliente,pr.nombre_cliente order by  CAST(pr.codigo_cliente AS Numeric(10,0)) "
        print sql2
        cursor.execute(sql2)
        rop = cursor.fetchall()
        total_g=0
        for c in rop:
            html+='<tr>'
            html+='<td colspan="5"><b>' + str(c[1])+ '-'+ str(c[2].encode('utf8'))+ '</b></td>'
            html+='</tr>'
            sql3="select m.id,m.tipo_documento_id,m.fecha_emision,t.descripcion,m.numero_comprobante,m.numero_cheque,pr.ruc,pr.cedula,pr.codigo_cliente,m.paguese_a,m.descripcion,m.monto,p.nombre_plan,p.codigo_plan,p.plan_id,sum(ad.debe),sum(ad.haber),a.glosa from movimiento m,contabilidad_plandecuentas p,contabilidad_asiento a,contabilidad_asientodetalle ad,tipo_documento t,cliente pr where a.asiento_id=ad.asiento_id and ad.cuenta_id=p.plan_id"
            sql3+=" and m.cliente_id=pr.id_cliente and t.id=m.tipo_documento_id and m.asiento_id=a.asiento_id"
            sql3+=" and p.codigo_plan::float>= "+str(cuenta_cod_desde.codigo_plan)+" and p.codigo_plan::float<= "+str(cuenta_cod_hasta.codigo_plan)
            sql3+=" and pr.id_cliente= "+str(c[0])
            sql3+=" and m.fecha_emision >= '"+str(fecha_desde)+"' and m.fecha_emision <= '"+str(fecha_hasta)+"'"
            sql3+=" and m.tipo_documento_id=3"
            
            if conciliado == "1":
                sql3+=" and m.conciliacion_id is not Null"
            if conciliado == "2":
                sql3+=" and m.conciliacion_id is  Null"
            
            if activo == "1":
                sql3+=" and m.activo is True"
            if activo == "2":
                sql3+=" and m.activo is not True"
            
            
            sql3+=" GROUP BY m.id,m.tipo_documento_id,m.fecha_emision,t.descripcion,m.numero_comprobante,p.nombre_plan,p.codigo_plan,p.plan_id,a.glosa,m.numero_cheque,pr.ruc,pr.cedula,pr.codigo_cliente,m.paguese_a,m.descripcion,m.monto order by m.fecha_emision"
            print sql3
            cursor.execute(sql3)
            rop1 = cursor.fetchall()
            total_c=0
            for cuentas in rop1:
                html+='<tr>'
                html+='<td >' + str(cuentas[4])+ '</td>'
                html+='<td >' + str(cuentas[2])+ '</td>'
                html+='<td >' + str(cuentas[10].encode('utf8'))+ '</td>'
                html+='<td >' + str("%2.2f" % cuentas[11]).replace('.', ',')+ '</td>'
                total_c=total_c+cuentas[11]
                
                html+='</tr>'
            
            html+='<tr>'
            html+='<td colspan="3" style="text-align:right"><b>Total</b></td>'
            html+='<td ><b>' + str("%2.2f" % total_c).replace('.', ',')+ '</b></td>'
            html+='</tr>'
            total_g=total_g+total_c
                     
        html+='<tr>'
        html+='<td colspan="3" style="text-align:right"><b>Total General</b></td>'
        html+='<td ><b>' + str("%2.2f" % total_g).replace('.', ',')+ '</b></td>'
        html+='</tr>'    
            
        html+='</tbody>'
    else:
        raise Http404

    return HttpResponse(
            html
        )
    #return HttpResponse(json_resultados, content_type="application/json")
    
    
@login_required()
def reporteporNotadeDebitoView(request):
    cursor = connection.cursor();
    cursor.execute("SELECT proveedor_id,codigo_proveedor,nombre_proveedor from proveedor order by CAST(codigo_proveedor AS Numeric(10,0))" );
    row = cursor.fetchall();
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')

    return render_to_response('reportes/reportes_por_nota_debito.html',RequestContext(request, {'proveedor': row,'cuentas': plan_ctas,}))


@login_required()
def ConsultaReporteporNotadeDebitoView(request):
    if request.method == "POST" and request.is_ajax:
        cuenta = request.POST['inputCuentaDesde']
        fecha_desde = request.POST['fechainicial']
        fecha_hasta = request.POST['fechafin']
        cuenta_hasta = request.POST['inputCuentaHasta']
        proveedor_desde = request.POST['proveedor']
        proveedor_hasta= request.POST['proveedor_hasta']
        conciliado = request.POST['conciliado']
        activo = request.POST['activo']
        
        try:
            cuenta_cod_desde = PlanDeCuentas.objects.get(plan_id=cuenta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_desde = None
            
        try:
            cuenta_cod_hasta = PlanDeCuentas.objects.get(plan_id=cuenta_hasta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_hasta= None
        
    

        cursor = connection.cursor()
        html=''
        html+='<table class="table table-bordered " id="cheques">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="4" style="text-align: center">'
        #<b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>'
        html+='<b><b>REPORTE DE NOTAS DE DEBITO <br />DESDE:'+str(fecha_desde)+' HASTA: '+str(fecha_hasta)+'</b></td></tr>'
        html+='<tr><th style="text-align: center"><b>No. Movimiento</b></th><th style="text-align: center"><b>Fecha</b></th>'
        html+='<th style="text-align: center"><b>Concepto</b></th>'
        html+='<th style="text-align: center"><b>Total</b></th>'
        html+='</tr></thead>'
        html+='<tbody>'
        
        sql2="select pr.proveedor_id,pr.codigo_proveedor,pr.nombre_proveedor from movimiento m,contabilidad_plandecuentas p,contabilidad_asiento a,contabilidad_asientodetalle ad,tipo_documento t,proveedor pr where a.asiento_id=ad.asiento_id and ad.cuenta_id=p.plan_id"
        sql2+=" and m.proveedor_id=pr.proveedor_id and t.id=m.tipo_documento_id and m.asiento_id=a.asiento_id"
        sql2+=" and p.codigo_plan::float>= "+str(cuenta_cod_desde.codigo_plan)+" and p.codigo_plan::float<= "+str(cuenta_cod_hasta.codigo_plan)
        if proveedor_desde != "0":
            sql2+=" and pr.codigo_proveedor::float>= "+str(proveedor_desde)
        if proveedor_hasta != "0":
            sql2+=" and pr.codigo_proveedor::float<= "+str(proveedor_hasta)
        sql2+=" and m.fecha_emision >= '"+str(fecha_desde)+"' and m.fecha_emision <= '"+str(fecha_hasta)+"'"
        sql2+=" and m.tipo_documento_id=2"
        
        if conciliado == "1":
            sql2+=" and m.conciliacion_id is not Null"
        if conciliado == "2":
            sql2+=" and m.conciliacion_id is  Null"
        
        if activo == "1":
            sql2+=" and m.activo is True"
        if activo == "2":
            sql2+=" and m.activo is not True"
        
        
        sql2+=" GROUP BY  pr.proveedor_id,pr.codigo_proveedor,pr.nombre_proveedor "
        print sql2
        cursor.execute(sql2)
        rop = cursor.fetchall()
        total_g=0
        for c in rop:
            html+='<tr>'
            html+='<td colspan="5"><b>' + str(c[1])+ '-'+ str(c[2].encode('utf8'))+ '</b></td>'
            html+='</tr>'
            sql3="select m.id,m.tipo_documento_id,m.fecha_emision,t.descripcion,m.numero_comprobante,m.numero_cheque,pr.ruc,pr.cedula,pr.codigo_proveedor,m.paguese_a,m.descripcion,m.monto,p.nombre_plan,p.codigo_plan,p.plan_id,sum(ad.debe),sum(ad.haber),a.glosa from movimiento m,contabilidad_plandecuentas p,contabilidad_asiento a,contabilidad_asientodetalle ad,tipo_documento t,proveedor pr where a.asiento_id=ad.asiento_id and ad.cuenta_id=p.plan_id"
            sql3+=" and m.proveedor_id=pr.proveedor_id and t.id=m.tipo_documento_id and m.asiento_id=a.asiento_id"
            sql3+=" and p.codigo_plan::float>= "+str(cuenta_cod_desde.codigo_plan)+" and p.codigo_plan::float<= "+str(cuenta_cod_hasta.codigo_plan)
            sql3+=" and pr.proveedor_id= "+str(c[0])
            sql3+=" and m.fecha_emision >= '"+str(fecha_desde)+"' and m.fecha_emision <= '"+str(fecha_hasta)+"'"
            sql3+=" and m.tipo_documento_id=3"
            
            if conciliado == "1":
                sql3+=" and m.conciliacion_id is not Null"
            if conciliado == "2":
                sql3+=" and m.conciliacion_id is  Null"
            
            if activo == "1":
                sql3+=" and m.activo is True"
            if activo == "2":
                sql3+=" and m.activo is not True"
            
            
            sql3+=" GROUP BY m.id,m.tipo_documento_id,m.fecha_emision,t.descripcion,m.numero_comprobante,p.nombre_plan,p.codigo_plan,p.plan_id,a.glosa,m.numero_cheque,pr.ruc,pr.cedula,pr.codigo_proveedor,m.paguese_a,m.descripcion,m.monto"
            print sql3
            cursor.execute(sql3)
            rop1 = cursor.fetchall()
            total_c=0
            for cuentas in rop1:
                html+='<tr>'
                html+='<td >' + str(cuentas[4])+ '</td>'
                html+='<td >' + str(cuentas[2])+ '</td>'
                html+='<td >' + str(cuentas[10].encode('utf8'))+ '</td>'
                html+='<td >' + str("%2.2f" % cuentas[11]).replace('.', ',')+ '</td>'
                total_c=total_c+cuentas[11]
                
                html+='</tr>'
            
            html+='<tr>'
            html+='<td colspan="3" style="text-align:right"><b>Total</b></td>'
            html+='<td ><b>' + str("%2.2f" % total_c).replace('.', ',')+ '</b></td>'
            html+='</tr>'
            total_g=total_g+total_c
                     
        html+='<tr>'
        html+='<td colspan="3" style="text-align:right"><b>Total General</b></td>'
        html+='<td ><b>' + str("%2.2f" % total_g).replace('.', ',')+ '</b></td>'
        html+='</tr>'    
            
        html+='</tbody>'
    else:
        raise Http404

    return HttpResponse(
            html
        )
    #return HttpResponse(json_resultados, content_type="application/json")



@login_required()
@transaction.atomic
def consultar_nota_credito_electronica(request):
    #db = MySQLdb.connect(host="104.192.6.75, user="sa",passwd="U7BKm3eayFCn9cTx", db="FacturaNotaCreditoYDebito")
    with transaction.atomic():
        id = request.POST['id']
        try:
            factura = Movimiento.objects.get(id=id)
        except Movimiento.DoesNotExist:
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
        #Factura(01) NotaCredito(04) NotaDebito(05) GuiaRemision(06) ComprobanteRetencion(07)    
        codDoc='04'
        valor_razonSocial=Parametros.objects.get(clave='fe_razonSocial').valor
        razonSocial=valor_razonSocial
        
        id_f=Parametros.objects.get(clave='fe_factura_nota_credito').valor
             
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
        #CASO DE NOTA DE CREDITO O DEBITO
        try:
            factura_detalles = MovimientoNotaCredito.objects.get(movimiento_id=id)
        except MovimientoNotaCredito.DoesNotExist:
            factura_detalles = None
        
        codDocModificado='01'
        numDocModificado=factura_detalles.documento_venta.establecimiento+'-'+factura_detalles.documento_venta.punto_emision+'-'+factura_detalles.documento_venta.secuencial
        fechaEmisionDocSustento=factura_detalles.documento_venta.fecha_emision
        valorModificacion=factura.monto
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
    
        if factura:
            if factura.razon_social_id:
                razonSocialComprador=factura.razon_social.nombre
                identificacionComprador=factura.razon_social.ruc
                direccionComprador=factura.razon_social.direccion1
                email=factura.razon_social.email1
                #ruc=factura.razon_social.ruc
                if len(factura.razon_social.ruc)>9:
                    tipoIdentificacionComprador='04'
                    
                else:
                    tipoIdentificacionComprador='05'
                
                
            else:
                razonSocialComprador=factura.cliente.nombre_cliente
                email=factura.cliente.email1
                
                direccionComprador=factura.cliente.direccion1
                if len(factura.cliente.ruc)>2:
                    identificacionComprador=factura.cliente.ruc
                    tipoIdentificacionComprador='04'
                    #ruc=factura.cliente.ruc
                else:
                    identificacionComprador=factura.cliente.cedula
                    tipoIdentificacionComprador='05'
                    #ruc=factura.cliente.cedula
                    
                
                
            guiaRemision=''
                
            
            
            
            motivo=factura.descripcion
            direccion=factura.direccion
            telefono=factura.telefono
            direccionComprador=factura.direccion
            
            
            subtotal=float(factura.subtotal)
            totalSinImpuestos=subtotal
            totalDescuento=0
            importeTotal=factura.monto
            codigoPorcentajeICE=0
            tarifaICE=0
            baseICE=0
            valorICE=0
            baseIVA0=0
            valorIVA0=0
            
            
            baseIVA14=0
            valorIVA14=0
            propina=0
            
            if factura_detalles.lleva_iva:
                baseIVA12=subtotal
                valorIVA12=factura.iva
            
            else:
                baseIVA0=subtotal
                baseIVA12=0
                valorIVA12=0
                
            
            secuencialTransaccion=''
            tipoDocTransaccion=''
            id=id_f
            #PREGUNTAR POR EL ESTABLECIMIENTO Y PUNTO EMISION
            festablecimiento=factura.puntos_venta.establecimiento
            fpunto_emision=factura.puntos_venta.punto_emision
            fsecuencial=factura.nro_nota_credito
            logn_fsecuencial=len(str(fsecuencial))
            if logn_fsecuencial<9:
                fsecuencial=str(fsecuencial).zfill(9) 
            
            fecha_emision=factura.fecha_emision
        
            conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
            cursor = conn.cursor()
            sqlCommanf="INSERT INTO infoDocumentoCliente (id,ambiente,tipoEmision,razonSocial,nombreComercial,ruc,codDoc,estab,ptoEmi,secuencial,secuencialTransaccion,tipoDocTransaccion,dirMatriz,fechaEmision,dirEstablecimiento,contribuyenteEspecial,obligadoContabilidad,codDocModificado,numDocModificado,fechaEmisionDocSustento,valorModificacion,tipoIdentificacionComprador,guiaRemision,razonSocialComprador,identificacionComprador,totalSinImpuestos,totalDescuento,importeTotal,moneda,motivo,direccion,telefono,email,codigoPorcentajeICE,tarifaICE,baseICE,valorICE,baseIVA0,valorIVA0,baseIVA12,valorIVA12,direccionComprador,propina,baseIVA14,valorIVA14) values ("+str(id)+",'"+str(ambiente)+"','"+str(tipoEmision)+"','"+str(razonSocial)+"','"+str(nombreComercial)+"','"+str(ruc)+"','"+str(codDoc)+"','"+str(festablecimiento)+"','"+str(fpunto_emision)+"','"+str(fsecuencial)+"','"+str(secuencialTransaccion)+"','"+str(tipoDocTransaccion)+"','"+str(dirMatriz)+"','"+str(fecha_emision)+"','"+str(dirEstablecimiento)+"','"+str(contribuyenteEspecial)+"','"+str(obligadoContabilidad)+"','"+str(codDocModificado)+"','"+str(numDocModificado)+"','"+str(fechaEmisionDocSustento)+"',"+str(valorModificacion)+",'"+str(tipoIdentificacionComprador)+"','"+str(guiaRemision)+"','"+str(razonSocialComprador.encode('utf8'))+"','"+str(identificacionComprador)+"',"+str(totalSinImpuestos)+","+str(totalDescuento)+","+str(importeTotal)+",'"+str(moneda)+"','"+str(motivo.encode('utf8'))+"','"+str(direccion.encode('utf8'))+"','"+str(telefono)+"','"+str(email)+"','"+str(codigoPorcentajeICE)+"',"+str(tarifaICE)+","+str(baseICE)+","+str(valorICE)+","+str(baseIVA0)+","+str(valorIVA0)+","+str(baseIVA12)+","+str(valorIVA12)+",'"+str(direccionComprador)+"',"+str(propina)+","+str(baseIVA14)+","+str(valorIVA14)+")"
            cursor.execute(sqlCommanf)
            conn.commit()
            #post_id = cursor.lastrowid
            #post_id = factura.id
            post_id=id_f    
            
            secuencia=1
            
            codigoPrincipal=''
            codigoAuxiliar=''
            fdescripcion=''
            precioUnitario=0
            cantidad=0
            
            try:
                factura_detalle_venta = DocumentosVentaDetalle.objects.filter(documento_venta_id=factura_detalles.documento_venta_id).exclude(cantidad=0)
            except DocumentosVentaDetalle.DoesNotExist:
                factura_detalle_venta = None
            if  factura_detalle_venta:
                count=DocumentosVentaDetalle.objects.filter(documento_venta_id=factura_detalles.documento_venta_id).exclude(cantidad=0).count()
                if count:
                    print count
                    montoDetalle=factura.subtotal/count
                
                for f in factura_detalle_venta:
                    codigoPrincipal='0000000'
                    codigoAuxiliar='0000000'
                    fdescripcion=f.descripcion
                    
                    if factura_detalles.lleva_iva:
                        if iva=='12':
                            fcodigoPorcentajeIVA='02'
                        else:
                            if iva=='14':
                                fcodigoPorcentajeIVA='03'
                            else:
                                fcodigoPorcentajeIVA='0'
                                
                                
                        print fcodigoPorcentajeIVA    
                    
                        if iva:
                            fuprecio_iva=float(montoDetalle)*(float(iva)/100)
                            fsin_impuesto=float(montoDetalle)
                           
                        
                        precioUnitario=float(montoDetalle)/float(f.cantidad)
                        print precioUnitario
                    
                        fbaseIVA0=0
                        fvalorIVA0=0
                        fbaseIVA12=float(montoDetalle)
                        valorfIVA12=fbaseIVA12*(float(iva)/100)
                        
                        fvalorIVA12=valorfIVA12
                       
                    
                        
                        
                            
                            
                    else:
                        fuprecio_iva=0
                        fsin_impuesto=float(montoDetalle)
                        precioUnitario=float(montoDetalle)/float(f.cantidad)

                        
                        fbaseIVA0=float(montoDetalle)
                        fvalorIVA0=0
                        fbaseIVA12=0
                        valorfIVA12=0
                        fvalorIVA12=valorfIVA12
                        fcodigoPorcentajeIVA='0'
                        
                        
                        
                        
                    cantidad=f.cantidad
                    fdescuento=0
                    fprecioTotalSinImpuesto=montoDetalle
                    fcodigoPorcentajeICE=0
                    ftarifaICE=0
                    fbaseICE=0
                    fvalorICE=0
                    funidadMedida=''
                        
                    
                        
                    
                    sqlComman1="INSERT INTO detalleInfoDocumentoCliente (id,secuencia,codigoPrincipal,codigoAuxiliar,descripcion,cantidad,precioUnitario,descuento,precioTotalSinImpuesto,codigoPorcentajeICE,tarifaICE,baseICE,valorICE,baseIVA0,valorIVA0,baseIVA12,valorIVA12,unidadMedida,codigoPorcentajeIVA,baseIVA14,valorIVA14) values ("+str(post_id)+","+str(secuencia)+",'"+str(codigoPrincipal)+"','"+str(codigoAuxiliar)+"','"+str(fdescripcion)+"',"+str(cantidad)+","+str(precioUnitario)+","+str(fdescuento)+","+str(fprecioTotalSinImpuesto)+","+str(fcodigoPorcentajeICE)+","+str(ftarifaICE)+","+str(fbaseICE)+","+str(fvalorICE)+","+str(fbaseIVA0)+","+str(fvalorIVA0)+","+str(fbaseIVA12)+","+str(fvalorIVA12)+",'"+str(funidadMedida)+"','"+str(fcodigoPorcentajeIVA)+"',"+str(baseIVA14)+","+str(valorIVA14)+")"
                    
                    cursor.execute(sqlComman1)
                    conn.commit()
                    secuencia=secuencia+1
            
            
            
            try:
                factura_fpago = DocumentoVentaFormaPago.objects.filter(documento_venta_id=factura_detalles.documento_venta_id)
            except DocumentoVentaFormaPago.DoesNotExist:
                factura_fpago = None
            
            secuenciafpago=1
            if factura_fpago:
                for fp in factura_fpago:

                    if fp.forma_pago_ventas_id:
                        formaPago=fp.forma_pago_ventas.codigo
                        fptotal=fp.documento_venta.total
                        try:
                            v_plazo = Parametros.objects.get(clave='fe_dias_plazo').valor
                        except Parametros.DoesNotExist:
                            v_plazo = 15

                        # v_plazo=Parametros.objects.get(clave='fe_dias_plazo').valor
                        fpplazo = v_plazo
                        fpunidadTiempo = 'dias'
                        sqlComman2="INSERT INTO infoFormaPago (id,secuencia,formaPago,total,plazo,unidadTiempo) values ("+str(post_id)+","+str(secuenciafpago)+",'"+str(formaPago)+"',"+str(fptotal)+",'"+str(fpplazo)+"','"+str(fpunidadTiempo)+"')"
                        cursor.execute(sqlComman2)
                        conn.commit()


                        secuenciafpago=secuenciafpago+1



            html = 'Se ingreso la nota de credito electronicamente'
            factura.facturacion_eletronica = True
            factura.id_facturacion_eletronica = int(post_id)
            factura.save()
            try:
                param = Parametros.objects.get(clave='fe_factura_nota_credito')
            except Parametros.DoesNotExist:
                param = None
            if param:
                valor_f = int(post_id) + 1
                param.valor = valor_f
                param.save()
            
            
            return HttpResponse(html)
    
        else:
            raise Http404    
        
            
@login_required()
@transaction.atomic
def consultar_nota_debito_electronica(request):
    #db = MySQLdb.connect(host="104.192.6.75, user="sa",passwd="U7BKm3eayFCn9cTx", db="FacturaNotaCreditoYDebito")
    with transaction.atomic():
        id = request.POST['id']
        try:
            factura = Movimiento.objects.get(id=id)
        except Movimiento.DoesNotExist:
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
        
        tipoEmision='01'
        #Factura(01) NotaCredito(04) NotaDebito(05) GuiaRemision(06) ComprobanteRetencion(07)    
        codDoc='04'
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
        #CASO DE NOTA DE CREDITO O DEBITO
        try:
            factura_detalles = DocumentoAbono.objects.get(movimiento_id=id)
        except DocumentoAbono.DoesNotExist:
            factura_detalles = None
        
        codDocModificado='01'
        numDocModificado=factura_detalles.documento_compra.establecimiento+''+factura_detalles.documento_compra.punto_emision+''+factura_detalles.documento_compra.secuencial
        fechaEmisionDocSustento=factura_detalles.documento_compra.fecha_emision
        valorModificacion=factura_detalles.documento_compra.total
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
    
        if factura:
            razonSocialComprador=factura.proveedor.nombre_proveedor
            if factura.proveedor.ruc:
                identificacionComprador=factura.proveedor.ruc
                tipoIdentificacionComprador='04'
            else:
                identificacionComprador=factura.proveedor.cedula
                tipoIdentificacionComprador='05'
            direccionComprador=factura.proveedor.direccion1
            email=factura.proveedor.e_mail1
                #ruc=factura.razon_social.ruc
               
    
            guiaRemision=''
                
            motivo=factura.descripcion
            direccion=factura.proveedor.direccion1
            telefono=factura.proveedor.telefono1
            direccionComprador=factura.proveedor.direccion1
            
            iva_valor=float(factura.monto)*float(iva/100)
            subtotal=float(factura.monto)-iva_valor
            totalSinImpuestos=subtotal
            totalDescuento=0
            importeTotal=factura.monto
            codigoPorcentajeICE=0
            tarifaICE=0
            baseICE=0
            valorICE=0
            baseIVA0=0
            valorIVA0=0
            
            baseIVA12=subtotal
            valorIVA12=iva_valor
            
            secuencialTransaccion=''
            tipoDocTransaccion=''
            id=factura.id
            #PREGUNTAR POR EL ESTABLECIMIENTO Y PUNTO EMISION
            
            festablecimiento=factura.puntos_venta.establecimiento
            fpunto_emision=factura.puntos_venta.punto_emision
            fsecuencial=nro_nota_credito
            
            #---------------------------------------
            fecha_emision=factura.fecha_emision
        
            conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=FEDemo")
            cursor = conn.cursor()
            sqlCommanf="INSERT INTO infoDocumentoCliente (id,ambiente,tipoEmision,razonSocial,nombreComercial,ruc,codDoc,estab,ptoEmi,secuencial,secuencialTransaccion,tipoDocTransaccion,dirMatriz,fechaEmision,dirEstablecimiento,contribuyenteEspecial,obligadoContabilidad,codDocModificado,numDocModificado,fechaEmisionDocSustento,valorModificacion,tipoIdentificacionComprador,guiaRemision,razonSocialComprador,identificacionComprador,totalSinImpuestos,totalDescuento,importeTotal,moneda,motivo,direccion,telefono,email,codigoPorcentajeICE,tarifaICE,baseICE,valorICE,baseIVA0,valorIVA0,baseIVA12,valorIVA12,direccionComprador) values ("+str(id)+",'"+str(ambiente)+"','"+str(tipoEmision)+"','"+str(razonSocial)+"','"+str(nombreComercial)+"','"+str(ruc)+"','"+str(codDoc)+"','"+str(festablecimiento)+"','"+str(fpunto_emision)+"','"+str(fsecuencial)+"','"+str(secuencialTransaccion)+"','"+str(tipoDocTransaccion)+"','"+str(dirMatriz)+"','"+str(fecha_emision)+"','"+str(dirEstablecimiento)+"','"+str(contribuyenteEspecial)+"','"+str(obligadoContabilidad)+"','"+str(codDocModificado)+"','"+str(numDocModificado)+"','"+str(fechaEmisionDocSustento)+"',"+str(valorModificacion)+",'"+str(tipoIdentificacionComprador)+"','"+str(guiaRemision)+"','"+str(razonSocialComprador.encode('utf8'))+"','"+str(identificacionComprador)+"',"+str(totalSinImpuestos)+","+str(totalDescuento)+","+str(importeTotal)+",'"+str(moneda)+"','"+str(motivo.encode('utf8'))+"','"+str(direccion.encode('utf8'))+"','"+str(telefono)+"','"+str(email)+"','"+str(codigoPorcentajeICE)+"',"+str(tarifaICE)+","+str(baseICE)+","+str(valorICE)+","+str(baseIVA0)+","+str(valorIVA0)+","+str(baseIVA12)+","+str(valorIVA12)+",'"+str(direccionComprador)+"')"
            cursor.execute(sqlCommanf)
            conn.commit()
            
            #post_id = cursor.lastrowid
            post_id = factura.id
    
            
            secuencia=1
            
            codigoPrincipal=''
            codigoAuxiliar=''
            fdescripcion=''
            precioUnitario=0
            cantidad=0
            
            try:
                factura_detalle = DocumentosCompraDetalle.objects.filter(documento_compra_id=factura_detalles.documento_compra_id)
            except DocumentosCompraDetalle.DoesNotExist:
                factura_detalle = None
            if  factura_detalle:
                for f in factura_detalle:
                    codigoPrincipal='0000000'
                    codigoAuxiliar='0000000'
                    fdescripcion=f.descripcion
                    
                    
                    if iva=='12':
                        fuprecio_iva=f.base_iva*0.12
                    
                    
                    fsin_impuesto=float(f.base_iva)-float(fuprecio_iva)
                        
                    precioUnitario=f.base_iva
                    cantidad=f.cantidad
                    fdescuento=0
                    fprecioTotalSinImpuesto=f.subtotal
                    fcodigoPorcentajeICE=0
                    ftarifaICE=0
                    fbaseICE=0
                    fvalorICE=0
                    fbaseIVA0=0
                    fvalorIVA0=0
                    fbaseIVA12=f.subtotal
                    valorfIVA12=f.subtotal*0.12
                    
                    fvalorIVA12=valorfIVA12
                    funidadMedida=''
                    fcodigoPorcentajeIVA=''
                    
                    if iva=='12':
                        fcodigoPorcentajeIVA='02'
                    else:
                        if iva=='14':
                            fcodigoPorcentajeIVA='03'
                        else:
                            fcodigoPorcentajeIVA='0'
                        
                    
                    sqlComman1="INSERT INTO detalleInfoDocumentoCliente (id,secuencia,codigoPrincipal,codigoAuxiliar,descripcion,cantidad,precioUnitario,descuento,precioTotalSinImpuesto,codigoPorcentajeICE,tarifaICE,baseICE,valorICE,baseIVA0,valorIVA0,baseIVA12,valorIVA12,unidadMedida,codigoPorcentajeIVA) values ("+str(post_id)+","+str(secuencia)+",'"+str(codigoPrincipal)+"','"+str(codigoAuxiliar)+"','"+str(fdescripcion)+"',"+str(cantidad)+","+str(precioUnitario)+","+str(fdescuento)+","+str(fprecioTotalSinImpuesto)+","+str(fcodigoPorcentajeICE)+","+str(ftarifaICE)+","+str(fbaseICE)+","+str(fvalorICE)+","+str(fbaseIVA0)+","+str(fvalorIVA0)+","+str(fbaseIVA12)+","+str(fvalorIVA12)+",'"+str(funidadMedida)+"','"+str(fcodigoPorcentajeIVA)+"')"
                    cursor.execute(sqlComman1)
                    conn.commit()
                    secuencia=secuencia+1
            
            
            
            # try:
            #     factura_fpago = DocumentoVentaFormaPago.objects.filter(documento_venta_id=factura_detalles.documento_venta_id)
            # except DocumentoVentaFormaPago.DoesNotExist:
            #     factura_fpago = None
            # 
            # secuenciafpago=1
            # if factura_fpago:
            #     formaPago=factura_fpago.forma_pago_ventas.codigo
            #     fptotal=factura_fpago.documento_venta.total
            #     v_plazo=Parametros.objects.get(clave='fe_dias_plazo').valor
            #     fpplazo=v_plazo
            #     fpunidadTiempo='dias'
            #     sqlComman2="INSERT INTO infoFormaPago (id,secuencia,formaPago,total,plazo,unidadTiempo) values ("+str(post_id)+","+str(secuenciafpago)+",'"+str(formaPago)+"',"+str(fptotal)+",'"+str(fpplazo)+"','"+str(fpunidadTiempo)+"')"
            #     print sqlComman2
            #     cursor.execute(sqlComman2)
            #     conn.commit()
            #     
            #     
            #     secuenciafpago=secuenciafpago+1
            secuenciafpago=1
            formaPago='01'
            fptotal=factura.monto
            v_plazo=Parametros.objects.get(clave='fe_dias_plazo').valor
            fpplazo=v_plazo
            fpunidadTiempo='dias'
            sqlComman2="INSERT INTO infoFormaPago (id,secuencia,formaPago,total,plazo,unidadTiempo) values ("+str(post_id)+","+str(secuenciafpago)+",'"+str(formaPago)+"',"+str(fptotal)+",'"+str(fpplazo)+"','"+str(fpunidadTiempo)+"')"
            print sqlComman2
            cursor.execute(sqlComman2)
            conn.commit()


            html='Se ingreso la nota de debito electronicamente'
            factura.facturacion_eletronica=True
            factura.save()
            
            return HttpResponse(html)
    
        else:
            raise Http404    
        
             
@login_required()
@transaction.atomic
def consultar_datos_nota_credito_electronica(request,pk):
    #db = MySQLdb.connect(host="104.192.6.75, user="sa",passwd="U7BKm3eayFCn9cTx", db="FacturaNotaCreditoYDebito")
    with transaction.atomic():
        id = pk
        try:
            factura = Movimiento.objects.get(id=id)
        except Movimiento.DoesNotExist:
            factura = None
      
        
        if factura:
            if factura.id_facturacion_eletronica:
                conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
                cursor = conn.cursor()
                sqlCommanf="select claveAcceso,estado,numeroAutorizacion,fechaAutorizacion,msjeSRI,estadoCorreo,msjeCorreo,estadoPdf,msjePdf,secuencial  from infoDocumentoCliente where id="+str(factura.id_facturacion_eletronica)+";"
                cursor.execute(sqlCommanf)
                row = cursor.fetchall()
                conn.commit()
                
                
                return render_to_response('movimientos/consultar_datos_nota_electronica.html', {'row': row}, RequestContext(request))
    
        else:
            raise Http404
