from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, \
    eliminarByPkView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, render_to_response
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
from models import *
from django.forms.extras.widgets import *
from django.contrib.auth import authenticate, login
from inventario.tables import *
# from login.lib.tools import Tools
from inventario.models import *
from config.models import *
from django.db import IntegrityError, transaction
from transacciones.models import DocumentoCompra,DocumentosCompraDetalle
from django.db import connection



# from config.models import Mensajes



from login.lib.tools import Tools
from django.contrib import auth
# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse




def OrdenCompraListView(request):
    cursor = connection.cursor()
    query=" select o.compra_id,o.nro_compra,p.nombre_proveedor,o.total,o.notas,o.fecha,o.aprobada,o.anulado, o.facturada,bp.id from orden_compra o left join proveedor p on p.proveedor_id=o.proveedor_id left join bloqueo_periodo bp on  date_part('year',bp.fecha)=EXTRACT(YEAR FROM o.fecha) and date_part('month',bp.fecha)=EXTRACT(MONTH from o.fecha) order by o.fecha"

    cursor.execute(query)
    ro = cursor.fetchall()
    return render_to_response('ordenescompra/list.html', {'ordenesdecompras': ro},
                                  RequestContext(request))
    


# =====================================================#
class OrdenCompraDetailView(ObjectDetailView):
    model = OrdenCompra
    template_name = 'ordenescompra/detail.html'


# =====================================================#
@login_required()
@transaction.atomic
def OrdenCompraCreateView(request):
    if request.method == 'POST':
        ordencompra_form = OrdenCompraForm(request.POST)
        productos = Producto.objects.exclude(tipo_producto=2)

        if ordencompra_form.is_valid():
            with transaction.atomic():
                new_orden = ordencompra_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.subtotal = request.POST["total"]
                new_orden.total = request.POST["total_g"]
                new_orden.dscto_pciento = request.POST["porcentaje_descuento"]
                new_orden.dscto_monto = request.POST["descuento"]
                new_orden.impuesto_pciento = request.POST["porcentaje_iva"]
                new_orden.subtotal_descuento = request.POST["subtotal_desc"]
                new_orden.impuesto_monto = request.POST["iva"]

                # new_orden.subtotal=request.POST["total"]
                #subtotal = request.POST["total"]
                #impuesto_mont = float(request.POST["total"]) * 0.12
                # new_orden.impuesto_monto=float(request.POST["total"])*0.12
                # new_orden.total=round (float(subtotal)+float(impuesto_mont),2)

                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='ordenesdecompra')
                    if secuencial.secuencial!=new_orden.nro_compra:
                        new_orden.nro_compra=secuencial.secuencial
                        new_orden.save()
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
                            comprasdetalle = ComprasDetalle()
                            comprasdetalle.compra_id = new_orden.compra_id
                            comprasdetalle.producto_id = request.POST["id_kits" + str(i)]
                            comprasdetalle.proveedor_id = request.POST["proveedor"]
                            comprasdetalle.bodega_id = request.POST["bodega"]
                            comprasdetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                            # kits.costo=float(request.POST["costo_kits1"])
                            comprasdetalle.precio_compra = request.POST["costo_kits" + str(i)]
                            comprasdetalle.tipo_precio = request.POST["tipo_precio_kits" + str(i)]
                            comprasdetalle.total = request.POST["total_kits" + str(i)]
                            comprasdetalle.save()
                            print('contadorsd prueba' + str(contador))

            return HttpResponseRedirect('/OrdenesdeCompra/OrdenesdeCompra')
        else:
            print 'error'
            print ordencompra_form.errors, len(ordencompra_form.errors)
    else:

        ordencompra_form = OrdenCompraForm
        productos = Producto.objects.exclude(tipo_producto=2)
        iva = Parametros.objects.get(clave='iva')

    return render_to_response('ordenescompra/create.html',
                              {'ordencompra_form': ordencompra_form,'productos':productos, 'iva': iva},
                              RequestContext(request))


