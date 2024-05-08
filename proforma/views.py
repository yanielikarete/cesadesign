
# Create your views here.
# -*- coding: utf-8 -*-
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
import simplejson as json
import datetime
from .models import *
from clientes.models import *
from .forms import *
from ambiente.models import *
from django.db.models import Q
from django.conf import settings

from .tables import *
from .filters import *
from django.views.decorators.csrf import csrf_exempt
from inventario.models import *
from django.db import connection, transaction
from reunion.models import *
from config.models import *
from django.views.generic import TemplateView

from django.forms.extras.widgets import *
from django.contrib.auth import authenticate,login
#from login.lib.tools import Tools


import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

# import ho.pisa as pisa
from xhtml2pdf import pisa
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

#======================PROFORMA=============================#


class ProformaListView(ObjectListView):
    model = Proforma
    paginate_by = 100
    template_name = 'proforma/index.html'
    table_class = ProformaTable
    filter_class = ProformaFilter
    context_object_name = 'reuniones'

    def get_context_data(self, **kwargs):
        context = super(ProformaListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('proforma-delete')
        return context

@login_required()
def ConsultaProformaListView(request):
    #proformas = Proforma.objects.all().order_by('id')
    cursor = connection.cursor()
    query=" select o.id,o.abreviatura_codigo,o.codigo,o.fecha,p.nombre,c.nombre_cliente,v.nombre,o.tiempo_respuesta,o.aprobada,o.anulada,bp.id from proforma o left join puntos_venta p on p.id=o.puntos_venta_id left join cliente c on c.id_cliente=o.cliente_id left join vendedor v on v.id=o.vendedor_id left join bloqueo_periodo bp on  date_part('year',bp.fecha)=EXTRACT(YEAR FROM o.fecha) and date_part('month',bp.fecha)=EXTRACT(MONTH from o.fecha) order by o.fecha desc"

    cursor.execute(query)
    ro = cursor.fetchall()


    return render_to_response('proforma/list.html', {'proformas': ro}, RequestContext(request))

@login_required()
def SeguimientoReuniones(request):
    cursor = connection.cursor();

    cursor.execute("SELECT  distinct reunion.codigo,reunion.motivo,reunion.fecha,reunion.tiempo_respuesta,proforma.codigo, proforma.fecha FROM reunion LEFT JOIN proforma ON proforma.reunion_codigo=reunion.codigo");
    row = cursor.fetchall();
    return render_to_response('proforma/seguimiento_reuniones.html', { 'row': row,},  RequestContext(request))



#=====================================================#
class ProformaDetailView(ObjectDetailView):
    model = Proforma
    template_name = 'proforma/detail.html'

#=====================================================#
@login_required()
@transaction.atomic
def ProformaCreateView(request):
      if request.method == 'POST':
        proforma_form=ProformaForm(request.POST)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')
        proformas=CotizacionProforma.objects.filter(cotizacion_finalizada=True)


        if proforma_form.is_valid():
            try:
                with transaction.atomic():
                    new_orden=proforma_form.save()
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
                        if new_orden.puntos_venta_id == 1:
                            if new_orden.hierro_proforma:
                                secuencial = Secuenciales.objects.get(modulo='proformafabricahierro')
                            else:
                                secuencial = Secuenciales.objects.get(modulo='proforma')

                        if new_orden.puntos_venta_id == 2:
                            secuencial = Secuenciales.objects.get(modulo='proformasamborondon')
                        if new_orden.puntos_venta_id == 3:
                            secuencial = Secuenciales.objects.get(modulo='proformaurdesa')

                        if secuencial.secuencial!=new_orden.codigo:
                            new_orden.codigo='00'+str(secuencial.secuencial)
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
                        print('entro comoqw'+str(i))
                        if int(i)> int(contador):
                            print('entrosd')
                            break
                        else:
                            if 'id_kits'+str(i) in request.POST:
                                product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                                ambiente=Ambiente.objects.get(id=request.POST["ambientes_kits"+str(i)])

                                proformadetalle=ProformaDetalle()
                                proformadetalle.proforma_id = new_orden.id
                                proformadetalle.producto_id=request.POST["id_kits"+str(i)]
                                proformadetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                                proformadetalle.nombre=request.POST["nombre_kits"+str(i)]
                                proformadetalle.medida=request.POST["medida_kits"+str(i)]
                                proformadetalle.detalle=request.POST["detalle_kits"+str(i)]
                                proformadetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                                proformadetalle.imagen =product.imagen

                                # if (len(request.POST["imagen_kits"+str(i)])) != 0:
                                #     print('prueba'+str(contador))

                                if "imagen_kits" + str(i) in request.FILES:
                                    proformadetalle.imagen = request.FILES["imagen_kits" + str(i)]

                                proformadetalle.observaciones=request.POST["observacion_kits"+str(i)]

                                #kits.costo=float(request.POST["costo_kits1"])
                                proformadetalle.precio_compra=request.POST["costo_kits"+str(i)] if len(request.POST["costo_kits"+str(i)]) > 0 else 0
                                proformadetalle.total=request.POST["total_kits"+str(i)] if not request.POST["total_kits"+str(i)] == "NaN" else 0
                                proformadetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                                proformadetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                                proformadetalle.save()

                        print(i)
                        print('contadorsd prueba'+str(contador))
            except IntegrityError:
                print 'error'
                print proforma_form.errors, len(proforma_form.errors)
            return HttpResponseRedirect('/proforma/consultarproforma')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
      else:
        proforma_form=ProformaForm
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')
        iva = Parametros.objects.get(clave='iva')
        cotizacionproformas = CotizacionProforma.objects.filter(cotizacion_finalizada=True).order_by('id')


      return render_to_response('proforma/create.html', { 'form': proforma_form,'productos':productos,'cotizacionproformas':cotizacionproformas,'ambientes':ambientes,'iva':iva},  RequestContext(request))

@login_required()
def ProformaCreateReunionView(request, pk):
      if request.method == 'POST':
        proforma_form=ProformaForm(request.POST)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

        if proforma_form.is_valid():
            new_orden=proforma_form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.total=request.POST["total"]

            new_orden.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='proforma')
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
                print('entro comoqw'+str(i))
                if int(i)> int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits'+str(i) in request.POST:
                        product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                        proformadetalle=ProformaDetalle()
                        proformadetalle.proforma_id = new_orden.id
                        proformadetalle.producto_id=request.POST["id_kits"+str(i)]
                        proformadetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                        proformadetalle.nombre=request.POST["nombre_kits"+str(i)]
                        proformadetalle.medida=request.POST["medida_kits"+str(i)]

                        #proformadetalle.imagen=request.POST["imagen_kits"+str(i)]

                        proformadetalle.observaciones=request.POST["observacion_kits"+str(i)]

                        #kits.costo=float(request.POST["costo_kits1"])
                        proformadetalle.precio_compra=request.POST["costo_kits"+str(i)]
                        proformadetalle.total=request.POST["total_kits"+str(i)]
                        proformadetalle.save()

                print(i)
                print('contadorsd prueba'+str(contador))

            return HttpResponseRedirect('/proforma/proforma')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
      else:
        proforma_form=ProformaForm
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        reunion = Reunion.objects.get(id=pk)


      return render_to_response('proforma/createreunion.html', { 'form': proforma_form,'productos':productos,'reunion':reunion},  RequestContext(request))


# class ProformaCreateView(ObjectCreateView):
#     model = Proforma
#     form_class = ProformaForm
#     template_name = 'proforma/create.html'
#     url_success = 'proforma-list'
#     url_success_other = 'proforma-create'
#     url_cancel = 'proforma-list'


#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.created_by = self.request.user
#         self.object.created_at = datetime.now()
#         self.object.updated_at = datetime.now()
#         self.object.save()

#         return super(ProformaCreateView, self).form_valid(form)

#     def get_success_url(self):
#         mensaje = "Ha ingresado 1 nueva proforma."
#         messages.success(self.request, mensaje)

#         if '_addanother' in self.request.POST and self.request.POST['_addanother']:
#             return reverse_lazy(self.url_success_other)
#         else:
#             return reverse_lazy(self.url_success)

