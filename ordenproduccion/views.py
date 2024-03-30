from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, eliminarByPkView
from django.core.urlresolvers import reverse_lazy,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render,render_to_response
from django.contrib import messages
import simplejson as json
import datetime
from .models import *
from .forms import *
from .tables import *
from .filters import *
from clientes.models import *
from django.views.generic import TemplateView
from django import forms
from django.forms.extras.widgets import *
from django.contrib.auth import authenticate,login
from inventario.tables import *
#from login.lib.tools import Tools
from inventario.models import *
from django.db import connection, transaction
from config.models import *
from subordenproduccion.models import *
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
#from config.models import Mensajes



from login.lib.tools import Tools
from django.contrib import auth
from django.db import IntegrityError, transaction


@login_required()
def OrdenProduccionListView(request):
    #ordenes = OrdenProduccion.objects.all().order_by('id')
    ordenes=''
    #OrdenProduccion.objects.all().order_by('id')


    return render_to_response('ordenproduccion/list.html', {'ordenes': ordenes}, RequestContext(request))


@transaction.atomic
def OrdenProduccionCreateView(request):
      if request.method == 'POST':
        ordenproduccion_form=OrdenProduccionForm(request.POST)
        productos = Producto.objects.all()
        ambientes = Ambiente.objects.all()

        cursor = connection.cursor();
        cursor.execute("SELECT pd.id,p.codigo,p.fecha,p.cliente_id,p.vendedor_id,p.fechaentrega,pd.pedido_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.imagen,c.nombre_cliente,pd.producto_id,pd.detalle,pd.medida,pd.reparacion,pd.codigo_produccion from pedido p,pedido_detalle pd,cliente c where pd.pedido_id=p.id and c.id_cliente=p.cliente_id and p.aprobada=true and pd.no_producir!=True and NOT EXISTS (select * from orden_produccion op  where op.pedido_detalle_id=pd.id)");
        row = cursor.fetchall();
        if ordenproduccion_form.is_valid():
            try:
                with transaction.atomic():
                    new_orden=ordenproduccion_form.save()
                    new_orden.created_at = datetime.now()
                    new_orden.created_by = request.user.get_full_name()
                    new_orden.updated_by = request.user.get_full_name()
                    if 'imagen' in request.FILES:
                        new_orden.imagen=request.FILES["imagen"]
                    if 'imagen_global' in request.FILES:
                        new_orden.imagen_global=request.FILES["imagen_global"]
                    else:
                        id_ped=request.POST["deta"]
                        pedDet = PedidoDetalle.objects.get(id=id_ped)
                        if pedDet:
                            if pedDet.imagen:
                                new_orden.imagen = pedDet.imagen
                            else:
                                prod = Producto.objects.get(producto_id=pedDet.producto_id)
                                if prod:
                                    new_orden.imagen =prod.imagen
                    new_orden.pedido_detalle_id=request.POST["deta"]
                    new_orden.pedido_id=request.POST["pedido"]
                    new_orden.save()
                    try:
                        if new_orden.garantia or new_orden.tipo == 'OR':
                            secuencial = Secuenciales.objects.get(modulo='ordenreparacion')
                        else:
                            secuencial = Secuenciales.objects.get(modulo='ordenproduccion')
                        secuencial.secuencial=secuencial.secuencial+1
                        secuencial.created_by = request.user.get_full_name()
                        secuencial.updated_by = request.user.get_full_name()

                        secuencial.save()
                    except Secuenciales.DoesNotExist:
                        secuencial = None

                    contador=request.POST["columnas_receta"]
                    print contador
                    i=0

                    # while int(i)<=int(contador):
                    #     i+= 1
                    #     print('entro comoqw'+str(i))
                    #     if int(i)> int(contador):
                    #         print('entrosd')
                    #         break
                    #     else:
                    #         if 'id_kits'+str(i) in request.POST:
                    #             # product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                    #             # comprasdetalle=ComprasDetalle()
                    #             # comprasdetalle.compra_id = new_orden.compra_id
                    #             # comprasdetalle.producto_id=request.POST["id_kits"+str(i)]
                    #             # comprasdetalle.proveedor_id=request.POST["proveedor"]
                    #             # comprasdetalle.bodega_id=request.POST["bodega"]
                    #             # comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                    #             # #kits.costo=float(request.POST["costo_kits1"])
                    #             # comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                    #             # comprasdetalle.total=request.POST["total_kits"+str(i)]
                    #             # comprasdetalle.save()
                    #
                    #     print(i)
                    #     print('contadorsd prueba'+str(contador))

                    context = {
                   'section_title':'Actualizar Orden Produccion',
                    'button_text':'Actualizar',
                    'ordenproduccion_form':ordenproduccion_form,
                    'row':row,
                     }


                    # return render_to_response(
                    #     'ordenproduccion/actualizar.html',
                    #     context,
                    #     context_instance=RequestContext(request))

                    return HttpResponseRedirect('/ordenproduccion/ordenproduccion')
            except IntegrityError:
                print 'error'
                print ordenproduccion_form.errors, len(ordenproduccion_form.errors)
                return HttpResponseRedirect('/ordenproduccion/ordenproduccion')
        else:
        	print 'error'
    		print ordenproduccion_form.errors, len(ordenproduccion_form.errors)
      else:
        ordenproduccion_form=OrdenProduccionForm
        productos = Producto.objects.all()
        ambientes = Ambiente.objects.all()

        cursor = connection.cursor();
        cursor.execute("SELECT pd.id,p.codigo,p.fecha,p.cliente_id,p.vendedor_id,p.fechaentrega,pd.pedido_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.imagen,c.nombre_cliente,pd.producto_id,pd.detalle,pd.medida,pd.reparacion,pd.codigo_produccion from pedido p,pedido_detalle pd,cliente c where pd.pedido_id=p.id and c.id_cliente=p.cliente_id and p.aprobada=true and pd.no_producir!=True and NOT EXISTS (select * from orden_produccion op  where op.pedido_detalle_id=pd.id)");
        row = cursor.fetchall();



      return render_to_response('ordenproduccion/create.html', { 'ordenproduccion_form': ordenproduccion_form,'productos':productos,'ambientes':ambientes,'row':row},  RequestContext(request))