# =====================================================#
@login_required()
@transaction.atomic
def OrdenCompraUpdateView(request, pk):
    if request.method == 'POST':
        ordencompra = OrdenCompra.objects.get(compra_id=pk)
        ordencompra_form = OrdenCompraForm(request.POST, request.FILES, instance=ordencompra)
        print ordencompra_form.is_valid(), ordencompra_form.errors, type(ordencompra_form.errors)

        if ordencompra_form.is_valid():
            with transaction.atomic():
                new_orden = ordencompra_form.save()
                new_orden.nro_fact_proveedor = request.POST["nro_fact_proveedor"]
                new_orden.subtotal = request.POST["total23"]
                new_orden.total = request.POST["total_g"]
                new_orden.dscto_pciento = request.POST["porcentaje_descuento"]
                new_orden.dscto_monto = request.POST["descuento"]
                new_orden.impuesto_pciento = request.POST["porcentaje_iva"]
                new_orden.subtotal_descuento = request.POST["subtotal_desc"]
                new_orden.impuesto_monto = request.POST["iva"]

                new_orden.save()

                contador = request.POST["columnas_receta"]
                print contador
                i = 1
                while int(i) <= int(contador):

                    if int(i) > int(contador):
                        print('entrosd')
                        break
                    else:
                        product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
                        detalle_id = request.POST["id_detalle" + str(i)]
                # if detalle_id:
                #             detallecompra = ComprasDetalle.objects.get(compras_detalle_id=detalle_id)
                #             detallecompra.updated_by = request.user.get_full_name()
                #             #detallecompra.updated_at = datetime.now()

                #             detallecompra.save()
                #             nd=detallecompra.save()
                #             i+= 1
                #             print('entro holaaaa'+str(nd.compra_id))
                #             if 'recibido_kits'+str(i) in request.POST:
                #             	print('entrorecibido')
                #             	nd.recibido=request.POST["recibido_kits"+str(i)]
                #             	nd.save()
                #             	kardez = Kardex.objects.get(modulo=detalle_id)
                #             	if kardez:
                #             		print('ya existe')
                #             	else:
                #             		k=Kardex()
                #             		k.nro_documento =new_orden.nro_compra
                #             		k.producto=product
                #             		k.cantidad=nd.cantidad
                #             		k.descripcion='Orden de Compra'
                #             		k.costo=nd.precio_compra
                #             		k.bodega=new_orden.bodega
                #             		k.modulo=detalle_id
                #             		k.fecha_ingreso=datetime.now()
                #             		k.save()

                #         else:
                #             comprasdetalle=ComprasDetalle()
                #             comprasdetalle.compra_id = new_orden.compra_id
                #             comprasdetalle.producto=product
                #             comprasdetalle.proveedor=new_orden.proveedor
                #             comprasdetalle.bodega=new_orden.bodega
                #             comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                #             #kits.costo=float(request.POST["costo_kits1"])
                #             comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                #             comprasdetalle.total=request.POST["total_kits"+str(i)]
                #             comprasdetalle.save()
                #             i+= 1
                #             print('No Tiene detalle'+str(i))
                #             print('contadorsd prueba'+str(contador))
                # #ordencompra_form=OrdenCompraForm(request.POST)
                print('El id de la compra' + str(pk))
                detalle = ComprasDetalle.objects.filter(compra_id=pk)

                context = {
                    'section_title': 'Actualizar Orden Compra',
                    'button_text': 'Actualizar',
                    'ordencompra_form': ordencompra_form,
                    'detalle': detalle}

                return render_to_response(
                    'ordenescompra/factura.html',
                    context,
                    context_instance=RequestContext(request))
        else:

            ordencompra_form = OrdenCompraForm(request.POST)
            detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)

            context = {
                'section_title': 'Actualizar Orden Compra',
                'button_text': 'Actualizar',
                'ordencompra_form': ordencompra_form,
                'detalle': detalle}

        return render_to_response(
            'ordenescompra/factura.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordencompra = OrdenCompra.objects.get(compra_id=pk)
        ordencompra_form = OrdenCompraForm(instance=ordencompra)
        detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)

        context = {
            'section_title': 'Actualizar Orden Compra',
            'button_text': 'Actualizar',
            'ordencompra_form': ordencompra_form,
            'detalle': detalle}

        return render_to_response(
            'ordenescompra/factura.html',
            context,
            context_instance=RequestContext(request))


# =====================================================#
@login_required()
def ordenescompraEliminarView(request):
    return eliminarView(request, OrdenCompra, 'ordenescompra-list')


# =====================================================#
@login_required()
def ordenescompraEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, OrdenCompra)