#=====================================================#
class ProformaUpdateView(ObjectUpdateView):
    def get(self, request, *args, **kwargs):

        proforma = Proforma.objects.get(id=kwargs['pk'])
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')

        proforma_form=ProformaForm(instance=proforma)
        detalle = ProformaDetalle.objects.filter(proforma_id=proforma.id).filter(Q(no_producir=False) | Q(no_producir__isnull=True))

        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'form':proforma_form,
        'productos':productos,
        'ambientes':ambientes,
        'detalle':detalle,
        'proforma':proforma
        }

        return render_to_response(
            'proforma/actualizar.html', context,context_instance=RequestContext(request))


    def post(sel, request, *args, **kwargs):
        proforma = Proforma.objects.get(id=kwargs['pk'])
        proforma_form = ProformaForm(request.POST,request.FILES,instance=proforma)
        p_id=kwargs['pk']
        print(p_id)
        print proforma_form.is_valid(), proforma_form.errors, type(proforma_form.errors)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

        if proforma_form.is_valid() :

            new_orden=proforma_form.save()
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
                            detallecompra = ProformaDetalle.objects.get(id=detalle_id)
                            print('product_id:'+str(product.producto_id))
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto =product
                            detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
                            detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
                            detallecompra.total=request.POST["total_kits"+str(i)]
                            detallecompra.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            if 'imagen_kits'+str(i) in request.FILES:
                                detallecompra.imagen=request.FILES["imagen_kits"+str(i)]

                            #detallecompra.imagen=request.POST["imagen_kits"+str(i)]
                            detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
                            detallecompra.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                            detallecompra.medida=request.POST["medida_kits"+str(i)]
                            detallecompra.nombre=request.POST["nombre_kits"+str(i)]
                            detallecompra.detalle=request.POST["detalle_kits"+str(i)]
                            detallecompra.almacen=request.POST.get('almacen_kits'+str(i), False)
                            detallecompra.reparacion=request.POST.get('reparacion_kits'+str(i), False)

                            #detallecompra.updated_at = datetime.now()
                            #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                            detallecompra.save()

                            print('Tiene detalle'+str(i))
                        else:
                            comprasdetalle=ProformaDetalle()
                            comprasdetalle.proforma_id = new_orden.id
                            comprasdetalle.producto=product
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            comprasdetalle.total=request.POST["total_kits"+str(i)]
                            if 'imagen_kits'+str(i) in request.FILES:
                                comprasdetalle.imagen=request.FILES["imagen_kits"+str(i)]
                            #comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
                            comprasdetalle.observaciones=request.POST["observacion_kits"+str(i)]
                            comprasdetalle.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                            comprasdetalle.medida=request.POST["medida_kits"+str(i)]
                            comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
                            comprasdetalle.detalle=request.POST["detalle_kits"+str(i)]
                            comprasdetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            comprasdetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                            comprasdetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            comprasdetalle.save()

                            print('No Tiene detalle'+str(i))
                            print('contadorsd prueba'+str(contador))
            #ordencompra_form=OrdenCompraForm(request.POST)
            detalle = ProformaDetalle.objects.filter(proforma_id=p_id).filter(Q(no_producir=False) | Q(no_producir__isnull=True))
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
            ambientes = Ambiente.objects.all().order_by('descripcion')


            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'productos':productos,
            'ambientes':ambientes,
            'proforma':proforma,
            'mensaje':'Proforma actualizada con exito'}


            # return render_to_response(
            #     'proforma/actualizar.html',
            #     context,
            #     context_instance=RequestContext(request))
            return HttpResponseRedirect('/proforma/consultarproforma/')
        else:

            proforma_form=ProformaForm(request.POST)
            detalle = ProformaDetalle.objects.filter(proforma_id=proforma.id).filter(Q(no_producir=False) | Q(no_producir__isnull=True))
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'mensaje':'Proforma actualizada con exito'}

        return render_to_response(
            'proforma/actualizar.html',
            context,
            context_instance=RequestContext(request))




#=====================================================#
@login_required()
def ProformaEliminarView(request):
    return eliminarView(request, Proforma, 'proforma-list')