#=====================================================#
@transaction.atomic
def OrdenProduccionUpdateView(request,pk):
    if request.method == 'POST':
        orden = OrdenProduccion.objects.get(id=pk)
        ordenproduccion_form = OrdenProduccionForm(request.POST,request.FILES,instance=orden)

        productos = Producto.objects.all()
        cursor = connection.cursor();

        cursor.execute("SELECT pd.id,p.codigo,p.fecha,p.cliente_id,p.vendedor_id,p.fechaentrega,pd.pedido_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.imagen,c.nombre_cliente,pd.producto_id,pd.reparacion,pd.codigo_produccion from pedido p,pedido_detalle pd,cliente c where pd.pedido_id=p.id and pd.no_producir!=True and c.id_cliente=p.cliente_id and NOT EXISTS (select * from orden_produccion op  where op.pedido_detalle_id=pd.id)");
        row = cursor.fetchall();

        if ordenproduccion_form.is_valid():
            with transaction.atomic():
                new_orden=ordenproduccion_form.save()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.updated_at = datetime.now()
                if 'imagen' in request.FILES:
                    new_orden.imagen=request.FILES["imagen"]
                if 'imagen_global' in request.FILES:
                    new_orden.imagen_global=request.FILES["imagen_global"]
                new_orden.save()

                context = {
               'section_title':'Actualizar Orden Produccion',
                'button_text':'Actualizar',
                'ordenproduccion_form':ordenproduccion_form,
                'mensaje': 'Actualizado con exito',
                'op':orden,
                'row':row,
                 }


                return render_to_response(
                    'ordenproduccion/actualizar.html',
                    context,
                    context_instance=RequestContext(request))
        else:
            orden = OrdenProduccion.objects.get(id=pk)
            ordenproduccion_form=OrdenProduccionForm(request.POST,request.FILES,instance=orden)
            #detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)
            cursor = connection.cursor();
            cursor.execute("SELECT pd.id,p.codigo,p.fecha,p.cliente_id,p.vendedor_id,p.fechaentrega,pd.pedido_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.imagen,c.nombre_cliente,pd.producto_id,pd.reparacion,pd.codigo_produccion from pedido p,pedido_detalle pd,cliente c where pd.pedido_id=p.id and c.id_cliente=p.cliente_id and pd.no_producir!=True and NOT EXISTS (select * from orden_produccion op  where op.pedido_detalle_id=pd.id)");
            row = cursor.fetchall();


            context = {
            'section_title':'Actualizar Orden Produccion',
            'button_text':'Actualizar',
            'ordenproduccion_form':ordenproduccion_form,
            'op':orden,
            'mensaje': 'Actualizado con exito',
            'row':row,
           	}

        return render_to_response(
            'ordenproduccion/actualizar.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordenproduccion=OrdenProduccion.objects.get(id=pk)
        ordenproduccion_form=OrdenProduccionForm(instance=ordenproduccion)
        cursor = connection.cursor();
        cursor.execute("SELECT pd.id,p.codigo,p.fecha,p.cliente_id,p.vendedor_id,p.fechaentrega,pd.pedido_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.imagen,c.nombre_cliente,pd.producto_id,pd.reparacion,pd.codigo_produccion from pedido p,pedido_detalle pd,cliente c where pd.pedido_id=p.id and c.id_cliente=p.cliente_id and NOT EXISTS (select * from orden_produccion op  where op.pedido_detalle_id=pd.id)");
        row = cursor.fetchall();
        #detalle = ComprasDetalle.objects.filter(compra_id=ordenproduccion.id)

        context = {
            'section_title':'Actualizar Orden Produccion',
            'button_text':'Actualizar',
            'ordenproduccion_form':ordenproduccion_form,
            'op':ordenproduccion,
            'row':row,
            }

        return render_to_response(
            'ordenproduccion/actualizar.html',
            context,
            context_instance=RequestContext(request))
@login_required()
def OrdenProduccionEliminarView(request):
    return eliminarView(request, OrdenProduccion, 'ordenproduccion-list')

#=====================================================#
@login_required()
def OrdenProduccionEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, OrdenProduccion)