# MUEDIRSA
def OrdenCompraListAprobarView(request):

    ordenesdecompras = OrdenCompra.objects.all()
    return render_to_response('ordenescompra/aprobada.html', {'ordenesdecompras': ordenesdecompras},
                              RequestContext(request))


    # model = OrdenCompra
    # paginate_by = 100
    # template_name = 'ordenescompra/aprobada.html'
    # table_class = OrdenCompraAprobadaTable
    # filter_class = OrdenCompraAprobadaFilter
    # context_object_name = 'ordenesdecompras'
    #
    # def get_context_data(self, **kwargs):
    #     context = super(OrdenCompraListAprobarView, self).get_context_data(**kwargs)
    #     context['url_delete'] = reverse_lazy('ordencompra-delete')
    #     return context


# =====================================================#
@login_required()
def ordenescompraAprobarByPkView(request, pk):
    objetos = OrdenCompra.objects.filter(compra_id=pk)
    for obj in objetos:
        obj.aprobada = True
        obj.save()

    return HttpResponseRedirect('/OrdenesdeCompra/OrdenesdeCompraAprobar')


@login_required()
def aprobarByPkView(request, pk):
    try:
        aprobar(request, pk, OrdenCompra)
    except Exception as e:
        # Tools.manejadorErrores(e)
        messages.error(request, 'Ocurrio un Error.')

    return HttpResponse('')


# =====================================================#
@login_required()
def aprobar(request, ids, Model):
    objetos = Model.objects.filter(id__in=ids)
    for obj in objetos:
        obj.aprobada = True
        obj.save()
    # obj.delete()
    if not objetos:
        messages.error(request, 'Los Datos Predeterminados No Pueden ser Eliminados.')
        return 0
    return 1


class OrdenCreateView(ObjectCreateView):
    model = OrdenCompra
    form_class = OrdenCompraForm
    template_name = 'ordenescompra/orden_form.html'
    url_success = 'ordencompra-list'
    url_success_other = 'ordencompra-create'
    url_cancel = 'ordencompra-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(OrdenCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva ordendecompra."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


@login_required()
@transaction.atomic
def OrdenNuevoView(request):
    if request.method == 'POST':
        ordencompra_form = OrdenCompraForm(request.POST)
        productos = Producto.objects.all()

        if ordencompra_form.is_valid():
            with transaction.atomic():
                new_orden = ordencompra_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.total = request.POST["total"]

                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='ordenesdecompra')
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
                            comprasdetalle = ComprasDetalle()
                            comprasdetalle.compra_id = new_orden.compra_id
                            comprasdetalle.producto = product
                            comprasdetalle.proveedor = new_orden.proveedor
                            comprasdetalle.bodega = new_orden.bodega
                            comprasdetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                            # kits.costo=float(request.POST["costo_kits1"])
                            comprasdetalle.precio_compra = request.POST["costo_kits" + str(i)]
                            comprasdetalle.total = request.POST["total_kits" + str(i)]
                            comprasdetalle.save()

                    print(i)
                    print('contadorsd prueba' + str(contador))

            return HttpResponseRedirect('/OrdenesdeCompra/OrdenesdeCompra')
        else:
            print 'error'
            print ordencompra_form.errors, len(ordencompra_form.errors)
    else:
        ordencompra_form = OrdenCompraForm
        productos = Producto.objects.all()

    return render_to_response('ordenescompra/create1.html',
                              {'ordencompra_form': ordencompra_form, 'productos': productos}, RequestContext(request))
@login_required()
def ComprasLocalesListView(request):
    
    compraslocales = ComprasLocales.objects.all()
    return render_to_response('compraslocales/list.html', {'compraslocales': compraslocales},RequestContext(request))
   