#=====================================================#
@login_required()
def ProformaEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Proforma)
#======================================================#
@login_required()
@csrf_exempt
def misProformaGuardar(request):
    item = {'exito':0}
    if request.method == 'POST':
        try:

            proformas = request.POST['data']
            proformas = json.loads(proformas)

            for proforma in proformas:
                if not proforma['codigo'] == "":
                    try:
                            a = Proforma()
                            a.created_by = request.user
                            a.updated_at = datetime.now()
                            a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar la proforma")
                        pass

                    item = {'exito':1}

            if item['exito'] == 1:
                messages.info(request, 'Proforma guardado!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito':0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')

class ProformaRenderListView(ObjectListView):
    model = Proforma
    paginate_by = 100
    template_name = 'proforma/subir_render_list.html'
    table_class = ProformaTable
    filter_class = ProformaFilter
    context_object_name = 'proformas'

    def get_context_data(self, **kwargs):
        context = super(ProformaRenderListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('proforma-delete')
        return context

@login_required()
def ProformaListAprobarView(request):
    proformas = Proforma.objects.all().order_by('id')


    return render_to_response('proforma/aprobada.html', {'proformas': proformas}, RequestContext(request))

@login_required()
def ProformaAprobarByPkView(request, pk):

    objetos = Proforma.objects.filter(id= pk)
    for obj in objetos:
        if obj.total > 0:
            obj.aprobada = True
            obj.save()

    return HttpResponseRedirect('/proforma/proformaAprobar')

@login_required()
def ProformaAnularByPkView(request, pk):

    objetos = Proforma.objects.filter(id= pk)
    for obj in objetos:
        obj.anulada = True
        obj.save()

    return HttpResponseRedirect('/proforma/proformaAprobar')

@login_required()
def CotizacionProformaListView(request):
    cotizacionproformas =  CotizacionProforma.objects.all().order_by('id')


    return render_to_response('cotizacionproforma/list.html', {'cotizacionproformas': cotizacionproformas}, RequestContext(request))


@login_required()
@transaction.atomic
def CotizacionProformaCreateView(request):
      if request.method == 'POST':
        proforma_form=CotizacionProformaForm(request.POST)
        productos = ProductoGeneral.objects.all().order_by('descripcion')
        ambientes = Ambiente.objects.all().order_by('descripcion')
        iva = Parametros.objects.get(clave='iva')


        if proforma_form.is_valid():
            try:
                with transaction.atomic():
                    new_orden=proforma_form.save()
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
                    new_orden.save()

                    try:
                        if new_orden.puntos_venta_id == 1:
                            secuencial = Secuenciales.objects.get(modulo='cotizacionproforma')
                            if new_orden.hierro_proforma:
                                secuencial = Secuenciales.objects.get(modulo='cotizacionproformahierro')
                            else:
                                secuencial = Secuenciales.objects.get(modulo='cotizacionproforma')

                        if new_orden.puntos_venta_id == 2:
                            secuencial = Secuenciales.objects.get(modulo='cotizacionproformasamborondon')
                        if new_orden.puntos_venta_id == 3:
                            secuencial = Secuenciales.objects.get(modulo='cotizacionproformaurdesa')

                        if secuencial.secuencial!=new_orden.codigo:
                            new_orden.codigo='00'+str(secuencial.secuencial)
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
                        print('entro comoqw'+str(i))
                        if int(i)> int(contador):
                            print('entrosd')
                            break
                        else:
                            if 'id_kits'+str(i) in request.POST:
                                product=ProductoGeneral.objects.get(id=request.POST["id_kits"+str(i)])
                                ambiente=Ambiente.objects.get(id=request.POST["ambientes_kits"+str(i)])

                                proformadetalle=CotizacionProformaDetalle()
                                proformadetalle.cotizacion_proforma_id = new_orden.id
                                proformadetalle.producto_general_id=request.POST["id_kits"+str(i)]
                                proformadetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                                proformadetalle.nombre=request.POST["nombre_kits"+str(i)]
                                proformadetalle.medida=request.POST["medida_kits"+str(i)]
                                proformadetalle.detalle=request.POST["detalle_kits"+str(i)]
                                proformadetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                                if 'imagen_kits' + str(i) in request.FILES:
                                    proformadetalle.imagen=request.FILES["imagen_kits"+str(i)]

                                proformadetalle.observaciones=request.POST["observacion_kits"+str(i)]

                                #kits.costo=float(request.POST["costo_kits1"])
                                proformadetalle.precio_compra=request.POST["costo_kits"+str(i)]
                                proformadetalle.total=request.POST["total_kits"+str(i)]
                                proformadetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                                proformadetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                                proformadetalle.created_by = request.user.get_full_name()
                                proformadetalle.updated_by = request.user.get_full_name()
                                proformadetalle.created_at = datetime.now()
                                proformadetalle.updated_at = datetime.now()
                                proformadetalle.save()

                        print(i)
                        print('contadorsd prueba'+str(contador))
            except IntegrityError:
                print 'error'
                print proforma_form.errors, len(proforma_form.errors)

            return HttpResponseRedirect('/proforma/cotizarproforma')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
      else:
        proforma_form=CotizacionProformaForm
        productos = ProductoGeneral.objects.all().order_by('descripcion')
        ambientes = Ambiente.objects.all().order_by('descripcion')
        iva = Parametros.objects.get(clave='iva')

      return render_to_response('cotizacionproforma/create.html', { 'form': proforma_form,'productos':productos,'ambientes':ambientes,'iva':iva},  RequestContext(request))

class CotizacionProformaUpdateView(ObjectUpdateView):
    def get(self, request, *args, **kwargs):

        proforma = CotizacionProforma.objects.get(id=kwargs['pk'])
        productos = ProductoGeneral.objects.all().order_by('descripcion')
        ambientes = Ambiente.objects.all().order_by('descripcion')

        proforma_form=CotizacionProformaForm(instance=proforma)
        detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=proforma.id).order_by('id')

        context = {
        'section_title':'Actualizar Cotizacion',
        'button_text':'Actualizar',
        'form':proforma_form,
        'productos':productos,
        'ambientes':ambientes,
        'detalle':detalle,
        'proforma':proforma
        }

        return render_to_response(
            'cotizacionproforma/actualizar.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        proforma = CotizacionProforma.objects.get(id=kwargs['pk'])
        proforma_form = CotizacionProformaForm(request.POST,request.FILES,instance=proforma)
        p_id=kwargs['pk']
        print(p_id)
        print proforma_form.is_valid(), proforma_form.errors, type(proforma_form.errors)
        productos = ProductoGeneral.objects.all().order_by('descripcion')

        if proforma_form.is_valid() :

            new_orden=proforma_form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            contador=request.POST["columnas_receta"]
            new_orden.total=request.POST["total"]
            new_orden.subtotal=request.POST["subtotal"]
            new_orden.descuento=request.POST["descuento"]
            new_orden.porcentaje_descuento=request.POST["porcentaje_descuento"]
            new_orden.iva=request.POST["iva"]
            new_orden.porcentaje_iva=request.POST["porcentaje_iva"]
            new_orden.save()

            i=0
            while int(i) <= int(contador):
                i+= 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits'+str(i) in request.POST:
                        product=ProductoGeneral.objects.get(id=request.POST["id_kits"+str(i)])

                        if 'id_detalle'+str(i) in request.POST:
                            detalle_id=request.POST["id_detalle"+str(i)]
                            detallecompra = CotizacionProformaDetalle.objects.get(id=detalle_id)
                            print('product_id:'+str(product.id))
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto_general =product
                            detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
                            detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
                            detallecompra.total=request.POST["total_kits"+str(i)]
                            detallecompra.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            if 'imagen_kits' + str(i) in request.FILES:
                                detallecompra.imagen = request.FILES["imagen_kits" + str(i)]

                            detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
                            detallecompra.medida=request.POST["medida_kits"+str(i)]
                            detallecompra.nombre=request.POST["nombre_kits"+str(i)]
                            detallecompra.detalle=request.POST["detalle_kits"+str(i)]
                            detallecompra.almacen=request.POST.get('almacen_kits'+str(i), False)
                            detallecompra.reparacion=request.POST.get('reparacion_kits'+str(i), False)

                            #detallecompra.updated_at = datetime.now()
                            #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                            detallecompra.save()

                            print('Tiene detalle'+str(i))
                        else:
                            comprasdetalle=CotizacionProformaDetalle()
                            comprasdetalle.cotizacion_proforma_id = new_orden.id
                            comprasdetalle.producto_general=product
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            comprasdetalle.total=request.POST["total_kits"+str(i)]
                            if 'imagen_kits' + str(i) in request.FILES:
                                comprasdetalle.imagen = request.FILES["imagen_kits" + str(i)]
                            #comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
                            comprasdetalle.observaciones=request.POST["observacion_kits"+str(i)]
                            comprasdetalle.medida=request.POST["medida_kits"+str(i)]
                            comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
                            comprasdetalle.detalle=request.POST["detalle_kits"+str(i)]
                            comprasdetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            comprasdetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                            comprasdetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            comprasdetalle.save()
                            print('No Tiene detalle'+str(i))
                            print('contadorsd prueba'+str(contador))
            #ordencompra_form=OrdenCompraForm(request.POST)
            detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=p_id).order_by('id')
            productos = ProductoGeneral.objects.all().order_by('descripcion')

            ambientes = Ambiente.objects.all().order_by('descripcion')


            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'productos':productos,
            'ambientes':ambientes,
            'proforma':proforma,
            'mensaje':'Proforma actualizada con exito'}


            return render_to_response(
                'cotizacionproforma/actualizar.html',
                context,
                context_instance=RequestContext(request))
        else:

            proforma_form=CotizacionProformaForm(request.POST)
            detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=proforma.id).order_by('id')
            productos = ProductoGeneral.objects.all().order_by('descripcion')


            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'mensaje':'Cotizacion de Proforma actualizada con exito'}

        return render_to_response(
            'cotizacionproforma/actualizar.html',
            context,
            context_instance=RequestContext(request))



@login_required()
def CotizacionProformaListCotizarView(request):
    cotizacionproformas =  CotizacionProforma.objects.all().order_by('id')


    return render_to_response('cotizacionproforma/cotizar_list.html', {'cotizacionproformas': cotizacionproformas}, RequestContext(request))