def OrdenProduccionListAprobarView(request):
    ordenes = OrdenProduccion.objects.all().order_by('id')


    return render_to_response('ordenproduccion/aprobada.html', {'ordenes': ordenes}, RequestContext(request))


@login_required()
@transaction.atomic
def OrdenProduccionAprobarByPkView(request, pk):
    with transaction.atomic():

        objetos = OrdenProduccion.objects.get(id= pk)
        objetos.aprobada = True
        objetos.fecha_aprobacion = datetime.now()
        objetos.save()
        try:
            pedidoDetalle = PedidoDetalle.objects.get(id=objetos.pedido_detalle_id)
        except PedidoDetalle.DoesNotExist:
            pedidoDetalle = None

        if pedidoDetalle:
            productosAreas=ProductoAreas.objects.filter(producto_id=pedidoDetalle.producto_id)
            if productosAreas:
                for pa in productosAreas:
                    re=SubordenProduccion()
                    re.orden_produccion_id=objetos.id
                    re.areas_id=pa.areas_id
                    re.costo_horas=float(pa.costo_horas*pedidoDetalle.cantidad)
                    re.costo_materiales = float(pa.costo_materiales * pedidoDetalle.cantidad)
                    re.horas=float(pa.horas * pedidoDetalle.cantidad)
                    #re.total=float(pa.total*pedidoDetalle.cantidad)
                    re.secuencia=pa.secuencia
                    subore=re.save()
                    print ('ID de la SubOreden'+str(re.id))
                    print ('ID de la Areas'+str(pa.areas_id))
                    kit=Kits.objects.filter(padre_id=pedidoDetalle.producto_id).filter(areas_id=pa.areas_id)
                    if kit:
                        for k in kit:
                            print ('Entro en la receta'+str(k.hijo_id))
                            receta=OrdenProduccionReceta()
                            receta.producto_id=k.hijo_id
                            receta.cantidad=float(k.cantidad*pedidoDetalle.cantidad)
                            receta.costo=k.costo
                            receta.total=float(k.total*pedidoDetalle.cantidad)
                            receta.medida=k.medida
                            receta.areas_id=k.areas_id
                            receta.suborden_produccion_id=re.id
                            receta.nombre = k.nombre
                            receta.otros_costos = k.otros_costos
                            receta.save()
                    manoobra=ProductoManoObra.objects.filter(producto_areas_id=pa.id)
                    if manoobra:
                        for m in manoobra:
                            mano=SubordenProduccionDetalle()
                            mano.suborden_produccion_id=re.id
                            mano.operacion_unitaria=m.operacion_unitaria
                            mano.total=float(m.total*pedidoDetalle.cantidad)
                            mano.costo_hora=m.costo_hora
                            mano.hora_total=float(m.hora_total*pedidoDetalle.cantidad)
                            mano.save()

    return HttpResponseRedirect('/ordenproduccion/ordenproduccionAprobar')