@login_required()
@transaction.atomic
def ComprasLocalesCreateView(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        compraslocales_form = ComprasLocalesForm(request.POST)
        productos = Producto.objects.all()

        if compraslocales_form.is_valid():
            with transaction.atomic():
                new_orden = compraslocales_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.subtotal = request.POST["subtotal"]
                new_orden.iva = request.POST["iva"]
                new_orden.total = request.POST["total"]
                new_orden.orden_compra_id = request.POST["orden_compra_id"]
                new_orden.recibida = request.POST["recibo"]

                new_orden.dscto_pciento = request.POST["porcentaje_descuento"]
                new_orden.dscto_monto = request.POST["descuento"]
                new_orden.iva_pciento = request.POST["porcentaje_iva"]
                new_orden.subtotal_descuento = request.POST["subtotal_desc"]
                new_orden.save()
                documento = DocumentoCompra()
                documento.created_by = request.user.get_full_name()
                documento.updated_by = request.user.get_full_name()
                documento.created_at = datetime.now()
                documento.updated_at = datetime.now()
                documento.fecha_emision = new_orden.fecha
                documento.fecha_vencimiento = new_orden.fecha
                documento.proveedor = new_orden.proveedor
                documento.orden_compra_id = new_orden.orden_compra_id
                documento.establecimiento = new_orden.proveedor.establecimiento
                documento.punto_emision = new_orden.proveedor.establecimiento
                documento.no_afecta=True
                if new_orden.nro_fact_proveedor:
                    documento.secuencial = new_orden.nro_fact_proveedor
                else:
                    documento.secuencial = new_orden.recibida
                documento.autorizacion = new_orden.proveedor.autorizacion_sri
                documento.descripcion = new_orden.comentario
                # documento.base_iva_0 =
                # documento.base_iva =
                documento.base_iva = new_orden.subtotal
                documento.valor_iva = new_orden.iva
                documento.porcentaje_iva = new_orden.iva_pciento
                # documento.base_ice =
                # documento.valor_ice =
                # documento.porcentaje_ice =
                documento.descuento = new_orden.dscto_monto
                documento.total = new_orden.total
                # documento.tipo_provision = cleaned_data.get('tipo_provision')
                documento.pagado = False
                documento.generada = True
                documento.compra_id=new_orden.id
                documento.save()


                objet = OrdenCompra.objects.filter(compra_id=request.POST["orden_compra_id"])
                for ob in objet:
                    ob.facturada = True
                    ob.save()

                objetos = ComprasDetalle.objects.filter(compra_id=request.POST["orden_compra_id"])
                print('Cantidad de objetos en la compra detalle')
                print len(objetos)
                for obj in objetos:
                    obj.recibido = True
                    obj.save()
                    documento_detalle = DocumentosCompraDetalle()
                    documento_detalle.documento_compra_id = int(documento.id)
                    documento_detalle.producto_id = obj.producto_id
                    documento_detalle.descripcion = obj.producto.descripcion_producto
                    # documento_detalle.base_iva_0 = producto['producto_id']
                    # documento_detalle.valor_iva_0 = producto['producto_id']
                    # documento_detalle.base_iva = producto['precio']
                    # documento_detalle.valor_iva = producto['precio']
                    # documento_detalle.porcentaje_iva = cleaned_data.get('porcentaje_iva')
                    documento_detalle.base_ice = 0
                    documento_detalle.valor_ice = 0
                    documento_detalle.porcentaje_ice = 0
                    documento_detalle.descuento = 0
                    documento_detalle.cantidad = obj.cantidad
                    documento_detalle.save()

                    id = obj.compras_detalle_id
                    print id

                    #Obtenemos las unidades actuales para obtener el costo promedio

                    lcSql = "SELECT A.cantidad, B.costo_promedio "
                    lcSql += "from producto_en_bodega A "
                    lcSql += "inner join producto B on (A.producto_id = B.producto_id) "
                    lcSql += "where B.producto_id = " + str(obj.producto_id) + " "
                    lcSql += "and A.bodega_id = " + str(obj.bodega_id)

                    cursor.execute(lcSql)
                    costosp = cursor.fetchall()
                    oStock = 0
                    oCosto = 0
                    oCostoP = 0
                    for row in costosp:
                        if row[0]:
                            oStock = row[0]
                        if row[1]:
                            oCosto = row[1]

                    #Sumarizamos las unidades existentes + las unidades compradas
                    oInvVal = oStock * oCosto
                    oCompra = obj.precio_compra * obj.cantidad
                    oUnidad = oStock + obj.cantidad
                    oTotal = oInvVal + oCompra
                    oCostoP = oTotal / oUnidad

                    try:
                        product = Producto.objects.get(producto_id=obj.producto_id)
                    except Producto.DoesNotExist:
                        product = None
                    if product:
                        product.costo=obj.precio_compra
                        product.costo_promedio=oCostoP
                        product.save()
                        print ("Se actualizo el producto")

                    new_orden_compra = OrdenCompra.objects.get(compra_id=obj.compra_id)
                    try:
                        kardez = Kardex.objects.filter(modulo=id).filter(nro_documento=new_orden_compra.nro_compra).filter(producto_id=obj.producto_id).filter(fecha_ingreso=datetime.now())
                    except Kardex.DoesNotExist:
                        kardez = None

                    if kardez:
                        print('ya existe')
                        print len(kardez)
                    else:
                        print ('No existe cardex del detalle_id' + str(id)+'CCompra No.'+str(new_orden_compra.nro_compra))

                        k = Kardex()
                        k.nro_documento = new_orden_compra.nro_compra
                        k.producto = obj.producto
                        k.cantidad = obj.cantidad
                        k.descripcion = 'Ingreso a Bodega de Materia Prima'

                        #Costo Promedio no puede ser 0, dejamos el costo ultima compra como Promedio
                        k.costo = obj.precio_compra

                        # if (oCostoP == 0):
                        #     k.costo = obj.precio_compra
                        # else:
                        #     k.costo = oCostoP

                        k.bodega = new_orden_compra.bodega
                        k.modulo = id
                        k.un_doc_soporte='Orden de Compra No.'+str(new_orden_compra.nro_compra)+' Compra Local No.'+str(new_orden.codigo)
                        #k.fecha_ingreso = datetime.now()
                        k.fecha_ingreso = new_orden.fecha
                        k.save()

                    prod1 = ProductoEnBodega.objects.filter(producto_id=obj.producto_id).filter(bodega_id=obj.bodega_id)

                    if prod1:
                        for prod in prod1:
                            prod.cantidad = float(prod.cantidad) + float(obj.cantidad)
                            prod.updated_at = new_orden.fecha
                            prod.updated_by = request.user.get_full_name()
                            prod.save()
                    else:
                        k = ProductoEnBodega()
                        k.producto_id = obj.producto_id
                        k.bodega_id = obj.bodega_id
                        k.cantidad = obj.cantidad
                        k.created_by = request.user.get_full_name()
                        k.updated_by = request.user.get_full_name()
                        k.created_at = new_orden.fecha
                        k.updated_at = datetime.now()
                        k.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='compraslocales')
                    secuencial.secuencial = secuencial.secuencial + 1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = datetime.now()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None


            return HttpResponseRedirect('/OrdenesdeCompra/comprasLocales')
        else:
            print 'error'
            print compraslocales_form.errors, len(compraslocales_form.errors)
    else:
        compraslocales_form = ComprasLocalesForm
        productos = Producto.objects.all()

    return render_to_response('compraslocales/create.html',
                              {'compraslocales_form': compraslocales_form, 'productos': productos},
                              RequestContext(request))