class CotizacionProformaUpdateCotizarView(ObjectUpdateView):

    def get(self, request, *args, **kwargs):

        proforma = CotizacionProforma.objects.get(id=kwargs['pk'])
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')
        producto_general=ProductoGeneral.objects.all().order_by('descripcion')

        proforma_form=CotizacionProformaForm(instance=proforma)
        detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=proforma.id).order_by('id')

        context = {
        'section_title':'Actualizar Cotizacion',
        'button_text':'Actualizar',
        'form':proforma_form,
        'productos':productos,
        'producto_general':producto_general,
        'ambientes':ambientes,
        'detalle':detalle,
        'proforma':proforma
        }

        return render_to_response(
            'cotizacionproforma/actualizar_cotizar.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        proforma = CotizacionProforma.objects.get(id=kwargs['pk'])
        proforma_form = CotizacionProformaForm(request.POST,request.FILES,instance=proforma)
        producto_general=ProductoGeneral.objects.all().order_by('descripcion')
        p_id=kwargs['pk']
        print(p_id)
        print proforma_form.is_valid(), proforma_form.errors, type(proforma_form.errors)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

        if proforma_form.is_valid() :

            new_orden=proforma_form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            contador=request.POST["columnas_receta"]
            new_orden.total=request.POST["total"]
            new_orden.subtotal=request.POST["subtotal"]
            new_orden.descuento=request.POST["descuento"]
            new_orden.porcentaje_descuento=request.POST["porcentaje_descuento"]
            new_orden.iva=request.POST["iva"]
            new_orden.porcentaje_iva=request.POST["porcentaje_iva"]
            new_orden.save()

            i=0
            while int(i) <= int(contador):
                i+= 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits'+str(i) in request.POST:
                        product=ProductoGeneral.objects.get(id=request.POST["id_kits"+str(i)])
                        detalle_id=request.POST["id_detalle"+str(i)]
                        print('detalle_id:'+str(detalle_id))
                        if detalle_id:
                            detallecompra = CotizacionProformaDetalle.objects.get(id=detalle_id)
                            print('product_id:'+str(product.id))
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto_general =product
                            if 'id_kits_referenciado'+str(i) in request.POST:
                                detallecompra.producto_creado_id=request.POST["id_kits_referenciado"+str(i)]
                                detallecompra.nombre_producto_creado=request.POST["nombre_referenciado_kits"+str(i)]

                            detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
                            detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
                            detallecompra.total=request.POST["total_kits"+str(i)]
                            detallecompra.ambiente_id=request.POST["ambientes_kits"+str(i)]

                            #detallecompra.imagen=request.POST["imagen_kits"+str(i)]
                            detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
                            detallecompra.medida=request.POST["medida_kits"+str(i)]
                            detallecompra.nombre=request.POST["nombre_kits"+str(i)]
                            detallecompra.detalle=request.POST["detalle_kits"+str(i)]
                            detallecompra.almacen=request.POST.get('almacen_kits'+str(i), False)
                            detallecompra.reparacion=request.POST.get('reparacion_kits'+str(i), False)

                            #detallecompra.updated_at = datetime.now()
                            #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                            detallecompra.save()

                            print('Tiene detalle'+str(i))
                        else:
                            comprasdetalle=CotizacionProformaDetalle()
                            comprasdetalle.cotizacion_proforma_id = new_orden.id
                            comprasdetalle.producto_general=product
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            comprasdetalle.total=request.POST["total_kits"+str(i)]
                            #comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
                            comprasdetalle.observaciones=request.POST["observacion_kits"+str(i)]
                            comprasdetalle.medida=request.POST["medida_kits"+str(i)]
                            comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
                            comprasdetalle.detalle=request.POST["detalle_kits"+str(i)]
                            comprasdetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            comprasdetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                            comprasdetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            comprasdetalle.save()
                            i+= 1
                            print('No Tiene detalle'+str(i))
                            print('contadorsd prueba'+str(contador))
            #ordencompra_form=OrdenCompraForm(request.POST)
            detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=p_id).order_by('id')
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
            ambientes = Ambiente.objects.all().order_by('descripcion')
            producto_general=ProductoGeneral.objects.all().order_by('descripcion')


            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'productos':productos,
            'producto_general':producto_general,
            'ambientes':ambientes,
            'proforma':proforma,
            'mensaje':'Cotizacion de Proforma costeada con exito'}


            return render_to_response(
                'cotizacionproforma/actualizar_cotizar.html',
                context,
                context_instance=RequestContext(request))
        else:

            proforma_form=CotizacionProformaForm(request.POST)
            detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=proforma.id).order_by('id')
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
            producto_general=ProductoGeneral.objects.all().order_by('descripcion')

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'productos':productos,
            'producto_general':producto_general,
            'mensaje':'Cotizacion de Proforma actualizada con exito'}

        return render_to_response(
            'cotizacionproforma/actualizar_cotizar.html',
            context,
            context_instance=RequestContext(request))

class CotizacionProformaRenderListView(ObjectListView):
    model = CotizacionProforma
    paginate_by = 100
    template_name = 'cotizacionproforma/subir_render_list.html'
    table_class = CotizacionProformaTable
    filter_class = CotizacionProformaFilter
    context_object_name = 'cotizacionproformas'

    def get_context_data(self, **kwargs):
        context = super(CotizacionProformaRenderListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('proforma-delete')
        return context

def SubirImagenesView(request, pk):
    if request.method == 'POST':
        proforma_form=ImagenesCotizacionProformaForm(request.POST)


        if proforma_form.is_valid():
            if 'imagen' in request.FILES:
                new_orden=proforma_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.cotizacion_proforma_detalle_id = pk

                new_orden.imagen=request.FILES["imagen"]

                new_orden.save()
            proforma_form=ImagenesCotizacionProformaForm
            detalle = ImagenesCotizacionProforma.objects.filter(cotizacion_proforma_detalle_id=pk)
            detailprof = CotizacionProformaDetalle.objects.get(id=pk)
            prof = CotizacionProforma.objects.get(id=detailprof.cotizacion_proforma_id)


            return render_to_response('cotizacionproforma/subir_imagenes.html', { 'form': proforma_form,'detalle':detalle,'detailprof':detailprof,'prof':prof},  RequestContext(request))

        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
    else:
        proforma_form=ImagenesCotizacionProformaForm
        detalle = ImagenesCotizacionProforma.objects.filter(cotizacion_proforma_detalle_id=pk)
        detailprof = CotizacionProformaDetalle.objects.get(id=pk)
        prof = CotizacionProforma.objects.get(id=detailprof.cotizacion_proforma_id)


        return render_to_response('cotizacionproforma/subir_imagenes.html', { 'form': proforma_form,'detalle':detalle,'detailprof':detailprof,'prof':prof},  RequestContext(request))

class CotizacionProformaVerView(ObjectUpdateView):
    def get(self, request, *args, **kwargs):

        proforma = CotizacionProforma.objects.get(id=kwargs['pk'])
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')

        proforma_form=CotizacionProformaForm(instance=proforma)
        detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=proforma.id).order_by('id')

        context = {
        'section_title':'Actualizar Cotizacion',
        'button_text':'Actualizar',
        'form':proforma_form,
        'productos':productos,
        'ambientes':ambientes,
        'detalle':detalle,
        'proforma':proforma
        }

        return render_to_response(
            'cotizacionproforma/ver.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        proforma = CotizacionProforma.objects.get(id=kwargs['pk'])
        proforma_form = CotizacionProformaForm(request.POST,request.FILES,instance=proforma)
        p_id=kwargs['pk']
        print(p_id)
        print proforma_form.is_valid(), proforma_form.errors, type(proforma_form.errors)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

        if proforma_form.is_valid() :

            new_orden=proforma_form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            contador=request.POST["columnas_receta"]
            new_orden.total=request.POST["total"]
            new_orden.subtotal=request.POST["subtotal"]
            new_orden.descuento=request.POST["descuento"]
            new_orden.porcentaje_descuento=request.POST["porcentaje_descuento"]
            new_orden.iva=request.POST["iva"]
            new_orden.save()

            i=0
            while int(i) <= int(contador):
                i+= 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits'+str(i) in request.POST:
                        product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                        detalle_id=request.POST["id_detalle"+str(i)]
                        print('detalle_id:'+str(detalle_id))
                        if detalle_id:
                            detallecompra = CotizacionProformaDetalle.objects.get(id=detalle_id)
                            print('product_id:'+str(product.producto_id))
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto =product
                            if 'id_kits_referenciado'+str(i) in request.POST:
                                detallecompra.producto_creado_id=request.POST["id_kits_referenciado"+str(i)]
                                detallecompra.nombre_producto_creado=request.POST["nombre_referenciado_kits"+str(i)]

                            detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
                            detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
                            detallecompra.total=request.POST["total_kits"+str(i)]
                            detallecompra.ambiente_id=request.POST["ambientes_kits"+str(i)]

                            #detallecompra.imagen=request.POST["imagen_kits"+str(i)]
                            detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
                            detallecompra.medida=request.POST["medida_kits"+str(i)]
                            detallecompra.nombre=request.POST["nombre_kits"+str(i)]
                            detallecompra.detalle=request.POST["detalle_kits"+str(i)]
                            detallecompra.almacen=request.POST.get('almacen_kits'+str(i), False)
                            detallecompra.reparacion=request.POST.get('reparacion_kits'+str(i), False)

                            #detallecompra.updated_at = datetime.now()
                            #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                            detallecompra.save()

                            print('Tiene detalle'+str(i))
                        else:
                            comprasdetalle=CotizacionProformaDetalle()
                            comprasdetalle.cotizacion_proforma_id = new_orden.id
                            comprasdetalle.producto=product
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            comprasdetalle.total=request.POST["total_kits"+str(i)]
                            #comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
                            comprasdetalle.observaciones=request.POST["observacion_kits"+str(i)]
                            comprasdetalle.medida=request.POST["medida_kits"+str(i)]
                            comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
                            comprasdetalle.detalle=request.POST["detalle_kits"+str(i)]
                            comprasdetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            comprasdetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                            comprasdetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            comprasdetalle.save()
                            i+= 1
                            print('No Tiene detalle'+str(i))
                            print('contadorsd prueba'+str(contador))
            #ordencompra_form=OrdenCompraForm(request.POST)
            detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=p_id).order_by('id')
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
            ambientes = Ambiente.objects.all().order_by('descripcion')


            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'productos':productos,
            'ambientes':ambientes,
            'proforma':proforma,
            'mensaje':'Proforma actualizada con exito'}


            return render_to_response(
                'cotizacionproforma/ver.html',
                context,
                context_instance=RequestContext(request))
        else:

            proforma_form=CotizacionProformaForm(request.POST)
            detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=proforma.id).order_by('id')
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'mensaje':'Cotizacion de Proforma actualizada con exito'}

        return render_to_response(
            'cotizacionproforma/ver.html',
            context,
            context_instance=RequestContext(request))

