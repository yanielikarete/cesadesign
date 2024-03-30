# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, eliminarByPkView,cambiarEstadoByPkView
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
from config.models import *
from django.template import RequestContext, loader

from login.lib.tools import Tools

from config.models import Mensajes
from django.template import RequestContext
from django.forms.extras.widgets import *
from django.contrib import auth
from django.views.generic import TemplateView,UpdateView

from django import forms

from django.forms.extras.widgets import *
from django.contrib.auth import authenticate,login
from inventario.tables import *
#from login.lib.tools import Tools
from inventario.models import *



class ReunionListView(ObjectListView):
    model = Reunion
    paginate_by = 100
    template_name = 'reunion/index.html'
    table_class = ReunionTable
    filter_class = ReunionFilter
    context_object_name = 'reuniones'
    def get_context_data(self, **kwargs):
        context = super(ReunionListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('reunion-delete')
        return context

class ReunionCotizacionBodegaListView(ObjectListView):
    model = Reunion
    paginate_by = 100
    template_name = 'reunion/cotizacion.html'
    table_class = ReunionTable
    filter_class = ReunionFilter
    context_object_name = 'reuniones'

    def get_context_data(self, **kwargs):
        context = super(ReunionCotizacionBodegaListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('reunion-delete')
        return context
#=====================================================#
class ReunionDetailView(ObjectDetailView):
    model = Reunion
    template_name = 'reunion/detail.html'

#=====================================================#
class ReunionCreateView(ObjectCreateView):
    model = Reunion
    form_class = ReunionForm
    template_name = 'reunion/create.html'
    url_success = 'reunion-list'
    url_success_other = 'reunion-create'
    url_cancel = 'reunion-list'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user.get_full_name()
        self.object.created_by = self.request.user.get_full_name()
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        
        objetos = Secuenciales.objects.get(modulo = 'reunion')
        
        modulo_secuencial = objetos.secuencial+1
        objetos.secuencial=modulo_secuencial
        objetos.save()

        notificacion = Notificaciones()
        notificacion.user_id = self.request.user.id
        notificacion.mensaje = "Se ha creado una nueva reunion con el codigo " + str(
            self.object.codigo) + " el dia " + str(self.object.fecha) + " con el cliente " + str(
            self.object.cliente) + " a cargo del vendedor " + str(self.object.vendedor) + " " + str(self.object.motivo)
        notificacion.url = "reunion/reunion/"
        notificacion.updated_by = self.request.user.get_full_name()
        notificacion.created_by = self.request.user.get_full_name()
        notificacion.created_at = datetime.now()
        notificacion.updated_at = datetime.now()
        notificacion.save()

        notificacion = Notificaciones()
        notificacion.group_id = 12
        notificacion.mensaje = "Se ha creado una nueva reunion con el codigo " + str(
            self.object.codigo) + " el dia " + str(self.object.fecha) + " con el cliente " + str(
            self.object.cliente) + " a cargo del vendedor " + str(self.object.vendedor) + " " + str(self.object.motivo)
        notificacion.url = "reunion/reunion/"
        notificacion.updated_by = self.request.user.get_full_name()
        notificacion.created_by = self.request.user.get_full_name()
        notificacion.created_at = datetime.now()
        notificacion.updated_at = datetime.now()
        notificacion.save()

        notificacion = Notificaciones()
        notificacion.group_id = 14
        notificacion.mensaje = "Se ha creado una nueva reunion con el codigo " + str(
            self.object.codigo) + " el dia " + str(self.object.fecha) + " con el cliente " + str(
            self.object.cliente) + " a cargo del vendedor " + str(self.object.vendedor) + " " + str(self.object.motivo)
        notificacion.url = "reunion/reunion/"
        notificacion.updated_by = self.request.user.get_full_name()
        notificacion.created_by = self.request.user.get_full_name()
        notificacion.created_at = datetime.now()
        notificacion.updated_at = datetime.now()
        notificacion.save()

        return super(ReunionCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva reunion."
        messages.success(self.request, mensaje)






        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#

def ReunionUpdateView(request,pk):
    if request.method == 'POST':
        reunion=Reunion.objects.get(compra_id=pk)
        reunion_form=OrdenCompraForm(request.POST,request.FILES,instance=ordencompra)
        print reunion_form.is_valid(), ordencompra_form.errors, type(ordencompra_form.errors)

        if ordencompra_form.is_valid():
            new_orden=ordencompra_form.save()
            new_orden.nro_fact_proveedor=request.POST["nro_fact_proveedor"]
            new_orden.save()
            

            contador=request.POST["columnas_receta"]
            print contador
            i=1
            while int(i) <= int(contador):
              
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                    detalle_id=request.POST["id_detalle"+str(i)]
            #         if detalle_id:
            #             detallecompra = ComprasDetalle.objects.get(compras_detalle_id=detalle_id)
            #             detallecompra.updated_by = request.user.get_full_name()
            #             #detallecompra.updated_at = datetime.now()
                        
            #             detallecompra.save()
            #             nd=detallecompra.save()
            #             i+= 1
            #             print('entro holaaaa'+str(nd.compra_id))
            #             if 'recibido_kits'+str(i) in request.POST:
            #               print('entrorecibido')
            #               nd.recibido=request.POST["recibido_kits"+str(i)]
            #               nd.save()
            #               kardez = Kardex.objects.get(modulo=detalle_id)
            #               if kardez:
            #                   print('ya existe')
            #               else:
            #                   k=Kardex()
            #                   k.nro_documento =new_orden.nro_compra
            #                   k.producto=product
            #                   k.cantidad=nd.cantidad
            #                   k.descripcion='Orden de Compra'
            #                   k.costo=nd.precio_compra
            #                   k.bodega=new_orden.bodega
            #                   k.modulo=detalle_id
            #                   k.fecha_ingreso=datetime.now()
            #                   k.save()

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
            print('El id de la compra'+str(pk))
            detalle = ComprasDetalle.objects.filter(compra_id=pk)
           
            context = {
           'section_title':'Actualizar Orden Compra',
            'button_text':'Actualizar',
            'ordencompra_form':ordencompra_form,
            'detalle':detalle }


            return render_to_response(
                'ordenescompra/factura.html', 
                context,
                context_instance=RequestContext(request))
        else:
    
            ordencompra_form=OrdenCompraForm(request.POST)
            detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)
           
            context = {
            'section_title':'Actualizar Orden Compra',
            'button_text':'Actualizar',
            'ordencompra_form':ordencompra_form,
            'detalle':detalle }

        return render_to_response(
            'ordenescompra/factura.html', 
            context,
            context_instance=RequestContext(request))
    else:
        ordencompra=OrdenCompra.objects.get(compra_id=pk)
        ordencompra_form=OrdenCompraForm(instance=ordencompra)
        detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)
           
        context = {
            'section_title':'Actualizar Orden Compra',
            'button_text':'Actualizar',
            'ordencompra_form':ordencompra_form,
            'detalle':detalle }

        return render_to_response(
            'ordenescompra/factura.html', 
            context,
            context_instance=RequestContext(request))




#=====================================================#
@login_required()
def ReunionEliminarView(request):
    return eliminarView(request, Reunion, 'reunion-list')

#=====================================================#
@login_required()
def ReunionEliminarByPkView(request, pk):
    objetos = Reunion.objects.filter(id__in = pk)
    for obj in objetos:
        if obj.activo:
            obj.activo = False
        else:
            obj.activo= True

        obj.save()

    return HttpResponseRedirect('/reunion/reunion')

#======================================================#
@login_required()
@csrf_exempt
def misReunionGuardar(request):
    item = {'exito':0}
    if request.method == 'POST':
        try:
           
            reuniones = request.POST['data']
            reuniones = json.loads(reuniones)
           
            for reunion in reuniones:
                if not alumno['codigo'] == "" :
                    try:
                            a = Reunion()
                            a.codigo = reunion['codigo']
                            a.nombre = reunion['nombre']
			    a.created_by = request.user
                            a.updated_at = datetime.now()
                            a.save()
                       
                    except:
                        messages.error(request, "Oh, No se pudo guardar la reunion")
                        pass

                    item = {'exito':1}

            if item['exito'] == 1:
                messages.info(request, 'Reunion guardadas!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito':0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')

def SubirImagenesReunionView(request):
    if request.method == 'POST':
        form=ImagenesReunionForm(request.POST)
        

        if form.is_valid():
            new_orden=form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            #new_orden.imagenes_reunion_id = pk
            #new_orden.imagen=request.FILES["imagen"]

            new_orden.save()

            detalle=ImagenesReunionDetalle()
            detalle.imagenes_reunion_id = new_orden.id
            detalle.descripcion=request.POST["descripcion_imagen"]
            detalle.imagen=request.FILES["imagen_reunion"]
            detalle.save()
            imagenesreunion = ImagenesReunion.objects.get(id=new_orden.id)

            form=ImagenesReunionForm(instance=imagenesreunion)
            detalle = ImagenesReunionDetalle.objects.filter(imagenes_reunion_id=new_orden.id)
            return HttpResponseRedirect('/reunion/reunion/'+str(new_orden.id)+'/editarSubirImagen/')


        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form=ImagenesReunionForm
       

        
        return render_to_response('reunion_imagenes/subir_imagenes.html', { 'form': form},  RequestContext(request))
def SubirImagenesReunionActualizarView(request,pk):
    if request.method == 'POST':
        imagenesreunion = ImagenesReunion.objects.get(id=pk)
        form = ImagenesReunionForm(request.POST,request.FILES,instance=imagenesreunion)
        p_id=pk
        

        if form.is_valid() :
            
            new_orden=form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            new_orden.save()
           
            detalle=ImagenesReunionDetalle()
            detalle.imagenes_reunion_id = new_orden.id
            detalle.descripcion=request.POST["descripcion_imagen"]
            detalle.imagen=request.FILES["imagen_reunion"]
            detalle.save()

            detalle = ImagenesReunionDetalle.objects.filter(imagenes_reunion_id=new_orden.id)

            form=ImagenesReunionForm(instance=imagenesreunion)
            return render_to_response('reunion_imagenes/actualizar.html', { 'form': form,'detalle':detalle,'imagenesreunion':imagenesreunion},  RequestContext(request))



        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        imagenesreunion = ImagenesReunion.objects.get(id=pk)
        detalle = ImagenesReunionDetalle.objects.filter(imagenes_reunion_id=pk)

        form=ImagenesReunionForm(instance=imagenesreunion)  
        detalle = ImagenesReunionDetalle.objects.filter(imagenes_reunion_id=imagenesreunion.id)

        
        return render_to_response('reunion_imagenes/actualizar.html', { 'form': form,'detalle':detalle,'imagenesreunion':imagenesreunion},  RequestContext(request))


class ImagenesReunionListView(ObjectListView):
    model = ImagenesReunion
    paginate_by = 100
    template_name = 'reunion_imagenes/index.html'
    table_class = ReunionTable
    filter_class = ReunionFilter
    context_object_name = 'reuniones'
    def get_context_data(self, **kwargs):
        context = super(ImagenesReunionListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('reunion-delete')
        return context