@login_required()
@transaction.atomic

def ComprasLocalesUpdateView(request, pk):
    if request.method == 'POST':
        ordencompra = ComprasLocales.objects.get(id=pk)
        orden = OrdenCompra.objects.get(compra_id=ordencompra.orden_compra_id)
        ordencompra_form = ComprasLocalesForm(request.POST, request.FILES, instance=ordencompra)
        print ordencompra_form.is_valid(), ordencompra_form.errors, type(ordencompra_form.errors)

        if ordencompra_form.is_valid():
            with transaction.atomic():
                new_orden = ordencompra_form.save()
                new_orden.nro_fact_proveedor = request.POST["nro_fact_proveedor"]
                new_orden.save()

                contador = request.POST["columnas_receta"]
                print contador
                i = 1

                print('El id de la compra' + str(pk))
                detalle = ComprasDetalle.objects.filter(compra_id=new_orden.orden_compra_id)

                context = {
                    'section_title': 'Actualizar Orden Compra',
                    'button_text': 'Actualizar',
                    'ordencompra_form': ordencompra_form,
                    'detalle': detalle,
                    'orden': orden,
                }

                return render_to_response(
                    'compraslocales/actualizar.html',
                    context,
                    context_instance=RequestContext(request))
        else:

            ordencompra_form = ComprasLocalesForm(request.POST)
            detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.orden_compra_id)
            orden = OrdenCompra.objects.get(compra_id=ordencompra.orden_compra_id)

            context = {
                'section_title': 'Actualizar Compras Locales',
                'button_text': 'Actualizar',
                'ordencompra_form': ordencompra_form,
                'detalle': detalle,
                'orden': orden,}

        return render_to_response(
            'compraslocales/actualizar.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordencompra = ComprasLocales.objects.get(id=pk)
        ordencompra_form = ComprasLocalesForm(instance=ordencompra)
        detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.orden_compra_id)
        orden = OrdenCompra.objects.get(compra_id=ordencompra.orden_compra_id)

        context = {
            'section_title': 'Actualizar Orden Compra',
            'button_text': 'Actualizar',
            'ordencompra_form': ordencompra_form,
            'detalle': detalle,
            'orden': orden,}

        return render_to_response(
            'compraslocales/actualizar.html',
            context,
            context_instance=RequestContext(request))


