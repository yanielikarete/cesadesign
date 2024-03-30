import StringIO
from collections import namedtuple
from rexec import FileWrapper

from django.db import connection,IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from xml.dom import minidom
from numpy import math


# Create your views here.

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

#=====================================================#


@login_required()
def index(request):

    return render(request, 'ats/generar_archivo_ats.html')
#=====================================================#
@csrf_exempt
def generarXmlAts(request):
    if request.method == 'GET':
        mes = request.GET.get('mes')
        anio = request.GET.get('anio')
        cursor = connection.cursor();

        root = minidom.Document()

        xml = root.createElement('iva')
        root.appendChild(xml)

        childOfIva = root.createElement('TipoIDInformante')
        childOfIva.appendChild(root.createTextNode('R'))
        xml.appendChild(childOfIva)

        childOfIva = root.createElement('IdInformante')
        childOfIva.appendChild(root.createTextNode('0992128372001'))
        xml.appendChild(childOfIva)

        childOfIva = root.createElement('razonSocial')
        childOfIva.appendChild(root.createTextNode('MUEBLES Y DIVERSIDADES MUEDIRSA SA'))
        xml.appendChild(childOfIva)

        childOfIva = root.createElement('Anio')
        childOfIva.appendChild(root.createTextNode(str(anio)))
        xml.appendChild(childOfIva)
        

        childOfIva = root.createElement('Mes')
        
        childOfIva.appendChild(root.createTextNode(str(mes.zfill(2))))
        xml.appendChild(childOfIva)

        childOfIva = root.createElement('numEstabRuc')
        childOfIva.appendChild(root.createTextNode('003'))
        xml.appendChild(childOfIva)

        # sql_total_ventas = "SELECT distinct " \
        #                    "sum(dv.total) as total " \
        #                    "FROM documento_venta dv " \
        #                    "LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id " \
        #                    "LEFT JOIN puntos_venta p ON dv.punto_venta_id=p.id " \
        #                    "LEFT JOIN razon_social r ON r.id=dv.razon_social_id " \
        #                    "WHERE Extract(month from dv.fecha_emision) ='" + str(
        #     mes) + "' AND Extract(year from dv.fecha_emision) ='" + str(anio) + "'  AND dv.activo is True;"
        
        sql_total_ventas = "SELECT distinct " \
                           "sum(dv.base_iva) as total,sum(dv.base_iva_0),sum(dv.descuento)" \
                           "FROM documento_venta dv " \
                           "LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id " \
                           "LEFT JOIN puntos_venta p ON dv.punto_venta_id=p.id " \
                           "LEFT JOIN razon_social r ON r.id=dv.razon_social_id " \
                           "WHERE Extract(month from dv.fecha_emision) ='" + str(
            mes) + "' AND Extract(year from dv.fecha_emision) ='" + str(anio) + "'  AND dv.activo is True AND dv.facturacion_eletronica is True;"
        cursor.execute(sql_total_ventas);
        #AGREGADO DEBIDO PORQUE EN EL CAMBO base imp es el subtotal-descuento
        arr_ventas=cursor.fetchone()
        #print arr_ventas
        subtotal_ventas = arr_ventas[0]
        descuento_ventas = arr_ventas[2]
        # print  arr_ventas[0]
        # print  arr_ventas[2]
        #total_ventas = cursor.fetchone()[0]
        total_ventas=subtotal_ventas-descuento_ventas

        totalVentas = root.createElement('totalVentas')
        totalVentas.appendChild(root.createTextNode(str("%.2f" % total_ventas)))
        xml.appendChild(totalVentas)

        childOfIva = root.createElement('codigoOperativo')
        childOfIva.appendChild(root.createTextNode('IVA'))
        xml.appendChild(childOfIva)

        #----------------------------------------INICIO COMPRAS-------------------------------------
        childOfIvaCompras = root.createElement('compras')
        xml.appendChild(childOfIvaCompras)

        # sql_compras=" SELECT  distinct " \
        #             "documento_compra.fecha_emision," \
        #             "documento_compra.establecimiento as documento_compra_establecimiento," \
        #             "documento_compra.punto_emision as documento_compra_punto_emision," \
        #             "documento_compra.secuencial as documento_compra_secuencial," \
        #             "documento_compra.autorizacion as documento_compra_autorizacion," \
        #             "documento_compra.descripcion as documento_compra_descricion," \
        #             "documento_compra.base_iva_0," \
        #             "documento_compra.valor_iva_0," \
        #             "documento_compra.base_iva," \
        #             "documento_compra.valor_iva," \
        #             "documento_compra.porcentaje_iva," \
        #             "documento_compra.subtotal," \
        #             "documento_compra.descuento," \
        #             "documento_compra.total," \
        #             "documento_compra.punto_emision," \
        #             "documento_compra.valor_ice," \
        #             "proveedor.nombre_proveedor," \
        #             "orden_compra.nro_compra," \
        #             "compras_locales.codigo," \
        #             "sustento_tributario.descripcion as sustento_tributario_descripcion," \
        #             "sustento_tributario.codigo as sustento_tributario_codigo," \
        #             "sri_forma_pago.descripcion as sri_forma_pago_descripcion," \
        #             "documento_retencion_compra.fecha_emision as documento_retencion_compra_fecha_emision," \
        #             "documento_retencion_compra.establecimiento as documento_retencion_compra_establecimiento," \
        #             "documento_retencion_compra.punto_emision as documento_retencion_compra_punto_emision," \
        #             "documento_retencion_compra.secuencial as documento_retencion_compra_secuencial," \
        #             "documento_retencion_compra.autorizacion as documento_retencion_compra_autorizacion," \
        #             "documento_retencion_compra.valor_retenido, " \
        #             "proveedor.codigo_proveedor," \
        #             "proveedor.pasaporte as proveedor_pasaporte," \
        #             "proveedor.ruc as proveedor_ruc," \
        #             "documento_retencion_compra.id as id_documento_retencion_compra," \
        #             "documento_compra.tipo_provision," \
        #             "documento_compra.base_no_iva_factura," \
        #             "documento_compra.base_rise_factura, " \
        #             "(SELECT COALESCE( (SELECT detalle_documento_retencion.valor_retenido from documento_retencion_detalle_compra as detalle_documento_retencion LEFT JOIN retencion_detalle as retencion_detalle ON retencion_detalle.id = detalle_documento_retencion.retencion_detalle_id where detalle_documento_retencion.documento_retencion_compra_id = documento_compra.id and retencion_detalle.tipo_retencion_id = 2 and retencion_detalle.codigo = '721'), 0) as valRetBien10), " \
        #             "(SELECT COALESCE( (SELECT detalle_documento_retencion.valor_retenido from documento_retencion_detalle_compra as detalle_documento_retencion LEFT JOIN retencion_detalle as retencion_detalle ON retencion_detalle.id = detalle_documento_retencion.retencion_detalle_id where detalle_documento_retencion.documento_retencion_compra_id = documento_compra.id and retencion_detalle.tipo_retencion_id = 2 and retencion_detalle.codigo = '723'), 0) as valRetServ20), " \
        #             "(SELECT COALESCE( (SELECT detalle_documento_retencion.valor_retenido from documento_retencion_detalle_compra as detalle_documento_retencion LEFT JOIN retencion_detalle as retencion_detalle ON retencion_detalle.id = detalle_documento_retencion.retencion_detalle_id where detalle_documento_retencion.documento_retencion_compra_id = documento_compra.id and retencion_detalle.tipo_retencion_id = 2 and retencion_detalle.codigo = '725'), 0) as valretbien30), " \
        #             "(SELECT COALESCE( (SELECT detalle_documento_retencion.valor_retenido from documento_retencion_detalle_compra as detalle_documento_retencion LEFT JOIN retencion_detalle as retencion_detalle ON retencion_detalle.id = detalle_documento_retencion.retencion_detalle_id where detalle_documento_retencion.documento_retencion_compra_id = documento_compra.id and retencion_detalle.tipo_retencion_id = 2 and retencion_detalle.codigo = '729'), 0) as valretserv70), " \
        #             "(SELECT COALESCE( (SELECT detalle_documento_retencion.valor_retenido from documento_retencion_detalle_compra as detalle_documento_retencion LEFT JOIN retencion_detalle as retencion_detalle ON retencion_detalle.id = detalle_documento_retencion.retencion_detalle_id where detalle_documento_retencion.documento_retencion_compra_id = documento_compra.id and retencion_detalle.tipo_retencion_id = 2 and retencion_detalle.codigo = '731'), 0) as valRetServ100) " \
        #             "FROM documento_compra " \
        #             "LEFT JOIN proveedor ON proveedor.proveedor_id=documento_compra.proveedor_id " \
        #             "LEFT JOIN sustento_tributario ON sustento_tributario.id=documento_compra.sustento_tributario_id " \
        #             "LEFT JOIN orden_compra ON orden_compra.compra_id=documento_compra.orden_compra_id " \
        #             "LEFT JOIN compras_locales ON compras_locales.id=documento_compra.compra_id " \
        #             "LEFT JOIN sri_forma_pago ON sri_forma_pago.id=documento_compra.sri_forma_pago_id " \
        #             "LEFT JOIN documento_retencion_compra ON documento_retencion_compra.documento_compra_id=documento_compra.id " \
        #             "WHERE Extract(month from documento_compra.fecha_emision) ='" + str(mes) + "'and Extract(year from documento_compra.fecha_emision) ='" + str(anio) + "' and documento_compra.anulado is not True and documento_compra.no_afecta is not True order by documento_compra.fecha_emision"
        
        
        sql_compras=" SELECT  distinct " \
                    "documento_compra.fecha_emision," \
                    "documento_compra.establecimiento as documento_compra_establecimiento," \
                    "documento_compra.punto_emision as documento_compra_punto_emision," \
                    "documento_compra.secuencial as documento_compra_secuencial," \
                    "documento_compra.autorizacion as documento_compra_autorizacion," \
                    "documento_compra.descripcion as documento_compra_descricion," \
                    "documento_compra.base_iva_0," \
                    "documento_compra.valor_iva_0," \
                    "documento_compra.base_iva," \
                    "documento_compra.valor_iva," \
                    "documento_compra.porcentaje_iva," \
                    "documento_compra.subtotal," \
                    "documento_compra.descuento," \
                    "documento_compra.total," \
                    "documento_compra.punto_emision," \
                    "documento_compra.valor_ice," \
                    "proveedor.nombre_proveedor," \
                    "orden_compra.nro_compra," \
                    "compras_locales.codigo," \
                    "sustento_tributario.descripcion as sustento_tributario_descripcion," \
                    "sustento_tributario.codigo as sustento_tributario_codigo," \
                    "sri_forma_pago.descripcion as sri_forma_pago_descripcion," \
                    "documento_retencion_compra.fecha_emision as documento_retencion_compra_fecha_emision," \
                    "documento_retencion_compra.establecimiento as documento_retencion_compra_establecimiento," \
                    "documento_retencion_compra.punto_emision as documento_retencion_compra_punto_emision," \
                    "documento_retencion_compra.secuencial as documento_retencion_compra_secuencial," \
                    "documento_retencion_compra.autorizacion as documento_retencion_compra_autorizacion," \
                    "documento_retencion_compra.valor_retenido, " \
                    "proveedor.codigo_proveedor," \
                    "proveedor.pasaporte as proveedor_pasaporte," \
                    "proveedor.ruc as proveedor_ruc," \
                    "documento_retencion_compra.id as id_documento_retencion_compra," \
                    "documento_compra.tipo_provision," \
                    "documento_compra.base_no_iva_factura," \
                    "documento_compra.base_rise_factura, " \
                    "(SELECT COALESCE( (SELECT detalle_documento_retencion.retenciones from documento_compra_retenciones_codigo as detalle_documento_retencion where detalle_documento_retencion.documento_compra_id = documento_compra.id  " \
                    "and detalle_documento_retencion.tipo_retencion_id = 2 and detalle_documento_retencion.codigo = '721'), 0) as valRetBien10),  " \
                    "(SELECT COALESCE( (SELECT detalle_documento_retencion.retenciones from documento_compra_retenciones_codigo as detalle_documento_retencion where detalle_documento_retencion.documento_compra_id = documento_compra.id and detalle_documento_retencion.tipo_retencion_id = 2 and detalle_documento_retencion.codigo = '723'), 0) as valRetServ20), " \
                    "(SELECT COALESCE( (SELECT detalle_documento_retencion.retenciones from documento_compra_retenciones_codigo as detalle_documento_retencion where detalle_documento_retencion.documento_compra_id = documento_compra.id and detalle_documento_retencion.tipo_retencion_id = 2 and detalle_documento_retencion.codigo = '725'), 0) as valretbien30),  " \
                    "(SELECT COALESCE( (SELECT detalle_documento_retencion.retenciones from documento_compra_retenciones_codigo as detalle_documento_retencion where detalle_documento_retencion.documento_compra_id = documento_compra.id and detalle_documento_retencion.tipo_retencion_id = 2 and detalle_documento_retencion.codigo = '729'), 0) as valretserv70),  " \
                    "(SELECT COALESCE( (SELECT detalle_documento_retencion.retenciones from documento_compra_retenciones_codigo as detalle_documento_retencion where detalle_documento_retencion.documento_compra_id = documento_compra.id and detalle_documento_retencion.tipo_retencion_id = 2 and detalle_documento_retencion.codigo = '731'), 0) as valRetServ100) " \
                    "FROM documento_compra " \
                    "LEFT JOIN proveedor ON proveedor.proveedor_id=documento_compra.proveedor_id " \
                    "LEFT JOIN sustento_tributario ON sustento_tributario.id=documento_compra.sustento_tributario_id " \
                    "LEFT JOIN orden_compra ON orden_compra.compra_id=documento_compra.orden_compra_id " \
                    "LEFT JOIN compras_locales ON compras_locales.id=documento_compra.compra_id " \
                    "LEFT JOIN sri_forma_pago ON sri_forma_pago.id=documento_compra.sri_forma_pago_id " \
                    "LEFT JOIN documento_retencion_compra ON documento_retencion_compra.documento_compra_id=documento_compra.id " \
                    "WHERE Extract(month from documento_compra.fecha_emision) ='" + str(mes) + "'and Extract(year from documento_compra.fecha_emision) ='" + str(anio) + "' and documento_compra.anulado is not True and documento_compra.no_afecta is not True and documento_compra.ats is True order by documento_compra.fecha_emision"
        #print sql_compras
        
        cursor.execute(sql_compras);
        results = namedtuplefetchall(cursor)


        for compra in results:
            #if compra.proveedor_ruc.strip('0'):#QUITAR
            childOfCompras = root.createElement('detalleCompras')
            childOfIvaCompras.appendChild(childOfCompras)

            childOfDetalleCompras = root.createElement('codSustento')
            childOfDetalleCompras.appendChild(root.createTextNode(compra.sustento_tributario_codigo))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('tpIdProv')
            if compra.proveedor_pasaporte:
                childOfDetalleCompras.appendChild(root.createTextNode('03'))
            else:
                if len(compra.proveedor_ruc) > 10:
                    childOfDetalleCompras.appendChild(root.createTextNode('01'))
                elif len(compra.proveedor_ruc) <= 10:
                    childOfDetalleCompras.appendChild(root.createTextNode('02'))

            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('idProv')
            if len(compra.proveedor_ruc) > 10:
                childOfDetalleCompras.appendChild(root.createTextNode(compra.proveedor_ruc.zfill(13)))
            elif len(compra.proveedor_ruc) <= 10:
                childOfDetalleCompras.appendChild(root.createTextNode(compra.proveedor_ruc.zfill(10)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('tipoComprobante')
            if compra.tipo_provision.lower() == 'factura':
                childOfDetalleCompras.appendChild(root.createTextNode('01'))
            elif compra.tipo_provision.lower() == 'nota de venta':
                childOfDetalleCompras.appendChild(root.createTextNode('02'))
            elif compra.tipo_provision.lower() == 'nota de credito':
                childOfDetalleCompras.appendChild(root.createTextNode('04'))
            elif compra.tipo_provision.lower() == 'nota de debito':
                childOfDetalleCompras.appendChild(root.createTextNode('05'))
            elif compra.tipo_provision.lower() == 'liquidacion compra':
                childOfDetalleCompras.appendChild(root.createTextNode('03'))
            else:
                childOfDetalleCompras.appendChild(root.createTextNode('01')) #VALIDAR NULOS


            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('parteRel')
            childOfDetalleCompras.appendChild(root.createTextNode('NO'))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('fechaRegistro')
            childOfDetalleCompras.appendChild(root.createTextNode(compra.fecha_emision.strftime("%d/%m/%Y")))#REVISAR
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('establecimiento')
            childOfDetalleCompras.appendChild(root.createTextNode(compra.documento_compra_establecimiento))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('puntoEmision')
            childOfDetalleCompras.appendChild(root.createTextNode(str(compra.punto_emision)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('secuencial')
            childOfDetalleCompras.appendChild(root.createTextNode(str(compra.documento_compra_secuencial)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('fechaEmision')
            childOfDetalleCompras.appendChild(root.createTextNode(compra.fecha_emision.strftime("%d/%m/%Y")))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('autorizacion')
            childOfDetalleCompras.appendChild(root.createTextNode(str(compra.documento_compra_autorizacion)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('baseNoGraIva')
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.base_no_iva_factura)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('baseImponible')
            if compra.tipo_provision.lower() == 'factura':
                base_imponible = compra.base_iva_0
            elif compra.tipo_provision.lower() == 'nota de venta':
                base_imponible = compra.base_rise_factura
            else:
                base_imponible = compra.base_iva_0 #VALIDAR NULOS
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % base_imponible)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('baseImpGrav')
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.base_iva)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('baseImpExe')#REVISAR
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('montoIce')
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valor_ice)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('montoIva')
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valor_iva)))
            childOfCompras.appendChild(childOfDetalleCompras)

            #RETENCIONES MAYORES QUE MONTO IVA GENERAN ERROR
            childOfDetalleCompras = root.createElement('valRetBien10')
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valretbien10)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('valRetServ20')
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valretserv20)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('valorRetBienes')# RETENCION 30%
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valretbien30)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('valRetServ50')# NO APLICA (SOLO EMPRESAS MINERAS)
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('valorRetServicios')# RETENCION 70%
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valretserv70)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('valRetServ100')
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valretserv100)))
            #childOfDetalleCompras.appendChild(root.createTextNode(compra.valRetServ100))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('totbasesImpReemb')
            childOfDetalleCompras.appendChild(root.createTextNode('0.00')) #NO APLICA
            childOfCompras.appendChild(childOfDetalleCompras)

            #---------------------------PAGO EXTERIOR----------------------
            childOfDetalleComprasPagoExterior = root.createElement('pagoExterior')
            childOfCompras.appendChild(childOfDetalleComprasPagoExterior)

            childOfPagoExterior = root.createElement('pagoLocExt')
            childOfPagoExterior.appendChild(root.createTextNode("01"))
            childOfDetalleComprasPagoExterior.appendChild(childOfPagoExterior)

            childOfPagoExterior = root.createElement('paisEfecPago')
            childOfPagoExterior.appendChild(root.createTextNode("NA"))
            childOfDetalleComprasPagoExterior.appendChild(childOfPagoExterior)

            childOfPagoExterior = root.createElement('aplicConvDobTrib')
            childOfPagoExterior.appendChild(root.createTextNode("NA"))
            childOfDetalleComprasPagoExterior.appendChild(childOfPagoExterior)

            childOfPagoExterior = root.createElement('pagExtSujRetNorLeg')
            childOfPagoExterior.appendChild(root.createTextNode("NA"))
            childOfDetalleComprasPagoExterior.appendChild(childOfPagoExterior)
            #-----------------------FIN PAGO EXTERIOR----------------------


            #-----------------------INICIO FORMAS DE PAGO----------------------
            # Cuando la suma de las BASES IMPONIBLES y los MONTOS de IVA e ICE exceden los USD. 1000.00.
            if compra.base_no_iva_factura + base_imponible + compra.valor_ice + compra.valor_iva + compra.base_iva >= 1000:
                childOfDetalleComprasFormasDePago = root.createElement('formasDePago')
                childOfCompras.appendChild(childOfDetalleComprasFormasDePago)

                childOfFormaDePago = root.createElement('formaPago')#VALIDAR LA FORMA DE PAGO
                childOfFormaDePago.appendChild(root.createTextNode("01"))
                childOfDetalleComprasFormasDePago.appendChild(childOfFormaDePago)

            #--------------------------FIN FORMAS DE PAGO----------------------

            #-----------------------------AIR------------------------------
            sql_retenciones_air = "SELECT retencion_detalle.codigo, " \
                                  "retencion_detalle.porcentaje, " \
                                  "detalle_documento_retencion.valor_retenido, " \
                                  "detalle_documento_retencion.base_imponible, " \
                                  "detalle_documento_retencion.porcentaje_retencion " \
                                  "FROM documento_retencion_detalle_compra as detalle_documento_retencion " \
                                  "LEFT JOIN retencion_detalle as retencion_detalle ON retencion_detalle.id = detalle_documento_retencion.retencion_detalle_id " \
                                  "WHERE detalle_documento_retencion.documento_retencion_compra_id = " + str(compra.id_documento_retencion_compra) + " " \
                                  "AND retencion_detalle.tipo_retencion_id = 1"

            cursor.execute(sql_retenciones_air);
            results_retenciones_air = namedtuplefetchall(cursor)

            childOfDetalleComprasAir = root.createElement('air')
            childOfCompras.appendChild(childOfDetalleComprasAir)
            cont=0

            for air in results_retenciones_air:
                childOfAir = root.createElement('detalleAir')
                childOfDetalleComprasAir.appendChild(childOfAir)

                childOfDetalleAir = root.createElement('codRetAir')
                childOfDetalleAir.appendChild(root.createTextNode(air.codigo))
                childOfAir.appendChild(childOfDetalleAir)
                childOfDetalleAir = root.createElement('baseImpAir')
                childOfDetalleAir.appendChild(root.createTextNode(str("%.2f" % air.base_imponible)))
                childOfAir.appendChild(childOfDetalleAir)
                
                if air.codigo=='332':
    
                    childOfDetalleAir = root.createElement('porcentajeAir')
                    childOfDetalleAir.appendChild(root.createTextNode(str('0')))
                    childOfAir.appendChild(childOfDetalleAir)
    
                    childOfDetalleAir = root.createElement('valRetAir')
                    childOfDetalleAir.appendChild(root.createTextNode(str('0')))
                    childOfAir.appendChild(childOfDetalleAir)
                else:
                    
                    childOfDetalleAir = root.createElement('porcentajeAir')
                    childOfDetalleAir.appendChild(root.createTextNode(str(air.porcentaje)))
                    childOfAir.appendChild(childOfDetalleAir)
    
                    childOfDetalleAir = root.createElement('valRetAir')
                    childOfDetalleAir.appendChild(root.createTextNode(str("%.2f" % air.valor_retenido)))
                    childOfAir.appendChild(childOfDetalleAir)
                    cont=1

            #---------------------------FIN AIR----------------------------
            #Validar resultados 0000
            if cont != 0:
                if compra.documento_retencion_compra_establecimiento: 
                    if int(compra.documento_retencion_compra_establecimiento) != 0:
                        childOfDetalleCompras = root.createElement('estabRetencion1')
                        childOfDetalleCompras.appendChild(root.createTextNode(str(compra.documento_retencion_compra_establecimiento)))
                        childOfCompras.appendChild(childOfDetalleCompras)
                #VALIDAR RESULTADOS 0000000
                if compra.documento_retencion_compra_punto_emision:
                    if int(compra.documento_retencion_compra_punto_emision) != 0:
                        childOfDetalleCompras = root.createElement('ptoEmiRetencion1')
                        childOfDetalleCompras.appendChild(root.createTextNode(str(compra.documento_retencion_compra_punto_emision)))
                        childOfCompras.appendChild(childOfDetalleCompras)
    
                #VALIDAR RESULTADOS 0000000
                if compra.documento_retencion_compra_secuencial:
                    if int(compra.documento_retencion_compra_secuencial) == 0:
                        print ''
                        
                    else:
                        childOfDetalleCompras = root.createElement('secRetencion1')
                        childOfDetalleCompras.appendChild(root.createTextNode(str(compra.documento_retencion_compra_secuencial)))
                        childOfCompras.appendChild(childOfDetalleCompras)
                else:
                    print 'h'
            
                
                
            #VALIDAR RESULTADOS 0000000
                if compra.documento_retencion_compra_autorizacion:
                    if int(compra.documento_retencion_compra_autorizacion) != 0:
                        childOfDetalleCompras = root.createElement('autRetencion1')
                        childOfDetalleCompras.appendChild(root.createTextNode(str(compra.documento_retencion_compra_autorizacion)))
                        childOfCompras.appendChild(childOfDetalleCompras)
    
                childOfDetalleCompras = root.createElement('fechaEmiRet1')
                childOfDetalleCompras.appendChild(root.createTextNode(compra.documento_retencion_compra_fecha_emision.strftime("%d/%m/%Y")))
                childOfCompras.appendChild(childOfDetalleCompras)
        #-----------------------------------------FIN COMPRAS----------------------------------------


        
        #NOTA DE CREDITOS PRUEBA
        sql_nc=" SELECT  distinct movimiento.fecha_emision,movimiento.nc_establecimiento ,movimiento.nc_punto_emision ,movimiento.nc_secuencial ,movimiento.nc_autorizacion ,movimiento.descripcion as movimiento_descripcion,movimiento.subtotal_0,movimiento.rise,movimiento.porcentaje_iva,movimiento.monto," \
        "proveedor.nombre_proveedor, proveedor.codigo_proveedor,proveedor.pasaporte as proveedor_pasaporte,proveedor.ruc as proveedor_ruc,movimiento.tipo_anticipo_id,movimiento.id as movimiento_id,movimiento_nota_credito.subtotal as base_no_iva_factura ,movimiento_nota_credito.iva as base_iva " \
        "FROM movimiento LEFT JOIN proveedor ON proveedor.proveedor_id=movimiento.proveedor_id LEFT JOIN movimiento_nota_credito ON movimiento_nota_credito.movimiento_id=movimiento.id  and movimiento_nota_credito.proveedor is True WHERE movimiento.tipo_documento_id=3 and " \
        "Extract(month from movimiento.fecha_emision)  ='" + str(mes) + "'and Extract(year from movimiento.fecha_emision) ='" + str(anio) + "'  and movimiento.tipo_anticipo_id=1 and movimiento.activo is  True  and movimiento.ats is True order by movimiento.fecha_emision"
        #print sql_nc
        
        cursor.execute(sql_nc);
        results_nc = namedtuplefetchall(cursor)


        for nc in results_nc:
            #if compra.proveedor_ruc.strip('0'):#QUITAR
            childOfCompras = root.createElement('detalleCompras')
            childOfIvaCompras.appendChild(childOfCompras)

            childOfDetalleCompras = root.createElement('codSustento')
            childOfDetalleCompras.appendChild(root.createTextNode('01'))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('tpIdProv')
            if nc.proveedor_pasaporte:
                childOfDetalleCompras.appendChild(root.createTextNode('03'))
            else:
                if len(nc.proveedor_ruc) > 10:
                    childOfDetalleCompras.appendChild(root.createTextNode('01'))
                elif len(nc.proveedor_ruc) <= 10:
                    childOfDetalleCompras.appendChild(root.createTextNode('02'))

            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('idProv')
            if len(nc.proveedor_ruc) > 10:
                childOfDetalleCompras.appendChild(root.createTextNode(nc.proveedor_ruc.zfill(13)))
            elif len(nc.proveedor_ruc) <= 10:
                childOfDetalleCompras.appendChild(root.createTextNode(nc.proveedor_ruc.zfill(10)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('tipoComprobante')
            #NOTA DE CREDITO
            childOfDetalleCompras.appendChild(root.createTextNode('04'))
            

            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('parteRel')
            childOfDetalleCompras.appendChild(root.createTextNode('NO'))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('fechaRegistro')
            childOfDetalleCompras.appendChild(root.createTextNode(nc.fecha_emision.strftime("%d/%m/%Y")))#REVISAR
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('establecimiento')
            childOfDetalleCompras.appendChild(root.createTextNode(nc.nc_establecimiento))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('puntoEmision')
            childOfDetalleCompras.appendChild(root.createTextNode(str(nc.nc_punto_emision)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('secuencial')
            if nc.nc_secuencial:
                nc_sec=int(nc.nc_secuencial)
            else:
                nc_sec=0
            childOfDetalleCompras.appendChild(root.createTextNode(str(nc_sec)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('fechaEmision')
            childOfDetalleCompras.appendChild(root.createTextNode(compra.fecha_emision.strftime("%d/%m/%Y")))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('autorizacion')
            childOfDetalleCompras.appendChild(root.createTextNode(str(nc.nc_autorizacion)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('baseNoGraIva')
            #childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % nc.base_no_iva_factura)))
            childOfDetalleCompras.appendChild(root.createTextNode(str('0.00')))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('baseImponible')
            if compra.tipo_provision.lower() == 'factura':
                #base_imponible = nc.base_iva_0
                base_imponible = nc.subtotal_0
            elif compra.tipo_provision.lower() == 'nota de venta':
                base_imponible = nc.rise
            else:
                #base_imponible = compra.base_iva_0
                base_imponible = 0 #VALIDAR NULOS
            #childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % base_imponible)))
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            childOfCompras.appendChild(childOfDetalleCompras)

            #Valor de Impo
            childOfDetalleCompras = root.createElement('baseImpGrav')
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % nc.base_no_iva_factura)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('baseImpExe')#REVISAR
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('montoIce')
            #childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % nc.valor_ice)))
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            childOfCompras.appendChild(childOfDetalleCompras)

            #Valor de IVA
            childOfDetalleCompras = root.createElement('montoIva')
            childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % nc.base_iva)))
            childOfCompras.appendChild(childOfDetalleCompras)

            #RETENCIONES MAYORES QUE MONTO IVA GENERAN ERROR
            childOfDetalleCompras = root.createElement('valRetBien10')
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            #childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valretbien10)))
            childOfCompras.appendChild(childOfDetalleCompras)
            # 
            childOfDetalleCompras = root.createElement('valRetServ20')
            #childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valretserv20
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            childOfCompras.appendChild(childOfDetalleCompras)
            # 
            childOfDetalleCompras = root.createElement('valorRetBienes')# RETENCION 30%
            # childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valretbien30)))
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            childOfCompras.appendChild(childOfDetalleCompras)
            # 
            childOfDetalleCompras = root.createElement('valRetServ50')# NO APLICA (SOLO EMPRESAS MINERAS)
            # childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            childOfCompras.appendChild(childOfDetalleCompras)
            # 
            childOfDetalleCompras = root.createElement('valorRetServicios')# RETENCION 70%
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            # childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valretserv70)))
            childOfCompras.appendChild(childOfDetalleCompras)
            # 
            childOfDetalleCompras = root.createElement('valRetServ100')
            childOfDetalleCompras.appendChild(root.createTextNode('0.00'))
            # childOfDetalleCompras.appendChild(root.createTextNode(str("%.2f" % compra.valretserv100)))
            childOfCompras.appendChild(childOfDetalleCompras)

            childOfDetalleCompras = root.createElement('totbasesImpReemb')
            childOfDetalleCompras.appendChild(root.createTextNode('0.00')) #NO APLICA
            childOfCompras.appendChild(childOfDetalleCompras)

            #---------------------------PAGO EXTERIOR----------------------
            childOfDetalleComprasPagoExterior = root.createElement('pagoExterior')
            childOfCompras.appendChild(childOfDetalleComprasPagoExterior)

            childOfPagoExterior = root.createElement('pagoLocExt')
            childOfPagoExterior.appendChild(root.createTextNode("01"))
            childOfDetalleComprasPagoExterior.appendChild(childOfPagoExterior)

            childOfPagoExterior = root.createElement('paisEfecPago')
            childOfPagoExterior.appendChild(root.createTextNode("NA"))
            childOfDetalleComprasPagoExterior.appendChild(childOfPagoExterior)

            childOfPagoExterior = root.createElement('aplicConvDobTrib')
            childOfPagoExterior.appendChild(root.createTextNode("NA"))
            childOfDetalleComprasPagoExterior.appendChild(childOfPagoExterior)

            childOfPagoExterior = root.createElement('pagExtSujRetNorLeg')
            childOfPagoExterior.appendChild(root.createTextNode("NA"))
            childOfDetalleComprasPagoExterior.appendChild(childOfPagoExterior)
            
            #-----------------------FIN PAGO EXTERIOR----------------------


            #-----------------------INICIO FORMAS DE PAGO----------------------
            # Cuando la suma de las BASES IMPONIBLES y los MONTOS de IVA e ICE exceden los USD. 1000.00.
            if float(nc.base_no_iva_factura) + float(base_imponible)  + float(nc.base_iva) >= 1000:
                childOfDetalleComprasFormasDePago = root.createElement('formasDePago')
                childOfCompras.appendChild(childOfDetalleComprasFormasDePago)
                childOfFormaDePago = root.createElement('formaPago')#VALIDAR LA FORMA DE PAGO
                childOfFormaDePago.appendChild(root.createTextNode(""))
                childOfDetalleComprasFormasDePago.appendChild(childOfFormaDePago)

            
            
            
            sql_factura = "SELECT  distinct documento_compra.fecha_emision,documento_compra.establecimiento as f_establecimiento,documento_compra.punto_emision as f_punto_emision,documento_compra.secuencial as f_secuencial,documento_compra.autorizacion as f_autorizacion" \
            " FROM documento_compra,movimiento_nota_credito where  documento_compra.id=movimiento_nota_credito.documento_compra_id and  movimiento_nota_credito.movimiento_id=" + str(nc.movimiento_id) 
            #print sql_factura
            cursor.execute(sql_factura);
            results_factura = namedtuplefetchall(cursor)
            
            for f in results_factura:
                docModificado='01'
                estabModificado=f.f_establecimiento
                ptoEmiModificado=f.f_punto_emision
                secModificado=f.f_secuencial
                autModificado=f.f_autorizacion

            
            childOfDetalleCompras = root.createElement('docModificado')
            childOfDetalleCompras.appendChild(root.createTextNode(str(docModificado)))
            childOfCompras.appendChild(childOfDetalleCompras)
            childOfDetalleCompras = root.createElement('estabModificado')
            childOfDetalleCompras.appendChild(root.createTextNode(str(estabModificado)))
            childOfCompras.appendChild(childOfDetalleCompras)
            
            
            childOfDetalleCompras = root.createElement('ptoEmiModificado')
            childOfDetalleCompras.appendChild(root.createTextNode(str(ptoEmiModificado)))
            childOfCompras.appendChild(childOfDetalleCompras)
            
            
            childOfDetalleCompras = root.createElement('secModificado')
            childOfDetalleCompras.appendChild(root.createTextNode(str(secModificado)))
            childOfCompras.appendChild(childOfDetalleCompras)
            
            childOfDetalleCompras = root.createElement('autModificado')
            childOfDetalleCompras.appendChild(root.createTextNode(str(autModificado)))
            childOfCompras.appendChild(childOfDetalleCompras)
            
            
            
            # cont=0
            # 
            # for air in results_retenciones_air:
            
            
            
        #-----------------------------------------FIN NOTA DE CREDITO----------------------------------------

        
        
        
        #-----------------------------------------INICIO VENTAS----------------------------------------

        childOfIvaVentas = root.createElement('ventas')
        xml.appendChild(childOfIvaVentas)
        """
        sql_ventas = "SELECT  distinct dv.id," \
                     "dv.fecha_emision," \
                     "dv.establecimiento," \
                     "dv.punto_emision," \
                     "dv.secuencial," \
                     "dv.autorizacion," \
                     "dv.descripcion," \
                     "dv.base_iva_0," \
                     "dv.valor_iva_0," \
                     "dv.valor_ice," \
                     "dv.base_iva," \
                     "dv.valor_iva," \
                     "dv.porcentaje_iva," \
                     "dv.subtotal," \
                     "dv.descuento," \
                     "dv.total," \
                     "c.nombre_cliente," \
                     "c.codigo_cliente," \
                     "c.ruc as cliente_ruc," \
                     "c.pasaporte as cliente_pasaporte," \
                     "p.nombre as puntos_venta_nombre," \
                     "dv.activo," \
                     "r.codigo_razon_social," \
                     "r.nombre as razon_social_nombre," \
                     "r.ruc as razon_social_ruc " \
                     "FROM documento_venta dv " \
                     "LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id " \
                     "LEFT JOIN puntos_venta p ON dv.punto_venta_id=p.id  " \
                     "LEFT JOIN razon_social r ON r.id=dv.razon_social_id " \
                     "where dv.razon_social_id is NULL and Extract(month from dv.fecha_emision)  ='" + str(mes) + "' and Extract(year from dv.fecha_emision) ='" + str(anio) +  "';"
                    """

        sql_ventas = "SELECT distinct " \
                     "sum(dv.base_iva_0) as base_iva_0, " \
                     "sum(dv.valor_iva_0) as valor_iva_0, " \
                     "sum(dv.valor_ice) as valor_ice, " \
                     "sum(dv.base_iva) as base_iva, " \
                     "sum(dv.valor_iva) as valor_iva, " \
                     "sum(dv.descuento) as descuento, " \
                     "sum(dv.total) as total, " \
                     "c.ruc as cliente_ruc, " \
                     "c.pasaporte as cliente_pasaporte," \
                     "c.id_cliente as cliente_id," \
                     "((sum(dv.subtotal) * ((sum(dv.porcentaje_iva)/count(*))/100))) as monto_iva_total," \
                     "(count(*)) as numero_facturas,c.cedula as cliente_cedula " \
                     "FROM documento_venta dv " \
                     "LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id " \
                     "LEFT JOIN puntos_venta p ON dv.punto_venta_id=p.id " \
                     "LEFT JOIN razon_social r ON r.id=dv.razon_social_id " \
                     "WHERE dv.razon_social_id is NULL and  Extract(month from dv.fecha_emision)  ='" + str(mes) + "'" \
                     "AND Extract(year from dv.fecha_emision) ='" + str(anio) +  "' AND dv.activo is True  AND dv.facturacion_eletronica is True GROUP BY cliente_ruc, cliente_pasaporte, c.id_cliente,cliente_cedula;"
        # print sql_ventas
        # print '-----------------2----------------------------------'
        cursor.execute(sql_ventas);
        results = namedtuplefetchall(cursor)

        for venta in results:
            #if venta.cliente_ruc.strip('0') != '': # QUITAR
            childOfVentas = root.createElement('detalleVentas')
            childOfIvaVentas.appendChild(childOfVentas)

            childOfDetalleVentas = root.createElement('tpIdCliente')
            if venta.cliente_pasaporte:
                childOfDetalleVentas.appendChild(root.createTextNode('06'))
            else:
                if venta.cliente_cedula:
                    childOfDetalleVentas.appendChild(root.createTextNode('05'))
                else:
                    if len(venta.cliente_ruc) > 10:
                        childOfDetalleVentas.appendChild(root.createTextNode('04'))
                    elif len(venta.cliente_ruc) <= 10:
                        childOfDetalleVentas.appendChild(root.createTextNode('05'))
                    # CONSUMIDOR FINAL? 07

            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('idCliente')
            if len(venta.cliente_ruc) <= 10:
                childOfDetalleVentas.appendChild(root.createTextNode(venta.cliente_ruc.zfill(10)))
            elif len(venta.cliente_ruc) > 10:
                childOfDetalleVentas.appendChild(root.createTextNode(venta.cliente_ruc.zfill(13)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('parteRelVtas')
            childOfDetalleVentas.appendChild(root.createTextNode('NO'))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('tipoComprobante')
            childOfDetalleVentas.appendChild(root.createTextNode('18'))#VALIDAR SI ES NOTA DE CREDITO O FACTURA
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('tipoEmision')
            childOfDetalleVentas.appendChild(root.createTextNode('F'))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('numeroComprobantes')
            childOfDetalleVentas.appendChild(root.createTextNode(str(venta.numero_facturas)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('baseNoGraIva')
            childOfDetalleVentas.appendChild(root.createTextNode('0.00'))#REVISAR
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('baseImponible')
            if not (venta.base_iva_0 is None):
                childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % venta.base_iva_0)))
            else:
                childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % 0)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('baseImpGrav')
            childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % venta.base_iva)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('montoIva')
            childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % venta.valor_iva)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('montoIce')
            if not (venta.valor_ice is None):
                childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % venta.valor_ice)))
            else:
                childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % 0)))

            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('valorRetIva')#SUMA RETENCIONES IVA = 2

            #CAMBIO KORBAN SOLO LAS FACTURAS ACTIVOS Y LOS DOCUMENTOS DE RETENCION ACTIVOS
            sel_valorRetIva = "(SELECT COALESCE( (" \
                              "SELECT sum(drdv.valor_retenido) " \
                              "FROM documento_venta dv " \
                              "INNER JOIN documento_retencion_venta drv  on drv.documento_venta_id = dv.id  and drv.anulado is False " \
                              "INNER JOIN documento_retencion_detalle_venta drdv on drdv.documento_retencion_venta_id = drv.id " \
                              "INNER JOIN retencion_detalle rd on rd.id = drdv.retencion_detalle_id and rd.tipo_retencion_id = 2 " \
                              "WHERE dv.cliente_id = '" + str(venta.cliente_id) +  "' AND dv.activo is True AND dv.razon_social_id is NULL " \
                              "AND Extract(month from dv.fecha_emision) ='" + str(mes) +  "'" \
                              "AND Extract(year from dv.fecha_emision) ='" + str(anio) +  "'), 0) as valorRetIva) "
            
            # print '-----------------30----------------------------------'
            # print sel_valorRetIva
            # # print '-----------------31----------------------------------'
        
            cursor.execute(sel_valorRetIva);
            valorRetIva = cursor.fetchone()[0]
            childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % valorRetIva)))
            childOfVentas.appendChild(childOfDetalleVentas)

            #CAMBIO KORBAN SOLO LAS FACTURAS ACTIVOS Y LOS DOCUMENTOS DE RETENCION ACTIVOS
            childOfDetalleVentas = root.createElement('valorRetRenta')#SUMA RETENCIONES FUENTE
            sel_valorRetRenta = "(SELECT COALESCE( (" \
                              "SELECT sum(drdv.valor_retenido) " \
                              "FROM documento_venta dv " \
                              "INNER JOIN documento_retencion_venta drv  on drv.documento_venta_id = dv.id and drv.anulado is False " \
                              "INNER JOIN documento_retencion_detalle_venta drdv on drdv.documento_retencion_venta_id = drv.id " \
                              "INNER JOIN retencion_detalle rd on rd.id = drdv.retencion_detalle_id and rd.tipo_retencion_id = 1 " \
                              "WHERE dv.cliente_id = '" + str(venta.cliente_id) + "' AND dv.activo is True AND dv.razon_social_id is NULL  " \
                              "AND Extract(month from dv.fecha_emision) ='" + str(mes) + "'" \
                              "AND Extract(year from dv.fecha_emision) ='" + str(anio) + "'), 0) as valorRetIva) "
            # print '-----------------40----------------------------------'
            # print sel_valorRetRenta
            # print '-----------------4----------------------------------'
            # 
            
        
            cursor.execute(sel_valorRetRenta);
            valorRetRenta = cursor.fetchone()[0]
            if valorRetRenta:
                valorRetRenta=valorRetRenta
            else:
                valorRetRenta=0
            
            if valorRetRenta == 'nan':
                valorRetRenta=0
            if valorRetRenta == ' ':
                valorRetRenta=0
            if valorRetRenta is None:
                valorRetRenta=0
            print valorRetRenta
            print '----------------77-4----------------------------------'
            
            childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % valorRetRenta)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentasFormasDePago = root.createElement('formasDePago')
            childOfVentas.appendChild(childOfDetalleVentasFormasDePago)

            childOfFormasDePago = root.createElement('formaPago')
            childOfFormasDePago.appendChild(root.createTextNode('20'))#BUSCAR EN DB (NO ESTA EL CAMPO EN EL MODELO)
            childOfDetalleVentasFormasDePago.appendChild(childOfFormasDePago)

          
          
        #------------------VENTAS POR RAZONES SOCIALES----------------------------
        sql_ventas = "SELECT distinct " \
                     "sum(dv.base_iva_0) as base_iva_0, " \
                     "sum(dv.valor_iva_0) as valor_iva_0, " \
                     "sum(dv.valor_ice) as valor_ice, " \
                     "sum(dv.base_iva) as base_iva, " \
                     "sum(dv.valor_iva) as valor_iva, " \
                     "sum(dv.descuento) as descuento, " \
                     "sum(dv.total) as total, " \
                     "r.ruc as cliente_ruc, " \
                     "c.ruc as cliente_pasaporte," \
                     "c.id_cliente as cliente_id," \
                     "((sum(dv.subtotal) * ((sum(dv.porcentaje_iva)/count(*))/100))) as monto_iva_total," \
                     "(count(*)) as numero_facturas,r.tipo_cliente_id as tipo_cliente " \
                     "FROM documento_venta dv " \
                     "LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id " \
                     "LEFT JOIN puntos_venta p ON dv.punto_venta_id=p.id " \
                     "LEFT JOIN razon_social r ON r.id=dv.razon_social_id " \
                     "WHERE dv.razon_social_id is NOT NULL and Extract(month from dv.fecha_emision)  ='" + str(mes) + "'" \
                     "AND Extract(year from dv.fecha_emision) ='" + str(anio) +  "' AND dv.activo is True AND dv.facturacion_eletronica is True GROUP BY cliente_ruc, cliente_pasaporte, c.id_cliente,r.tipo_cliente_id;"
        # print sql_ventas
        # print '-----------------2----------------------------------'
        cursor.execute(sql_ventas);
        results = namedtuplefetchall(cursor)

        for venta in results:
            #if venta.cliente_ruc.strip('0') != '': # QUITAR
            childOfVentas = root.createElement('detalleVentas')
            childOfIvaVentas.appendChild(childOfVentas)

            childOfDetalleVentas = root.createElement('tpIdCliente')
            # if venta.cliente_pasaporte:
            #     childOfDetalleVentas.appendChild(root.createTextNode('06'))
            # else:
            #     if len(venta.cliente_ruc) > 10:
            #         childOfDetalleVentas.appendChild(root.createTextNode('04'))
            #     elif len(venta.cliente_ruc) <= 10:
            #         childOfDetalleVentas.appendChild(root.createTextNode('05'))
            if venta.tipo_cliente==9:
                childOfDetalleVentas.appendChild(root.createTextNode('06'))
                

            else:
                
                if len(venta.cliente_ruc) > 10:
                    childOfDetalleVentas.appendChild(root.createTextNode('04'))
                elif len(venta.cliente_ruc) <= 10:
                    childOfDetalleVentas.appendChild(root.createTextNode('05'))
                    # CONSUMIDOR FINAL? 07

            childOfVentas.appendChild(childOfDetalleVentas)
            

            childOfDetalleVentas = root.createElement('idCliente')
            if len(venta.cliente_ruc) <= 10:
                childOfDetalleVentas.appendChild(root.createTextNode(venta.cliente_ruc.zfill(10)))
            elif len(venta.cliente_ruc) > 10:
                childOfDetalleVentas.appendChild(root.createTextNode(venta.cliente_ruc.zfill(13)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('parteRelVtas')
            childOfDetalleVentas.appendChild(root.createTextNode('NO'))
            childOfVentas.appendChild(childOfDetalleVentas)
            if venta.tipo_cliente==9:
                childOfDetalleVentas = root.createElement('tipoCliente')
                childOfDetalleVentas.appendChild(root.createTextNode('01'))
                childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('tipoComprobante')
            childOfDetalleVentas.appendChild(root.createTextNode('18'))#VALIDAR SI ES NOTA DE CREDITO O FACTURA
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('tipoEmision')
            childOfDetalleVentas.appendChild(root.createTextNode('F'))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('numeroComprobantes')
            childOfDetalleVentas.appendChild(root.createTextNode(str(venta.numero_facturas)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('baseNoGraIva')
            childOfDetalleVentas.appendChild(root.createTextNode('0.00'))#REVISAR
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('baseImponible')
            if not (venta.base_iva_0 is None):
                childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % venta.base_iva_0)))
            else:
                childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % 0)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('baseImpGrav')
            #Se suma el subtotal- descuentos
            # print 'Desuentos:'
            # print venta.descuento
            total_base_imp=float(venta.base_iva)-float(venta.descuento)
            childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % total_base_imp)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('montoIva')
            childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % venta.valor_iva)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('montoIce')
            if not (venta.valor_ice is None):
                childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % venta.valor_ice)))
            else:
                childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % 0)))

            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentas = root.createElement('valorRetIva')#SUMA RETENCIONES IVA = 2

            #CAMBIO KORBAN SOLO LAS FACTURAS ACTIVOS Y LOS DOCUMENTOS DE RETENCION ACTIVOS
            sel_valorRetIva = "(SELECT COALESCE( (" \
                              "SELECT sum(drdv.valor_retenido) " \
                              "FROM documento_venta dv " \
                              "INNER JOIN documento_retencion_venta drv  on drv.documento_venta_id = dv.id  and drv.anulado is False " \
                              "INNER JOIN documento_retencion_detalle_venta drdv on drdv.documento_retencion_venta_id = drv.id " \
                              "INNER JOIN retencion_detalle rd on rd.id = drdv.retencion_detalle_id and rd.tipo_retencion_id = 2 " \
                              "WHERE dv.cliente_id = '" + str(venta.cliente_id) +  "' AND dv.activo is True  AND dv.razon_social_id is NOT NULL  " \
                              "AND Extract(month from dv.fecha_emision) ='" + str(mes) +  "'" \
                              "AND Extract(year from dv.fecha_emision) ='" + str(anio) +  "'), 0) as valorRetIva) "
            
            # print '-----------------30----------------------------------'
            # print sel_valorRetIva
            # print '-----------------31----------------------------------'
        
            cursor.execute(sel_valorRetIva);
            valorRetIva = cursor.fetchone()[0]
            childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % valorRetIva)))
            childOfVentas.appendChild(childOfDetalleVentas)

            #CAMBIO KORBAN SOLO LAS FACTURAS ACTIVOS Y LOS DOCUMENTOS DE RETENCION ACTIVOS
            childOfDetalleVentas = root.createElement('valorRetRenta')#SUMA RETENCIONES FUENTE
            sel_valorRetRenta = "(SELECT COALESCE( (" \
                              "SELECT sum(drdv.valor_retenido) " \
                              "FROM documento_venta dv " \
                              "INNER JOIN documento_retencion_venta drv  on drv.documento_venta_id = dv.id and drv.anulado is False " \
                              "INNER JOIN documento_retencion_detalle_venta drdv on drdv.documento_retencion_venta_id = drv.id " \
                              "INNER JOIN retencion_detalle rd on rd.id = drdv.retencion_detalle_id and rd.tipo_retencion_id = 1 " \
                              "WHERE dv.cliente_id = '" + str(venta.cliente_id) + "' AND dv.activo is True AND dv.razon_social_id is NOT NULL  " \
                              "AND Extract(month from dv.fecha_emision) ='" + str(mes) + "'" \
                              "AND Extract(year from dv.fecha_emision) ='" + str(anio) + "'), 0) as valorRetIva) "
            # print '-----------------40----------------------------------'
            # print sel_valorRetRenta
            # print '-----------------4----------------------------------'
        
            
        
            cursor.execute(sel_valorRetRenta);
            valorRetRenta = cursor.fetchone()[0]
            if valorRetRenta:
                valorRetRenta=valorRetRenta
            else:
                valorRetRenta=0
            
            if valorRetRenta == 'nan':
                valorRetRenta=0
            if valorRetRenta == 'NaN':
                valorRetRenta=0
            if math.isnan(valorRetRenta):
                valorRetRenta=0
                print 'Valor de nan'
            
            if float(valorRetRenta) == float('nan'):
                valorRetRenta=0
                
            if valorRetRenta == ' ':
                valorRetRenta=0
            if valorRetRenta is None:
                valorRetRenta=0
            print valorRetRenta
            print '----------------775----------------------------------'
            childOfDetalleVentas.appendChild(root.createTextNode(str("%.2f" % valorRetRenta)))
            childOfVentas.appendChild(childOfDetalleVentas)

            childOfDetalleVentasFormasDePago = root.createElement('formasDePago')
            childOfVentas.appendChild(childOfDetalleVentasFormasDePago)

            childOfFormasDePago = root.createElement('formaPago')
            childOfFormasDePago.appendChild(root.createTextNode('20'))#BUSCAR EN DB (NO ESTA EL CAMPO EN EL MODELO)
            childOfDetalleVentasFormasDePago.appendChild(childOfFormasDePago)

          
            #-----------------------------------------FIN VENTAS----------------------------------------


            #-----------------------------------------INICIO VENTAS ESTABLECIMIENTO----------------------------------------
        childOfIvaVentasEstablecimiento = root.createElement('ventasEstablecimiento')
        xml.appendChild(childOfIvaVentasEstablecimiento)
        #CAMBIO KORBAN SOLO LAS FACTURAS ACTIVAS

        # sql_ventas_establecimiento = "SELECT pv.establecimiento AS code_estab, " \
        #                              "(SELECT COALESCE( (round (sum(dv.total)::DECIMAL, 2)::DECIMAL), 0) AS ventas_estab), " \
        #                              "(SELECT COALESCE( (round (sum(0)::DECIMAL, 2)::DECIMAL), 0) AS iva_comp) " \
        #                              "FROM puntos_venta pv LEFT OUTER JOIN documento_venta dv on dv.establecimiento = pv.establecimiento and Extract(month from dv.fecha_emision) = '" + str(mes) + "'  and Extract(year from dv.fecha_emision)='" + str(anio) + "'" \
        #                              " and dv.activo is True GROUP BY pv.establecimiento ORDER BY pv.establecimiento ASC"
        sql_ventas_establecimiento = "SELECT pv.establecimiento AS code_estab, " \
                                     "(SELECT COALESCE( (round (sum(dv.base_iva)::DECIMAL, 2)::DECIMAL), 0) AS ventas_estab), " \
                                     "(SELECT COALESCE( (round (sum(0)::DECIMAL, 2)::DECIMAL), 0) AS iva_comp) " \
                                     "FROM puntos_venta pv LEFT OUTER JOIN documento_venta dv on dv.establecimiento = pv.establecimiento and Extract(month from dv.fecha_emision) = '" + str(mes) + "'  and Extract(year from dv.fecha_emision)='" + str(anio) + "'" \
                                     " and dv.activo is True and dv.facturacion_eletronica is True GROUP BY pv.establecimiento ORDER BY pv.establecimiento ASC"
        # print '-----------------50----------------------------------'
        # print sql_ventas_establecimiento
        # print '-----------------51----------------------------------'
        # 
        
        cursor.execute(sql_ventas_establecimiento);
        results_ventas_establecimiento = namedtuplefetchall(cursor)

        for venta_establecimiento in results_ventas_establecimiento:
            childOfVentasEstablecimiento = root.createElement('ventaEst')
            childOfIvaVentasEstablecimiento.appendChild(childOfVentasEstablecimiento)

            childOfDetalleVentasEstablecimiento = root.createElement('codEstab')
            childOfDetalleVentasEstablecimiento.appendChild(root.createTextNode(str(venta_establecimiento.code_estab)))
            childOfVentasEstablecimiento.appendChild(childOfDetalleVentasEstablecimiento)

            childOfDetalleVentasEstablecimiento = root.createElement('ventasEstab')
            #CAMBIO KORBAN SOLO LAS FACTURAS ACTIVAS
            # sql_total_ventas_establecimiento = "SELECT COALESCE( (sum(dv.total)), 0) as total " \
            #                    "FROM documento_venta dv " \
            #                    "LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id " \
            #                    "LEFT JOIN puntos_venta p ON dv.punto_venta_id=p.id " \
            #                    "LEFT JOIN razon_social r ON r.id=dv.razon_social_id " \
            #                    "WHERE Extract(month from dv.fecha_emision) ='" + str(mes) + "'" \
            #                    "AND Extract(year from dv.fecha_emision) ='" + str(anio) + "'" \
            #                    "AND dv.establecimiento = '" + str(venta_establecimiento.code_estab) + "' and dv.activo is True;"
            
            sql_total_ventas_establecimiento = "SELECT COALESCE( (sum(dv.base_iva)), 0) as total,COALESCE( (sum(dv.descuento)), 0) as descuento " \
                               "FROM documento_venta dv " \
                               "LEFT JOIN cliente c ON c.id_cliente=dv.cliente_id " \
                               "LEFT JOIN puntos_venta p ON dv.punto_venta_id=p.id " \
                               "LEFT JOIN razon_social r ON r.id=dv.razon_social_id " \
                               "WHERE Extract(month from dv.fecha_emision) ='" + str(mes) + "'" \
                               "AND Extract(year from dv.fecha_emision) ='" + str(anio) + "'" \
                               "AND dv.establecimiento = '" + str(venta_establecimiento.code_estab) + "' and dv.activo is True and dv.facturacion_eletronica is True;"
        
            
            # print '-----------------60----------------------------------'
            # print sql_total_ventas_establecimiento
            # print '-----------------61------------------------------'
        
            cursor.execute(sql_total_ventas_establecimiento);
            arr_total_ventas_establecimiento = cursor.fetchone()
            
            subtotal_ventas_establecimiento = arr_total_ventas_establecimiento[0]
            descuento_ventas_establecimiento = arr_total_ventas_establecimiento[1]
            # print  arr_ventas[0]
            # print  arr_ventas[2]
            #total_ventas = cursor.fetchone()[0]
            total_ventas_establecimiento=subtotal_ventas_establecimiento-descuento_ventas_establecimiento

            childOfDetalleVentasEstablecimiento.appendChild(root.createTextNode(str("%.2f" % total_ventas_establecimiento)))
            childOfVentasEstablecimiento.appendChild(childOfDetalleVentasEstablecimiento)

            childOfDetalleVentasEstablecimiento = root.createElement('ivaComp')
            childOfDetalleVentasEstablecimiento.appendChild(root.createTextNode(str("%.2f" % venta_establecimiento.iva_comp)))
            childOfVentasEstablecimiento.appendChild(childOfDetalleVentasEstablecimiento)

        #-----------------------------------------FIN VENTAS ESTABLECIMIENTO----------------------------------------

        #-----------------------------------------INICIO ANULACIONES----------------------------------------
        childOfIvaAnulados = root.createElement('anulados')
        xml.appendChild(childOfIvaAnulados)

        sql_anulaciones_documento_venta = "SELECT DISTINCT dv.id, dv.fecha_emision, " \
                                     "dv.establecimiento, " \
                                     "dv.punto_emision, " \
                                     "dv.secuencial, " \
                                     "dv.autorizacion, " \
                                     "dv.activo " \
                                     "FROM documento_venta dv " \
                                     "WHERE EXTRACT(month from dv.fecha_emision)  = '" + str(mes) + "'" \
                                     "AND EXTRACT(year FROM dv.fecha_emision) = '" + str(anio) + "'" \
                                     "AND dv.activo = FALSE AND dv.facturacion_eletronica is True"

        cursor.execute(sql_anulaciones_documento_venta);
        anulaciones_documento_venta = namedtuplefetchall(cursor)


        for anulacion in anulaciones_documento_venta:
            childOfAnulado = root.createElement('detalleAnulados')
            childOfIvaAnulados.appendChild(childOfAnulado)

            childOfDetalleAnulado = root.createElement('tipoComprobante')
            childOfDetalleAnulado.appendChild(root.createTextNode("01"))
            childOfAnulado.appendChild(childOfDetalleAnulado)

            childOfDetalleAnulado = root.createElement('establecimiento')
            childOfDetalleAnulado.appendChild(root.createTextNode(str(anulacion.establecimiento)))
            childOfAnulado.appendChild(childOfDetalleAnulado)

            childOfDetalleAnulado = root.createElement('puntoEmision')
            childOfDetalleAnulado.appendChild(root.createTextNode(str(anulacion.punto_emision)))
            childOfAnulado.appendChild(childOfDetalleAnulado)
            
            #VALIDAR SECUENCIAL
            if anulacion.secuencial:
                if int(anulacion.secuencial) != 0:
                    childOfDetalleAnulado = root.createElement('secuencialInicio')
                    childOfDetalleAnulado.appendChild(root.createTextNode(str(anulacion.secuencial)[-5:]))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
                else:
                    childOfDetalleAnulado = root.createElement('secuencialInicio')
                    childOfDetalleAnulado.appendChild(root.createTextNode('0'))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
               
                    

            #VALIDAR SECUENCIAL
            if anulacion.secuencial:
                if int(anulacion.secuencial) != 0:
                    childOfDetalleAnulado = root.createElement('secuencialFin')
                    childOfDetalleAnulado.appendChild(root.createTextNode(str(anulacion.secuencial)[-5:]))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
                else:
                    childOfDetalleAnulado = root.createElement('secuencialFin')
                    childOfDetalleAnulado.appendChild(root.createTextNode('0'))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
               
                    
            if anulacion.secuencial:
                if int(anulacion.secuencial) != 0:
                    childOfDetalleAnulado = root.createElement('autorizacion')
                    childOfDetalleAnulado.appendChild(root.createTextNode(str(anulacion.autorizacion)))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
                else:
                    childOfDetalleAnulado = root.createElement('autorizacion')
                    childOfDetalleAnulado.appendChild('0')
                    childOfAnulado.appendChild(childOfDetalleAnulado)
                    

        sql_anulaciones_retencion_compra = "SELECT DISTINCT dc.anulado, " \
                                           "dc.tipo_provision, " \
                                           "drc.establecimiento, " \
                                           "drc.punto_emision, " \
                                           "drc.secuencial, " \
                                           "drc.autorizacion " \
                                           "FROM documento_retencion_compra drc " \
                                           "LEFT JOIN documento_compra dc ON dc.id = drc.documento_compra_id " \
                                           "WHERE dc.anulado = TRUE AND dc.ats is True " \
                                           "AND Extract(month FROM drc.fecha_emision) = '" + str(mes) + "'" \
                                           "AND Extract(year FROM drc.fecha_emision) = '" + str(anio) + "'"

        cursor.execute(sql_anulaciones_retencion_compra);
        anulaciones_retencion_compra = namedtuplefetchall(cursor)

        for anulacion in anulaciones_retencion_compra:
            if anulacion.secuencial:
                if int(anulacion.secuencial) != 0:
                    childOfAnulado = root.createElement('detalleAnulados')
                    childOfIvaAnulados.appendChild(childOfAnulado)
        
                    childOfDetalleAnulado = root.createElement('tipoComprobante')
                    childOfDetalleAnulado.appendChild(root.createTextNode("07"))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
        
                    childOfDetalleAnulado = root.createElement('establecimiento')
                    childOfDetalleAnulado.appendChild(root.createTextNode(str(anulacion.establecimiento)))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
        
                    childOfDetalleAnulado = root.createElement('puntoEmision')
                    childOfDetalleAnulado.appendChild(root.createTextNode(str(anulacion.punto_emision)))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
            #validacion ultima secuencial inicio
            if anulacion.secuencial:
                if int(anulacion.secuencial) != 0:
                    childOfDetalleAnulado = root.createElement('secuencialInicio')
                    childOfDetalleAnulado.appendChild(root.createTextNode(str(anulacion.secuencial)[-5:]))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
                #else:
                    # childOfDetalleAnulado = root.createElement('secuencialInicio')
                    # childOfDetalleAnulado.appendChild(root.createTextNode('0'))
                    # childOfAnulado.appendChild(childOfDetalleAnulado)
                

            if anulacion.secuencial:
                if int(anulacion.secuencial) != 0:
                    childOfDetalleAnulado = root.createElement('secuencialFin')
                    childOfDetalleAnulado.appendChild(root.createTextNode(str(anulacion.secuencial)[-5:]))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
                # else:
                #     childOfDetalleAnulado = root.createElement('secuencialFin')
                #     childOfDetalleAnulado.appendChild(root.createTextNode('0'))
                #     childOfAnulado.appendChild(childOfDetalleAnulado)
                    
                
            if anulacion.secuencial:
                if int(anulacion.secuencial) != 0:
                    childOfDetalleAnulado = root.createElement('autorizacion')
                    childOfDetalleAnulado.appendChild(root.createTextNode(str(anulacion.autorizacion)))
                    childOfAnulado.appendChild(childOfDetalleAnulado)
                # else:
                #     childOfDetalleAnulado = root.createElement('autorizacion')
                #     childOfDetalleAnulado.appendChild(root.createTextNode('0'))
                #     childOfAnulado.appendChild(childOfDetalleAnulado)
        #-----------------------------------------FIN ANULACIONES----------------------------------------

        xmlFile = StringIO.StringIO()
        xmlFile.write(root.toprettyxml(encoding="UTF-8"))

        # generate the file
        response = HttpResponse(xmlFile.getvalue(), content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=AT-' + mes.zfill(2) + anio + '.xml'
        response['Content-Length'] = xmlFile.tell()
        return response
    else:
        raise Http404

# =====================================================#