def index(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    ordenproduccion=OrdenProduccion.objects.get(id=pk)
    try:
        pedido = PedidoDetalle.objects.get(id=ordenproduccion.pedido_detalle_id)
        p = Pedido.objects.get(id=pedido.pedido_id)

    except PedidoDetalle.DoesNotExist:
        pedido = None
        p=None



    html = render_to_string('ordenproduccion/imprimir.html', {'pagesize':'A4','ordenproduccion':ordenproduccion,'pedido':p,'media_root':settings.MEDIA_ROOT}, context_instance=RequestContext(request))
    return generar_pdf(html)
    # context = {
    #         'ordenproduccion':ordenproduccion,
    #         }

    # return render_to_response(
    #         'ordenproduccion/imprimir.html',
    #         context,
    #         context_instance=RequestContext(request))




def generar_pdf(html):
    # Funci?n para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

class RopListView(ObjectListView):
    model = Rop
    paginate_by = 100
    template_name = 'rop/list.html'
    table_class = RopTable
    filter_class = RopFilter
    context_object_name = 'ordenes'

    def get_context_data(self, **kwargs):
        context = super(RopListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('rop-delete')
        return context

@transaction.atomic
def RopCreateView(request):
      if request.method == 'POST':
        rop_form=RopForm(request.POST)
        productos = Producto.objects.all()
        ambientes = Ambiente.objects.all()

        cursor = connection.cursor();
        cursor.execute("SELECT op.id,op.codigo as codigo_op, op.fecha, op.cliente_id,op.descripcion,op.detalle,op.cantidad,op.largo,op.fondo,op.madera,op.vidrio,op.hierro,op.marmol,op.enchape,op.enchape_detalle,op.tallado,op.tallado_detalle,op.tono,op.retractil,op.panorama,op.corredizo,op.oleo,op.conchaperla,op.tela_almacen,op.tela_cliente,op.agarraderas,op.imagen,op.adicional,op.fechapedido,op.tipo,op.tipo_mueb_id,op.mate,op.semimate,op.brillante,op.pulido,op.aluminio,op.acero,op.abrillantado,op.pintado,op.satinado,op.fechacotizacion,op.engrampe,op.impulso,op.poroabierto,op.vendedor_id,op.tiempo_respuesta,op.fuera_ciudad,op.observacion,op.codigo_item,op.profundidad,op.ancho,op.patina_color,op.pintado_mano,op.cuero_cliente,op.cuero_almacen,op.fechainicio,op.fechaentrega,op.metal_hierro,c.nombre_cliente,op.alto from cliente c, orden_produccion op where  c.id_cliente=op.cliente_id  and op.bodega_productos_blanco=true");
        row = cursor.fetchall();
        if rop_form.is_valid():
            with transaction.atomic():
                new_orden=rop_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.orden_produccion_id=request.POST["deta"]
                if 'imagen' in request.FILES:
                    new_orden.imagen=request.FILES["imagen"]
                if 'imagen_global' in request.FILES:
                    new_orden.imagen_global=request.FILES["imagen_global"]
                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='rop')
                    secuencial.secuencial=secuencial.secuencial+1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = datetime.now()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None

                contador=request.POST["columnas_receta"]
                print contador
                i=0
                # pedidoDetalle=PedidoDetalle.objects.get(id=request.POST["deta"])

                # if pedidoDetalle:


                #     productosAreas=ProductoAreas.objects.filter(producto_id=pedidoDetalle.producto_id)
                #     print new_orden.id
                #     if productosAreas:
                #         for pa in productosAreas:
                #             re=SubordenProduccion()
                #             re.orden_produccion_id=new_orden.id
                #             re.areas_id=pa.areas_id
                #             re.costo=pa.costo_horas
                #             re.total=pa.total
                #             re.secuencia=pa.secuencia
                #             subore=re.save()
                #             print ('ID de la SubOreden'+str(re.id))
                #             print ('ID de la Areas'+str(pa.areas_id))
                #             kit=Kits.objects.filter(padre_id=pedidoDetalle.producto_id).filter(areas_id=pa.areas_id)
                #             if kit:
                #                 for k in kit:
                #                     print ('Entro en la receta'+str(k.hijo_id))
                #                     receta=OrdenProduccionReceta()
                #                     receta.producto_id=k.hijo_id
                #                     receta.cantidad=k.cantidad
                #                     receta.costo=k.costo
                #                     receta.total=k.total
                #                     receta.medida=k.medida
                #                     receta.areas_id=k.areas_id
                #                     receta.suborden_produccion_id=re.id

                #                     receta.save()


                return HttpResponseRedirect('/ordenproduccion/rop')
        else:
            print 'error'
            print rop_form.errors, len(rop_form.errors)
      else:
        rop_form=RopForm
        productos = Producto.objects.all()
        ambientes = Ambiente.objects.all()

        cursor = connection.cursor();
        cursor.execute("SELECT op.id,op.codigo as codigo_op, op.fecha, op.cliente_id,op.descripcion,op.detalle,op.cantidad,op.largo,op.fondo,op.madera,op.vidrio,op.hierro,op.marmol,op.enchape,op.enchape_detalle,op.tallado,op.tallado_detalle,op.tono,op.retractil,op.panorama,op.corredizo,op.oleo,op.conchaperla,op.tela_almacen,op.tela_cliente,op.agarraderas,op.imagen,op.adicional,op.fechapedido,op.tipo,op.tipo_mueb_id,op.mate,op.semimate,op.brillante,op.pulido,op.aluminio,op.acero,op.abrillantado,op.pintado,op.satinado,op.fechacotizacion,op.engrampe,op.impulso,op.poroabierto,op.vendedor_id,op.tiempo_respuesta,op.fuera_ciudad,op.observacion,op.codigo_item,op.profundidad,op.ancho,op.patina_color,op.pintado_mano,op.cuero_cliente,op.cuero_almacen,op.fechainicio,op.fechaentrega,op.metal_hierro,c.nombre_cliente,op.alto from cliente c, orden_produccion op where  c.id_cliente=op.cliente_id  and op.bodega_productos_blanco=true");
        row = cursor.fetchall();



      return render_to_response('rop/create.html', { 'ordenproduccion_form': rop_form,'productos':productos,'ambientes':ambientes,'row':row},  RequestContext(request))

@transaction.atomic
def RopUpdateView(request,pk):
    if request.method == 'POST':
        orden = Rop.objects.get(id=pk)
        ordenproduccion_form = RopForm(request.POST,request.FILES,instance=orden)

        productos = Producto.objects.all()
        cursor = connection.cursor();
        cursor.execute("SELECT op.id,op.codigo as codigo_op, op.fecha, op.cliente_id,op.descripcion,op.detalle,op.cantidad,op.largo,op.fondo,op.madera,op.vidrio,op.hierro,op.marmol,op.enchape,op.enchape_detalle,op.tallado,op.tallado_detalle,op.tono,op.retractil,op.panorama,op.corredizo,op.oleo,op.conchaperla,op.tela_almacen,op.tela_cliente,op.agarraderas,op.imagen,op.adicional,op.fechapedido,op.tipo,op.tipo_mueb_id,op.mate,op.semimate,op.brillante,op.pulido,op.aluminio,op.acero,op.abrillantado,op.pintado,op.satinado,op.fechacotizacion,op.engrampe,op.impulso,op.poroabierto,op.vendedor_id,op.tiempo_respuesta,op.fuera_ciudad,op.observacion,op.codigo_item,op.profundidad,op.ancho,op.patina_color,op.pintado_mano,op.cuero_cliente,op.cuero_almacen,op.fechainicio,op.fechaentrega,op.metal_hierro,c.nombre_cliente,op.alto from cliente c, orden_produccion op where  c.id_cliente=op.cliente_id  and op.bodega_productos_blanco=true");
        row = cursor.fetchall();

        if ordenproduccion_form.is_valid():
            with transaction.atomic():
                new_orden=ordenproduccion_form.save()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.updated_at = datetime.now()
                if 'imagen' in request.FILES:
                    new_orden.imagen=request.FILES["imagen"]
                if 'imagen_global' in request.FILES:
                    new_orden.imagen_global=request.FILES["imagen_global"]
                new_orden.save()

                context = {
               'section_title':'Actualizar ROP',
                'button_text':'Actualizar',
                'ordenproduccion_form':ordenproduccion_form,
                'op':orden,
                'row':row,
                 }


                return render_to_response(
                    'rop/actualizar.html',
                    context,
                    context_instance=RequestContext(request))
        else:

            orden = Rop.objects.get(id=pk)
            ordenproduccion_form = RopForm(request.POST,request.FILES,instance=orden)

            #detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)
            cursor = connection.cursor();
            cursor.execute("SELECT op.id,op.codigo as codigo_op, op.fecha, op.cliente_id,op.descripcion,op.detalle,op.cantidad,op.largo,op.fondo,op.madera,op.vidrio,op.hierro,op.marmol,op.enchape,op.enchape_detalle,op.tallado,op.tallado_detalle,op.tono,op.retractil,op.panorama,op.corredizo,op.oleo,op.conchaperla,op.tela_almacen,op.tela_cliente,op.agarraderas,op.imagen,op.adicional,op.fechapedido,op.tipo,op.tipo_mueb_id,op.mate,op.semimate,op.brillante,op.pulido,op.aluminio,op.acero,op.abrillantado,op.pintado,op.satinado,op.fechacotizacion,op.engrampe,op.impulso,op.poroabierto,op.vendedor_id,op.tiempo_respuesta,op.fuera_ciudad,op.observacion,op.codigo_item,op.profundidad,op.ancho,op.patina_color,op.pintado_mano,op.cuero_cliente,op.cuero_almacen,op.fechainicio,op.fechaentrega,op.metal_hierro,c.nombre_cliente,op.alto from cliente c, orden_produccion op where  c.id_cliente=op.cliente_id  and op.bodega_productos_blanco=true");
            row = cursor.fetchall();


            context = {
            'section_title':'Actualizar Orden Produccion',
            'button_text':'Actualizar',
            'ordenproduccion_form':ordenproduccion_form,
            'op':orden,
            'row':row,
            }

        return render_to_response(
            'rop/actualizar.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordenproduccion=Rop.objects.get(id=pk)
        ordenproduccion_form=RopForm(instance=ordenproduccion)
        cursor = connection.cursor();
        cursor.execute("SELECT op.id,op.codigo as codigo_op, op.fecha, op.cliente_id,op.descripcion,op.detalle,op.cantidad,op.largo,op.fondo,op.madera,op.vidrio,op.hierro,op.marmol,op.enchape,op.enchape_detalle,op.tallado,op.tallado_detalle,op.tono,op.retractil,op.panorama,op.corredizo,op.oleo,op.conchaperla,op.tela_almacen,op.tela_cliente,op.agarraderas,op.imagen,op.adicional,op.fechapedido,op.tipo,op.tipo_mueb_id,op.mate,op.semimate,op.brillante,op.pulido,op.aluminio,op.acero,op.abrillantado,op.pintado,op.satinado,op.fechacotizacion,op.engrampe,op.impulso,op.poroabierto,op.vendedor_id,op.tiempo_respuesta,op.fuera_ciudad,op.observacion,op.codigo_item,op.profundidad,op.ancho,op.patina_color,op.pintado_mano,op.cuero_cliente,op.cuero_almacen,op.fechainicio,op.fechaentrega,op.metal_hierro,c.nombre_cliente,op.alto from cliente c, orden_produccion op where  c.id_cliente=op.cliente_id  and op.bodega_productos_blanco=true");
        row = cursor.fetchall();
        #detalle = ComprasDetalle.objects.filter(compra_id=ordenproduccion.id)

        context = {
            'section_title':'Actualizar ROP',
            'button_text':'Actualizar',
            'ordenproduccion_form':ordenproduccion_form,
            'op':ordenproduccion,
            'row':row,
            }

        return render_to_response(
            'rop/actualizar.html',
            context,
            context_instance=RequestContext(request))


class RopListAprobarView(ObjectListView):
    model = Rop
    paginate_by = 100
    template_name = 'rop/aprobada.html'
    table_class = RopTable
    filter_class = RopFilter
    context_object_name = 'ordenes'


    def get_context_data(self, **kwargs):
        context = super(RopListAprobarView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('rop-delete')
        return context
@login_required()
def RopAprobarByPkView(request, pk):

    objetos = Rop.objects.get(id= pk)
    ordenproduccion=OrdenProduccion.objects.get(id=objetos.orden_produccion_id)
    pedidoDetalle=PedidoDetalle.objects.get(id=ordenproduccion.pedido_detalle_id)
    ob=Producto.objects.get(producto_id=pedidoDetalle.producto_id)

    objetos.aprobada = True
    objetos.save()

    k=Kardex()
    k.nro_documento =objetos.codigo
    k.producto_id=ob.producto_id
    k.cantidad=ordenproduccion.cantidad
    k.descripcion='Orden de Egreso por ROP'
    k.costo=pedidoDetalle.total
    k.bodega_id=4
    k.modulo=objetos.id
    k.fecha_egreso=datetime.now()
    k.cliente_id=ordenproduccion.cliente_id
    k.save()
    try:
        objetose = ProductoEnBodega.objects.get(producto_id= ob.producto_id,bodega_id=4)
    except ProductoEnBodega.DoesNotExist:
        objetose = None

    if objetose:
        cant=objetose.cantidad
        objetose.cantidad=cant-float(objetos.cantidad)
        objetose.updated_at = datetime.now()
        objetose.updated_by = request.user.get_full_name()
        objetose.save()


    return HttpResponseRedirect('/ordenproduccion/ropAprobar')

@login_required()
def OrdenProduccionListSubordenesView(request):
    #ordenes = OrdenProduccion.objects.all().order_by('id')
    ordenes=''

    return render_to_response('ordenproduccion/list_subordenesproducccion.html', {'ordenes': ordenes}, RequestContext(request))

class OrdenProduccionHistoricoListView(ObjectListView):
    model = OrdenProduccion
    paginate_by = 100
    template_name = 'ordenproduccion/historico.html'
    table_class = OrdenProduccionTable
    filter_class = OrdenProduccionFilter
    context_object_name = 'ordenes'

    def get_context_data(self, **kwargs):
        context = super(OrdenProduccionHistoricoListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('ordenproduccion-delete')
        return context
def OrdenProduccionHistoricoUpdateView(request,pk):
    if request.method == 'POST':
        orden = OrdenProduccion.objects.get(id=pk)
        ordenproduccion_form = OrdenProduccionForm(request.POST,request.FILES,instance=orden)

        productos = Producto.objects.all()
        cursor = connection.cursor();
        cursor.execute("SELECT pd.id,p.codigo,p.fecha,p.cliente_id,p.vendedor_id,p.fechaentrega,pd.pedido_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.imagen,c.nombre_cliente,pd.producto_id,pd.reparacion,pd.codigo_produccion from pedido p,pedido_detalle pd,cliente c where pd.pedido_id=p.id and c.id_cliente=p.cliente_id and NOT EXISTS (select * from orden_produccion op  where op.pedido_detalle_id=pd.id)");
        row = cursor.fetchall();

        if ordenproduccion_form.is_valid():

            new_orden=ordenproduccion_form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            new_orden.save()

            context = {
           'section_title':'Actualizar Orden Produccion',
            'button_text':'Actualizar',
            'ordenproduccion_form':ordenproduccion_form,
            'op':orden,
            'row':row,
             }


            return render_to_response(
                'ordenproduccion/actualizar_historico.html',
                context,
                context_instance=RequestContext(request))
        else:

            ordenproduccion=OrdenProduccion.objects.get(id=pk)
            ordenproduccion_form=OrdenProduccionForm(instance=ordenproduccion)
            #detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)
            cursor = connection.cursor();
            cursor.execute("SELECT pd.id,p.codigo,p.fecha,p.cliente_id,p.vendedor_id,p.fechaentrega,pd.pedido_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.imagen,c.nombre_cliente,pd.producto_id,pd.reparacion,pd.codigo_produccion from pedido p,pedido_detalle pd,cliente c where pd.pedido_id=p.id and c.id_cliente=p.cliente_id and NOT EXISTS (select * from orden_produccion op  where op.pedido_detalle_id=pd.id)");
            row = cursor.fetchall();


            context = {
            'section_title':'Actualizar Orden Produccion',
            'button_text':'Actualizar',
            'ordenproduccion_form':ordenproduccion_form,
            'op':ordenproduccion,
            'row':row,
            }

        return render_to_response(
            'ordenproduccion/actualizar_historico.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordenproduccion=OrdenProduccion.objects.get(id=pk)
        ordenproduccion_form=OrdenProduccionForm(instance=ordenproduccion)
        cursor = connection.cursor();
        cursor.execute("SELECT pd.id,p.codigo,p.fecha,p.cliente_id,p.vendedor_id,p.fechaentrega,pd.pedido_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.imagen,c.nombre_cliente,pd.producto_id,pd.reparacion,pd.codigo_produccion from pedido p,pedido_detalle pd,cliente c where pd.pedido_id=p.id and c.id_cliente=p.cliente_id and NOT EXISTS (select * from orden_produccion op  where op.pedido_detalle_id=pd.id)");
        row = cursor.fetchall();
        #detalle = ComprasDetalle.objects.filter(compra_id=ordenproduccion.id)

        context = {
            'section_title':'Actualizar Orden Compra',
            'button_text':'Actualizar',
            'ordenproduccion_form':ordenproduccion_form,
            'op':ordenproduccion,
            'row':row,
            }

        return render_to_response(
            'ordenproduccion/actualizar_historico.html',
            context,
            context_instance=RequestContext(request))

@login_required()
@csrf_exempt
def orden_produccion_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order=request.GET['order[0][column]']
        _order_dir=request.GET['order[0][dir]']
        cursor = connection.cursor()
        #sql="  select m.id,t.descripcion,m.fecha_emision,m.numero_comprobante,m.paguese_a,p.ruc,td.descripcion,m.numero_cheque,b.nombre,m.monto_cheque,m.monto,m.descripcion,m.activo,m.conciliacion_id from movimiento m left join proveedor p on p.proveedor_id=m.proveedor_id left join tipo_documento td on td.id=m.tipo_documento_id and td.id=1 left join tipo_anticipo t on t.id=m.tipo_anticipo_id and t.id=1 left join banco b on b.id=m.banco_id where m.tipo_anticipo_id=1 and m.tipo_documento_id=1 "
        sql="select p.id,p.tipo,p.codigo,p.fecha,p.descripcion,c.nombre_cliente,p.detalle,p.cantidad,p.aprobada,p.finalizada from orden_produccion p left join cliente c on c.id_cliente=p.cliente_id where 1=1 "
        if _search_value:
            sql+=" and ( UPPER(p.codigo) like '%"+_search_value+"%' or UPPER(p.tipo) like '%"+_search_value.upper()+"%' or UPPER(p.descripcion) like '%"+_search_value.upper()+"%' or UPPER(c.nombre_cliente) like '%"+_search_value.upper()+"%'  or UPPER(p.detalle) like '%"+_search_value.upper()+"%' or CAST(p.cantidad as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(p.fecha as VARCHAR)  like '%"+_search_value+"%'"
        
        if _search_value.upper()  in 'APROBADA':
            sql+=" or p.aprobada is True"
        
        if _search_value.upper()  in 'ESPERANDO APROBACION':
            sql+=" or p.aprobada is not True"
        if _search_value.upper()  in 'FINALIZADA':
            sql+=" or p.finalizada is  True"
        
        
        if _search_value:
             sql+=" ) "
            
           
    
        #sql +=" order by fecha"
        print _order
        if _order == '0':
            sql +=" order by p.tipo "+_order_dir
        if _order == '1':
            sql +=" order by CAST(p.codigo AS Numeric(10,0)) "+_order_dir
        if _order == '2':
            sql +=" order by p.fecha "+_order_dir
        
        if _order == '3':
            sql +=" order by p.descripcion "+_order_dir
        
        if _order == '4':
            sql +=" order by c.nombre_cliente "+_order_dir
        if _order == '5':
            sql +=" order by p.detalle "+_order_dir
        if _order == '6':
            
            sql +=" order by p.cantidad "+_order_dir
        
        
        
        print sql
        cursor.execute(sql)
        compras = cursor.fetchall()
            
        compras_filtered = compras[_start:_start + _end]

        compras_list = []
        for o in compras_filtered:
            compras_obj = []
            
            compras_obj.append(o[1])
            compras_obj.append(o[2])
            compras_obj.append(o[3].strftime('%Y-%m-%d'))
            
            compras_obj.append(o[4])
            compras_obj.append(o[5])
            compras_obj.append(o[6])
            compras_obj.append(o[7])
            
            html=''

            if o[8]:
                compras_obj.append("Aprobada")
                html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/subordenproduccion/subordenproduccion/'+str(o[0])+'/list/" style=""><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> SubOrdenes de Produccion</button></a>'        
            else:
                
                if o[9]:
                    compras_obj.append("Finalizada")
                else:
                    
                        compras_obj.append("Esperando Aprobacion")
                        html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/ordenproduccion/ordenproduccion/'+str(o[0])+'/editar" ><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Editar</button></a>'
            
            html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/ordenproduccion/imprimir/'+str(o[0])+'/" style=""><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Imprimir</button></a>'        
            
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
@csrf_exempt
def orden_produccion_suborden_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order=request.GET['order[0][column]']
        _order_dir=request.GET['order[0][dir]']
        cursor = connection.cursor()
        #sql="  select m.id,t.descripcion,m.fecha_emision,m.numero_comprobante,m.paguese_a,p.ruc,td.descripcion,m.numero_cheque,b.nombre,m.monto_cheque,m.monto,m.descripcion,m.activo,m.conciliacion_id from movimiento m left join proveedor p on p.proveedor_id=m.proveedor_id left join tipo_documento td on td.id=m.tipo_documento_id and td.id=1 left join tipo_anticipo t on t.id=m.tipo_anticipo_id and t.id=1 left join banco b on b.id=m.banco_id where m.tipo_anticipo_id=1 and m.tipo_documento_id=1 "
        sql="select p.id,p.tipo,p.codigo,p.fecha,p.descripcion,c.nombre_cliente,p.detalle,p.cantidad,p.aprobada,p.finalizada from orden_produccion p left join cliente c on c.id_cliente=p.cliente_id where 1=1 "
        if _search_value:
            sql+=" and ( UPPER(p.codigo) like '%"+_search_value+"%' or UPPER(p.tipo) like '%"+_search_value.upper()+"%' or UPPER(p.descripcion) like '%"+_search_value.upper()+"%' or UPPER(c.nombre_cliente) like '%"+_search_value.upper()+"%'  or UPPER(p.detalle) like '%"+_search_value.upper()+"%' or CAST(p.cantidad as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(p.fecha as VARCHAR)  like '%"+_search_value+"%'"
        
        if _search_value.upper()  in 'APROBADA':
            sql+=" or p.aprobada is True"
        
        if _search_value.upper()  in 'ESPERANDO APROBACION':
            sql+=" or p.aprobada is not True"
        if _search_value.upper()  in 'FINALIZADA':
            sql+=" or p.finalizada is  True"
        
        
        if _search_value:
             sql+=" ) "
            
           
    
        #sql +=" order by fecha"
        print _order
        if _order == '0':
            sql +=" order by p.tipo "+_order_dir
        if _order == '1':
            sql +=" order by CAST(p.codigo AS Numeric(10,0)) "+_order_dir
        if _order == '2':
            sql +=" order by p.fecha "+_order_dir
        
        if _order == '3':
            sql +=" order by p.descripcion "+_order_dir
        
        if _order == '4':
            sql +=" order by c.nombre_cliente "+_order_dir
        if _order == '5':
            sql +=" order by p.detalle "+_order_dir
        if _order == '6':
            
            sql +=" order by p.cantidad "+_order_dir
        
        
        
        print sql
        cursor.execute(sql)
        compras = cursor.fetchall()
            
        compras_filtered = compras[_start:_start + _end]

        compras_list = []
        for o in compras_filtered:
            compras_obj = []
            
            compras_obj.append(o[1])
            compras_obj.append(o[2])
            compras_obj.append(o[3].strftime('%Y-%m-%d'))
            
            compras_obj.append(o[4])
            compras_obj.append(o[5])
            compras_obj.append(o[6])
            compras_obj.append(o[7])
            
            html=''

            if o[8]:
                compras_obj.append("Aprobada")
                html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/subordenproduccion/subordenproduccion/'+str(o[0])+'/listdetalle/" style=""><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> SubOrdenes de Produccion</button></a>'        
            else:
                
                if o[9]:
                    compras_obj.append("Finalizada")
                else:
                    
                        compras_obj.append("Esperando Aprobacion")
                        #html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/ordenproduccion/ordenproduccion/'+str(o[0])+'/editar" ><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Editar</button></a>'
            
            html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/ordenproduccion/imprimir/'+str(o[0])+'/" style=""><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Imprimir</button></a>'        
            
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