@login_required()
def SubirImagenesVerView(request, pk):
    if request.method == 'POST':
        proforma_form=ImagenesCotizacionProformaForm(request.POST)


        if proforma_form.is_valid():
            new_orden=proforma_form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.cotizacion_proforma_detalle_id = pk
            new_orden.imagen=request.FILES["imagen"]

            new_orden.save()
            proforma_form=ImagenesCotizacionProformaForm
            detalle = ImagenesCotizacionProforma.objects.filter(cotizacion_proforma_detalle_id=pk).order_by('id')
            detailprof = CotizacionProformaDetalle.objects.get(id=pk)
            prof = CotizacionProforma.objects.get(id=detailprof.cotizacion_proforma_id)


            return render_to_response('cotizacionproforma/subir_imagenes_ver.html', { 'form': proforma_form,'detalle':detalle,'detailprof':detailprof,'prof':prof},  RequestContext(request))

        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
    else:
        proforma_form=ImagenesCotizacionProformaForm
        detalle = ImagenesCotizacionProforma.objects.filter(cotizacion_proforma_detalle_id=pk)
        detailprof = CotizacionProformaDetalle.objects.get(id=pk)
        prof = CotizacionProforma.objects.get(id=detailprof.cotizacion_proforma_id)


        return render_to_response('cotizacionproforma/subir_imagenes_ver.html', { 'form': proforma_form,'detalle':detalle,'detailprof':detailprof,'prof':prof},  RequestContext(request))

@login_required()
@transaction.atomic
def CotizacionProformaCreateProformaView(request, pk):

      if request.method == 'POST':
        proforma_form=ProformaForm(request.POST)
        ambientes = Ambiente.objects.all().order_by('descripcion')
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        cotizacion = CotizacionProforma.objects.get(id=pk)
        detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=pk).order_by('id')

        if proforma_form.is_valid():
            try:
                with transaction.atomic():
                    new_orden=proforma_form.save()
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
                    new_orden.save()
                    try:
                        if new_orden.puntos_venta_id == 1:
                            if new_orden.hierro_proforma:
                                secuencial = Secuenciales.objects.get(modulo='proformafabricahierro')
                            else:
                                secuencial = Secuenciales.objects.get(modulo='proforma')

                        if new_orden.puntos_venta_id == 2:
                            secuencial = Secuenciales.objects.get(modulo='proformasamborondon')
                        if new_orden.puntos_venta_id == 3:
                            secuencial = Secuenciales.objects.get(modulo='proformaurdesa')

                        if secuencial.secuencial != new_orden.codigo:
                            new_orden.codigo = '00' + str(secuencial.secuencial)
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
                        print('entro comoqw'+str(i))
                        if int(i)> int(contador):
                            print('entrosd')
                            break
                        else:
                            if 'id_kits'+str(i) in request.POST:
                                product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                                ambiente=Ambiente.objects.get(id=request.POST["ambientes_kits"+str(i)])

                                proformadetalle=ProformaDetalle()
                                proformadetalle.proforma_id = new_orden.id
                                proformadetalle.producto_id=request.POST["id_kits"+str(i)]
                                proformadetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                                proformadetalle.nombre=request.POST["nombre_kits"+str(i)]
                                proformadetalle.medida=request.POST["medida_kits"+str(i)]
                                proformadetalle.detalle=request.POST["detalle_kits"+str(i)]
                                proformadetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                                proformadetalle.imagen=product.imagen

                                # if (len(request.POST["imagen_kits"+str(i)]))!=0:
                                #     print('prueba'+str(contador))

                                #     proformadetalle.imagen=request.FILES["imagen_kits"+str(i)]

                                proformadetalle.observaciones=request.POST["observacion_kits"+str(i)]

                                #kits.costo=float(request.POST["costo_kits1"])
                                proformadetalle.precio_compra=request.POST["costo_kits"+str(i)]
                                proformadetalle.total=request.POST["total_kits"+str(i)]
                                proformadetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                                proformadetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                                proformadetalle.save()

                        print(i)
                        print('contadorsd prueba'+str(contador))


            except IntegrityError:
                print 'error'
                print proforma_form.errors, len(proforma_form.errors)
            return HttpResponseRedirect('/proforma/consultarproforma')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
      else:
        proforma_form=ProformaForm
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        cotizacion = CotizacionProforma.objects.get(id=pk)
        detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=pk).order_by('id')
        ambientes = Ambiente.objects.all().order_by('descripcion')

        print('contadorsd prueba'+str(cotizacion.reunion_codigo))
      return render_to_response('proforma/cotizacionproformacrearproforma.html', { 'form': proforma_form,'productos':productos,'ambientes':ambientes,'cotizacion':cotizacion,'detalle':detalle},  RequestContext(request))

