# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.shortcuts import render
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
from models import *
from django.forms.extras.widgets import *
from django.contrib.auth import authenticate,login
from config.models import *
from pedido.models import *
from facturacion.models import *
from ordenproduccion.models import *
from django.db import IntegrityError, transaction
#=========================Orden de Servicio============================#
@login_required()
def OrdenServicioListView(request):
    if request.method == 'POST':
        ordenes = OrdenServicio.objects.all()
        clientes = Cliente.objects.all()

        return render_to_response('ordenservicio/index.html', { 'ordenes': ordenes,'clientes':clientes},  RequestContext(request))



    else:
        ordenes = OrdenServicio.objects.all()
        clientes = Cliente.objects.all()



        return render_to_response('ordenservicio/index.html', { 'ordenes': ordenes,'clientes':clientes},  RequestContext(request))


class OrdenServicioDetailView(ObjectDetailView):
    model = OrdenServicio
    template_name = 'ordenservicio/detail.html'


# class OrdenServicioCreateView(ObjectCreateView):
#     model = OrdenServicio
#     form_class = OrdenServicioForm
#     template_name = 'ordenservicio/create.html'
#     url_success = 'ordenservicio-list'
#     url_success_other = 'ordenservicio-create'
#     url_cancel = 'ordenservicio-list'


#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         #self.object.placa = str(self.object.placa).upper()
#         self.object.created_by = self.request.user
#         self.object.created_at = datetime.now()
#         self.object.updated_at = datetime.now()
#         self.object.save()

#         return super(OrdenServicioCreateView, self).form_valid(form)

#     def get_success_url(self):
#         mensaje = "Ha ingresado 1 nueva OrdenServicio."
#         messages.success(self.request, mensaje)

#         if '_addanother' in self.request.POST and self.request.POST['_addanother']:
#             return reverse_lazy(self.url_success_other)
#         else:
#             return reverse_lazy(self.url_success)
@login_required()
@transaction.atomic
def OrdenServicioCreateView(request):
    if request.method == 'POST':
        form = OrdenServicioForm(request.POST)
        guias = GuiaRemision.objects.all()
        ordenes = OrdenProduccion.objects.all()
        pedidos = Pedido.objects.all()

        if form.is_valid():
            with transaction.atomic():
                new_orden=form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()

                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='ordenServicio')
                    secuencial.secuencial=secuencial.secuencial+1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = datetime.now()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None

                return HttpResponseRedirect('/ordenServicio/ordenservicio')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form=OrdenServicioForm
        guias = GuiaRemision.objects.all()
        ordenes = OrdenProduccion.objects.all()
        pedidos = Pedido.objects.all()


    return render_to_response('ordenservicio/create.html', { 'form': form, 'guias':guias, 'ordenes':ordenes, 'pedidos':Pedido,},  RequestContext(request))


# class OrdenServicioUpdateView(ObjectUpdateView):
#     model = OrdenServicio
#     form_class = OrdenServicioForm
#     template_name = 'ordenservicio/create.html'
#     url_success = 'ordenservicio-list'
#     url_cancel = 'ordenservicio-list'


#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         #self.object.placa = str(self.object.placa).upper()
#         self.object.save()


#         return super(ObjectUpdateView, self).form_valid(form)
#     def get_success_url(self):
#         messages.success(self.request, 'OrdenServicio actualizado con exito')
#         if '_addanother' in self.request.POST and self.request.POST['_addanother']:
#             return reverse_lazy(self.url_success_other)
#         else:
#             return reverse_lazy(self.url_success)
@login_required()
def OrdenServicioUpdateView(request,pk):
    if request.method == 'POST':
        ordenservicio=OrdenServicio.objects.get(orden_id=pk)
        form=OrdenServicioForm(request.POST,request.FILES,instance=ordenservicio)
        print form.is_valid(), form.errors, type(form.errors)

        if form.is_valid():
            orden=form.save()


            return HttpResponseRedirect('/ordenServicio/ordenservicio')
        else:

            form=OrdenServicioForm(request.POST)

            context = {
            'section_title':'Actualizar Orden de Servicio',
            'button_text':'Actualizar',
            'form':form,
            }

        return render_to_response(
            'ordenservicio/create.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordenservicio=OrdenServicio.objects.get(orden_id=pk)
        form=OrdenServicioForm(instance=ordenservicio)

        context = {
            'section_title':'Actualizar Guia Remision',
            'button_text':'Actualizar',
            'form':form,
            }

        return render_to_response(
            'ordenservicio/create.html',
            context,
            context_instance=RequestContext(request))

#=====================================================#
@login_required()
def OrdenServicioEliminarView(request):
    return eliminarView(request, OrdenServicio, 'ordenservicio-list')

#=====================================================#
@login_required()
def OrdenServicioEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, OrdenServicio)


@login_required()
@csrf_exempt
def agregarOrdenServicio(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        os = request.POST.get('os')
        cliente = request.POST.get('cliente')
        pedido = request.POST.get('pedido')
        op = request.POST.get('op')
        maestro = request.POST.get('maestro')
        trabajo = request.POST.get('trabajo')
        observaciones = request.POST.get('observaciones')
        obj = request.POST.get('obj')

        re=OrdenServicio()
        re.fecha=fecha
        re.nro_orden=os
        re.cliente_id=cliente
        re.maestro=maestro
        re.observaciones=observaciones
        re.objeto_orden=obj
        re.codigo_pedido=pedido
        re.codigo_orden_produccion=op
        re.trabajos_realizar=trabajo
        re.save()
        try:
            secuencial = Secuenciales.objects.get(modulo='ordenServicio')
            secuencial.secuencial = secuencial.secuencial + 1
            secuencial.created_by = request.user.get_full_name()
            secuencial.updated_by = request.user.get_full_name()
            secuencial.created_at = datetime.now()
            secuencial.updated_at = datetime.now()
            secuencial.save()
        except Secuenciales.DoesNotExist:
            secuencial = None


        ordenes = OrdenServicio.objects.all()
        clientes = Cliente.objects.all()

        return render_to_response('ordenservicio/index.html', { 'ordenes': ordenes,'clientes':clientes},  RequestContext(request))

    else:
        raise Http404