@login_required()
@transaction.atomic
def OrdenesComprasLocalesCreateView(request, pk):
    if request.method == 'POST':
        cursor = connection.cursor()
        compraslocales_form = ComprasLocalesForm(request.POST)
        productos = Producto.objects.all()

        if compraslocales_form.is_valid():
            with transaction.atomic():
                new_orden = compraslocales_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.subtotal = request.POST["subtotal"]
                new_orden.iva = request.POST["iva"]
                new_orden.total = request.POST["total"]
                new_orden.orden_compra_id = request.POST["orden_compra_id"]

                new_orden.dscto_pciento = request.POST["porcentaje_descuento"]
                new_orden.dscto_monto = request.POST["descuento"]
                new_orden.iva_pciento = request.POST["porcentaje_iva"]
                new_orden.subtotal_descuento = request.POST["subtotal_desc"]
                new_orden.save()
                objet = OrdenCompra.objects.filter(compra_id=request.POST["orden_compra_id"])
                for ob in objet:
                    ob.facturada = True
                    ob.save()

                objetos = ComprasDetalle.objects.filter(compra_id=request.POST["orden_compra_id"])
                for obj in objetos:
                    obj.recibido = True
                    obj.save()
                    id = obj.compras_detalle_id
                    try:
                        kardez = Kardex.objects.filter(modulo=id)
                    except Kardex.DoesNotExist:
                        kardez = None
                    if kardez.exists():
                        print('ya existe')
                    else:
                        new_orden_compra = OrdenCompra.objects.get(compra_id=obj.compra_id)
                        k = Kardex()
                        k.nro_documento = new_orden_compra.nro_compra
                        k.producto = obj.producto
                        k.cantidad = obj.cantidad
                        k.descripcion = 'Ingreso a Bodega de Materia Prima'
                        k.costo = obj.precio_compra
                        k.bodega = new_orden_compra.bodega
                        k.modulo = id
                        k.fecha_ingreso = datetime.now()
                        k.save()

                    prod1 = ProductoEnBodega.objects.filter(producto_id=obj.producto_id).filter(bodega_id=obj.bodega_id)
                    if prod1:
                        for prod in prod1:
                            prod.cantidad = float(prod.cantidad) + float(obj.cantidad)
                            prod.updated_at = datetime.now()
                            prod.updated_by = request.user.get_full_name()
                            prod.save()
                    else:
                        k = ProductoEnBodega()
                        k.producto_id = obj.producto_id
                        k.bodega_id = obj.bodega_id
                        k.cantidad = obj.cantidad
                        k.created_by = request.user.get_full_name()
                        k.updated_by = request.user.get_full_name()
                        k.created_at = datetime.now()
                        k.updated_at = datetime.now()
                        k.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='compraslocales')
                    secuencial.secuencial = secuencial.secuencial + 1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = datetime.now()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None

            return HttpResponseRedirect('/OrdenesdeCompra/comprasLocales')
        else:
            print 'error'
            print compraslocales_form.errors, len(compraslocales_form.errors)
    else:
        compraslocales_form = ComprasLocalesForm
        productos = Producto.objects.all()
        detalle = ComprasDetalle.objects.filter(compra_id=pk)
        orden = OrdenCompra.objects.get(compra_id=pk)

    return render_to_response('ordenescompra/compraslocalescreate.html',
                              {'compraslocales_form': compraslocales_form, 'productos': productos, 'detalle': detalle,
                               'orden': orden}, RequestContext(request))