def index(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    proforma=Proforma.objects.get(id=pk)
    subt=proforma.subtotal+proforma.descuento
    cursor = connection.cursor();
    cursor.execute("select distinct pd.ambiente_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.total,pd.detalle,pd.id,pd.proforma_id, pd.imagen from proforma p,proforma_detalle pd where p.id=pd.proforma_id and (pd.no_producir is NULL or pd.no_producir=False) and p.id="+pk+" ORDER BY pd.id ASC ");
    row = cursor.fetchall();

    anio = Parametros.objects.get(clave='anio_vigente')
    anio_vigente=anio.valor

    cursor = connection.cursor();
    sql="select distinct pd.ambiente_id,am.descripcion,pd.id from proforma p, proforma_detalle pd,ambiente am where p.id=pd.proforma_id and pd.ambiente_id=am.id and (pd.no_producir is NULL or pd.no_producir=False) and p.id="+pk+" order by pd.id"
    cursor.execute(sql);
    row1 = cursor.fetchall();
    ambientes = []
    x=0

    for r in row1:
        print('Consulta'+str(r[0]))
        print('Arreglo longitud' + str(len(ambientes)))
        if len(ambientes)>0:
            cont=0
            print('Contador inicial' + str(cont))
            for a in ambientes:
                print('AMBIENTE' + str(a[0])+'sql'+ str(r[0]))

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





    html = render_to_string('proforma/imprimir.html', {'pagesize':'A4','proforma':proforma,'subt':subt,'row':row,'anio':anio_vigente,'ambiente':ambientes,'media_root':settings.MEDIA_ROOT}, context_instance=RequestContext(request))
    return generar_pdf(html)

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
def HistoricoListView(request):
    proformas =  Proforma.objects.all().order_by('id')


    return render_to_response('proforma/historico.html', {'proformas': proformas}, RequestContext(request))


class ProformaHistoricoUpdateView(ObjectUpdateView):
    def get(self, request, *args, **kwargs):

        proforma = Proforma.objects.get(id=kwargs['pk'])
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')

        proforma_form=ProformaForm(instance=proforma)
        detalle = ProformaDetalle.objects.filter(proforma_id=proforma.id)

        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'form':proforma_form,
        'productos':productos,
        'ambientes':ambientes,
        'detalle':detalle,
        'proforma':proforma
        }

        return render_to_response(
            'proforma/actualizar_historico.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        proforma = Proforma.objects.get(id=kwargs['pk'])
        proforma_form = ProformaForm(request.POST,request.FILES,instance=proforma)
        p_id=kwargs['pk']
        print(p_id)
        print proforma_form.is_valid(), proforma_form.errors, type(proforma_form.errors)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

        if proforma_form.is_valid() :

            new_orden=proforma_form.save()
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
                        detalle_id=request.POST["id_detalle"+str(i)]
                        print('detalle_id:'+str(detalle_id))
                        if detalle_id:
                            detallecompra = ProformaDetalle.objects.get(id=detalle_id)
                            print('product_id:'+str(product.producto_id))
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto =product
                            detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
                            detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
                            detallecompra.total=request.POST["total_kits"+str(i)]
                            detallecompra.ambiente_id=request.POST["ambientes_kits"+str(i)]

                            #detallecompra.imagen=request.POST["imagen_kits"+str(i)]
                            detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
                            detallecompra.medida=request.POST["medida_kits"+str(i)]
                            detallecompra.nombre=request.POST["nombre_kits"+str(i)]
                            detallecompra.detalle=request.POST["detalle_kits"+str(i)]
                            detallecompra.almacen=request.POST.get('almacen_kits'+str(i), False)
                            detallecompra.reparacion=request.POST.get('reparacion_kits'+str(i), False)

                            #detallecompra.updated_at = datetime.now()
                            #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                            detallecompra.save()

                            print('Tiene detalle'+str(i))
                        else:
                            comprasdetalle=ProformaDetalle()
                            comprasdetalle.proforma_id = new_orden.id
                            comprasdetalle.producto=product
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            comprasdetalle.total=request.POST["total_kits"+str(i)]
                            #comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
                            comprasdetalle.observaciones=request.POST["observacion_kits"+str(i)]
                            comprasdetalle.medida=request.POST["medida_kits"+str(i)]
                            comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
                            comprasdetalle.detalle=request.POST["detalle_kits"+str(i)]
                            comprasdetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            comprasdetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                            comprasdetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            comprasdetalle.save()
                            i+= 1
                            print('No Tiene detalle'+str(i))
                            print('contadorsd prueba'+str(contador))
            #ordencompra_form=OrdenCompraForm(request.POST)
            detalle = ProformaDetalle.objects.filter(proforma_id=p_id)
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
            ambientes = Ambiente.objects.all().order_by('descripcion')


            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'productos':productos,
            'ambientes':ambientes,
            'proforma':proforma,
            'mensaje':'Proforma actualizada con exito'}


            return render_to_response(
                'proforma/actualizar_historico.html',
                context,
                context_instance=RequestContext(request))
        else:

            proforma_form=ProformaForm(request.POST)
            detalle = ProformaDetalle.objects.filter(proforma_id=proforma.id)
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'mensaje':'Proforma actualizada con exito'}

        return render_to_response(
            'proforma/actualizar_historico.html',
            context,
            context_instance=RequestContext(request))


@csrf_exempt
def obtenerAbreviatura(request):
    if request.method == 'POST':
        codigo = request.POST.get('id')

        objetos = PuntosVenta.objects.get(id = codigo)
        if codigo=='1':
            secuencial = Secuenciales.objects.get(modulo ="proforma")
        if codigo=='2':
            secuencial = Secuenciales.objects.get(modulo ="proformasamborondon")
        if codigo=='3':
            secuencial = Secuenciales.objects.get(modulo ="proformaurdesa")

        modulo_secuencial = secuencial.secuencial

        item = {
            'abreviatura_codigo': objetos.codigo_proforma,
            'codigo': modulo_secuencial,


        }
    return HttpResponse(json.dumps(item), content_type='application/json')

def imprimirCotizacion(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    proforma=CotizacionProforma.objects.get(id=pk)
    cursor = connection.cursor();
    cursor.execute("select distinct pd.ambiente_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.total,pd.detalle,pd.id,pd.cotizacion_proforma_id,pd.imagen from cotizacion_proforma p,cotizacion_proforma_detalle pd where p.id=pd.cotizacion_proforma_id and p.id="+pk+" ORDER BY pd.id ASC ");
    row = cursor.fetchall();

    cursor = connection.cursor()
    cursor.execute("select distinct pd.ambiente_id,am.descripcion,am.orden,pd.id from cotizacion_proforma p, cotizacion_proforma_detalle pd,ambiente am where p.id=pd.cotizacion_proforma_id and pd.ambiente_id=am.id and p.id="+pk+" order by pd.id")
    row1 = cursor.fetchall()
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
        else:
            print('Entro 1 vez')
            ambientes.append(r)
            x = x + 1

    anio = Parametros.objects.get(clave='anio_vigente')
    anio_vigente = anio.valor

    html = render_to_string('cotizacionproforma/imprimir.html', {'pagesize':'A4','proforma':proforma,'anio':anio_vigente,'row':row,'ambiente':ambientes,'media_root':settings.MEDIA_ROOT}, context_instance=RequestContext(request))
    return generar_pdf(html)

    #         'ordenproduccion':ordenproduccion,
    #         }

    # return render_to_response(
    #         'ordenproduccion/imprimir.html',
    #         context,
    #         context_instance=RequestContext(request))

@csrf_exempt
def obtenerAbreviaturaCotizacion(request):
    if request.method == 'POST':
        codigo = request.POST.get('id')

        objetos = PuntosVenta.objects.get(id = codigo)
        if codigo=='1':
            secuencial = Secuenciales.objects.get(modulo ="cotizacionproforma")
        if codigo=='2':
            secuencial = Secuenciales.objects.get(modulo ="cotizacionproformasamborondon")
        if codigo=='3':
            secuencial = Secuenciales.objects.get(modulo ="cotizacionproformaurdesa")

        modulo_secuencial = secuencial.secuencial

        item = {
            'abreviatura_codigo': objetos.codigo_proforma,
            'codigo': modulo_secuencial,


        }
    return HttpResponse(json.dumps(item), content_type='application/json')

def MostrarImagenView(request):
    if request.method == 'POST':
        id=request.POST["id"]

        proforma_form=ImagenesCotizacionProformaForm
        detalle = ImagenesCotizacionProforma.objects.filter(cotizacion_proforma_detalle_id=id).order_by('id')
        detailprof = CotizacionProformaDetalle.objects.get(id=id)
        prof = CotizacionProforma.objects.get(id=detailprof.cotizacion_proforma_id)
        return render_to_response('cotizacionproforma/mostrar_imagen.html', { 'form': proforma_form,'detalle':detalle,'detailprof':detailprof,'prof':prof},  RequestContext(request))



    else:
        id=request.POST["id"]

        proforma_form=ImagenesCotizacionProformaForm
        detalle = ImagenesCotizacionProforma.objects.filter(cotizacion_proforma_detalle_id=id).order_by('id')
        detailprof = CotizacionProformaDetalle.objects.get(id=id)
        prof = CotizacionProforma.objects.get(id=detailprof.cotizacion_proforma_id)
        return render_to_response('cotizacionproforma/mostrar_imagen.html', { 'form': proforma_form,'detalle':detalle,'detailprof':detailprof,'prof':prof},  RequestContext(request))

@login_required()
def ImagenEliminarView(request):
    pk=request.POST["id"]
    objetos = ImagenesCotizacionProforma.objects.get(id=pk)

    id=objetos.cotizacion_proforma_detalle_id
    objetos.delete()


    proforma_form=ImagenesCotizacionProformaForm
    detalle = ImagenesCotizacionProforma.objects.filter(cotizacion_proforma_detalle_id=id)
    detailprof = CotizacionProformaDetalle.objects.get(id=id)
    prof = CotizacionProforma.objects.get(id=detailprof.cotizacion_proforma_id)
    return render_to_response('cotizacionproforma/subir_imagenes.html', { 'form': proforma_form,'detalle':detalle,'detailprof':detailprof,'prof':prof},  RequestContext(request))


@login_required()
def ProformaFacturaCreateView(request):
      if request.method == 'POST':
        proforma_form=ProformaFacturaForm(request.POST)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')


        if proforma_form.is_valid():
            new_orden=proforma_form.save()
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
                secuencial = Secuenciales.objects.get(modulo='proformafactura')
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
                print('entro comoqw'+str(i))
                if int(i)> int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits'+str(i) in request.POST:
                        product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                        ambiente=Ambiente.objects.get(id=request.POST["ambientes_kits"+str(i)])

                        proformadetalle=ProformaDetalleFactura()
                        proformadetalle.proforma_factura_id = new_orden.id
                        proformadetalle.producto_id=request.POST["id_kits"+str(i)]
                        proformadetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                        proformadetalle.nombre=request.POST["nombre_kits"+str(i)]
                        proformadetalle.medida=request.POST["medida_kits"+str(i)]
                        proformadetalle.detalle=request.POST["detalle_kits"+str(i)]
                        proformadetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]

                        # if (len(request.POST["imagen_kits"+str(i)]))!=0:
                        #     print('prueba'+str(contador))

                        #     proformadetalle.imagen=request.FILES["imagen_kits"+str(i)]

                        proformadetalle.observaciones=request.POST["observacion_kits"+str(i)]

                        #kits.costo=float(request.POST["costo_kits1"])
                        proformadetalle.precio_compra=request.POST["costo_kits"+str(i)]
                        proformadetalle.total=request.POST["total_kits"+str(i)]
                        proformadetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                        proformadetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                        proformadetalle.save()

                print(i)
                print('contadorsd prueba'+str(contador))

            return HttpResponseRedirect('/proforma/proformafactura')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
      else:
        proforma_form=ProformaFacturaForm
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')
        iva = Parametros.objects.get(clave='iva')
        proformas = Proforma.objects.filter(aprobada=True)



      return render_to_response('proforma_factura/create.html', { 'form': proforma_form,'productos':productos,'ambientes':ambientes,'iva':iva,'proformas':proformas,},  RequestContext(request))

