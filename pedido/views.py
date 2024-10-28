from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, eliminarByPkView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.contrib import messages
from django.db import connection, transaction
import simplejson as json
import datetime
from .models import *
from clientes.models import *
from .forms import *
from .tables import *
from .filters import *
from django.views.decorators.csrf import csrf_exempt
from proforma.models import *
from config.models import *
from django.db.models import Q
from django.views.generic import TemplateView

from django.forms.extras.widgets import *
from django.contrib.auth import authenticate,login
#from login.lib.tools import Tools

import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
#from config.models import Mensajes
from django.db import IntegrityError, transaction


from login.lib.tools import Tools
from django.contrib import auth
from django.conf import settings

#======================PEDIDO=============================#

@login_required()
def PedidoListView(request):
    #pedido = Pedido.objects.all().order_by('id')
    pedido=''


    return render_to_response('pedido/index.html', {'pedidos': pedido}, RequestContext(request))


#=====================================================#
class PedidoDetailView(ObjectDetailView):
    model = Pedido
    template_name = 'pedido/detail.html'

#=====================================================#
@transaction.atomic
def PedidoCreateView(request):
      if request.method == 'POST':
        pedido_form=PedidoForm(request.POST)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        proformas = Proforma.objects.filter(aprobada=True)
        ambientes = Ambiente.objects.all().order_by('descripcion')

        if pedido_form.is_valid():
            with transaction.atomic():
                new_orden=pedido_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.total=request.POST["total"]
                new_orden.subtotal=request.POST["subtotal"]
                new_orden.descuento=request.POST["descuento"]
                new_orden.porcentaje_descuento=request.POST["porcentaje_descuento"]
                new_orden.iva=request.POST["iva"]
                new_orden.porcentaje_iva=request.POST["porcentaje_iva"]
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='pedido')
                    if secuencial.secuencial != new_orden.codigo:
                        new_orden.codigo = secuencial.secuencial
                        new_orden.save()
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
                while int(i)<=int(contador):
                    i+= 1
                    print('entro cw'+str(i))
                    if int(i)> int(contador):
                        print('entrosd')
                        break
                    else:
                        print('entroAguardar')
                        if 'id_kits'+str(i) in request.POST:
                            product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                            pedidodetalle=PedidoDetalle()
                            pedidodetalle.pedido_id = new_orden.id
                            pedidodetalle.producto_id=request.POST["id_kits"+str(i)]
                            pedidodetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            pedidodetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            pedidodetalle.nombre=request.POST["nombre_kits"+str(i)]
                            pedidodetalle.medida=request.POST["medida_kits"+str(i)]
                            if 'imagen_kits'+str(i) in request.POST:
                                pedidodetalle.imagen=request.FILES["imagen_kits"+str(i)]

                            pedidodetalle.observaciones=request.POST["observacion_kits"+str(i)]
                            pedidodetalle.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                            #kits.costo=float(request.POST["costo_kits1"])
                            pedidodetalle.detalle=request.POST["detalle_kits"+str(i)]
                            pedidodetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            pedidodetalle.total=request.POST["total_kits"+str(i)]
                            pedidodetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                            pedidodetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            pedidodetalle.no_producir= request.POST.get('no_producir_kits' + str(i), False)
                            pedidodetalle.save()
                            print('se guardo'+str(contador))


                    print(i)
                    print('contadorsd prueba'+str(contador))

                return HttpResponseRedirect('/pedido/pedido')
        else:
            print 'error'
            print pedido_form.errors, len(pedido_form.errors)
      else:
        pedido_form=PedidoForm
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        proformas = Proforma.objects.filter(aprobada=True)
        cursor = connection.cursor();
        cursor.execute(
            "SELECT p.id,p.codigo,p.fecha,p.cliente_id,p.vendedor_id,p.fecha,c.nombre_cliente,p.abreviatura_codigo,v.nombre from proforma p,cliente c,vendedor v where v.id=p.vendedor_id and c.id_cliente=p.cliente_id and p.aprobada=true  and NOT EXISTS (select * from pedido op  where  op.abreviatura_codigo=p.abreviatura_codigo and op.proforma_codigo=p.codigo or op.proforma_id=p.id)");
        row = cursor.fetchall();
        ambientes = Ambiente.objects.all().order_by('descripcion')
        iva = Parametros.objects.get(clave='iva')

      return render_to_response('pedido/create.html', { 'form': pedido_form,'productos':productos,'proformas':proformas,'ambientes':ambientes,'iva':iva,'row':row},  RequestContext(request))

