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
from .tables import *
from .filters import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,Group,Permission
from OrdenesdeCompra.models import *

from inventario.models import *
from config.models import *
from proforma.models import *
from reunion.models import *
from ordenEgreso.models import *
from pedido.models import *
from ajustes.models import *

from ordenIngreso.models import *

@login_required()
@csrf_exempt
def modificarEmpresa(request):
    if request.method == 'POST':
        empresa = request.POST.get('id')
        empresa_texto = request.POST.get('texto')

        request.session['empresa_user'] = empresa

        response_data = {}
        response_data['result'] = empresa_texto

	return HttpResponse(
	            empresa_texto
	        )
    else:
        raise Http404

@login_required()
@csrf_exempt
def obtenerDetalleCompra(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')


        detalle = ComprasDetalle.objects.filter(compra_id=modulo)
        html=''
        for detal in detalle:
            product=Producto.objects.get(producto_id=detal.producto_id)

            html+='<tr><td>'+product.codigo_producto+'</td>'
            html+='<td>'+product.descripcion_producto+'</td>'
            html+='<td>'+str(detal.cantidad)+'</td>'
            html+='<td>'+str(detal.precio_compra)+'</td>'
            html+='<td>'+str(detal.total)+'</td></tr>'



        return HttpResponse(
                html
            )
    else:
        raise Http404


#-------------------------
@login_required()
@csrf_exempt
def obtenerDetalleAjuste(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')


        detalle = AjustesDetalle.objects.filter(ajustes=modulo)

        html=''
        html += "<thead><tr>"
        html += "<th>Codigo</th>"
        html += "<th> Producto </th >"
        html += "<th> Cantidad </th >"
        html += "<th> Costo </th >"
        html += "<th> Total </th >"
        html += "</tr></thead>"

        for detal in detalle:
            product=Producto.objects.get(producto_id=detal.producto_id)

            html+='<tr><td>'+product.codigo_producto+'</td>'
            html+='<td>'+product.descripcion_producto+'</td>'
            html+='<td>'+str(detal.cantidad)+'</td>'
            html+='<td>'+str(detal.costo)+'</td>'
            html+='<td>'+str(detal.total)+'</td></tr>'



        return HttpResponse(
                html
            )
    else:
        raise Http404
#-------------------------

@login_required()
@csrf_exempt
def eliminarDetalleCompra(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        detalle = ComprasDetalle.objects.get(compras_detalle_id=id)
        detalle.delete()


        return HttpResponse(

            )
    else:
        raise Http404

@login_required()
@csrf_exempt
def recibirDetalleCompra(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        nd = ComprasDetalle.objects.get(compras_detalle_id=id)
        nd.recibido=True


        try:
            kardez = Kardex.objects.get(modulo=id)

        except Kardex.DoesNotExist:
            kardez = None

        if kardez:
            print('ya existe')
        else:
            new_orden = OrdenCompra.objects.get(compra_id=nd.compra_id)
            k=Kardex()
            k.nro_documento =new_orden.nro_compra
            k.producto=nd.producto
            k.cantidad=nd.cantidad
            k.descripcion='Orden de Compra'
            k.costo=nd.precio_compra
            k.bodega=new_orden.bodega
            k.modulo=id
            k.fecha_ingreso=datetime.now()
            k.save()


        return HttpResponse(

            )
    else:
        raise Http404

@login_required()
@csrf_exempt
def obtenerSecuencial(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')


        objetos = Secuenciales.objects.get(modulo = modulo)

        modulo_secuencial = objetos.secuencial

        return HttpResponse(
                modulo_secuencial
            )
    else:
        raise Http404

@login_required()
@csrf_exempt
def obtenerParametro(request):

    if request.method == 'POST':
        clave = request.POST.get('clave')
        objetos = Parametros.objects.get(clave = clave)
        valor = objetos.valor

        return HttpResponse(
                valor
            )
    else:
        raise Http404


@login_required()
@csrf_exempt
def obtenerReunion(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')

        objetos = Reunion.objects.get(codigo = codigo)

        modulo_secuencial = objetos.cliente_id
        item = {
            'cliente': objetos.cliente_id,
            'vendedor': objetos.vendedor_id,
            'direccion': objetos.direccion,

        }
    return HttpResponse(json.dumps(item), content_type='application/json')

@login_required()
@csrf_exempt
def obtenerProforma(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')
        abreviatura = request.POST.get('abreviatura')


        objetos = Proforma.objects.get(codigo = codigo,abreviatura_codigo=abreviatura)

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
@csrf_exempt
def obtenerOrdenCompra(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')

        objetos = OrdenCompra.objects.get(nro_compra = codigo,aprobada=True,facturada=False)


        detalle = ComprasDetalle.objects.filter(compra_id = objetos.compra_id)
        ids_detalle=""
        ids=""
        for detl in detalle:
            ids=detl.compras_detalle_id
            ids_detalle+=str(ids)+','


        item = {
            'proveedor': objetos.proveedor_id,
            'compra_id': objetos.compra_id,
            'fecha': str(objetos.fecha),
            'concepto': objetos.notas,
            'comentario': objetos.comentario,
            'subtotal': objetos.subtotal,
            'total': objetos.total,
            'iva_pciento': objetos.impuesto_pciento,
            'iva': objetos.impuesto_monto,
            'dscto_pciento': objetos.dscto_pciento,
            'dscto_monto': objetos.dscto_monto,
            'subtotal_descuento': objetos.subtotal_descuento,
            'bodega': objetos.bodega.nombre,
            'detalle':ids_detalle,
        }
    return HttpResponse(json.dumps(item), content_type='application/json')
# @csrf_exempt
# def obtenerDetalleProforma(request):
#     if request.method == 'POST':
#         modulo = request.POST.get('id')
#         codigo = request.POST.get('id')

#         objetos = ProformaDetalle.objects.get(id = codigo)
#         product = Producto.objects.get(producto_id = objetos.producto_id)
#         codigo=product.codigo_producto


#         item = {
#             'nombre': objetos.nombre,
#             'producto': objetos.producto_id,
#             'cantidad': objetos.cantidad,
#             'precio_compra': objetos.precio_compra,
#             'medida': objetos.medida,
#             'total': objetos.total,
#             'codigo': codigo,
#             'id': objetos.id,
#             'reparacion': objetos.reparacion,
#         }
#     return HttpResponse(json.dumps(item), content_type='application/json')

@login_required()
@csrf_exempt
def obtenerCompraDetalle(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')

        objetos = ComprasDetalle.objects.get(compras_detalle_id = codigo)
        product = Producto.objects.get(producto_id = objetos.producto_id)
        codigo=product.codigo_producto
        nombre=product.descripcion_producto



        item = {
            'nombre': nombre,
            'producto': objetos.producto_id,
            'cantidad': objetos.cantidad,
            'precio_compra': objetos.precio_compra,
            'codigo': codigo,
            'id': objetos.compras_detalle_id,
            'codigo': codigo,
            'total': objetos.total,
            'tipo_precio': objetos.tipo_precio,

        }
    return HttpResponse(json.dumps(item), content_type='application/json')
#======================AREAS=============================#

#======================AREAS=============================#

@login_required()
def AreasListView(request):
    areas = Areas.objects.all()
    return render_to_response('areas/index.html', {'areas':areas},  RequestContext(request))
      
#=====================================================#
class AreasDetailView(ObjectDetailView):
    model = Areas
    template_name = 'areas/detail.html'

#=====================================================#

class AreasCreateView(ObjectCreateView):
    model = Areas
    form_class = AreasForm
    template_name = 'areas/create.html'
    url_success = 'areas-list'
    url_success_other = 'areas-create'
    url_cancel = 'areas-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        objetos = Secuenciales.objects.get(modulo = 'area')
        modulo_secuencial = objetos.secuencial+1
        objetos.secuencial=modulo_secuencial
        objetos.save()
        return super(AreasCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva area."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
class AreasUpdateView(ObjectUpdateView):
    model = Areas
    form_class = AreasForm
    template_name = 'areas/create.html'
    url_success = 'areas-list'
    url_cancel = 'areas-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Area actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def AreasEliminarView(request):
    return eliminarView(request, Areas, 'areas-list')

#=====================================================#
@login_required()
def AreasEliminarByPkView(request, pk):
    objetos = Areas.objects.filter(id__in = pk)
    for obj in objetos:
        if obj.activo:
            obj.activo = False
        else:
            obj.activo= True

        obj.save()

    return HttpResponseRedirect('/config/areas')

#======================================================#
@login_required()
@csrf_exempt
def misAreasGuardar(request):
    item = {'exito':0}
    if request.method == 'POST':
        try:

            areas = request.POST['data']
            areas = json.loads(bodegas)

            for area in areas:
                if not area['codigo'] == "":
                    try:
                            a = Areas()
                            a.created_by = request.user
                            a.updated_at = datetime.now()
                            a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar el area")
                        pass

                    item = {'exito':1}

            if item['exito'] == 1:
                messages.info(request, 'Areas guardadas!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito':0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')

#======================Vehiculos=============================#

class VehiculoListView(ObjectListView):
    model = Vehiculo
    paginate_by = 100
    template_name = 'vehiculo/index.html'
    table_class = VehiculoTable
    filter_class = VehiculoFilter

    def get_context_data(self, **kwargs):
        context = super(VehiculoListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('vehiculo-delete')
        return context

#=====================================================#

class VehiculoDetailView(ObjectDetailView):
    model = Vehiculo
    template_name = 'vehiculo/detail.html'

#=====================================================#
class VehiculoCreateView(ObjectCreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/create.html'
    url_success = 'vehiculo-list'
    url_success_other = 'vehiculo-create'
    url_cancel = 'vehiculo-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo = 'vehiculo')

        modulo_secuencial = objetos.secuencial+1
        objetos.secuencial=modulo_secuencial
        objetos.save()

        return super(VehiculoCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo vehiculo."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
class VehiculoUpdateView(ObjectUpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/create.html'
    url_success = 'vehiculo-list'
    url_cancel = 'vehiculo-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Vehiculo actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def VehiculoEliminarView(request):
    return eliminarView(request, Vehiculo, 'vehiculo-list')

#=====================================================#
@login_required()
def VehiculoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Vehiculo)
#======================================================#
@login_required()
@csrf_exempt
def misVehiculoGuardar(request):
    item = {'exito':0}
    if request.method == 'POST':
        try:

            vehiculos = request.POST['data']
            vehiculos = json.loads(vehiculos)

            for vehiculo in vehiculos:
                if not vehiculo['codigo'] == "":
                    try:
                            a = Vehiculo()
                            a.created_by = request.user
                            a.updated_at = datetime.now()
                            a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar el vehiculo")
                        pass

                    item = {'exito':1}

            if item['exito'] == 1:
                messages.info(request, 'Vehiculo guardadas!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito':0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')




#======================Estados Pro=============================#
class EstadosProListView(ObjectListView):
    model = EstadosPro
    paginate_by = 100
    template_name = 'estadospro/index.html'
    table_class = EstadosProTable
    filter_class = EstadosProFilter

    def get_context_data(self, **kwargs):
        context = super(EstadosProListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('estadospro-delete')
        return context

#=====================================================#
class EstadosProDetailView(ObjectDetailView):
    model = EstadosPro
    template_name = 'estadospro/detail.html'

#=====================================================#
class EstadosProCreateView(ObjectCreateView):
    model = EstadosPro
    form_class = EstadosProForm
    template_name = 'estadospro/create.html'
    url_success = 'estadospro-list'
    url_success_other = 'estadospro-create'
    url_cancel = 'estadospro-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo = 'estado')

        modulo_secuencial = objetos.secuencial+1
        objetos.secuencial=modulo_secuencial
        objetos.save()
        return super(EstadosProCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo estado."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
class EstadosProUpdateView(ObjectUpdateView):
    model = EstadosPro
    form_class = EstadosProForm
    template_name = 'estadospro/create.html'
    url_success = 'estadospro-list'
    url_cancel = 'estadospro-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Estado actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def EstadosProEliminarView(request):
    return eliminarView(request, EstadosPro, 'estadospro-list')

#=====================================================#
@login_required()
def EstadosProEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, EstadosPro)
#======================================================#
@login_required()
@csrf_exempt
def misEstadosProGuardar(request):
    item = {'exito':0}
    if request.method == 'POST':
        try:

            estadospros = request.POST['data']
            estadospros = json.loads(estadospros)

            for estadospro in estadospros:
                if not estadospros['codigo'] == "":
                    try:
                            a = EstadosPro()
                            a.created_by = request.user
                            a.updated_at = datetime.now()
                            a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar el estado")
                        pass

                    item = {'exito':1}

            if item['exito'] == 1:
                messages.info(request, 'Estado guardadas!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito':0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')

#======================Tipor Mue=============================#
class TipoMuebListView(ObjectListView):
    model = TipoMueb
    paginate_by = 100
    template_name = 'tipomueb/index.html'
    table_class = TipoMuebTable
    filter_class = TipoMuebFilter

    def get_context_data(self, **kwargs):
        context = super(TipoMuebListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('tipomueb-delete')
        return context

#=====================================================#
class TipoMuebDetailView(ObjectDetailView):
    model = TipoMueb
    template_name = 'tipomueb/detail.html'

#=====================================================#

class TipoMuebCreateView(ObjectCreateView):
    model = TipoMueb
    form_class = TipoMuebForm
    template_name = 'tipomueb/create.html'
    url_success = 'tipomueb-list'
    url_success_other = 'tipomueb-create'
    url_cancel = 'tipomueb-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo = 'tipomueble')

        modulo_secuencial = objetos.secuencial+1
        objetos.secuencial=modulo_secuencial
        objetos.save()

        return super(TipoMuebCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo tipo."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
class TipoMuebUpdateView(ObjectUpdateView):
    model = TipoMueb
    form_class = TipoMuebForm
    template_name = 'tipomueb/create.html'
    url_success = 'tipomueb-list'
    url_cancel = 'tipomueb-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Tipo actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def TipoMuebEliminarView(request):
    return eliminarView(request, TipoMueb, 'estadospro-list')

#=====================================================#
@login_required()
def TipoMuebEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, TipoMueb)
#======================================================#
@login_required()
@csrf_exempt
def misTipoMuebGuardar(request):
    item = {'exito':0}
    if request.method == 'POST':
        try:

            tipomuebs = request.POST['data']
            tipomuebs = json.loads(tipomuebs)

            for tipomueb in tipomuebs:
                if not tipomueb['codigo'] == "":
                    try:
                            a = TipoMueb()
                            a.created_by = request.user
                            a.updated_at = datetime.now()
                            a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar el estado")
                        pass

                    item = {'exito':1}

            if item['exito'] == 1:
                messages.info(request, 'Estado guardadas!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito':0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')

#==============SECUENCIALES=======================================#
@login_required()
def SecuencialesListView(request):
    if request.method == 'POST':

        secuenciales = Secuenciales.objects.all()
        return render_to_response('secuenciales/index.html', {'secuenciales': secuenciales}, RequestContext(request))
    else:
        secuenciales = Secuenciales.objects.all()
        return render_to_response('secuenciales/index.html', {'secuenciales': secuenciales}, RequestContext(request))


#=====================================================#
class SecuencialesDetailView(ObjectDetailView):
    model = Secuenciales
    template_name = 'secuenciales/detail.html'

#=====================================================#
@login_required()
def SecuencialesCreateView(request):
    if request.method == 'POST':
        form = SecuencialesForm(request.POST)

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()


            return HttpResponseRedirect('/config/secuenciales')
        else:
            print 'error'
        print form.errors, len(form.errors)
    else:
        form = SecuencialesForm

    return render_to_response('secuenciales/create.html', {'form': form}, RequestContext(request))


#=====================================================#
class SecuencialesUpdateView(ObjectUpdateView):
    model = Secuenciales
    form_class = SecuencialesForm
    template_name = 'secuenciales/create.html'
    url_success = 'secuenciales-list'
    url_cancel = 'secuenciales-list'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Secuenciales actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def SecuencialesEliminarView(request):
    return eliminarView(request, Secuenciales, 'secuenciales-list')

#=====================================================#
@login_required()
def SecuencialesEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Secuenciales)

#==============MENU=======================================#
class MenuListView(ObjectListView):
    model = Menu
    paginate_by = 100
    template_name = 'menu/index.html'
    table_class = MenuTable
    filter_class = MenuFilter

    def get_context_data(self, **kwargs):
        context = super(MenuListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('menu-delete')
        return context

#=====================================================#
class MenuDetailView(ObjectDetailView):
    model = Menu
    template_name = 'menu/detail.html'

#=====================================================#


@login_required()
def MenuCreateView(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='empleados')
                secuencial.secuencial = secuencial.secuencial + 1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None


            return HttpResponseRedirect('/config/menu/')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = MenuForm


    return render_to_response('menu/create.html', {'form': form,},
                              RequestContext(request))

#=====================================================#
class MenuUpdateView(ObjectUpdateView):
    model = Menu
    form_class = MenuForm
    template_name = 'menu/create.html'
    url_success = 'menu-list'
    url_cancel = 'menu-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Menu actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def MenuEliminarView(request):
    return eliminarView(request, Menu, 'menu-list')

#=====================================================#
@login_required()
def MenuEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Menu)

#==============MENUGROUP=======================================#
class MenuGroupListView(ObjectListView):
    model = MenuGroup
    paginate_by = 100
    template_name = 'menu_group/index.html'

    table_class = MenuGroupTable
    filter_class = MenuGroupFilter

    def get_context_data(self, **kwargs):
        context = super(MenuGroupListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('menu-group-delete')
        #context['menu'] = Menu.objects.get(id=self.request.pk)

        return context

class MenuGroupCreateView(ObjectCreateView):

    model = MenuGroup
    form_class = MenuGroupForm
    template_name = 'menu_group/create.html'
    url_success = 'menu-group-list'
    url_success_other = 'menu-group-create'
    url_cancel = 'menu-group-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(MenuGroupCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo menu."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
class MenuGroupUpdateView(ObjectUpdateView):
    model = MenuGroup
    form_class = MenuGroupForm
    template_name = 'menu_group/create.html'
    url_success = 'menu-group-list'
    url_cancel = 'menu-group-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Menu actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def MenuGroupEliminarView(request):
    return eliminarView(request, MenuGroup, 'menu-group-list')

#=====================================================#
@login_required()
def MenuGroupEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, MenuGroup)


@login_required()
@csrf_exempt
def obtenerDetalleOrdenEgreso(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')


        detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=modulo)
        html=''
        for detal in detalle:
            product=Producto.objects.get(producto_id=detal.producto_id)

            html+='<tr><td>'+product.codigo_producto+'</td>'
            html+='<td>'+product.descripcion_producto+'</td>'
            html+='<td>'+str(detal.cantidad)+'</td>'
            html+='<td>'+str(detal.precio_compra)+'</td>'
            html+='<td>'+str(detal.total)+'</td></tr>'



        return HttpResponse(
                html
            )
    else:
        raise Http404

@login_required()
@csrf_exempt
def despacharDetalleOrdenEgreso(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        nd = OrdenEgresoDetalle.objects.get(id=id)
        nd.despachar=True
        nd.save()

        # try:
        #     kardez = Kardex.objects.get(modulo=id)

        # except Kardex.DoesNotExist:
        #     kardez = None

        # if kardez:
        #     print('ya existe')
        # else:
        #     new_orden = OrdenCompra.objects.get(compra_id=nd.compra_id)
        #     k=Kardex()
        #     k.nro_documento =new_orden.nro_compra
        #     k.producto=nd.producto
        #     k.cantidad=nd.cantidad
        #     k.descripcion='Orden de Compra'
        #     k.costo=nd.precio_compra
        #     k.bodega=new_orden.bodega
        #     k.modulo=id
        #     k.fecha_ingreso=datetime.now()
        #     k.save()


        return HttpResponse(

            )
    else:
        raise Http404

@login_required()
@csrf_exempt
def obtenerOrdenEgreso(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')

        objetos = OrdenEgreso.objects.get(codigo = codigo,aprobada=True)
        try:
            oeo = EgresoOrdenEgreso.objects.filter(orden_egreso_id=objetos.id)

        except EgresoOrdenEgreso.DoesNotExist:
            oeo = None


        if oeo:

            raise Http404

        else:

            detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id = objetos.id)
            ids_detalle=""
            ids=""
            for detl in detalle:
                ids=detl.id
                ids_detalle+=str(ids)+','

            subtotal = '0'
            iva = '0'
            total = '0'
            if objetos.subtotal:
                subtotal=objetos.subtotal

            if objetos.impuesto_monto:
                iva = objetos.impuesto_monto
            if objetos.total:
                total = objetos.total

            item = {
                'id': objetos.id,
                'fecha': str(objetos.fecha.strftime('%Y-%m-%d')),
                'concepto': objetos.notas,
                'comentario': objetos.comentario,
                'subtotal': subtotal,
                'iva': iva,
                'total': total,
                'bodega': objetos.bodega.nombre,
                'detalle':ids_detalle,
            }
        return HttpResponse(json.dumps(item), content_type='application/json')
    else:
        raise Http404

@login_required()
@csrf_exempt
def obtenerOrdenEgresoDetalleUnico(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')

        objetos = OrdenEgresoDetalle.objects.get(id = codigo)
        product = Producto.objects.get(producto_id = objetos.producto_id)
        codigo=product.codigo_producto
        nombre=product.descripcion_producto
        try:
            kardex = ProductoEnBodega.objects.get(producto_id=product.producto_id,bodega_id=objetos.bodega_id)

        except ProductoEnBodega.DoesNotExist:
            kardex = None


        if kardex:
            if kardex.bodega_id == objetos.bodega_id:
                inventario=kardex.cantidad
                if objetos.cantidad<=kardex.cantidad:
                    existe=1
                else:
                    existe=0
            else:
                existe=0
        else:
            existe=0

        item = {
            'nombre': nombre,
            'producto': objetos.producto_id,
            'cantidad': objetos.cantidad,
            'precio_compra': objetos.precio_compra,
            'codigo': codigo,
            'id': objetos.id,
            'codigo': codigo,
            'total': objetos.total,
            'despachar': objetos.despachar,
            'existe': existe,
            'disminuir_kardex': objetos.disminuir_kardex,
        }
    return HttpResponse(json.dumps(item), content_type='application/json')
#======================AREAS=============================#
@login_required()
@csrf_exempt
def eliminarEgreso(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        detalle = OrdenEgresoDetalle.objects.get(id=id)
        detalle.delete()


        return HttpResponse(

            )
    else:
        raise Http404

@login_required()
@csrf_exempt
def obtenerDetalleProforma(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')


        detalle = ProformaDetalle.objects.filter(proforma_id=modulo)
        html=''
        for detal in detalle:
            product=Producto.objects.get(producto_id=detal.producto_id)
            detail=(detal.nombre).encode('ascii', 'ignore').decode('ascii')
            if detal.reparacion:
                repar='SI'
            else:
                repar='NO'

            html+='<tr><td>'+str(product.codigo_producto)+'</td>'
            html+='<td>'+str(detail)+'</td>'
            html+='<td>'+str(detal.cantidad)+'</td>'
            html+='<td>'+str(detal.precio_compra)+'</td>'
            html+='<td>'+str(detal.total)+'</td>'
            html+='<td>'+str(repar)+'</td>'
            html+='<td><img src="/media/'+str(detal.imagen)+'" alt="X" width="60px" height="40px"></td></tr>'




        return HttpResponse(
                html
            )
    else:
        raise Http404

@login_required()
@csrf_exempt
def obtenerDetallePedido(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')


        detalle = PedidoDetalle.objects.filter(pedido_id=modulo)
        html=''
        repar=''
        for detal in detalle:
            product=Producto.objects.get(producto_id=detal.producto_id)
            detail=(detal.nombre).encode('ascii', 'ignore').decode('ascii')
            if detal.reparacion:
                repar='SI'
            else:
                repar='NO'


            if detal.no_producir:
                mensaje='NO SE VA A PRODUCIR'
            else:
                mensaje = ''


            html+='<tr><td>'+product.codigo_producto+'</td>'
            html+='<td>'+str(detail)+'</td>'
            html+='<td>'+str(detal.cantidad)+'</td>'
            html+='<td>'+str(detal.precio_compra)+'</td>'
            html+='<td>'+str(detal.total)+'</td>'
            html+='<td>'+str(repar)+'</td>'
            html+='<td><img src="/media/'+str(detal.imagen)+'" alt="X" width="60px" height="40px"></td>'
            html += '<td>' + str(mensaje) + '</td></tr>'


        return HttpResponse(
                html
            )
    else:
        raise Http404

@login_required()
@csrf_exempt
def obtenerCliente(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')

        objetos = Cliente.objects.get(id_cliente = codigo)

        modulo_secuencial = objetos.id_cliente
        item = {
            'cliente': objetos.direccion1,

        }
    return HttpResponse(json.dumps(item), content_type='application/json')

@login_required()
@csrf_exempt
def obtenerDetalleOrdenIngreso(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')


        detalle = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=modulo)
        html=''
        for detal in detalle:
            product=Producto.objects.get(producto_id=detal.producto_id)

            html+='<tr><td>'+product.codigo_producto+'</td>'
            html+='<td>'+product.descripcion_producto+'</td>'
            html+='<td>'+str(detal.cantidad)+'</td>'
            html+='<td>'+str(detal.medida)+'</td></tr>'

        return HttpResponse(
                html
            )
    else:
        raise Http404

#======================TIPO LUGAR=============================#
class TipoLugarListView(ObjectListView):
    model = TipoLugar
    paginate_by = 100
    template_name = 'tipolugar/index.html'
    table_class = TipoLugarTable
    filter_class = TipoLugarFilter

    def get_context_data(self, **kwargs):
        context = super(TipoLugarListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('tipolugar-delete')
        return context

#=====================================================#
class TipoLugarDetailView(ObjectDetailView):
    model = TipoLugar
    template_name = 'tipolugar/detail.html'

#=====================================================#
class TipoLugarCreateView(ObjectCreateView):
    model = TipoLugar
    form_class = TipoLugarForm
    template_name = 'tipolugar/create.html'
    url_success = 'tipolugar-list'
    url_success_other = 'tipolugar-create'
    url_cancel = 'tipolugar-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        objetos = Secuenciales.objects.get(modulo = 'tipolugar')
        modulo_secuencial = objetos.secuencial+1
        objetos.secuencial=modulo_secuencial
        objetos.save()
        return super(TipoLugarCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo tipo de lugar."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
class TipoLugarUpdateView(ObjectUpdateView):
    model = TipoLugar
    form_class = TipoLugarForm
    template_name = 'tipolugar/create.html'
    url_success = 'tipolugar-list'
    url_cancel = 'tipolugar-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Tipo Lugar actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def TipoLugarEliminarView(request):
    return eliminarView(request, TipoLugar, 'tipolugar-list')

#=====================================================#
@login_required()
def TipoLugarEliminarByPkView(request, pk):
    objetos = TipoLugar.objects.filter(id__in = pk)
    for obj in objetos:
        if obj.activo:
            obj.activo = False
        else:
            obj.activo= True

        obj.save()

    return HttpResponseRedirect('/config/tipolugar')

@login_required()
@csrf_exempt
def obtenerPedidoOrdenProduccion(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')

        objetos = PedidoDetalle.objects.get(id = modulo)

        item = {
            'nombre': objetos.nombre,
            'cantidad': objetos.cantidad,
            'detalle': objetos.detalle,
            'medida': str(objetos.medida),
            'codigoproduccion': objetos.codigo_produccion,
            'reparacion': objetos.reparacion,


        }
    return HttpResponse(json.dumps(item), content_type='application/json')


#======================PuntosVenta=============================#
@login_required()
def PuntosVentaListView(request):
    if request.method == 'POST':

        areas = PuntosVenta.objects.all()
        return render_to_response('puntosventa/index.html', {'puntosventa': areas}, RequestContext(request))
    else:
        areas = PuntosVenta.objects.all()
        return render_to_response('puntosventa/index.html', {'puntosventa': areas}, RequestContext(request))

#=====================================================#
class PuntosVentaDetailView(ObjectDetailView):
    model = PuntosVenta
    template_name = 'puntosventa/detail.html'

#=====================================================#
class PuntosVentaCreateView(ObjectCreateView):
    model = PuntosVenta
    form_class = PuntosVentaForm
    template_name = 'puntosventa/create.html'
    url_success = 'puntosventa-list'
    url_success_other = 'puntosventa-create'
    url_cancel = 'puntosventa-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        objetos = Secuenciales.objects.get(modulo = 'puntosventa')
        modulo_secuencial = objetos.secuencial+1
        objetos.secuencial=modulo_secuencial
        objetos.save()
        return super(PuntosVentaCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva area."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
class PuntosVentaUpdateView(ObjectUpdateView):
    model = PuntosVenta
    form_class = PuntosVentaForm
    template_name = 'puntosventa/create.html'
    url_success = 'puntosventa-list'
    url_cancel = 'puntosventa-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Punto de Venta actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def PuntosVentaEliminarView(request):
    return eliminarView(request, PuntosVenta, 'puntosventa-list')

#=====================================================#
@login_required()
def PuntosVentaEliminarByPkView(request, pk):
    objetos = PuntosVenta.objects.filter(id__in = pk)
    for obj in objetos:
        if obj.activo:
            obj.activo = False
        else:
            obj.activo= True

        obj.save()

    return HttpResponseRedirect('/config/puntosventa')

@login_required()
@csrf_exempt
def obtenerAnalisisProductosBodega(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        producto=ProductoEnBodega.objects.filter(bodega_id=id)
        html=""
        i=0
        for p in producto:
            i+= 1
            html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"><i class=" glyphicon glyphicon-trash icon-white"></i></a></td>'
            html+='<td><input type="hidden" class="form-control" id="id_kits'+str(i)+'" name="id_kits'+str(i)+'" value="'+str(p.producto.producto_id)+'"><input type="text" class="form-control" id="codigo_kits'+str(i)+'" name="codigo_kits'+str(i)+'" value="'+str(p.producto.codigo_producto)+'"></td>'
            html+='<td><textarea class="form-control" id="nombre_kits'+str(i)+'" name="nombre_kits'+str(i)+'">'+str(p.producto.descripcion_producto) +'</textarea></td>'
            html+='<td><textarea class="form-control" id="detalle_kits'+str(i)+'" name="detalle_kits'+str(i)+'"></textarea></td>'
            html+='<td><input type="text" name="cantidad_kits'+str(i)+'" id="cantidad_kits'+str(i)+'" value="'+str( p.cantidad)+'" /></td>'
            html+='<td><input type="text" name="cantidad_real_kits'+str(i)+'" id="cantidad_real_kits'+str(i)+'" value="" /></td>'
            # html+='<td><input type="text" name="costo_kits'+str(i)+'" id="costo_kits'+str(i)+'" value="'+str( p.producto.precio1)+'" /></td>'
            # total=p.producto.precio1*p.cantidad
            # html+='<td><input type="text" name="total_kits'+str(i)+'" id="total_kits'+str(i)+'" value="'+str(total)+'" /></td>'
            html+='</tr>'


        return HttpResponse(
                html
            )
    else:
        raise Http404

@login_required()
def ParametrosListView(request):
      if request.method == 'POST':

        row = Parametros.objects.all().order_by('clave')
        return render_to_response('parametros/index.html', {'row':row},  RequestContext(request))
      else:
        row = Parametros.objects.all().order_by('clave')
        return render_to_response('parametros/index.html', {'row':row},  RequestContext(request))

class ParametrosCreateView(ObjectCreateView):
    model = Parametros
    form_class = ParametrosForm
    template_name = 'parametros/nuevo.html'
    url_success = 'parametros-list'
    url_success_other = 'parametros-create'
    url_cancel = 'parametros-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()



        return super(ParametrosCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva parametro."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
class ParametrosUpdateView(ObjectUpdateView):
    model = Parametros
    form_class = ParametrosForm
    template_name = 'parametros/nuevo.html'
    url_success = 'parametros-list'
    url_cancel = 'parametros-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Parametro actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

@login_required()
def ParametrosNuevoView(request):
      if request.method == 'POST':
        proforma_form=ParametrosForm(request.POST)


        if proforma_form.is_valid():
            new_orden=proforma_form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()

            return HttpResponseRedirect('/config/parametros')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
      else:
        proforma_form=ParametrosForm

      return render_to_response('parametros/nuevo.html', { 'form': proforma_form,},  RequestContext(request))

@login_required()
def CiudadListView(request):
    if request.method == 'POST':

        ciudades = Ciudad.objects.all()
        return render_to_response('ciudad/index.html', {'ciudades': ciudades}, RequestContext(request))
    else:
        ciudades = Ciudad.objects.all()
        return render_to_response('ciudad/index.html', {'ciudades': ciudades}, RequestContext(request))


class CiudadCreateView(ObjectCreateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'ciudad/create.html'
    url_success = 'ciudad-list'
    url_success_other = 'ciudad-create'
    url_cancel = 'ciudad-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo='ciudad')

        modulo_secuencial = objetos.secuencial + 1
        objetos.secuencial = modulo_secuencial
        objetos.save()

        return super(CiudadCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva ciudad."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class CiudadUpdateView(ObjectUpdateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'ciudad/create.html'
    url_success = 'ciudad-list'
    url_cancel = 'ciudad-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Ciudad actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


@login_required()
def EstadoCivilListView(request):
    if request.method == 'POST':

        estados = EstadoCivil.objects.all()
        return render_to_response('estado_civil/index.html', {'estados': estados}, RequestContext(request))
    else:
        estados = EstadoCivil.objects.all()
        return render_to_response('estado_civil/index.html', {'estados': estados}, RequestContext(request))


class EstadoCivilCreateView(ObjectCreateView):
    model = EstadoCivil
    form_class = EstadoCivilForm
    template_name = 'estado_civil/create.html'
    url_success = 'estado-civil-list'
    url_success_other = 'estado-civil-create'
    url_cancel = 'estado-civil-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo='estado_civil')

        modulo_secuencial = objetos.secuencial + 1
        objetos.secuencial = modulo_secuencial
        objetos.save()

        return super(EstadoCivilCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo estado."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class EstadoCivilUpdateView(ObjectUpdateView):
    model = EstadoCivil
    form_class = EstadoCivilForm
    template_name = 'estado_civil/create.html'
    url_success = 'estado-civil-list'
    url_cancel = 'estado-civil-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Estado Civil actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


@login_required()
def PaisListView(request):
    if request.method == 'POST':

        paises = Pais.objects.all()
        return render_to_response('pais/index.html', {'paises': paises}, RequestContext(request))
    else:
        paises = Pais.objects.all()
        return render_to_response('pais/index.html', {'paises': paises}, RequestContext(request))


class PaisCreateView(ObjectCreateView):
    model = Pais
    form_class = PaisForm
    template_name = 'pais/create.html'
    url_success = 'pais-list'
    url_success_other = 'pais-create'
    url_cancel = 'pais-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo='pais')

        modulo_secuencial = objetos.secuencial + 1
        objetos.secuencial = modulo_secuencial
        objetos.save()

        return super(PaisCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo pais."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class PaisUpdateView(ObjectUpdateView):
    model = Pais
    form_class = PaisForm
    template_name = 'pais/create.html'
    url_success = 'pais-list'
    url_cancel = 'pais-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Pais actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


@login_required()
def ProvinciaListView(request):
    if request.method == 'POST':

        provincias = Provincia.objects.all()
        return render_to_response('provincia/index.html', {'provincias': provincias}, RequestContext(request))
    else:
        provincias = Provincia.objects.all()
        return render_to_response('provincia/index.html', {'provincias': provincias}, RequestContext(request))


class ProvinciaCreateView(ObjectCreateView):
    model = Provincia
    form_class = ProvinciaForm
    template_name = 'provincia/create.html'
    url_success = 'provincia-list'
    url_success_other = 'provincia-create'
    url_cancel = 'provincia-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo='provincia')

        modulo_secuencial = objetos.secuencial + 1
        objetos.secuencial = modulo_secuencial
        objetos.save()

        return super(ProvinciaCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo provincia."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class ProvinciaUpdateView(ObjectUpdateView):
    model = Provincia
    form_class = ProvinciaForm
    template_name = 'provincia/create.html'
    url_success = 'provincia-list'
    url_cancel = 'provincia-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Provincia actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

@login_required()
def RelacionLaboralListView(request):
    if request.method == 'POST':

        relaciones = RelacionLaboral.objects.all()
        return render_to_response('relacion_laboral/index.html', {'relaciones': relaciones}, RequestContext(request))
    else:
        relaciones = RelacionLaboral.objects.all()
        return render_to_response('relacion_laboral/index.html', {'relaciones': relaciones}, RequestContext(request))


class RelacionLaboralCreateView(ObjectCreateView):
    model = RelacionLaboral
    form_class = RelacionLaboralForm
    template_name = 'relacion_laboral/create.html'
    url_success = 'relacion-laboral-list'
    url_success_other = 'relacion-laboral-create'
    url_cancel = 'relacion-laboral-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo='relacion_laboral')

        modulo_secuencial = objetos.secuencial + 1
        objetos.secuencial = modulo_secuencial
        objetos.save()

        return super(RelacionLaboralCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo relacion laboral."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class RelacionLaboralUpdateView(ObjectUpdateView):
    model = RelacionLaboral
    form_class = RelacionLaboralForm
    template_name = 'relacion_laboral/create.html'
    url_success = 'relacion-laboral-list'
    url_cancel = 'relacion-laboral-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Relacion laboral actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)



@login_required()
def TipoRemuneracionListView(request):
    if request.method == 'POST':

        tipos = TipoRemuneracion.objects.all()
        return render_to_response('tipo_remuneracion/index.html', {'tipos': tipos}, RequestContext(request))
    else:
        tipos = TipoRemuneracion.objects.all()
        return render_to_response('tipo_remuneracion/index.html', {'tipos': tipos}, RequestContext(request))


class TipoRemuneracionCreateView(ObjectCreateView):
    model = TipoRemuneracion
    form_class = TipoRemuneracionForm
    template_name = 'tipo_remuneracion/create.html'
    url_success = 'tipo-remuneracion-list'
    url_success_other = 'tipo-remuneracion-create'
    url_cancel = 'tipo-remuneracion-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo='tipo_remuneracion')

        modulo_secuencial = objetos.secuencial + 1
        objetos.secuencial = modulo_secuencial
        objetos.save()

        return super(TipoRemuneracionCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo tipo de remuneracion."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class TipoRemuneracionUpdateView(ObjectUpdateView):
    model = TipoRemuneracion
    form_class = TipoRemuneracionForm
    template_name = 'tipo_remuneracion/create.html'
    url_success = 'tipo-remuneracion-list'
    url_cancel = 'tipo-remuneracion-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Tipo remuneracion actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


@login_required()
def FormaPagoEmpleadoListView(request):
    if request.method == 'POST':

        formas = FormaPagoEmpleado.objects.all()
        return render_to_response('forma_pago_empleado/index.html', {'formas': formas}, RequestContext(request))
    else:
        formas = FormaPagoEmpleado.objects.all()
        return render_to_response('forma_pago_empleado/index.html', {'formas': formas}, RequestContext(request))

class FormaPagoEmpleadoCreateView(ObjectCreateView):
    model = FormaPagoEmpleado
    form_class = FormaPagoEmpleadoForm
    template_name = 'forma_pago_empleado/create.html'
    url_success = 'forma-pago-empleado-list'
    url_success_other = 'forma-pago-empleado-create'
    url_cancel = 'forma-pago-empleado-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo='forma_pago_empleado')

        modulo_secuencial = objetos.secuencial + 1
        objetos.secuencial = modulo_secuencial
        objetos.save()

        return super(FormaPagoEmpleadoCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva forma de pago."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class FormaPagoEmpleadoUpdateView(ObjectUpdateView):
    model = FormaPagoEmpleado
    form_class = FormaPagoEmpleadoForm
    template_name = 'forma_pago_empleado/create.html'
    url_success = 'forma-pago-empleado-list'
    url_cancel = 'forma-pago-empleado-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Forma de Pago Empleado actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)




@login_required()
def AnioListView(request):
      if request.method == 'POST':
          anios = Anio.objects.all()
          return render_to_response('anio/index.html', {'anios':anios},  RequestContext(request))
      else:
          anios = Anio.objects.all()
          return render_to_response('anio/index.html', {'anios': anios}, RequestContext(request))

#=====================================================#

class AnioCreateView(ObjectCreateView):
    model = Anio
    form_class = AnioForm
    template_name = 'anio/create.html'
    url_success = 'anio-list'
    url_success_other = 'anio-create'
    url_cancel = 'anio-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        # objetos = Secuenciales.objects.get(modulo = 'area')
        # modulo_secuencial = objetos.secuencial+1
        # objetos.secuencial=modulo_secuencial
        # objetos.save()
        return super(AnioCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo anio."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
class AnioUpdateView(ObjectUpdateView):
    model = Anio
    form_class = AnioForm
    template_name = 'anio/create.html'
    url_success = 'anio-list'
    url_cancel = 'anio-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Anio actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)



@login_required()
def BloqueoPeriodoListView(request):
    if request.method == 'POST':
        bloqueos = BloqueoPeriodo.objects.all()
        return render_to_response('bloqueo_periodo/index.html', {'bloqueos':bloqueos},  RequestContext(request))
    else:
        bloqueos = BloqueoPeriodo.objects.all()
        return render_to_response('bloqueo_periodo/index.html', {'bloqueos':bloqueos},  RequestContext(request))


@login_required()
def BloqueoPeriodoCreateView(request):
    if request.method == 'POST':
        proforma_form = BloqueoPeriodoForm(request.POST)

        if proforma_form.is_valid():
            new_orden = proforma_form.save(commit=False)
            new_orden.created_by = request.user
            new_orden.updated_by = request.user
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            
            new_orden.save()
            formato = "%m/%Y"
            fecha=str(new_orden.mes_id)+'/'+str(new_orden.anio.nombre)
            new_orden.fecha= datetime.strptime(fecha, formato)
            new_orden.save()
            

            return HttpResponseRedirect('/config/bloqueo_periodo')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
    else:
        proforma_form = BloqueoPeriodoForm

    return render_to_response('bloqueo_periodo/create.html', {'form': proforma_form,}, RequestContext(request))


class BloqueoPeriodoUpdateView(ObjectUpdateView):
    model = BloqueoPeriodo
    form_class = BloqueoPeriodoForm
    template_name = 'bloqueo_periodo/create.html'
    url_success = 'bloqueo-periodo-list'
    url_cancel = 'bloqueo-periodo-list'

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()
        formato = "%m/%Y"
        fecha=str(self.object.mes_id)+'/'+str(self.object.anio.nombre)
        self.object.fecha= datetime.strptime(fecha, formato)
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Registro actualizado con exito')

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


  
@csrf_exempt
def eliminarBloqueoPeriodo(request,pk):
    if request.method == 'POST':
        detalle = BloqueoPeriodo.objects.get(id=pk)
        detalle.delete()


        return HttpResponseRedirect('/config/bloqueo_periodo')
    else:
        detalle = BloqueoPeriodo.objects.get(id=pk)
        detalle.delete()


        return HttpResponseRedirect('/config/bloqueo_periodo')