@login_required()
def ProformaFacturaCrearProformaView(request,pk):
    if request.method == 'POST':
        pedido_form=ProformaFacturaForm(request.POST)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        proformas = Proforma.objects.filter(aprobada=True)
        ambientes = Ambiente.objects.all().order_by('descripcion')

        if pedido_form.is_valid():
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
                secuencial = Secuenciales.objects.get(modulo='proformafactura')
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
                        pedidodetalle=ProformaDetalleFactura()
                        pedidodetalle.proforma_factura_id = new_orden.id
                        pedidodetalle.producto_id=request.POST["id_kits"+str(i)]
                        pedidodetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                        pedidodetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                        pedidodetalle.nombre=request.POST["nombre_kits"+str(i)]
                        pedidodetalle.medida=request.POST["medida_kits"+str(i)]
                        pedidodetalle.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                        pedidodetalle.imagen=request.POST["imagen_kits"+str(i)]
                        pedidodetalle.observaciones=request.POST["observacion_kits"+str(i)]
                        pedidodetalle.detalle=request.POST["detalle_kits"+str(i)]
                        pedidodetalle.precio_compra=request.POST["costo_kits"+str(i)]
                        pedidodetalle.total=request.POST["total_kits"+str(i)]
                        pedidodetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                        pedidodetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                        pedidodetalle.save()
                        print('se guardo'+str(contador))


                print(i)
                print('contadorsd prueba'+str(contador))

            return HttpResponseRedirect('/proforma/proformafactura')
        else:
            print 'error'
            print pedido_form.errors, len(pedido_form.errors)
    else:
        pedido_form=ProformaFacturaForm
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        proformas_aprobada = Proforma.objects.get(id = pk)
        detalle_proforma = ProformaDetalle.objects.filter(proforma_id = pk)
        proformas = Proforma.objects.filter(aprobada=True)
        ambientes = Ambiente.objects.all().order_by('descripcion')
        return render_to_response('proforma_factura/proforma_create.html', { 'form': pedido_form,'productos':productos,'proformas':proformas,'detalle_proforma':detalle_proforma,'proformas_aprobada':proformas_aprobada,'ambientes':ambientes},  RequestContext(request))

@login_required()
def ProformaFacturaListView(request):
    if request.method == 'POST':
        proforma = ProformaFactura.objects.all()
        return render_to_response('proforma_factura/index.html', {'proforma':proforma},  RequestContext(request))
    else:
        proforma = ProformaFactura.objects.all()
        return render_to_response('proforma_factura/index.html', {'proforma':proforma},  RequestContext(request))

class ProformaFacturaUpdateView(ObjectUpdateView):
    def get(self, request, *args, **kwargs):

        proforma = ProformaFactura.objects.get(id=kwargs['pk'])
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
        ambientes = Ambiente.objects.all().order_by('descripcion')

        proforma_form=ProformaFacturaForm(instance=proforma)
        detalle = ProformaDetalleFactura.objects.filter(proforma_factura_id=proforma.id)

        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'form':proforma_form,
        'productos':productos,
        'ambientes':ambientes,
        'detalle':detalle,
        'proforma':proforma
        }

        return render_to_response(
            'proforma_factura/actualizar.html', context,context_instance=RequestContext(request))

    @login_required()
    def post(sel, request, *args, **kwargs):
        proforma = ProformaFactura.objects.get(id=kwargs['pk'])
        proforma_form = ProformaFacturaForm(request.POST,request.FILES,instance=proforma)
        p_id=kwargs['pk']
        print(p_id)
        print proforma_form.is_valid(), proforma_form.errors, type(proforma_form.errors)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

        if proforma_form.is_valid() :

            new_orden=proforma_form.save()
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
                            detallecompra = ProformaDetalleFactura.objects.get(id=detalle_id)
                            print('product_id:'+str(product.producto_id))
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto =product
                            detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
                            detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
                            detallecompra.total=request.POST["total_kits"+str(i)]
                            detallecompra.ambiente_id=request.POST["ambientes_kits"+str(i)]


                            #detallecompra.imagen=request.POST["imagen_kits"+str(i)]
                            detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
                            detallecompra.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                            detallecompra.medida=request.POST["medida_kits"+str(i)]
                            detallecompra.nombre=request.POST["nombre_kits"+str(i)]
                            detallecompra.detalle=request.POST["detalle_kits"+str(i)]
                            detallecompra.almacen=request.POST.get('almacen_kits'+str(i), False)
                            detallecompra.reparacion=request.POST.get('reparacion_kits'+str(i), False)

                            #detallecompra.updated_at = datetime.now()
                            #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                            detallecompra.save()

                            print('Tiene detalle'+str(i))
                        else:
                            comprasdetalle=ProformaDetalleFactura()
                            comprasdetalle.proforma_factura_id = new_orden.id
                            comprasdetalle.producto=product
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            comprasdetalle.total=request.POST["total_kits"+str(i)]
                            if 'imagen_kits'+str(i) in request.FILES:
                                comprasdetalle.imagen=request.FILES["imagen_kits"+str(i)]
                            #comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
                            comprasdetalle.observaciones=request.POST["observacion_kits"+str(i)]
                            comprasdetalle.codigo_produccion=request.POST["codigo_produccion_kits"+str(i)]
                            comprasdetalle.medida=request.POST["medida_kits"+str(i)]
                            comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
                            comprasdetalle.detalle=request.POST["detalle_kits"+str(i)]
                            comprasdetalle.ambiente_id=request.POST["ambientes_kits"+str(i)]
                            comprasdetalle.almacen=request.POST.get('almacen_kits'+str(i), False)
                            comprasdetalle.reparacion=request.POST.get('reparacion_kits'+str(i), False)
                            comprasdetalle.save()
                            i+= 1
                            print('No Tiene detalle'+str(i))
                            print('contadorsd prueba'+str(contador))
            #ordencompra_form=OrdenCompraForm(request.POST)
            detalle = ProformaDetalleFactura.objects.filter(proforma_factura_id=p_id)
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)
            ambientes = Ambiente.objects.all().order_by('descripcion')


            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'productos':productos,
            'ambientes':ambientes,
            'proforma':proforma,
            'mensaje':'Proforma actualizada con exito'}


            return render_to_response(
                'proforma_factura/actualizar.html',
                context,
                context_instance=RequestContext(request))
        else:

            proforma_form=ProformaFacturaForm(request.POST)
            detalle = ProformaDetalleFactura.objects.filter(proforma_factura_id=proforma.id)
            productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo','precio1','precio2').exclude(tipo_producto=1)

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'mensaje':'Proforma actualizada con exito'}

        return render_to_response(
            'proforma_factura/actualizar.html',
            context,
            context_instance=RequestContext(request))