#=====================================================#
class PedidoUpdateView(ObjectUpdateView):


    def get(self, request, *args, **kwargs):

        pedido = Pedido.objects.get(id=kwargs['pk'])
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')

        pedido_form=PedidoForm(instance=pedido)
        detalle = PedidoDetalle.objects.filter(pedido_id=pedido.id).filter(Q(no_producir=False) | Q(no_producir__isnull=True)).order_by('id')

        context = {
        'section_title':'Actualizar Pedido',
        'button_text':'Actualizar',
        'form':pedido_form,
        'productos':productos,
        'ambientes':ambientes,
        'detalle':detalle,
        'pedido':pedido
        }

        return render_to_response(
            'pedido/actualizar.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        pedido = Pedido.objects.get(id=kwargs['pk'])
        pedido_form = PedidoForm(request.POST,request.FILES,instance=pedido)
        p_id=kwargs['pk']
        print(p_id)
        print pedido_form.is_valid(), pedido_form.errors, type(pedido_form.errors)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

        if pedido_form.is_valid() :

            new_orden=pedido_form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            new_orden.save()
            contador=request.POST["columnas_receta"]

            i=0
            print('contador:'+str(contador))
            while int(i) <= int(contador):
                i+= 1
                print('contadorentro1:'+str(i))
                if int(i) > int(contador):
                    print('entrosd')
                    print('contadorentro2:'+str(contador))
                    break
                else:
                    if 'id_kits'+str(i) in request.POST:
                        product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                        print('entroA:'+str(i))

                        if 'id_detalle'+str(i) in request.POST:
                            detalle_id=request.POST["id_detalle"+str(i)]
                            detallecompra = PedidoDetalle.objects.get(id=detalle_id)
                            print('product_id:'+str(product.producto_id))
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto =product
                            detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
                            detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
                            detallecompra.total=request.POST["total_kits"+str(i)]
                            detallecompra.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            if 'imagen_kits'+str(i) in request.FILES:
                                detallecompra.imagen=request.FILES["imagen_kits"+str(i)]
                                print('entro imagen:')
                            #detallecompra.imagen=request.FILES["imagen_kits"+str(i)]
                            detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
                            detallecompra.medida=request.POST["medida_kits"+str(i)]
                            detallecompra.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                            detallecompra.nombre=request.POST["nombre_kits"+str(i)]
                            detallecompra.detalle=request.POST["detalle_kits"+str(i)]
                            detallecompra.almacen=request.POST.get('almacen_kits'+str(i), False)
                            detallecompra.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            detallecompra.no_producir = request.POST.get('no_producir_kits' + str(i), False)
                            if 'id_proforma_kits'+str(i) in request.POST:
                                detallecompra.proforma_detalle_id=request.POST["id_proforma_kits"+str(i)]
                                prof_de=ProformaDetalle.objects.get(id=request.POST["id_proforma_kits"+str(i)])
                                prof_de.no_producir = request.POST.get('no_producir_kits' + str(i), False)
                                prof_de.save()
                                proforma_id=prof_de.proforma_id

                            #detallecompra.updated_at = datetime.now()
                            #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                            detallecompra.save()

                            print('Tiene detalle'+str(i))
                        else:
                            print('NO Tiene detalle'+str(i))
                            comprasdetalle=PedidoDetalle()
                            comprasdetalle.pedido_id = new_orden.id
                            comprasdetalle.producto=product
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            comprasdetalle.total=request.POST["total_kits"+str(i)]
                            if 'imagen_kits'+str(i) in request.FILES:
                                comprasdetalle.imagen=request.FILES["imagen_kits"+str(i)]
                            comprasdetalle.observaciones=request.POST["observacion_kits"+str(i)]
                            comprasdetalle.medida=request.POST["medida_kits"+str(i)]
                            comprasdetalle.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                            comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
                            comprasdetalle.detalle=request.POST["detalle_kits"+str(i)]
                            comprasdetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            comprasdetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                            comprasdetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            comprasdetalle.no_producir = request.POST.get('no_producir_kits' + str(i), False)
                            if 'id_proforma_kits'+str(i) in request.POST:
                                comprasdetalle.proforma_detalle_id=request.POST["id_proforma_kits"+str(i)]
                                prof_de=ProformaDetalle.objects.get(id=request.POST["id_proforma_kits"+str(i)])
                                prof_de.no_producir = request.POST.get('no_producir_kits' + str(i), False)
                                prof_de.save()
                                proforma_id=prof_de.proforma_id
                            comprasdetalle.save()

                            print('No Tiene detalle'+str(i))
                            print('contadorsd prueba'+str(contador))
                    else:
                        print('No Tiene id_kits'+str(i))
            #ordencompra_form=OrdenCompraForm(request.POST)
            if proforma_id!=0:
                prof=Proforma.objects.get(id=proforma_id)
                prof.total=new_orden.total
                prof.subtotal=new_orden.subtotal
                prof.descuento=new_orden.descuento
                prof.porcentaje_descuento=new_orden.porcentaje_descuento
                prof.porcentaje_iva=new_orden.porcentaje_iva
                prof.iva=new_orden.iva
                prof.save()
            detalle = PedidoDetalle.objects.filter(pedido_id=p_id).filter(Q(no_producir=False) | Q(no_producir__isnull=True))
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
            ambientes = Ambiente.objects.all().order_by('descripcion')


            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':pedido_form,
            'detalle':detalle,
            'productos':productos,
            'ambientes':ambientes,
            'pedido':pedido,
            'mensaje':'Pedido actualizada con exito'}


            # return render_to_response(
            #     'pedido/actualizar.html',
            #     context,
            #     context_instance=RequestContext(request))
            return HttpResponseRedirect('/pedido/pedido/')
        else:

            pedido_form=PedidoForm(request.POST)
            detalle = PedidoDetalle.objects.filter(pedido_id=pedido.id)
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':pedido_form,
            'detalle':detalle,
            'mensaje':'Pedido actualizada con exito'}

        return render_to_response(
            'pedido/actualizar.html',
            context,
            context_instance=RequestContext(request))

#=====================================================#
@login_required()
def PedidoEliminarView(request):
    return eliminarView(request, Pedido, 'pedido-list')

