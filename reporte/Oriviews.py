# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, \
    eliminarByPkView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.contrib import messages
import simplejson as json
import datetime
import time
from .models import *
from clientes.models import *
from ambiente.models import *
from inventario.models import *
from django.db import connection,IntegrityError, transaction
from django.core.serializers.json import DjangoJSONEncoder
from proveedores.models import *
from reunion.models import *
from django.db.models import Sum
from config.models import *
from pedido.models import *
from proforma.models import *
from ordenproduccion.models import *
from facturacion.models import *
from subordenproduccion.models import *
from OrdenesdeCompra.models import *
from ordenIngreso.models import *
from ordenEgreso.models import *
from recursos_humanos.models import *
from contabilidad.models import PlanDeCuentas
from django.utils.encoding import smart_str, smart_unicode
from transacciones.models import DocumentosRetencionDetalleCompra,DocumentoRetencionDetalleVenta
from django.views.generic import TemplateView

from django.forms.extras.widgets import *
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta

import csv
from django.utils.encoding import *


import locale
# from login.lib.tools import Tools


import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
# from config.models import Mensajes
from decimal import Decimal


from login.lib.tools import Tools
from django.contrib import auth
from datetime import datetime, timedelta


# Create your views here.
def principal(request):
    cursor = connection.cursor();

    cursor.execute(
        "SELECT  distinct reunion.codigo,reunion.motivo,reunion.fecha,reunion.tiempo_respuesta,proforma.codigo, proforma.fecha FROM reunion LEFT JOIN proforma ON proforma.reunion_codigo=reunion.codigo");
    row = cursor.fetchall();

    return render_to_response('principal/index.html', {'row': row}, RequestContext(request))


def reportepedido(request):
    cursor = connection.cursor();

    cursor.execute(
        "SELECT  distinct reunion.codigo,reunion.motivo,reunion.fecha,reunion.tiempo_respuesta,proforma.codigo, proforma.fecha FROM reunion LEFT JOIN proforma ON proforma.reunion_codigo=reunion.codigo");
    row = cursor.fetchall();
    cliente = Cliente.objects.values('id_cliente', 'codigo_cliente', 'nombre_cliente')

    return render_to_response('pedido/pendiente.html', {'row': row, 'cliente': cliente,}, RequestContext(request))


@csrf_exempt
def obtenerPedidoPendiente(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor.execute(
            "select p.id,p.codigo,c.nombre_cliente,p.fecha,p.fechaentrega,p.abono,p.proforma_codigo from pedido p,cliente c where p.cliente_id=c.id_cliente and p.cliente_id=" + cliente);
        row = cursor.fetchall();

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            ped = PedidoDetalle.objects.filter(pedido_id=p[0])
            html += '<tr><td colspan="4"><b>Pedido#&nbsp;&nbsp;' + str(
                p[1]) + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(p[2]) + '<b></td></tr>'
            html += '<tr><td colspan="4">Ingreso' + str(p[3]) + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Entrega:' + str(
                p[4]) + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Abono:' + str(p[5]) + '</td></tr>'
            html += '<tr><td>Articulo </td><td>Cantidad </td><td>Proforma </td><td>Op </td></tr>'
            for pe in ped:
                html += '<tr><td>' + str(pe.nombre.encode('utf8')) + '</td>'
                html += '<td>' + str(pe.cantidad) + '</td>'
                html += '<td>' + str(p[6]) + '</td>'
                op = OrdenProduccion.objects.filter(pedido_detalle_id=pe.id)
            if op:
                html += '<td>'
                for op1 in op:
                    html += str(op1.codigo) + '<br />'
                html += '</td></tr>'
            else:
                html += '<td></td></tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteordenproduccion(request):
    cliente = Cliente.objects.values('id_cliente', 'codigo_cliente', 'nombre_cliente')

    return render_to_response('ordenproduccion/cliente.html', {'cliente': cliente}, RequestContext(request))


@csrf_exempt
def obtenerOrdenProduccionCliente(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor.execute(
            "select p.id,p.tipo,p.codigo,p.fecha,p.descripcion,p.detalle,p.cantidad, p.codigo_item,p.pedido_codigo,c.nombre_cliente from orden_produccion p,cliente c where p.cliente_id=c.id_cliente and p.cliente_id=" + cliente + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");
        row = cursor.fetchall();

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            html += '<tr><td>' + str(p[1].encode('utf8')) + '</td>'
            html += '<td>' + str(p[2]) + '</td>'
            html += '<td>' + str(p[3]) + '</td>'
            html += '<td>' + str(p[4].encode('utf8')) + ' ' + str(p[5].encode('utf8')) + '</td>'
            html += '<td>' + str(p[6]) + '</td>'
            html += '<td>' + str(p[7].encode('utf8')) + '</td>'
            html += '<td>' + str(p[8].encode('utf8')) + '</td></tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteguias(request):
    cursor = connection.cursor();

    cursor.execute(
        "SELECT  distinct reunion.codigo,reunion.motivo,reunion.fecha,reunion.tiempo_respuesta,proforma.codigo, proforma.fecha FROM reunion LEFT JOIN proforma ON proforma.reunion_codigo=reunion.codigo");
    row = cursor.fetchall();
    cliente = Cliente.objects.values('id_cliente', 'codigo_cliente', 'nombre_cliente')

    return render_to_response('guia/emitidas.html', {'row': row, 'cliente': cliente,}, RequestContext(request))


@csrf_exempt
def obtenerGuiaEmitida(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor.execute(
            "select distinct p.guia_id,p.nro_guia,p.fecha_inicio,c.nombre_cliente,v.descripcion,p.aprobada,t.descripcion,p.egreso,p.ingreso,ec.nombre from facturacion_guiaremision p,cliente c,vehiculo v, empleados_chofer ec, empleados_empleado,tipo_guia t where p.cliente_id=c.id_cliente and t.id=p.tipo_guia_id and v.id=p.vehiculo_id and ec.chofer_id=p.chofer_id and p.cliente_id=" + cliente + " and p.fecha_inicio>='" + fechainicial + "'and p.fecha_inicio<='" + fechafin + "'");
        row = cursor.fetchall();

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            ped = GuiaDetalle.objects.filter(guia_id_id=str(p[0]))
            html += '<tr style="background:#f0f3f5" ><td colspan="4"><b>Guia#&nbsp;&nbsp;' + str(
                p[1]) + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(
                p[2]) + '&nbsp;&nbsp;&nbsp;&nbsp;' + str(p[3]) + '<b></td></tr>'
            html += '<tr ><td colspan="4">Chofer:&nbsp;' + str(
                p[9]) + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Vehiculo:&nbsp;' + str(
                p[4]) + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </td></tr>'
            html += '<tr style="background:#f0f3f5" ><td colspan="4">Tipo Guia:&nbsp;' + str(
                p[6]) + '&nbsp;&nbsp;&nbsp;Ingreso:&nbsp;' + str(p[8]) + '&nbsp;&nbsp;&nbsp; Egreso:' + str(
                p[7]) + '</td></tr>'

            html += '<tr style="background:#f0f3f5" ><th>Articulo </th><th>Cantidad </th></tr>'
            for pe in ped:
                html += '<tr><td>' + str(pe.producto_id) + '</td>'
                html += '<td>' + str(
                    pe.cantidad) + '</td></tr><tr style="background:white"><td colspan="2">&nbsp;&nbsp;&nbsp;</td></tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reportepedidoporfacturar(request):
    cursor = connection.cursor();

    cursor.execute(
        "SELECT  distinct reunion.codigo,reunion.motivo,reunion.fecha,reunion.tiempo_respuesta,proforma.codigo, proforma.fecha FROM reunion LEFT JOIN proforma ON proforma.reunion_codigo=reunion.codigo");
    row = cursor.fetchall();
    cliente = Cliente.objects.values('id_cliente', 'codigo_cliente', 'nombre_cliente')

    return render_to_response('pedido/porfacturar.html', {'row': row, 'cliente': cliente,}, RequestContext(request))


@csrf_exempt
def obtenerPedidoPorFacturar(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor.execute(
            "select p.id,p.codigo,c.nombre_cliente,p.fecha,p.fechaentrega,p.abono,p.proforma_codigo,p.total from pedido p,cliente c where p.cliente_id=c.id_cliente and (p.abona IS NULL or p.abona=false) and p.cliente_id=" + cliente + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");
        row = cursor.fetchall();

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:

            html += '<tr><td>' + str(p[1]) + '</td><td>' + str(p[4]) + '</td><td>' + str(p[2].encode('utf8')) + '</td>'
            ped = PedidoDetalle.objects.filter(pedido_id=str(p[0]))
            html += '<td>'
            for pe in ped:
                html += '' + str(pe.nombre.encode('utf8')) + '&nbsp;&nbsp;' + str(pe.cantidad) + ' '
                op = OrdenProduccion.objects.get(pedido_detalle_id=pe.id)
                html += '<b>' + str(op.tipo) + ':' + str(op.codigo) + '</b>'
                html += '<br/>'
            html += '</td>'
            html += '<td>' + str(p[7]) + '</td></tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteglobal(request):
    cursor = connection.cursor();

    cursor.execute(
        "SELECT  distinct reunion.codigo,reunion.motivo,reunion.fecha,reunion.tiempo_respuesta,proforma.codigo, proforma.fecha FROM reunion LEFT JOIN proforma ON proforma.reunion_codigo=reunion.codigo");
    row = cursor.fetchall();
    cliente = Cliente.objects.values('id_cliente', 'codigo_cliente', 'nombre_cliente')

    return render_to_response('pedido/global.html', {'row': row, 'cliente': cliente,}, RequestContext(request))


@csrf_exempt
def obtenerGlobal(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor.execute(
            "select p.id,p.codigo,c.nombre_cliente,p.fecha,p.total from proforma p,cliente c where p.cliente_id=c.id_cliente and p.cliente_id=" + cliente + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");
        row = cursor.fetchall();
        print(
        "select p.id,p.codigo,c.nombre_cliente,p.fecha,p.total from proforma p,cliente c where p.cliente_id=c.id_cliente and p.cliente_id=" + str(
            cliente) + "and p.fecha>='" + str(fechainicial) + "'and p.fecha<='" + str(fechafin) + "'")

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:

            html += '<tr><td>' + str(p[1].encode('utf8')) + '</td><td>' + str(p[4]) + '</td><td>' + str(
                p[2].encode('utf8')) + '</td>'
            pedido = Pedido.objects.get(proforma_codigo=str(p[1]))
            if pedido:
                print("entro")
                html += '<td>' + str(pedido.codigo) + '</td>'
                ped = PedidoDetalle.objects.filter(pedido_id=str(pedido.id))
                html += '<td>'
                for pe in ped:
                    # html+='<tr>'
                    # html+='<td>'
                    html += '' + str(pe.nombre.encode('utf8')) + '&nbsp;&nbsp;' + str(pe.cantidad) + ' '
                    # html+='</td>'
                    # html+='<td>'

                    op = OrdenProduccion.objects.get(pedido_detalle_id=pe.id)

                    # html+='</td>'
                    # html+='<td>'
                    if op:
                        subop = SubordenProduccion.objects.filter(orden_produccion_id=op.id)
                    html += '<b>' + str(op.tipo) + ':' + str(op.codigo) + '</b>'
                    if subop:
                        for sp in subop:
                            # html+='<tr>'
                            # html+='<td>'
                            html += '<b>' + str(sp.areas.descripcion.encode('utf8')) + '</b>&nbsp;'
                            if sp.finalizada:
                                html += 'Finalizado'
                            else:
                                html += 'En Proceso'
                                # html+='</td>'
                            html += '|'
                            # html+='</tr>'
                            # html+='</td>'
                    html += '<br/>'
                    # html+='</tr>'
                html += '</td>'

            else:
                html += '<td></td>'

            html += '<td></td></tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteliquidacioncomisiones(request):
    vendedor = Vendedor.objects.values('id', 'codigo', 'nombre')

    return render_to_response('ventas/liquidacion_comisiones.html', {'vendedor': vendedor,}, RequestContext(request))


@csrf_exempt
def obtenerLiquidacionesComisiones(request):
    if request.method == 'POST':
        vendedor = request.POST.get('vendedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor.execute(
            "select distinct p.id,p.tipo,p.fecha,p.codigo,p.descripcion,p.detalle,p.cantidad,p.codigo,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva,p.total from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + vendedor + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");
        row = cursor.fetchall();

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            html += '<tr><td>' + str(p[2]) + '</td>'
            html += '<td>' + str(p[3]) + '</td>'
            html += '<td>' + str(p[8].encode('utf8')) + '</td>'
            html += '<td>'
            ped = ProformaDetalle.objects.filter(proforma_id=str(p[0]))
            for pe in ped:
                html += '' + str(pe.cantidad) + ' ' + str(pe.nombre.encode('utf8')) + '<br />'
            html += '</td>'
            html += '<td>' + str(p[10]) + '</td>'
            html += '<td>' + str(p[11]) + '</td>'
            html += '<td>' + str(p[12]) + '</td>'
            html += '<td></td>'
            html += '<td></td>'
            html += '<td></td>'
            html += '<td></td>'
            html += '<td></td>'
            html += '<td></td>'
            html += '<td></td>'
            html += '<td></td></tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteDiarioVentas(request):
    vendedor = Vendedor.objects.values('id', 'codigo', 'nombre')

    return render_to_response('ventas/diario_ventas.html', {'vendedor': vendedor,}, RequestContext(request))


@csrf_exempt
def obtenerDiarioVentas(request):
    if request.method == 'POST':
        vendedor = request.POST.get('vendedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor1 = connection.cursor();

        if vendedor == '0':
            cursor1.execute(
                "select distinct v.id,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");

        else:
            cursor1.execute(
                "select distinct v.id,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and v.id=" + vendedor + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");

        row1 = cursor1.fetchall();

        total = 0
        descuento = 0
        porcentaje = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p1 in row1:
            total = 0
            descuento = 0
            porcentaje = 0
            subtotal = 0
            iva = 0
            html += '<tr><th colspan="9"> ' + str(p1[1]) + '</th></tr>'
            cursor.execute(
                "select distinct p.id,p.tipo,p.fecha,p.codigo,p.descripcion,p.detalle,p.cantidad,p.codigo,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva,p.total,p.porcentaje_descuento,p.descuento,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");
            row = cursor.fetchall();
            html = ''
            for p in row:
                html += '<tr><td>' + str(p[2]) + '</td>'
                html += '<td>' + str(p[3]) + '</td>'
                html += '<td></td>'
                html += '<td>' + str(p[8]) + '</td>'
                html += '<td>'
                ped = ProformaDetalle.objects.filter(proforma_id=str(p[0]))
                for pe in ped:
                    html += '' + str(pe.cantidad) + ' ' + str(pe.nombre.encode('utf8')) + '<br />'
                html += '</td>'
                html += '<td>' + str(p[10]) + '</td>'
                html += '<td>' + str(p[13]) + '</td>'

                html += '<td>' + str(p[14]) + '</td>'

                html += '<td>' + str(p[11]) + '</td>'
                html += '<td>' + str(p[12]) + '</td>'
                html += '</tr>'
                iva = iva + p[11]
                total = total + p[12]
                porcentaje = porcentaje + p[13]
                descuento = descuento + p[14]
                subtotal = subtotal + p[10]
            html += '<tr><th colspan="5">Total de ' + str(p[15]) + '</th>'
            html += '<th>' + str(subtotal) + '</th>'
            html += '<th>' + str(porcentaje) + '</th>'
            html += '<th>' + str(descuento) + '</th>'
            html += '<th>' + str(iva) + '</th>'
            html += '<th>' + str(total) + '</th>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteDiarioGuias(request):
    vendedor = Vendedor.objects.values('id', 'codigo', 'nombre')

    return render_to_response('ventas/diario_guias.html', {'vendedor': vendedor,}, RequestContext(request))


@csrf_exempt
def obtenerDiarioGuias(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor.execute(
            "select distinct p.guia_id,p.nro_guia,p.fecha_inicio,c.nombre_cliente,v.descripcion,p.aprobada,t.descripcion,p.egreso,p.ingreso,ec.nombre,p.partida,p.destino from facturacion_guiaremision p,cliente c,vehiculo v, empleados_chofer ec, empleados_empleado,tipo_guia t where p.cliente_id=c.id_cliente and t.id=p.tipo_guia_id and v.id=p.vehiculo_id and ec.chofer_id=p.chofer_id and p.fecha_inicio>='" + fechainicial + "'and p.fecha_inicio<='" + fechafin + "'");
        row = cursor.fetchall();
        total = 0
        descuento = 0
        porcentaje = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            html += '<tr><td>' + str(p[2]) + '</td>'
            html += '<td>' + str(p[1]) + '</td>'
            html += '<td></td>'
            html += '<td>' + str(p[10]) + '</td>'
            html += '<td>' + str(p[11]) + '</td>'
            html += '<td>' + str(p[3]) + '</td>'
            html += '<td>'
            ped = GuiaDetalle.objects.filter(guia_id_id=str(p[0]))
            for pe in ped:
                html += '' + str(pe.cantidad) + ' ' + str(pe.producto_id) + '<br />'
            html += '</td>'
            html += '<td>' + str(p[6]) + '</td>'

            html += '<td>' + str(p[8]) + '</td>'
            html += '<td>' + str(p[7]) + '</td>'

            html += '</tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def principalInventario(request):
    cursor = connection.cursor();

    cursor.execute(
        "SELECT  distinct reunion.codigo,reunion.motivo,reunion.fecha,reunion.tiempo_respuesta,proforma.codigo, proforma.fecha FROM reunion LEFT JOIN proforma ON proforma.reunion_codigo=reunion.codigo");
    row = cursor.fetchall();

    return render_to_response('principal/principal_inventario.html', {'row': row}, RequestContext(request))


def reporteInventario(request):
    bodega = Bodega.objects.values('id', 'codigo_bodega', 'nombre')
    tipos = TipoProducto.objects.values('id', 'codigo', 'descripcion')

    return render_to_response('inventario/inventario.html', {'bodega': bodega, 'tipos': tipos}, RequestContext(request))


@csrf_exempt
def obtenerInventario(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        tipos = request.POST.get('tipos')
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        cursor = connection.cursor();
        sql=''
        if tipos == '0':
            sql+="select distinct pb.producto_bodega_id,pb.producto_id,p.codigo_producto,p.descripcion_producto,pb.cantidad,pb.bodega_id,b.codigo_bodega,b.nombre,p.cant_maxima,p.cant_minimia,t.descripcion,p.costo,p.unidad from producto_en_bodega pb,producto p,bodega b,tipo_producto t where pb.producto_id=p.producto_id and b.id=pb.bodega_id and p.tipo_producto=t.id and pb.bodega_id=" + bodega

        else:
            sql +="select distinct pb.producto_bodega_id,pb.producto_id,p.codigo_producto,p.descripcion_producto,pb.cantidad,pb.bodega_id,b.codigo_bodega,b.nombre,p.cant_maxima,p.cant_minimia,t.descripcion,p.costo,p.unidad from producto_en_bodega pb,producto p,bodega b,tipo_producto t where pb.producto_id=p.producto_id and b.id=pb.bodega_id and p.tipo_producto=t.id and p.tipo_producto=" + tipos + " and pb.bodega_id=" + bodega

        if codigo!= '':
            sql +=" and p.codigo_producto like '%" +codigo+ "%'"
        if nombre!= '':
            sql +=" and p.descripcion_producto like '%" +nombre+ "%'"
        cursor.execute(sql);
        row = cursor.fetchall();
        total_cantidad = 0
        total_costo = 0.0
        total_c = 0
        total_valor=0
        cant=0
        cost=0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            cost = 0
            cant =0
            html += '<tr><td>' + str(p[2]) + '</td>'
            html += '<td>' + str(p[3].encode('utf8')) + '</td>'
            html += '<td>' + str(p[12])+ '</td>'
            if p[4] < p[9]:
                html += '<td style="font-weight:bold;color:red">' + str(p[4]) + '</td>'
            else:
                html += '<td>' + str(p[4]) + '</td>'
            #html += '<td>' + str(p[8]) + '</td>'
            #html += '<td>' + str(p[9]) + '</td>'
            if p[11]:
                cls=p[11]*1
            else:
                cls=0
            html += '<td>' + str(round(cls,2)) + '</td>'
            if p[4]:
                cant=p[4]
            if p[11]:
                cost=p[11]
            total_c=round(cant*cost,2)
            html += '<td>' + str(total_c) + '</td>'
            total_cantidad = round((total_cantidad + p[4]),2)
            total_valor = total_valor + total_c
	    #total_kit=float(p[4])*float(p[11])
	    #html += '<td>' + str(total_kit) + '</td>'
            if p[11]:
                total_costo = round(total_costo + p[11],2)
            html += '</tr>'
        html += '<tr><td colspan="3"><b>Total</b></td>'
        html += '<td><b>' + str(total_cantidad) + '</b></td>'
        html += '<td><b>' + str(total_costo) + '</b></td>'
        html += '<td><b>' + str(total_valor) + '</b></td>'
        html += '</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteOrdenCompra(request):
    proveedor = Proveedor.objects.values('proveedor_id', 'codigo_proveedor', 'nombre_proveedor')

    return render_to_response('inventario/ordenes_compra.html', {'proveedor': proveedor,}, RequestContext(request))


@csrf_exempt
def obtenerOrdenCompra(request):
    if request.method == 'POST':
        proveedor = request.POST.get('proveedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor()
        sql="select distinct p.compra_id,p.nro_compra,p.fecha,p.notas,p.bodega_id,p.proveedor_id,c.nombre_proveedor,p.subtotal,p.impuesto_monto,p.total,b.nombre from orden_compra p,proveedor c,bodega b where p.proveedor_id=c.proveedor_id and b.id=p.bodega_id"
        if proveedor != '0':
            sql+=" and p.proveedor_id=" + proveedor
        else:
            print("entro no proveedor")

        print fechainicial
        print("fecha inicial")
        if fechainicial == '0':
            print("entro no feccha inicial")

        else:
            sql += " and p.fecha>='" + fechainicial + "'"
        if fechafin == '0':
            print("entro no fecha final")

        else:
            sql += " and p.fecha<='" + fechafin + "'"


        sql+=" order by p.fecha"
        cursor.execute(sql)

        row = cursor.fetchall()
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:

            ped = ComprasDetalle.objects.filter(compra_id=str(p[0]))
            cont=0
            for pe in ped:
                html += '<tr>'
                cont=cont+1
                if cont==1:
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[2]) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[1]) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[6].encode('utf8')) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[3].encode('utf8')) + '</td>'
                html += '<td>'
                html += ''+str(pe.producto.codigo_producto) + '</td><td>'  + str(pe.producto.descripcion_producto.encode('utf8'))+'</td><td> ' + str(pe.cantidad) + '</td><td> ' + str(pe.precio_compra) + '</td>'
                if cont == 1:
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[7]) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[8]) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[9]) + '</td>'
                    total = total + p[9]
                    subtotal = subtotal + p[7]
                    iva = iva + p[8]
                html += '</tr>'
        html += '<tr><td colspan="7"></td>'
        html += '<td></td>'
        html += '<td><b>' + str(subtotal) + '</b></td>'
        html += '<td><b>' + str(iva) + '</b></td>'
        html += '<td><b>' + str(total) + '</b></td>'
        html += '</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteOrdenIngreso(request):
    bodega = Bodega.objects.values('id', 'codigo_bodega', 'nombre')

    return render_to_response('inventario/ordenes_ingreso.html', {'bodega': bodega,}, RequestContext(request))


@csrf_exempt
def obtenerOrdenIngreso(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor.execute(
            "select distinct p.id,p.codigo,p.fecha,p.notas,p.comentario,p.bodega_id,p.cliente_id,p.aprobada,p.orden_produccion_codigo,b.nombre from orden_ingreso p,bodega b where b.id=p.bodega_id and p.bodega_id=" + bodega + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            html += '<tr><td>' + str(p[2]) + '</td>'
            html += '<td>' + str(p[1]) + '</td>'
            html += '<td>' + str(p[3]) + '</td>'
            html += '<td>' + str(p[4]) + '</td>'
            html += '<td>' + str(p[8]) + '</td>'

            html += '<td>'
            ped = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=str(p[0]))
            for pe in ped:
                html += '' + str(pe.cantidad) + ' ' + str(pe.producto) + '<br />'
            html += '</td>'
            html += '<td>'
            if p[7]:
                html += 'Aprobada'
            html += '</td>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteOrdenEgreso(request):
    bodega = Bodega.objects.values('id', 'codigo_bodega', 'nombre')

    return render_to_response('inventario/ordenes_egreso.html', {'bodega': bodega,}, RequestContext(request))


@csrf_exempt
def obtenerOrdenEgreso(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();

        sql = "select distinct p.id,p.codigo,p.fecha,p.notas,p.comentario,p.bodega_id,p.aprobada,p.orden_produccion_codigo,b.nombre from orden_egreso p,bodega b where b.id=p.bodega_id and p.bodega_id=" + bodega

        if fechainicial == '0':
            print("entro no feccha inicial")

        else:
            sql += " and p.fecha>='" + fechainicial + "'"
        if fechafin == '0':
            print("entro no fecha final")

        else:
            sql += " and p.fecha<='" + fechafin + "'"

        sql += " order by p.fecha"
        cursor.execute(sql)
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        total=0
        cantidad=0
        costo=0
        for p in row:

            ped = OrdenEgresoDetalle.objects.filter(orden_egreso_id=str(p[0]))
            cont=0
            for pe in ped:
                cont=cont+1

                html += '<tr>'
                if cont == 1:
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[2]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[1]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[3].encode('utf8'

                                                                                                                  )) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[4].encode('utf8')) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[7].encode('utf8')) + '</td>'

                html += ' <td> ' + str(pe.producto.codigo_producto.encode('utf8')) + ' </td>'
                html += ' <td> ' + str(pe.producto.descripcion_producto.encode('utf8')) + ' </td>'
                html += '<td>' + str(pe.cantidad) + '</td>'
                html += '<td>'+str(pe.precio_compra)+'</td><td>'+str(pe.total)+'</td>'
                html += '</tr>'
                total = total + pe.total
                cantidad = cantidad + pe.cantidad
                costo = costo + pe.precio_compra

        html += '<tr><td colspan="6"></td>'
        html += '<td><b>Total</b></td>'
        html += '<td><b>' + str(cantidad) + '</b></td>'
        html += '<td><b>' + str(costo) + '</b></td>'
        html += '<td><b>' + str(total) + '</b></td>'
        html += '</tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteDiarioVentasActual(request):
    vendedor = Vendedor.objects.values('id', 'codigo', 'nombre')

    return render_to_response('ventas/diario_ventas_actual.html', {'vendedor': vendedor,}, RequestContext(request))


@csrf_exempt
def obtenerDiarioVentasActual(request):
    if request.method == 'POST':
        vendedor = request.POST.get('vendedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor1 = connection.cursor();

        if vendedor == '0':
            cursor1.execute(
                "select distinct v.id,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");

        else:
            cursor1.execute(
                "select distinct v.id,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and v.id=" + vendedor + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");

        row1 = cursor1.fetchall();

        total = 0
        descuento = 0
        porcentaje = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p1 in row1:
            total = 0
            descuento = 0
            porcentaje = 0
            subtotal = 0
            iva = 0
            html += '<tr><th colspan="9"> ' + str(p1[1]) + '</th></tr>'
            cursor.execute(
                "select distinct p.id,p.tipo,p.fecha,p.codigo,p.descripcion,p.detalle,p.cantidad,p.codigo,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva,p.total,p.porcentaje_descuento,p.descuento,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");
            row = cursor.fetchall();
            for p in row:
                html += '<tr><td>' + str(p[3]) + '</td>'
                html += '<td>' + str(p[2]) + '</td>'
                html += '<td></td>'
                html += '<td>' + str(p[8]) + '</td>'
                html += '<td>'
                ped = ProformaDetalle.objects.filter(proforma_id=str(p[0]))
                for pe in ped:
                    html += '' + str(pe.cantidad) + ' ' + str(pe.nombre) + '<br />'
                html += '</td>'
                html += '<td>MUEDIRSA</td>'
                html += '<td>' + str(p[10]) + '</td>'
                html += '<td>' + str(p[10]) + '</td>'
                html += '<td>' + str(p[13]) + '</td>'

                html += '<td>' + str(p[14]) + '</td>'
                html += '<td>' + str(p[10]) + '</td>'
                html += '<td>' + str(p[11]) + '</td>'
                html += '<td>' + str(p[12]) + '</td>'
                html += '</tr>'
                iva = iva + p[11]
                total = total + p[12]
                porcentaje = porcentaje + p[13]
                descuento = descuento + p[14]
                subtotal = subtotal + p[10]
            html += '<tr><th colspan="5">Total de ' + str(p[15]) + '</th>'
            html += '<th>0</th>'
            html += '<th>' + str(subtotal) + '</th>'
            html += '<th>' + str(subtotal) + '</th>'
            html += '<th>' + str(porcentaje) + '</th>'
            html += '<th>' + str(descuento) + '</th>'
            html += '<th>' + str(subtotal) + '</th>'
            html += '<th>' + str(iva) + '</th>'
            html += '<th>' + str(total) + '</th>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteGuiasGeneral(request):
    cliente = Cliente.objects.values('id_cliente', 'nombre_cliente')
    tipos = TipoGuia.objects.all()

    return render_to_response('guia/general.html', {'cliente': cliente, 'tipos': tipos}, RequestContext(request))


@csrf_exempt
def obtenerGuiasGeneral(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        tipos = request.POST.get('tipos')
        cliente = request.POST.get('cliente')

        cursor = connection.cursor();
        if cliente == 0:
            cursor.execute(
                "select distinct p.guia_id,p.nro_guia,p.fecha_inicio,c.nombre_cliente,v.descripcion,p.aprobada,t.descripcion,p.egreso,p.ingreso,ec.nombre,p.partida,p.destino from facturacion_guiaremision p,cliente c,vehiculo v, empleados_chofer ec, empleados_empleado,tipo_guia t where p.cliente_id=c.id_cliente and t.id=p.tipo_guia_id and v.id=p.vehiculo_id and ec.chofer_id=p.chofer_id and t.id='" + tipos + "' and p.fecha_inicio>='" + fechainicial + "'and p.fecha_inicio<='" + fechafin + "'");

        else:
            cursor.execute(
                "select distinct p.guia_id,p.nro_guia,p.fecha_inicio,c.nombre_cliente,v.descripcion,p.aprobada,t.descripcion,p.egreso,p.ingreso,ec.nombre,p.partida,p.destino from facturacion_guiaremision p,cliente c,vehiculo v, empleados_chofer ec, empleados_empleado,tipo_guia t where p.cliente_id=c.id_cliente and t.id=p.tipo_guia_id and v.id=p.vehiculo_id and ec.chofer_id=p.chofer_id and t.id='" + tipos + "' and p.cliente_id=" + cliente + " and p.fecha_inicio>='" + fechainicial + "'and p.fecha_inicio<='" + fechafin + "'");
        row = cursor.fetchall();
        total = 0
        descuento = 0
        porcentaje = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            html += '<tr><td>' + str(p[2]) + '</td>'
            html += '<td>' + str(p[1]) + '</td>'
            html += '<td></td>'
            html += '<td>' + str(p[10]) + '</td>'
            html += '<td>' + str(p[11]) + '</td>'
            html += '<td>' + str(p[3]) + '</td>'
            html += '<td>'
            ped = GuiaDetalle.objects.filter(guia_id_id=str(p[0]))
            for pe in ped:
                html += '' + str(pe.cantidad) + ' ' + str(pe.producto_id) + '<br />'
            html += '</td>'
            html += '<td>' + str(p[6]) + '</td>'

            html += '<td>' + str(p[8]) + '</td>'
            html += '<td>' + str(p[7]) + '</td>'

            html += '</tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteComprasLocales(request):
    proveedor = Proveedor.objects.values('proveedor_id', 'codigo_proveedor', 'nombre_proveedor')

    return render_to_response('inventario/compras_locales.html', {'proveedor': proveedor,}, RequestContext(request))


@csrf_exempt
def obtenerComprasLocales(request):
    if request.method == 'POST':
        proveedor = request.POST.get('proveedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        producto = request.POST.get('producto')
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')

        cursor = connection.cursor();
        sql = 'select distinct p.id,p.codigo,p.fecha,co.notas,co.bodega_id,p.proveedor_id,c.nombre_proveedor,p.subtotal,p.iva,p.total,b.nombre,co.aprobada,co.nro_compra,co.compra_id from compras_locales p,orden_compra co,proveedor c,bodega b where p.proveedor_id=c.proveedor_id and b.id=co.bodega_id and co.compra_id=p.orden_compra_id '
        if proveedor != '0':
            sql += " and p.proveedor_id=" + proveedor
        else:
            print("entro no proveedor")



        print fechainicial
        print("fecha inicial")
        if fechainicial == '0':
            print("entro no feccha inicial")

        else:
            sql += " and p.fecha>='" + fechainicial + "'"
        if fechafin == '0':
            print("entro no fecha final")

        else:
            sql += " and p.fecha<='" + fechafin + "'"



        sql += " order by p.fecha"
        cursor.execute(sql)


        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<thead><tr><th>Cod.</th><th>Producto</th><th width="100px">Cantidad&nbsp;&nbsp;</th><th>Precio Unitario</th><th>Subtotal</th><th>Iva</th><th>Total</th></tr></thead>'
        for p in row:
            html += '<tr style="border:1px solid #ddd"><td colspan="3" style="border-right:0px;border-left:0px"><b>Fecha:' + str(
                p[2]) + '</b></td><td style="border-right:0px;border-left:0px"  colspan="4"><b>N&uacute;mero:</b>' + str(
                p[1]) + '</td></tr><tr><td style="border-left:0px" colspan="3"><b>Proveedor:' + str(p[6].encode('utf8')) + '</b></td><td  colspan="4" style="border-right:0px;border-left:0px"><b>OC:' + str(
                p[12]) + '</b></td></tr>'
            ped = ComprasDetalle.objects.filter(compra_id=str(p[13]))
            cont=0
            for pe in ped:
                cont=cont+1
                html += '<tr>'
                html += '<td style="border-right:0px">' + str(pe.producto.codigo_producto.encode('utf8')) + '</td>'
                html += '<td style="border-right:0px">' + str(pe.producto.descripcion_producto.encode('utf8')) + '</td>'
                html += '<td style="border-right:0px;border-left:0px">' + str(pe.cantidad) + '</td>'
                html += '<td style="border-left:0px">' + str(pe.precio_compra) + '</td>'
                if cont==1:
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[7]) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[8]) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[9]) + '</td>'
                html += '</tr>'
            total = total + p[9]
            subtotal = subtotal + p[7]
            iva = iva + p[8]
        html+='</tr>'
        html+='<tr><td colspan="3"></td>'
        html+='<td>Total</td>'
        html+='<td><b>'+str(subtotal)+'</b></td>'
        html+='<td><b>'+str(iva)+'</b></td>'
        html+='<td><b>'+str(total)+'</b></td>'
        html+='</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404


@csrf_exempt
def obtenerComprasLocalesAgruparProducto(request):
    if request.method == 'POST':
        proveedor = request.POST.get('proveedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        producto = request.POST.get('producto')
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')

        cursor = connection.cursor();
        sql = "select distinct cd.compra_id,cd.producto_id,pro.codigo_producto,pro.descripcion_producto,cd.cantidad,p.id,p.fecha,co.notas,co.bodega_id,p.proveedor_id,c.nombre_proveedor,p.subtotal,p.iva,p.total,b.nombre,co.aprobada,co.nro_compra,co.compra_id from compras_locales p,orden_compra co,proveedor c,bodega b,compras_detalle cd,producto pro where p.proveedor_id=c.proveedor_id and b.id=co.bodega_id and co.compra_id=p.orden_compra_id and cd.compra_id=co.compra_id and pro.producto_id= cd.producto_id "
        if proveedor != '0':
            sql += " and p.proveedor_id=" + proveedor
        else:
            print("entro no proveedor")
        if codigo!= '':
            sql +=" and pro.codigo_producto like '%" +codigo+ "%'"
        if nombre!= '':
            sql +=" and pro.descripcion_producto like '%" +nombre+ "%'"

        print fechainicial
        print("fecha inicial")
        if fechainicial == '0':
            print("entro no feccha inicial")

        else:
            sql += " and p.fecha>='" + fechainicial + "'"

        if fechafin == '0':
            print("entro no fecha final")

        else:
            sql += " and p.fecha<='" + fechafin + "'"

        print sql

        cursor.execute(sql);


        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<thead><tr><th>CL</th><th>Proveedor</th><th width="100px">Factura&nbsp;&nbsp;</th><th>Cantidad</th><th>Precio</th><th>Subtotal</th></tr></thead>'
        for p in row:
            html += '<tr style="border:1px solid #ddd"><td colspan="5" style="border-right:0px"><b>PRODUCTO:&nbsp;&nbsp;' + str(
                p[2]) + '</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>' + str(p[3].encode('utf8')) + '</b></td></tr>'
            try:
                ped = ComprasDetalle.objects.filter(producto_id=str(p[1]))
            except ComprasDetalle.DoesNotExist:
                ped = None

            if ped:
                for pe in ped:
                    try:
                        cl = ComprasLocales.objects.get(orden_compra_id=str(pe.compra_id))
                    except ComprasLocales.DoesNotExist:
                        cl = None
                    if cl:

                        html += '<tr>'
                        html += '<td>' + str(cl.codigo) + '</td>'
                        html += '<td style="border-right:0px">' + str(cl.proveedor.nombre_proveedor.encode('utf8')) + '</td>'
                        html += '<td style="border-left:0px">' + str(cl.nro_fact_proveedor) + '</td>'
                        html += '<td style="border-left:0px">' + str(pe.cantidad) + '</td>'
                        html += '<td style="border-left:0px">' + str(pe.precio_compra) + '</td>'
                        calculo_st=pe.cantidad * pe.precio_compra
                        html += '<td style="border-left:0px">' + str(calculo_st) + '</td>'

                        html += '</tr>'
            else:
                html += '<tr>'
                html += '<td></td>'
                html += '<td style="border-right:0px"></td>'
                html += '<td style="border-left:0px"></td>'
                html += '<td style="border-left:0px"></td>'
                html += '<td style="border-left:0px"></td>'
                html += '</tr>'
        # html+='<tr><td colspan="4"></td>'
        # html+='<td></td>'
        # html+='<td><b>'+str(subtotal)+'</b></td>'
        # html+='<td><b>'+str(iva)+'</b></td>'
        # html+='<td><b>'+str(total)+'</b></td>'
        # html+='</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404


@csrf_exempt
def obtenerOrdenCompraAgruparProducto(request):
    if request.method == 'POST':
        proveedor = request.POST.get('proveedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        producto = request.POST.get('producto')

        cursor = connection.cursor();
        sql='select distinct cd.compra_id,cd.producto_id,pro.codigo_producto,pro.descripcion_producto,cd.cantidad,p.id,p.fecha,co.notas,co.bodega_id,p.proveedor_id,c.nombre_proveedor,p.subtotal,p.iva,p.total,b.nombre,co.aprobada,co.nro_compra,co.compra_id from compras_locales p,orden_compra co,proveedor c,bodega b,compras_detalle cd,producto pro where p.proveedor_id=c.proveedor_id and b.id=co.bodega_id and co.compra_id=p.orden_compra_id and cd.compra_id=co.compra_id and pro.producto_id= cd.producto_id';
        if proveedor != '0':
            sql+=" and p.proveedor_id=" + proveedor
        else:
            print("entro no proveedor")

        print fechainicial
        print("fecha inicial")
        if fechainicial == '0':
            print("entro no feccha inicial")

        else:
            sql += " and p.fecha>='" + fechainicial + "'"
        if fechafin == '0':
            print("entro no fecha final")

        else:
            sql += " and p.fecha<='" + fechafin + "'"


        sql+=" order by p.fecha"
        cursor.execute(sql)

        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<thead><tr><th>OC</th><th>Proveedor</th><th>Cantidad</th><th>Precio</th></tr></thead>'
        for p in row:
            html += '<tr style="border:1px solid #ddd"><td colspan="5" style="border-right:0px"><b>PRODUCTO:&nbsp;&nbsp;' + str(
                p[2]) + '</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>' + str(p[3].encode('utf8')) + '</b></td></tr>'
            ped = ComprasDetalle.objects.filter(producto_id=str(p[1]))
            for pe in ped:
                cl = OrdenCompra.objects.get(compra_id=str(pe.compra_id))
                html += '<tr>'
                html += '<td>' + str(cl.nro_compra) + '</td>'
                html += '<td style="border-right:0px">' + str(cl.proveedor.nombre_proveedor.encode('utf8')) + '</td>'
                html += '<td style="border-left:0px">' + str(pe.cantidad) + '</td>'
                html += '<td style="border-left:0px">' + str(pe.precio_compra) + '</td>'
                html += '</tr>'
        # html+='<tr><td colspan="4"></td>'
        # html+='<td></td>'
        # html+='<td><b>'+str(subtotal)+'</b></td>'
        # html+='<td><b>'+str(iva)+'</b></td>'
        # html+='<td><b>'+str(total)+'</b></td>'
        # html+='</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404


@csrf_exempt
def obtenerInventarioTipoProducto(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        tipos = request.POST.get('tipos')
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        cursor = connection.cursor();

        sql=''
        if tipos == '0':
            sql+="select distinct t.id,t.descripcion from producto_en_bodega pb,producto p,bodega b,tipo_producto t where pb.producto_id=p.producto_id and b.id=pb.bodega_id and p.tipo_producto=t.id and pb.bodega_id=" + bodega

        else:
            sql+="select distinct t.id,t.descripcion from producto_en_bodega pb,producto p,bodega b,tipo_producto t where pb.producto_id=p.producto_id and b.id=pb.bodega_id and p.tipo_producto=t.id and p.tipo_producto=" + tipos + " and pb.bodega_id=" + bodega

        if codigo!= '':
            sql +=" and p.codigo_producto like '%" +codigo+ "%'"
        if nombre!= '':
            sql +=" and p.descripcion_producto like '%" +nombre+ "%'"

        cursor.execute(sql);
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        sql1=''
        for p in row:
            html += '<tr style="border:1px solid #ddd"><td colspan="5" style="border-right:0px"><b>' + str(
                p[1]) + '</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td></tr>'
            cursor1 = connection.cursor();
            sql1="select distinct pb.producto_bodega_id,pb.producto_id,p.codigo_producto,p.descripcion_producto,pb.cantidad,pb.bodega_id,b.codigo_bodega,b.nombre,p.cant_maxima,p.cant_minimia,t.descripcion ,p.costo,p.unidad from producto_en_bodega pb,producto p,bodega b,tipo_producto t where pb.producto_id=p.producto_id and b.id=pb.bodega_id and p.tipo_producto=t.id and p.tipo_producto=" + str(
                    p[0]) + " and pb.bodega_id=" + bodega

            if codigo != '':
                sql1 += " and p.codigo_producto like '%" + codigo + "%'"
            if nombre != '':
                sql1 += " and p.descripcion_producto like '%" + nombre + "%'"
            cursor1.execute(sql1)
            row1 = cursor1.fetchall()
            total_c=0
            cant=0
            cost=0
            total_valor=0
            for pe in row1:
                cost = 0
                cant = 0
                html += '<tr>'
                html += '<td>' + str(pe[2]) + '</td><td> ' + str(pe[3].encode('utf8')) + '</td>'
                html += '<td style="border-left:0px">' + str(pe[12]) + '</td>'
                html += '<td style="border-right:0px">' + str(pe[4]) + '</td>'
                #html += '<td style="border-left:0px">' + str(pe[8]) + '</td>'
                #html += '<td style="border-left:0px">' + str(pe[9]) + '</td>'
                html += '<td style="border-left:0px">' + str(pe[11]) + '</td>'
                if pe[4]:
                    cant = pe[4]
                if pe[11]:
                    cost = pe[11]
                total_c = cant * cost
                html += '<td>' + str(total_c) + '</td>'
                total_valor = total_valor + total_c
                html += '</tr>'
        # html+='<tr><td colspan="4"></td>'
        # html+='<td></td>'
        # html+='<td><b>'+str(subtotal)+'</b></td>'
        # html+='<td><b>'+str(iva)+'</b></td>'
        # html+='<td><b>'+str(total)+'</b></td>'
        # html+='</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404


def export_to_excel(request):
    # your excel html format
    template_name = "pedido.html"
    html = request.POST.get('html')
    response = render_to_response('pedido/exportar_excel.html', {'html': html,})

    # this is the output file
    filename = "pedido.xls"

    response['Content-Disposition'] = 'attachment; filename=' + filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
    return response


def reporteLiquidacionTotal(request):
    vendedor = Vendedor.objects.values('id', 'codigo', 'nombre')

    return render_to_response('ventas/liquidacion_total.html', {'vendedor': vendedor,}, RequestContext(request))


@csrf_exempt
def obtenerLiquidacionTotal(request):
    if request.method == 'POST':
        vendedor = request.POST.get('vendedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor()
        cursor.execute(
            "select distinct c.id_cliente,c.nombre_cliente from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + vendedor + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "' group by c.id_cliente,c.nombre_cliente")
        row = cursor.fetchall()
        total = 0
        descuento = 0
        porcentaje = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            html += '<tr><th colspan="9">CLIENTE:' + str(p[1]) + '</th><tr>'
            curso = connection.cursor()
            curso.execute(
                "select distinct p.id,p.tipo,p.fecha,p.codigo,p.descripcion,p.detalle,p.cantidad,p.codigo,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva,p.total,p.porcentaje_descuento,p.descuento,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + vendedor + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "' and c.id_cliente=" + str(
                    p[0]) + "");
            row1 = curso.fetchall();
            html += '<tr><th>FECHA</th><th>PROFORMA</th><th>FACTURA NO.</th><th>DESCRIPCION</th><th>COMPANIA</th><th>VALOR</th><th>ABONOS</th><th>SALDO</th><th>OBSERVACION</th></tr>'
            valor_total = 0
            saldo_total = 0
            abono_total = 0
            abono = 0
            for p1 in row1:
                html += '<tr><td>' + str(p1[2]) + '</td>'
                html += '<td>' + str(p1[3]) + '</td>'
                factura = Factura.objects.filter(proforma_factura_id=p1[3])
                html += '<td>'
                if len(factura):
                    for f in factura:
                        html += str(f.nro_factura) + '<br />'
                html += '</td>'
                html += '<td>'
                ped = ProformaDetalle.objects.filter(proforma_id=str(p1[0]))
                for pe in ped:
                    html += '' + str(pe.cantidad) + ' ' + str(pe.nombre) + '<br />'
                html += '</td>'
                html += '<td>MUEDIRSA</td>'
                html += '<td style="text-align: right; padding:10px 1px">' + str(p1[12]) + '</td>'
                idp = p1[0]
                cursor2 = connection.cursor()
                cursor2.execute(
                    "select sum(rpcd.valor_a_pagar) from registrar_cobro_pago_detalle rpcd, registrar_cobro_pago rcp, proforma_factura pf where rpcd.proforma_factura_id=" + str(
                        idp) + " and rcp.id=rpcd.registrar_cobro_pago_id and rpcd.proforma_factura_id=pf.id and pf.vendedor_id=" + str(
                        vendedor) + "");
                row2 = cursor2.fetchall();
                if row2[0][0]:
                    abono = row2[0][0]
                html += '<td style="text-align: right; padding:10px 1px">' + str(abono) + '</td>'
                valor_total = valor_total + p1[12]
                abono_total = abono_total + abono

                saldo = p1[12] - abono
                saldo_total = saldo_total + saldo

                html += '<td style="text-align: right; padding:10px 1px">' + str(saldo) + '</td>'
                html += '<td style="text-align: right; padding:10px 1px"></td></tr>'
            html += '<tr><th colspan="5">Total </th>'
            html += '<th style="text-align: right; padding:10px 1px">' + str(valor_total) + '</th>'
            html += '<th style="text-align: right; padding:10px 1px">' + str(abono_total) + '</th>'
            html += '<th style="text-align: right; padding:10px 1px">' + str(saldo_total) + '</th>'
            html += '<th style="text-align: right; padding:10px 1px"></th>'
            html += '</tr>'
        html += '<tr><th colspan="9"></th></tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteDiarioVentasMensual(request):
    vendedor = Vendedor.objects.values('id', 'codigo', 'nombre')

    return render_to_response('ventas/diario_ventas_mes.html', {'vendedor': vendedor,}, RequestContext(request))


@csrf_exempt
def obtenerDiarioVentasMensual(request):
    if request.method == 'POST':
        vendedor = request.POST.get('vendedor')
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')
        mes_txt = request.POST.get('mes_txt')

        cursor = connection.cursor();
        cursor1 = connection.cursor();

        if vendedor == '0':
            if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                cursor1.execute(
                    "select distinct v.id,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.fecha>='" + str(
                        anio) + "-" + str(mes) + "-01'and p.fecha<='" + str(anio) + "-" + str(mes) + "-31'")
            else:
                if mes == 2:
                    cursor1.execute(
                        "select distinct v.id,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.fecha>='" + str(
                            anio) + "-" + str(mes) + "-01'and p.fecha<='" + str(anio) + "-" + str(mes) + "-29'")
                else:
                    cursor1.execute(
                        "select distinct v.id,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.fecha>='" + str(
                            anio) + "-" + str(mes) + "-01'and p.fecha<='" + str(anio) + "-" + str(mes) + "-30'")



        else:
            if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                cursor1.execute(
                    "select distinct v.id,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + vendedor + " and p.fecha>='" + str(
                        anio) + "-" + str(mes) + "-01'and p.fecha<='" + str(anio) + "-" + str(mes) + "-31'");
            else:
                if mes == 2:
                    cursor1.execute(
                        "select distinct v.id,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + vendedor + " and p.fecha>='" + str(
                            anio) + "-" + str(mes) + "-01'and p.fecha<='" + str(anio) + "-" + str(mes) + "-29'");
                else:
                    cursor1.execute(
                        "select distinct v.id,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + vendedor + " and p.fecha>='" + str(
                            anio) + "-" + str(mes) + "-01'and p.fecha<='" + str(anio) + "-" + str(mes) + "-30'");

        row1 = cursor1.fetchall();

        total = 0
        descuento = 0
        porcentaje = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)

        html = ''

        html += '<tr><th colspan="9" style="text-align:center"> ' + str(mes_txt) + '</th></tr>'
        for p1 in row1:
            total = 0
            descuento = 0
            porcentaje = 0
            subtotal = 0
            iva = 0

            html += '<tr><th colspan="9" > ' + str(p1[1]) + '</th></tr>'
            html += '<tr><tr><th>Fecha</th><th>No. Factura</th><th width="100px">Cliente&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th><th>Subtotal</th><th>%Dscto.</th><th>V.Dscto.</th><th>iva</th><th>Total</th></tr></tr>'
            if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                cursor.execute(
                    "select distinct p.factura_id,p.tipo,p.fecha,p.nro_factura,p.descripcion,p.detalle,p.cantidad,p.codigo,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva,p.total,p.porcentaje_descuento,p.descuento,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id  and v.id=" + str(
                        p1[0]) + "and p.fecha>='" + str(anio) + "-" + str(mes) + "-01'and p.fecha<='" + str(
                        anio) + "-" + str(mes) + "-31'")
            else:
                if mes == 2:
                    cursor.execute(
                        "select distinct p.factura_id,p.tipo_factura,p.fecha,p.nro_factura,p.observacion,p.notas,p.ruc,p.nro_factura,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva_monto,p.total,p.dscto_pciento,p.dscto_monto,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + str(
                            p1[0]) + "and p.fecha>='" + str(anio) + "-" + str(mes) + "-01'and p.fecha<='" + str(
                            anio) + "-" + str(mes) + "-29'")
                else:
                    cursor.execute(
                        "select distinct p.factura_id,p.tipo_factura,p.fecha,p.nro_factura,p.observacion,p.notas,p.ruc,p.nro_factura,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva_monto,p.total,p.dscto_pciento,p.dscto_monto,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + str(
                            p1[0]) + "and p.fecha>='" + str(anio) + "-" + str(mes) + "-01'and p.fecha<='" + str(
                            anio) + "-" + str(mes) + "-30'")
            row = cursor.fetchall();

            for p in row:
                html += '<tr><td>' + str(p[2]) + '</td>'
                html += '<td>' + str(p[3]) + '</td>'
                html += '<td></td>'
                html += '<td>' + str(p[8]) + '</td>'
                # html+='<td>'
                # ped=ProformaDetalleFactura.objects.filter(proforma_factura_id=str(p[0]))
                # for pe in ped:
                #     html+=''+str(pe.cantidad)+' '+str(pe.nombre)+'<br />'
                # html+='</td>'
                html += '<td>' + str(p[10]) + '</td>'
                html += '<td>' + str(p[13]) + '</td>'

                html += '<td>' + str(p[14]) + '</td>'

                html += '<td>' + str(p[11]) + '</td>'
                html += '<td>' + str(p[12]) + '</td>'
                html += '</tr>'
                iva = iva + p[11]
                total = total + p[12]
                porcentaje = porcentaje + p[13]
                descuento = descuento + p[14]
                subtotal = subtotal + p[10]
            html += '<tr><th colspan="4">Total de ' + str(p[15]) + '</th>'
            html += '<th>' + str(subtotal) + '</th>'
            html += '<th>' + str(porcentaje) + '</th>'
            html += '<th>' + str(descuento) + '</th>'
            html += '<th>' + str(iva) + '</th>'
            html += '<th>' + str(total) + '</th>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteDiarioVentasAnual(request):
    vendedor = Vendedor.objects.values('id', 'codigo', 'nombre')

    return render_to_response('ventas/diario_ventas_anual.html', {'vendedor': vendedor,}, RequestContext(request))


@csrf_exempt
def obtenerDiarioVentasAnual(request):
    if request.method == 'POST':
        vendedor = request.POST.get('vendedor')
        anio = request.POST.get('anio')

        cursor = connection.cursor();
        cursor1 = connection.cursor()

        if vendedor == '0':
            cursor1.execute(
                "select distinct v.id,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id ")

        else:
            cursor1.execute(
                "select distinct v.id,v.nombre from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + vendedor + " ");

        row1 = cursor1.fetchall();

        total = 0
        descuento = 0
        porcentaje = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)

        html = ''

        html += '<tr><th style="text-align:center">Vendedor</th><th style="text-align:center">Enero</th><th style="text-align:center">Febrero</th><th style="text-align:center">Marzo</th><th style="text-align:center">Abril</th><th style="text-align:center">Mayo</th><th style="text-align:center">Junio</th><th style="text-align:center">Julio</th><th style="text-align:center">Agosto</th><th style="text-align:center">Septiembre</th><th style="text-align:center">Octubre</th><th style="text-align:center">Noviembre</th><th style="text-align:center">Diciembre</th></tr>'
        for p1 in row1:
            total = 0
            descuento = 0
            porcentaje = 0
            subtotal = 0
            iva = 0
            enero = 0
            febrero = 0
            marzo = 0
            abril = 0
            mayo = 0
            junio = 0
            julio = 0
            agosto = 0
            septiembre = 0
            octubre = 0
            noviembre = 0
            diciembre = 0

            html += '<tr><th> ' + str(p1[1]) + '</th>'
            cursor.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-01-01'and p.fecha<='" + str(anio) + "-01-31'")
            row = cursor.fetchall();
            if row[0][0]:
                enero = row[0][0]
            html += '<td>' + str(enero) + '</td>'
            cursor2 = connection.cursor()
            cursor2.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-02-01'and p.fecha<='" + str(anio) + "-02-29'")
            row2 = cursor2.fetchall();
            if row2[0][0]:
                febrero = row2[0][0]
            html += '<td>' + str(febrero) + '</td>'

            cursor3 = connection.cursor()
            cursor3.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-03-01'and p.fecha<='" + str(anio) + "-03-31'")
            row3 = cursor3.fetchall();

            if row3[0][0]:
                marzo = row3[0][0]

            html += '<td>' + str(marzo) + '</td>'

            cursor4 = connection.cursor()

            cursor4.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id  and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-04-01'and p.fecha<='" + str(anio) + "-04-30'")
            row4 = cursor4.fetchall();
            if row4[0][0]:
                abril = row4[0][0]

            html += '<td>' + str(abril) + '</td>'

            cursor5 = connection.cursor()
            cursor5.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-05-01'and p.fecha<='" + str(anio) + "-05-31'")
            row5 = cursor5.fetchall();
            if row5[0][0]:
                mayo = row5[0][0]

            html += '<td>' + str(mayo) + '</td>'

            cursor6 = connection.cursor()
            cursor6.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id  and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-06-01'and p.fecha<='" + str(anio) + "-06-30'")
            row6 = cursor6.fetchall();
            if row6[0][0]:
                junio = row6[0][0]

            html += '<td>' + str(junio) + '</td>'

            cursor7 = connection.cursor()
            cursor7.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-07-01'and p.fecha<='" + str(anio) + "-07-31'")
            row7 = cursor7.fetchall();
            if row7[0][0]:
                julio = row7[0][0]

            html += '<td>' + str(julio) + '</td>'

            cursor8 = connection.cursor()
            cursor8.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id  and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-08-01'and p.fecha<='" + str(anio) + "-08-31'")
            row8 = cursor8.fetchall();
            if row8[0][0]:
                agosto = row8[0][0]

            html += '<td>' + str(agosto) + '</td>'

            cursor9 = connection.cursor()
            cursor9.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-09-01'and p.fecha<='" + str(anio) + "-09-30'")
            row9 = cursor9.fetchall();
            if row9[0][0]:
                septiembre = row9[0][0]

            html += '<td>' + str(septiembre) + '</td>'

            cursor10 = connection.cursor()
            cursor10.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id  and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-10-01'and p.fecha<='" + str(anio) + "-10-31'")
            row10 = cursor10.fetchall();
            if row10[0][0]:
                octubre = row10[0][0]

            html += '<td>' + str(octubre) + '</td>'

            cursor11 = connection.cursor()
            cursor11.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-11-01'and p.fecha<='" + str(anio) + "-11-30'")
            row11 = cursor11.fetchall();
            if row11[0][0]:
                noviembre = row11[0][0]

            html += '<td>' + str(noviembre) + '</td>'

            cursor12 = connection.cursor()
            cursor12.execute(
                "select sum(p.total) from factura p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + str(anio) + "-12-01'and p.fecha<='" + str(anio) + "-12-31'")
            row12 = cursor12.fetchall();
            if row12[0][0]:
                diciembre = row12[0][0]

            html += '<td>' + str(diciembre) + '</td>'

            total = enero + febrero + marzo + abril + mayo + junio + julio + agosto + septiembre + octubre + diciembre + noviembre
            html += '<td>' + str(total) + '</td>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteCuentasCobrar(request):
    vendedor = Vendedor.objects.values('id', 'codigo', 'nombre')

    return render_to_response('ventas/cuentas_cobrar.html', {'vendedor': vendedor,}, RequestContext(request))


@csrf_exempt
def obtenerCuentasCobrar(request):
    if request.method == 'POST':
        vendedor = request.POST.get('vendedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor1 = connection.cursor();

        if vendedor == '0':
            cursor1.execute(
                "select distinct v.id,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' ");

        else:
            cursor1.execute(
                "select distinct v.id,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and v.id=" + vendedor + "");

        row1 = cursor1.fetchall();

        total = 0
        descuento = 0
        porcentaje = 0
        subtotal = 0
        iva = 0
        tabono = 0
        tsaldo = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p1 in row1:
            total = 0
            descuento = 0
            porcentaje = 0
            subtotal = 0
            iva = 0
            html += '<tr><td></td><th colspan="9"> ' + str(p1[1]) + '</th></tr>'
            cursor.execute(
                "select distinct p.id,p.tipo,p.fecha,p.codigo,p.descripcion,p.detalle,p.cantidad,p.codigo,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva,p.total,p.porcentaje_descuento,p.descuento,v.nombre,p.id from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");
            row = cursor.fetchall();

            for p in row:
                html += '<tr><td>' + str(p[8]) + '</td>'
                try:
                    pr = Proforma.objects.get(codigo=str(p[16]))
                except Proforma.DoesNotExist:
                    pr = None

                if pr:
                    html += '<td>' + str(pr.fechapedido) + '</td>'
                else:
                    html += '<td></td>'
                html += '<td>'
                ped = ProformaDetalle.objects.filter(proforma_id=str(p[0]))
                for pe in ped:
                    html += '*' + str(pe.cantidad) + ' ' + str(pe.nombre.encode('utf8')) + '<br />'
                html += '</td>'
                if pr:
                    html += '<td>' + str(pr.codigo) + '</td>'
                else:
                    html += '<td></td>'

                html += '<td>' + str(p[3]) + '</td>'
                try:
                    fac = Factura.objects.get(proforma_factura_id=str(p[0]))
                except Factura.DoesNotExist:
                    fac = None
                if fac:
                    html += '<td>' + str(fac.nro_factura) + '</td>'
                else:
                    html += '<td></td>'

                html += '<td>' + str(p[12]) + '</td>'
                idp = p[0]
                cursor2 = connection.cursor()
                cursor2.execute(
                    "select sum(rpcd.valor_a_pagar) from registrar_cobro_pago_detalle rpcd, registrar_cobro_pago rcp, proforma_factura pf where rpcd.proforma_factura_id=" + str(
                        idp) + " and rcp.id=rpcd.registrar_cobro_pago_id and rpcd.proforma_factura_id=pf.id and pf.vendedor_id=" + str(
                        p[9]) + "");
                row2 = cursor2.fetchall();
                abono = 0
                if row2[0][0]:
                    abono = row2[0][0]
                saldo = p[12] - abono

                html += '<td>' + str(abono) + '</td>'
                html += '<td>' + str(saldo) + '</td>'
                html += '<td></td>'
                html += '</tr>'
                tabono = tabono + abono
                tsaldo = tsaldo + saldo
                total = total + p[12]

            html += '<tr><th colspan="7">Total de ' + str(p[15]) + '</th>'
            html += '<th>' + str(total) + '</th>'
            html += '<th>' + str(tabono) + '</th>'
            html += '<th>' + str(tsaldo) + '</th>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def leerArchivoCSV(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        portfolio = csv.DictReader(paramFile)
        users = []
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        # archi=open(paramFil,'r')
        # linea=paramFile.readline()
        # while linea!="":

        # linea=archi.readline()
        #print 'quincena' + str(quincena)
        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            print x[0]
            if len(x[0]):
                print 'entro1'
                try:
                    empleado = Empleado.objects.get(codigo_reloj=x[0])

                except Empleado.DoesNotExist:
                    empleado = None

                if empleado:
                    print 'entro2'
                    formato = "%H:%M:%S"


                    h1 = x[2].strip() + ':00'
                    h2 = x[3].strip() + ':00'


                    fecha = datetime.strptime(x[1], '%d/%m/%Y')
                    numero = fecha.strftime('%A')
                    try:
                        dias_feriados = DiasFeriados.objects.get(fecha=fecha)

                    except DiasFeriados.DoesNotExist:
                        dias_feriados = None

                    if numero == "Sunday" or numero == "Saturday" or dias_feriados != None:
                        print "entro horas E"
                        print h1
                        if h1 == ':00':
                            h1 = '00:00:00'
                        if h2 == ':00':
                            h2 = '00:00:00'


                        hora_inicial = datetime.strptime(h1, formato)
                        hora_final = datetime.strptime(h2, formato)
                        delta = hora_final - hora_inicial
                        minutos = float(delta.seconds % 3600 / 60.0) / 60
                        horas = float(delta.seconds // 3600)
                        total = float(minutos) + float(horas)
                        hora_comida = datetime.strptime('13:30:00', formato)
                        if hora_final > hora_comida:
                            total = total - float(0.5)

                        sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=empleado.empleado_id,
                                                                         tipo_ingreso_egreso_empleado_id=24)
                        valor = (sueldo.valor_mensual / 240) * 2 * total
                        print 'valor cambiado'
                        print h1
                        print h2

                        dias = IngresosRolEmpleado()
                        dias.anio = anio
                        dias.mes = mes
                        #dias.quincena = quincena
                        dias.empleado = empleado
                        dias.fecha = x[1]
                        dias.hora_inicio = x[2]
                        dias.hora_fin = x[3]
                        dias.horas = round(float(total), 2)
                        dias.tipo_ingreso_egreso_empleado_id = 25
                        dias.valor = round(float(valor), 2)
                        dias.nombre = "HORAS EXTRAORDINARIAS"
                        print 'formato de x2'
                        print x[2]
                        print 'formato de x3'
                        print x[3]

                        try:
                            horasExtrasRegistradas = Permiso.objects.get(empleados_empleado_id=empleado.empleado_id,tipo_solicitud_id=3,
                                                                         fecha_solicitud=fecha,hora_desde=h1,hora_hasta=h2,activo=True)

                        except Permiso.DoesNotExist:
                            horasExtrasRegistradas = None

                        if horasExtrasRegistradas:
                            dias.pagar=True

                        dias.save()
                    else:
                        print "entro horario de LUNES A VIERNES"
                        if h1 == ':00':
                            print "NO FUE A TRABAJAR"
                            delta = 8
                            sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=empleado.empleado_id,
                                                                             tipo_ingreso_egreso_empleado_id=24)
                            valor = (sueldo.valor_mensual / 240) * 8 * 2
                            dias = DiasNoLaboradosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            #dias.quincena = quincena
                            dias.empleado = empleado
                            dias.dias = 8
                            dias.tipo_ausencia_id = 3
                            dias.valor = round(float(valor), 2)
                            dias.fecha = x[1]
                            dias.hora_inicio = x[2]
                            dias.hora_fin = x[3]
                            try:
                                permisoHora = Permiso.objects.get(empleados_empleado_id=empleado.empleado_id,
                                                                             tipo_solicitud_id=1,fecha_desde__gt=fecha,fecha_desde__lt=fecha, activo=True,)

                            except Permiso.DoesNotExist:
                                permisoHora = None

                            if permisoHora:
                                dias.descontar = False
                            else:
                                dias.descontar = True
                            dias.save()
                        else:
                            print "SI FUE A TRABAJAR"
                            hora_inicial = datetime.strptime(h1, formato)
                            hora_inicio_trabajo = datetime.strptime('08:00:00', formato)
                            if hora_inicial < hora_inicio_trabajo:
                                hora_inicial = hora_inicio_trabajo
                            else:
                                print "OOOO"
                            hora_final = datetime.strptime(h2, formato)
                            delta = hora_final - hora_inicial
                            d1 = timedelta(hours=8, minutes=30)
                            hora_trabajo = datetime.strptime('08:30:00', formato)
                            print 'hora inicial:' + str(hora_inicial)
                            print str(x[0]) + 'hora' + str(delta)
                            if delta < d1:
                                print "NO TRABAJO LAS HORAS COMPLETAS"
                                horas_trabajadas = hora_trabajo - delta
                                minutos = float(horas_trabajadas.minute) / 60
                                horas = horas_trabajadas.hour
                                total = float(minutos) + float(horas)
                                print 'hora_inicio:' + str(hora_inicial)
                                print 'hora_fin:' + str(hora_final)
                                print 'delta:' + str(delta)
                                print 'minutos:' + str(minutos)
                                print 'horas:' + str(horas)
                                print 'horas_trabajadas/' + str(total)
                                sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=empleado.empleado_id,
                                                                                 tipo_ingreso_egreso_empleado_id=24)
                                horas_f = 8
                                dias = DiasNoLaboradosRolEmpleado()
                                dias.anio = anio
                                dias.mes = mes
                                #dias.quincena = quincena
                                dias.empleado = empleado
                                dias.fecha = x[1]
                                dias.hora_inicio = x[2]
                                dias.hora_fin = x[3]
                                dias.descontar = True
                                if total < horas_f:
                                    valor = (sueldo.valor_mensual / 240) * total * 2
                                    print 'valor:' + str(valor)
                                    dias.dias = round(float(total), 2)
                                    dias.tipo_ausencia_id = 5
                                    dias.valor = round(float(valor), 2)
                                else:
                                    print 'horas_f:' + str(horas_f) + 'gsh' + str(total)
                                    dias.dias = 0
                                    dias.valor = 0
                                dias.save()
                            else:
                                if delta > d1:
                                    print "SOBRETIEMPO"
                                    d1 = timedelta(hours=8, minutes=45)
                                    horas_trabajadas = delta - d1
                                    segundos = horas_trabajadas.seconds
                                    minutos = float(horas_trabajadas.seconds % 3600 / 60.0) / 60
                                    horas = float(horas_trabajadas.seconds // 3600)
                                    total = float(minutos) + float(horas)
                                    print 'horas trabajadas HE:' + str(horas_trabajadas)
                                    print 'horas trabajadas HE horas:' + str(horas)
                                    print 'horas trabajadas HE minutos:' + str(minutos)
                                    print 'horas trabajadas HE totsl:' + str(total)
                                    print 'horas trabajadas HE second:' + str(segundos)
                                    print 'horas trabajadas HE days:' + str(horas_trabajadas.days)
                                    if horas_trabajadas.days >= 0:
                                        sueldo = IngresosProyectadosEmpleado.objects.get(
                                            empleado_id=empleado.empleado_id, tipo_ingreso_egreso_empleado_id=24)
                                        valor = (sueldo.valor_mensual / 240) * 1.5 * total
                                        fecha = datetime.strptime(x[1], '%d/%m/%Y')
                                        numero = fecha.strftime('%A')
                                        print 'horas extras:' + str(numero)
                                        dias = IngresosRolEmpleado()
                                        dias.anio = anio
                                        dias.mes = mes
                                        #dias.quincena = quincena
                                        dias.empleado = empleado
                                        dias.fecha = x[1]
                                        dias.hora_inicio = x[2]
                                        dias.hora_fin = x[3]
                                        dias.horas = round(float(total), 2)
                                        dias.tipo_ingreso_egreso_empleado_id = 5
                                        dias.valor = round(float(valor), 2)
                                        dias.nombre = "HORAS SUPLEMENTARIAS"
                                        dias.save()
                                    else:
                                        print 'NO ES SOBRETIEMPO' + str(hora_final)


                                        # dias=DiasNoLaboradosRolEmpleado()
                                        # dias.anio=anio
                                        # dias.mes=mes
                                        # dias.quincea=quincena
                                        # dias.empleado=empleado
                                        # dias.dias=
                else:
                    print('entroNOempleado')




            else:
                print('hola')

        texto = "text"
        anio = Anio.objects.all()
        return render_to_response('cargar_archivo/index.html', {'texto': texto,'anio': anio}, RequestContext(request))


    else:
        texto = "text"
        anio = Anio.objects.all()
        return render_to_response('cargar_archivo/index.html', {'texto': texto,'anio': anio}, RequestContext(request))


def cargarPlantillaCSV(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        abreviatura = request.POST['abreviatura']
        observaciones = request.POST['observacion']
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        portfolio = csv.DictReader(paramFile)
        users = []
        # archi=open(paramFil,'r')
        # linea=paramFile.readline()
        # while linea!="":

        # linea=archi.readline()
        plantilla = PlantillaRrhh()
        plantilla.codigo = codigo
        plantilla.abreviatura = abreviatura
        plantilla.nombre = nombre
        plantilla.observaciones = observaciones
        plantilla.created_by = request.user.get_full_name()
        plantilla.updated_by = request.user.get_full_name()
        plantilla.created_at = datetime.now()
        plantilla.updated_at = datetime.now()
        plantilla.save()

        try:
            secuencial = Secuenciales.objects.get(modulo='plantillas')
            secuencial.secuencial = secuencial.secuencial + 1
            secuencial.created_by = request.user.get_full_name()
            secuencial.updated_by = request.user.get_full_name()
            secuencial.created_at = datetime.now()
            secuencial.updated_at = datetime.now()
            secuencial.save()
        except Secuenciales.DoesNotExist:
            secuencial = None

        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            print ('Valor de linea' + str(x[0]))
            if len(x[0]):

                try:
                    empleado = Empleado.objects.get(cedula_empleado=x[1])

                except Empleado.DoesNotExist:
                    empleado = None

                if empleado:
                    try:
                        existe = PlantillaRrhhDetalle.objects.get(empleado_id=empleado.empleado_id,
                                                                  plantilla_rrhh_id=plantilla.id,
                                                                  tipo_ingreso_egreso_empleado_id=14)

                    except PlantillaRrhhDetalle.DoesNotExist:
                        existe = None

                    if existe:
                        valor_actual = existe.valor
                        v = float(x[6].replace(',', '.'))
                        # print ('sueldo unificado entro' + str(x[6]))
                        valor = float(v)

                        valor_total = float(valor_actual + valor)
                        existe.valor = valor_total
                        existe.save()

                    else:

                        detalle = PlantillaRrhhDetalle()
                        detalle.plantilla_rrhh_id = plantilla.id
                        detalle.empleado_id = empleado.empleado_id
                        detalle.tipo_ingreso_egreso_empleado_id = 14
                        v = float(x[6].replace(',', '.'))
                        print ('sueldo unificado' + str(x[6]))
                        valor = float(v)
                        detalle.valor = valor
                        detalle.save()


                else:
                    print('entroNOempleado')




            else:
                print('hola')

        existe_recorrer = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=plantilla.id,
                                                              tipo_ingreso_egreso_empleado_id=14)
        if existe_recorrer:
            for r in existe_recorrer:
                valor_cambiar = r.valor

                valor = float(valor_cambiar / 2) + 0.000001
                r.valor = round(valor, 2)
                r.save()

        texto = "text"
        return render_to_response('cargar_archivo/plantillas.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('cargar_archivo/plantillas.html', {'texto': texto}, RequestContext(request))


def reporteVentas(request):
    vendedor = Vendedor.objects.values('id', 'codigo', 'nombre')

    return render_to_response('ventas/reporte_ventas.html', {'vendedor': vendedor,}, RequestContext(request))


@csrf_exempt
def obtenerReporteVentas(request):
    if request.method == 'POST':
        vendedor = request.POST.get('vendedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        cursor1 = connection.cursor();

        if vendedor == '0':
            cursor1.execute(
                "select distinct v.id,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");

        else:
            cursor1.execute(
                "select distinct v.id,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and v.id=" + vendedor + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");

        row1 = cursor1.fetchall();

        total = 0
        descuento = 0
        porcentaje = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p1 in row1:
            total = 0
            descuento = 0
            porcentaje = 0
            subtotal = 0
            iva = 0
            html += '<tr><th colspan="9"> ' + str(p1[1]) + '</th></tr>'
            cursor.execute(
                "select distinct p.id,p.tipo,p.fecha,p.codigo,p.descripcion,p.detalle,p.cantidad,p.codigo,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva,p.total,p.porcentaje_descuento,p.descuento,v.nombre from proforma p,cliente c,vendedor v where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True' and v.id=" + str(
                    p1[0]) + "and p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "'");
            row = cursor.fetchall();
            html = ''
            for p in row:
                html += '<tr><td>Muedirsa</td><td>' + str(p[2]) + '</td>'
                html += '<td>' + str(p[3]) + '</td>'
                html += '<td></td>'
                html += '<td>' + str(p[8]) + '</td>'

                html += '<td>' + str(p[12]) + '</td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'

                html += '</tr>'
                iva = iva + p[11]
                total = total + p[12]
                porcentaje = porcentaje + p[13]
                descuento = descuento + p[14]
                subtotal = subtotal + p[10]
            html += '<tr><th colspan="5">Total de ' + str(p[15]) + '</th>'
            html += '<th>' + str(subtotal) + '</th>'
            html += '<th>' + str(porcentaje) + '</th>'
            html += '<th>' + str(descuento) + '</th>'
            html += '<th>' + str(iva) + '</th>'
            html += '<th>' + str(total) + '</th>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


@csrf_exempt
def controlCobroDiarioReport(request):
    if request.method == 'POST':
        texto = "Hola mundo"
        return render_to_response('ventas/cobro-diario.html', {'texto': texto}, RequestContext(request))
    else:
        texto = "Hola mundo"
        return render_to_response('ventas/cobro-diario.html', {'texto': texto}, RequestContext(request))





def cargarPlantillaNormalCSV(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        abreviatura = request.POST['abreviatura']
        observaciones = request.POST['observacion']
        tipo = request.POST['tipo']
        dividir = request.POST['dividir']
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        portfolio = csv.DictReader(paramFile)
        users = []
        # archi=open(paramFil,'r')
        # linea=paramFile.readline()
        # while linea!="":

        # linea=archi.readline()
        plantilla = PlantillaRrhh()
        plantilla.codigo = codigo
        plantilla.abreviatura = abreviatura
        plantilla.nombre = nombre
        plantilla.observaciones = observaciones
        plantilla.created_by = request.user.get_full_name()
        plantilla.updated_by = request.user.get_full_name()
        plantilla.created_at = datetime.now()
        plantilla.updated_at = datetime.now()
        plantilla.save()

        try:
            secuencial = Secuenciales.objects.get(modulo='plantillas')
            secuencial.secuencial = secuencial.secuencial + 1
            secuencial.created_by = request.user.get_full_name()
            secuencial.updated_by = request.user.get_full_name()
            secuencial.created_at = datetime.now()
            secuencial.updated_at = datetime.now()
            secuencial.save()
        except Secuenciales.DoesNotExist:
            secuencial = None

        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            print x[0]
            if len(x[0]):

                try:
                    empleado = Empleado.objects.get(cedula_empleado=x[0])

                except Empleado.DoesNotExist:
                    empleado = None

                if empleado:
                    try:
                        existe = PlantillaRrhhDetalle.objects.get(empleado_id=empleado.empleado_id,
                                                                  plantilla_rrhh_id=plantilla.id,
                                                                  tipo_ingreso_egreso_empleado_id=tipo)

                    except PlantillaRrhhDetalle.DoesNotExist:
                        existe = None

                    if existe:
                        valor_actual = existe.valor
                        v =float(x[1].replace(',', '.'))
                        print ('sueldo unificado entro' + str(x[1]))
                        valor = float(v)

                        valor_total = valor_actual + valor
                        existe.valor = valor_total
                        existe.save()

                    else:

                        detalle = PlantillaRrhhDetalle()
                        detalle.plantilla_rrhh_id = plantilla.id
                        detalle.empleado_id = empleado.empleado_id
                        detalle.tipo_ingreso_egreso_empleado_id = tipo
                        v = float(x[1].replace(',', '.'))
                        print ('sueldo unificado' + str(x[1]))
                        valor = float(v)
                        detalle.valor = valor
                        detalle.save()


                else:
                    print('entroNOempleado')




            else:
                print('hola')

        texto = "text"
        if dividir!=1 :
            existe_recorrer = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=plantilla.id,
                                                  tipo_ingreso_egreso_empleado_id=tipo)
            if existe_recorrer:
                for r in existe_recorrer:
                    valor_cambiar=float(r.valor)


                    valor = float(valor_cambiar)/float(dividir)
                    valor=float(valor+0.000001)

                    r.valor = round(valor,2)
                    r.save()

        tipo = TipoIngresoEgresoEmpleado.objects.all()
        return render_to_response('cargar_archivo/plantillas_normal.html', {'texto': texto,'tipo': tipo}, RequestContext(request))


    else:
        texto = "text"
        tipo=TipoIngresoEgresoEmpleado.objects.all()
        return render_to_response('cargar_archivo/plantillas_normal.html', {'texto': texto,'tipo': tipo}, RequestContext(request))


# Create your views here.
def prueba(request):
    row = "text"

    return render_to_response('principal/permiso.html', {'row': row}, RequestContext(request))

@transaction.atomic
def MigracionCliente(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            print "validando..."

            if len(x[0]):

                codigo = x[0].decode('unicode-escape')
                razon_social = x[1].decode('unicode-escape')
                nombre = x[2].decode('unicode-escape')
                direccion = x[3].decode('unicode-escape')
                ruc = x[4]
                telefono = x[9]





                try:
                    cliente = Cliente.objects.get(codigo_cliente=codigo)

                except Cliente.DoesNotExist:
                    cliente = None
                usern=request.user.get_full_name()
                fecha=datetime.now()

                if cliente:
                    print ("entroooooo")
                    print cliente.id_cliente

                else:
                    with transaction.atomic():
                        rz = RazonSocial()
                        rz.codigo_razon_social=codigo
                        rz.nombre=razon_social
                        rz.direccion1=direccion
                        rz.telefono1=telefono
                        rz.contacto=nombre
                        rz.created_by = request.user.get_full_name()
                        rz.updated_by = request.user.get_full_name()
                        rz.created_at = datetime.now()
                        rz.updated_at = datetime.now()
                        rz.base = True
                        rz.plan_de_cuentas_id=1055
                        rz.save()

                        # cursor = connection.cursor();
                        # sql = "insert into cliente (codigo_cliente,nombre_cliente,ruc,direccion1,contacto,telefono1,created_by,updated_by,base,cuenta_contable_venta_id,cuenta_cobrar_id,created_at,updated_at) VALUES ('"+str(codigo)+ "','" +str(nombre)+ "','" +ruc+ "','" +str(direccion)+ "','" +str(nombre) + "','" + telefono + "','" + str(usern)+ "','" + str(usern) + "','True',1055,22,'"+str(fecha)+"','"+str(fecha)+"')"
                        # cursor.execute(sql)
                        # row = cursor.fetchall();
                        #
                        # try:
                        #     cliente_a = Cliente.objects.get(codigo_cliente=codigo)
                        #
                        # except Cliente.DoesNotExist:
                        #     cliente_a = None

                        cliente= Cliente()
                        cliente.codigo_cliente = codigo
                        cliente.nombre_cliente = nombre
                        cliente.ruc = ruc
                        cliente.direccion1 = direccion
                        cliente.contacto = nombre
                        cliente.telefono1 = telefono
                        cliente.created_by = request.user.get_full_name()
                        cliente.updated_by = request.user.get_full_name()
                        cliente.created_at = datetime.now()
                        cliente.updated_at = datetime.now()
                        cliente.cuenta_contable_venta_id=1055
                        cliente.cuenta_cobrar_id=22
                        cliente.base = True
                        cliente.save()

                        razon_cliente=RazonSocialClientes()
                        razon_cliente.cliente_id =cliente.id_cliente
                        razon_cliente.razon_social_id=rz.id
                        razon_cliente.created_by = request.user.get_full_name()
                        razon_cliente.updated_by = request.user.get_full_name()
                        razon_cliente.created_at = datetime.now()
                        razon_cliente.updated_at = datetime.now()
                        razon_cliente.save()
                        print('entroNOempleado')

            else:
                print('hola')

        texto = "text"
        return render_to_response('cargar_archivo/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('cargar_archivo/migracion.html', {'texto': texto}, RequestContext(request))



def reporteEgresoxOrdenEgreso(request):
    bodega = Bodega.objects.values('id', 'codigo_bodega', 'nombre')

    return render_to_response('inventario/egreso_orden_egreso.html', {'bodega': bodega,}, RequestContext(request))


@csrf_exempt
def obtenerEgresoxOrdenEgreso(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();

        sql = "select distinct p.id,ep.codigo,ep.fecha,p.notas,ep.comentario,p.bodega_id,p.aprobada,p.orden_produccion_codigo,b.nombre,p.codigo,ep.subtotal,ep.iva,ep.total from orden_egreso p,bodega b,egreso_orden_egreso ep where b.id=p.bodega_id and ep.orden_egreso_id=p.id and p.bodega_id=" + bodega

        if fechainicial == '0':
            print("entro no feccha inicial")

        else:
            sql += " and ep.fecha>='" + fechainicial + "'"
        if fechafin == '0':
            print("entro no fecha final")

        else:
            sql += " and ep.fecha<='" + fechafin + "'"

        sql += " order by ep.fecha"
        cursor.execute(sql)
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        total=0
        cantidad=0
        costo=0
        total_t=0
        subtotal_t=0
        iva_t=0
        for p in row:

            ped = OrdenEgresoDetalle.objects.filter(orden_egreso_id=str(p[0]))
            cont=0
            for pe in ped:
                cont=cont+1

                html += '<tr>'
                if cont == 1:
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[2]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[1]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="' + str(ped.count()) + '">' + str(p[9]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[3].encode('utf8')) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[4].encode('utf8')) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[7].encode('utf8')) + '</td>'

                html += ' <td> ' + str(pe.producto.codigo_producto.encode('utf8')) + ' </td>'
                html += ' <td> ' + str(pe.producto.descripcion_producto.encode('utf8')) + ' </td>'
                html += '<td>' + str(pe.cantidad) + '</td>'
                html += '<td>'+str(pe.precio_compra)+'</td><td>'+str(pe.total)+'</td>'
                if cont == 1:
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[10]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[11]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="' + str(ped.count()) + '">' + str(p[12]) + '</td>'
                    subtotal_t = subtotal_t + p[10]
                    iva_t = iva_t + p[11]
                    total_t=total_t+p[12]

                html += '</tr>'
                total = total + pe.total
                cantidad = cantidad + pe.cantidad
                costo = costo + pe.precio_compra

        html += '<tr><td colspan="7"></td>'
        html += '<td><b>Total</b></td>'
        html += '<td><b>' + str(cantidad) + '</b></td>'
        html += '<td><b>' + str(costo) + '</b></td>'
        html += '<td><b>' + str(total) + '</b></td>'

        html += '<td><b>' + str(subtotal_t) + '</b></td>'
        html += '<td><b>' + str(iva_t) + '</b></td>'
        html += '<td><b>' + str(total_t) + '</b></td>'
        html += '</tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404




def reporteKardex(request):
    bodega = Bodega.objects.values('id', 'codigo_bodega', 'nombre')
    tipos = TipoProducto.objects.values('id', 'codigo', 'descripcion')

    return render_to_response('inventario/kardex.html', {'bodega': bodega, 'tipos': tipos}, RequestContext(request))


@csrf_exempt
def obtenerKardex(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        cursor = connection.cursor();
        sql=''
        sql+="select distinct k.egreso,k.fecha_ingreso,k.fecha_egreso,p.codigo_producto,p.descripcion_producto,k.descripcion,b.codigo_bodega,b.nombre,p.cant_maxima,p.cant_minimia,t.descripcion,p.costo,k.cantidad,k.created_at,p.producto_id,b.id from producto p,bodega b,tipo_producto t,kardex k where  b.id=k.bodega_id and p.tipo_producto=t.id and k.producto_id=p.producto_id and k.bodega_id=" + bodega

        if codigo!= '':
            sql +=" and p.codigo_producto like '%" +codigo+ "%'"
        if nombre!= '':
            sql +=" and p.descripcion_producto like '%" +nombre+ "%'"
        sql+=" order by k.created_at"
        cursor.execute(sql);
        row = cursor.fetchall();
        total_cantidad = 0
        total_costo = 0.0
        total_c = 0
        total_valor=0
        cant=0
        cost=0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        entrada=0
        salida=0
        for p in row:
            html += '<tr>'

            if p[0]:
                html += '<td>' +  str(p[2]) + '</td>'
            else:
                html += '<td>' + str(p[1]) + '</td>'
            html += '<td>' + str(p[3].encode('utf8')) + '</td>'
            html += '<td>' + str(p[4].encode('utf8'))+ '</td>'
            html += '<td>' + str(p[5]) + '</td>'
            html += '<td>' + str(p[7].encode('utf8')) + '</td>'

            if p[0]:
                html += '<td>0</td>'
            else:
                html += '<td>'+ str(p[12]) + '</td>'
                entrada=entrada+float(p[12])

            if p[0]:
                html += '<td>' + str(p[12]) + '</td>'
                salida = salida + +float(p[12])
            else:
                html += '<td>0</td>'
            try:
                pb = ProductoEnBodega.objects.filter(producto_id=str(p[14])).filter(bodega_id=str(p[15]))
            except ProductoEnBodega.DoesNotExist:
                pb = None

            if pb:
                html += '<td>' + str(pb[0].cantidad) + '</td>'
            else:
                html += '<td>0</td>'


	    #total_kit=float(p[4])*float(p[11])
	    #html += '<td>' + str(total_kit) + '</td>'

            html += '</tr>'
        html += '<tr><td colspan="5"><b>Total</b></td>'
        html += '<td><b>' + str(entrada) + '</b></td>'
        html += '<td><b>' + str(salida) + '</b></td>'
        html += '<td><b></b></td>'
        html += '</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404





def cargarReloj(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        portfolio = csv.DictReader(paramFile)
        users = []
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        # archi=open(paramFil,'r')
        # linea=paramFile.readline()
        # while linea!="":

        # linea=archi.readline()
        print 'quincena' + str(quincena)
        lineas = paramFile.split('\n')
        sabado = 0
        domingo = 0
        horas_sabado = 0
        horas_domingo = 0
        minutos_sabado = 0
        minutos_domingo = 0
        total_sabado = 0
        total_domingo = 0
        horas_no_trabajadas =0

        for linea in lineas:
            if len(linea):
                x = linea.split(";")


                if len(x[1]):
                    print 'entro1'
                    try:
                        empleado = Empleado.objects.get(codigo_reloj=x[1])

                    except Empleado.DoesNotExist:
                        empleado = None

                    if empleado:
                        print 'entro2'

                        # CALCULO DE HORAS TRABAJADAS DE SABADO Y DOMINGO


                        sabado= x[4].split(":")
                        domingo = x[5].split(":")
                        horas_sabado=sabado[0]
                        horas_domingo=domingo[0]
                        minutos_sabado = float(sabado[1])/60
                        minutos_domingo = float(domingo[1])/60

                        total_sabado=float(horas_sabado)+minutos_sabado
                        total_domingo=float(horas_domingo)+minutos_domingo
                        total_complementaria=0


                        if total_sabado>0:
                            total_complementaria=total_sabado
                        if total_domingo>0:
                            total_complementaria=total_complementaria+total_domingo

                        if total_complementaria > 0:
                            sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=empleado.empleado_id,
                                                                             tipo_ingreso_egreso_empleado_id=24)
                            valor = (sueldo.valor_mensual / 240) * 2 * total_complementaria
                            dias = IngresosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.quincena = quincena
                            dias.empleado = empleado
                            dias.fecha = x[1]
                            dias.hora_inicio = x[2]
                            dias.hora_fin = x[3]
                            dias.horas = round(float(total_complementaria), 2)
                            dias.tipo_ingreso_egreso_empleado_id = 25
                            dias.valor = round(float(valor), 2)
                            dias.pagar=True
                            dias.nombre = "HORAS EXTRAORDINARIAS"
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.save()

                        # CALCULO DE HORAS TRABAJADAS DE LUNES A VIERNES

                        lunes_viernes = x[6].split(":")
                        horas_lunes_viernes = float(lunes_viernes[0])
                        minutos_lunes_viernes = float(lunes_viernes[1]) / 60

                        total_lunes_viernes= horas_lunes_viernes + minutos_lunes_viernes
                        if total_lunes_viernes>0:
                            sueldo = IngresosProyectadosEmpleado.objects.get(
                                empleado_id=empleado.empleado_id, tipo_ingreso_egreso_empleado_id=24)
                            valor = (sueldo.valor_mensual / 240) * 1.5 * total_lunes_viernes
                            dias = IngresosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.quincena = quincena
                            dias.empleado = empleado
                            dias.horas = round(float(total_lunes_viernes), 2)
                            dias.tipo_ingreso_egreso_empleado_id = 5
                            dias.valor = round(float(valor), 2)
                            dias.nombre = "HORAS SUPLEMENTARIAS"
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.pagar = True
                            dias.save()

                        # CALCULO DE ATRASOS
                        # atraso= float(x[7])
                        # if atraso>0:
                        #     sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=empleado.empleado_id,
                        #                                                      tipo_ingreso_egreso_empleado_id=24)
                        #     horas_f = 8
                        #     valor = (sueldo.valor_mensual / 240) * float(atraso) * 2
                        #     dias = DiasNoLaboradosRolEmpleado()
                        #     dias.anio = anio
                        #     dias.mes = mes
                        #     dias.quincena = quincena
                        #     dias.empleado = empleado
                        #     dias.descontar = True
                        #     dias.dias = round(float(atraso), 2)
                        #     dias.tipo_ausencia_id = 5
                        #     dias.valor = round(float(valor), 2)
                        #     dias.save()

                        # CALCULO DE fLTAS INJUSTIFICADAS
                        faltas_injustificados=float(x[8])
                        if faltas_injustificados>0:
                            sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=empleado.empleado_id,
                                                                             tipo_ingreso_egreso_empleado_id=24)
                            valor = (sueldo.valor_mensual / 240) * 8 *float(faltas_injustificados) * 2
                            dias = DiasNoLaboradosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.quincena = quincena
                            dias.empleado = empleado
                            dias.dias = 8*float(faltas_injustificados)
                            dias.tipo_ausencia_id = 3
                            dias.valor = round(float(valor), 2)
                            dias.descontar = True
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.save()
                        # CALCULO DE fLTAS JUSTIFICADAS
                        faltas_justificados = float(x[9])
                        if faltas_justificados > 0:
                            sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=empleado.empleado_id,
                                                                             tipo_ingreso_egreso_empleado_id=24)
                            valor = (sueldo.valor_mensual / 240) * 8 * float(faltas_justificados)* 2
                            dias = DiasNoLaboradosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.quincena = quincena
                            dias.empleado = empleado
                            dias.dias = 8*float(faltas_justificados)
                            dias.tipo_ausencia_id = 2
                            dias.valor = round(float(valor), 2)
                            dias.descontar = True
                            dias.cargar_vacaciones = True
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.save()


                        # CALCULO DE HORAS NO TRABAJADAS
                        thoras_no_trabajadas= x[10].split(":")
                        horas_no_trabajadas = float(thoras_no_trabajadas[0])
                        minutos_horas_no_trabajadas = float(thoras_no_trabajadas[1]) / 60

                        total_horas_no_trabajadas= horas_no_trabajadas + minutos_horas_no_trabajadas

                        if total_horas_no_trabajadas>0:
                            sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=empleado.empleado_id,
                                                                             tipo_ingreso_egreso_empleado_id=24)
                            horas_f = 8
                            dias = DiasNoLaboradosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.quincena = quincena
                            dias.empleado = empleado
                            dias.descontar = True
                            valor = (sueldo.valor_mensual / 240) * total_horas_no_trabajadas * 2
                            dias.dias = round(float(total_horas_no_trabajadas), 2)
                            dias.tipo_ausencia_id = 5
                            dias.valor = round(float(valor), 2)
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.save()

                    else:
                        print('entroNOempleado')




                else:
                    print('hola')

        texto = "text"
        return render_to_response('cargar_archivo/index.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('cargar_archivo/index.html', {'texto': texto}, RequestContext(request))










def cargarRelojFinal(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        portfolio = csv.DictReader(paramFile)
        users = []
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        # archi=open(paramFil,'r')
        # linea=paramFile.readline()
        # while linea!="":

        # linea=archi.readline()
        #print 'quincena' + str(quincena)
        lineas = paramFile.split('\n')
        sabado = 0
        domingo = 0
        horas_sabado = 0
        horas_domingo = 0
        minutos_sabado = 0
        minutos_domingo = 0
        total_sabado = 0
        total_domingo = 0
        horas_no_trabajadas =0

        for linea in lineas:
            if len(linea):
                x = linea.split(";")


                if len(x[1]):
                    print 'entro1'
                    try:
                        empleado = Empleado.objects.get(cedula_empleado=x[0])

                    except Empleado.DoesNotExist:
                        empleado = None

                    if empleado:
                        print 'entro2'

                        # CALCULO DE HORAS TRABAJADAS DE SABADO Y DOMINGO


                        sabado= x[7]
                        domingo = x[8]
                        total_sabado=float(sabado.replace(',', '.'))
                        total_domingo = float(domingo.replace(',', '.'))




                        if total_sabado>0:
                            sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=empleado.empleado_id,
                                                                             tipo_ingreso_egreso_empleado_id=24)
                            valor = (sueldo.valor_mensual / 240) * 2 * total_sabado
                            dias = IngresosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.empleado = empleado
                            dias.horas = round(float(total_sabado), 2)
                            dias.tipo_ingreso_egreso_empleado_id = 25
                            dias.valor = round(float(valor), 2)
                            dias.pagar = True
                            dias.nombre = "HORAS EXTRA SABADOS"
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.save()
                        if total_domingo>0:
                            sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=empleado.empleado_id,
                                                                             tipo_ingreso_egreso_empleado_id=24)
                            valor = (sueldo.valor_mensual / 240) * 2 * total_domingo
                            dias = IngresosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.empleado = empleado
                            dias.horas = round(float(total_domingo), 2)
                            dias.tipo_ingreso_egreso_empleado_id = 26
                            dias.valor = round(float(valor), 2)
                            dias.pagar = True
                            dias.nombre = "HORAS EXTRA DOM Y FERIADOS"
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.save()


                        # CALCULO DE HORAS TRABAJADAS DE LUNES A VIERNES

                        lunes_viernes = float(x[6].replace(',','.'))

                        if lunes_viernes>0:
                            sueldo = IngresosProyectadosEmpleado.objects.get(
                                empleado_id=empleado.empleado_id, tipo_ingreso_egreso_empleado_id=24)
                            valor = (sueldo.valor_mensual / 240) * 1.5 * lunes_viernes
                            dias = IngresosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.empleado = empleado
                            dias.horas = round(float(lunes_viernes), 2)
                            dias.tipo_ingreso_egreso_empleado_id = 5
                            dias.valor = round(float(valor), 2)
                            dias.nombre = "HORAS SUPLEMENTARIAS"
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.pagar = True
                            dias.save()


                        # Comisiones

                        comisiones=float(x[9].replace(',','.'))

                        if comisiones>0:
                            dias = IngresosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.empleado = empleado
                            dias.tipo_ingreso_egreso_empleado_id = 4
                            dias.valor = round(float(comisiones), 2)
                            dias.nombre = "COMISIONES"
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.pagar = True
                            dias.save()

                        if x[10]:
                            bonificaciones= float(x[10].replace(',','.'))

                            if bonificaciones > 0:
                                dias = IngresosRolEmpleado()
                                dias.anio = anio
                                dias.mes = mes
                                dias.empleado = empleado
                                dias.tipo_ingreso_egreso_empleado_id = 3
                                dias.valor = round(float(bonificaciones), 2)
                                dias.nombre = "BONIFICACIONES"
                                dias.created_by = request.user.get_full_name()
                                dias.updated_by = request.user.get_full_name()
                                dias.created_at = datetime.now()
                                dias.updated_at = datetime.now()
                                dias.pagar = True
                                dias.save()

                        alimentacion = float(x[11].replace(',','.'))

                        if alimentacion > 0:
                            dias = IngresosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.empleado = empleado
                            dias.tipo_ingreso_egreso_empleado_id = 1
                            dias.valor = round(float(alimentacion), 2)
                            dias.nombre = "ALIMENTACION Y TRANSP."
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.pagar = True
                            dias.save()
                        #ATRASOS
                        if x[17]:
                            atrasos = float(x[17].replace(',', '.'))

                            if atrasos > 0:
                                sueldo = IngresosProyectadosEmpleado.objects.get(
                                    empleado_id=empleado.empleado_id, tipo_ingreso_egreso_empleado_id=24)
                                valor = ((sueldo.valor_mensual / 30)/8)* atrasos
                                dias = EgresosRolEmpleado()
                                dias.anio = anio
                                dias.mes = mes
                                dias.empleado = empleado
                                dias.tipo_ingreso_egreso_empleado_id = 21
                                dias.valor = round(float(valor), 2)
                                dias.nombre = "MULTAS"
                                dias.created_by = request.user.get_full_name()
                                dias.updated_by = request.user.get_full_name()
                                dias.created_at = datetime.now()
                                dias.updated_at = datetime.now()
                                dias.pagar = True
                                dias.save()

                    else:
                        print('entroNOempleado')




                else:
                    print('hola')

        texto = "text"
        anio = Anio.objects.all()
        return render_to_response('cargar_archivo/index.html', {'texto': texto,'anio': anio}, RequestContext(request))


    else:
        texto = "text"
        anio = Anio.objects.all()
        return render_to_response('cargar_archivo/index.html', {'texto': texto,'anio': anio}, RequestContext(request))



def reporteInventarioExistente(request):
    html='Inventario'

    return render_to_response('inventario/inventario_existente.html', {'html': html,}, RequestContext(request))


@csrf_exempt
def obtenerInventarioInicial(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        date = datetime.strptime(fechainicial, "%Y-%m-%d").date()
        total_inve=0
        cursor = connection.cursor()
        sql="SELECT p.producto_id,codigo_producto,descripcion_producto,p.tipo_producto,p.costo,inventario,total_compras,total_egresos FROM producto p LEFT JOIN (  SELECT cd.producto_id, SUM(cd.cantidad) total_compras FROM compras_detalle cd,orden_compra oc," \
            "compras_locales cl where cd.compra_id=oc.compra_id and cl.orden_compra_id=oc.compra_id and cl.fecha>='2017-01-01 00:00:00' and cl.fecha<'"+str(fechainicial)+"' and cd.recibido=True GROUP BY producto_id ) compras ON p.producto_id = compras.producto_id LEFT JOIN ( SELECT od.producto_id, SUM(od.cantidad) total_egresos FROM orden_egreso_detalle od,orden_egreso oe, egreso_orden_egreso eoe " \
             "where od.orden_egreso_id=oe.id and eoe.orden_egreso_id=oe.id and od.disminuir_kardex=True and eoe.fecha>='2017-01-01 00:00:00' and eoe.fecha<'"+str(fechainicial)+"' GROUP BY producto_id ) egresos ON p.producto_id = egresos.producto_id" \
              " LEFT JOIN (  SELECT producto_id, SUM(cantidad) inventario FROM inventario GROUP BY producto_id ) inventarios ON p.producto_id = inventarios.producto_id where p.tipo_producto!=2 and  p.tipo_producto!=7";

        cursor.execute(sql)
        print sql

        row = cursor.fetchall()
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            print('entro'+str(p[0]))
            cantidad_actual=0
            html += '<tr>'
            html+='<td>'+str(p[1])+'</td>'
            html += '<td>' + str(p[2].encode('utf8')) + '</td>'
            # html += '<td>' + str(p[5]) + '</td>'
            # html += '<td>'+ str(p[3]) + '</td>'
            # html += '<td>'+ str(p[4]) + '</td>'
            if p[5]:
                cantidad_inicial=p[5]
            else:
                cantidad_inicial=0

            if p[6]:
                ingresos=p[6]
            else:
                ingresos=0

            if p[7]:
                egresos=p[7]
            else:
                egresos=0

            cantidad_actual=cantidad_inicial+ingresos-egresos

            html += '<td>' + str(cantidad_actual).replace('.', ',') + '</td>'

            sql1 = "SELECT p.producto_id,total_compras,total_egresos FROM producto p LEFT JOIN (  SELECT cd.producto_id, SUM(cd.cantidad) total_compras FROM compras_detalle cd,orden_compra oc,compras_locales cl where " \
                   "cl.orden_compra_id=oc.compra_id and cd.compra_id=oc.compra_id and cl.fecha>='"+str(fechainicial)+"' and cl.fecha<='"+str(fechafin)+"'  and cd.recibido=True GROUP BY producto_id )  compras ON p.producto_id = compras.producto_id LEFT JOIN (  SELECT od.producto_id, SUM(od.cantidad) total_egresos FROM orden_egreso_detalle od,orden_egreso oe, egreso_orden_egreso eoe where od.orden_egreso_id=oe.id and eoe.orden_egreso_id=oe.id and od.disminuir_kardex=True " \
                   "and eoe.fecha>='"+str(fechainicial)+"' and eoe.fecha<='"+str(fechafin)+"'  and eoe.anulado is not True  and oe.anulado is not True GROUP BY producto_id ) egresos ON p.producto_id = egresos.producto_id where p.tipo_producto!=2 and  p.tipo_producto!=7 and p.producto_id="+str(p[0])+"; "
            cursor.execute(sql1)
            row_ingresos = cursor.fetchall()
            if row_ingresos:
                ingresos=0
                egresos = 0
                for i in row_ingresos:
                    if i[1]:
                        ingresos=ingresos+i[1]

                    if i[2]:
                        egresos = egresos + i[2]
            else:
                ingresos=0
                egresos = 0

            html += '<td>' + str(ingresos).replace('.', ',') + '</td>'
            html += '<td>' + str(egresos).replace('.', ',') + '</td>'
            total_inve=cantidad_actual+ingresos-egresos
            html+= '<td>' + str(total_inve).replace('.', ',') + '</td>'
            if p[4]:
                total_costo=p[4]*total_inve
            else:
                total_costo=0
            html += '<td>' + str(p[4]).replace('.', ',') + '</td>'
            html += '<td>' + str(total_costo).replace('.', ',') + '</td>'
            total_inve=total_inve+total_costo

            html += '</tr>'


        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteFacturaProveedor(request):

    return render_to_response('transacciones/facturas_proveedores.html', {}, RequestContext(request))

@csrf_exempt
def obtenerFacturaProveedor(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        sql_v=" SELECT  distinct documento_compra.fecha_emision,documento_compra.establecimiento,documento_compra.punto_emision,documento_compra.secuencial,documento_compra.autorizacion,documento_compra.descripcion,documento_compra.base_iva_0,documento_compra.valor_iva_0,documento_compra.base_iva,documento_compra.valor_iva,"
        sql_v+=" documento_compra.porcentaje_iva,documento_compra.subtotal,documento_compra.descuento,documento_compra.total,proveedor.nombre_proveedor,orden_compra.nro_compra,compras_locales.codigo,sustento_tributario.descripcion, "
        sql_v+="sri_forma_pago.descripcion,documento_retencion_compra.establecimiento,documento_retencion_compra.punto_emision,documento_retencion_compra.secuencial,documento_retencion_compra.autorizacion,documento_retencion_compra.valor_retenido, proveedor.codigo_proveedor,proveedor.ruc,documento_retencion_compra.id,documento_compra.tipo_provision,documento_compra.base_no_iva_factura,documento_compra.base_rise_factura,sustento_tributario.codigo FROM documento_compra LEFT JOIN proveedor ON proveedor.proveedor_id=documento_compra.proveedor_id "
        sql_v+="LEFT JOIN sustento_tributario ON sustento_tributario.id=documento_compra.sustento_tributario_id LEFT JOIN orden_compra ON orden_compra.compra_id=documento_compra.orden_compra_id LEFT JOIN compras_locales ON compras_locales.id=documento_compra.compra_id LEFT JOIN sri_forma_pago ON sri_forma_pago.id=documento_compra.sri_forma_pago_id LEFT JOIN documento_retencion_compra ON documento_retencion_compra.documento_compra_id=documento_compra.id where documento_compra.fecha_emision>='" + fechainicial + "'and documento_compra.fecha_emision<='" + fechafin + "' and documento_compra.anulado is not True and documento_compra.no_afecta is not True order by documento_compra.fecha_emision"
        cursor.execute(sql_v);
        row = cursor.fetchall();
        print(sql_v)
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table2 table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead><tr><th>TIPO</th><th>RUC del Proveedor</th><th>Codigo del Proveedor</th><th>Fecha</th>'
        html+='<th>Proveedor</th><th>Detalle de la factura</th><th>Forma de Pago</th><th>Sustento Tributario</th><th>Codigo del establecimiento</th>'
        html+='<th>Punto Emision</th><th>Secuencial</th><th>No. Autorizacion</th>'
        html += '<th>Base 0%</th><th>Base no sujeto a IVA</th><th>RISE</th>'
        html += '<th>Base IVA 14%</th><th>IVA 14%</th><th>Total</th><th>Codigo Ret. IVA</th><th>Codigo Ret Fuent.</th><th>Valor ret. imp. Renta'
        html+='</th><th>%Retenc. IVA</th><th>Valor Retencion iva</th><th>No. Retencion</th><th>No. Autoriz. Retencion</th><th>Valor cancelado</th></tr></thead>'
        html+='<tbody><tr>'
        
        for p in row:
            if p[27]:
                html += '<td style="text-align:center">' + str(p[27].encode('utf8')) +'</td>'
            else:
                html += '<td></td>'
                
            if p[25]:
                html += '<td style="text-align:left">&nbsp;' + str(p[25].encode('utf8')) +'</td>'
            else:
                html += '<td></td>'
                
            if p[24]:
                html += '<td style="text-align:center">' + str(p[24].encode('utf8'))+''+ '</td>'
            else:
                html += '<td></td>'
                
            html += '<td>' + str(p[0]) + '</td>'
            html += '<td style="text-align:center">' + str(p[14].encode('utf8')) + '</td>'
            html += '<td>' + str(p[5].encode('utf8')) + '</td>'
            
            if p[18]:
                html += '<td>' + str(p[18].encode('utf8')) + '</td>'
            else:
                html += '<td></td>'
                
            #Sustento Tributario
            if p[30]:
                html += '<td style="text-align:center">' + str(p[30]) + '</td>'
            else:
                html += '<td></td>'
            if p[1]:
                html += '<td style="text-align:center">' + str(p[1]) + '</td>'
            else:
                html += '<td></td>'
            
            if p[2]:
                html += '<td style="text-align:center">' + str(p[2]) + '</td>'
            else:
                html += '<td></td>'
            
            if p[3]:
                html += '<td style="text-align:center">' + str(p[3]) + '</td>'
            else:
                html += '<td></td>'
            if p[4]:
                html += '<td style="text-align:left">&nbsp;' + str(p[4].encode('utf8')) + '</td>'
            else:
                html += '<td></td>'
            
            # if p[15]:
            #     html += '<td>' + str(p[15]) +' ' +'</td>'
            # else:
            #     html += '<td></td>'
            # 
            # if p[16]:
            #     html += '<td>' + str(p[16]) +' '+ '</td>'
            # else:
            #     html += '<td></td>'
                
            
            if p[6]:
                html += '<td align="right">' + str("%2.2f" % p[6]).replace('.', ',')  + '</td>'
            else:
                html += '<td></td>'
            if p[28]:
                html += '<td align="right">' + str("%2.2f" % p[28]).replace('.', ',') + '</td>'
            else:
                html += '<td align="right"></td>'
            
            if p[29]:
                html += '<td align="right">' + str("%2.2f" % p[29]).replace('.', ',')  + '</td>'
            else:
                html += '<td align="right"></td>'
            
                
            if p[8]:
                html += '<td align="right">' + str("%2.2f" % p[8]).replace('.', ',') + '</td>'
            else:
                html += '<td></td>'
            if p[9]:
                html += '<td align="right">' + str("%2.2f" % p[9]).replace('.', ',') + '</td>'
            else:
                html += '<td></td>'
            
           
            
            if p[13]:
                html += '<td align="right">' + str("%2.2f" % p[13]).replace('.', ',')  + '</td>'
                totalf=p[13]
            else:
                html += '<td></td>'
                totalf=0
            
            if p[19]:
                ret=p[19]
            else:
                ret=''
            
            if p[20]:
                ret2=p[20]
            else:
                ret2=''
            
            if p[21]:
                ret3=p[21]
            else:
                ret3=''
  
            ret_val=0
            codigo_retencion=''
            porcentaje=0
            valor_iva=0
            valor_rf=0
            codigo_rf=''
            
            
            if p[26]:
                cursor = connection.cursor();
                sql="select dc.documento_retencion_compra_id,dc.retencion_detalle_id,dc.valor_retenido,rd.codigo,rd.descripcion,rd.tipo_retencion_id,dc.porcentaje_retencion from documento_retencion_detalle_compra dc,retencion_detalle rd where rd.id=dc.retencion_detalle_id  and dc.documento_retencion_compra_id=" + str(p[26])
                print sql
                cursor.execute(sql);
                row2 = cursor.fetchall()
                for p2 in row2:
                    if p2[5] == 2 :
                        
                        if p2[3]:
                            codigo_retencion=str(p2[3])+' '
                            
                        
                        if p2[6]:
                            porcentaje=p2[6]
                        
                        if p2[2]:
                            valor_iva=p2[2]
                    else:
                        
                        codigo_rf=str(p2[3])+' '
                        if p2[2]:
                            valor_rf=p2[2]
                        
                        
                            
                
                html+='<td style="text-align:center">'+str(codigo_retencion)+'</td>'
                html+='<td style="text-align:center">'+str(codigo_rf)+'</td>'
                cod=1
            
                # if codigo_rf == '332 ':
                #     if codigo_retencion.isalnum():
                #         
                #         cod=1
                #     else:
                #         cod=0
                # else:
                #     cod=1
                
                
                    
                html+='<td align="right">'+str("%2.2f" % valor_rf).replace('.', ',') +'</td>'
                html+='<td align="right">'+str("%2.2f" % porcentaje).replace('.', ',') +'</td>'
                html+='<td align="right">'+str("%2.2f" % valor_iva).replace('.', ',') +'</td>'
                
                retdetalle = DocumentosRetencionDetalleCompra.objects.filter(documento_retencion_compra_id=str(p[26])).aggregate(Sum('valor_retenido'))

               
                if retdetalle['valor_retenido__sum']:
                    ret_val=retdetalle['valor_retenido__sum']
                    #html += '<td>'+str(retdetalle['valor_retenido__sum'])+'</td>'
                
                    
                
            else:
                html += '<td align="right"></td>'
                html += '<td align="right"></td>'
                html += '<td align="right">0,00</td>'
                html += '<td align="right">0,00</td>'
                html += '<td align="right">0,00</td>'
            
            #html += '<td>' + str(ret) + '-'+ str(ret2) + '-'+ str(ret3) + '</td>'
            est_ret=''
            pt_ret=''
            sec_ret=''
            if p[19]:
                est_ret=p[19] +'-'
            else:
                est_ret=''
            
            if p[20]:
                pt_ret=p[20] +'-'
            else:
                pt_ret=''
            
            if p[21]:
                sec_ret=p[21] 
            else:
                sec_ret=''
            
            if cod == 0:
                html += '<td style="text-align:center"></td>'
                html += '<td></td>'
    
                
            else:
                html += '<td style="text-align:center">' + str(est_ret) +''+str(pt_ret)+' '+str(sec_ret)+'</td>'
                if p[22]:
                    html += '<td style="text-align:center">' + str(p[22]) + '</td>'
                else:
                    html += '<td></td>'
    
            total=totalf-ret_val
            html += '<td align="right">' + str("%2.2f" % total).replace('.', ',') + '</td>'
                
             
            html += '</tr>'
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404
def reportePorProveedorFacurasCanceladasCheque(request):
    proveedor = Proveedor.objects.all()

    return render_to_response('transacciones/facturas_proveedor_canceladas_cheque.html', {'proveedor': proveedor}, RequestContext(request))

@csrf_exempt
def obtenerFacturaProveedorFacurasCanceladasCheque(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        proveedor = request.POST.get('proveedor')

        cursor = connection.cursor();
        cursor.execute(" SELECT  distinct documento_compra.fecha_emision,documento_compra.establecimiento,documento_compra.punto_emision,documento_compra.secuencial,documento_compra.autorizacion,documento_compra.descripcion,documento_compra.base_iva_0,documento_compra.valor_iva_0,documento_compra.base_iva,documento_compra.valor_iva,documento_compra.porcentaje_iva,documento_compra.subtotal,documento_compra.descuento,documento_compra.total,proveedor.nombre_proveedor,orden_compra.nro_compra,compras_locales.codigo,sustento_tributario.descripcion,sri_forma_pago.descripcion,documento_retencion_compra.establecimiento,documento_retencion_compra.punto_emision,documento_retencion_compra.secuencial,documento_retencion_compra.autorizacion,documento_retencion_compra.valor_retenido, proveedor.codigo_proveedor,proveedor.ruc,documento_retencion_compra.id,documento_compra.tipo_provision,documento_compra.base_no_iva_factura,documento_compra.base_rise_factura,documento_compra.anulado,documento_compra.id FROM documento_compra LEFT JOIN proveedor ON proveedor.proveedor_id=documento_compra.proveedor_id LEFT JOIN sustento_tributario ON sustento_tributario.id=documento_compra.sustento_tributario_id LEFT JOIN orden_compra ON orden_compra.compra_id=documento_compra.orden_compra_id LEFT JOIN compras_locales ON compras_locales.id=documento_compra.compra_id LEFT JOIN sri_forma_pago ON sri_forma_pago.id=documento_compra.sri_forma_pago_id LEFT JOIN documento_retencion_compra ON documento_retencion_compra.documento_compra_id=documento_compra.id where documento_compra.fecha_emision>='" + fechainicial + "'and documento_compra.fecha_emision<='" + fechafin + "' and documento_compra.proveedor_id="+proveedor+" and documento_compra.no_afecta is not True and documento_compra.anulado is not True");
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead><tr><th>TIPO</th>'
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        html+= '<th>No. Cheque</th>'
        html+= '<th>Fecha</th>'
        ##html+='<th>Proveedor</th>'
        ##html+='<th>Forma de Pago</th>'
        html+='<th>Factura</th>'

        # html+='<th>Codigo del establecimiento</th>'
        # html+='<th>Punto Emision</th><th>Secuencial</th>'
        ##html+='<th>No. Autorizacion</th>'
        # html += '<th>Base 0%</th><th>Base no sujeto a IVA</th><th>RISE</th>'
        # html += '<th>Base IVA 14%</th><th>IVA 14%</th>'
        html+='<th>Total de Facturas</th>'
        # html+='<th>Codigo Ret. IVA</th><th>Codigo Ret Fuent.</th><th>Valor ret. imp. Renta'
        # html+='</th><th>%Retenc. IVA</th><th>Valor Retencion iva</th><th>No. Retencion</th><th>No. Autoriz. Retencion</th>'
        html+='<th>Debito</th><th>Credito</th><th>Saldo</th><th>Concepto</th><th>Estado</th></tr></thead>'
        html+='<tbody><tr>'
        
        for p in row:
            if p[27]:
                html += '<td style="text-align:center"><b>' + str(p[27].encode('utf8')) +'</b></td>'
            else:
                html += '<td></td>'
            html+='<td></td>'
                
            # if p[25]:
            #     html += '<td style="text-align:center">' + str(p[25].encode('utf8')) +'</td>'
            # else:
            #     html += '<td></td>'
            #     
            # if p[24]:
            #     html += '<td style="text-align:center">' + str(p[24])+''+ '</td>'
            # else:
            #     html += '<td></td>'
                
            html += '<td><b>' + str(p[0]) + '</b></td>'
            #FORMA DE PAGO
            #html += '<td style="text-align:center">' + str(p[14].encode('utf8')) + '</td>'
            
            # if p[18]:
            #     html += '<td>' + str(p[18].encode('utf8')) + '</td>'
            # else:
            #     html += '<td></td>'
            factura=''
            if p[1]:
                #html += '<td style="text-align:center">' + str(p[1]) + '</td>'
                factura+=''+str(p[1]) +'-'
            else:
                factura+='-'
                #html += '<td></td>'
            
            if p[2]:
                #html += '<td style="text-align:center">' + str(p[2]) + '</td>'
                factura+=''+str(p[2]) +'-'
            else:
                #html += '<td></td>'
                factura+='-'
            
            if p[3]:
                #html += '<td style="text-align:center">' + str(p[3]) + '</td
                factura+=''+str(p[3]) 
            else:
                #html += '<td></td>'
                factura+=''
            html += '<td style="text-align:center"><b>' + str(factura) + '</b></td>'

         
            
            if p[13]:
                html += '<td style="text-align:center"><b>' + str("%2.2f" % p[13]).replace('.', ',') + '</b></td>'
                totalf=p[13]
            else:
                html += '<td></td>'
                totalf=0
            
            if p[19]:
                ret=p[19]
            else:
                ret=''
            
            if p[20]:
                ret2=p[20]
            else:
                ret2=''
            
            if p[21]:
                ret3=p[21]
            else:
                ret3=''
  
            ret_val=0
            codigo_retencion=''
            porcentaje=''
            valor_iva=''
            valor_rf=''
            codigo_rf=''
            
            
            if p[26]:
                cursor = connection.cursor();
                sql="select dc.documento_retencion_compra_id,dc.retencion_detalle_id,dc.valor_retenido,rd.codigo,rd.descripcion,rd.tipo_retencion_id,dc.porcentaje_retencion from documento_retencion_detalle_compra dc,retencion_detalle rd where rd.id=dc.retencion_detalle_id  and dc.documento_retencion_compra_id=" + str(p[26])
                print sql
                cursor.execute(sql);
                row2 = cursor.fetchall()
                for p2 in row2:
                    if p2[5] == 2 :
                        print("entro a 2")
                        print p2[1]
                        print p2[3]
                        if p2[3]:
                            codigo_retencion=str(p2[3])+' '
                            
                        
                        if p2[6]:
                            porcentaje=str(p2[6])+'&nbsp;'
                        
                        if p2[2]:
                            valor_iva=str(p2[2])+'&nbsp;'
                    else:
                        print("entro ret fue")
                        print p2[1]
                        print p2[2]
                        if p2[2]:
                            codigo_rf=str(p2[3])+' '
                        if p2[2]:
                            valor_rf=str(p2[2])+' '
                        
                            
                
                # html+='<td style="text-align:center">'+str(codigo_retencion)+'</td>'
                # html+='<td style="text-align:center">'+str(codigo_rf)+'</td>'
                # html+='<td style="text-align:center">'+str(valor_rf)+'</td>'
                # html+='<td style="text-align:center">'+str(porcentaje)+'</td>'
                # html+='<td style="text-align:center">'+str(valor_iva)+'</td>'
                
                retdetalle = DocumentosRetencionDetalleCompra.objects.filter(documento_retencion_compra_id=str(p[26])).aggregate(Sum('valor_retenido'))

               
                if retdetalle['valor_retenido__sum']:
                    ret_val=retdetalle['valor_retenido__sum']
                    #html += '<td>'+str(retdetalle['valor_retenido__sum'])+'</td>'
                
                    
                
            else:
                print 'no entro'
                # html += '<td></td>'
                # html += '<td></td>'
                # html += '<td></td>'
                # html += '<td></td>'
                # html += '<td></td>'
            
       

            total=totalf-ret_val
            html += '<td style="text-align:center"><b>' +str("%2.2f" % total).replace('.', ',') + '</b></td>'
            html+='<td></td>'
            html+='<td></td>'
            
            html += '<td><b>' + str(p[5].encode('utf8')) + '</b></td>'
            if p[30]==True:
                estado='ANULADO'
            else:
                estado='ACTIVO'
            html += '<td><b>' + str(estado) + '</b></td>'

            
            

                
             
            html += '</tr>'
            if p[31]:
                cursor = connection.cursor();
                sql3="select da.abono,da.activo,da.anulado,da.observacion,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion from documento_abono da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where  da.anulado is not True and da.documento_compra_id=" + str(p[31])
                print sql3
                cursor.execute(sql3);
                row3 = cursor.fetchall()
                saldo=0
                for p3 in row3:
                    html += '<tr>'
                    html += '<td>'+str(p3[13])+'</td>'
                    if p3[6]:
                        html += '<td>'+str(p3[6])+'</td>'
                    else:
                        html += '<td></td>'
                    html += '<td>'+str(p3[4])+'</td>'
                    #html += '<td></td>'
                    #html += '<td>'+str(p3[13])+'</td>'
                    html += '<td>'+str(factura)+'</td>'
                    #html += '<td></td>'
                    html += '<td></td>'
                    html += '<td></td>'
                    #credito
                    html += '<td>'+str("%2.2f" % p3[0]).replace('.', ',')+'</td>'
                    total_a=0
                    
                    if p[11]==False:
                        html += '<td></td>'
                        estadof='ANULADO'
                        
                    else:                        
                        saldo=saldo+p3[0]
                        total_a=float(total)-float(saldo)
                        html += '<td>'+str("%2.2f" % total_a).replace('.', ',')+'</td>'
                        estadof='ACTIVO'
                        
                        
                    
                    
                    if p3[8]:
                        html += '<td>'+str(p3[8].encode('utf8'))+'</td>'
                    else:
                        html += '<td></td>'
                    html += '<td>'+str(estadof)+'</td>'
                    html += '</tr>'
                    
                    print 'hrl'
             
            
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


#REPORTE DE FACTURA VS PROFORMA

def reporteProformavsFactura(request):
    return render_to_response('transacciones/facturas_vs_proforma_cliente.html', {}, RequestContext(request))

@csrf_exempt
def obtenerProformavsFactura(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')

        cursor = connection.cursor();
        cursor.execute(" select pr.fecha,pr.id,pr.codigo,pr.abreviatura_codigo,p.nombre,c.nombre_cliente,pr.descripcion,v.nombre,pr.tiempo_respuesta,pr.aprobada,pr.anulada,pr.observacion,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial from proforma pr LEFT JOIN vendedor v ON v.id=pr.vendedor_id LEFT JOIN puntos_venta p ON p.id=pr.puntos_venta_id LEFT JOIN cliente c ON c.id_cliente=pr.cliente_id LEFT JOIN documento_venta dv ON dv.proforma_id=pr.id  where pr.fecha>='" + fechainicial + "'and pr.fecha<='" + fechafin + "'");
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info">'
        html+='<thead>'
        html+='<tr><td colspan="10" style="text-align:center"><b>REPORTE DE PROFORMAS VS FACTURAS</td></tr><tr><td colspan="3"><b>DESDE</b></td><td colspan="2">'+str(fechainicial)+'</td><td colspan="3"><b>HASTA</b></td><td colspan="2">'+str(fechafin)+'</td></tr>'
        
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        html+= '<tr><th style="width:120px !important">Codigo</th>'
        html+= '<th style="width:120px !important">Fecha</th>'
        html+= '<th style="width:120px !important">Punto Venta</th>'
        html+= '<th style="width:150px !important">Cliente</th>'
        html+= '<th>Observacion</th>'
        html+= '<th>Vendedor</th>'
        html+= '<th>Tiempo Respuesta</th>'
        html+= '<th>Estado</th>'
        ##html+='<th>Proveedor</th>'
        ##html+='<th>Forma de Pago</th>'
        html+='<th>Fecha de Factura</th>'
        html+='<th>Factura</th>'
        

        # html+='<th>Codigo del establecimiento</th>'
        # html+='<th>Punto Emision</th><th>Secuencial</th>'
        ##html+='<th>No. Autorizacion</th>'
        # html += '<th>Base 0%</th><th>Base no sujeto a IVA</th><th>RISE</th>'
        # html += '<th>Base IVA 14%</th><th>IVA 14%</th>'
        # html+='<th>Codigo Ret. IVA</th><th>Codigo Ret Fuent.</th><th>Valor ret. imp. Renta'
        # html+='</th><th>%Retenc. IVA</th><th>Valor Retencion iva</th><th>No. Retencion</th><th>No. Autoriz. Retencion</th>'
        html+='</tr></thead>'
        html+='<tbody><tr>'
        
        for p in row:
            if p[2]:
                html += '<td style="text-align:center">'+ str(p[3]) +'-' + str(p[2]) +'</td>'
            else:
                html += '<td></td>'
                
            # if p[25]:
            #     html += '<td style="text-align:center">' + str(p[25].encode('utf8')) +'</td>'
            # else:
            #     html += '<td></td>'
            #     
            # if p[24]:
            #     html += '<td style="text-align:center">' + str(p[24])+''+ '</td>'
            # else:
            #     html += '<td></td>'
                
            html += '<td>' + str(p[0]) + '</td>'
            if p[4]:
                html += '<td>' + str(p[4].encode('utf8')) + '</td>'
            else:
                 html += '<td></td>'
                 
            if p[5]:
                html += '<td>' + str(p[5].encode('utf8')) + '</td>'
            else:
                 html += '<td></td>'
                 
            if p[11]:
                html += '<td>' + str(p[11].encode('utf8')) + '</td>'
            else:
                 html += '<td></td>'
                 
            if p[7]:
                html += '<td>' + str(p[7].encode('utf8')) + '</td>'
            else:
                 html += '<td></td>'
            html += '<td>' + str(p[8]) + '</td>'
            if p[10]==True:
                estadof='ANULADO'
            else:
                if p[9]==True:
                    estadof='APROBADA'
                else:
                    
                    estadof='ESPERANDO APROBACION'

            html += '<td>' + str(estadof) + '</td>'
            factura=''
            if p[13]:
                #html += '<td style="text-align:center">' + str(p[1]) + '</td>'
                factura+=''+str(p[13]) +'-'
            else:
                factura+='-'
                #html += '<td></td>'
            
            if p[14]:
                #html += '<td style="text-align:center">' + str(p[2]) + '</td>'
                factura+=''+str(p[14]) +'-'
            else:
                #html += '<td></td>'
                factura+='-'
            
            if p[15]:
                #html += '<td style="text-align:center">' + str(p[3]) + '</td
                factura+=''+str(p[15]) 
            else:
                #html += '<td></td>'
                factura+=''
            if p[12]:
                html += '<td style="text-align:center">' + str(p[12]) + '</td>'
            else:
                html += '<td></td>'
            
            html += '<td style="text-align:center">' + str(factura) + '</td>'
            html += '</tr>'
                    
             
            
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


#REPORTE DE FACTURAS PAGADAS ABONADAS

def reporteFacturasPagadasAbonadas(request):
    return render_to_response('transacciones/facturas_pagadas_abonadas.html', {}, RequestContext(request))

@csrf_exempt
def obtenerFacturasPagadasAbonadas(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')

        cursor = connection.cursor();
        total_deuda=0
        total_abonada=0
        total_disminuido=0
        total_retencion=0
        subtotal=0
        
        cursor.execute("select distinct dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.total,dv.cliente_id,dv.razon_social_id,c.nombre_cliente,r.nombre,c.codigo_cliente,dv.id,dv.activo,dv.proforma_id from documento_venta dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id LEFT JOIN razon_social r ON r.id=dv.razon_social_id where dv.fecha_emision>='" + fechainicial + "'and dv.fecha_emision<='" + fechafin + "'");
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        
        html= '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info">'
        html+='<thead>'
        html+='<tr><td colspan="10" style="text-align:center"><b>REPORTE DE FACTURAS PAGADAS, ABONADAS Y POR CANCELAR</b></td></tr><tr><td colspan="3"><b>DESDE</b></td><td colspan="2">'+str(fechainicial)+'</td><td colspan="3"><b>HASTA</b></td><td colspan="2">'+str(fechafin)+'</td></tr>'
        html+='<tr>'
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        html+= '<th style="width:120px !important">Factura</th>'
        html+= '<th style="width:120px !important">Fecha</th>'
        html+= '<th style="width:100px !important">Cliente</th>'
        html+= '<th style="width:150px !important">Nombre</th>'
        html+= '<th>Valor</th>'
        html+= '<th>Retencion</th>'
        html+= '<th>Valor a recibir</th>'
        html+= '<th>Abono</th>'
        html+= '<th>Saldo</th>'
        html+= '<th>Descripcion</th>'
        ##html+='<th>Proveedor</th>'
        ##html+='<th>Forma de Pago</th>'
       
        
        html+='</tr></thead>'
        html+='<tbody><tr>'
        total_factura_proforma=0
        for p in row:
            factura=''
            total_menos_retencion=0
            if p[1]:
                #html += '<td style="text-align:center">' + str(p[1]) + '</td>'
                factura+=''+str(p[1]) +'-'
            else:
                factura+='-'
                #html += '<td></td>'
            
            if p[2]:
                #html += '<td style="text-align:center">' + str(p[2]) + '</td>'
                factura+=''+str(p[2]) +'-'
            else:
                #html += '<td></td>'
                factura+='-'
            
            if p[3]:
                #html += '<td style="text-align:center">' + str(p[3]) + '</td
                factura+=''+str(p[3]) 
            else:
                #html += '<td></td>'
                factura+=''
            
            html += '<td style="text-align:center">' + str(factura) + '</td>'
            html += '<td style="text-align:center">' + str(p[0]) + '</td>'
            if p[11]!='' and p[11]!='NoneType':
                html += '<td>' + str(p[11].encode('utf8')) + '</td>'
            else:
                html += '<td></td>'
            if p[9]!='' and p[9]!='NoneType':
                html += '<td>' + str(p[9].encode('utf8')) + '</td>'
            else:
                html += '<td></td>'
                
            if p[13]:
                if p[6]:
                    html += '<td style="text-align:right">'+ str("%2.2f" % p[6]).replace('.', ',') +'</td>'
                    total=float(p[6])
                    total_deuda=total
                    total_factura_proforma=total_factura_proforma+total
                else:
                    total=0
                    html += '<td style="text-align:right">0,00</td>'
                retencion=0
                if p[12]:
                    cursor = connection.cursor();
                    sql="select sum(drdv.valor_retenido),count(drv.id) from documento_retencion_venta drv,documento_retencion_detalle_venta drdv where drv.id=drdv.documento_retencion_venta_id and drv.anulado is not True and drv.documento_venta_id=" + str(p[12])
                    print sql
                    cursor.execute(sql);
                    rowr2 = cursor.fetchall()
                    retencion=0
                    for pr2 in rowr2:
                        
                        if pr2[0]:
                            retencion_a=pr2[0]
                        else:
                            retencion_a=0
                        html+='<td style="text-align:right">'+str("%2.2f" % retencion_a).replace('.', ',')+'</td>'
                        retencion=retencion+retencion_a
                        total_retencion=total_retencion+retencion
                    
                total_menos_retencion=float(total)-float(retencion)
                subtotal=subtotal+total_menos_retencion
                html += '<td style="text-align:right">'+ str("%2.2f" % total_menos_retencion).replace('.', ',') +'</td>'
                
                #html += '<td>'+str(retdetalle['valor_retenido__sum'])+'</td>'
                
                    
                
                if p[12]:
                    cursor = connection.cursor();
                    sql="select sum(dav.abono) from documento_abono_venta dav where dav.anulado is not True and dav.documento_venta_id=" + str(p[12])
                    if p[14]:
                        sql+="or dav.proforma_id="+ str(p[14])
                    print sql
                    cursor.execute(sql);
                    row2 = cursor.fetchall()
                    for p2 in row2:
                        if p2[0]:
                            abono=float(p2[0])
                            html += '<td style="text-align:right">'+ str("%2.2f" % p2[0]).replace('.', ',') +'</td>'
                        else:
                            abono=0
                            html += '<td style="text-align:right">0,00</td>'
                        totalf=total_menos_retencion-abono
                        total_abonada=total_abonada+abono
                        total_disminuido=total_disminuido+totalf
                        
                        html += '<td style="text-align:right">'+ str("%2.2f" % totalf).replace('.', ',') +'</td>'
                        
        
            else:
                html += '<td style="text-align:right">0,00</td>'
                html += '<td style="text-align:right">0,00</td>'
                html += '<td style="text-align:right">0,00</td>'
                html += '<td style="text-align:right">0,00</td>'
                html += '<td style="text-align:right">0,00</td>'
                
            if p[5] is None:
                html += '<td></td>'
                
            else:
                html += '<td>' + str(p[5].encode('utf8')) + '</td>'
                
            
            html += '</tr>'
                    
             
            
        cursor.execute("select distinct dv.fecha,dv.abreviatura_codigo,dv.codigo,dv.codigo,dv.vendedor_id,dv.descripcion,dv.total,dv.cliente_id,dv.puntos_venta_id,c.nombre_cliente,c.nombre_cliente,c.codigo_cliente,dv.id from proforma dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id where dv.fecha>='" + fechainicial + "'and dv.fecha<='" + fechafin + "' and dv.id NOT IN (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL) and dv.aprobada is True");
        row21 = cursor.fetchall();
        for p21 in row21:
            proforma=''
            if p21[1]:
                #html += '<td style="text-align:center">' + str(p[1]) + '</td>'
                proforma+=''+str(p21[1]) +'-'
            else:
                proforma+='-'
                #html += '<td></td>'
            
            if p21[2]:
                #html += '<td style="text-align:center">' + str(p[2]) + '</td>'
                proforma+=''+str(p21[2]) +'-'
            else:
                #html += '<td></td>'
                proforma+=''
            
            
            
            html += '<td style="text-align:center">' + str(proforma) + '</td>'
            html += '<td style="text-align:center">' + str(p21[0]) + '</td>'
            if p21[11] is None:
                html += '<td></td>'
            else:
                html += '<td>' + str(p21[11].encode('utf8')) + '</td>'
                
            
            if p21[9] is None:
                html += '<td></td>'
                
            else:
                html += '<td>' + str(p21[9].encode('utf8')) + '</td>'
                
            
            if p21[6]:
                html += '<td style="text-align:right">'+ str("%2.2f" % p21[6]).replace('.', ',') +'</td>'
                totalp=float(p21[6])
                total_deuda=totalp
                total_factura_proforma=total_factura_proforma+totalp
            else:
                totalp=0
                html += '<td style="text-align:right">0,00</td>'
                
            
            html += '<td style="text-align:right">0,00</td>'
            html += '<td style="text-align:right">'+ str("%2.2f" % totalp).replace('.', ',') +'</td>'
            if p21[12]:
                cursor = connection.cursor();
                sql="select sum(dav.abono) from documento_abono_venta dav where dav.anulado is not True and dav.proforma_id=" + str(p21[12])
                print sql
                cursor.execute(sql);
                row22 = cursor.fetchall()
                for p22 in row22:
                    if p22[0]:
                        abono=float(p22[0])
                        html += '<td style="text-align:right">'+ str("%2.2f" %  p22[0]).replace('.', ',') +'</td>'
                    else:
                        abono=0
                        html += '<td style="text-align:right">0,00</td>'
                    totalp=totalp-abono
                    total_abonada=total_abonada+abono
                    total_disminuido=total_disminuido+totalp
                    html += '<td style="text-align:right">'+ str("%2.2f" %  totalp).replace('.', ',') +'</td>'
                    
                    
            if p21[5] is None:
                html += '<td></td>'
            else:
                
                html += '<td>' + str(p21[5].encode('utf8')) + '</td>'
            
            html += '</tr>'
                    
        
        total_menos_r=total_factura_proforma-total_retencion
        html+='</tbody>'
        html+='<tfoot><tr><td></td><td></td> <td></td><td></td><td style="text-align:right">'+str("%2.2f" %  total_factura_proforma).replace('.', ',')+'</td><td style="text-align:right">'+str("%2.2f" % total_retencion).replace('.', ',')+'</td><td style="text-align:right">'+str("%2.2f" %  total_menos_r).replace('.', ',')+'</td><td style="text-align:right">'+str("%2.2f" %  total_abonada).replace('.', ',')+'</td><td style="text-align:right">'+str("%2.2f" %  total_disminuido).replace('.', ',')+'</td><td></td></tr><tfoot>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404



#REPORTE DE TARJETA DE CREDITO

def reporteMovimientoTarjetaCredito(request):
    return render_to_response('transacciones/tarjeta_credito.html', {}, RequestContext(request))

@csrf_exempt
def obtenerMovimientosTarjetaCredito(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')

        cursor = connection.cursor();
        
        cursor.execute("select distinct a.asiento_id,a.codigo_asiento,a.fecha,ad.cuenta_id,ad.debe,ad.haber,ad.concepto,ad.centro_costo_id,m.id,m.numero_comprobante,t.nombre,m.numero_ingreso,tp.descripcion,cp.codigo_plan,cp.nombre_plan from contabilidad_asiento a LEFT JOIN contabilidad_asientodetalle ad ON ad.asiento_id=a.asiento_id LEFT JOIN movimiento m ON m.asiento_id=a.asiento_id LEFT JOIN tipo_documento tp ON tp.id=m.tipo_documento_id LEFT JOIN tarjeta_credito t ON t.id=m.tarjeta_credito_id  LEFT JOIN contabilidad_plandecuentas cp ON cp.plan_id=ad.cuenta_id where ad.cuenta_id=609 and a.fecha>='" + fechainicial + "'and a.fecha<='" + fechafin + "'");
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead>'
        html+='<tr><td colspan="10" style="text-align:center"><b>REPORTE DE TARJETA DE CREDITO</td></tr><tr><td colspan="3"><b>DESDE</b></td><td colspan="2">'+str(fechainicial)+'</td><td colspan="3"><b>HASTA</b></td><td colspan="2">'+str(fechafin)+'</td></tr>'
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        html+= '<tr><th style="width:120px !important">Tipo</th>'
        html+= '<th style="width:120px !important">Numero</th>'
        html+= '<th style="width:120px !important">Fecha</th>'
        html+= '<th style="width:100px !important">Debito</th>'
        html+= '<th style="width:150px !important">Credito</th>'
        
        html+= '<th>Saldo</th>'
        html+= '<th>Concepto</th>'
        html+= '<th>Cuenta</th>'
        html+= '<th>Nombre</th>'
        html+= '<th>Tarjeta de Cred.</th>'
        
        ##html+='<th>Proveedor</th>'
        ##html+='<th>Forma de Pago</th>'
       
        
        html+='</tr></thead>'
        html+='<tbody><tr>'
        
        for p in row:
           
               
           
            html += '<td>' + str(p[12].encode('utf8')) + '</td>'
            html += '<td>' + str(p[11].encode('utf8')) + '</td>'
            total=0
            if p[2]:
                html += '<td style="text-align:center">'+ str(p[2]) +'</td>'
            else:
                html += '<td></td>'
            
            if p[4]:
                html += '<td style="text-align:center">'+ str(p[4]) +'</td>'
                total=total+p[4]
            else:
                html += '<td></td>'
            
            if p[5]:
                html += '<td style="text-align:center">'+ str(p[5]) +'</td>'
                total=total-p[5]
            else:
                html += '<td></td>'
                
                
            html += '<td style="text-align:center">'+ str(total) +'</td>'
            html += '<td>' + str(p[6].encode('utf8')) + '</td>'
            html += '<td>' + str(p[13].encode('utf8')) + '</td>'
            html += '<td>' + str(p[14].encode('utf8')) + '</td>'
            html += '<td>' + str(p[10].encode('utf8')) + '</td>'
           
            html += '</tr>'
                    
             
            
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reportePorEstadoCuentaFacturasClientes(request):
    cliente = Cliente.objects.all().order_by('codigo_cliente')

    return render_to_response('transacciones/estado_cuenta_facturas_clientes.html', {'cliente': cliente}, RequestContext(request))


@csrf_exempt
def obtenerEstadoCuentaFacturasClientes(request):
    if request.method == 'POST':
        fechaini = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')

        cliente_ini = request.POST.get('cliente')
        cliente_fin = request.POST.get('cliente_hasta')

        cliente_s=Cliente.objects.get(id_cliente=cliente_ini)
        if cliente_s:
            nombre_cliente=cliente_s.codigo_cliente+' -'+cliente_s.nombre_cliente
            codigo_cliente=cliente_s.codigo_cliente
        else:
            nombre_cliente=''
        
        cliente_h=Cliente.objects.get(id_cliente=cliente_fin)
        if cliente_h:
            nombre_cliente_h=cliente_h.codigo_cliente+' -'+cliente_h.nombre_cliente
            codigo_cliente_h=cliente_h.codigo_cliente
        else:
            nombre_cliente_h=''

        cursor = connection.cursor()

        total_debito=0
        total_credito=0
        total_saldo_acum=0
        subtotal = 0
        iva = 0
        total_saldo=0
        total = 0

        # border="0" style="width:100%"
        html = '<table id="tabla" class="table table-bordered " aria-describedby="data-table_info">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="8" style="text-align:center"><b>ESTADO DE CUENTA DEL CLIENTE <br> DESDE '+str(nombre_cliente.encode('utf8'))+'    HASTA '+str(nombre_cliente_h.encode('utf8'))+'</b></td></tr>'
        html+='<tr><td colspan="1"><b>DESDE:</b></td><td colspan="1">'+str(fechaini)+'</td><td colspan="1"><b>HASTA:</b></td><td colspan="1">'+str(fechafin)+'</td><td colspan="4"></td></tr>'
        html+='</thead>'
        html+='<tbody>'

        cursor.execute('select id_cliente,codigo_cliente,nombre_cliente from cliente '
            ' where codigo_cliente::int>=%s '
            ' and  codigo_cliente::int<=%s '
            ' order by codigo_cliente ', (int(codigo_cliente),int(codigo_cliente_h)))

        rowc = cursor.fetchall();
        total_a=0
        total_ap=0
        for pc in rowc:
            PagosmId = ''
            DeudaTot = 0
            PagosTot = 0
            SaldoTot = 0
            PagoParc = 0

            total_cuenta=0
            total_factura=0
            total_proforma=0
            total_cheque=0
            total_chequepro=0
            total_saldo=0
            total_saldo_por_cuenta=0

            cliente=pc[0]
            
            #Facturas
            lcSql = "SELECT  distinct dv.id,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0, "
            lcSql += "dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,drv.establecimiento,drv.punto_emision, "
            lcSql += "drv.secuencial,drv.autorizacion,c.codigo_cliente,c.ruc,drv.id,dv.activo,dv.proforma_id "
            lcSql += "FROM documento_venta dv "
            lcSql += "LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
            lcSql += "LEFT JOIN documento_retencion_venta drv ON drv.documento_venta_id=dv.id  and drv.anulado is not True "
            lcSql += "where dv.activo is not False and dv.fecha_emision>='" + fechaini + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id="+str(cliente)
            lcSql += " order by dv.fecha_emision"

            cursor1 = connection.cursor()
            cursor1.execute(lcSql);
            row = cursor1.fetchall();
            
            #Proformas
            cursor2 = connection.cursor()
            sql2 = "SELECT  distinct dv.id,dv.fecha,dv.abreviatura_codigo,dv.codigo,dv.puntos_venta_id,dv.vendedor_id,dv.observacion,dv.iva,dv.porcentaje_iva,dv.subtotal,"
            sql2 += "dv.descuento,dv.total,c.nombre_cliente,c.codigo_cliente,c.ruc,dv.aprobada "
            sql2 += "FROM proforma dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
            sql2 += "LEFT JOIN documento_abono_venta da ON da.proforma_id = dv.id "
            sql2 += "LEFT JOIN movimiento m ON m.id=da.movimiento_id "
            sql2 += "where dv.fecha>='" + fechaini + "' and dv.fecha<='" + fechafin + "' and dv.id "
            sql2 += "NOT IN (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL and d.cliente_id=" + str(cliente) + ") "
            sql2 += "and dv.aprobada is True and dv.cliente_id=" + str(cliente)
            cursor2.execute(sql2)
            row21 = cursor2.fetchall()
            
            #PROFORMAS QUE FUERON ABONADAS ANTES DE CONVERTIRSE EN FACTURA
            cursor22 = connection.cursor()
            sql22 = "SELECT  distinct dv.id,dv.fecha,dv.abreviatura_codigo,dv.codigo,dv.puntos_venta_id,dv.vendedor_id,dv.observacion,dv.iva,dv.porcentaje_iva, "
            sql22 += "dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,c.codigo_cliente,c.ruc,dv.aprobada "
            sql22 += "FROM proforma dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
            sql22 += "where dv.fecha>='" + fechaini + "' and dv.fecha<='" + fechafin + "' and dv.id IN ("
            sql22 += "select da.proforma_id from documento_abono_venta da where da.anulado is not True and da.documento_venta_id is null) "
            sql22 += "and dv.id IN (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL and d.cliente_id ="+str(cliente) + ") "
            sql22 += "and dv.aprobada is True and dv.cliente_id="+str(cliente)
            cursor22.execute(sql22)

            row22 = cursor22.fetchall()
            
            #SQL CHEQUES PROTESTADOS
            
            cursor3 = connection.cursor()
            sql5 = "select distinct cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante "
            sql5 += "from cheques_protestados cp,movimiento m,documento_abono_venta da,documento_venta dv "
            sql5 += "where cp.anulado is not True and m.id=cp.movimiento_id and da.movimiento_id=m.id and da.documento_venta_id=dv.id and cp.fecha_emision>='" + fechaini + "' and cp.fecha_emision<='" + fechafin + "' and dv.cliente_id="+str(cliente)
            #print sql5
            cursor3.execute(sql5);
            chequesp = cursor3.fetchall()
            
            cursor4 = connection.cursor()
            sql6 = "select distinct cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante "
            sql6 += "from cheques_protestados cp,movimiento m,documento_abono_venta da,proforma dv "
            sql6 += "where cp.anulado is not True and m.id=cp.movimiento_id and da.movimiento_id=m.id and da.proforma_id=dv.id and da.documento_venta_id is null and dv.fecha>='" + fechaini + "' and dv.fecha<='" + fechafin + "' and dv.cliente_id="+str(cliente)
            #print sql6
            cursor4.execute(sql6);
            chequespr = cursor4.fetchall()

            if len(row)>0 or len(row21)>0  or len(chequesp)>0  or len(chequespr)>0 :
                html+='<tr style="background-color: #EBF5FB"><td colspan="8"><h5><b>'+str(pc[1])+'-'+str(pc[2].encode('utf8'))+'</b></h5></td></tr>'
                html+='<tr style="background-color: #EEEEEE"><th>Tipo</th>'
                html+='<th style="width:150px ;">Numero Doc</th>'
                html+='<th style="width:150px ;">Fecha Trx</th>'
                html+='<th>Debito</th><th>Credito</th><th>Saldo</th><th>Saldo Cuenta</th><th>Concepto</th></tr>'
                
            for p in row:
                html+='<tr>'
                html += '<td><b>&nbsp;Facturas</b></td>'

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
                html += '<td >' + str(factura) + '</td>'
    
                if p[1]:
                    html += '<td style="text-align:center">' + str(p[1]) +'</td>'
                else:
                    html += '<td></td>'

                if p[14]:
                    totalf=p[14]
                else:
                    totalf=0
                
                total_debito=total_debito+totalf
                DeudaTot = float(DeudaTot) + float(totalf)
                SaldoTot = float(SaldoTot) + float(totalf)

                html += '<td style="text-align:right">' + str("%0.2f" % totalf).replace('.', ',')  + '</td>'
                html += '<td style="text-align:right">0,00</td>'
                html += '<td style="text-align:right">' + str("%0.2f" % totalf).replace('.', ',')  + '</td>'
                html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',')  + '</b></td>'
                html += '<td style="text-align:center">'+str(p[5].encode('utf8'))+'</td>'
                html += '</tr>'

                total_cuenta=float(total_cuenta)+totalf

                #RETENCIONES
                if p[0]:
                    saldo=0
                    cursor = connection.cursor()
                    lcSql = "select sum(drdv.valor_retenido),drv.id,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id  "
                    lcSql += "from documento_retencion_venta drv,documento_retencion_detalle_venta drdv "
                    lcSql += "where drv.id=drdv.documento_retencion_venta_id and drv.documento_venta_id="+ str(p[0])+" and drv.anulado is not True "
                    lcSql += " group by drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id"

                    #print lcSql
                    cursor.execute(lcSql);
                    rowr3 = cursor.fetchall()
                    retencion=0
                    retencion1=0
                    for pr2 in rowr3:
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
                        html += '<td><b>&nbsp;Retenciones</b></td>'
                        html+='<td style="text-align:left">'+str(retencion_cod)+'</td>'
                        html+='<td style="text-align:center">'+str(pr2[5])+'</td>'
                        html+='<td style="text-align:right">0,00</td>'
                        
                        if pr2[0]:
                            saldo=Decimal(saldo)+Decimal(pr2[0])
                            PagosTot = float(PagosTot) + float(pr2[0])
                            PagoParc = float(pr2[0])

                        SaldoTot = float(SaldoTot) - float(PagoParc)
                        total_a=float(totalf)-float(saldo)
                        total_credito=total_credito+float(pr2[0])
                        html+='<td style="text-align:right">'+str("%0.2f" % pr2[0]).replace('.', ',')+'</td>'
                        html+='<td style="text-align:right">'+str("%0.2f" % total_a).replace('.', ',') +'</td>'
                        html+='<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
                        html+='<td style="text-align:center">'+str(pr2[6].encode('utf8'))+'</td>'
                        html += '</tr>'
                        total_cuenta=float(total_cuenta)-float(pr2[0])

                    #Depositos - Pagos
                    cursor = connection.cursor();
                    lcSql = "select distinct da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id "
                    lcSql += "from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                    lcSql += "where da.anulado is not True and da.documento_venta_id="+ str(p[0])+" and m.fecha_emision>='" + fechaini + "' and m.fecha_emision<='" + fechafin + "' order by m.fecha_emision"
                    cursor.execute(lcSql);
                    row3 = cursor.fetchall()
                    
                    for p3 in row3:
                        if len(PagosmId)>0:
                            PagosmId += ',' + str(p3[14])
                        else:
                            PagosmId += str(p3[14])

                        html += '<tr>'
                        html += '<td><b>&nbsp;'+str(p3[13].encode('utf8'))+'<b></td>'
                        html += '<td>'+str(p3[9])+'</td>'
                        html += '<td style="text-align:center">'+str(p3[4])+'</td>'
                        html += '<td style="text-align:right">0,00</td>'

                        #credito
                        html += '<td style="text-align:right">'+str("%0.2f" % p3[0]).replace('.', ',')+'</td>'
                        total_a=0
                        
                        if p[11]==True:
                            html += '<td style="text-align:right">0,00</td>'
                            estadof='ANULADO'
                        else:                        
                            saldo=saldo+p3[0]
                            PagosTot = float(PagosTot) + float(p3[0])
                            PagoParc = float(p3[0])
                            total_a=float(totalf)-float(saldo)
                            html += '<td style="text-align:right">'+str("%0.2f" % total_a).replace('.', ',')+'</td>'
                            estadof='ACTIVO'
                            total_credito=total_credito+float(p3[0])
                            total_cuenta=float(total_cuenta)-float(p3[0])

                        SaldoTot = float(SaldoTot) - float(PagoParc)

                        html += '<td style="text-align:right"><b>'+str("%0.2f" % SaldoTot).replace('.', ',')+'</b></td>'
                        html += '<td style="text-align:center">'+str(p3[8].encode('utf8'))+'</td>'
                        html += '</tr>'

                    #NOTA DE CREDITO
                    cursor = connection.cursor();
                    lcSql = "select distinct da.total,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion "
                    lcSql +="from movimiento_nota_credito da "
                    lcSql +="LEFT JOIN movimiento m ON m.id=da.movimiento_id and m.activo is True LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.documento_venta_id="+ str(p[0])
                    lcSql +=" order by m.fecha_emision"

                    cursor.execute(lcSql);
                    row4 = cursor.fetchall()
                    for p4 in row4:
                        html += '<tr>'
                        html += '<td><b>'+str(p4[13].encode('utf8'))+'</b></td>'
                        html += '<td>'+str(p4[9])+'</td>'
                        html += '<td>'+str(p4[4])+'</td>'
                        #credito
                        html += '<td style="text-align:right">0,00</td>'
                        html += '<td style="text-align:right">'+str("%2.2f" % p4[0]).replace('.', ',')+'</td>'
                        
                        total_a=0
                            
                        if p[11]==True:
                            html += '<td></td>'
                            estadof='ANULADO'
                        else:                        
                            saldo=saldo+p4[0]
                            PagosTot = PagosTot + float(p4[0])
                            PagoParc = float(p4[0])
                            total_a=float(totalf)-float(saldo)
                            html += '<td style="text-align:right">'+str("%2.2f" % total_a).replace('.', ',')+'</td>'
                            estadof='ACTIVO'
                            total_credito=total_credito+float(p4[0])

                        SaldoTot = float(SaldoTot) - float(PagoParc)

                        html += '<td style="text-align:right"><b>'+str("%0.2f" % SaldoTot).replace('.', ',')+'</b></td>'
                        html += '<td style="text-align:center">'+str(p4[8].encode('utf8'))+'</td>'
                        html += '</tr>'

                    total_factura=float(total_factura)+ float(total_a)

            #PROFORMA

            for p21 in row21:
                proforma=''
                if p21[1]:
                    proforma+=''+str(p21[2]) +'-'
                else:
                    proforma+='-'

                if p21[2]:
                    proforma+=''+str(p21[3]) +'-'
                else:
                    proforma+='-'

                html+='<tr>'
                html += '<td style=""><b>&nbsp;Proformas</b></td>'
                html += '<td >' + str(proforma) + '</td>'
                html += '<td style="text-align:center">' + str(p21[1]) + '</td>'
                html += '<td style="text-align:right">' + str("%0.2f" % p21[11]).replace('.', ',')+ '</td>'
                html += '<td style="text-align:right">0,00</td>'

                if p21[11]:
                    totalp=float(p21[11])
                    #totalp = 0
                else:
                    totalp=0

                total_debito=total_debito+float(totalp)
                DeudaTot = float(DeudaTot) + float(totalp)
                SaldoTot = float(SaldoTot) + float(totalp)

                html += '<td style="text-align:right">' +str("%0.2f" % p21[11]).replace('.', ',')+ '</td>'
                html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
                html += '<td><b>' + str(p21[6].encode('utf8')) + '</b></td>'
                html += '</tr>'

                total_cuenta=float(total_cuenta)+float(totalp)

                if p21[0]:
                    cursor = connection.cursor();
                    lcSql = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id "
                    lcSql += "from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                    lcSql += "where da.anulado is not True and m.asociado_cheques_protestados is not True and da.proforma_id="+ str(p21[0])+" order by m.fecha_emision"

                    cursor.execute(lcSql);
                    row4 = cursor.fetchall()
                    saldop=0
                    for p4 in row4:
                        html += '<tr>'
                        html += '<td>&nbsp;<b>'+str(p4[13].encode('utf8'))+'</b></td>'
                        html += '<td>'+str(p4[9])+'</td>'
                        html += '<td style="text-align:center">'+str(p4[4])+'</td>'
                        html += '<td style="text-align:right">0,00</td>'
                        #credito
                        if p4[0]:
                            PagoParc = float(p4[0])
                            PagosTot = PagosTot + float(p4[0])

                        html += '<td style="text-align:right">'+str("%0.2f" % p4[0]).replace('.', ',')+'</td>'

                        SaldoTot = float(SaldoTot) - float(PagoParc)
                        total_ap = 0
                        saldop=saldop+p4[0]
                        total_ap=float(totalp)-float(saldop)
                        html += '<td style="text-align:right">'+str("%0.2f" % total_ap).replace('.', ',')+'</td>'
                        total_credito=total_credito+float(p4[0])
                        total_cuenta=float(total_cuenta)-float(p4[0])

                        html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
                        html += '<td>'+str(p4[8].encode('utf8'))+'</td>'
                        html += '</tr>'

                    total_proforma=float(total_proforma)+float(total_ap)


            #CHEQUES PROTESTADOS
            saldocp=0
            total_cp=0
            print 'cheques protestados'
            
            
            if chequesp:
                for chp in chequesp:
                
                    html += '<tr>'
                    html += '<td><b>&nbsp;CH. PROTESTADO No.'+str(chp[2])+'</b></td>'
                
                    html += '<td>'+str(chp[10])+'</td>'
                    html += '<td style="text-align:center">'+str(chp[1])+'</td>'
                    html += '<td style="text-align:right">'+str("%0.2f" % chp[4]).replace('.', ',')+'</td>'
                    #credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_a=0
                    
                    saldocp=Decimal(saldocp)+Decimal(chp[4])
                    total_cp=Decimal(total_cp)+Decimal(saldocp)
                    total_debito=float(total_debito)+float(chp[4])
                    html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                    html += '<td style="text-align:right">0,00</td>'
                    html += '<td style="text-align:center">'+str(chp[6].encode('utf8'))+'</td>'
                    html += '</tr>'
                    total_cuenta=float(total_cuenta)+float(chp[4])
                    
                    html += '<tr>'
                    html += '<td><b>&nbsp;CH. PROTESTADO  No.'+str(chp[2])+' MULTA</b></td>'
                    html += '<td>'+str(chp[10])+'</td>'
                    html += '<td style="text-align:center">'+str(chp[1])+'</td>'
                    html += '<td style="text-align:right">'+str("%0.2f" % chp[5]).replace('.', ',')+'</td>'
                    #credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_ac=0
                    
                    saldocp=Decimal(saldocp)+Decimal(chp[5])
                    total_cp=Decimal(total_cp)+Decimal(saldocp)
                    total_debito=float(total_debito)+float(chp[5])
                    html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                    html += '<td style="text-align:right">0,00</td>'
                    html += '<td style="text-align:center">'+str(chp[6].encode('utf8'))+'</td>'
                    html += '</tr>'
                    total_cuenta=float(total_cuenta)+float(chp[5])
                    
                    #Abono Cheques Protestados
                    cursor = connection.cursor();
                    sqlc3="select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_cheque da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.cheques_protestados_id="+ str(chp[0])+" order by m.fecha_emision"
                    print sqlc3
                    cursor.execute(sqlc3);
                    rowc3 = cursor.fetchall()
                    saldoabono=0
                    
                    for pc3 in rowc3:
                        html += '<tr>'
                        html += '<td>&nbsp;'+str(pc3[13].encode('utf8'))+'</td>'
                        html += '<td>'+str(pc3[9])+'</td>'
                        html += '<td style="text-align:center">'+str(pc3[4])+'</td>'
                        html += '<td></td>'
                        #credito
                        html += '<td style="text-align:right">'+str("%0.2f" % pc3[0]).replace('.', ',')+'</td>'
                        total_ch=0
                        
                        if pc3[1]==True:
                            html += '<td style="text-align:right">0,00</td>'
                            estadof='ANULADO'
                            
                        else:                        
                            saldoabono=saldoabono+pc3[0]
                            saldocp=float(saldocp)-float(saldoabono)
                            html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                            estadof='ACTIVO'
                            total_credito=total_credito+float(pc3[0])
                            total_cuenta=float(total_cuenta)-float(pc3[0])

                        html += '<td style="text-align:center">'+str(pc3[8].encode('utf8'))+'</td>'
                        
                        html += '</tr>'
                    
                total_cheque=float(total_cheque)+float(saldocp)

            #FINAL DE CHEQUES PROTESTADOS
            #CHEQUES PROTESTADOS proformaas

            if chequespr:
                for chpr in chequespr:
                
                    html += '<tr>'
                    html += '<td>&nbsp;CH. PROTESTADO  No.'+str(chpr[2])+'</td>'
                
                    html += '<td>'+str(chpr[10])+'</td>'
                    html += '<td style="text-align:center">'+str(chpr[1])+'</td>'
                    #html += '<td></td>'
                    html += '<td style="text-align:right">'+str("%0.2f" % chpr[4]).replace('.', ',')+'</td>'
                    #credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_a=0
                    
                    saldocp=Decimal(saldocp)+Decimal(chpr[4])
                    total_cp=Decimal(total_cp)+Decimal(saldocp)
                    total_debito=float(total_debito)+float(chpr[4])
                    html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                    html += '<td>'+str(chpr[6].encode('utf8'))+'</td>'
                    html += '</tr>'
                    total_cuenta=float(total_cuenta)+float(chpr[4])
                    html += '<tr>'
                    html += '<td>&nbsp;CH. PROTESTADO  No.'+str(chpr[2])+' MULTA</td>'
                    html += '<td>'+str(chpr[10])+'</td>'
                    html += '<td style="text-align:center">'+str(chpr[1])+'</td>'
                    html += '<td style="text-align:right">'+str("%0.2f" % chpr[5]).replace('.', ',')+'</td>'
                    #credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_ac=0
                    
                    saldocp=Decimal(saldocp)+Decimal(chpr[5])
                    total_cp=Decimal(total_cp)+Decimal(saldocp)
                    total_debito=float(total_debito)+float(chpr[5])
                    html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                    
                    html += '<td>'+str(chpr[6].encode('utf8'))+'</td>'
                    
                    html += '</tr>'
                    total_cuenta=float(total_cuenta)+float(chpr[5])
                    cursor = connection.cursor();

                    lcSql = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id "
                    lcSql += "from documento_abono_cheque da "
                    lcSql += "LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                    lcSql += "where da.anulado is not True and da.cheques_protestados_id="+ str(chpr[0])+" order by m.fecha_emision"

                    cursor.execute(lcSql);
                    rowc4 = cursor.fetchall()
                    saldoabono=0
                    
                    for pc3 in rowc4:
                        html += '<tr>'
                        html += '<td>&nbsp;'+str(pc3[13].encode('utf8'))+'</td>'
                        
                        html += '<td>'+str(pc3[9])+'</td>'
                        html += '<td style="text-align:center">'+str(pc3[4])+'</td>'
                        html += '<td></td>'
                        #credito
                        html += '<td style="text-align:right">'+str("%0.2f" % pc3[0]).replace('.', ',')+'</td>'
                        total_ch=0
                        
                        if pc3[1]==True:
                            html += '<td style="text-align:right">0,00</td>'
                            estadof='ANULADO'
                            
                        else:                        
                            saldoabono=saldoabono+pc3[0]
                            saldocp=float(saldocp)-float(saldoabono)
                            html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                            estadof='ACTIVO'
                            total_credito=total_credito+float(pc3[0])
                            total_cuenta=float(total_cuenta)-float(pc3[0])

                        html += '<td> style="text-align:center"'+str(pc3[8].encode('utf8'))+'</td>'
                        html += '</tr>'
                    
                    total_chequepro=float(total_chequepro)+float(saldocp)

            #Pagos realizados antes de generar facturas
            lcSql = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque, "
            lcSql += "m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id "
            lcSql += "from documento_abono_venta da "
            lcSql += "LEFT JOIN movimiento m ON m.id=da.movimiento_id "
            lcSql += "LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id "
            lcSql += "where da.documento_venta_id is not null and  da.anulado is not True and m.asociado_cheques_protestados is not True "
            lcSql += "and m.fecha_emision>='" + fechaini + "' and m.fecha_emision<='" + fechafin + "'"
            lcSql += "and m.cliente_id = " + str(cliente) + " "
            if len(PagosmId) > 0:
                lcSql += "and m.id not in (" + PagosmId + ") "
            lcSql += "order by m.fecha_emision"
            cursor.execute(lcSql);
            rowc5 = cursor.fetchall()

            for irow in rowc5:
                #pagoMov = 0
                if irow[0]:
                    #pagoMov += float(irow[11])
                    html += '<tr>'
                    html += '<td><b>&nbsp;' + str(irow[13].encode('utf8')) + '<b></td>'
                    html += '<td>' + str(irow[9]) + '</td>'
                    html += '<td style="text-align:center">' + str(irow[4]) + '</td>'
                    html += '<td style="text-align:right">0,00</td>'
                    # credito
                    html += '<td style="text-align:right">' + str("%0.2f" % irow[0]).replace('.', ',') + '</td>'
                    total_a = 0

                    if irow[1] == True:
                        html += '<td style="text-align:right">0,00</td>'
                        estadof = 'ANULADO'
                    else:
                        saldo=saldo+irow[0]
                        PagosTot = float(PagosTot) + float(irow[0])
                        PagoParc = float(irow[0])
                        total_a=float(totalf)-float(saldo)
                        html += '<td style="text-align:right">'+str("%0.2f" % total_a).replace('.', ',')+'</td>'
                        estadof='ACTIVO'
                        total_credito=total_credito+float(irow[0])
                        total_cuenta=float(total_cuenta)-float(irow[0])

                    SaldoTot = float(SaldoTot) - float(PagoParc)
                    html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
                    html += '<td style="text-align:center">' + str(irow[8].encode('utf8')) + '</td>'
                    html += '</tr>'

            #Pagos no relacionados
            lcSql = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque, "
            lcSql += "m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id "
            lcSql += "from documento_abono_venta da "
            lcSql += "LEFT JOIN movimiento m ON m.id=da.movimiento_id "
            lcSql += "LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id "
            lcSql += "where da.documento_venta_id is null and  da.anulado is not True and m.asociado_cheques_protestados is not True "
            lcSql += "and m.fecha_emision>='" + fechaini + "' and m.fecha_emision<='" + fechafin + "'"
            lcSql += "and m.cliente_id = " + str(cliente) + " "
            if len(PagosmId) > 0:
                lcSql += "and m.id not in (" + PagosmId + ") "
            lcSql += "order by m.fecha_emision"
            cursor.execute(lcSql);
            rowc6 = cursor.fetchall()

            for frow in rowc6:
                #pagoMov = 0
                if frow[0]:
                    #pagoMov += float(irow[11])
                    html += '<tr>'
                    html += '<td><b>&nbsp;' + str(frow[13].encode('utf8')) + '<b></td>'
                    html += '<td>' + str(frow[9]) + '</td>'
                    html += '<td style="text-align:center">' + str(frow[4]) + '</td>'
                    html += '<td style="text-align:right">0,00</td>'
                    # credito
                    html += '<td style="text-align:right">' + str("%0.2f" % frow[0]).replace('.', ',') + '</td>'
                    total_a = 0

                    if frow[1] == True:
                        html += '<td style="text-align:right">0,00</td>'
                        estadof = 'ANULADO'
                    else:
                        saldo=saldo+frow[0]
                        PagosTot = float(PagosTot) + float(frow[0])
                        PagoParc = float(frow[0])
                        total_a=float(totalf)-float(saldo)
                        html += '<td style="text-align:right">'+str("%0.2f" % total_a).replace('.', ',')+'</td>'
                        estadof='ACTIVO'
                        total_credito=total_credito+float(frow[0])
                        total_cuenta=float(total_cuenta)-float(frow[0])

                    SaldoTot = float(SaldoTot) - float(PagoParc)
                    html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
                    html += '<td style="text-align:center">' + str(frow[8].encode('utf8')) + '</td>'
                    html += '</tr>'


            #proformas hechas facturas abonos
            for p22 in row22:
                deudaprf = 0
                if p22[11]:
                    deudaprf = float(p22[11])
                proforma=''
                if p22[1]:
                    proforma+=''+str(p22[2]) +'-'
                else:
                    proforma+='-'

                if p22[2]:
                    proforma+=''+str(p22[3]) +'-'
                else:
                    proforma+='-'
                totalp=0

                if p22[0]:
                    cursor = connection.cursor();
                    sql41="select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.documento_venta_id is null and  da.anulado is not True and m.asociado_cheques_protestados is not True and da.proforma_id="+ str(p22[0])+" order by m.fecha_emision"

                    cursor.execute(sql41);
                    row41 = cursor.fetchall()
                    saldop=0
                    if row41:
                        html += '<tr><td colspan="8" style="background-color: #F1948A">Abonos a Proformas que se Convertiran en Diferentes Facturas [ANTICIPOS] Proforma: '+str(proforma)+' </td></tr>'
                        html += '<tr>'
                        html += '<td style=""><b>&nbsp;Proformas</b></td>'
                        html += '<td>' + proforma + '</td>'
                        html += '<td style="text-align:center">' + str(p22[1]) + '</td>'
                        html += '<td style="text-align:right">' + str("%0.2f" % deudaprf).replace('.', ',') + '</td>'
                        #credito
                        total_debito = float(total_debito) + float(deudaprf)
                        DeudaTot = float(DeudaTot) + float(deudaprf)
                        SaldoTot = float(SaldoTot) + float(deudaprf)
                        total_cuenta = float(total_cuenta) + float(deudaprf)

                        html += '<td style="text-align:right">0,00</td>'
                        html += '<td style="text-align:right">' + str("%0.2f" % deudaprf).replace('.', ',') + '</td>'
                        html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',',') + '</b></td>'
                        html += '<td></td>'
                        html += '</tr>'

                        for p4 in row41:
                            html += '<tr>'
                            html += '<td>&nbsp;<b>'+str(p4[13].encode('utf8'))+'</b></td>'
                            html += '<td>'+str(p4[9])+'</td>'
                            html += '<td style="text-align:center">'+str(p4[4])+'</td>'
                            html += '<td style="text-align:right">0,00</td>'
                            #credito
                            html += '<td style="text-align:right">'+str("%0.2f" % p4[0]).replace('.', ',')+'</td>'

                            if p4[0]:
                                PagoParc = float(p4[0])
                                PagosTot = PagosTot + float(p4[0])

                            #total_debito = total_debito + deudaprf

                            SaldoTot = float(SaldoTot) - float(PagoParc)
                            total_ap=0
                            saldop=saldop+p4[0]
                            total_ap=float(totalp)-float(saldop)

                            html += '<td style="text-align:right">'+str("%0.2f" % total_ap).replace('.', ',')+'</td>'
                            total_credito=total_credito+float(p4[0])
                            total_cuenta=float(total_cuenta)-float(p4[0])
                            html += '<td style="text-align:right"><b>'+str("%0.2f" % SaldoTot).replace('.', ',')+'</b></td>'
                            html += '<td>'+str(p4[8].encode('utf8'))+'</td>'
                            html += '</tr>'

                    total_proforma=float(total_proforma)+float(total_ap)
        
            if len(row)>0 or len(row21)>0  or len(chequesp)>0  or len(chequespr)>0 :
                total_saldo_por_cuenta=total_factura+total_proforma+total_cheque+total_chequepro    
                html+='<tr style="background-color: #EBF5FB"><td colspan="3"><b>Saldo Final Cuenta ' +str(nombre_cliente.encode('utf8')) +'</b></td><td style="text-align:right">'+str("%0.2f" % DeudaTot).replace('.', ',')+'</td><td style="text-align:right">'+str("%0.2f" % PagosTot).replace('.', ',')+'</td><td style="text-align:right">'+str("%0.2f" % total_cuenta).replace('.', ',')+'</td><td></td><td></td></tr>'

        #print 'hrl'
        total_saldo_acum=float(total_debito)-float(total_credito)

        html+='</tbody>'
        html+='<tfoot style="background-color: #EEEEEE"><tr><td colspan="3"><b>Saldos Totales Clientes:</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_debito).replace('.', ',')+'</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_credito).replace('.', ',')+'</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_saldo_acum).replace('.', ',')+'</b></td><td></td><td></td></tr></tfoot>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404

#------------------------------------------->

def reportePorEstadoCuentaClientesResumen(request):
    cliente = Cliente.objects.all().order_by('codigo_cliente')

    return render_to_response('transacciones/estado_cuenta_clientes_resumen.html', {'cliente': cliente}, RequestContext(request))


@csrf_exempt
def obtenerEstadoCuentaClientesResumen(request):
    if request.method == 'POST':
        fechaini = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')

        cliente_ini = request.POST.get('cliente')
        cliente_fin = request.POST.get('cliente_hasta')

        cliente_s = Cliente.objects.get(id_cliente=cliente_ini)
        if cliente_s:
            nombre_cliente = cliente_s.codigo_cliente + ' -' + cliente_s.nombre_cliente
            codigo_cliente = cliente_s.codigo_cliente
        else:
            nombre_cliente = ''

        cliente_h = Cliente.objects.get(id_cliente=cliente_fin)
        if cliente_h:
            nombre_cliente_h = cliente_h.codigo_cliente + ' -' + cliente_h.nombre_cliente
            codigo_cliente_h = cliente_h.codigo_cliente
        else:
            nombre_cliente_h = ''

        cursor = connection.cursor()

        total_debito = 0
        total_credito = 0
        total_saldo_acum = 0
        subtotal = 0
        iva = 0
        total_saldo = 0
        total = 0

        # border="0" style="width:100%"
        html = '<table id="tabla" class="table table-bordered " aria-describedby="data-table_info">'
        html += '<thead style="background-color: #EEEEEE">'
        html += '<tr><td colspan="8" style="text-align:center"><b>ESTADO DE CUENTA RESUMEN DE CLIENTES <br> DESDE ' + str(
            nombre_cliente.encode('utf8')) + '    HASTA ' + str(nombre_cliente_h.encode('utf8')) + '</b></td></tr>'
        html += '<tr><td colspan="1"><b>DESDE:</b></td><td colspan="1">' + str(
            fechaini) + '</td><td colspan="1"><b>HASTA:</b></td><td colspan="1">' + str(
            fechafin) + '</td><td colspan="4"></td></tr>'
        html += '<tr><td colspan="5" style="background-color: #EBF5FB"><h6><b>Cliente</b><h6></td>'
        html += '<td style="background-color: #EBF5FB; text-align:center"><h6><b>Débito</b><h6></td>'
        html += '<td style="background-color: #EBF5FB; text-align:center"><h6><b>Crédito</b><h6></td>'
        html += '<td style="background-color: #EBF5FB; text-align:center"><h6><b>Saldo</b><h6></td></tr>'
        html += '</thead>'
        html += '<tbody>'

        #style = "text-align:center"

        cursor.execute('select id_cliente,codigo_cliente,nombre_cliente from cliente '
                       ' where codigo_cliente::int>=%s '
                       ' and  codigo_cliente::int<=%s '
                       ' order by codigo_cliente ', (int(codigo_cliente), int(codigo_cliente_h)))

        rowc = cursor.fetchall();
        total_a = 0
        total_ap = 0
        for pc in rowc:
            oCodCliente = ''
            oNomCliente = ''
            PagosmId = ''
            DeudaTot = 0
            PagosTot = 0
            SaldoTot = 0
            PagoParc = 0
            PagoCruc = 0
            nRecord = 0
            total_cuenta = 0
            total_factura = 0
            total_proforma = 0
            total_cheque = 0
            total_chequepro = 0
            total_saldo = 0
            total_saldo_por_cuenta = 0
            cliente = pc[0]

            lcSql = "SELECT COUNT(*) Reg "
            lcSql += "FROM vw_transacciones "
            lcSql += "WHERE id_cliente = " + str(cliente)

            cursort = connection.cursor()
            cursort.execute(lcSql);
            reg = cursort.fetchall();

            if len(reg) > 0:
                for r in reg:
                    if r[0]:
                        nRecord = r[0]

            if (nRecord > 0):
                # Facturas
                lcSql = "SELECT " #distinct
                lcSql += "dv.id,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0, "
                lcSql += "dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente, "
                lcSql += "c.codigo_cliente,c.ruc " #,drv.id,dv.activo,dv.proforma_id "
                lcSql += "FROM documento_venta dv "
                lcSql += "LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
                lcSql += "where dv.fecha_emision>='" + fechaini + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id=" + str(cliente) + "and dv.activo is not False "

                cursor1 = connection.cursor()
                cursor1.execute(lcSql);
                row = cursor1.fetchall();

                # PROFORMAS QUE FUERON ABONADAS ANTES DE CONVERTIRSE EN FACTURA
                cursor22 = connection.cursor()
                sql22 = "SELECT  dv.id,dv.fecha,dv.abreviatura_codigo,dv.codigo,dv.puntos_venta_id,dv.vendedor_id,dv.observacion,dv.iva,dv.porcentaje_iva, "
                sql22 += "dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,c.codigo_cliente,c.ruc,dv.aprobada "
                sql22 += "FROM proforma dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
                sql22 += "where dv.fecha>='" + fechaini + "' and dv.fecha<='" + fechafin + "' and dv.id  IN ("
                sql22 += "select da.proforma_id from documento_abono_venta da where da.documento_venta_id is null and da.anulado is not True ) "
                sql22 += "and dv.id in (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL and d.cliente_id =" + str(cliente) + ") "
                sql22 += "and dv.aprobada is True and dv.cliente_id=" + str(cliente)
                cursor22.execute(sql22)
                row22 = cursor22.fetchall()

                # SQL CHEQUES PROTESTADOS
                # sql5 = "select cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante "
                # sql5 += "from cheques_protestados cp,movimiento m,documento_abono_venta da,documento_venta dv "
                # sql5 += "where cp.fecha_emision>='" + fechaini + "' and cp.fecha_emision<='" + fechafin + "' and "
                # sql5 += "cp.anulado is not True and m.id=cp.movimiento_id and da.movimiento_id=m.id and da.documento_venta_id=dv.id and dv.cliente_id=" + str(cliente)
                lcSql = "select cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante "
                lcSql += "from cheques_protestados cp "
                lcSql += "inner join movimiento m on (cp.movimiento_id = m.id) "
                lcSql += "inner join documento_abono_venta da on (da.movimiento_id=m.id) "
                lcSql += "inner join documento_venta dv on (da.documento_venta_id=dv.id) "
                lcSql += "where cp.fecha_emision>='" + fechaini + "' and cp.fecha_emision<='" + fechafin + "' and "
                lcSql += "dv.cliente_id=" +str(cliente) + " and cp.anulado is not True"

                cursor3 = connection.cursor()
                cursor3.execute(lcSql);
                chequesp = cursor3.fetchall()

                # sql6 = "select cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante "
                # sql6 += "from cheques_protestados cp,movimiento m,documento_abono_venta da,proforma dv "
                # sql6 += "where cp.anulado is not True and m.id=cp.movimiento_id and da.movimiento_id=m.id "
                # sql6 += "and da.proforma_id=dv.id and da.documento_venta_id is null and dv.fecha>='" + fechaini + "' and dv.fecha<='" + fechafin + "' and dv.cliente_id=" + str(cliente)
                lcSql = "select cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante "
                lcSql += "from cheques_protestados cp "
                lcSql += "inner join movimiento m on (cp.movimiento_id = m.id) "
                lcSql += "inner join documento_abono_venta da on (da.movimiento_id=m.id) "
                lcSql += "inner join proforma dv on (da.proforma_id=dv.id and dv.cliente_id= " + str(cliente) + " and dv.fecha>='" + fechaini + "' and dv.fecha<='" + fechafin + "') "
                lcSql += "where cp.anulado is not True and da.documento_venta_id is null "

                cursor4 = connection.cursor()
                cursor4.execute(lcSql);
                chequespr = cursor4.fetchall()

                if len(row) > 0 or len(chequesp) > 0 or len(chequespr) > 0:
                    oCodCliente = pc[1].encode('utf8')
                    oNomCliente = pc[2].encode('utf8')

                for p in row:
                    if p[14]:
                        totalf = p[14]
                    else:
                        totalf = 0

                    total_debito = total_debito + totalf
                    DeudaTot = float(DeudaTot) + float(totalf)
                    SaldoTot = float(SaldoTot) + float(totalf)
                    total_cuenta = float(total_cuenta) + totalf

                    # RETENCIONES
                    if p[0]:
                        saldo = 0
                        cursor = connection.cursor()
                        lcSql = "select sum(drdv.valor_retenido),drv.id,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id  "
                        lcSql += "from documento_retencion_venta drv,documento_retencion_detalle_venta drdv "
                        lcSql += "where drv.id=drdv.documento_retencion_venta_id and drv.documento_venta_id=" + str(p[0]) + " and drv.anulado is not True "
                        lcSql += " group by drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id"

                        cursor.execute(lcSql);
                        rowr3 = cursor.fetchall()
                        retencion = 0
                        retencion1 = 0
                        for pr2 in rowr3:
                            if pr2[0]:
                                saldo = Decimal(saldo) + Decimal(pr2[0])
                                PagosTot = float(PagosTot) + float(pr2[0])
                                PagoParc = float(pr2[0])

                            SaldoTot = float(SaldoTot) - float(PagoParc)
                            total_a = float(totalf) - float(saldo)
                            total_credito = total_credito + float(pr2[0])
                            total_cuenta = float(total_cuenta) - float(pr2[0])

                        # Depositos - Pagos
                        cursor = connection.cursor();
                        lcSql = "select da.abono,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,"
                        lcSql += "m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,m.id " #t.descripcion"
                        lcSql += "from documento_abono_venta da "
                        lcSql += "INNER JOIN movimiento m ON (m.id=da.movimiento_id and m.fecha_emision>='" + fechaini + "' and m.fecha_emision<='" + fechafin + "') "
                        #lcSql += "INNER JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                        lcSql += "where da.documento_venta_id = " + str(p[0]) + " and da.anulado is not True "

                        cursor.execute(lcSql);
                        row3 = cursor.fetchall()

                        for p3 in row3:
                            total_a = 0
                            if len(PagosmId)>0:
                                if p3[12] != 'None':
                                    PagosmId += ',' + str(p3[12])
                            else:
                                if p3[12] != 'None':
                                    PagosmId += str(p3[12])

                            if p[10] == True:
                                estadof = 'ANULADO'
                            else:
                                saldo = saldo + p3[0]
                                PagosTot = float(PagosTot) + float(p3[0])
                                PagoParc = float(p3[0])
                                total_a = float(totalf) - float(saldo)
                                estadof = 'ACTIVO'
                                total_credito = total_credito + float(p3[0])
                                total_cuenta = float(total_cuenta) - float(p3[0])

                            SaldoTot = float(SaldoTot) - float(PagoParc)

                        # NOTA DE CREDITO
                        #DISTINCT
                        cursor = connection.cursor();
                        lcSql = "select da.total,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,"
                        lcSql += "m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque " #t.descripcion "
                        lcSql += "from movimiento_nota_credito da "
                        lcSql += "LEFT JOIN movimiento m ON m.id=da.movimiento_id and m.activo is True "
                        #lcSql += "INNER JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                        lcSql += "WHERE da.documento_venta_id=" + str(p[0]) + " and da.anulado is not True "
                        #lcSql += " order by m.fecha_emision"

                        cursor.execute(lcSql);
                        row4 = cursor.fetchall()
                        for p4 in row4:
                            total_a = 0

                            if p[10] == True:
                                estadof = 'ANULADO'
                            else:
                                saldo = saldo + p4[0]
                                PagosTot = PagosTot + float(p4[0])
                                PagoParc = float(p4[0])
                                total_a = float(totalf) - float(saldo)
                                estadof = 'ACTIVO'
                                total_credito = total_credito + float(p4[0])

                            SaldoTot = float(SaldoTot) - float(PagoParc)

                        total_factura = float(total_factura) + float(total_a)

                # CHEQUES PROTESTADOS
                saldocp = 0
                total_cp = 0

                if chequesp:
                    for chp in chequesp:
                        total_a = 0
                        saldocp = Decimal(saldocp) + Decimal(chp[4])
                        total_cp = Decimal(total_cp) + Decimal(saldocp)
                        total_debito = float(total_debito) + float(chp[4])
                        total_cuenta = float(total_cuenta) + float(chp[4])
                        total_ac = 0
                        saldocp = Decimal(saldocp) + Decimal(chp[5])
                        total_cp = Decimal(total_cp) + Decimal(saldocp)
                        total_debito = float(total_debito) + float(chp[5])
                        total_cuenta = float(total_cuenta) + float(chp[5])

                        # Abono Cheques Protestados
                        cursor = connection.cursor();
                        sqlc3 = "select da.abono,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,"
                        sqlc3 += "m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,m.id " #t.descripcion,"
                        sqlc3 += "from documento_abono_cheque da "
                        sqlc3 += "LEFT JOIN movimiento m ON m.id=da.movimiento_id " #INNER JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                        sqlc3 += "where da.anulado is not True and da.cheques_protestados_id=" + str(chp[0])

                        cursor.execute(sqlc3);
                        rowc3 = cursor.fetchall()
                        saldoabono = 0

                        for pc3 in rowc3:
                            total_ch = 0

                            if pc3[1] == True:
                                #html += '<td style="text-align:right">0,00</td>'
                                estadof = 'ANULADO'
                            else:
                                saldoabono = saldoabono + pc3[0]
                                saldocp = float(saldocp) - float(saldoabono)
                                estadof = 'ACTIVO'
                                total_credito = total_credito + float(pc3[0])
                                total_cuenta = float(total_cuenta) - float(pc3[0])

                    total_cheque = float(total_cheque) + float(saldocp)

                # CHEQUES PROTESTADOS proformaas
                if chequespr:
                    for chpr in chequespr:
                        total_a = 0
                        saldocp = Decimal(saldocp) + Decimal(chpr[4])
                        total_cp = Decimal(total_cp) + Decimal(saldocp)
                        total_debito = float(total_debito) + float(chpr[4])
                        total_cuenta = float(total_cuenta) + float(chpr[4])
                        total_ac = 0
                        saldocp = Decimal(saldocp) + Decimal(chpr[5])
                        total_cp = Decimal(total_cp) + Decimal(saldocp)
                        total_debito = float(total_debito) + float(chpr[5])
                        total_cuenta = float(total_cuenta) + float(chpr[5])
                        cursor = connection.cursor();

                        lcSql = "select da.abono,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,"
                        lcSql += "m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,m.id " #t.descripcion,"
                        lcSql += "from documento_abono_cheque da "
                        lcSql += "LEFT JOIN movimiento m ON m.id=da.movimiento_id " #INNER JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                        lcSql += "where da.anulado is not True and da.cheques_protestados_id=" + str(chpr[0])

                        cursor.execute(lcSql);
                        rowc4 = cursor.fetchall()
                        saldoabono = 0

                        for pc3 in rowc4:
                            total_ch = 0
                            if pc3[1] == True:
                                estadof = 'ANULADO'
                            else:
                                saldoabono = saldoabono + pc3[0]
                                saldocp = float(saldocp) - float(saldoabono)
                                estadof = 'ACTIVO'
                                total_credito = total_credito + float(pc3[0])
                                total_cuenta = float(total_cuenta) - float(pc3[0])

                        total_chequepro = float(total_chequepro) + float(saldocp)

                # proformas hechas facturas abonos
                for p22 in row22:
                    deudaprf = 0
                    totalp = 0
                    if p22[11]:
                        deudaprf = float(p22[11])

                    if p22[0]:
                        cursor = connection.cursor();
                        sql41 = "select da.abono,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,"
                        sql41 += "m.monto,m.activo,m.monto_cheque,m.id " #t.descripcion,"
                        sql41 += "from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id " #LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                        sql41 += "where da.documento_venta_id is null and da.anulado is not True and m.asociado_cheques_protestados is not True and da.proforma_id=" + str(p22[0])
                        if len(PagosmId) > 0:
                            sql41 += " and m.id not in (" + PagosmId + ") "

                        cursor.execute(sql41);
                        row41 = cursor.fetchall()
                        saldop = 0
                        if row41:
                            for p4 in row41:
                                if p4[0]:
                                    PagoParc = float(p4[0])
                                    PagosTot = PagosTot + float(p4[0])

                                SaldoTot = float(SaldoTot) - float(PagoParc)
                                total_ap = 0
                                saldop = saldop + p4[0]
                                total_ap = float(totalp) - float(saldop)
                                total_credito = total_credito + float(p4[0])
                                total_cuenta = float(total_cuenta) - float(p4[0])

                        total_proforma = float(total_proforma) + float(total_ap)

                # Pagos hechos antes de emitir factura y cruzados posteriomente
                lcSql = "select da.abono,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque, "
                lcSql += "m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,m.id " #",t.descripcion"
                lcSql += "from documento_abono_venta da "
                lcSql += "LEFT JOIN movimiento m ON m.id=da.movimiento_id "
                #lcSql += "INNER JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                lcSql += "where da.documento_venta_id is not null and da.anulado is not True  "
                lcSql += "and m.fecha_emision>='" + fechaini + "' and m.fecha_emision<='" + fechafin + "' "
                lcSql += "and m.cliente_id = " + str(cliente) + " and m.asociado_cheques_protestados is not True "
                if len(PagosmId)>0:
                    lcSql += "and m.id not in (" + PagosmId + ") "

                cursor.execute(lcSql);
                rowc5 = cursor.fetchall()

                #Lista = "[" + PagosmId + "]"
                for irow in rowc5:
                    if irow[0]:
                        #idLista = str(irow[12])
                        #if idLista not in Lista:
                        PagosTot += float(irow[0])
                        total_credito += float(irow[0])
                        total_cuenta = total_cuenta - float(irow[0])

                if len(row) > 0 or len(chequesp) > 0 or len(chequespr) > 0:
                    total_saldo_por_cuenta = total_factura + total_proforma + total_cheque + total_chequepro
                    html += '<tr><td colspan="5"><b>' + str(oCodCliente.encode('utf8')) + '-' + oNomCliente + '</b></td>'
                    html += '<td style="text-align:right">' + str("%0.2f" % DeudaTot).replace('.', ',') + '</td>'
                    html += '<td style="text-align:right">' + str("%0.2f" % PagosTot).replace('.', ',') + '</td>'
                    html += '<td style="text-align:right">' + str("%0.2f" % total_cuenta).replace('.', ',') + '</td></tr>'

            total_saldo_acum = float(total_debito) - float(total_credito)

        html += '</tbody>'
        html += '<tfoot style="background-color: #EEEEEE"><tr><td colspan="5"><b>TOTALES : </b></td>'
        html += '<td style="text-align:right"><b>' + str("%0.2f" % total_debito).replace('.', ',') + '</b></td>'
        html += '<td style="text-align:right"><b>' + str("%0.2f" % total_credito).replace('.', ',') + '</b></td>'
        html += '<td style="text-align:right"><b>' + str("%0.2f" % total_saldo_acum).replace('.', ',') + '</b></td></tr></tfoot>'
        html += '</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


#------------------------------------------->

def reporteAnticiposClientesResumen(request):
    cliente = Cliente.objects.all().order_by('codigo_cliente')

    return render_to_response('transacciones/saldos_anticipos_cobrar.html', {'cliente': cliente}, RequestContext(request))

@csrf_exempt
def obtenerAnticiposClientesResumen(request):
    if request.method == 'POST':
        html=''
        return HttpResponse(
            html
        )
    else:
        raise Http404

#------------------------------------------>
#Nuevo Estado de Cuenta
def obtenerEstadoCuentaClientes(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cliente0 = request.POST.get('cliente')
        cliente_hasta0 = request.POST.get('cliente_hasta')
        cliente_s = Cliente.objects.get(id_cliente=cliente0)
        total_saldo_acum = 0
        if cliente_s:
            nombre_cliente = cliente_s.codigo_cliente + ' -' + cliente_s.nombre_cliente
            codigo_cliente = cliente_s.codigo_cliente
        else:
            nombre_cliente = ''

        cliente_h = Cliente.objects.get(id_cliente=cliente_hasta0)
        if cliente_h:
            nombre_cliente_h = cliente_h.codigo_cliente + ' -' + cliente_h.nombre_cliente
            codigo_cliente_h = cliente_h.codigo_cliente
        else:
            nombre_cliente_h = ''
        # qle="SELECT  distinct dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0,dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,c.codigo_cliente,c.ruc,drv.id,dv.activo,dv.cliente_id FROM documento_venta dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id LEFT JOIN documento_retencion_venta drv ON drv.documento_venta_id=dv.id  where dv.activo is not False and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id="+cliente
        # print qle

        cursor = connection.cursor()

        total = 0
        subtotal = 0
        iva = 0
        total_debito = 0
        total_credito = 0
        total_saldo = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="" border="0" style="width:100%"  aria-describedby="data-table_info">'
        html += '<thead style="border:1px solid black">'
        html += '<tr><td colspan="7" style="text-align:center"><b>REPORTE DE ESTADO DE CUENTA DEL CLIENTE <br > DESDE ' + str(
            nombre_cliente.encode('utf8')) + '    HASTA ' + str(nombre_cliente_h.encode('utf8')) + '</b></td></tr>'
        html += '<tr><td colspan="2"><b>DESDE</b></td><td colspan="2">' + str(
            fechainicial) + '</td><td colspan="2"><b>HASTA</b></td><td colspan="1">' + str(fechafin) + '</td></tr>'
        # html+='<tr><th>TIPO</th>'
        # #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        # html+='<th style="width:150px ;">Numero</th>'
        # html+= '<th style="width:81px ;">Fecha</th>'
        # html+='<th>Debito</th><th>Credito</th><th>Saldo</th><th>Concepto</th></tr></thead>'
        html += '</thead>'
        html += '<tbody>'
        # sql0="select id_cliente,codigo_cliente,nombre_cliente from cliente where  Cast(codigo_cliente as int)>="+str(codigo_cliente)+"and  Cast(codigo_cliente as int)<="+str(codigo_cliente_h)
        # cursor.execute(sql0);
        cursor.execute('select id_cliente,codigo_cliente,nombre_cliente from cliente '
                       ' where codigo_cliente::int>=%s '
                       'and  codigo_cliente::int<=%s '
                       'order by codigo_cliente ', (int(codigo_cliente), int(codigo_cliente_h)))

        rowc = cursor.fetchall();
        total_a = 0
        total_ap = 0
        for pc in rowc:
            total_cuenta = 0
            total_factura = 0
            total_proforma = 0
            total_cheque = 0
            total_chequepro = 0
            total_saldo = 0
            total_saldo_por_cuenta = 0

            cliente = pc[0]

            # Facturas
            lcSql = "SELECT  distinct dv.id,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0, "
            lcSql += "dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,drv.establecimiento,drv.punto_emision, "
            lcSql += "drv.secuencial,drv.autorizacion,c.codigo_cliente,c.ruc,drv.id,dv.activo,dv.proforma_id "
            lcSql += "FROM documento_venta dv "
            lcSql += "LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
            lcSql += "LEFT JOIN documento_retencion_venta drv ON drv.documento_venta_id=dv.id  and drv.anulado is not True "
            lcSql += "where dv.activo is not False and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id=" + str(
                cliente)

            cursor1 = connection.cursor()
            cursor1.execute();
            row = cursor1.fetchall();

            # Proformas
            cursor2 = connection.cursor()
            sql2 = "SELECT  distinct dv.id,dv.fecha,dv.abreviatura_codigo,dv.codigo,dv.puntos_venta_id,dv.vendedor_id,dv.observacion,dv.iva,dv.porcentaje_iva,dv.subtotal,"
            sql2 += "dv.descuento,dv.total,c.nombre_cliente,c.codigo_cliente,c.ruc,dv.aprobada "
            sql2 += "FROM proforma dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
            sql2 += "where dv.fecha>='" + fechainicial + "' and dv.fecha<='" + fechafin + "' and dv.id "
            sql2 += "NOT IN (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL) and dv.aprobada is True and dv.cliente_id=" + str(
                cliente)
            cursor2.execute(sql2)
            row21 = cursor2.fetchall()

            # PROFORMAS QUE FUERON ABONADAS ANTES DE CONVERTIRSE EN FACTURA
            cursor22 = connection.cursor()
            sql22 = "SELECT  distinct dv.id,dv.fecha,dv.abreviatura_codigo,dv.codigo,dv.puntos_venta_id,dv.vendedor_id,dv.observacion,dv.iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,c.codigo_cliente,c.ruc,dv.aprobada FROM proforma dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id where dv.fecha>='" + fechainicial + "' and dv.fecha<='" + fechafin + "' and dv.id  IN(select da.proforma_id from documento_abono_venta da  where da.anulado is not True and da.documento_venta_id is null) and dv.id in (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL) and dv.aprobada is True and dv.cliente_id=" + str(
                cliente)
            cursor22.execute(sql22)
            row22 = cursor22.fetchall()

            # SQL CHEQUES PROTESTADOS

            cursor3 = connection.cursor()
            sql5 = "select distinct cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante from cheques_protestados cp,movimiento m,documento_abono_venta da,documento_venta dv where cp.anulado is not True and m.id=cp.movimiento_id and da.movimiento_id=m.id and da.documento_venta_id=dv.id and cp.fecha_emision>='" + fechainicial + "' and cp.fecha_emision<='" + fechafin + "' and dv.cliente_id=" + str(
                cliente)
            print sql5
            cursor3.execute(sql5);
            chequesp = cursor3.fetchall()

            cursor4 = connection.cursor()
            sql6 = "select distinct cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante from cheques_protestados cp,movimiento m,documento_abono_venta da,proforma dv where cp.anulado is not True and m.id=cp.movimiento_id and da.movimiento_id=m.id and da.proforma_id=dv.id and da.documento_venta_id is null and dv.fecha>='" + fechainicial + "' and dv.fecha<='" + fechafin + "' and dv.cliente_id=" + str(
                cliente)
            print sql6
            cursor4.execute(sql6);
            chequespr = cursor4.fetchall()

            if len(row) > 0 or len(row21) > 0 or len(chequesp) > 0 or len(chequespr) > 0:
                html += '<tr><td colspan="7"><h5><b>' + str(pc[1]) + '-' + str(
                    pc[2].encode('utf8')) + '</b></h5></td></tr>'
                html += '<tr style="border:solid 1px black"><th>TIPO</th>'
                # html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
                html += '<th style="width:150px ;">Numero</th>'
                html += '<th style="width:81px ;">Fecha</th>'
                html += '<th>Debito</th><th>Credito</th><th>Saldo</th><th>Concepto</th></tr>'

            for p in row:
                html += '<tr>'
                html += '<td><b>&nbsp;FACTURA</b></td>'

                factura = ''
                if p[2]:
                    factura += '' + str(p[2]) + '-'
                else:
                    factura += '-'

                if p[3]:
                    factura += '' + str(p[3]) + '-'
                else:
                    factura += '-'

                if p[4]:
                    factura += '' + str(p[4])
                else:
                    factura += ''
                html += '<td ><b>' + str(factura) + '</b></td>'

                if p[1]:
                    html += '<td style="text-align:center"><b>' + str(p[1]) + '</b></td>'
                else:
                    html += '<td></td>'

                if p[14]:
                    # html += '<td style="text-align:center">' + str(p[14]) + '</td>'
                    totalf = p[14]
                else:
                    # html += '<td></td>'
                    totalf = 0

                total_debito = total_debito + totalf
                html += '<td style="text-align:right"><b>' + str("%0.2f" % totalf).replace('.', ',') + '</b></td>'
                html += '<td style="text-align:center"></td>'
                html += '<td style="text-align:right"><b>' + str("%0.2f" % totalf).replace('.', ',') + '</b></td>'
                html += '<td><b>' + str(p[5].encode('utf8')) + '</b></td>'

                html += '</tr>'
                total_cuenta = float(total_cuenta) + totalf
                # RETENCIONES SUMA

                if p[0]:

                    saldo = 0

                    cursor = connection.cursor()
                    sqlr3 = "select sum(drdv.valor_retenido),drv.id,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id from documento_retencion_venta drv,documento_retencion_detalle_venta drdv where drv.id=drdv.documento_retencion_venta_id and drv.documento_venta_id=" + str(
                        p[
                            0]) + " and drv.anulado is not True group by drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id"
                    print sqlr3
                    cursor.execute(sqlr3);
                    rowr3 = cursor.fetchall()
                    retencion = 0
                    retencion1 = 0
                    for pr2 in rowr3:

                        retencion_cod = ''
                        if pr2[2]:
                            retencion_cod += '' + str(pr2[2]) + '-'
                        else:
                            retencion_cod += '-'

                        if pr2[3]:
                            retencion_cod += '' + str(pr2[3]) + '-'
                        else:
                            retencion_cod += '-'

                        if pr2[4]:
                            retencion_cod += '' + str(pr2[4])
                        else:
                            retencion_cod += ''

                        html += '<tr>'
                        html += '<td>&nbsp;RETENCIONES</td>'

                        html += '<td style="text-align:center">' + str(retencion_cod) + '</td>'
                        html += '<td style="text-align:center">' + str(pr2[5]) + '</td>'
                        html += '<td style="text-align:right">0,00</td>'

                        if pr2[0]:
                            saldo = Decimal(saldo) + Decimal(pr2[0])

                        total_a = float(totalf) - float(saldo)
                        total_credito = total_credito + float(pr2[0])
                        html += '<td style="text-align:right">' + str("%0.2f" % pr2[0]).replace('.', ',') + '</td>'
                        html += '<td style="text-align:right">' + str("%0.2f" % total_a).replace('.', ',') + '</td>'
                        html += '<td style="text-align:center">' + str(pr2[6].encode('utf8')) + '</td>'

                        html += '</tr>'
                        total_cuenta = float(total_cuenta) - float(pr2[0])
                    cursor = connection.cursor();
                    sql3 = "select distinct da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.documento_venta_id=" + str(
                        p[
                            0]) + " and m.fecha_emision>='" + fechainicial + "' and m.fecha_emision<='" + fechafin + "' order by m.fecha_emision"
                    print sql3
                    cursor.execute(sql3);
                    row3 = cursor.fetchall()

                    for p3 in row3:
                        html += '<tr>'
                        html += '<td>&nbsp;' + str(p3[13].encode('utf8')) + '</td>'

                        # html += '<td></td>'
                        # html += '<td>'+str(p3[13])+'</td>'
                        html += '<td>' + str(p3[9]) + '</td>'
                        html += '<td style="text-align:center">' + str(p3[4]) + '</td>'
                        # html += '<td></td>'
                        html += '<td></td>'
                        # credito
                        html += '<td style="text-align:right">' + str("%0.2f" % p3[0]).replace('.', ',') + '</td>'
                        total_a = 0

                        if p[11] == True:
                            html += '<td style="text-align:right">0,00</td>'
                            estadof = 'ANULADO'

                        else:
                            saldo = saldo + p3[0]
                            total_a = float(totalf) - float(saldo)
                            html += '<td style="text-align:right">' + str("%0.2f" % total_a).replace('.', ',') + '</td>'
                            estadof = 'ACTIVO'
                            total_credito = total_credito + float(p3[0])
                            total_cuenta = float(total_cuenta) - float(p3[0])

                        html += '<td>' + str(p3[8].encode('utf8')) + '</td>'

                        html += '</tr>'

                    # NOTA DE CREDITO
                    # NOTAS DE CREDITO
                    cursor = connection.cursor();
                    sql4 = "select distinct da.total,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion from movimiento_nota_credito da LEFT JOIN movimiento m ON m.id=da.movimiento_id and m.activo is True LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.documento_venta_id=" + str(
                        p[0]) + " order by m.fecha_emision"
                    # print sql4
                    cursor.execute(sql4);
                    row4 = cursor.fetchall()
                    for p4 in row4:
                        html += '<tr>'
                        html += '<td>' + str(p4[13].encode('utf8')) + '</td>'

                        html += '<td>' + str(p4[9]) + '</td>'
                        html += '<td>' + str(p4[4]) + '</td>'
                        # html += '<td></td>'

                        # credito
                        html += '<td style="text-align:right">0,00</td>'
                        html += '<td style="text-align:right">' + str("%2.2f" % p4[0]).replace('.', ',') + '</td>'

                        total_a = 0

                        if p[11] == True:
                            html += '<td></td>'
                            estadof = 'ANULADO'

                        else:
                            saldo = saldo + p4[0]
                            total_a = float(totalf) - float(saldo)
                            html += '<td style="text-align:right">' + str("%2.2f" % total_a).replace('.', ',') + '</td>'
                            estadof = 'ACTIVO'
                            total_credito = total_credito + float(p4[0])

                        html += '<td>' + str(p4[8].encode('utf8')) + '</td>'

                        html += '</tr>'

                    total_factura = float(total_factura) + float(total_a)

                    # if p[24]:
                #     cursor = connection.cursor();
                #     sql31="select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and m.asociado_cheques_protestados is not True and da.proforma_id="+ str(p[24])+" and da.documento_venta_id is null order by m.fecha_emision"
                #     print sql31
                #     cursor.execute(sql31);
                #     row31 = cursor.fetchall()
                #
                #     for p31 in row31:
                #         html += '<tr>'
                #         html += '<td>&nbsp;'+str(p31[13].encode('utf8'))+'</td>'
                #
                #         #html += '<td></td>'
                #         #html += '<td>'+str(p3[13])+'</td>'
                #         html += '<td>'+str(p31[9])+'</td>'
                #         html += '<td style="text-align:center">'+str(p31[4])+'</td>'
                #         #html += '<td></td>'
                #         html += '<td style="text-align:right">0,00</td>'
                #         #credito
                #         html += '<td style="text-align:right">'+str("%0.2f" % p31[0]).replace('.', ',')+'</td>'
                #         total_a=0
                #
                #         if p[11]==True:
                #             html += '<td style="text-align:right">0,00</td>'
                #             estadof1='ANULADO'
                #
                #         else:
                #             saldo=saldo+p31[0]
                #             total_a=float(totalf)-float(saldo)
                #             total_credito=total_credito+float(p31[0])
                #             html += '<td style="text-align:right">'+str("%0.2f" % total_a).replace('.', ',')+'</td>'
                #             estadof='ACTIVO'
                #             total_cuenta=float(total_cuenta)-float(p31[0])
                #
                #
                #
                #         html += '<td>'+str(p31[8].encode('utf8'))+'</td>'
                #
                #         html += '</tr>'
                #

            # PROFORMA
            for p21 in row21:
                proforma = ''
                if p21[1]:
                    proforma += '' + str(p21[2]) + '-'
                else:
                    proforma += '-'

                if p21[2]:
                    proforma += '' + str(p21[3]) + '-'
                else:
                    proforma += '-'

                html += '<tr>'
                html += '<td style=""><b>&nbsp;PROFORMA</b></td>'
                html += '<td ><b>' + str(proforma) + '</b></td>'
                html += '<td style="text-align:center"><b>' + str(p21[1]) + '</b></td>'
                html += '<td style="text-align:right"><b>' + str("%0.2f" % p21[11]).replace('.', ',') + '</b></td>'
                html += '<td style="text-align:right"><b>0,00</b></td>'
                if p21[11]:
                    totalp = float(p21[11])

                else:
                    totalp = 0
                total_debito = total_debito + float(totalp)
                html += '<td style="text-align:right"><b>' + str("%0.2f" % p21[11]).replace('.', ',') + '</b></td>'
                html += '<td><b>' + str(p21[6].encode('utf8')) + '</b></td>'
                html += '</tr>'
                total_cuenta = float(total_cuenta) + float(totalp)

                if p21[0]:
                    cursor = connection.cursor();
                    sql4 = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and m.asociado_cheques_protestados is not True and da.proforma_id=" + str(
                        p21[0]) + "order by m.fecha_emision"
                    print sql4

                    cursor.execute(sql4);
                    row4 = cursor.fetchall()
                    saldop = 0
                    for p4 in row4:
                        html += '<tr>'
                        html += '<td>&nbsp;' + str(p4[13].encode('utf8')) + '</td>'

                        # html += '<td></td>'
                        # html += '<td>'+str(p3[13])+'</td>'
                        html += '<td>' + str(p4[9]) + '</td>'
                        html += '<td style="text-align:center">' + str(p4[4]) + '</td>'
                        # html += '<td></td>'
                        html += '<td style="text-align:right">0,00</td>'
                        # credito
                        html += '<td style="text-align:right">' + str("%0.2f" % p4[0]).replace('.', ',') + '</td>'
                        total_ap = 0

                        saldop = saldop + p4[0]
                        print saldop
                        total_ap = float(totalp) - float(saldop)
                        print total_ap
                        html += '<td style="text-align:right">' + str("%0.2f" % total_ap).replace('.', ',') + '</td>'
                        total_credito = total_credito + float(p4[0])

                        total_cuenta = float(total_cuenta) - float(p4[0])

                        html += '<td>' + str(p4[8].encode('utf8')) + '</td>'

                        html += '</tr>'

                    total_proforma = float(total_proforma) + float(total_ap)
                    # CHEQUES PROTESTADOS
            saldocp = 0
            total_cp = 0
            print 'cheques protestados'

            if chequesp:
                for chp in chequesp:

                    html += '<tr>'
                    html += '<td>&nbsp;CH. PROTESTADO No.' + str(chp[2]) + '</td>'

                    html += '<td>' + str(chp[10]) + '</td>'
                    html += '<td style="text-align:center">' + str(chp[1]) + '</td>'
                    # html += '<td></td>'
                    html += '<td style="text-align:right">' + str("%0.2f" % chp[4]).replace('.', ',') + '</td>'
                    # credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_a = 0

                    saldocp = Decimal(saldocp) + Decimal(chp[4])
                    total_cp = Decimal(total_cp) + Decimal(saldocp)
                    total_debito = float(total_debito) + float(chp[4])
                    html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'

                    html += '<td>' + str(chp[6].encode('utf8')) + '</td>'

                    html += '</tr>'
                    total_cuenta = float(total_cuenta) + float(chp[4])

                    html += '<tr>'
                    html += '<td>&nbsp;CH. PROTESTADO  No.' + str(chp[2]) + ' MULTA</td>'
                    html += '<td>' + str(chp[10]) + '</td>'
                    html += '<td style="text-align:center">' + str(chp[1]) + '</td>'
                    # html += '<td></td>'
                    html += '<td style="text-align:right">' + str("%0.2f" % chp[5]).replace('.', ',') + '</td>'
                    # credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_ac = 0

                    saldocp = Decimal(saldocp) + Decimal(chp[5])
                    total_cp = Decimal(total_cp) + Decimal(saldocp)
                    total_debito = float(total_debito) + float(chp[5])
                    html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'

                    html += '<td>' + str(chp[6].encode('utf8')) + '</td>'

                    html += '</tr>'
                    total_cuenta = float(total_cuenta) + float(chp[5])

                    # Abono Cheques Protestados
                    cursor = connection.cursor();
                    sqlc3 = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_cheque da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.cheques_protestados_id=" + str(
                        chp[0]) + " order by m.fecha_emision"
                    print sqlc3
                    cursor.execute(sqlc3);
                    rowc3 = cursor.fetchall()
                    saldoabono = 0

                    for pc3 in rowc3:
                        html += '<tr>'
                        html += '<td>&nbsp;' + str(pc3[13].encode('utf8')) + '</td>'

                        # html += '<td></td>'
                        # html += '<td>'+str(p3[13])+'</td>'
                        html += '<td>' + str(pc3[9]) + '</td>'
                        html += '<td style="text-align:center">' + str(pc3[4]) + '</td>'
                        # html += '<td></td>'
                        html += '<td></td>'
                        # credito
                        html += '<td style="text-align:right">' + str("%0.2f" % pc3[0]).replace('.', ',') + '</td>'
                        total_ch = 0

                        if pc3[1] == True:
                            html += '<td style="text-align:right">0,00</td>'
                            estadof = 'ANULADO'

                        else:
                            saldoabono = saldoabono + pc3[0]
                            saldocp = float(saldocp) - float(saldoabono)
                            html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'
                            estadof = 'ACTIVO'
                            total_credito = total_credito + float(pc3[0])
                            total_cuenta = float(total_cuenta) - float(pc3[0])

                        html += '<td>' + str(pc3[8].encode('utf8')) + '</td>'

                        html += '</tr>'

                total_cheque = float(total_cheque) + float(saldocp)

            # FINAL DE CHEQUES PROTESTADOS
            # CHEQUES PROTESTADOS proformaas

            if chequespr:
                for chpr in chequespr:

                    html += '<tr>'
                    html += '<td>&nbsp;CH. PROTESTADO  No.' + str(chpr[2]) + '</td>'

                    html += '<td>' + str(chpr[10]) + '</td>'
                    html += '<td style="text-align:center">' + str(chpr[1]) + '</td>'
                    # html += '<td></td>'
                    html += '<td style="text-align:right">' + str("%0.2f" % chpr[4]).replace('.', ',') + '</td>'
                    # credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_a = 0

                    saldocp = Decimal(saldocp) + Decimal(chpr[4])
                    total_cp = Decimal(total_cp) + Decimal(saldocp)
                    total_debito = float(total_debito) + float(chpr[4])
                    html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'

                    html += '<td>' + str(chpr[6].encode('utf8')) + '</td>'

                    html += '</tr>'
                    total_cuenta = float(total_cuenta) + float(chpr[4])
                    html += '<tr>'
                    html += '<td>&nbsp;CH. PROTESTADO  No.' + str(chpr[2]) + ' MULTA</td>'
                    html += '<td>' + str(chpr[10]) + '</td>'
                    html += '<td style="text-align:center">' + str(chpr[1]) + '</td>'
                    # html += '<td></td>'
                    html += '<td style="text-align:right">' + str("%0.2f" % chpr[5]).replace('.', ',') + '</td>'
                    # credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_ac = 0

                    saldocp = Decimal(saldocp) + Decimal(chpr[5])
                    total_cp = Decimal(total_cp) + Decimal(saldocp)
                    total_debito = float(total_debito) + float(chpr[5])
                    html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'

                    html += '<td>' + str(chpr[6].encode('utf8')) + '</td>'

                    html += '</tr>'
                    total_cuenta = float(total_cuenta) + float(chpr[5])
                    cursor = connection.cursor();
                    sqlc4 = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_cheque da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.cheques_protestados_id=" + str(
                        chpr[0]) + " order by m.fecha_emision"
                    print sqlc4
                    cursor.execute(sqlc4);
                    rowc4 = cursor.fetchall()
                    saldoabono = 0

                    for pc3 in rowc4:
                        html += '<tr>'
                        html += '<td>&nbsp;' + str(pc3[13].encode('utf8')) + '</td>'

                        # html += '<td></td>'
                        # html += '<td>'+str(p3[13])+'</td>'
                        html += '<td>' + str(pc3[9]) + '</td>'
                        html += '<td style="text-align:center">' + str(pc3[4]) + '</td>'
                        # html += '<td></td>'
                        html += '<td></td>'
                        # credito
                        html += '<td style="text-align:right">' + str("%0.2f" % pc3[0]).replace('.', ',') + '</td>'
                        total_ch = 0

                        if pc3[1] == True:
                            html += '<td style="text-align:right">0,00</td>'
                            estadof = 'ANULADO'

                        else:
                            saldoabono = saldoabono + pc3[0]
                            saldocp = float(saldocp) - float(saldoabono)
                            html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'
                            estadof = 'ACTIVO'
                            total_credito = total_credito + float(pc3[0])
                            total_cuenta = float(total_cuenta) - float(pc3[0])

                        html += '<td>' + str(pc3[8].encode('utf8')) + '</td>'

                        html += '</tr>'

                    total_chequepro = float(total_chequepro) + float(saldocp)

            # proformas hechas facturas abonos
            for p22 in row22:

                proforma = ''
                if p22[1]:
                    proforma += '' + str(p22[2]) + '-'
                else:
                    proforma += '-'

                if p22[2]:
                    proforma += '' + str(p22[3]) + '-'
                else:
                    proforma += '-'
                #
                #
                # html+='<tr>'
                # html += '<td style=""><b>&nbsp;PROFORMA</b></td>'
                # html += '<td ><b>' + str(proforma) + '</b></td>'
                # html += '<td style="text-align:center"><b>' + str(p22[1]) + '</b></td>'
                # html += '<td style="text-align:right"><b>' + str("%0.2f" % p22[11]).replace('.', ',')+ '</b></td>'
                # html += '<td style="text-align:right"><b>0,00</b></td>'
                # if p22[11]:
                #     totalp=float(p22[11])
                #
                # else:
                #
                # total_debito=total_debito+float(totalp)
                # html += '<td style="text-align:right"><b>' +str("%0.2f" % p22[11]).replace('.', ',')+ '</b></td>'
                # html += '<td><b>' + str(p22[6].encode('utf8')) + '</b></td>'
                # html += '</tr>'
                # total_cuenta=float(total_cuenta)+float(totalp)

                totalp = 0

                if p22[0]:
                    cursor = connection.cursor();
                    sql41 = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.documento_venta_id is null and  da.anulado is not True and m.asociado_cheques_protestados is not True and da.proforma_id=" + str(
                        p22[0]) + "order by m.fecha_emision"
                    print sql41

                    cursor.execute(sql41);
                    row41 = cursor.fetchall()
                    saldop = 0
                    if row41:
                        html += '<tr><td colspan="7" style="background-color:yellow">Abonos a proforma ' + str(
                            proforma) + ' que se convirtieron en diferentes facturas </td></tr>'

                        for p4 in row41:
                            html += '<tr>'
                            html += '<td>&nbsp;' + str(p4[13].encode('utf8')) + '</td>'

                            # html += '<td></td>'
                            # html += '<td>'+str(p3[13])+'</td>'
                            html += '<td>' + str(p4[9]) + '</td>'
                            html += '<td style="text-align:center">' + str(p4[4]) + '</td>'
                            # html += '<td></td>'
                            html += '<td style="text-align:right">0,00</td>'
                            # credito
                            html += '<td style="text-align:right">' + str("%0.2f" % p4[0]).replace('.', ',') + '</td>'
                            total_ap = 0

                            saldop = saldop + p4[0]
                            print saldop
                            total_ap = float(totalp) - float(saldop)
                            print total_ap
                            html += '<td style="text-align:right">' + str("%0.2f" % total_ap).replace('.',
                                                                                                      ',') + '</td>'
                            total_credito = total_credito + float(p4[0])

                            total_cuenta = float(total_cuenta) - float(p4[0])

                            html += '<td>' + str(p4[8].encode('utf8')) + '</td>'

                            html += '</tr>'

                    total_proforma = float(total_proforma) + float(total_ap)

            if len(row) > 0 or len(row21) > 0 or len(chequesp) > 0 or len(chequespr) > 0:
                total_saldo_por_cuenta = total_factura + total_proforma + total_cheque + total_chequepro
                html += '<tr><td></td><td></td><td></td><td colspan="2">SALDO FINAL </td><td style="text-align:right">' + str(
                    "%0.2f" % total_cuenta).replace('.', ',') + '</td><td></td></tr>'
                # FINAL DE CHEQUES PROTESTADOS

        print 'hrl'
        total_saldo_acum = float(total_debito) - float(total_credito)

        html += '</tbody>'
        html += '<tfoot><tr><td></td><td></td><td></td><td style="text-align:right">' + str(
            "%0.2f" % total_debito).replace('.', ',') + '</td><td style="text-align:right">' + str(
            "%0.2f" % total_credito).replace('.', ',') + '</td><td>' + str("%0.2f" % total_saldo_acum).replace('.',
                                                                                                               ',') + '</td><td></td></tr></tfoot>'
        html += '</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


#NUEVO REPORTE DE INVENTARIO
def reporteInventarioNuevo(request):
    bodega = Bodega.objects.values('id', 'codigo_bodega', 'nombre')
    tipos = TipoProducto.objects.values('id', 'codigo', 'descripcion')

    return render_to_response('inventario/inventario_nuevo.html', {'bodega': bodega, 'tipos': tipos}, RequestContext(request))


@csrf_exempt
def obtenerInventarioNuevo(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        tipos = request.POST.get('tipos')
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        cursor = connection.cursor();
        sql=''
        if tipos == '0':
            sql+="select distinct pb.producto_bodega_id,pb.producto_id,p.codigo_producto,p.descripcion_producto,pb.cantidad,pb.bodega_id,b.codigo_bodega,b.nombre,p.cant_maxima,p.cant_minimia,t.descripcion,p.costo,p.unidad from producto_en_bodega pb,producto p,bodega b,tipo_producto t where pb.producto_id=p.producto_id and b.id=pb.bodega_id and p.tipo_producto=t.id and pb.bodega_id=" + bodega

        else:
            sql +="select distinct pb.producto_bodega_id,pb.producto_id,p.codigo_producto,p.descripcion_producto,pb.cantidad,pb.bodega_id,b.codigo_bodega,b.nombre,p.cant_maxima,p.cant_minimia,t.descripcion,p.costo,p.unidad from producto_en_bodega pb,producto p,bodega b,tipo_producto t where pb.producto_id=p.producto_id and b.id=pb.bodega_id and p.tipo_producto=t.id and p.tipo_producto=" + tipos + " and pb.bodega_id=" + bodega

        if codigo!= '':
            # sql +=" and p.codigo_producto like '%" +codigo+ "%'"
            sql +=" and p.codigo_producto ='" +codigo+ "'"
        if nombre!= '':
            sql +=" and p.descripcion_producto like '%" +nombre+ "%'"
        cursor.execute(sql);
        row = cursor.fetchall();
        total_cantidad = 0
        total_costo = 0.0
        total_c = 0
        total_valor=0
        cant=0
        cost=0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            cost = 0
            cant =0
            html += '<tr><td>' + str(p[2]) + '</td>'
            html += '<td>' + str(p[3].encode('utf8')) + '</td>'
            html += '<td>' + str(p[10]) + '</td>'
            #html += '<td>' + str(p[12])+ '</td>'
            if p[4] < p[9]:
                html += '<td style="font-weight:bold;color:red">' + str(p[4]) + '</td>'
            else:
                html += '<td>' + str(p[4]) + '</td>'
            #html += '<td>' + str(p[8]) + '</td>'
            #html += '<td>' + str(p[9]) + '</td>'
            if p[11]:
                cls=p[11]*1
            else:
                cls=0
            html += '<td>' + str(round(cls,2)) + '</td>'
            if p[4]:
                cant=p[4]
            if p[11]:
                cost=p[11]
            total_c=round(cant*cost,2)
            html += '<td>' + str(total_c) + '</td>'
            total_cantidad = round((total_cantidad + p[4]),2)
            total_valor = total_valor + total_c
	    #total_kit=float(p[4])*float(p[11])
	    #html += '<td>' + str(total_kit) + '</td>'
            if p[11]:
                total_costo = round(total_costo + p[11],2)
            html += '</tr>'
        html += '<tr><td colspan="3"><b>Total</b></td>'
        html += '<td><b>' + str(total_cantidad) + '</b></td>'
        html += '<td><b>' + str(total_costo) + '</b></td>'
        html += '<td><b>' + str(total_valor) + '</b></td>'
        html += '</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404



def reporteOrdenCompraNuevo(request):
    proveedor = Proveedor.objects.values('proveedor_id', 'codigo_proveedor', 'nombre_proveedor')

    return render_to_response('inventario/ordenes_compra_nuevo.html', {'proveedor': proveedor,}, RequestContext(request))


@csrf_exempt
def obtenerOrdenCompraNuevo(request):
    if request.method == 'POST':
        proveedor = request.POST.get('proveedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor()
        sql="select distinct p.compra_id,p.nro_compra,p.fecha,p.notas,p.bodega_id,p.proveedor_id,c.nombre_proveedor,p.subtotal,p.impuesto_monto,p.total,b.nombre from orden_compra p,proveedor c,bodega b where p.proveedor_id=c.proveedor_id and b.id=p.bodega_id"
        if proveedor != '0':
            sql+=" and p.proveedor_id=" + proveedor
        else:
            print("entro no proveedor")

        print fechainicial
        print("fecha inicial")
        if fechainicial == '0':
            print("entro no feccha inicial")

        else:
            sql += " and p.fecha>='" + fechainicial + "'"
        if fechafin == '0':
            print("entro no fecha final")

        else:
            sql += " and p.fecha<='" + fechafin + "'"


        sql+=" order by p.fecha"
        cursor.execute(sql)

        row = cursor.fetchall()
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        html += '<thead><tr><th>Fecha</th><th>No.Compra</th><th width="100px">Proveedor&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th><th>Concepto</th><th width="150px">Codigo&nbsp;&nbsp;</th><th>Producto</th><th>Subtotal</th><th>iva</th><th>Total</th></tr></thead>'
        html += '<tbody>'
        for p in row:

            ped = ComprasDetalle.objects.filter(compra_id=str(p[0]))
            cont=0
            for pe in ped:
                html += '<tr>'
                cont=cont+1
                if cont==1:
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[2]) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[1]) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[6].encode('utf8')) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[3].encode('utf8')) + '</td>'
                html += '<td>'
                html += ''+str(pe.producto.codigo_producto) + '</td><td>'  + str(pe.producto.descripcion_producto.encode('utf8'))+'</td>'
                #html += '<td> ' + str(pe.cantidad) + '</td><td> ' + str(pe.precio_compra) + '</td>'
                if cont == 1:
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[7]) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[8]) + '</td>'
                    html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[9]) + '</td>'
                    total = total + p[9]
                    subtotal = subtotal + p[7]
                    iva = iva + p[8]
                html += '</tr>'
        html += '<tr><td colspan="5"></td>'
        html += '<td></td>'
        html += '<td><b>' + str(subtotal) + '</b></td>'
        html += '<td><b>' + str(iva) + '</b></td>'
        html += '<td><b>' + str(total) + '</b></td>'
        html += '</tr>'
        html += '</tbody>'
        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteComprasLocalesNuevo(request):
    proveedor = Proveedor.objects.values('proveedor_id', 'codigo_proveedor', 'nombre_proveedor')

    return render_to_response('inventario/compras_locales_nuevo.html', {'proveedor': proveedor,}, RequestContext(request))


@csrf_exempt
def obtenerComprasLocalesNuevo(request):
    if request.method == 'POST':
        proveedor = request.POST.get('proveedor')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        producto = request.POST.get('producto')
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')

        cursor = connection.cursor();
        sql = 'select distinct p.id,p.codigo,p.fecha,co.notas,co.bodega_id,p.proveedor_id,c.nombre_proveedor,p.subtotal,p.iva,p.total,b.nombre,co.aprobada,co.nro_compra,co.compra_id from compras_locales p,orden_compra co,proveedor c,bodega b where p.proveedor_id=c.proveedor_id and b.id=co.bodega_id and co.compra_id=p.orden_compra_id '
        if proveedor != '0':
            sql += " and p.proveedor_id=" + proveedor
        else:
            print("entro no proveedor")



        print fechainicial
        print("fecha inicial")
        if fechainicial == '0':
            print("entro no feccha inicial")

        else:
            sql += " and p.fecha>='" + fechainicial + "'"
        if fechafin == '0':
            print("entro no fecha final")

        else:
            sql += " and p.fecha<='" + fechafin + "'"
        
        



        sql += " order by p.fecha"
        cursor.execute(sql)
        row = cursor.fetchall();
        
    
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html=''
        
        for p in row:
            sql3='select distinct p.codigo_producto,p.descripcion_producto,cd.* from producto p,compras_detalle cd where cd.producto_id=p.producto_id and cd.recibido is True and cd.compra_id='+str(p[13])
            if codigo!= '':
                sql3 +=" and p.codigo_producto like '%" +codigo+ "%'"
            if nombre!= '':
                sql3 +=" and p.descripcion_producto like '%" +nombre+ "%'"
            
            cursor.execute(sql3)
            row3 = cursor.fetchall();
            if row3:
                html += '<tr style="border:1px solid #ddd"><td colspan="3" style="border-right:0px;border-left:0px"><b>Fecha:' + str(
                        p[2]) + '</b></td><td style="border-right:0px;border-left:0px"  colspan="4"><b>N&uacute;mero:</b>' + str(
                        p[1]) + '</td></tr><tr><td style="border-left:0px" colspan="3"><b>Proveedor:' + str(p[6].encode('utf8')) + '</b></td>'
                html += '<td  colspan="4" style="border-right:0px;border-left:0px">'
                    #html += '<b>OC:' + str(p[12]) + '</b>'
                html += '</td></tr>'
                html += '<tr><th>Cod.</th><th>Producto</th><th width="100px">Cantidad&nbsp;&nbsp;</th><th>Precio Unitario</th><th>Subtotal</th><th>Iva</th><th>Total</th></tr>'
                ped = ComprasDetalle.objects.filter(compra_id=str(p[13]))
                cont=0
                for pe in ped:
                    cont=cont+1
                    html += '<tr>'
                    html += '<td style="border-right:0px">' + str(pe.producto.codigo_producto.encode('utf8')) + '</td>'
                    html += '<td style="border-right:0px">' + str(pe.producto.descripcion_producto.encode('utf8')) + '</td>'
                    html += '<td style="border-right:0px;border-left:0px">' + str(pe.cantidad) + '</td>'
                    html += '<td style="border-left:0px">' + str(pe.precio_compra) + '</td>'
                    if cont==1:
                        html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[7]) + '</td>'
                        html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[8]) + '</td>'
                        html += '<td style="border-left:0px;vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[9]) + '</td>'
                    html += '</tr>'
                    total = total + p[9]
                    subtotal = subtotal + p[7]
                    iva = iva + p[8]
                html+='</tr>'
                    
                    
                    
                    
        html+='<tr><td colspan="3"></td>'
        html+='<td>Total</td>'
        html+='<td><b>'+str(subtotal)+'</b></td>'
        html+='<td><b>'+str(iva)+'</b></td>'
        html+='<td><b>'+str(total)+'</b></td>'
        html+='</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404

def reporteOrdenEgresoNuevo(request):
    bodega = Bodega.objects.values('id', 'codigo_bodega', 'nombre')

    return render_to_response('inventario/ordenes_egreso_nuevo.html', {'bodega': bodega,}, RequestContext(request))


@csrf_exempt
def obtenerOrdenEgresoNuevo(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();

        sql = "select distinct p.id,p.codigo,p.fecha,p.notas,p.comentario,p.bodega_id,p.aprobada,p.orden_produccion_codigo,b.nombre from orden_egreso p,bodega b where b.id=p.bodega_id and p.bodega_id=" + bodega

        if fechainicial == '0':
            print("entro no feccha inicial")

        else:
            sql += " and p.fecha>='" + fechainicial + "'"
        if fechafin == '0':
            print("entro no fecha final")

        else:
            sql += " and p.fecha<='" + fechafin + "'"

        sql += " order by p.fecha"
        cursor.execute(sql)
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        total=0
        cantidad=0
        costo=0
        for p in row:

            ped = OrdenEgresoDetalle.objects.filter(orden_egreso_id=str(p[0]))
            cont=0
            for pe in ped:
                cont=cont+1

                html += '<tr>'
                if cont == 1:
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[2]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[1]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[3].encode('utf8'

                                                                                                                  )) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[4].encode('utf8')) + '</td>'
                    #html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[7].encode('utf8')) + '</td>'
                if pe.orden_produccion_receta:
                    html += ' <td> '+ str(pe.orden_produccion_receta.suborden_produccion.orden_produccion.codigo.encode('utf8')) + ' </td>'
                else:
                     html += '<td></td>'
                    
                html += ' <td> ' + str(pe.producto.codigo_producto.encode('utf8')) + ' </td>'
                html += ' <td> ' + str(pe.producto.descripcion_producto.encode('utf8')) + ' </td>'
                html += '<td>' + str(pe.cantidad) + '</td>'
                html += '<td>'+str(pe.precio_compra)+'</td><td>'+str(pe.total)+'</td>'
                html += '</tr>'
                total = total + pe.total
                cantidad = cantidad + pe.cantidad
                costo = costo + pe.precio_compra

        html += '<tr><td colspan="6"></td>'
        html += '<td><b>Total</b></td>'
        html += '<td><b>' + str(cantidad) + '</b></td>'
        html += '<td><b>' + str(costo) + '</b></td>'
        html += '<td><b>' + str(total) + '</b></td>'
        html += '</tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteEgresoxOrdenEgresoNuevo(request):
    bodega = Bodega.objects.values('id', 'codigo_bodega', 'nombre')
    proveedor = Proveedor.objects.values('proveedor_id', 'codigo_proveedor', 'nombre_proveedor')
    areas = Areas.objects.values('id', 'descripcion')

    return render_to_response('inventario/egreso_orden_egreso_nuevo.html', {'bodega': bodega,'proveedor': proveedor, 'areas': areas}, RequestContext(request))


@csrf_exempt
def obtenerEgresoxOrdenEgresoNuevo(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        proveedor = request.POST.get('proveedor')
        cursor = connection.cursor();

        sql = "select distinct p.id,ep.codigo,ep.fecha,p.notas,ep.comentario,p.bodega_id,p.aprobada,p.orden_produccion_codigo,b.nombre,p.codigo,ep.subtotal,ep.iva,ep.total,ep.proveedor_id from orden_egreso p,bodega b,egreso_orden_egreso ep where b.id=p.bodega_id and ep.orden_egreso_id=p.id and p.bodega_id=" + bodega

        if fechainicial == '0':
            print("entro no feccha inicial")

        else:
            sql += " and ep.fecha>='" + fechainicial + "'"
        if fechafin == '0':
            print("entro no fecha final")

        else:
            sql += " and ep.fecha<='" + fechafin + "'"
        
        if proveedor != '0':
            sql+=" and ep.proveedor_id=" + proveedor
        else:
            print("entro no proveedor")

        sql += " order by ep.fecha"
        cursor.execute(sql)
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        total=0
        cantidad=0
        costo=0
        total_t=0
        subtotal_t=0
        iva_t=0
        for p in row:

            ped = OrdenEgresoDetalle.objects.filter(orden_egreso_id=str(p[0]))
            cont=0
            for pe in ped:
                cont=cont+1
                Areaid = pe.areas_id
                QueryArea = Areas.objects.filter(id = Areaid)

                for a in QueryArea:
                    area = a

                DetArea = area.descripcion


                html += '<tr>'

                des = DetArea
                if cont == 1:
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[2]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[1]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="' + str(ped.count()) + '">' + str(p[9]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[3].encode('utf8')) + '</td>'
                    if p[13]:
                        prov = Proveedor.objects.get(proveedor_id=str(p[13]))
                    else:
                        prov= None
                    if prov:
                        html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(prov.nombre_proveedor.encode('utf8')) + '</td>'
                    else:
                        html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'"></td>'

                    #html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[4].encode('utf8')) + '</td>'
                    
                    #html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[7].encode('utf8')) + '</td>'

                if pe.orden_produccion_receta:
                    html += ' <td> '+ str(pe.orden_produccion_receta.suborden_produccion.orden_produccion.tipo.encode('utf8')) +'-' + str(pe.orden_produccion_receta.suborden_produccion.orden_produccion.codigo.encode('utf8')) + ' </td>'
                else:
                     html += '<td></td>'
                #html += ' <td> ' + DetArea + ' </td>'
                html += ' <td> ' + DetArea.encode('utf8') + ' </td>'
                html += ' <td> ' + str(pe.producto.codigo_producto.encode('utf8')) + ' </td>'
                html += ' <td> ' + str(pe.producto.descripcion_producto.encode('utf8')) + ' </td>'
                html += '<td>' + str(pe.cantidad) + '</td>'
                html += '<td>'+str(pe.precio_compra)+'</td><td>'+str(pe.total)+'</td>'
                if cont == 1:
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[10]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="'+str(ped.count())+'">' + str(p[11]) + '</td>'
                    html += '<td style="vertical-align:middle" rowspan="' + str(ped.count()) + '">' + str(p[12]) + '</td>'
                    subtotal_t = subtotal_t + p[10]
                    iva_t = iva_t + p[11]
                    total_t=total_t+p[12]

                html += '</tr>'
                total = total + pe.total
                cantidad = cantidad + pe.cantidad
                costo = costo + pe.precio_compra

        html += '<tr><td colspan="7"></td>'
        html += '<td><b>Total</b></td>'
        html += '<td><b>' + str(cantidad) + '</b></td>'
        html += '<td><b>' + str(costo) + '</b></td>'
        html += '<td><b>' + str(total) + '</b></td>'

        html += '<td><b>' + str(subtotal_t) + '</b></td>'
        html += '<td><b>' + str(iva_t) + '</b></td>'
        html += '<td><b>' + str(total_t) + '</b></td>'
        html += '</tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteKardexNuevo(request):
    bodega = Bodega.objects.values('id', 'codigo_bodega', 'nombre')
    tipos = TipoProducto.objects.values('id', 'codigo', 'descripcion')

    return render_to_response('inventario/kardex_nuevo.html', {'bodega': bodega, 'tipos': tipos}, RequestContext(request))


@csrf_exempt
def obtenerKardexNuevo(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        # fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor();
        sql=''
        sql+="select distinct k.egreso,k.fecha_ingreso,k.fecha_egreso,p.codigo_producto,p.descripcion_producto," \
             "k.descripcion,b.codigo_bodega,b.nombre,p.cant_maxima,p.cant_minimia,t.descripcion,p.costo,k.cantidad," \
             "k.created_at,p.producto_id,b.id from producto p,bodega b,tipo_producto t,kardex k where  " \
             "b.id=k.bodega_id and p.tipo_producto=t.id and k.producto_id=p.producto_id and k.bodega_id=" + bodega

        if codigo!= '':
            sql +=" and p.codigo_producto like '%" +codigo+ "%'"
        if nombre!= '':
            sql +=" and p.descripcion_producto like '%" +nombre+ "%'"
        # if fechainicial!= '':
        #     sql +=" and (k.fecha_ingreso >= '" +fechainicial+ "' or k.fecha_egreso >= '" +fechainicial+ "')"
        if fechafin!= '':
            sql +=" and (k.fecha_ingreso<='" +fechafin+ "' or k.fecha_egreso <= '" +fechafin+ "')"
        sql+=" order by k.created_at"
        print sql
        cursor.execute(sql)
        row = cursor.fetchall()
        print row
        total_cantidad = 0
        total_costo = 0.0
        total_c = 0
        total_valor=0
        cant=0
        cost=0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        entrada=0
        salida=0
        id_product=''
        for p in row:
            html += '<tr>'
            if id_product=='':
                id_product=p[14]
            else:
                if id_product==p[14]:
                    print p[14]
                
                else:
                     id_product=p[14]
                     entrada=0
                     salida=0
                
                

            if p[0]:
                html += '<td>' +  str(p[2]) + '</td>'
            else:
                html += '<td>' + str(p[1]) + '</td>'
            html += '<td>' + str(p[3].encode('utf8')) + '</td>'
            html += '<td>' + str(p[4].encode('utf8'))+ '</td>'
            html += '<td>' + str(p[5]) + '</td>'
            html += '<td>' + str(p[7].encode('utf8')) + '</td>'

            if p[0]:
                html += '<td>0</td>'
            else:
                html += '<td>'+ str(p[12]) + '</td>'
                entrada=entrada+float(p[12])

            if p[0]:
                html += '<td>' + str(p[12]) + '</td>'
                salida = salida + float(p[12])
            else:
                html += '<td>0</td>'
            
            
            total=entrada-salida
            html += '<td>'+ str(total) + '</td>'

            # sql2= "select distinct k.egreso,k.fecha_ingreso,k.fecha_egreso,p.codigo_producto,p.descripcion_producto," \
            #        "k.descripcion,b.codigo_bodega,b.nombre,p.cant_maxima,p.cant_minimia,t.descripcion,p.costo,k.cantidad," \
            #        "k.created_at,p.producto_id,b.id from producto p,bodega b,tipo_producto t,kardex k where  " \
            #        "b.id=k.bodega_id and p.tipo_producto=t.id and k.producto_id=p.producto_id and k.bodega_id=" + str(p[15])
            # 
            # sql2 += " and p.producto_id=" + str(p[14])
            # # 
            # # if fechainicial != '':
            # #     sql2 += " and (k.fecha_ingreso < '" + fechainicial + "' or k.fecha_egreso < '" +fechainicial+ "')"
            # # 
            # if fechafin != '':
            #     sql2 += " and (k.fecha_ingreso < '" + fechafin + "' or k.fecha_egreso < '" +fechafin+ "')"
            # sql2 += " order by k.created_at"
            # cursor = connection.cursor()
            # cursor.execute(sql2)
            # row2 = cursor.fetchall()
            # entradat=0
            # salidat=0
            # if row2:
            #     for p2 in row2:
            #         if p2[0]:
            #             entradat=entradat+0
            #         else:
            #             entradat = entradat + float(p2[12])
            # 
            #         if p[0]:
            #             salidat = salidat+ +float(p2[12])
            # 
            # entradatotal=entradat+entrada
            # salidatotal=salidat+salida
            # saldo=entradatotal-salidatotal
            # html += '<td>' + str(saldo) + '</td>'
            # try:
            #     pb = ProductoEnBodega.objects.filter(producto_id=str(p[14])).filter(bodega_id=str(p[15]))
            # except ProductoEnBodega.DoesNotExist:
            #     pb = None
            # 
            # if pb:
            #     html += '<td>' + str(pb[0].cantidad) + '</td>'
            # else:
            #     html += '<td>0</td>'


	    #total_kit=float(p[4])*float(p[11])
	    #html += '<td>' + str(total_kit) + '</td>'

            html += '</tr>'
        html += '<tr><td colspan="5"><b>Total</b></td>'
        html += '<td><b>' + str(entrada) + '</b></td>'
        html += '<td><b>' + str(salida) + '</b></td>'
        html += '<td><b></b></td>'
        html += '</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404


def principalInventarioNuevo(request):
    cursor = connection.cursor();

    cursor.execute(
        "SELECT  distinct reunion.codigo,reunion.motivo,reunion.fecha,reunion.tiempo_respuesta,proforma.codigo, proforma.fecha FROM reunion LEFT JOIN proforma ON proforma.reunion_codigo=reunion.codigo");
    row = cursor.fetchall();

    return render_to_response('principal/principal_inventario_nuevo.html', {'row': row}, RequestContext(request))
def reporteManoObra(request):
    return render_to_response('ordenproduccion/costo_horas_asignadas.html', {}, RequestContext(request))

@csrf_exempt
def obtenerManoObra(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')

        cursor = connection.cursor();
        
        cursor.execute("select distinct sdd.fecha,sdd.empleado,sdd.operacion_unitaria,sdd.hora_total,sdd.costo_hora,sdd.total,sd.id,sd.areas_id,a.descripcion,o.id,o.codigo,o.tipo,o.fecha,o.descripcion,o.detalle,o.cantidad from suborden_produccion_detalle sdd,suborden_produccion sd,orden_produccion o,areas a where sdd.suborden_produccion_id=sd.id and sd.orden_produccion_id=o.id and a.id=sd.areas_id and sdd.fecha>='" + fechainicial + "'and sdd.fecha<='" + fechafin + "'  order by o.codigo,o.tipo");
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead><tr>'
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        html+= '<th style="width:120px !important">Fecha</th>'
        html+= '<th style="width:120px !important">OP-OR</th>'
        html+= '<th style="width:100px !important">Descripcion</th>'
        html+= '<th style="width:150px !important">Unidades</th>'
        html+= '<th>Areas</th>'
        html+= '<th>Operario</th>'
        html+= '<th>Horas</th>'
        html+= '<th>Cto.Horas</th>'
        ##html+='<th>Proveedor</th>'
        ##html+='<th>Forma de Pago</th>'
       
        
        html+='</tr></thead>'
        html+='<tbody><tr>'
        
        for p in row:
           
            
            html += '<td style="text-align:center">' + str(p[0]) + '</td>'
            html += '<td style="text-align:center">' + str(p[10]) + '</td>'
            html += '<td>' + str(p[13].encode('utf8')) + '</td>'
            html += '<td>' + str(p[15]) + '</td>'
            html += '<td>' + str(p[8].encode('utf8')) + '</td>'
            html += '<td>' + str(p[1].encode('utf8')) + '</td>'
            html += '<td>' + str(p[3]) + '</td>'
            html += '<td>' + str(p[5]) + '</td>'

            html += '</tr>'
                    
             
            
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404



def reporteCostoMateriales(request):
    return render_to_response('ordenproduccion/costo_materiales.html', {}, RequestContext(request))

@csrf_exempt
def obtenerCostoMateriales(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')

        cursor = connection.cursor();
        
        cursor.execute("select distinct sdd.fecha,sdd.material,sdd.producto_id,p.unidad,sdd.costo,sdd.total,sd.id,sd.areas_id,a.descripcion,o.id,o.codigo,o.tipo,o.fecha,o.descripcion,o.detalle,sdd.cantidad from orden_produccion_receta sdd,suborden_produccion sd,orden_produccion o,areas a,producto p where p.producto_id=sdd.producto_id and sdd.suborden_produccion_id=sd.id and sd.orden_produccion_id=o.id and a.id=sd.areas_id and sdd.fecha>='" + fechainicial + "'and sdd.fecha<='" + fechafin + "'  order by o.codigo,o.tipo");
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead><tr>'
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        html+= '<th style="width:120px !important">Fecha</th>'
        html+= '<th style="width:120px !important">OP-OR</th>'
        html+= '<th>Areas</th>'
        html+= '<th style="width:300px !important">Produccion</th>'
        html+= '<th style="width:100px !important">Material</th>'
        html+= '<th>Unid</th>'
        html+= '<th>Cantidad</th>'
        html+= '<th>Costo Unid.</th>'
        html+= '<th>Total</th>'
        ##html+='<th>Proveedor</th>'
        ##html+='<th>Forma de Pago</th>'
       
        
        html+='</tr></thead>'
        html+='<tbody><tr>'
        
        for p in row:
           
            
            html += '<td style="text-align:center">' + str(p[0]) + '</td>'
            html += '<td style="text-align:center">' + str(p[10]) + '</td>'
            html += '<td>' + str(p[8].encode('utf8')) + '</td>'
            html += '<td>' + str(p[13].encode('utf8')) + '</td>'
            html += '<td>' + str(p[1].encode('utf8')) + '</td>'
            html += '<td>' + str(p[3]) + '</td>'
            html += '<td>' + str(p[15]) + '</td>'
            html += '<td>' + str(p[4]) + '</td>'
            html += '<td>' + str(p[5]) + '</td>'

            html += '</tr>'
                    
             
            
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404

def reporteValoresReaudados(request):

    return render_to_response('transacciones/valores_recaudados.html', {}, RequestContext(request))

@csrf_exempt
def obtenerValoresRecaudados(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        qle="select m.cliente_id,sum(m.monto),c.codigo_cliente,c.nombre_cliente from movimiento m LEFT JOIN cliente c ON c.id_cliente=m.cliente_id where m.activo is True and m.fecha_emision>='" + fechainicial + "' and m.fecha_emision<='" + fechafin + "'  group by m.cliente_id,c.codigo_cliente,c.nombre_clienteselect m.cliente_id,sum(m.monto) from movimiento m where m.activo is True and m.fecha_emision>='" + fechainicial + "' and m.fecha_emision<='" + fechafin + "'  group by cliente_id "
        print qle
        print "-----------------------"

        cursor = connection.cursor();
        cursor.execute("select m.cliente_id,sum(m.monto),c.codigo_cliente,c.nombre_cliente from movimiento m LEFT JOIN cliente c ON c.id_cliente=m.cliente_id where m.activo is True and m.fecha_emision>='" + fechainicial + "' and m.fecha_emision<='" + fechafin + "'  group by m.cliente_id,c.codigo_cliente,c.nombre_cliente ");
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead><tr><th>TIPO</th>'
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        
        #html+='<th>Forma de Pago</th>'
        html+= '<th>Fecha</th>'
        html+='<th colspan="2">Aplica</th>'
        #html+='<th></th>'
        
        html+='<th>Valor</th>'
        html+='<th>Concepto</th>'
        html+='<tbody>'
        
        for p in row:
            
        
            if p[0]:
                html+='<tr><td colspan="6"><b>'+str(p[2])+' '+str(p[3].encode('utf8'))+'<b></td></tr>'
                cursor = connection.cursor();
                sql3="select da.abono,da.anulado,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,dv.establecimiento,dv.punto_emision,dv.secuencial,pr.codigo,pr.puntos_venta_id,pr.abreviatura_codigo,dv.id,pr.id from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id LEFT JOIN documento_venta dv ON dv.id=da.documento_venta_id LEFT JOIN proforma pr ON pr.id=da.proforma_id where m.cliente_id="+ str(p[0])+" and da.anulado is False and m.activo is True and m.fecha_emision>='" + fechainicial + "' and m.fecha_emision<='" + fechafin + "' order by m.fecha_emision"
                print sql3
                cursor.execute(sql3);
                row3 = cursor.fetchall()
                saldo=0
               
                for p3 in row3:
                    if p3[0]:
                        html += '<tr>'
                        html += '<td>'+str(p3[11].encode('utf8'))+'</td>'
                        
                        #html += '<td></td>'
                        #html += '<td>'+str(p3[13])+'</td>'
                        html += '<td>'+str(p3[2])+'</td>'
                        if p3[18]:
                            html += '<td>FA</td>'
                            html += '<td>'+str(p3[12])+'-'+str(p3[13])+'-'+str(p3[14])+'</td>'
                        else:
                            html += '<td>PR</td>'
                            html += '<td>'+str(p3[17])+' '+str(p3[15])+'</td>'
                            
                            
                        html += '<td>'+str(p3[0])+'</td>'
                        #html += '<td></td>'
                        #credito
                        html += '<td>'+str(p3[6])+'</td>'
                        total_a=0
                        
                        
                        html += '</tr>'
                    
                    print 'hrl'
             
                html+='<tr><td colspan="6"><b>TOTAL '+str(p[1])+'</b></td></tr>'
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404

#FACTURAS EMITIDAS
def reportePorClientesDiarioVentas(request):
    cliente = Cliente.objects.all()
    puntos_venta= PuntosVenta.objects.all()
    vendedor = Vendedor.objects.all()

    return render_to_response('transacciones/clientes_diario_ventas.html', {'cliente': cliente,'puntos_venta': puntos_venta,'vendedor': vendedor}, RequestContext(request))

@csrf_exempt
def obtenerClientesDiarioVentas(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cliente = request.POST.get('cliente')
        punto = request.POST.get('punto')
        vendedor = request.POST.get('vendedor')
        no_factura = request.POST.get('no_factura')
        #cliente_s=Cliente.objects.get(id_cliente=cliente)
        sql="SELECT  distinct dv.id,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0,dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,c.codigo_cliente,c.ruc,p.nombre,dv.activo,r.codigo_razon_social,r.nombre,r.ruc FROM documento_venta dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id LEFT JOIN puntos_venta p ON dv.punto_venta_id=p.id  LEFT JOIN razon_social r ON r.id=dv.razon_social_id where dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' "
        if cliente and  cliente!= '0' :
            sql+=" and dv.cliente_id=" + cliente

        
        if punto!= '' and  punto!= '0':
            sql+=" and dv.punto_venta_id=" + punto
        if vendedor!= '' and vendedor!= '0':
            sql+=" and dv.vendedor_id=" + vendedor
        if no_factura!= '':
            sql +=" and dv.secuencial like '%" +no_factura+ "%'"
            
        
        sql+=" order by  dv.fecha_emision"
        print sql

        cursor = connection.cursor();
        cursor.execute(sql);
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0
        total_debito=0
        total_credito=0
        total_saldo=0
        
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info">'
        html+='<thead>'
        html+='<tr><td colspan="11" style="text-align:center"><b>REPORTE DE DIARIO DE VENTAS </b></td></tr>'
        html+='<tr><td colspan="3"><b>DESDE</b></td><td colspan="3">'+str(fechainicial)+'</td><td colspan="3"><b>HASTA</b></td><td colspan="2">'+str(fechafin)+'</td></tr>'
        html+='<tr><th>FECHA</th><th>Punto Venta</th>'
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        html+='<th>Cliente</th>'
        html+= '<th>RUC</th>'
        html+='<th>Razon Social</th>'
        html+= '<th>RUC</th>'
        html+='<th>No. Factura</th><th>Subtotal</th><th>Descuento</th><th>Base Iva</th><th>Total</th></tr></thead>'
        html+='<tbody><tr>'
        subtotalf=0
        ivaf=0
        descuentof=0
        
        for p in row:
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
            

            if p[1]:
                html += '<td style="text-align:center">' + str(p[1]) +'</td>'
            else:
                html += '<td></td>'
            if p[18]:
                html += '<td style="text-align:center">' + str(p[18].encode('utf8')) +'</td>'
            else:
                html += '<td></td>'
                
            if p[15]:
                html += '<td style="text-align:right">' + str(p[15].encode('utf8')) +'</td>'
            else:
                html += '<td></td>'
            
            
           
            if p[17]:
                html += '<td style="text-align:left">&nbsp;' + str(p[17].encode('utf8')) +'&nbsp;</td>'
            else:
                html += '<td></td>'
            
            if p[21]:
                html += '<td style="text-align:center">' + str(p[21].encode('utf8')) +'</td>'
            else:
                html += '<td></td>'
                
            if p[22]:
                html += '<td style="text-align:left">&nbsp;' + str(p[22].encode('utf8')) +'</td>'
            else:
                html += '<td></td>'
            
            
            html += '<td style="text-align:center">' + str(factura) + '</td>'
             
            if p[19]:
                html += '<td style="text-align:right">' + str("%0.2f" % p[12]).replace('.', ',') + '</td>'
                
                html += '<td style="text-align:right">' + str("%0.2f" % p[13]).replace('.', ',') + '</td>'
                html += '<td style="text-align:right">' + str("%0.2f" % p[10]).replace('.', ',') + '</td>'
                if p[12]:
                    
                    subtotalf=subtotalf+p[12]
                if p[13]:
                    
                    descuentof=descuentof+p[13]
                if p[10]:
                    
                    ivaf=ivaf+p[10]
                
                
                
               
                
                if p[14]:
                    
                    totalf=p[14]
                else:
                    
                    totalf=0
                
                total_debito=total_debito+totalf
                html += '<td style="text-align:right">' + str("%0.2f" % totalf).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0,00</td>'
                html += '<td style="text-align:right">0,00</td>'
                html += '<td style="text-align:right">0,00</td>'
                html += '<td style="text-align:right">0,00</td>'
             
            html += '</tr>'

        html+='</tbody>'
        html+='<tfoot><tr><td></td><td></td><td></td><td></td><td></td><td></td><td style="text-align:right"></td><td style="text-align:right">'+str("%0.2f" % subtotalf).replace('.', ',')+'</td><td style="text-align:right">'+str("%0.2f" % descuentof).replace('.', ',')+'</td><td style="text-align:right">'+str("%0.2f" % ivaf).replace('.', ',')+'</td><td style="text-align:right">'+str("%0.2f" % total_debito).replace('.', ',')+'</td></tr></tfoot>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404
def reportePorDiarioRecaudaciones(request):
    cliente = Cliente.objects.all()
    tipos= TipoDocumento.objects.all()
    puntos_venta= PuntosVenta.objects.all()
    vendedor = Vendedor.objects.all()

    return render_to_response('transacciones/diario_recaudaciones.html', {'cliente': cliente,'puntos_venta': puntos_venta,'tipos': tipos}, RequestContext(request))



@csrf_exempt
def obtenerDiarioRecaudaciones(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cliente = request.POST.get('cliente')
        tipos = request.POST.get('tipos')
        
        
        qle=" select m.id,m.tipo_documento_id,m.fecha_emision,m.paguese_a,m.numero_cheque,m.descripcion,m.numero_comprobante,m.monto,m.monto_cheque,m.activo,c.nombre_cliente,t.descripcion from movimiento m LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id LEFT JOIN cliente c ON c.id_cliente=m.cliente_id where m.activo is True and m.tipo_anticipo_id=2"
        if fechainicial:
            qle += " and m.fecha_emision>='"+str(fechainicial)+"'"
        if fechafin:
            qle += " and m.fecha_emision<='"+str(fechafin)+"' "
        if tipos:
            qle += " and m.tipo_documento_id= "+str(tipos)
            
        cliente_s=''
        if cliente!="0" and cliente!=""  :
            qle+=" and m.cliente_id="+cliente
            
            cliente_s=Cliente.objects.get(id_cliente=cliente)
            
        if cliente_s:
            nombre_cliente=cliente_s.nombre_cliente
        else:
            nombre_cliente=''
            

        cursor = connection.cursor()
        cursor.execute(qle)
        row = cursor.fetchall()
        total = 0
        subtotal = 0
        iva = 0
        total_debito=0
        total_credito=0
        total_saldo=0
        
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info">'
        html+='<thead>'
        html+='<tr><td colspan="7" style="text-align:center"><b>REPORTE DE DIARIO DE RECAUDACIONES'+str(nombre_cliente.encode('utf8'))+'</b></td></tr>'
        html+='<tr><td colspan="2"><b>DESDE</b></td><td colspan="2">'+str(fechainicial)+'</td><td colspan="2"><b>HASTA</b></td><td colspan="1">'+str(fechafin)+'</td></tr>'
        html+='<tr><th>Tipo</th>'
        html+='<th>Persona</th>'
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        
        html+='<th>Numero</th>'
        html+= '<th>Fecha</th>'
        html+='<th>Aplica</th><th>Valor</th><th>Concepto</th></tr></thead>'
        html+='<tbody>'
        
        for p in row:
            
            

            
            cursor = connection.cursor()
            sqlr3=" select d.id,d.documento_venta_id,d.movimiento_id,d.abono,d.proforma_id,d.anulado,dv.establecimiento,dv.punto_emision,dv.secuencial,p.codigo,p.abreviatura_codigo from documento_abono_venta d LEFT JOIN documento_venta dv ON dv.id=d.documento_venta_id LEFT JOIN proforma p ON p.id=d.proforma_id where d.anulado is False and d.movimiento_id="+str(p[0])
            cursor.execute(sqlr3);
            rowr3 = cursor.fetchall()
            if rowr3:
                
                for pr2 in rowr3:
                    html+='<tr>'
                    if p[11]:
                        html += '<td style="text-align:center">' + str(p[11].encode('utf8')) +'</td>'
                    else:
                        html += '<td></td>'
                    if p[3]:
                        html += '<td style="text-align:center">' + str(p[3].encode('utf8')) +'</td>'
                    else:
                        html += '<td></td>'
                    html += '<td style="text-align:center">' + str(p[4].encode('utf8')) +'</td>'
                    html += '<td style="text-align:center">' + str(p[2]) +'</td>'
                    if pr2[1]:
                        
                        html += '<td style="text-align:center">FA ' + str(pr2[6]) +'-'+ str(pr2[7])+'-'+ str(pr2[8]) +'</td>'
                        
                    else:
                        html += '<td style="text-align:center">PR ' + str(pr2[10]) +' '+ str(pr2[9])+'</td>'
                    html += '<td style="text-align:center">' + str(pr2[3]) +'</td>'
                    
                    html += '<td style="text-align:center">' + str(p[5].encode('utf8')) +'</td>'
                    html+='</tr>'
                        
                    
            else:
                html+='<tr>'
                if p[11]:
                    html += '<td style="text-align:center">' + str(p[11].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
                    
                if p[3]:
                    html += '<td style="text-align:center">' + str(p[3].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
                html += '<td style="text-align:center">' + str(p[4].encode('utf8')) +'</td>'
                html += '<td style="text-align:center">' + str(p[2]) +'</td>'
                html += '<td style="text-align:center"></td>'
                html += '<td style="text-align:center">' + str(p[7]) +'</td>'
                html += '<td style="text-align:center">' + str(p[5].encode('utf8')) +'</td>'
                html+='</tr>'
            
           
            
            
             
            html += '</tr>'
            #RETENCIONES SUMA
              
   
                    
                    
            
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404



def reportePorEstadoCuentaFacturasClientesSinProforma(request):
    cliente = Cliente.objects.all().order_by('codigo_cliente')

    return render_to_response('transacciones/estado_cuenta_facturas_clientes_sin_proforma.html', {'cliente': cliente}, RequestContext(request))

@csrf_exempt
def obtenerEstadoCuentaFacturasClientesSinProforma(request):
    #111
    if request.method == 'POST':
        fechaini = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cliente0 = request.POST.get('cliente')
        cliente_hasta0 = request.POST.get('cliente_hasta')
        cliente_s=Cliente.objects.get(id_cliente=cliente0)
        total_saldo_acum=0
        if cliente_s:
            nombre_cliente=cliente_s.codigo_cliente+' -'+cliente_s.nombre_cliente
            codigo_cliente=cliente_s.codigo_cliente
        else:
            nombre_cliente=''
        
        cliente_h=Cliente.objects.get(id_cliente=cliente_hasta0)
        if cliente_h:
            nombre_cliente_h=cliente_h.codigo_cliente+' -'+cliente_h.nombre_cliente
            codigo_cliente_h=cliente_h.codigo_cliente
        else:
            nombre_cliente_h=''

        cursor = connection.cursor()
        
        total = 0
        subtotal = 0
        iva = 0
        total_debito=0
        total_credito=0
        total_saldo=0
        
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        #style="width:100%"
        html ='<table id="tabla" class="table table-bordered" aria-describedby="data-table_info">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="8" style="text-align:center"><b>ESTADO DE CUENTA DEL CLIENTE SIN PROFORMA <br > DESDE '+str(nombre_cliente.encode('utf8'))+'    HASTA '+str(nombre_cliente_h.encode('utf8'))+'</b></td></tr>'
        html+='<tr><td colspan="1"><b>DESDE</b></td><td colspan="1">'+str(fechaini)+'</td><td colspan="1"><b>HASTA</b></td><td colspan="1">'+str(fechafin)+'</td><td colspan="4"></td></tr>'
        html+='</thead>'
        html+='<tbody>'

        cursor.execute('select id_cliente,codigo_cliente,nombre_cliente from cliente '
            ' where codigo_cliente::int>=%s '
            'and  codigo_cliente::int<=%s '
            'order by codigo_cliente ', (int(codigo_cliente),int(codigo_cliente_h)))

        rowc = cursor.fetchall();
        for pc in rowc:
            DeudaTot = 0
            PagosTot = 0
            SaldoTot = 0
            PagoParc = 0
            PagosmId = ''

            cliente=pc[0]
            cursor1 = connection.cursor()

            #Facturas
            lcSql = "SELECT  distinct dv.id,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0,dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,c.codigo_cliente,c.ruc,drv.id,dv.activo,dv.proforma_id "
            lcSql += "FROM documento_venta dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
            lcSql += "LEFT JOIN documento_retencion_venta drv ON drv.documento_venta_id=dv.id and drv.anulado is not True "
            lcSql += "where dv.activo is not False and dv.fecha_emision>='" + fechaini + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id="+str(cliente)

            cursor1.execute(lcSql);
            row = cursor1.fetchall();

            sql0="SELECT  distinct dv.id,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0,dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,c.codigo_cliente,c.ruc,drv.id,dv.activo,dv.proforma_id FROM documento_venta dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id LEFT JOIN documento_retencion_venta drv ON drv.documento_venta_id=dv.id and drv.anulado is not True  where dv.activo is not False and dv.fecha_emision>='" + fechaini + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id="+str(cliente)

            #Proformas
            cursor2 = connection.cursor()
            sql2="SELECT  distinct dv.id,dv.fecha,dv.abreviatura_codigo,dv.codigo,dv.puntos_venta_id,dv.vendedor_id,dv.observacion,dv.iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,c.codigo_cliente,c.ruc,dv.aprobada "
            sql2 +="FROM proforma dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
            sql2 += "where dv.fecha>='" + fechaini + "'and dv.fecha<='" + fechafin + "' and dv.id NOT IN (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL) "
            sql2 += "and dv.aprobada is True and dv.cliente_id=" + str(cliente)

            cursor2.execute(sql2)
            row21 = cursor2.fetchall()

            #PROFORMAS QUE FUERON ABONADAS ANTES DE CONVERTIRSE EN FACTURA
            cursor22 = connection.cursor()
            sql22="SELECT  distinct dv.id,dv.fecha,dv.abreviatura_codigo,dv.codigo,dv.puntos_venta_id,dv.vendedor_id,dv.observacion,dv.iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,c.codigo_cliente,c.ruc,dv.aprobada FROM proforma dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id where dv.fecha>='" + fechaini + "' and dv.fecha<='" + fechafin + "' and dv.id  IN(select da.proforma_id from documento_abono_venta da  where da.anulado is not True and da.documento_venta_id is null) and dv.id in (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL) and dv.aprobada is True and dv.cliente_id="+str(cliente)
            cursor22.execute(sql22)
            row22 = cursor22.fetchall()
            
            cursor3 = connection.cursor()
            sql5="select distinct cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante "
            sql5 +="from cheques_protestados cp,movimiento m,documento_abono_venta da,documento_venta dv "
            sql5 += "where cp.anulado is not True and m.id=cp.movimiento_id and da.movimiento_id=m.id and da.documento_venta_id=dv.id and dv.fecha_emision>='" + fechaini + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id="+str(cliente)

            cursor3.execute(sql5);
            chequesp = cursor3.fetchall()
            
            cursor4 = connection.cursor()
            sql6="select distinct cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante "
            sql6 +="from cheques_protestados cp,movimiento m,documento_abono_venta da,proforma dv "
            sql6 +="where cp.anulado is not True and m.id=cp.movimiento_id and da.movimiento_id=m.id and da.proforma_id=dv.id and da.documento_venta_id is null and dv.fecha>='" + fechaini + "' and dv.fecha<='" + fechafin + "' and dv.cliente_id="+str(cliente)
            cursor4.execute(sql6)
            chequespr = cursor4.fetchall()

            if len(row)>0 or len(row21)>0  or len(chequesp)>0  or len(chequespr)>0 :
                html+='<tr style="background-color: #EBF5FB"><td colspan="8"><h5><b>'+str(pc[1])+'-'+str(pc[2].encode('utf8'))+'</b></h5></td></tr>'
                html+='<tr style="background-color: #EEEEEE"><th>Tipo</th>'
                html+='<th style="width:150px;">Numero Doc</th>'
                html+='<th style="width:150px;">Fecha Trx</th>'
                html+='<th>Debito</th><th>Credito</th><th>Saldo</th><th>Saldo Cuenta</th><th>Concepto</th></tr>'
                total_saldo_por_cliente=0
                total_debito_por_cliente=0
                total_credito_por_cliente=0
                totalxCliente=0

            for p in row:
                html += '<tr>'
                html += '<td><b>&nbsp;Facturas</b></td>'

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
                html += '<td >' + str(factura) + '</td>'
    
                if p[1]:
                    html += '<td style="text-align:center">' + str(p[1]) +'</td>'
                else:
                    html += '<td></td>'

                if p[14]:
                    totalf=p[14]
                else:
                    totalf=0
                
                DeudaTot = float(DeudaTot) + float(totalf)
                SaldoTot = float(SaldoTot) + float(totalf)
                total_debito=total_debito+totalf
                total_debito_por_cliente=total_debito_por_cliente+totalf
                html += '<td style="text-align:right">' + str("%0.2f" % totalf).replace('.', ',')  + '</td>'
                html += '<td style="text-align:right">0,00</td>'
                html += '<td style="text-align:right">' + str("%0.2f" % totalf).replace('.', ',')  + '</td>'
                html += '<td style="text-align:right">' + str("%0.2f" % SaldoTot).replace('.', ',') + '</td>'
                html += '<td style="text-align:left">'+str(p[5].encode('utf8'))+'</td>'
                 
                html += '</tr>'
                #RETENCIONES SUMA
                  
                if p[0]:
                    saldo=0
                    cursor = connection.cursor()
                    sqlr3="select sum(drdv.valor_retenido),drv.id,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id from documento_retencion_venta drv,documento_retencion_detalle_venta drdv where drv.id=drdv.documento_retencion_venta_id and drv.documento_venta_id="+ str(p[0])+" and drv.anulado is not True group by drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id"
                    print sqlr3
                    cursor.execute(sqlr3);
                    rowr3 = cursor.fetchall()
                    retencion=0
                    retencion1=0
                    for pr2 in rowr3:
                        
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
                        html += '<td><b>&nbsp;Retenciones</b></td>'
                        html+='<td style="text-align:left">'+str(retencion_cod)+'</td>'
                        html+='<td style="text-align:center">'+str(pr2[5])+'</td>'
                        html+='<td style="text-align:right">0,00</td>'
                        
                        
                        if pr2[0]:
                            saldo=Decimal(saldo)+Decimal(pr2[0])
                            PagosTot = float(PagosTot) + float(pr2[0])
                            PagoParc = float(pr2[0])

                        SaldoTot = float(SaldoTot) - float(PagoParc)
                        total_a=float(totalf)-float(saldo)
                        total_credito=total_credito+float(pr2[0])
                        total_credito_por_cliente=total_credito_por_cliente+float(pr2[0])
                        html+='<td style="text-align:right">'+str("%0.2f" % pr2[0]).replace('.', ',')+'</td>'
                        html+='<td style="text-align:right">'+str("%0.2f" % total_a).replace('.', ',') +'</td>'
                        html+='<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
                        html+='<td style="text-align:left">'+str(pr2[6].encode('utf8'))+'</td>'
                        html+='</tr>'
                    cursor = connection.cursor();
                    sql3 = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,"
                    sql3 += "m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id "
                    sql3 += "from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                    sql3 += "where da.anulado is not True and da.documento_venta_id="+ str(p[0])+" order by m.fecha_emision"

                    #print sql3
                    cursor.execute(sql3);
                    row3 = cursor.fetchall()
                    
                    for p3 in row3:
                        html += '<tr>'
                        html += '<td><b>&nbsp;'+str(p3[13].encode('utf8'))+'</b></td>'
                        html += '<td>'+str(p3[9])+'</td>'
                        html += '<td style="text-align:center">'+str(p3[4])+'</td>'
                        html += '<td style="text-align:right">0,00</td>'
                        #credito
                        html += '<td style="text-align:right">'+str("%0.2f" % p3[0]).replace('.', ',')+'</td>'
                        total_a=0
                        if len(PagosmId) > 0:
                            if p3[14] != 'None':
                                PagosmId += ',' + str(p3[14])
                        else:
                            if p3[12] != 'None':
                                PagosmId += str(p3[14])

                        if p[11]==True:
                            html += '<td style="text-align:right">0,00</td>'
                            estadof='ANULADO'
                        else:                        
                            saldo=saldo+p3[0]
                            PagosTot = float(PagosTot) + float(p3[0])
                            PagoParc = float(p3[0])
                            total_a=float(totalf)-float(saldo)
                            html += '<td style="text-align:right">'+str("%0.2f" % total_a).replace('.', ',')+'</td>'
                            estadof='ACTIVO'
                            total_credito=total_credito+float(p3[0])
                            total_credito_por_cliente=total_credito_por_cliente+float(p3[0])

                        SaldoTot = float(SaldoTot) - float(PagoParc)
                        html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',',') + '</b></td>'
                        html += '<td style="text-align:left">'+str(p3[8].encode('utf8'))+'</td>'
                        
                        html += '</tr>'
                        
                    ##NOTAS DE CREDITO
                    cursor = connection.cursor();
                    sql4="select distinct da.total,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion from movimiento_nota_credito da LEFT JOIN movimiento m ON m.id=da.movimiento_id and m.activo is True LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.documento_venta_id="+ str(p[0])+" order by m.fecha_emision"
                    #print sql4
                    cursor.execute(sql4);
                    row4 = cursor.fetchall()
                    for p4 in row4:
                        html += '<tr>'
                        html += '<td>'+str(p4[13].encode('utf8'))+'</td>'
                        html += '<td>'+str(p4[9])+'</td>'
                        html += '<td>'+str(p4[4])+'</td>'
                        html += '<td style="text-align:right">0,00</td>'
                        html += '<td style="text-align:right">'+str("%2.2f" % p4[0]).replace('.', ',')+'</td>'
                        
                        total_a=0
                            
                        if p[11]==True:
                            html += '<td></td>'
                            estadof='ANULADO'
                        else:                        
                            saldo=saldo+p4[0]
                            PagosTot = PagosTot + float(p4[0])
                            PagoParc = float(p4[0])
                            total_a=float(totalf)-float(saldo)
                            html += '<td style="text-align:right">'+str("%2.2f" % total_a).replace('.', ',')+'</td>'
                            estadof='ACTIVO'
                            total_credito=total_credito+float(p4[0])
                            total_credito_por_cliente=total_credito_por_cliente+float(p4[0])

                        SaldoTot = float(SaldoTot) - float(PagoParc)
                        html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',',') + '</b></td>'
                        html += '<td style="text-align:left">'+str(p4[8].encode('utf8'))+'</td>'
                        html += '</tr>'

            if row21:
                html += '<tr><td colspan="8" style="background-color: #F1948A"><b>**Abonos a proformas</b></td></tr>'
            for p21 in row21:
                proforma=''
                if p21[1]:
                    proforma+=''+str(p21[2]) +'-'
                else:
                    proforma+='-'

                if p21[2]:
                    proforma+=''+str(p21[3]) +'-'
                else:
                    proforma+='-'

                totalp=0
                if p21[0]:
                    cursor = connection.cursor();
                    lcSql="select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id "
                    lcSql+="from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                    lcSql+="where da.anulado is not True and da.proforma_id="+ str(p21[0])+"order by m.fecha_emision"

                    cursor.execute(sql4);
                    row4 = cursor.fetchall()
                    saldop=0
                    for p4 in row4:
                        html += '<tr>'
                        html += '<td><b>&nbsp;'+str(p4[13].encode('utf8'))+'</b></td>'
                        html += '<td>'+str(p4[9])+'</td>'
                        html += '<td style="text-align:center">'+str(p4[4])+'</td>'
                        html += '<td style="text-align:right">0,00</td>'
                        #credito
                        if p4[0]:
                            PagoParc = float(p4[0])
                            PagosTot = PagosTot + float(p4[0])
                        html += '<td style="text-align:right">'+str("%0.2f" % p4[0]).replace('.', ',')+'</td>'
                        total_ap=0

                        SaldoTot = float(SaldoTot) - float(PagoParc)
                        saldop=saldop+p4[0]
                        total_ap=float(totalp)-float(saldop)
                        html += '<td style="text-align:right">'+str("%0.2f" % total_ap).replace('.', ',')+'</td>'
                        total_credito=total_credito+float(p4[0])
                        total_credito_por_cliente=total_credito_por_cliente+float(p4[0])

                        html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
                        html += '<td style="text-align:left">'+str(p4[8].encode('utf8'))+'</td>'
                        html += '</tr>'
                        
                        
            #CHEQUES PROTESTADOS
            saldocp=0
            total_cp=0
            
            if chequesp:
                for chp in chequesp:
                
                    html += '<tr>'
                    html += '<td>&nbsp;CH. PROTESTADO</td>'
                
                    html += '<td>'+str(chp[10])+'</td>'
                    html += '<td style="text-align:center">'+str(chp[1])+'</td>'
                    #html += '<td></td>'
                    html += '<td style="text-align:right">'+str("%0.2f" % chp[4]).replace('.', ',')+'</td>'
                    #credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_a=0
                    
                    saldocp=Decimal(saldocp)+Decimal(chp[4])
                    total_cp=Decimal(total_cp)+Decimal(saldocp)
                    total_debito=float(total_debito)+float(chp[4])
                    total_debito_por_cliente=float(total_debito_por_cliente)+float(chp[4])
                    html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'

                    html += '<td>'+str(chp[6].encode('utf8'))+'</td>'
                    
                    html += '</tr>'
                    html += '<tr>'
                    html += '<td>&nbsp;CH. PROTESTADO MULTA</td>'
                    html += '<td>'+str(chp[10])+'</td>'
                    html += '<td style="text-align:center">'+str(chp[1])+'</td>'
                    #html += '<td></td>'
                    html += '<td style="text-align:right">'+str("%0.2f" % chp[5]).replace('.', ',')+'</td>'
                    #credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_ac=0
                    
                    saldocp=Decimal(saldocp)+Decimal(chp[5])
                    total_cp=Decimal(total_cp)+Decimal(saldocp)
                    total_debito=float(total_debito)+float(chp[5])
                    total_debito_por_cliente=float(total_debito_por_cliente)+float(chp[5])
                    html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                    html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
                    html += '<td style="text-align:left">'+str(chp[6].encode('utf8'))+'</td>'
                    html += '</tr>'
                    
                    #Abono Cheques Protestados
                    cursor = connection.cursor();
                    sqlc3="select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_cheque da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.cheques_protestados_id="+ str(chp[0])+" order by m.fecha_emision"
                    print sqlc3
                    cursor.execute(sqlc3);
                    rowc3 = cursor.fetchall()
                    saldoabono=0
                    
                    for pc3 in rowc3:
                        html += '<tr>'
                        html += '<td>&nbsp;'+str(pc3[13].encode('utf8'))+'</td>'
                        html += '<td>'+str(pc3[9])+'</td>'
                        html += '<td style="text-align:center">'+str(pc3[4])+'</td>'
                        html += '<td></td>'
                        #credito
                        html += '<td style="text-align:right">'+str("%0.2f" % pc3[0]).replace('.', ',')+'</td>'
                        total_ch=0
                        
                        if pc3[1]==True:
                            html += '<td style="text-align:right">0,00</td>'
                            estadof='ANULADO'
                            
                        else:                        
                            saldoabono=saldoabono+pc3[0]
                            saldocp=float(saldocp)-float(saldoabono)
                            html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                            estadof='ACTIVO'
                            total_credito=total_credito+float(pc3[0])
                            total_credito_por_cliente=total_credito_por_cliente+float(pc3[0])

                        html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',',') + '</b></td>'
                        html += '<td style="text-align:left">'+str(pc3[8].encode('utf8'))+'</td>'
                        html += '</tr>'

            #FINAL DE CHEQUES PROTESTADOS
            #CHEQUES PROTESTADOS proformaas
            
            if chequespr:
                for chpr in chequespr:
                
                    html += '<tr>'
                    html += '<td>&nbsp;CH. PROTESTADO</td>'
                    html += '<td>'+str(chpr[10])+'</td>'
                    html += '<td style="text-align:center">'+str(chpr[1])+'</td>'
                    html += '<td style="text-align:right">'+str("%0.2f" % chpr[4]).replace('.', ',')+'</td>'
                    #credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_a=0
                    
                    saldocp=Decimal(saldocp)+Decimal(chpr[4])
                    total_cp=Decimal(total_cp)+Decimal(saldocp)
                    total_debito=float(total_debito)+float(chpr[4])
                    total_debito_por_cliente=float(total_debito_por_cliente)+float(chpr[4])
                    html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                    html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
                    html += '<td style="text-align:left">'+str(chpr[6].encode('utf8'))+'</td>'

                    html += '</tr>'
                    html += '<tr>'
                    html += '<td>&nbsp;CH. PROTESTADO MULTA</td>'
                    html += '<td>'+str(chpr[10])+'</td>'
                    html += '<td style="text-align:center">'+str(chpr[1])+'</td>'
                    html += '<td style="text-align:right">'+str("%0.2f" % chpr[5]).replace('.', ',')+'</td>'
                    #credito
                    html += '<td style="text-align:right">0,00</td>'
                    total_ac=0
                    
                    saldocp=Decimal(saldocp)+Decimal(chpr[5])
                    total_cp=Decimal(total_cp)+Decimal(saldocp)
                    total_debito=float(total_debito)+float(chpr[5])
                    total_debito_por_cliente=float(total_debito_por_cliente)+float(chpr[5])
                    html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                    html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
                    html += '<td style="text-align:left">'+str(chpr[6].encode('utf8'))+'</td>'
                    html += '</tr>'
                    
                    #Abono Cheques Protestados
                    cursor = connection.cursor();
                    sqlcp3="select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_cheque da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.cheques_protestados_id="+ str(chpr[0])+" order by m.fecha_emision"
                    print sqlcp3
                    cursor.execute(sqlcp3);
                    rowcp3 = cursor.fetchall()
                    saldoabono=0
                    
                    for pc3 in rowcp3:
                        html += '<tr>'
                        html += '<td>&nbsp;'+str(pc3[13].encode('utf8'))+'</td>'
                        html += '<td>'+str(pc3[9])+'</td>'
                        html += '<td style="text-align:center">'+str(pc3[4])+'</td>'
                        html += '<td></td>'
                        #credito
                        html += '<td style="text-align:right">'+str("%0.2f" % pc3[0]).replace('.', ',')+'</td>'
                        total_ch=0
                        
                        if pc3[1]==True:
                            html += '<td style="text-align:right">0,00</td>'
                            estadof='ANULADO'
                        else:                        
                            saldoabono=saldoabono+pc3[0]
                            saldocp=float(saldocp)-float(saldoabono)
                            html += '<td style="text-align:right">'+str("%0.2f" % saldocp).replace('.', ',')+'</td>'
                            estadof='ACTIVO'
                            total_credito=total_credito+float(pc3[0])
                            total_credito_por_cliente=total_credito_por_cliente+float(pc3[0])

                        html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',',') + '</b></td>'
                        html += '<td style="text-align:left">'+str(pc3[8].encode('utf8'))+'</td>'
                        html += '</tr>'



            #proformas hechas facturas abonos

            for p22 in row22:
                proforma=''
                if p22[1]:
                    proforma+=''+str(p22[2]) +'-'
                else:
                    proforma+='-'

                if p22[2]:
                    proforma+=''+str(p22[3]) +'-'
                else:
                    proforma+='-'
                totalp=0

                if p22[0]:
                    cursor = connection.cursor();
                    sql41="select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id "
                    sql41 += "from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id "
                    sql41 += "where da.documento_venta_id is null and  da.anulado is not True and m.asociado_cheques_protestados is not True and da.proforma_id="+ str(p22[0])

                    if len(PagosmId) > 0:
                        sql41 += " and m.id not in (" + PagosmId + ") "

                    sql41 += " order by m.fecha_emision"

                    cursor.execute(sql41);
                    row41 = cursor.fetchall()
                    saldop=0
                    if row41:
                        html += '<tr><td colspan="8" style="background-color: #F1948A"><b>Abonos a Proformas '+str(proforma)+' que se convirtieron en diferentes facturas </b></td></tr>'

                        for p4 in row41:
                            html += '<tr>'
                            html += '<td><b>&nbsp;'+str(p4[13].encode('utf8'))+'</b></td>'
                            html += '<td>'+str(p4[9])+'</td>'
                            html += '<td style="text-align:center">'+str(p4[4])+'</td>'
                            html += '<td style="text-align:right">0,00</td>'
                            #credito
                            html += '<td style="text-align:right">'+str("%0.2f" % p4[0]).replace('.', ',')+'</td>'
                            total_ap=0

                            if p4[0]:
                                PagoParc = float(p4[0])
                                PagosTot = PagosTot + float(p4[0])

                            SaldoTot = float(SaldoTot) - float(PagoParc)
                            saldop=saldop+p4[0]
                            total_ap=float(totalp)-float(saldop)
                            html += '<td style="text-align:right">'+str("%0.2f" % total_ap).replace('.', ',')+'</td>'
                            total_credito=total_credito+float(p4[0])
                            total_credito_por_cliente=total_credito_por_cliente+float(p4[0])

                            html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',',') + '</b></td>'
                            html += '<td style="text-align:left">'+str(p4[8].encode('utf8'))+'</td>'
                            html += '</tr>'

            if len(row)>0 or len(row21)>0  or len(chequesp)>0  or len(chequespr)>0 :
                total_saldo_por_cliente=float(total_debito_por_cliente)-float(total_credito_por_cliente)
                html+='<tr style="background-color: #EBF5FB"><td colspan="3"><b>Saldo Final Cliente</b></td><td style="text-align:right">'+str("%0.2f" % total_debito_por_cliente).replace('.', ',')+'</td><td style="text-align:right">'+str("%0.2f" % total_credito_por_cliente).replace('.', ',')+'</td><td style="text-align:right">'+str("%0.2f" % total_saldo_por_cliente).replace('.', ',')+'</td><td></td><td></td></tr>'
        #FINAL DE CHEQUES PROTESTADOS
        
        print 'hrl'
        total_saldo_acum=float(total_debito)-float(total_credito)
                    
            
        html+='</tbody>'
        html+='<tfoot style="background-color: #EEEEEE"><tr><td colspan="3"><b>Saldos Totales Clientes:</b></td><td style="text-align:right">'+str("%0.2f" % total_debito).replace('.', ',')+'</td><td style="text-align:right">'+str("%0.2f" % total_credito).replace('.', ',')+'</td><td style="text-align:right">'+str("%0.2f" % total_saldo_acum).replace('.', ',')+'</td><td></td><td></td></tr></tfoot>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404

#Quitar
# @csrf_exempt
# def obtenerEstadoCuentaFacturasClientesSinProforma(request):
#     #222
#     if request.method == 'POST':
#         fechaini = request.POST.get('fechainicial')
#         fechafin = request.POST.get('fechafin')
#         cliente0 = request.POST.get('cliente')
#         cliente_hasta0 = request.POST.get('cliente_hasta')
#         cliente_s = Cliente.objects.get(id_cliente=cliente0)
#         total_saldo_acum = 0
#         if cliente_s:
#             nombre_cliente = cliente_s.codigo_cliente + ' -' + cliente_s.nombre_cliente
#             codigo_cliente = cliente_s.codigo_cliente
#         else:
#             nombre_cliente = ''
#
#         cliente_h = Cliente.objects.get(id_cliente=cliente_hasta0)
#         if cliente_h:
#             nombre_cliente_h = cliente_h.codigo_cliente + ' -' + cliente_h.nombre_cliente
#             codigo_cliente_h = cliente_h.codigo_cliente
#         else:
#             nombre_cliente_h = ''
#
#         cursor = connection.cursor()
#
#         total = 0
#         subtotal = 0
#         iva = 0
#         total_debito = 0
#         total_credito = 0
#         total_saldo = 0
#
#         # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
#         # style="width:100%"
#         html = '<table id="tabla" class="table table-bordered" aria-describedby="data-table_info">'
#         html += '<thead style="background-color: #EEEEEE">'
#         html += '<tr><td colspan="8" style="text-align:center"><b>ESTADO DE CUENTA DEL CLIENTE SIN PROFORMA <br > DESDE ' + str(
#             nombre_cliente.encode('utf8')) + '    HASTA ' + str(nombre_cliente_h.encode('utf8')) + '</b></td></tr>'
#         html += '<tr><td colspan="1"><b>DESDE</b></td><td colspan="1">' + str(
#             fechaini) + '</td><td colspan="1"><b>HASTA</b></td><td colspan="1">' + str(
#             fechafin) + '</td><td colspan="4"></td></tr>'
#         html += '</thead>'
#         html += '<tbody>'
#
#         cursor.execute('select id_cliente,codigo_cliente,nombre_cliente from cliente '
#                        ' where codigo_cliente::int>=%s '
#                        'and  codigo_cliente::int<=%s '
#                        'order by codigo_cliente ', (int(codigo_cliente), int(codigo_cliente_h)))
#
#         rowc = cursor.fetchall();
#         for pc in rowc:
#             DeudaTot = 0
#             PagosTot = 0
#             SaldoTot = 0
#             PagoParc = 0
#
#             cliente = pc[0]
#             cursor1 = connection.cursor()
#
#             # Facturas
#             lcSql = "SELECT  distinct dv.id,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0,dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,c.codigo_cliente,c.ruc,drv.id,dv.activo,dv.proforma_id "
#             lcSql += "FROM documento_venta dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
#             lcSql += "LEFT JOIN documento_retencion_venta drv ON drv.documento_venta_id=dv.id and drv.anulado is not True "
#             lcSql += "where dv.activo is not False and dv.fecha_emision>='" + fechaini + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id=" + str(
#                 cliente)
#
#             cursor1.execute(lcSql);
#             row = cursor1.fetchall();
#
#             sql0 = "SELECT  distinct dv.id,dv.fecha_emision,dv.establecimiento,dv.punto_emision,dv.secuencial,dv.autorizacion,dv.descripcion,dv.base_iva_0,dv.valor_iva_0,dv.base_iva,dv.valor_iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.autorizacion,c.codigo_cliente,c.ruc,drv.id,dv.activo,dv.proforma_id FROM documento_venta dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id LEFT JOIN documento_retencion_venta drv ON drv.documento_venta_id=dv.id and drv.anulado is not True  where dv.activo is not False and dv.fecha_emision>='" + fechaini + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id=" + str(
#                 cliente)
#
#             # Proformas
#             cursor2 = connection.cursor()
#             sql2 = "SELECT  distinct dv.id,dv.fecha,dv.abreviatura_codigo,dv.codigo,dv.puntos_venta_id,dv.vendedor_id,dv.observacion,dv.iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,c.codigo_cliente,c.ruc,dv.aprobada "
#             sql2 += "FROM proforma dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id "
#             sql2 += "where dv.fecha>='" + fechaini + "'and dv.fecha<='" + fechafin + "' and dv.id NOT IN (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL) "
#             sql2 += "and dv.aprobada is True and dv.cliente_id=" + str(cliente)
#
#             cursor2.execute(sql2)
#             row21 = cursor2.fetchall()
#
#             # PROFORMAS QUE FUERON ABONADAS ANTES DE CONVERTIRSE EN FACTURA
#             cursor22 = connection.cursor()
#             sql22 = "SELECT  distinct dv.id,dv.fecha,dv.abreviatura_codigo,dv.codigo,dv.puntos_venta_id,dv.vendedor_id,dv.observacion,dv.iva,dv.porcentaje_iva,dv.subtotal,dv.descuento,dv.total,c.nombre_cliente,c.codigo_cliente,c.ruc,dv.aprobada FROM proforma dv LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id where dv.fecha>='" + fechaini + "' and dv.fecha<='" + fechafin + "' and dv.id  IN(select da.proforma_id from documento_abono_venta da  where da.anulado is not True and da.documento_venta_id is null) and dv.id in (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL) and dv.aprobada is True and dv.cliente_id=" + str(
#                 cliente)
#             cursor22.execute(sql22)
#             row22 = cursor22.fetchall()
#
#             cursor3 = connection.cursor()
#             sql5 = "select distinct cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante "
#             sql5 += "from cheques_protestados cp,movimiento m,documento_abono_venta da,documento_venta dv "
#             sql5 += "where cp.anulado is not True and m.id=cp.movimiento_id and da.movimiento_id=m.id and da.documento_venta_id=dv.id and dv.fecha_emision>='" + fechaini + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id=" + str(
#                 cliente)
#
#             cursor3.execute(sql5);
#             chequesp = cursor3.fetchall()
#
#             cursor4 = connection.cursor()
#             sql6 = "select distinct cp.id,cp.fecha_emision,cp.numero_cheque,cp.fecha_cheque,cp.valor_cheque,cp.valor_multa,cp.descripcion,cp.cliente_id,cp.banco_id,cp.movimiento_id,m.numero_comprobante "
#             sql6 += "from cheques_protestados cp,movimiento m,documento_abono_venta da,proforma dv "
#             sql6 += "where cp.anulado is not True and m.id=cp.movimiento_id and da.movimiento_id=m.id and da.proforma_id=dv.id and da.documento_venta_id is null and dv.fecha>='" + fechaini + "' and dv.fecha<='" + fechafin + "' and dv.cliente_id=" + str(
#                 cliente)
#             cursor4.execute(sql6)
#             chequespr = cursor4.fetchall()
#
#             if len(row) > 0 or len(row21) > 0 or len(chequesp) > 0 or len(chequespr) > 0:
#                 html += '<tr style="background-color: #EBF5FB"><td colspan="8"><h5><b>' + str(pc[1]) + '-' + str(
#                     pc[2].encode('utf8')) + '</b></h5></td></tr>'
#                 html += '<tr style="background-color: #EEEEEE"><th>Tipo</th>'
#                 html += '<th style="width:150px;">Numero Doc</th>'
#                 html += '<th style="width:150px;">Fecha Trx</th>'
#                 html += '<th>Debito</th><th>Credito</th><th>Saldo</th><th>Saldo Cuenta</th><th>Concepto</th></tr>'
#                 total_saldo_por_cliente = 0
#                 total_debito_por_cliente = 0
#                 total_credito_por_cliente = 0
#                 totalxCliente = 0
#
#             for p in row:
#                 html += '<tr>'
#                 html += '<td><b>&nbsp;Facturas</b></td>'
#
#                 factura = ''
#                 if p[2]:
#                     factura += '' + str(p[2]) + '-'
#                 else:
#                     factura += '-'
#
#                 if p[3]:
#                     factura += '' + str(p[3]) + '-'
#                 else:
#                     factura += '-'
#
#                 if p[4]:
#                     factura += '' + str(p[4])
#                 else:
#                     factura += ''
#                 html += '<td >' + str(factura) + '</td>'
#
#                 if p[1]:
#                     html += '<td style="text-align:center">' + str(p[1]) + '</td>'
#                 else:
#                     html += '<td></td>'
#
#                 if p[14]:
#                     totalf = p[14]
#                 else:
#                     totalf = 0
#
#                 DeudaTot = float(DeudaTot) + float(totalf)
#                 SaldoTot = float(SaldoTot) + float(totalf)
#                 total_debito = total_debito + totalf
#                 total_debito_por_cliente = total_debito_por_cliente + totalf
#                 html += '<td style="text-align:right">' + str("%0.2f" % totalf).replace('.', ',') + '</td>'
#                 html += '<td style="text-align:right">0,00</td>'
#                 html += '<td style="text-align:right">' + str("%0.2f" % totalf).replace('.', ',') + '</td>'
#                 html += '<td style="text-align:right">' + str("%0.2f" % SaldoTot).replace('.', ',') + '</td>'
#                 html += '<td style="text-align:left">' + str(p[5].encode('utf8')) + '</td>'
#
#                 html += '</tr>'
#                 # RETENCIONES SUMA
#
#                 if p[0]:
#                     saldo = 0
#                     cursor = connection.cursor()
#                     sqlr3 = "select sum(drdv.valor_retenido),drv.id,drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id from documento_retencion_venta drv,documento_retencion_detalle_venta drdv where drv.id=drdv.documento_retencion_venta_id and drv.documento_venta_id=" + str(
#                         p[
#                             0]) + " and drv.anulado is not True group by drv.establecimiento,drv.punto_emision,drv.secuencial,drv.fecha_emision,drv.descripcion,drv.id"
#                     print sqlr3
#                     cursor.execute(sqlr3);
#                     rowr3 = cursor.fetchall()
#                     retencion = 0
#                     retencion1 = 0
#                     for pr2 in rowr3:
#
#                         retencion_cod = ''
#                         if pr2[2]:
#                             retencion_cod += '' + str(pr2[2]) + '-'
#                         else:
#                             retencion_cod += '-'
#
#                         if pr2[3]:
#                             retencion_cod += '' + str(pr2[3]) + '-'
#                         else:
#                             retencion_cod += '-'
#
#                         if pr2[4]:
#                             retencion_cod += '' + str(pr2[4])
#                         else:
#                             retencion_cod += ''
#
#                         html += '<tr>'
#                         html += '<td><b>&nbsp;Retenciones</b></td>'
#                         html += '<td style="text-align:left">' + str(retencion_cod) + '</td>'
#                         html += '<td style="text-align:center">' + str(pr2[5]) + '</td>'
#                         html += '<td style="text-align:right">0,00</td>'
#
#                         if pr2[0]:
#                             saldo = Decimal(saldo) + Decimal(pr2[0])
#                             PagosTot = float(PagosTot) + float(pr2[0])
#                             PagoParc = float(pr2[0])
#
#                         SaldoTot = float(SaldoTot) - float(PagoParc)
#                         total_a = float(totalf) - float(saldo)
#                         total_credito = total_credito + float(pr2[0])
#                         total_credito_por_cliente = total_credito_por_cliente + float(pr2[0])
#                         html += '<td style="text-align:right">' + str("%0.2f" % pr2[0]).replace('.', ',') + '</td>'
#                         html += '<td style="text-align:right">' + str("%0.2f" % total_a).replace('.', ',') + '</td>'
#                         html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',
#                                                                                                      ',') + '</b></td>'
#                         html += '<td style="text-align:left">' + str(pr2[6].encode('utf8')) + '</td>'
#                         html += '</tr>'
#                     cursor = connection.cursor();
#                     sql3 = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.documento_venta_id=" + str(
#                         p[0]) + " order by m.fecha_emision"
#                     print sql3
#                     cursor.execute(sql3);
#                     row3 = cursor.fetchall()
#
#                     for p3 in row3:
#                         html += '<tr>'
#                         html += '<td><b>&nbsp;' + str(p3[13].encode('utf8')) + '</b></td>'
#                         html += '<td>' + str(p3[9]) + '</td>'
#                         html += '<td style="text-align:center">' + str(p3[4]) + '</td>'
#                         html += '<td style="text-align:right">0,00</td>'
#                         # credito
#                         html += '<td style="text-align:right">' + str("%0.2f" % p3[0]).replace('.', ',') + '</td>'
#                         total_a = 0
#
#                         if p[11] == True:
#                             html += '<td style="text-align:right">0,00</td>'
#                             estadof = 'ANULADO'
#                         else:
#                             saldo = saldo + p3[0]
#                             PagosTot = float(PagosTot) + float(p3[0])
#                             PagoParc = float(p3[0])
#                             total_a = float(totalf) - float(saldo)
#                             html += '<td style="text-align:right">' + str("%0.2f" % total_a).replace('.', ',') + '</td>'
#                             estadof = 'ACTIVO'
#                             total_credito = total_credito + float(p3[0])
#                             total_credito_por_cliente = total_credito_por_cliente + float(p3[0])
#
#                         SaldoTot = float(SaldoTot) - float(PagoParc)
#                         html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',
#                                                                                                      ',') + '</b></td>'
#                         html += '<td style="text-align:left">' + str(p3[8].encode('utf8')) + '</td>'
#
#                         html += '</tr>'
#
#                     ##NOTAS DE CREDITO
#                     cursor = connection.cursor();
#                     sql4 = "select distinct da.total,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion from movimiento_nota_credito da LEFT JOIN movimiento m ON m.id=da.movimiento_id and m.activo is True LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.documento_venta_id=" + str(
#                         p[0]) + " order by m.fecha_emision"
#                     # print sql4
#                     cursor.execute(sql4);
#                     row4 = cursor.fetchall()
#                     for p4 in row4:
#                         html += '<tr>'
#                         html += '<td>' + str(p4[13].encode('utf8')) + '</td>'
#                         html += '<td>' + str(p4[9]) + '</td>'
#                         html += '<td>' + str(p4[4]) + '</td>'
#                         html += '<td style="text-align:right">0,00</td>'
#                         html += '<td style="text-align:right">' + str("%2.2f" % p4[0]).replace('.', ',') + '</td>'
#
#                         total_a = 0
#
#                         if p[11] == True:
#                             html += '<td></td>'
#                             estadof = 'ANULADO'
#                         else:
#                             saldo = saldo + p4[0]
#                             PagosTot = PagosTot + float(p4[0])
#                             PagoParc = float(p4[0])
#                             total_a = float(totalf) - float(saldo)
#                             html += '<td style="text-align:right">' + str("%2.2f" % total_a).replace('.', ',') + '</td>'
#                             estadof = 'ACTIVO'
#                             total_credito = total_credito + float(p4[0])
#                             total_credito_por_cliente = total_credito_por_cliente + float(p4[0])
#
#                         SaldoTot = float(SaldoTot) - float(PagoParc)
#                         html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',
#                                                                                                      ',') + '</b></td>'
#                         html += '<td style="text-align:left">' + str(p4[8].encode('utf8')) + '</td>'
#                         html += '</tr>'
#
#             #Se comenta en Este Informe
#             # if row21:
#             #     html += '<tr><td colspan="8" style="background-color: #F1948A"><b>**Abonos a proformas</b></td></tr>'
#             # for p21 in row21:
#             #     proforma = ''
#             #     if p21[1]:
#             #         proforma += '' + str(p21[2]) + '-'
#             #     else:
#             #         proforma += '-'
#             #
#             #     if p21[2]:
#             #         proforma += '' + str(p21[3]) + '-'
#             #     else:
#             #         proforma += '-'
#             #
#             #     totalp = 0
#             #     if p21[0]:
#             #         cursor = connection.cursor();
#             #         lcSql = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id "
#             #         lcSql += "from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id "
#             #         lcSql += "where da.anulado is not True and da.proforma_id=" + str(
#             #             p21[0]) + "order by m.fecha_emision"
#             #
#             #         cursor.execute(sql4);
#             #         row4 = cursor.fetchall()
#             #         saldop = 0
#             #         for p4 in row4:
#             #             html += '<tr>'
#             #             html += '<td><b>&nbsp;' + str(p4[13].encode('utf8')) + '</b></td>'
#             #             html += '<td>' + str(p4[9]) + '</td>'
#             #             html += '<td style="text-align:center">' + str(p4[4]) + '</td>'
#             #             html += '<td style="text-align:right">0,00</td>'
#             #             # credito
#             #             if p4[0]:
#             #                 PagoParc = float(p4[0])
#             #                 PagosTot = PagosTot + float(p4[0])
#             #             html += '<td style="text-align:right">' + str("%0.2f" % p4[0]).replace('.', ',') + '</td>'
#             #             total_ap = 0
#             #
#             #             SaldoTot = float(SaldoTot) - float(PagoParc)
#             #             saldop = saldop + p4[0]
#             #             total_ap = float(totalp) - float(saldop)
#             #             html += '<td style="text-align:right">' + str("%0.2f" % total_ap).replace('.', ',') + '</td>'
#             #             total_credito = total_credito + float(p4[0])
#             #             total_credito_por_cliente = total_credito_por_cliente + float(p4[0])
#             #
#             #             html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',
#             #                                                                                          ',') + '</b></td>'
#             #             html += '<td style="text-align:left">' + str(p4[8].encode('utf8')) + '</td>'
#             #             html += '</tr>'
#
#             # CHEQUES PROTESTADOS
#             saldocp = 0
#             total_cp = 0
#
#             if chequesp:
#                 for chp in chequesp:
#
#                     html += '<tr>'
#                     html += '<td>&nbsp;CH. PROTESTADO</td>'
#
#                     html += '<td>' + str(chp[10]) + '</td>'
#                     html += '<td style="text-align:center">' + str(chp[1]) + '</td>'
#                     # html += '<td></td>'
#                     html += '<td style="text-align:right">' + str("%0.2f" % chp[4]).replace('.', ',') + '</td>'
#                     # credito
#                     html += '<td style="text-align:right">0,00</td>'
#                     total_a = 0
#
#                     saldocp = Decimal(saldocp) + Decimal(chp[4])
#                     total_cp = Decimal(total_cp) + Decimal(saldocp)
#                     total_debito = float(total_debito) + float(chp[4])
#                     total_debito_por_cliente = float(total_debito_por_cliente) + float(chp[4])
#                     html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'
#
#                     html += '<td>' + str(chp[6].encode('utf8')) + '</td>'
#
#                     html += '</tr>'
#                     html += '<tr>'
#                     html += '<td>&nbsp;CH. PROTESTADO MULTA</td>'
#                     html += '<td>' + str(chp[10]) + '</td>'
#                     html += '<td style="text-align:center">' + str(chp[1]) + '</td>'
#                     # html += '<td></td>'
#                     html += '<td style="text-align:right">' + str("%0.2f" % chp[5]).replace('.', ',') + '</td>'
#                     # credito
#                     html += '<td style="text-align:right">0,00</td>'
#                     total_ac = 0
#
#                     saldocp = Decimal(saldocp) + Decimal(chp[5])
#                     total_cp = Decimal(total_cp) + Decimal(saldocp)
#                     total_debito = float(total_debito) + float(chp[5])
#                     total_debito_por_cliente = float(total_debito_por_cliente) + float(chp[5])
#                     html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'
#                     html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
#                     html += '<td style="text-align:left">' + str(chp[6].encode('utf8')) + '</td>'
#                     html += '</tr>'
#
#                     # Abono Cheques Protestados
#                     cursor = connection.cursor();
#                     sqlc3 = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_cheque da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.cheques_protestados_id=" + str(
#                         chp[0]) + " order by m.fecha_emision"
#                     print sqlc3
#                     cursor.execute(sqlc3);
#                     rowc3 = cursor.fetchall()
#                     saldoabono = 0
#
#                     for pc3 in rowc3:
#                         html += '<tr>'
#                         html += '<td>&nbsp;' + str(pc3[13].encode('utf8')) + '</td>'
#                         html += '<td>' + str(pc3[9]) + '</td>'
#                         html += '<td style="text-align:center">' + str(pc3[4]) + '</td>'
#                         html += '<td></td>'
#                         # credito
#                         html += '<td style="text-align:right">' + str("%0.2f" % pc3[0]).replace('.', ',') + '</td>'
#                         total_ch = 0
#
#                         if pc3[1] == True:
#                             html += '<td style="text-align:right">0,00</td>'
#                             estadof = 'ANULADO'
#
#                         else:
#                             saldoabono = saldoabono + pc3[0]
#                             saldocp = float(saldocp) - float(saldoabono)
#                             html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'
#                             estadof = 'ACTIVO'
#                             total_credito = total_credito + float(pc3[0])
#                             total_credito_por_cliente = total_credito_por_cliente + float(pc3[0])
#
#                         html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',
#                                                                                                      ',') + '</b></td>'
#                         html += '<td style="text-align:left">' + str(pc3[8].encode('utf8')) + '</td>'
#                         html += '</tr>'
#
#             # FINAL DE CHEQUES PROTESTADOS
#             # CHEQUES PROTESTADOS proformaas
#
#             if chequespr:
#                 for chpr in chequespr:
#
#                     html += '<tr>'
#                     html += '<td>&nbsp;CH. PROTESTADO</td>'
#                     html += '<td>' + str(chpr[10]) + '</td>'
#                     html += '<td style="text-align:center">' + str(chpr[1]) + '</td>'
#                     html += '<td style="text-align:right">' + str("%0.2f" % chpr[4]).replace('.', ',') + '</td>'
#                     # credito
#                     html += '<td style="text-align:right">0,00</td>'
#                     total_a = 0
#
#                     saldocp = Decimal(saldocp) + Decimal(chpr[4])
#                     total_cp = Decimal(total_cp) + Decimal(saldocp)
#                     total_debito = float(total_debito) + float(chpr[4])
#                     total_debito_por_cliente = float(total_debito_por_cliente) + float(chpr[4])
#                     html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'
#                     html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
#                     html += '<td style="text-align:left">' + str(chpr[6].encode('utf8')) + '</td>'
#
#                     html += '</tr>'
#                     html += '<tr>'
#                     html += '<td>&nbsp;CH. PROTESTADO MULTA</td>'
#                     html += '<td>' + str(chpr[10]) + '</td>'
#                     html += '<td style="text-align:center">' + str(chpr[1]) + '</td>'
#                     html += '<td style="text-align:right">' + str("%0.2f" % chpr[5]).replace('.', ',') + '</td>'
#                     # credito
#                     html += '<td style="text-align:right">0,00</td>'
#                     total_ac = 0
#
#                     saldocp = Decimal(saldocp) + Decimal(chpr[5])
#                     total_cp = Decimal(total_cp) + Decimal(saldocp)
#                     total_debito = float(total_debito) + float(chpr[5])
#                     total_debito_por_cliente = float(total_debito_por_cliente) + float(chpr[5])
#                     html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'
#                     html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.', ',') + '</b></td>'
#                     html += '<td style="text-align:left">' + str(chpr[6].encode('utf8')) + '</td>'
#                     html += '</tr>'
#
#                     # Abono Cheques Protestados
#                     cursor = connection.cursor();
#                     sqlcp3 = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_cheque da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.anulado is not True and da.cheques_protestados_id=" + str(
#                         chpr[0]) + " order by m.fecha_emision"
#                     print sqlcp3
#                     cursor.execute(sqlcp3);
#                     rowcp3 = cursor.fetchall()
#                     saldoabono = 0
#
#                     for pc3 in rowcp3:
#                         html += '<tr>'
#                         html += '<td>&nbsp;' + str(pc3[13].encode('utf8')) + '</td>'
#                         html += '<td>' + str(pc3[9]) + '</td>'
#                         html += '<td style="text-align:center">' + str(pc3[4]) + '</td>'
#                         html += '<td></td>'
#                         # credito
#                         html += '<td style="text-align:right">' + str("%0.2f" % pc3[0]).replace('.', ',') + '</td>'
#                         total_ch = 0
#
#                         if pc3[1] == True:
#                             html += '<td style="text-align:right">0,00</td>'
#                             estadof = 'ANULADO'
#                         else:
#                             saldoabono = saldoabono + pc3[0]
#                             saldocp = float(saldocp) - float(saldoabono)
#                             html += '<td style="text-align:right">' + str("%0.2f" % saldocp).replace('.', ',') + '</td>'
#                             estadof = 'ACTIVO'
#                             total_credito = total_credito + float(pc3[0])
#                             total_credito_por_cliente = total_credito_por_cliente + float(pc3[0])
#
#                         html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',
#                                                                                                      ',') + '</b></td>'
#                         html += '<td style="text-align:left">' + str(pc3[8].encode('utf8')) + '</td>'
#                         html += '</tr>'
#
#             # proformas hechas facturas abonos
#             #Se comenta en este Informe
#             # for p22 in row22:
#             #     proforma = ''
#             #     if p22[1]:
#             #         proforma += '' + str(p22[2]) + '-'
#             #     else:
#             #         proforma += '-'
#             #
#             #     if p22[2]:
#             #         proforma += '' + str(p22[3]) + '-'
#             #     else:
#             #         proforma += '-'
#             #     totalp = 0
#             #
#             #     if p22[0]:
#             #         cursor = connection.cursor();
#             #         sql41 = "select da.abono,da.anulado,da.anulado,da.created_by,m.fecha_emision,m.paguese_a,m.numero_cheque,m.fecha_cheque,m.descripcion,m.numero_comprobante,m.monto,m.activo,m.monto_cheque,t.descripcion,m.id from documento_abono_venta da LEFT JOIN movimiento m ON m.id=da.movimiento_id LEFT JOIN tipo_documento t ON t.id=m.tipo_documento_id where da.documento_venta_id is null and  da.anulado is not True and m.asociado_cheques_protestados is not True and da.proforma_id=" + str(
#             #             p22[0]) + "order by m.fecha_emision"
#             #
#             #         cursor.execute(sql41);
#             #         row41 = cursor.fetchall()
#             #         saldop = 0
#             #         if row41:
#             #             html += '<tr><td colspan="8" style="background-color: #F1948A"><b>Abonos a Proformas ' + str(
#             #                 proforma) + ' que se convirtieron en diferentes facturas </b></td></tr>'
#             #
#             #             for p4 in row41:
#             #                 html += '<tr>'
#             #                 html += '<td><b>&nbsp;' + str(p4[13].encode('utf8')) + '</b></td>'
#             #                 html += '<td>' + str(p4[9]) + '</td>'
#             #                 html += '<td style="text-align:center">' + str(p4[4]) + '</td>'
#             #                 html += '<td style="text-align:right">0,00</td>'
#             #                 # credito
#             #                 html += '<td style="text-align:right">' + str("%0.2f" % p4[0]).replace('.', ',') + '</td>'
#             #                 total_ap = 0
#             #
#             #                 if p4[0]:
#             #                     PagoParc = float(p4[0])
#             #                     PagosTot = PagosTot + float(p4[0])
#             #
#             #                 SaldoTot = float(SaldoTot) - float(PagoParc)
#             #                 saldop = saldop + p4[0]
#             #                 total_ap = float(totalp) - float(saldop)
#             #                 html += '<td style="text-align:right">' + str("%0.2f" % total_ap).replace('.',
#             #                                                                                           ',') + '</td>'
#             #                 total_credito = total_credito + float(p4[0])
#             #                 total_credito_por_cliente = total_credito_por_cliente + float(p4[0])
#             #
#             #                 html += '<td style="text-align:right"><b>' + str("%0.2f" % SaldoTot).replace('.',
#             #                                                                                              ',') + '</b></td>'
#             #                 html += '<td style="text-align:left">' + str(p4[8].encode('utf8')) + '</td>'
#             #                 html += '</tr>'
#
#             if len(row) > 0 or len(row21) > 0 or len(chequesp) > 0 or len(chequespr) > 0:
#                 total_saldo_por_cliente = float(total_debito_por_cliente) - float(total_credito_por_cliente)
#                 html += '<tr style="background-color: #EBF5FB"><td colspan="3"><b>Saldo Final Cuenta</b></td><td style="text-align:right">' + str(
#                     "%0.2f" % total_debito_por_cliente).replace('.', ',') + '</td><td style="text-align:right">' + str(
#                     "%0.2f" % total_credito_por_cliente).replace('.', ',') + '</td><td style="text-align:right">' + str(
#                     "%0.2f" % total_saldo_por_cliente).replace('.', ',') + '</td><td></td><td></td></tr>'
#         # FINAL DE CHEQUES PROTESTADOS
#
#         #print 'hrl'
#         total_saldo_acum = float(total_debito) - float(total_credito)
#
#         html += '</tbody>'
#         html += '<tfoot style="background-color: #EEEEEE"><tr><td></td><td></td><td></td><td style="text-align:right">' + str(
#             "%0.2f" % total_debito).replace('.', ',') + '</td><td style="text-align:right">' + str(
#             "%0.2f" % total_credito).replace('.', ',') + '</td><td style="text-align:right">' + str(
#             "%0.2f" % total_saldo_acum).replace('.', ',') + '</td><td></td><td></td></tr></tfoot>'
#         html += '</table>'
#
#         return HttpResponse(
#             html
#         )
#     else:
#         raise Http404


def reporteordenproduccionxEstado(request):

    return render_to_response('ordenproduccion/estado_op.html', {}, RequestContext(request))


@csrf_exempt
def obtenerOrdenProduccionxEstado(request):
    if request.method == 'POST':
        estado = request.POST.get('estado')
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor()
        sql="select distinct p.id,p.tipo,p.codigo,p.fecha,p.descripcion,p.detalle,p.cantidad, p.codigo_item,p.pedido_codigo,c.nombre_cliente,p.aprobada,p.finalizada,p.fecha_finalizacion from orden_produccion p left join cliente c on p.cliente_id=c.id_cliente where  p.fecha>='" + fechainicial + "'and p.fecha<='" + fechafin + "' "
        if estado == 1 or estado == '1':
            sql+=" and p.aprobada is not True and p.finalizada is not True "
        
        if estado == 2 or estado == '2':
            sql+=" and p.aprobada is  True and p.finalizada is not True "
        if estado == 3 or estado == '3':
            sql+=" and p.aprobada is  True and p.finalizada is  True "
        
        
        sql+= " order by p.fecha"    
        cursor.execute(sql)
        row = cursor.fetchall()

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        for p in row:
            html += '<tr><td>' + str(p[1].encode('utf8')) + '</td>'
            html += '<td>' + str(p[2]) + '</td>'
            html += '<td>' + str(p[3]) + '</td>'
            html += '<td>' + str(p[9].encode('utf8')) + '</td>'
            html += '<td>' + str(p[4].encode('utf8')) + ' ' + str(p[5].encode('utf8')) + '</td>'
            html += '<td>' + str(p[6]) + '</td>'
            html += '<td>' + str(p[7].encode('utf8')) + '</td>'
            html += '<td>' + str(p[8].encode('utf8')) + '</td>'
            if p[10] != True and p[11] != True :
                html += '<td>Creada</td>'
            if p[10] == True and p[11] != True :
                html += '<td>Aprobada</td>'
            
            if p[10] == True and p[11] == True :
                html += '<td>Finalizada</td>'
            if p[12]:
                html += '<td>' + str(p[12]) + '</td>'
            else:
                html += '<td></td>'
                
            html += '</tr>'

        return HttpResponse(
            html
        )
    else:
        raise Http404



def reporteSaldosClientesCobrarVenc(request):
    return render_to_response('transacciones/saldos_clientes_vencimientos.html', {}, RequestContext(request))

#Cuentas por Cobrar Clientes
def reporteSaldosClientesCobrar(request):
    return render_to_response('transacciones/saldos_clientes_cobrar.html', {}, RequestContext(request))

@csrf_exempt
def obtenerSaldosClientesCobrar(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor()
        sql0="select sum(dv.total),sum(rv.retenciones) from documento_venta dv left join cliente c on dv.cliente_id=c.id_cliente left join documento_venta_retenciones rv on rv.documento_venta_id=dv.id   where  dv.activo is  True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "'"
        cursor.execute(sql0)
        row = cursor.fetchall()
        
        cursor1 = connection.cursor()
        #sql="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,sum(dv.total),sum(rv.retenciones),sum(dav.abonos),sum(nc.total) from documento_venta dv left join cliente c on dv.cliente_id=c.id_cliente left join documento_venta_retenciones rv on rv.documento_venta_id=dv.id  left join movimiento_nota_credito  nc on nc.documento_venta_id=dv.id and  nc.anulado is not True left join documento_venta_abonos dav on dav.documento_venta_id=dv.id where  dv.activo is  True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0)) "
        #sql="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,sum(dv.total),sum(rv.retenciones),sum(dav.abono),sum(nc.total) from documento_venta dv left join cliente c on dv.cliente_id=c.id_cliente left join documento_venta_retenciones rv on rv.documento_venta_id=dv.id  left join movimiento_nota_credito_abonos  nc on nc.cliente_id=dv.cliente_id and  nc.activo is True and nc.fecha_emision>='" + fechainicial + "' and nc.fecha_emision<='" + fechafin + "' left join movimiento_factura_proforma_abono_cliente dav on dav.documento_venta_id=dv.id  and dav.activo is True and dav.fecha_emision>='" + fechainicial + "' and dav.fecha_emision<='" + fechafin + "' where  dv.activo is  True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0)) "
        sql="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,sum(dv.total),sum(rv.retenciones) from documento_venta dv left join cliente c on dv.cliente_id=c.id_cliente left join documento_venta_retenciones rv on rv.documento_venta_id=dv.id   where  dv.activo is  True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "'  group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0)) "
        print sql
        

        cursor1.execute(sql)
        row1 = cursor1.fetchall()
        
        #ABONOS DE FACTURAS
        cursor20 = connection.cursor()
        sql20="select sum(dv.total),sum(dav.abono) from documento_venta dv left join cliente c on dv.cliente_id=c.id_cliente left join movimiento_factura_proforma_abono_cliente dav on dav.documento_venta_id=dv.id  and dav.activo is True and dav.anulado is not True and dav.fecha_emision>='" + fechainicial + "' and dav.fecha_emision<='" + fechafin + "' where  dv.activo is  True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "'"
        cursor20.execute(sql20)
        row20 = cursor20.fetchall()
        #NOTAS DE CREDITOS
        cursor41 = connection.cursor()
        sql41="select sum(nc.total) from movimiento_nota_credito_abonos  nc where  nc.activo is True and nc.cliente_id is not null and nc.documento_compra_id is null and nc.proforma_id is null and nc.fecha_emision>='" + fechainicial + "' and nc.fecha_emision<='" + fechafin + "'"
        cursor41.execute(sql41)
        row41= cursor41.fetchall()
        print sql41
        
        
        html=''
        html+='<table class="table table-bordered " id="detalle">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="5" style="text-align: center"><b>REPORTE DE CUENTAS POR COBRAR <br >'
        #<b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>'
        html+='<b>DESDE:'+str(fechainicial)+' HASTA: '+str(fechafin)+'</b></td></tr>'
        html+='<tr><th style="text-align: center;width:100px"><b>Codigo</b></th><th style="text-align: center"><b>Cliente</b></th>'
        html+='<th style="text-align: center"><b>Deuda</b></th><th style="text-align: center"><b>%</b></th>'
        html+='<th style="text-align: center"><b>Status</b></th>'        
        html+='</tr></thead>'
        html+='<tbody>'
        
        
        for p0 in row:
            if p0[0]:
                total=p0[0]
            else:
                total=0
            if p0[1]:
                totalr=p0[1]
            else:
                totalr=0
            
            
        for p20 in row20:   
            if p20[1]:
                totala=p20[1]
            else:
                totala=0
                
                
        for p41 in row41:  
            if p41[0]:
                totaln=p41[0]
            else:
                totaln=0
                
        

        total_final=float(total)-float(totalr)-float(totala)-float(totaln)
        print 'Total de Fatura t'
        print total
        print 'Total de ret t'
        print totalr
        print 'Total de aboono t'
        print totala
        print 'Total de credito t'
        print totaln

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        total_clt = 0
        total_rt = 0
        total_at = 0
        total_nct = 0
        total_final_porcentaje=0
        for p in row1:
            total_cl = 0
            total_r = 0
            total_a = 0
            total_nc = 0
            html += '<tr>'
            html += '<td>' + str(p[1]) + '</td>'
            if p[2]:
                html += '<td>' + str(p[2].encode('utf8'))+ '</td>'
            else:
                html += '<td></td>'
            
            if p[3]:
                total_cl=total_cl+p[3]
            else:
                total_cl=total_cl+0
            
            if p[4]:
                total_r=total_r+p[4]
            else:
                total_r=total_r+0
            
            # if p[5]:
            #     total_a=total_a+p[5]
            # else:
            #     total_a=total_a+0
            # 
            # if p[6]:
            #     total_nc=total_nc+p[6]
            # else:
            #     total_nc=total_nc+0
                
            cursor2 = connection.cursor()
            #sql="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,sum(dv.total),sum(rv.retenciones),sum(dav.abonos),sum(nc.total) from documento_venta dv left join cliente c on dv.cliente_id=c.id_cliente left join documento_venta_retenciones rv on rv.documento_venta_id=dv.id  left join movimiento_nota_credito  nc on nc.documento_venta_id=dv.id and  nc.anulado is not True left join documento_venta_abonos dav on dav.documento_venta_id=dv.id where  dv.activo is  True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0)) "
            sql2="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,sum(dv.total),sum(dav.abono) from documento_venta dv left join cliente c on dv.cliente_id=c.id_cliente left join movimiento_factura_proforma_abono_cliente dav on dav.documento_venta_id=dv.id  and dav.activo is True and dav.anulado is not True  and dav.fecha_emision>='" + fechainicial + "' and dav.fecha_emision<='" + fechafin + "' and dav.cliente_id="+str(p[0])+"  where  dv.activo is  True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' and dv.cliente_id="+str(p[0])+" group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0))"

            
            
            cursor2.execute(sql2)
            row2 = cursor2.fetchall()
            for p2 in row2:
                if p2[4]:
                    total_a=total_a+p2[4]
                else:
                    total_a=total_a+0
            print ('codigo;' + str(p[1])+';'+str(total_a)) 
            cursor3 = connection.cursor()
            #sql="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,sum(dv.total),sum(rv.retenciones),sum(dav.abonos),sum(nc.total) from documento_venta dv left join cliente c on dv.cliente_id=c.id_cliente left join documento_venta_retenciones rv on rv.documento_venta_id=dv.id  left join movimiento_nota_credito  nc on nc.documento_venta_id=dv.id and  nc.anulado is not True left join documento_venta_abonos dav on dav.documento_venta_id=dv.id where  dv.activo is  True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0)) "
            sql3="select nc.cliente_id,sum(nc.total) from movimiento_nota_credito_abonos  nc where  nc.activo is True and nc.cliente_id is not null and nc.documento_compra_id is null and nc.proforma_id is null and nc.fecha_emision>='" + fechainicial + "' and nc.fecha_emision<='" + fechafin + "' and nc.cliente_id="+str(p[0])+"  group by nc.cliente_id"
            cursor3.execute(sql3)
            row3 = cursor3.fetchall()
            for p3 in row3:
                if p3[1]:
                    total_nc=total_nc+p3[1]
                    #print total_nc
                else:
                    total_nc=total_nc+0
                
            
            total_clt=float(total_clt)+float(total_cl)
            total_rt=float(total_rt)+float(total_r)
            total_at=float(total_at)+float(total_a)
            total_nct=float(total_nct)+float(total_nc)
            total_cancelar=float(total_cl)-float(total_r)-float(total_a) -float(total_nc)
            total_porcentaje=total_cancelar*100/total_final
            html += '<td style="text-align:right">' + str("%0.2f" % total_cancelar).replace('.', ',')+ '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % total_porcentaje).replace('.', ',') + '%</td>'
            html += '<td>ACTIVA</td>'
            html += '</tr>'
            total_final_porcentaje=total_final_porcentaje+total_porcentaje
        print 'Total de Fatura'    
        print total_clt
        print 'Total de ret'    
        print total_rt
        print 'Total de aboono'    
        print total_at
        print 'Total de credito'    
        print total_nct
                
        html += '<tr><th colspan="2">Total </th>'
        html += '<th style="text-align:right">' + str("%0.2f" % total_final).replace('.', ',')+ '</th>'
        html += '<th style="text-align:right">'+ str("%0.2f" % total_final_porcentaje).replace('.', ',')+ '%</th>'
        html += '<th></th>'
        html += '</tr>'
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404

#--------------------------------------------
@csrf_exempt
def obtenerSaldosClientesCobrarVenc(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')

        date = datetime.strptime(fechafin, "%Y-%m-%d")

        fecha30 = date - timedelta(days=30)
        fecha60 = date - timedelta(days=60)
        fecha90 = date - timedelta(days=90)
        fecha120 = date - timedelta(days=120)

        cursor = connection.cursor()
        sql = "select dv.cliente_id, dv.codigo_cliente, dv.nombre_cliente, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha30) + "' and dv.fecha_emision<= '" + str(date) + "' then dv.total else 0 end) dv30, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha30) + "' and dv.fecha_emision<= '" + str(date) + "' then dv.pagos else 0 end) pg30, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha30) + "' and dv.fecha_emision<= '" + str(date) + "' then dv.retenciones else 0 end) rt30, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha60) + "' and dv.fecha_emision<= '" + str(fecha30) + "' then dv.total else 0 end) dv60, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha60) + "' and dv.fecha_emision<= '" + str(fecha30) + "' then dv.pagos else 0 end) pg60, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha60) + "' and dv.fecha_emision<= '" + str(fecha30) + "' then dv.retenciones else 0 end) rt60, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha90) + "' and dv.fecha_emision<= '" + str(fecha60) + "' then dv.total else 0 end) dv90, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha90) + "' and dv.fecha_emision<= '" + str(fecha60) + "' then dv.pagos else 0 end) pg90, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha90) + "' and dv.fecha_emision<= '" + str(fecha60) + "' then dv.retenciones else 0 end) rt90, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha120) + "' and dv.fecha_emision<= '" + str(fecha90) + "' then dv.total else 0 end) dv120, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha120) + "' and dv.fecha_emision<= '" + str(fecha90) + "' then dv.pagos else 0 end) pg120, "
        sql += "sum(case when dv.fecha_emision>'" + str(fecha120) + "' and dv.fecha_emision<= '" + str(fecha90) + "' then dv.retenciones else 0 end) rt120, "
        sql += "sum(case when dv.fecha_emision<='" + str(fecha120) + "' then dv.total else 0 end) dvm120, "
        sql += "sum(case when dv.fecha_emision<='" + str(fecha120) + "' then dv.pagos else 0 end) pgm120, "
        sql += "sum(case when dv.fecha_emision<='" + str(fecha120) + "' then dv.retenciones else 0 end) rtm120 "
        sql += "from vw_deudas_pagos dv "
        sql += "where dv.fecha_emision<='" + str(date) + "' "
        sql += "group by dv.cliente_id, dv.codigo_cliente, dv.nombre_cliente "

        #dv.activo is True and

        cursor.execute(sql)
        row = cursor.fetchall()

        html = ''
        html += '<table class="table table-bordered " id="detalle">'
        html += '<thead style="background-color: #EEEEEE">'
        html += '<tr><td colspan="8" style="text-align: center"><b>LISTADO DE CUENTAS POR COBRAR POR VENCIMIENTOS <br >'
        html += '<b>DESDE:' + str(fechainicial) + ' HASTA: ' + str(fechafin) + '</b></td></tr>'
        html += '<tr><th style="text-align: center;width:100px"><b>Codigo</b></th><th style="text-align: center"><b>Cliente</b></th>'
        html += '<th style="text-align: center"><b>Total Cartera</b></th>'
        html += '<th style="text-align: center"><b> 0 a 30 dias </b></th>'
        html += '<th style="text-align: center"><b>31 a 60 dias </b></th>'
        html += '<th style="text-align: center"><b>61 a 90 dias </b></th>'
        html += '<th style="text-align: center"><b>91 a 120 dias</b></th>'
        html += '<th style="text-align: center"><b> > a 120 dias</b></th>'
        html += '</tr></thead>'
        html += '<tbody>'

        oTotCar = 0
        oCar030 = 0
        oCar060 = 0
        oCar090 = 0
        oCar120 = 0
        oCarMay = 0
        oTot030 = 0
        oTot060 = 0
        oTot090 = 0
        oTot120 = 0
        oTotMay = 0
        oTotals = 0

        for p0 in row:
            oCodigo = ''
            oNomCli = ''
            odv30 = 0
            opg30 = 0
            ort30 = 0
            odv60 = 0
            opg60 = 0
            ort60 = 0
            odv90 = 0
            opg90 = 0
            ort90 = 0
            odv120 = 0
            opg120 = 0
            ort120 = 0
            odvmay = 0
            opgmay = 0
            ortmay = 0


            if p0[1]:
                oCodigo = p0[1]
            if p0[2]:
                oNomCli = p0[2]
            if p0[3]:
                odv30 = float(p0[3])
            if p0[4]:
                opg30 = float(p0[4])
            if p0[5]:
                ort30 = float(p0[5])
            if p0[6]:
                odv60 = float(p0[6])
            if p0[7]:
                opg60 = float(p0[7])
            if p0[8]:
                ort60 = float(p0[8])
            if p0[9]:
                odv90 = float(p0[9])
            if p0[10]:
                opg90 = float(p0[10])
            if p0[11]:
                ort90 = float(p0[11])
            if p0[12]:
                odv120 = float(p0[12])
            if p0[13]:
                opg120 = float(p0[13])
            if p0[14]:
                ort120 = float(p0[14])
            if p0[15]:
                odv120 = float(p0[15])
            if p0[16]:
                opg120 = float(p0[16])
            if p0[17]:
                ort120 = float(p0[17])


            oCar030 = float(odv30) - float(opg30) - float(ort30)
            oCar060 = float(odv60) - float(opg60) - float(ort60)
            oCar090 = float(odv90) - float(opg90) - float(ort90)
            oCar120 = float(odv120) - float(opg120) - float(ort120)
            oCarMay = float(odvmay) - float(opgmay) - float(ortmay)

            oTotCar = float(oCar030) + float(oCar060) + float(oCar090) + float(oCar120) + float(oCarMay)
            oTot030 = float(oTot030) + float(oCar030)
            oTot060 = float(oTot060) + float(oCar060)
            oTot090 = float(oTot090) + float(oCar090)
            oTot120 = float(oTot120) + float(oCar120)
            oTotMay = float(oTotMay) + float(oCarMay)
            oTotals = float(oTotals) + float(oTotCar)

            html += '<tr>'
            html += '<td>' + oCodigo + '</td>'
            html += '<td>' + oNomCli + '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % oTotCar) + '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % oCar030) + '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % oCar060) + '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % oCar090) + '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % oCar120) + '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % oCarMay) + '</td>'


        html += '<tr style="background-color: #81C8F3"><th colspan="2">Totales </th>'
        html += '<th style="text-align:right">' + str("%0.2f" % oTotals).replace('.', ',') + '</th>'
        html += '<th style="text-align:right">' + str("%0.2f" % oTot030).replace('.', ',') + '</th>'
        html += '<th style="text-align:right">' + str("%0.2f" % oTot060).replace('.', ',') + '</th>'
        html += '<th style="text-align:right">' + str("%0.2f" % oTot090).replace('.', ',') + '</th>'
        html += '<th style="text-align:right">' + str("%0.2f" % oTot120).replace('.', ',') + '</th>'
        html += '<th style="text-align:right">' + str("%0.2f" % oTotMay).replace('.', ',') + '</th>'
        html += '</tr>'
        html += '</tbody>'
        html += '</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


#--------------------------------------------
def reporteSaldosAnticiposCobrar(request):
    return render_to_response('transacciones/saldos_anticipos_cobrar.html', {}, RequestContext(request))

@csrf_exempt
def obtenerSaldosAnticiposCobrar(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor()
        #sql0="select sum(p.total),sum(dav.abono) from proforma p left join cliente c on p.cliente_id=c.id_cliente  left join movimiento_factura_proforma_abono_cliente dav on dav.proforma_id=p.id and  dav.fecha_emision>='" + fechainicial + "' and dav.fecha_emision<='" + fechafin + "' and dav.activo is True where  p.aprobada is  True and p.fecha>='" + fechainicial + "' and p.fecha<='" + fechafin + "'  and p.id NOT IN (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL)  group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0)) "
        sql0 ="select sum(p.total),sum(dav.abono) "
        sql0 +="from proforma p "
        sql0 +="left join cliente c on p.cliente_id=c.id_cliente  "
        sql0 +="inner join movimiento_factura_proforma_abono_cliente dav on dav.proforma_id=p.id and dav.fecha_emision>='" + fechainicial + "' and dav.fecha_emision<='" + fechafin + "' and dav.activo is True and dav.anulado is False "
        sql0 +="where  p.aprobada is  True and p.fecha>='" + fechainicial + "' and p.fecha<='" + fechafin + "' "
        #sql0 +="group by c.id_cliente, c.codigo_cliente, c.nombre_cliente "
        #sql0 +="order by CAST(c.codigo_cliente AS Numeric(10,0)) "
        cursor.execute(sql0)
        row = cursor.fetchall()
        
        cursor1 = connection.cursor()
        #sql="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,sum(dav.abono) from documento_venta dv left join cliente c on dv.cliente_id=c.id_cliente left join documento_venta_retenciones rv on rv.documento_venta_id=dv.id left join documento_abono_venta dav on dav.documento_venta_id=dv.id where  dv.activo is  True and dv.fecha_emision>='" + fechainicial + "'and dv.fecha_emision<='" + fechafin + "' group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0)) "
        #sql="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,sum(p.total),sum(dav.abono) from proforma p left join cliente c on p.cliente_id=c.id_cliente  left join movimiento_factura_proforma_abono_cliente dav on dav.proforma_id=p.id and  dav.fecha_emision>='" + fechainicial + "' and dav.fecha_emision<='" + fechafin + "' and dav.activo is True where  p.aprobada is  True and p.fecha>='" + fechainicial + "' and p.fecha<='" + fechafin + "' and p.id NOT IN (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL)  group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0)) "
        sql="select c.id_cliente, c.codigo_cliente, c.nombre_cliente, sum(p.total), sum(dav.abono) "
        sql +="from proforma p "
        sql +="left join cliente c on p.cliente_id=c.id_cliente  "
        sql +="inner join movimiento_factura_proforma_abono_cliente dav on dav.proforma_id=p.id and dav.fecha_emision>='" + fechainicial + "' and dav.fecha_emision<='" + fechafin + "' and dav.activo is True and dav.anulado is False "
        sql +="where  p.aprobada is  True and p.fecha>='" + fechainicial + "' and p.fecha<='" + fechafin + "' "
        sql +="group by c.id_cliente,c.codigo_cliente,c.nombre_cliente "
        sql +="order by CAST(c.codigo_cliente AS Numeric(10,0)) "

        print sql
        cursor1.execute(sql)
        row1 = cursor1.fetchall()
        total=0
        saldo=0
        for p0 in row:
            if p0[0]:
                total=p0[0]
            else:
                total=0
            if p0[1]:
                totalabono=p0[1]
            else:
                totalabono=0
            #saldo = total - totalabono

        total_final=float(total)-float(totalabono)

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html=''
        html+='<table class="table table-bordered " id="detalle">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="5" style="text-align: center"><b>REPORTE DE ANTICIPO POR CLIENTES RESUMEN<br >'
        #<b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>'
        html+='<b>DESDE:'+str(fechainicial)+' HASTA: '+str(fechafin)+'</b></td></tr>'
        html+='<tr><th style="text-align: center;width:100px"><b>Codigo</b></th><th style="text-align: center"><b>Cliente</b></th>'
        html+='<th style="text-align: center"><b>Total Proformas</b></th>'
        html+='<th style="text-align: center"><b>Total Anticipos</b></th>'
        html+='<th style="text-align: center"><b>Saldos</b></th>'
        html+='</tr></thead>'
        html+='<tbody>'
        total_final_porcentaje=0
        for p in row1:
            total_cl = 0
            total_r = 0
            total_a = 0
            total_ab = 0
            #saldo_pr = 0
            html += '<tr>'
            html += '<td>' + str(p[1]) + '</td>'
            if p[2]:
                html += '<td>' + str(p[2].encode('utf8'))+ '</td>'
            else:
                html += '<td></td>'
            
            if p[3]:
                total_cl=total_cl+p[3]
            else:
                total_cl=total_cl+0
            
            if p[4]:
                total_ab=total_ab+p[4]
            else:
                total_ab=total_ab+0
            
            saldo_pr = float(total_cl) - float(total_ab)
            
            total_cancelar=float(total_cl)-float(total_ab)
            total_porcentaje=total_cancelar*100/total_final
            html += '<td style="text-align:right">' + str("%0.2f" % total_cl).replace('.', ',') + '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % total_ab).replace('.', ',') + '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % saldo_pr).replace('.', ',') + '</td>'
            html += '</tr>'
            total_final_porcentaje=total_final_porcentaje+total_porcentaje
                
        html += '<tr><th colspan="2">Total </th>'
        html += '<th style="text-align:right">' + str("%0.2f" % total).replace('.', ',')+ '</th>'
        html += '<th style="text-align:right">' + str("%0.2f" % totalabono).replace('.', ',') + '</th>'
        html += '<th style="text-align:right">' + str("%0.2f" % total_final).replace('.', ',') + '</th>'
        html += '</tr>'
        html += '</tbody>'
        html += '</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404



def reporteSaldosProveedoresPagar(request):
    return render_to_response('transacciones/saldos_proveedor_pagar.html', {}, RequestContext(request))

@csrf_exempt
def obtenerSaldosProveedoresPagar(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor()
        #sql0="select sum(dv.total),sum(rv.retenciones),sum(dav.abono),sum(p.saldo_factura) from documento_compra dv left join proveedor p on dv.proveedor_id=p.proveedor_id left join documento_compra_retenciones rv on rv.documento_compra_id=dv.id left join documento_abono dav on dav.documento_compra_id=dv.id and dav.anulado is not True where  dv.anulado is not  True and dv.no_afecta is not True and dv.fecha_emision>='" + fechainicial + "'and dv.fecha_emision<='" + fechafin + "'"
        #sql0="select sum(dv.total),sum(rv.retenciones),sum(dav.abono),p.saldo_factura,sum(dn.total) from documento_compra dv left join proveedor p on dv.proveedor_id=p.proveedor_id left join documento_compra_retenciones rv on rv.documento_compra_id=dv.id  left join movimiento_factura_abono_proveedores dav on dav.documento_compra_id=dv.id and dav.activo is True and  dav.fecha_emision>='" + fechainicial + "'and dav.fecha_emision<='" + fechafin + "' left join movimiento_nota_credito_abonos dn on dn.documento_compra_id=dv.id and dn.activo is True and  dn.fecha_emision>='" + fechainicial + "' and dn.fecha_emision<='" + fechafin + "' where  dv.anulado is not  True  and dv.no_afecta is not True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "'group by  p.proveedor_id,p.codigo_proveedor,p.nombre_proveedor order by CAST(p.codigo_proveedor AS Numeric(10,0))"
        sql0="select sum(dv.total),sum(rv.retenciones),p.saldo_factura,p.saldo_factura from documento_compra dv left join proveedor p on dv.proveedor_id=p.proveedor_id left join documento_compra_retenciones rv on rv.documento_compra_id=dv.id  where  dv.anulado is not  True  and dv.no_afecta is not True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "'group by  p.proveedor_id,p.codigo_proveedor,p.nombre_proveedor order by CAST(p.codigo_proveedor AS Numeric(10,0))"
        cursor.execute(sql0)
        row = cursor.fetchall()
        
        cursor1 = connection.cursor()
        #sql="select p.proveedor_id,p.codigo_proveedor,p.nombre_proveedor,sum(dv.total),sum(rv.retenciones),sum(dav.abono),p.saldo_factura from documento_compra dv left join proveedor p on dv.proveedor_id=p.proveedor_id left join documento_compra_retenciones rv on rv.documento_compra_id=dv.id left join documento_abono dav on dav.documento_compra_id=dv.id and dav.anulado is not True where  dv.anulado is not  True  and dv.no_afecta is not True and dv.fecha_emision>='" + fechainicial + "'and dv.fecha_emision<='" + fechafin + "' group by  p.proveedor_id,p.codigo_proveedor,p.nombre_proveedor order by CAST(p.codigo_proveedor AS Numeric(10,0)) "
        sql="select p.proveedor_id,p.codigo_proveedor,p.nombre_proveedor,sum(dv.total),sum(rv.retenciones),p.saldo_factura,p.saldo_factura from documento_compra dv left join proveedor p on dv.proveedor_id=p.proveedor_id left join documento_compra_retenciones rv on rv.documento_compra_id=dv.id  where  dv.anulado is not  True  and dv.no_afecta is not True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "'group by  p.proveedor_id,p.codigo_proveedor,p.nombre_proveedor order by CAST(p.codigo_proveedor AS Numeric(10,0))"

        print sql
        cursor1.execute(sql)
        row1 = cursor1.fetchall()
        cursor1.execute(sql)
        row1 = cursor1.fetchall()
        
        
        cursor20 = connection.cursor()
        sql20="select sum(abono) from proveedor_abono_saldo_inicial"
        cursor20.execute(sql20)
        row20 = cursor20.fetchall()
        
        
        
        cursor30 = connection.cursor()
        #sql0="select sum(dv.total),sum(rv.retenciones),sum(dav.abono),sum(p.saldo_factura) from documento_compra dv left join proveedor p on dv.proveedor_id=p.proveedor_id left join documento_compra_retenciones rv on rv.documento_compra_id=dv.id left join documento_abono dav on dav.documento_compra_id=dv.id and dav.anulado is not True where  dv.anulado is not  True and dv.no_afecta is not True and dv.fecha_emision>='" + fechainicial + "'and dv.fecha_emision<='" + fechafin + "'"
        sql30="select sum(dv.total),sum(rv.retenciones),sum(dav.abono),p.saldo_factura,sum(dn.total) from documento_compra dv left join proveedor p on dv.proveedor_id=p.proveedor_id left join documento_compra_retenciones rv on rv.documento_compra_id=dv.id  left join movimiento_factura_abono_proveedores dav on dav.documento_compra_id=dv.id and dav.activo is True and  dav.fecha_emision>='" + fechainicial + "'and dav.fecha_emision<='" + fechafin + "' left join movimiento_nota_credito_abonos dn on dn.documento_compra_id=dv.id and dn.activo is True and  dn.fecha_emision>='" + fechainicial + "' and dn.fecha_emision<='" + fechafin + "' where  dv.anulado is not  True  and dv.no_afecta is not True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "'group by  p.proveedor_id,p.codigo_proveedor,p.nombre_proveedor order by CAST(p.codigo_proveedor AS Numeric(10,0))"
        cursor30.execute(sql30)
        row30 = cursor30.fetchall()
       
        for p0 in row:
            if p0[0]:
                total=p0[0]
            else:
                total=0
            
            if p0[1]:
                totalr=p0[1]
            else:
                totalr=0
            
            # if p0[2]:
            #     totala=p0[2]
            # else:
            #     totala=0
            # 
            if p0[3]:
                totalsald=p0[3]
            else:
                totalsald=0
            
            # if p0[4]:
            #     totalnc=p0[4]
            # else:
            #     totalnc=0
            
        
        
        for p30 in row30:
            
            
            if p30[2]:
                totala=p30[2]
            else:
                totala=0
            
            
            
            if p30[4]:
                totalnc=p30[4]
            else:
                totalnc=0
            
        
        
        for p20 in row20:
            if p20[0]:
                total_abonado_saldo_inicial=p20[0]
            else:
                total_abonado_saldo_inicial=0
            
        total_final=float(total)-float(totalr)-float(totala)+float(totalsald)-float(total_abonado_saldo_inicial)-float(totalnc)

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html=''
        html+='<table class="table table-bordered " id="detalle">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="3" style="text-align: center"><b>REPORTE DE CUENTAS POR PAGAR PROVEEDORES<br >'
        #<b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>'
        html+='<b>DESDE:'+str(fechainicial)+' HASTA: '+str(fechafin)+'</b></td></tr>'
        html+='<tr><th style="text-align: center;width:100px"><b>Codigo</b></th><th style="text-align: center"><b>Nombre</b></th>'
        html+='<th style="text-align: center"><b>Saldo</b></th>'
        html+='</tr></thead>'
        html+='<tbody>'
        total_final_porcentaje=0
        for p in row1:
            total_cl = 0
            total_r = 0
            total_a = 0
            total_ncr=0
            html += '<tr>'
            html += '<td>' + str(p[1]) + '</td>'
            if p[2]:
                html += '<td>' + str(p[2].encode('utf8'))+ '</td>'
            else:
                html += '<td></td>'
            
            if p[3]:
                total_cl=total_cl+p[3]
            else:
                total_cl=total_cl+0
            
            if p[4]:
                total_r=total_r+p[4]
            else:
                total_r=total_r+0
            
            # if p[5]:
            #     total_a=total_a+p[5]
            # else:
            #     total_a=total_a+0
            # 
            # if p[7]:
            #     total_ncr=total_ncr+p[7]
            # else:
            #     total_ncr=total_ncr+0
            
            cursor2 = connection.cursor()
            sql2="select proveedor_id,sum(abono) from proveedor_abono_saldo_inicial where proveedor_id=" + str(p[0]) + " and  fecha_emision>='" + fechainicial + "'and fecha_emision<='" + fechafin + "'  group by  proveedor_id "
            cursor2.execute(sql2)
            row2 = cursor2.fetchall()
            total_anticipo=0
            for p2 in row2:
                total_anticipo=total_anticipo+p2[1]
            
            #total_anticipo_final=total_anticipo_final+total_anticipo
            #SQL DE ABONOS Y NOTAS DE CREDITO
            cursor31 = connection.cursor()
            sql31="select p.proveedor_id,p.codigo_proveedor,p.nombre_proveedor,sum(dv.total),sum(rv.retenciones),sum(dav.abono),p.saldo_factura,sum(dn.total) from documento_compra dv left join proveedor p on dv.proveedor_id=p.proveedor_id left join documento_compra_retenciones rv on rv.documento_compra_id=dv.id  left join movimiento_factura_abono_proveedores dav on dav.documento_compra_id=dv.id and dav.activo is True and  dav.fecha_emision>='" + fechainicial + "'and dav.fecha_emision<='" + fechafin + "' left join movimiento_nota_credito_abonos dn on dn.documento_compra_id=dv.id and dn.activo is True and  dn.fecha_emision>='" + fechainicial + "' and dn.fecha_emision<='" + fechafin + "' where  dv.anulado is not  True  and dv.no_afecta is not True and dv.fecha_emision>='" + fechainicial + "' and dv.fecha_emision<='" + fechafin + "' and p.proveedor_id=" + str(p[0]) + " group by  p.proveedor_id,p.codigo_proveedor,p.nombre_proveedor order by CAST(p.codigo_proveedor AS Numeric(10,0))"
            print sql31
            cursor31.execute(sql31)
            row31 = cursor31.fetchall()
            for p31 in row31:
                if p31[5]:
                    total_a=total_a+p31[5]
                else:
                    total_a=total_a+0
                
                if p31[7]:
                    total_ncr=total_ncr+p31[7]
                else:
                    total_ncr=total_ncr+0
            
        
            
            total_cancelar=float(total_cl)-float(total_r)-float(total_a)+float(p[6])-float(total_anticipo)-float(total_ncr)
            #total_porcentaje=total_cancelar*100/total_final
            total_final_porcentaje=total_final_porcentaje+total_cancelar
            html += '<td style="text-align:right">' + str("%0.2f" % total_cancelar).replace('.', ',')+ '</td>'
            html += '</tr>'
                
        html += '<tr><th colspan="2">Total </th>'
        html += '<th style="text-align:right">' + str("%0.2f" % total_final_porcentaje).replace('.', ',')+ '</th>'
        html += '</tr>'
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


def reporteRangoProveedores(request):
    
    cursor = connection.cursor();
    cursor.execute("SELECT proveedor_id,codigo_proveedor,nombre_proveedor from proveedor order by CAST(codigo_proveedor AS Numeric(10,0))" );
    row = cursor.fetchall();

    return render_to_response('transacciones/proveedores.html', {'proveedores':row}, RequestContext(request))


@csrf_exempt
def obtenerRangoProveedores(request):
    if request.method == 'POST':
        proveedor = request.POST.get('proveedor')
        proveedor_hasta = request.POST.get('proveedor_hasta')
        activo = request.POST.get('activo')
        datos= request.POST.get('datos')
        cursor = connection.cursor()
        
        
        cursor1 = connection.cursor()
        sql="select proveedor_id,codigo_proveedor,nombre_proveedor,direccion1,ruc,telefono1,sin_datos,activo from proveedor where 1=1 "
        if activo == "1":
            sql+=" and activo is True"
        if activo == "2":
            sql+=" and activo is not True"
        
        if datos == "1":
            sql+=" and sin_datos is not True"
        if datos == "2":
            sql+=" and sin_datos is True"
      
        if proveedor != "0":
            sql+=" and codigo_proveedor::float>= "+str(proveedor)
        if proveedor_hasta != "0":
            sql+=" and codigo_proveedor::float<= "+str(proveedor_hasta)
        sql+=" order by CAST(codigo_proveedor AS Numeric(10,0))"
        print sql

        cursor1.execute(sql)
        row1 = cursor1.fetchall()
        html = ''
        html = '<table id="tabla" class="table2 table-striped " border="0"   aria-describedby="data-table_info"><thead>'
        html+='<tr><td colspan="6" style="text-align:center  !important"><b>MUEBLES Y DIVERSIDADES MUEDIRSA S.A.</b><br>'
        
        html+='<b>Proveedores  </b><br>'
        html+='</td></tr>'
        
        #html+='<tr><td colspan="1"><b>DESDE</b></td><td colspan="1">'+str(fecha_desde)+'</td><td colspan="1"><b>HASTA</b></td><td colspan="2">'+str(fecha_hasta)+'</td></tr>'
        #html+='<tr><td colspan="2">Pertenecientes a una entidad individual<br><b>Grado de redondeo:</b>Sin redondeo</td><td colspan="3">AL '+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+'</td></tr>'
        html+='<tr>'
        html+='<th>Codigo</th><th>Nombre</th><th>Direccion</th><th>Ruc</th><th>Telefono</th><th>Datos</th><th>Activo</th>'
        
        html+='</tr></thead>'
        html+='<tbody>'
        
        for p in row1:
            
            html += '<tr>'
            html += '<td>' + str(p[1]) + '</td>'
            if p[2]:
                html += '<td>' + str(p[2].encode('utf8'))+ '</td>'
            else:
                html += '<td></td>'
            
            if p[3]:
                html += '<td>' + str(p[3].encode('utf8'))+ '</td>'
            else:
                html += '<td></td>'
            if p[4]:
                html += '<td>' + str(p[4].encode('utf8'))+ '</td>'
            else:
                html += '<td></td>'
            
            if p[5]:
                html += '<td>' + str(p[5].encode('utf8'))+ '</td>'
            else:
                html += '<td></td>'
            
            if p[6]:
                html += '<td>SIN</td>'
            else:
                html += '<td>CON</td>'
            
            if p[7]:
                html += '<td>SI</td>'
            else:
                html += '<td>NO</td>'
            
            
            
            
           
            html += '</tr>'
                
        

        html+='</tbody>'
        html+='</table>'
        return HttpResponse(
            html
        )
    else:
        raise Http404




def reporteSaldosEmpleadosCobrar(request):
    return render_to_response('transacciones/saldos_empleados_cobrar.html', {}, RequestContext(request))

@csrf_exempt
def obtenerSaldosEmpleadosCobrar(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        fecha_iarreglo = fechainicial.split('-')
        fecha_farreglo = fechafin.split('-')
        print fechainicial
        
        cursor1 = connection.cursor()
        sql="select e.empleado_id,e.codigo_empleado,e.nombre_empleado,sum(eg.valor),sum(d.valor) from empleados_empleado e"
        sql+=" left join egresos_rol_empleado eg on eg.empleado_id=e.empleado_id left join dias_no_laborados_rol_empleado d on d.empleado_id=e.empleado_id"
        sql+=" where  1=1 and eg.anio>='" + fecha_iarreglo[0] + "'and eg.mes>='" + fecha_iarreglo[1]  + "' and eg.anio<='" + fecha_farreglo[0] + "' and eg.mes<='" + fecha_farreglo[1]+"' group by e.empleado_id,e.codigo_empleado,e.nombre_empleado order by CAST(e.codigo_empleado AS Numeric(10,0)) "

        cursor1.execute(sql)
        row1 = cursor1.fetchall()
        
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html=''
        html+='<table class="table table-bordered " id="detalle">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="3" style="text-align: center"><b>REPORTE DE CUENTAS POR COBRAR EMPLEADOS<br >'
        #<b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>'
        html+='<b>DESDE:'+str(fechainicial)+' HASTA: '+str(fechafin)+'</b></td></tr>'
        html+='<tr><th style="text-align: center;width:100px"><b>Codigo</b></th><th style="text-align: center"><b>Nombre</b></th>'
        html+='<th style="text-align: center"><b>Saldo</b></th>'
        html+='</tr></thead>'
        html+='<tbody>'
        total_final_porcentaje=0
        total_final=0
        for p in row1:
            total_cl = 0
            total_r = 0
            total_a = 0
            html += '<tr>'
            html += '<td>' + str(p[1]) + '</td>'
            if p[2]:
                html += '<td>' + str(p[2].encode('utf8'))+ '</td>'
            else:
                html += '<td></td>'
            
            if p[3]:
                total_cl=total_cl+p[3]
            else:
                total_cl=total_cl+0
            
            if p[4]:
                total_r=total_r+p[4]
            else:
                total_r=total_r+0
            
            
            
            total_cancelar=float(total_cl)+float(total_r)
            html += '<td style="text-align:right">' + str("%0.2f" % total_cancelar).replace('.', ',')+ '</td>'
            html += '</tr>'
            total_final=total_final+total_cancelar
                
        html += '<tr><th colspan="2">Total </th>'
        html += '<th style="text-align:right">' + str("%0.2f" % total_final).replace('.', ',')+ '</th>'
        html += '</tr>'
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404



def reporteSaldosAnticiposPagados(request):
    return render_to_response('transacciones/saldos_anticipos_pagados.html', {}, RequestContext(request))

@csrf_exempt
def obtenerSaldosAnticiposPagados(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        cursor = connection.cursor()
        sql0="select sum(p.total),sum(dav.abono) from proforma p left join cliente c on p.cliente_id=c.id_cliente  left join movimiento_factura_proforma_abono_cliente dav on dav.proforma_id=p.id and  dav.fecha_emision>='" + fechainicial + "' and dav.fecha_emision<='" + fechafin + "' and dav.activo is True where  p.aprobada is  True and p.fecha>='" + fechainicial + "' and p.fecha<='" + fechafin + "'  and p.id NOT IN (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL) "
        cursor.execute(sql0)
        row = cursor.fetchall()
        
        cursor1 = connection.cursor()
        #sql="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,sum(dav.abono) from documento_venta dv left join cliente c on dv.cliente_id=c.id_cliente left join documento_venta_retenciones rv on rv.documento_venta_id=dv.id left join documento_abono_venta dav on dav.documento_venta_id=dv.id where  dv.activo is  True and dv.fecha_emision>='" + fechainicial + "'and dv.fecha_emision<='" + fechafin + "' group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0)) "
        sql="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,sum(p.total),sum(dav.abono) from proforma p left join cliente c on p.cliente_id=c.id_cliente  left join movimiento_factura_proforma_abono_cliente dav on dav.proforma_id=p.id and  dav.fecha_emision>='" + fechainicial + "' and dav.fecha_emision<='" + fechafin + "' and dav.activo is True where  p.aprobada is  True and p.fecha>='" + fechainicial + "' and p.fecha<='" + fechafin + "' and p.id NOT IN (select d.proforma_id from documento_venta d where d.activo is True and d.proforma_id is not NULL)  group by c.id_cliente,c.codigo_cliente,c.nombre_cliente order by CAST(c.codigo_cliente AS Numeric(10,0)) "
        print sql
        cursor1.execute(sql)
        row1 = cursor1.fetchall()
        total=0
        for p0 in row:
            if p0[0]:
                total=p0[0]
            else:
                total=0
            if p0[1]:
                totalabono=p0[1]
            else:
                totalabono=0

        total_final=float(totalabono)

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html=''
        html+='<table class="table table-bordered " id="detalle">'
        html+='<thead style="background-color: #EEEEEE">'
        html+='<tr><td colspan="5" style="text-align: center"><b>REPORTE DE CUENTAS POR COBRAR SALDOS DE ANTICIPO<br >'
        #<b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>'
        html+='<b>DESDE:'+str(fechainicial)+' HASTA: '+str(fechafin)+'</b></td></tr>'
        html+='<tr><th style="text-align: center;width:100px"><b>Codigo</b></th><th style="text-align: center"><b>Cliente</b></th>'
        html+='<th style="text-align: center"><b>Deuda</b></th><th style="text-align: center"><b>%</b></th>'
        html+='<th style="text-align: center"><b>Status</b></th>'        
        html+='</tr></thead>'
        html+='<tbody>'
        total_final_porcentaje=0
        for p in row1:
            total_cl = 0
            total_r = 0
            total_a = 0
            total_ab = 0
            html += '<tr>'
            html += '<td>' + str(p[1]) + '</td>'
            if p[2]:
                html += '<td>' + str(p[2].encode('utf8'))+ '</td>'
            else:
                html += '<td></td>'
            
            if p[3]:
                total_cl=total_cl+p[3]
            else:
                total_cl=total_cl+0
            
            if p[4]:
                total_ab=total_ab+p[4]
            else:
                total_ab=total_ab+0

            #total_cancelar=float(total_cl)-float(total_ab)
            total_cancelar=float(total_ab)
            total_porcentaje=total_cancelar*100/total_final
            html += '<td style="text-align:right">' + str("%0.2f" % total_cancelar).replace('.', ',')+ '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % total_porcentaje).replace('.', ',') + '%</td>'
            html += '<td>ACTIVA</td>'
            html += '</tr>'
            total_final_porcentaje=total_final_porcentaje+total_porcentaje
                
        html += '<tr><th colspan="2">Total </th>'
        html += '<th style="text-align:right">' + str("%0.2f" % total_final).replace('.', ',')+ '</th>'
        html += '<th style="text-align:right">'+ str("%0.2f" % total_final_porcentaje).replace('.', ',')+ '%</th>'
        html += '<th></th>'
        html += '</tr>'
        html += '</tbody>'
        html += '</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


csrf_exempt
def reporteInventarioNuevoContable(request):
    bodega = Bodega.objects.values('id', 'codigo_bodega', 'nombre')
    tipos = TipoProducto.objects.values('id', 'codigo', 'descripcion')

    return render_to_response('inventario/inventario_nuevo_contable.html', {'bodega': bodega, 'tipos': tipos}, RequestContext(request))


@csrf_exempt
def obtenerInventarioNuevoContable(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega')
        tipos = request.POST.get('tipos')
        fechafin = request.POST.get('fechafin')

        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        cursor = connection.cursor();
        sql=''
        if tipos == '0':
            sql+="select distinct pb.producto_bodega_id,pb.producto_id,p.codigo_producto,p.descripcion_producto,pb.cantidad,pb.bodega_id,b.codigo_bodega,b.nombre,p.cant_maxima,p.cant_minimia,t.descripcion,pb.cantidad_inicial,p.costo,p.unidad from producto_en_bodega pb,producto p,bodega b,tipo_producto t where pb.producto_id=p.producto_id and b.id=pb.bodega_id and p.tipo_producto=t.id and pb.bodega_id=" + bodega

        else:
            sql +="select distinct pb.producto_bodega_id,pb.producto_id,p.codigo_producto,p.descripcion_producto,pb.cantidad,pb.bodega_id,b.codigo_bodega,b.nombre,p.cant_maxima,p.cant_minimia,t.descripcion,pb.cantidad_inicial,p.costo,p.unidad from producto_en_bodega pb,producto p,bodega b,tipo_producto t where pb.producto_id=p.producto_id and b.id=pb.bodega_id and p.tipo_producto=t.id and p.tipo_producto=" + tipos + " and pb.bodega_id=" + bodega

        if codigo!= '':
            sql +=" and p.codigo_producto ='" +codigo+ "'"
        if nombre!= '':
            sql +=" and p.descripcion_producto like '%" +nombre+ "%'"
        cursor.execute(sql);
        row = cursor.fetchall();
        total_cantidad = 0
        total_costo = 0.0
        total_c = 0
        total_valor=0
        cant=0
        cost=0

        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = ''
        total=0
        total_ingresos=0
        total_egresos=0
        for p in row:
            cost = 0
            cant =0
            html += '<tr><td>' + str(p[2]) + '</td>'
            html += '<td>' + str(p[3].encode('utf8')) + '</td>'
            html += '<td>' + str(p[10]) + '</td>'
            if p[11]:
                cantidad_inicial=p[11]
            else:
                cantidad_inicial=0
            html += '<td>' + str(cantidad_inicial) + '</td>'
            
            cursor31 = connection.cursor()
            # sql31="select p.producto_id,p.codigo_producto, sum(e.cantidad),sum(e.total),sum(i.cantidad),sum(i.total) from producto p left join egresos_items e on e.producto_id=p.producto_id and e.fecha<='" + str(fechafin) +"' and e.asiento_id is not null left join ingresos_items i on i.producto_id=p.producto_id and i.fecha<='"+ str(fechafin) +"' and i.asiento_id is not null where p.producto_id= "+ str(p[1]) +" group by p.producto_id,p.codigo_producto"
            sql31="select p.producto_id,p.codigo_producto, sum(e.cantidad),sum(e.total) from producto p left join egresos_items e on e.producto_id=p.producto_id and e.fecha<='" + str(fechafin) +"' and e.asiento_id is not null where p.producto_id= "+ str(p[1]) +" group by p.producto_id,p.codigo_producto"
            cursor31.execute(sql31)
            row31 = cursor31.fetchall()
            c_ingresos=0
            t_ingresos=0
            c_egresos=0
            t_egresos=0
            
            
            ci_ingresos=0
            ti_ingresos=0
            ci_egresos=0
            ti_egresos=0
            for p31 in row31:
                # html += '<td>' + str(p31[4]) + '</td>'
                # html += '<td>' + str(p31[5]) + '</td>'
                # html += '<td>' + str(p31[2]) + '</td>'
                # html += '<td>' + str(p31[3]) + '</td>'
                
                if p31[2]:
                    c_egresos=c_egresos+p31[2]
                if p31[3]:
                    t_egresos=t_egresos+p31[3]
            
            
            
            cursor32 = connection.cursor()
            sql32="select distinct p.producto_id,p.codigo_producto, sum(i.cantidad),sum(i.total) from producto p left join ingresos_items i on i.producto_id=p.producto_id and i.fecha<='"+ str(fechafin) +"' and i.asiento_id is not null where p.producto_id= "+ str(p[1]) +" group by p.producto_id,p.codigo_producto"
            cursor32.execute(sql32)
            row32 = cursor32.fetchall()
            for p32 in row32:
                if p32[2]:
                    c_ingresos=c_ingresos+p32[2]
                if p32[3]:
                    t_ingresos=t_ingresos+p32[3]
                
            
            
            cursor33 = connection.cursor()
            sql33="select distinct cd.producto_id,cd.bodega_id,sum(cd.cantidad) as cantidad,sum(cd.total) as total,sum(d.base_iva) as subtotal,sum(d.total) as ftotal from compras_locales c,compras_detalle cd, documento_compra d,contabilidad_asiento a,contabilidad_asientodetalle ca where cd.compra_id=c.orden_compra_id and d.compra_id=c.id and c.fecha<='"+ str(fechafin) +"' and d.asiento_id=ca.asiento_id and ca.asiento_id=a.asiento_id  and ca.cuenta_id IN (650,646,645,647,648,644,628,648) and c.anulado is not True and d.anulado is not true and d.no_afecta is not True and cd.producto_id="+ str(p[1]) +" group by cd.producto_id,cd.bodega_id"
            cursor33.execute(sql33)
            row33 = cursor33.fetchall()
            for p33 in row33:
                if p33[2]:
                    c_ingresos=c_ingresos+p33[2]
                if p33[4]:
                    t_ingresos=t_ingresos+p33[3]
                    
                    
                    
            cursor34 = connection.cursor()
            sql34="select distinct i.producto_id,sum(i.cantidad),sum(i.total) from  orden_compra_ingresos i where i.fecha<='"+ str(fechafin) +"' and  i.producto_id= "+ str(p[1]) +" group by i.producto_id"
            cursor34.execute(sql34)
            row34 = cursor34.fetchall()
            for p34 in row34:
                if p34[1]:
                    ci_ingresos=ci_ingresos+p34[1]
                if p34[2]:
                    ti_ingresos=ti_ingresos+p34[2]
                
            
            
            cursor35 = connection.cursor()
            sql35="select distinct e.producto_id,sum(e.cantidad) ,sum(e.total)  from orden_egreso_egresos e where e.fecha<='"+ str(fechafin) +"' and  e.producto_id= "+ str(p[1]) +" group by e.producto_id"
            cursor35.execute(sql35)
            row35 = cursor33.fetchall()
            for p35 in row35:
                if p35[1]:
                    ci_egresos=ci_egresos+p35[1]
                if p35[2]:
                    ti_egresos=ti_egresos+p35[2]
                
            t_egresos=round(t_egresos,2)
            t_ingresos=round(t_ingresos,2)
            html += '<td>' + str(c_ingresos) + '</td>'

            html += '<td>' + str(c_egresos) + '</td>'
            cantidad=float(cantidad_inicial)+float(ci_ingresos)-float(ci_egresos)
            html += '<td>' + str(cantidad) + '</td>'
            html += '<td>' + str(t_ingresos) + '</td>'
            html += '<td>' + str(t_egresos) + '</td>'
            total_ingresos=float(total_ingresos)+float(t_ingresos)
            total_egresos= float(total_egresos) + float(t_egresos)
            total_cuenta=float(t_ingresos)-float(t_egresos)
            html += '<td>' + str(total_cuenta) + '</td>'


            html += '</tr>'
        
        
        html += '<tr><td colspan="6"><b>Total</b></td>'
        html += '<td><b>' + str(total_ingresos) + '</b></td>'
        html += '<td><b>' + str(total_egresos) + '</b></td>'
        total=float(total_ingresos)-float(total_egresos)
        html += '<td><b>' + str(total) + '</b></td>'
        html += '</tr>'
        
        
        html += '<tr><td colspan="8"><b>Saldos Iniciales</b></td></tr>'
        cursor34 = connection.cursor()
        sql34="select ca.cuenta_id,c.codigo_plan,c.nombre_plan,sum(debe),sum(haber) from contabilidad_asiento a, contabilidad_asientodetalle ca, contabilidad_plandecuentas c where a.asiento_id=ca.asiento_id and a.anulado is not true and a.inicial is true and c.plan_id=ca.cuenta_id and ca.cuenta_id IN (650,646,645,647,648,644,628,648) group by ca.cuenta_id,c.codigo_plan,c.nombre_plan"
        cursor34.execute(sql34)
        row34= cursor34.fetchall()
        for p34 in row34:
            html += '<tr><td colspan="2"><b>' + str(p34[1]) + '</b></td>'
            html += '<td colspan="4"><b>' + str(p34[2]) + '</b></td>'
            html += '<td>' + str(p34[3]) + '</td>'
            html += '<td>' + str(p34[4]) + '</td>'
            html += '</tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404