@login_required()
def ProformaFacturaListAprobarView(request):
    if request.method == 'POST':
        proforma = ProformaFactura.objects.all()
        return render_to_response('proforma_factura/aprobada.html', {'proforma':proforma},  RequestContext(request))
    else:
        proforma = ProformaFactura.objects.all()
        return render_to_response('proforma_factura/aprobada.html', {'proforma':proforma},  RequestContext(request))


@login_required()
def ProformaFacturaAprobarByPkView(request, pk):

    objetos = ProformaFactura.objects.filter(id= pk)
    for obj in objetos:
        obj.aprobada = True
        obj.save()

    return HttpResponseRedirect('/proforma/proformaFacturaAprobar')

@login_required()
def ProformaFacturaAnularByPkView(request, pk):

    objetos = ProformaFactura.objects.filter(id= pk)
    for obj in objetos:
        obj.anulada = True
        obj.save()

    return HttpResponseRedirect('/proforma/proformaFacturaAprobar')


@csrf_exempt
def obtenerDetalleProformaFactura(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')


        detalle = ProformaDetalleFactura.objects.filter(proforma_factura_id=modulo)
        html=''
        for detal in detalle:
            product=Producto.objects.get(producto_id=detal.producto_id)
            detail=(detal.nombre).encode('ascii', 'ignore').decode('ascii')


            html+='<tr><td>'+str(product.codigo_producto)+'</td>'
            html+='<td>'+str(detail)+'</td>'
            html+='<td>'+str(detal.cantidad)+'</td>'
            html+='<td>'+str(detal.precio_compra)+'</td>'
            html+='<td>'+str(detal.total)+'</td>'




        return HttpResponse(
                html
            )
    else:
        raise Http404


@csrf_exempt
def obtenerProformaFacturaFacturacion(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')

        objetos = Proforma.objects.get(codigo = codigo)

        modulo_secuencial = objetos.cliente_id

        detalle = ProformaDetalle.objects.filter(proforma_id = objetos.id)
        ids_detalle=""
        for detl in detalle:
            ids=detl.id
            ids_detalle+=str(ids)+','



        item = {
            'cliente': objetos.cliente_id,
            'vendedor': objetos.vendedor_id,
            'tipo_lugar': objetos.tipo_lugar_id,
            'puntos_venta': objetos.puntos_venta_id,
            'abreviatura_codigo': objetos.abreviatura_codigo,
            'fechapedido': str(objetos.fechapedido),
            'fecha': str(objetos.fecha),
            'descripcion': objetos.descripcion,
            'fuera_ciudad': objetos.fuera_ciudad,
            'tiempo_respuesta': objetos.tiempo_respuesta,
            'observacion': objetos.observacion,
            'ambiente': objetos.ambiente_id,
            'total': objetos.total,
            'subtotal': objetos.subtotal,
            'iva': objetos.iva,
            'porcentaje_descuento': objetos.porcentaje_descuento,
            'descuento': objetos.descuento,
            'id': objetos.id,
            'detalle':ids_detalle,
            'direccion': objetos.direccion_entrega,
            'forma_pago': objetos.forma_pago_id,
            'ruc': objetos.cliente.ruc,
            'puntos_venta': objetos.puntos_venta_id,
            'porcentaje_iva': objetos.porcentaje_iva,
        }
    return HttpResponse(json.dumps(item), content_type='application/json')

@login_required()
@transaction.atomic
def CopiarProformaView(request, pk):
    if request.method == 'POST':
        proforma_form = ProformaForm(request.POST)
        ambientes = Ambiente.objects.all().order_by('descripcion')
        productos = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto',
                                            'bloquea', 'medida_peso', 'costo', 'precio1', 'precio2').exclude(tipo_producto=1)
        cotizacion = Proforma.objects.get(id=pk)
        detalle = ProformaDetalle.objects.filter(proforma_id=pk)

        if proforma_form.is_valid():
            with transaction.atomic():
                new_orden = proforma_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.total = request.POST["total"]
                new_orden.subtotal = request.POST["subtotal"]
                new_orden.descuento = request.POST["descuento"]
                new_orden.porcentaje_descuento = request.POST["porcentaje_descuento"]
                new_orden.iva = request.POST["iva"]
                new_orden.porcentaje_iva = request.POST["porcentaje_iva"]
                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='proforma')
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
                    print('entro comoqw' + str(i))
                    if int(i) > int(contador):
                        print('entrosd')
                        break
                    else:
                        if 'id_kits' + str(i) in request.POST:
                            product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
                            ambiente = Ambiente.objects.get(id=request.POST["ambientes_kits" + str(i)])

                            proformadetalle = ProformaDetalle()
                            proformadetalle.proforma_id = new_orden.id
                            proformadetalle.producto_id = request.POST["id_kits" + str(i)]
                            proformadetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                            proformadetalle.nombre = request.POST["nombre_kits" + str(i)]
                            proformadetalle.medida = request.POST["medida_kits" + str(i)]
                            proformadetalle.detalle = request.POST["detalle_kits" + str(i)]
                            proformadetalle.ambiente_id = request.POST["ambientes_kits" + str(i)]

                            # if (len(request.POST["imagen_kits"+str(i)]))!=0:
                            #     print('prueba'+str(contador))

                            #     proformadetalle.imagen=request.FILES["imagen_kits"+str(i)]

                            proformadetalle.observaciones = request.POST["observacion_kits" + str(i)]

                            # kits.costo=float(request.POST["costo_kits1"])
                            proformadetalle.precio_compra = request.POST["costo_kits" + str(i)]
                            proformadetalle.total = request.POST["total_kits" + str(i)]
                            proformadetalle.almacen = request.POST.get('almacen_kits' + str(i), False)
                            proformadetalle.reparacion = request.POST.get('reparacion_kits' + str(i), False)
                            proformadetalle.save()

                    print(i)
                    print('contadorsd prueba' + str(contador))

                return HttpResponseRedirect('/proforma/consultarproforma')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
    else:
        proforma_form = ProformaForm
        productos = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto',
                                            'bloquea', 'medida_peso', 'costo', 'precio1', 'precio2').exclude(
            tipo_producto=1)
        cotizacion = Proforma.objects.get(id=pk)
        detalle = ProformaDetalle.objects.filter(proforma_id=pk).filter(Q(no_producir=False) | Q(no_producir__isnull=True))
        ambientes = Ambiente.objects.all().order_by('descripcion')

        print('contadorsd prueba' + str(cotizacion.reunion_codigo))
    return render_to_response('proforma/copiarproforma.html',{'form': proforma_form, 'productos': productos, 'ambientes': ambientes,
                               'cotizacion': cotizacion, 'detalle': detalle}, RequestContext(request))



@login_required()
def ProformaEliminarDetalleView(request):
    pk=request.POST["id"]
    objetos = ProformaDetalle.objects.get(id=pk)


    objetos.delete()
    mensaje="Eliminado con exito"

    return HttpResponse(

    )


@login_required()
def CotizacionProformaEliminarDetalleView(request):
    pk = request.POST["id"]
    objetos = CotizacionProformaDetalle.objects.get(id=pk)

    objetos.delete()
    mensaje = "Eliminado con exito"

    return HttpResponse(

    )