#=====================================================#
@login_required()
def PedidoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Pedido)
#======================================================#
@login_required()
@csrf_exempt
def misPedidoGuardar(request):
    item = {'exito':0}
    if request.method == 'POST':
        try:

            pedidos = request.POST['data']
            pedidos = json.loads(pedidos)

            for pedido in pedidos:
                if not pedido['codigo'] == "":
                    try:
                            a = Pedido()
                            a.created_by = request.user
                            a.updated_at = datetime.now()
                            a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar el area")
                        pass

                    item = {'exito':1}

            if item['exito'] == 1:
                messages.info(request, 'Pedido guardado!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito':0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')





def PedidoListAprobarView(request):
    cursor = connection.cursor()
    cursor.execute("select distinct p.id,p.codigo,p.fecha,c.nombre_cliente,v.nombre,p.fechaentrega,p.descuento,p.subtotal,p.iva,p.total,p.cliente_id,p.aprobada, p.finalizar_maqueteado,p.anulada,p.abona,count(d.id) from pedido p Left Join  pedido_detalle d on p.id=d.pedido_id and d.render=True Left Join  cliente c on c.id_cliente=p.cliente_id Left Join  vendedor v on v.id=p.vendedor_id where p.aprobada is not True and p.anulada!=True group by p.id,p.codigo,p.fecha,c.nombre_cliente,v.nombre,p.fechaentrega,p.descuento,p.subtotal,p.iva,p.total,p.cliente_id,p.aprobada,p.finalizar_maqueteado,p.anulada,p.abona")
    row = cursor.fetchall()




    #pedidos = Pedido.objects.all()
    return render_to_response('pedido/aprobada.html', {'row': row}, RequestContext(request))

# select distinct p.id,p.codigo,p.fecha,c.nombre_cliente,v.nombre,p.fechaentrega,p.descuento,p.subtotal,p.iva,p.total,p.cliente_id,p.aprobada,
# p.finalizar_maqueteado,p.anulada,p.abona,count(d.id) from pedido p
# Left Join  pedido_detalle d on p.id=d.pedido_id and d.render=True
# Left Join  cliente c on c.id_cliente=p.cliente_id
# Left Join  vendedor v on v.id=p.vendedor_id
# where p.aprobada is not True and p.anulada!=True
# group by p.id,p.codigo,p.fecha,c.nombre_cliente,v.nombre,p.fechaentrega,p.descuento,p.subtotal,p.iva,p.total,p.cliente_id,p.aprobada,p.finalizar_maqueteado,p.anulada,p.abona


@login_required()
def PedidoAprobarByPkView(request, pk):

    objetos = Pedido.objects.filter(id= pk)
    for obj in objetos:
        obj.aprobada = True
        obj.save()

        notificacion = Notificaciones()
        notificacion.group_id = 4
        notificacion.mensaje = "Se ha aprobado un nuevo PEDIDO #" + str(
            obj.codigo) + " con fecha de entrega " + str(obj.fechaentrega) + " del cliente " + str(
            obj.cliente) + " a cargo del vendedor " + str(obj.vendedor)
        notificacion.url = "reunion/reunion/"
        notificacion.created_by = request.user.get_full_name()
        notificacion.updated_by = request.user.get_full_name()
        notificacion.created_at = datetime.now()
        notificacion.updated_at = datetime.now()
        notificacion.save()


    return HttpResponseRedirect('/pedido/pedidoAprobar')

@transaction.atomic
def PedidoCrearProformaView(request,pk):
    if request.method == 'POST':
        pedido_form=PedidoForm(request.POST)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        proformas = Proforma.objects.filter(aprobada=True)
        ambientes = Ambiente.objects.all().order_by('descripcion')
        proforma_id=0

        if pedido_form.is_valid():
            with transaction.atomic():
                new_orden=pedido_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.total=request.POST["total"]
                new_orden.subtotal=request.POST["subtotal"]
                new_orden.descuento=request.POST["descuento"]
                new_orden.porcentaje_descuento=request.POST["porcentaje_descuento"]
                new_orden.porcentaje_iva=request.POST["porcentaje_iva"]
                new_orden.iva=request.POST["iva"]
                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='pedido')
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
                while int(i)<=int(contador):
                    i+= 1
                    print('entro cw'+str(i))
                    if int(i)> int(contador):
                        print('entrosd')
                        break
                    else:
                        print('entroAguardar')
                        if 'id_kits'+str(i) in request.POST:
                            product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                            pedidodetalle=PedidoDetalle()
                            pedidodetalle.pedido_id = new_orden.id
                            pedidodetalle.producto_id=request.POST["id_kits"+str(i)]
                            pedidodetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            pedidodetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            pedidodetalle.nombre=request.POST["nombre_kits"+str(i)]
                            pedidodetalle.medida=request.POST["medida_kits"+str(i)]
                            pedidodetalle.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                            if 'foto_kits'+str(i) in request.FILES:
                                pedidodetalle.imagen=request.FILES["foto_kits"+str(i)]
                                print('entroFoto'+str(i))

                            else:
                                pedidodetalle.imagen = request.POST["imagen_kits"+ str(i)]
                                img=request.POST["imagen_kits"+ str(i)]
                                print('entroImagen' + str(i))
                                print('Imagen:' + str(img))

                            pedidodetalle.observaciones=request.POST["observacion_kits"+str(i)]
                            pedidodetalle.detalle=request.POST["detalle_kits"+str(i)]
                            pedidodetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            pedidodetalle.total=request.POST["total_kits"+str(i)]
                            pedidodetalle.render = request.POST.get('render_kits' + str(i), False)
                            pedidodetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                            pedidodetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            pedidodetalle.no_producir = request.POST.get('no_producir_kits' + str(i), False)
                            if 'id_proforma_kits'+str(i) in request.POST:
                                pedidodetalle.proforma_detalle_id=request.POST["id_proforma_kits"+str(i)]
                                prof_de=ProformaDetalle.objects.get(id=request.POST["id_proforma_kits"+str(i)])
                                prof_de.no_producir = request.POST.get('no_producir_kits' + str(i), False)

                                prof_de.save()
                                proforma_id=prof_de.proforma_id


                            pedidodetalle.save()
                            if pedidodetalle.render:
                                new_orden.maqueteado=True
                                new_orden.save()
                            print('se guardo'+str(contador))


                    print(i)
                    print('contadorsd prueba'+str(contador))
                if proforma_id!=0:
                    prof=Proforma.objects.get(id=proforma_id)
                    prof.total=request.POST["total"]
                    prof.subtotal=request.POST["subtotal"]
                    prof.descuento=request.POST["descuento"]
                    prof.porcentaje_descuento=request.POST["porcentaje_descuento"]
                    prof.porcentaje_iva=request.POST["porcentaje_iva"]
                    prof.iva=request.POST["iva"]
                    prof.save()
                    new_orden.proforma_id=proforma_id
                    new_orden.save()

                return HttpResponseRedirect('/pedido/pedido')
        else:
            print 'error'
            print pedido_form.errors, len(pedido_form.errors)
    else:
        pedido_form=PedidoForm
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        proformas_aprobada = Proforma.objects.get(id = pk)
        detalle_proforma = ProformaDetalle.objects.filter(proforma_id = pk).filter(Q(no_producir=False) | Q(no_producir__isnull=True))
        proformas = Proforma.objects.filter(aprobada=True)
        ambientes = Ambiente.objects.all().order_by('descripcion')
        id_pk=pk
        cursor = connection.cursor()
        cursor.execute(
            "SELECT p.id,p.codigo,p.fecha,p.cliente_id,p.vendedor_id,p.fecha,c.nombre_cliente,p.abreviatura_codigo,v.nombre from proforma p,cliente c,vendedor v where v.id=p.vendedor_id and c.id_cliente=p.cliente_id and p.aprobada=true  and NOT EXISTS (select * from pedido op  where op.proforma_codigo=p.codigo or op.proforma_id=p.id)");

        row = cursor.fetchall();
        return render_to_response('pedido/proforma_create.html', { 'form': pedido_form,'productos':productos,'proformas':proformas,'detalle_proforma':detalle_proforma,'proformas_aprobada':proformas_aprobada,'ambientes':ambientes,'row':row,'id_pk':id_pk},  RequestContext(request))