def index(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    orden = ComprasLocales.objects.get(id=pk)
    detalle = ComprasDetalle.objects.filter(compra_id=orden.orden_compra_id)
    html = loader.get_template('compraslocales/imprimir.html')
    context = RequestContext(request, {'orden': orden, 'detalle': detalle})
    return HttpResponse(html.render(context))


def generar_pdf(html):
    # Funci?n para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


@login_required()
def indexOrdenCompra(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    orden = OrdenCompra.objects.get(compra_id=pk)
    detalle = ComprasDetalle.objects.filter(compra_id=orden.compra_id)

    html = render_to_string('ordenescompra/imprimir.html', {'pagesize': 'A4', 'orden': orden, 'detalle': detalle},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


@login_required()
@csrf_exempt
def obtenerPrecioProducto(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        tipo = request.POST.get('tipo')

        objetos = Producto.objects.get(producto_id=id)
        costo = 0
        if tipo == '1':
            costo = objetos.precio1
        if tipo == '2':
            costo = objetos.precio2
        if tipo == '3':
            costo = objetos.precio3

        return HttpResponse(
            costo
        )
    else:
        raise Http404


# =====================================================#
class OrdenCompraActualizarView(ObjectUpdateView):
    def get(self, request, *args, **kwargs):

        ordencompra = OrdenCompra.objects.get(compra_id=kwargs['pk'])
        productos = Producto.objects.all()
        ordencompra_form = OrdenCompraForm(instance=ordencompra)
        detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)

        context = {
            'section_title': 'Actualizar Presupuesto',
            'button_text': 'Actualizar',
            'ordencompra_form': ordencompra_form,
            'productos': productos,
            'detalle': detalle
        }
        print('ENTROO')

        return render_to_response(
            'ordenescompra/actualizar.html', context, context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        ordencompra = OrdenCompra.objects.get(compra_id=kwargs['pk'])
        ordencompra_form = OrdenCompraForm(request.POST, request.FILES, instance=ordencompra)
        p_id = kwargs['pk']
        print(p_id)
        print ordencompra_form.is_valid(), ordencompra_form.errors, type(ordencompra_form.errors)
        productos = Producto.objects.all()
        print('HOLAAAA')

        if ordencompra_form.is_valid():
            new_orden = ordencompra_form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            new_orden.subtotal = request.POST["total23"]
            new_orden.total = request.POST["total_g"]
            new_orden.dscto_pciento = request.POST["porcentaje_descuento"]
            new_orden.dscto_monto = request.POST["descuento"]
            new_orden.impuesto_pciento = request.POST["porcentaje_iva"]
            new_orden.subtotal_descuento = request.POST["subtotal_desc"]
            new_orden.impuesto_monto = request.POST["iva"]
            print ('Tiene impto' + str(request.POST["iva"]))
            new_orden.save()

            contador = request.POST["columnas_receta"]

            i = 0
            while int(i) <= int(contador):
                i += 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
		    print('contadorsd inicial' + str(contador))
                    if 'id_kits' + str(i) in request.POST:
			print('el valor de i' + str(i))

                        product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
                        #detalle_id = request.POST["id_detalle" + str(i)]

                        if "id_detalle" + str(i) in request.POST:
			    detalle_id = request.POST["id_detalle" + str(i)]
                            detallecompra = ComprasDetalle.objects.get(compras_detalle_id=detalle_id)
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto = product
                            detallecompra.cantidad = request.POST["cantidad_kits" + str(i)]
                            detallecompra.precio_compra = request.POST["costo_kits" + str(i)]
                            detallecompra.total = request.POST["total_kits" + str(i)]
			    detallecompra.tipo_precio = request.POST["tipo_precio_kits" + str(i)]
			    detallecompra.updated_at = datetime.now()
			    detallecompra.recibido = request.POST.get("recibido_kits" + str(i), False)
			    detallecompra.save()
			    print('Tiene detalle' + str(i))
			else:
			    comprasdetalle = ComprasDetalle()
			    comprasdetalle.compra_id = new_orden.compra_id
			    comprasdetalle.producto = product
			    comprasdetalle.proveedor = new_orden.proveedor
			    comprasdetalle.bodega = new_orden.bodega
			    comprasdetalle.cantidad = request.POST["cantidad_kits" + str(i)]
			    comprasdetalle.tipo_precio = request.POST["tipo_precio_kits" + str(i)]
			    comprasdetalle.precio_compra = request.POST["costo_kits" + str(i)]
			    comprasdetalle.total = request.POST["total_kits" + str(i)]
			    comprasdetalle.save()
			    #i += 1
			    print('No Tiene detalle' + str(i))
			    print('contadorsd prueba' + str(contador))
            # ordencompra_form=OrdenCompraForm(request.POST)
            ordencompra = OrdenCompra.objects.get(compra_id=kwargs['pk'])
            ordencompra_form = OrdenCompraForm(instance=ordencompra)

            detalle = ComprasDetalle.objects.filter(compra_id=p_id)
            productos = Producto.objects.all()

            context = {
                'section_title': 'Actualizar Orden Compra1',
                'button_text': 'Actualizar',
                'ordencompra_form': ordencompra_form,
                'ordencompra': ordencompra,
                'detalle': detalle,
                'productos': productos,
                'mensaje': 'Orden de Compra actualizada con exito'}

            return render_to_response(
                'ordenescompra/actualizar.html',
                context,
                context_instance=RequestContext(request))
        else:

            ordencompra = OrdenCompra.objects.get(compra_id=kwargs['pk'])
            ordencompra_form = OrdenCompraForm(instance=ordencompra)
            detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)
            productos = Producto.objects.all()

            context = {
                'section_title': 'Actualizar Orden Compra2',
                'button_text': 'Actualizar',
                'ordencompra_form': ordencompra_form,
                'ordencompra': ordencompra,
                'detalle': detalle,
                'mensaje': 'Orden de Compra actualizada con exito'}

        return render_to_response(
            'ordenescompra/actualizar.html',
            context,
            context_instance=RequestContext(request))

@login_required()
@csrf_exempt
def compras_locales_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order=request.GET['order[0][column]']
        _order_dir=request.GET['order[0][dir]']
        cursor = connection.cursor()
        sql=" select cl.id,cl.codigo,cl.fecha,o.nro_compra,p.nombre_proveedor,cl.subtotal,cl.total,cl.anulado from compras_locales cl left join proveedor p on p.proveedor_id=cl.proveedor_id left join orden_compra o on o.compra_id=cl.orden_compra_id where 1=1 "
        if _search_value:
            sql+=" and UPPER(p.nombre_proveedor) like '%"+_search_value+"%' or UPPER(cl.codigo) like '%"+_search_value.upper()+"%'  or CAST(o.nro_compra as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(cl.total as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(cl.subtotal as VARCHAR)  like '%"+_search_value.upper()+"%' or CAST(cl.fecha as VARCHAR)  like '%"+_search_value+"%' or UPPER(cl.codigo) like '%"+_search_value.upper()+"%'"
        
        if _search_value.upper()=='ANULADO'  or _search_value.upper()=='AN' or _search_value.upper()=='ANU' or _search_value.upper()=='ANUL'  or _search_value.upper()=='ANULA' or _search_value.upper()=='ANULAD':
            sql+=" or cl.anulado is True"
        
        if _search_value.upper()=='FINALIZADO' or _search_value.upper()=='FIN' or _search_value.upper()=='FINA' or _search_value.upper()=='FINAL' or _search_value.upper()=='FINALI' or _search_value.upper()=='FINALIZ' or _search_value.upper()=='FINALIZA' or _search_value.upper()=='FINALIZAD':
            sql+=" or cl.anulado is not True"
           
    
        #sql +=" order by fecha"
        print _order
        if _order == '0':
            sql +=" order by cl.codigo "+_order_dir
        if _order == '1':
            sql +=" order by cl.fecha "+_order_dir
        if _order == '2':
            sql +=" order by o.nro_compra "+_order_dir
        
        if _order == '3':
            sql +=" order by p.nombre_proveedor "+_order_dir
        
        if _order == '4':
            sql +=" order by cl.subtotal "+_order_dir
        if _order == '5':
            sql +=" order by cl.total "+_order_dir
        if _order == '6':
            
            sql +=" order by cl.anulado "+_order_dir
        print sql
        cursor.execute(sql)
        compras = cursor.fetchall()
            
        compras_filtered = compras[_start:_start + _end]

        compras_list = []
        for o in compras_filtered:
            compras_obj = []
            compras_obj.append(o[1])
            if o[2]:
                compras_obj.append(o[2].strftime('%Y-%m-%d'))
            else:
                compras_obj.append('')
            compras_obj.append(o[3])
            compras_obj.append(o[4])
            compras_obj.append(o[5])
            compras_obj.append(o[6])
            html=''

            if o[7]:
                compras_obj.append("Anulado")
                html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/OrdenesdeCompra/comprasLocales/'+str(o[0])+'/imprimir" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-print"></i></button></a>'
                
                

            else:
                compras_obj.append("Finalizado")
                html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/OrdenesdeCompra/comprasLocales/'+str(o[0])+'/imprimir" style=""><button type="button" class="btn btn-default btn-xs"><i class="fa fa-print"></i></button></a>'
            
           
            
            

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