class PedidoListAprobarVendedorView(ObjectListView):
    model = Pedido
    paginate_by = 100
    table_class = PedidoTable
    filter_class = PedidoFilter
    template_name = 'pedido/aprobadavendedor.html'
    context_object_name = 'pedidos'

    def get_context_data(self, **kwargs):
        context = super(PedidoListAprobarVendedorView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('pedido-delete')
        return context
@login_required()
def PedidoAprobarVendedorByPkView(request, pk):

    objetos = Pedido.objects.filter(id= pk)
    for obj in objetos:
        obj.aprobadavendedor = True
        obj.save()

    return HttpResponseRedirect('/pedido/pedidoAprobarVendor')

def PedidoRenderListView(request):
    cursor = connection.cursor()
    cursor.execute("select distinct p.id,p.codigo,p.fecha,c.nombre_cliente,v.nombre,p.fechaentrega,p.descuento,p.subtotal,p.iva,p.total,p.cliente_id,p.aprobada,p.finalizar_maqueteado,p.anulada,p.abona,count(d.id),p.observacion from pedido p INNER Join  pedido_detalle d on p.id=d.pedido_id and d.render=True Left Join  cliente c on c.id_cliente=p.cliente_id Left Join  vendedor v on v.id=p.vendedor_id where p.aprobada is not True and p.anulada!=True group by p.id,p.codigo,p.fecha,c.nombre_cliente,v.nombre,p.fechaentrega,p.descuento,p.subtotal,p.iva,p.total,p.cliente_id,p.aprobada,p.finalizar_maqueteado,p.anulada,p.abona")
    row = cursor.fetchall()

    #pedidos = Pedido.objects.all()
    return render_to_response('pedido/subir_render_list.html', {'row': row}, RequestContext(request))

# class PedidoRenderListView(ObjectListView):
#     model = Pedido
#     paginate_by = 100
#     template_name = 'pedido/subir_render_list.html'
#     table_class = PedidoTable
#     filter_class = PedidoFilter
#     context_object_name = 'pedidos'
#
#     def get_context_data(self, **kwargs):
#         context = super(PedidoRenderListView, self).get_context_data(**kwargs)
#         context['url_delete'] = reverse_lazy('pedido-delete')
#         return context

@login_required()
def PedidoAnularByPkView(request, pk):

    objetos = Pedido.objects.filter(id= pk)
    for obj in objetos:
        obj.anulada= True
        obj.save()

    return HttpResponseRedirect('/pedido/pedidoAprobar')

def index(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    pedido=Pedido.objects.get(id=pk)
    cursor = connection.cursor();
    cursor.execute("select distinct pd.ambiente_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.total,pd.codigo_produccion,pd.detalle,pd.imagen,op.codigo,op.imagen from pedido p,pedido_detalle pd LEFT JOIN orden_produccion op ON op.pedido_detalle_id=pd.id where p.id=pd.pedido_id and (pd.no_producir is NULL or pd.no_producir=False) and p.id="+pk);
    row = cursor.fetchall();

    cursor = connection.cursor();
    cursor.execute("select distinct pd.ambiente_id,am.descripcion,pd.id from pedido p, pedido_detalle pd,ambiente am where p.id=pd.pedido_id and pd.ambiente_id=am.id and (pd.no_producir is NULL or pd.no_producir=False) and p.id="+pk+" order by pd.id");
    row1 = cursor.fetchall();

    ambientes = []
    x = 0

    for r in row1:
        print('Consulta' + str(r[0]))
        print('Arreglo longitud' + str(len(ambientes)))
        if len(ambientes) > 0:
            cont = 0
            print('Contador inicial' + str(cont))
            for a in ambientes:
                print('AMBIENTE' + str(a[0]) + 'sql' + str(r[0]))

                if r[0] == a[0]:
                    print('Es igual' + str(r[0]))

                    cont = cont + 1

            print('Contador' + str(cont))
            if cont == 0:
                print('Arreglo' + str(a))
                print('Am' + str(a[0]))
                ambientes.append(r)
                x = x + 1
        else:
            print('Entro 1 vez')
            ambientes.append(r)
            x = x + 1

    html = render_to_string('pedido/imprimir.html', {'pagesize':'A4','pedido':pedido,'row':row,'ambiente':ambientes,'media_root':settings.MEDIA_ROOT}, context_instance=RequestContext(request))
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


@login_required()
def PedidoHistoricoListView(request):
    pedido = Pedido.objects.all().order_by('id')


    return render_to_response('pedido/historico.html', {'pedidos': pedido}, RequestContext(request))


class PedidoHistoricoUpdateView(ObjectUpdateView):


    def get(self, request, *args, **kwargs):

        pedido = Pedido.objects.get(id=kwargs['pk'])
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')

        pedido_form=PedidoForm(instance=pedido)
        detalle = PedidoDetalle.objects.filter(pedido_id=pedido.id)

        context = {
        'section_title':'Actualizar Pedido',
        'button_text':'Actualizar',
        'form':pedido_form,
        'productos':productos,
        'ambientes':ambientes,
        'detalle':detalle,
        'pedido':pedido
        }

        return render_to_response(
            'pedido/actualizar_historico.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        pedido = Pedido.objects.get(id=kwargs['pk'])
        pedido_form = PedidoForm(request.POST,request.FILES,instance=pedido)
        p_id=kwargs['pk']
        print(p_id)
        print pedido_form.is_valid(), pedido_form.errors, type(pedido_form.errors)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

        if pedido_form.is_valid() :

            new_orden=pedido_form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
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
                        product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                        if 'id_detalle'+str(i) in request.POST:
                            detalle_id=request.POST["id_detalle"+str(i)]
                            detallecompra = PedidoDetalle.objects.get(id=detalle_id)
                            print('product_id:'+str(product.producto_id))
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto =product
                            detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
                            detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
                            detallecompra.total=request.POST["total_kits"+str(i)]
                            detallecompra.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            if 'imagen_kits'+str(i) in request.FILES:
                                detallecompra.imagen=request.FILES["imagen_kits"+str(i)]
                                print('entro imagen:')
                            detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
                            detallecompra.medida=request.POST["medida_kits"+str(i)]
                            detallecompra.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                            detallecompra.nombre=request.POST["nombre_kits"+str(i)]
                            detallecompra.detalle=request.POST["detalle_kits"+str(i)]
                            detallecompra.almacen=request.POST.get('almacen_kits'+str(i), False)
                            detallecompra.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            detallecompra.no_producir = request.POST.get('no_producir_kits' + str(i), False)
                            if 'id_proforma_kits'+str(i) in request.POST:
                                detallecompra.proforma_detalle_id=request.POST["id_proforma_kits"+str(i)]
                                prof_de=ProformaDetalle.objects.get(id=request.POST["id_proforma_kits"+str(i)])
                                prof_de.no_producir = request.POST.get('no_producir_kits' + str(i), False)
                                prof_de.save()
                                proforma_id=prof_de.proforma_id

                            #detallecompra.updated_at = datetime.now()
                            #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                            detallecompra.save()

                            print('Tiene detalle'+str(i))
                        else:
                            comprasdetalle=PedidoDetalle()
                            comprasdetalle.pedido_id = new_orden.id
                            comprasdetalle.producto=product
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            comprasdetalle.total=request.POST["total_kits"+str(i)]
                            #comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
                            comprasdetalle.observaciones=request.POST["observacion_kits"+str(i)]
                            comprasdetalle.medida=request.POST["medida_kits"+str(i)]
                            comprasdetalle.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                            comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
                            comprasdetalle.detalle=request.POST["detalle_kits"+str(i)]
                            comprasdetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            comprasdetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                            comprasdetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            comprasdetalle.no_producir = request.POST.get('no_producir_kits' + str(i), False)

                            if 'id_proforma_kits'+str(i) in request.POST:
                                comprasdetalle.proforma_detalle_id=request.POST["id_proforma_kits"+str(i)]
                                prof_de=ProformaDetalle.objects.get(id=request.POST["id_proforma_kits"+str(i)])
                                prof_de.no_producir = request.POST.get('no_producir_kits' + str(i), False)
                                prof_de.save()
                                proforma_id=prof_de.proforma_id

                            comprasdetalle.save()
                            i+= 1
                            print('No Tiene detalle'+str(i))
                            print('contadorsd prueba'+str(contador))
            #ordencompra_form=OrdenCompraForm(request.POST)
            if proforma_id!=0:
                prof=Proforma.objects.get(id=proforma_id)
                prof.total=new_orden.total
                prof.subtotal=new_orden.subtotal
                prof.descuento=new_orden.descuento
                prof.porcentaje_descuento=new_orden.porcentaje_descuento
                prof.porcentaje_iva=new_orden.porcentaje_iva
                prof.iva=new_orden.iva
                prof.save()
            detalle = PedidoDetalle.objects.filter(pedido_id=p_id)
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
            ambientes = Ambiente.objects.all().order_by('descripcion')


            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':pedido_form,
            'detalle':detalle,
            'productos':productos,
            'ambientes':ambientes,
            'pedido':pedido,
            'mensaje':'Pedido actualizada con exito'}


            return render_to_response(
                'pedido/actualizar_historico.html',
                context,
                context_instance=RequestContext(request))
        else:

            pedido_form=PedidoForm(request.POST)
            detalle = PedidoDetalle.objects.filter(pedido_id=pedido.id)
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':pedido_form,
            'detalle':detalle,
            'mensaje':'Pedido actualizada con exito'}

        return render_to_response(
            'pedido/actualizar_historico.html',
            context,
            context_instance=RequestContext(request))



def imprimirValores(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    pedido=Pedido.objects.get(id=pk)
    cursor = connection.cursor();
    cursor.execute("select distinct pd.ambiente_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.total,pd.codigo_produccion,pd.detalle from pedido p,pedido_detalle pd where p.id=pd.pedido_id and (pd.no_producir is NULL or pd.no_producir=False) and p.id="+pk);
    row = cursor.fetchall();

    cursor = connection.cursor();
    cursor.execute("select distinct pd.ambiente_id,am.descripcion,pd.id from pedido p, pedido_detalle pd,ambiente am where p.id=pd.pedido_id and pd.ambiente_id=am.id and (pd.no_producir is NULL or pd.no_producir=False) and p.id="+pk+" order by pd.id");
    row1 = cursor.fetchall();
    ambientes = []
    x = 0

    for r in row1:
        print('Consulta' + str(r[0]))
        print('Arreglo longitud' + str(len(ambientes)))
        if len(ambientes) > 0:
            cont = 0
            print('Contador inicial' + str(cont))
            for a in ambientes:
                print('AMBIENTE' + str(a[0]) + 'sql' + str(r[0]))

                if r[0] == a[0]:
                    print('Es igual' + str(r[0]))

                    cont = cont + 1

            print('Contador' + str(cont))
            if cont == 0:
                print('Arreglo' + str(a))
                print('Am' + str(a[0]))
                ambientes.append(r)
                x = x + 1
        else:
            print('Entro 1 vez')
            ambientes.append(r)
            x = x + 1


    html = render_to_string('pedido/imprimir_valores.html', {'pagesize':'A4','pedido':pedido,'row':row,'ambiente':ambientes,'media_root':settings.MEDIA_ROOT}, context_instance=RequestContext(request))
    return generar_pdf(html)


# class PedidoRenderView(TemplateView):
#     def get(self, request, *args, **kwargs):
#
#         proforma = Pedido.objects.get(id=kwargs['pk'])
#         productos = Producto.objects.all()
#         proforma_form = PedidoForm(instance=proforma)
#         detalle = PedidoDetalle.objects.filter(pedido_id=proforma.id)
#
#         context = {
#             'section_title': 'Actualizar Presupuesto',
#             'button_text': 'Actualizar',
#             'form': proforma_form,
#             'productos': productos,
#             'detalle': detalle
#         }
#
#         return render_to_response(
#             'pedido/subir_render.html', context, context_instance=RequestContext(request))
#
#     def post(sel, request, *args, **kwargs):
#         proforma = Pedido.objects.get(id=kwargs['pk'])
#         proforma_form = PedidoForm(request.POST, request.FILES, instance=proforma)
#         p_id = kwargs['pk']
#         print(p_id)
#         print proforma_form.is_valid(), proforma_form.errors, type(proforma_form.errors)
#         productos = Producto.objects.all()
#
#         if proforma_form.is_valid():
#
#             proforma.save()
#
#             new_orden = proforma.save()
#
#             contador = request.POST["columnas_receta"]
#
#             i = 0
#             while int(i) <= int(contador):
#                 i += 1
#                 if int(i) > int(contador):
#                     print('entrosd')
#                     break
#                 else:
#                     if 'id_kits' + str(i) in request.POST:
#                         product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
#                         detalle_id = request.POST["id_detalle" + str(i)]
#
#                         if detalle_id:
#                             detallecompra = PedidoDetalle.objects.get(id=detalle_id)
#                             detallecompra.updated_by = request.user.get_full_name()
#                             detallecompra.producto = product
#                             # detallecompra.largo=request.POST["largo_kits"+str(i)]
#                             # detallecompra.fondo=request.POST["fondo_kits"+str(i)]
#                             # detallecompra.alto=request.POST["alto_kits"+str(i)]
#                             if (len(request.POST["imagen_kits" + str(i)])) != 0:
#                                 detallecompra.imagen = request.FILES["imagen_kits" + str(i)]
#                             detallecompra.observaciones = request.POST["observacion_kits" + str(i)]
#                             detallecompra.save()
#                         else:
#                             comprasdetalle = PedidoDetalle()
#                             comprasdetalle.pedido_id = new_orden.id
#                             comprasdetalle.producto = product
#                             # comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
#                             # comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
#                             # comprasdetalle.total=request.POST["total_kits"+str(i)]
#                             comprasdetalle.imagen = request.POST["imagen_kits" + str(i)]
#                             comprasdetalle.observaciones = request.POST["observacion_kits" + str(i)]
#
#                             comprasdetalle.save()
#                             i += 1
#                             print('No Tiene detalle' + str(i))
#                             print('contadorsd prueba' + str(contador))
#             # ordencompra_form=OrdenCompraForm(request.POST)
#             detalle = PedidoDetalle.objects.filter(pedido_id=p_id)
#             productos = Producto.objects.all()
#
#             context = {
#                 'section_title': 'Actualizar Proforma',
#                 'button_text': 'Actualizar',
#                 'form': proforma_form,
#                 'detalle': detalle,
#                 'productos': productos,
#                 'mensaje': 'Pedido actualizada con exito'}
#
#             return render_to_response(
#                 'pedido/subir_render.html',
#                 context,
#                 context_instance=RequestContext(request))
#         else:
#
#             proforma_form = PedidoForm(request.POST)
#             detalle = PedidoDetalle.objects.filter(pedido_id=proforma.id)
#             productos = Producto.objects.all()
#
#             context = {
#                 'section_title': 'Actualizar Pedido',
#                 'button_text': 'Actualizar',
#                 'form': proforma_form,
#                 'detalle': detalle,
#                 'mensaje': 'Proforma actualizada con exito'}
#
#         return render_to_response(
#             'pedido/subir_render.html',
#             context,
#             context_instance=RequestContext(request))
#


class PedidoRenderView(ObjectUpdateView):


    def get(self, request, *args, **kwargs):

        pedido = Pedido.objects.get(id=kwargs['pk'])
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')

        pedido_form=PedidoForm(instance=pedido)
        detalle = PedidoDetalle.objects.filter(pedido_id=pedido.id).filter(Q(no_producir=False) | Q(no_producir__isnull=True))

        context = {
        'section_title':'Actualizar Pedido',
        'button_text':'Actualizar',
        'form':pedido_form,
        'productos':productos,
        'ambientes':ambientes,
        'detalle':detalle,
        'pedido':pedido
        }

        return render_to_response(
            'pedido/subir_render.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        pedido = Pedido.objects.get(id=kwargs['pk'])
        pedido.finalizar_maqueteado=request.POST.get('finalizar_maqueteado', False)
        pedido.updated_by = request.user.get_full_name()
        pedido.updated_at = datetime.now()
        pedido.save()
        #pedido_form = PedidoForm(request.POST,request.FILES,instance=pedido)
        p_id=kwargs['pk']
        print(p_id)
        #print pedido_form.is_valid(), pedido_form.errors, type(pedido_form.errors)
        #productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

        # if pedido_form.is_valid() :
        #
        #     new_orden=pedido_form.save()
        #     new_orden.updated_by = request.user.get_full_name()
        #     new_orden.updated_at = datetime.now()
        #     new_orden.save()
        #     contador=request.POST["columnas_receta"]
        #
        #     i=0
        #     # print('contador:'+str(contador))
        #     # while int(i) <= int(contador):
        #     #     i+= 1
        #     #     print('contadorentro1:'+str(i))
        #     #     if int(i) > int(contador):
        #     #         print('entrosd')
        #     #         print('contadorentro2:'+str(contador))
        #     #         break
        #     #     else:
        #     #         if 'id_kits'+str(i) in request.POST:
        #     #             product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
        #     #             print('entroA:'+str(i))
        #     #
        #     #             if 'id_detalle'+str(i) in request.POST:
        #     #                 detalle_id=request.POST["id_detalle"+str(i)]
        #     #                 detallecompra = PedidoDetalle.objects.get(id=detalle_id)
        #     #                 print('product_id:'+str(product.producto_id))
        #     #                 detallecompra.updated_by = request.user.get_full_name()
        #     #                 detallecompra.producto =product
        #     #                 detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
        #     #                 detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
        #     #                 detallecompra.total=request.POST["total_kits"+str(i)]
        #     #                 detallecompra.ambiente_id=request.POST["ambientes_kits"+str(i)]
        #     #                 if 'imagen_kits'+str(i) in request.FILES:
        #     #                     detallecompra.imagen=request.FILES["imagen_kits"+str(i)]
        #     #                     print('entro imagen:')
        #     #                 #detallecompra.imagen=request.FILES["imagen_kits"+str(i)]
        #     #                 detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
        #     #                 detallecompra.medida=request.POST["medida_kits"+str(i)]
        #     #                 detallecompra.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
        #     #                 detallecompra.nombre=request.POST["nombre_kits"+str(i)]
        #     #                 detallecompra.detalle=request.POST["detalle_kits"+str(i)]
        #     #                 detallecompra.almacen=request.POST.get('almacen_kits'+str(i), False)
        #     #                 detallecompra.reparacion=request.POST.get('reparacion_kits'+str(i), False)
        #     #                 detallecompra.no_producir = request.POST.get('no_producir_kits' + str(i), False)
        #     #                 if 'id_proforma_kits'+str(i) in request.POST:
        #     #                     detallecompra.proforma_detalle_id=request.POST["id_proforma_kits"+str(i)]
        #     #                     prof_de=ProformaDetalle.objects.get(id=request.POST["id_proforma_kits"+str(i)])
        #     #                     prof_de.no_producir = request.POST.get('no_producir_kits' + str(i), False)
        #     #                     prof_de.save()
        #     #                     proforma_id=prof_de.proforma_id
        #     #
        #     #                 #detallecompra.updated_at = datetime.now()
        #     #                 #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
        #     #                 detallecompra.save()
        #     #
        #     #                 print('Tiene detalle'+str(i))
        #     #             else:
        #     #                 print('NO Tiene detalle'+str(i))
        #     #                 comprasdetalle=PedidoDetalle()
        #     #                 comprasdetalle.pedido_id = new_orden.id
        #     #                 comprasdetalle.producto=product
        #     #                 comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
        #     #                 comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
        #     #                 comprasdetalle.total=request.POST["total_kits"+str(i)]
        #     #                 if 'imagen_kits'+str(i) in request.FILES:
        #     #                     comprasdetalle.imagen=request.FILES["imagen_kits"+str(i)]
        #     #                 comprasdetalle.observaciones=request.POST["observacion_kits"+str(i)]
        #     #                 comprasdetalle.medida=request.POST["medida_kits"+str(i)]
        #     #                 comprasdetalle.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
        #     #                 comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
        #     #                 comprasdetalle.detalle=request.POST["detalle_kits"+str(i)]
        #     #                 comprasdetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
        #     #                 comprasdetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
        #     #                 comprasdetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
        #     #                 comprasdetalle.no_producir = request.POST.get('no_producir_kits' + str(i), False)
        #     #                 if 'id_proforma_kits'+str(i) in request.POST:
        #     #                     comprasdetalle.proforma_detalle_id=request.POST["id_proforma_kits"+str(i)]
        #     #                     prof_de=ProformaDetalle.objects.get(id=request.POST["id_proforma_kits"+str(i)])
        #     #                     prof_de.no_producir = request.POST.get('no_producir_kits' + str(i), False)
        #     #                     prof_de.save()
        #     #                     proforma_id=prof_de.proforma_id
        #     #                 comprasdetalle.save()
        #     #                 i+= 1
        #     #                 print('No Tiene detalle'+str(i))
        #     #                 print('contadorsd prueba'+str(contador))
        #     #         else:
        #     #             print('No Tiene id_kits'+str(i))
        #     # #ordencompra_form=OrdenCompraForm(request.POST)
        #     # if proforma_id!=0:
        #     #     prof=Proforma.objects.get(id=proforma_id)
        #     #     prof.total=new_orden.total
        #     #     prof.subtotal=new_orden.subtotal
        #     #     prof.descuento=new_orden.descuento
        #     #     prof.porcentaje_descuento=new_orden.porcentaje_descuento
        #     #     prof.porcentaje_iva=new_orden.porcentaje_iva
        #     #     prof.iva=new_orden.iva
        #     #     prof.save()
        #     detalle = PedidoDetalle.objects.filter(pedido_id=p_id).filter(Q(no_producir=False) | Q(no_producir__isnull=True))
        #     productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        #     ambientes = Ambiente.objects.all().order_by('descripcion')
        #
        #
        #     context = {
        #    'section_title':'Actualizar Proforma',
        #     'button_text':'Actualizar',
        #     'form':pedido_form,
        #     'detalle':detalle,
        #     'productos':productos,
        #     'ambientes':ambientes,
        #     'pedido':pedido,
        #     'mensaje':'Pedido actualizada con exito'}
        #
        #
        #     return render_to_response(
        #         'pedido/subir_render.html',
        #         context,
        #         context_instance=RequestContext(request))
        # else:
        #
        #     pedido_form=PedidoForm(request.POST)
        #     detalle = PedidoDetalle.objects.filter(pedido_id=pedido.id)
        #     productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        #
        #     context = {
        #     'section_title':'Actualizar Proforma',
        #     'button_text':'Actualizar',
        #     'form':pedido_form,
        #     'detalle':detalle,
        #     'mensaje':'Pedido actualizada con exito'}

        pedido_form = PedidoForm(request.POST)
        detalle = PedidoDetalle.objects.filter(pedido_id=pedido.id)
        #productos = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto','bloquea', 'medida_peso', 'costo', 'precio1', 'precio2').exclude(tipo_producto=1)

        context = {
            'section_title': 'Actualizar Proforma',
            'button_text': 'Actualizar',
            'form': pedido_form,
            'detalle': detalle,
            'mensaje': 'Pedido actualizada con exito'}
        return render_to_response(
            'pedido/subir_render.html',
            context,
            context_instance=RequestContext(request))



def SubirImagenesRenderView(request, pk):
    if request.method == 'POST':

        form=ImagenesPedidoForm(request.POST)


        if form.is_valid():
            if 'imagen' in request.FILES:
                new_orden=form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.pedido_detalle_id = pk

                new_orden.imagen=request.FILES["imagen"]

                new_orden.save()
            form=ImagenesPedidoForm
            detalle = ImagenesPedido.objects.filter(pedido_detalle_id=pk)
            detailprof = PedidoDetalle.objects.get(id=pk)
            prof = Pedido.objects.get(id=detailprof.pedido_id)


            return render_to_response('pedido/subir_imagenes.html', { 'form': form,'detalle':detalle,'detailprof':detailprof,'prof':prof},  RequestContext(request))

        else:
            print 'error'
            print form.errors, len(form.errors)
    else:

        form = ImagenesPedidoForm
        detalle = ImagenesPedido.objects.filter(pedido_detalle_id=pk)
        detailprof = PedidoDetalle.objects.get(id=pk)
        prof = Pedido.objects.get(id=detailprof.pedido_id)



        return render_to_response('pedido/subir_imagenes.html', { 'form': form,'detalle':detalle,'detailprof':detailprof,'prof':prof},  RequestContext(request))


@csrf_exempt
def guardarImagenesView(request):
    if request.method == 'POST':
        form = ImagenesPedidoForm(request.POST)

        if form.is_valid():
            if 'imagen' in request.FILES:
                new_orden = form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.pedido_detalle_id = pk

                new_orden.imagen = request.FILES["imagen"]

                new_orden.save()


            html='Guarddo'
            return HttpResponse(
                html
            )
        else:
            raise Http404
    else:
        form = ImagenesPedidoForm()

        raise Http404



def VerImagenesRenderPedidoView(request, pk):
    cursor = connection.cursor()
    cursor.execute(
        "select distinct p.id,p.descripcion,p.pedido_detalle_id,p.imagen from imagenes_pedido p,pedido ped,pedido_detalle pd where ped.id=pd.pedido_id and pd.id=p.pedido_detalle_id and ped.id="+str(pk))
    detalle = cursor.fetchall()
    #detalle = ImagenesPedido.objects.filter(pedido_detalle_id=pk)
    detailprof = PedidoDetalle.objects.filter(pedido_id=pk)
    prof = Pedido.objects.get(id=pk)

    return render_to_response('pedido/verrender.html', { 'detalle': detalle, 'detailprofs': detailprof, 'prof': prof,'media_root':settings.MEDIA_ROOT},
                              RequestContext(request))



@login_required()
@csrf_exempt
def pedido_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order=request.GET['order[0][column]']
        _order_dir=request.GET['order[0][dir]']
        cursor = connection.cursor()
        #sql="  select m.id,t.descripcion,m.fecha_emision,m.numero_comprobante,m.paguese_a,p.ruc,td.descripcion,m.numero_cheque,b.nombre,m.monto_cheque,m.monto,m.descripcion,m.activo,m.conciliacion_id from movimiento m left join proveedor p on p.proveedor_id=m.proveedor_id left join tipo_documento td on td.id=m.tipo_documento_id and td.id=1 left join tipo_anticipo t on t.id=m.tipo_anticipo_id and t.id=1 left join banco b on b.id=m.banco_id where m.tipo_anticipo_id=1 and m.tipo_documento_id=1 "
        sql="select p.id,p.codigo,p.fecha,c.nombre_cliente,p.subtotal,p.porcentaje_descuento,p.descuento,p.iva,p.total,p.proforma_codigo,p.abreviatura_codigo,p.anulada,p.aprobada,p.finalizar_maqueteado, COALESCE(p.saldo, 0) AS saldo  from pedido p left join cliente c on c.id_cliente=p.cliente_id left join proforma pr on pr.id=p.proforma_id where 1=1 "
        if _search_value:
            sql+=" and ( UPPER(p.codigo) like '%"+_search_value+"%' or UPPER(c.nombre_cliente) like '%"+_search_value.upper()+"%' or CAST(p.porcentaje_descuento as VARCHAR)  like '%"+_search_value.upper()+"%'  or CAST(p.descuento as VARCHAR)  like '%"+_search_value.upper()+"%'  or CAST(p.iva as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(p.subtotal as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(p.total as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(p.fecha as VARCHAR)  like '%"+_search_value+"%' or UPPER(p.proforma_codigo) like '%"+_search_value.upper()+"%' or UPPER(p.abreviatura_codigo) like '%"+_search_value.upper()+"%'"
        
        if _search_value.upper()  in 'APROBADA':
            sql+=" or p.aprobada is True"
        
        if _search_value.upper()  in 'ESPERANDO APROBACION':
            sql+=" or p.aprobada is not True"
        if _search_value.upper()  in 'FINALIZADO RENDER':
            sql+=" or p.finalizar_maqueteado is  True"
        if _search_value:
             sql+=" ) "
            
           
    
        #sql +=" order by fecha"
        print _order
        if _order == '0':
            sql +=" order by p.codigo "+_order_dir
        if _order == '1':
            sql +=" order by p.fecha "+_order_dir
        if _order == '2':
            sql +=" order by c.nombre_cliente "+_order_dir
        
        if _order == '3':
            sql +=" order by p.subtotal "+_order_dir
        
        if _order == '4':
            sql +=" order by p.porcentaje_descuento "+_order_dir
        if _order == '5':
            sql +=" order by p.descuento "+_order_dir
        if _order == '6':
            
            sql +=" order by p.iva "+_order_dir
        if _order == '7':
            
            sql +=" order by p.total "+_order_dir
        
        if _order == '8':
            sql +=" order by p.abreviatura_codigo,p.proforma_codigo "+_order_dir
            
        
        
        
        print sql
        cursor.execute(sql)
        compras = cursor.fetchall()
            
        compras_filtered = compras[_start:_start + _end]

        compras_list = []
        for o in compras_filtered:
            compras_obj = []
            
            compras_obj.append(o[1])
            compras_obj.append(o[2].strftime('%Y-%m-%d'))
            compras_obj.append(o[3])
            compras_obj.append(o[4])
            compras_obj.append(o[5])
            compras_obj.append(o[6])
            compras_obj.append(o[7])
            compras_obj.append(o[14])
            compras_obj.append(o[8])
            codigo=str(o[10])+'-'+str(o[9])
            compras_obj.append(codigo)
           
            html=''

            if o[12]:
                compras_obj.append("Aprobada")
            else:
                
                if o[11]:
                    compras_obj.append("Anulado")
                else:
                    if o[13]:
                        compras_obj.append("Esperando Aprobacion <br /> *Finalizado Render")
                        html+='<span class="input-group-btn input"><a href="javascript: render_ad('+str(o[0])+')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-camera">Ver Render</i></a></span>'
                    else:
                        compras_obj.append("Esperando Aprobacion")
                        html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/pedido/pedido/'+str(o[0])+'/editar" target="_blank"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Editar</button></a>'
                    
            html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/pedido/imprimir/'+str(o[0])+'/" style="" target="_blank"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Imprimir</button></a>'
            html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/pedido/imprimirValores/'+str(o[0])+'/" style="" target="_blank"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Imprimir Valores</button></a>'
            html+='<button type="button" class="btn btn-info btn-xs" data-toggle="modal" data-target="#quantityModal" data-product-id="'+str(o[0])+'"><i class="fa fa-cog"></i> Act. Totales</button>'
            
                   
            
            

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

def actualizar_saldo(request):
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        cantidad = request.POST.get('cantidad')
        # try:
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.saldo += cantidad
        pedido.save()
        return HttpResponse('lista_pedidos', 200)  # Redirige a una vista de lista de pedidos o cualquier otra vista
    return HttpResponse("Pedido no encontrado", status=404)
