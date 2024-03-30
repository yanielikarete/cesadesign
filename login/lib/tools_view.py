# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
import datetime
from django_tables2 import RequestConfig, SingleTableMixin, SingleTableView
from django.views.generic import ListView, CreateView, DetailView, UpdateView

#from login.lib.export import Export
from login.lib.tools import Tools
from login.models import *
from inventario.models import *

#=====================================================#
## Class Base Views
#=====================================================#
class ObjectListView(SingleTableView):
    paginate_by = 100
    context_object_name = 'entities'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ObjectListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        export_data = self.request.GET.get('export_data', None)
        if export_data:
            qs = self.get_queryset()

            if export_data == "pdf":
                return Export.export_to_pdf(qs,request.user.docente)

            """if export_data == "excel":
                return Export.export_to_excel(qs,self.table_class.fields_report)
            else:
                return Export.export_to_csv(qs,self.table_class.fields_report)"""

        return super(ObjectListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(ObjectListView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_paginate_by(self, queryset):
        self.paginate_by = self.request.GET.get('paginate_by', '100')
        if not self.paginate_by.isdigit():
            self.paginate_by = 100
        elif int(self.paginate_by) > 500:
            self.paginate_by = 100

        return self.paginate_by

    def get_table(self, **kwargs):
        table = super(ObjectListView, self).get_table()
        RequestConfig(self.request, paginate={"per_page": self.paginate_by}).configure(table)
        return table

    def get_context_data(self, **kwargs):
        context = super(ObjectListView, self).get_context_data(**kwargs)

        filter_num = 0
        for field in self.filter.form:
            if field.data:
                filter_num += 1

        context['paginate_by'] = self.paginate_by
        context['verbose_name'] = self.model._meta.verbose_name.title()
        context['verbose_name_plural'] = self.model._meta.verbose_name_plural.title()
        context['filter'] = self.filter
        context['filter_num'] = filter_num

        return context

#=====================================================#
class ObjectDetailView(DetailView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ObjectDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ObjectDetailView, self).get_context_data(**kwargs)
        queryset = super(ObjectDetailView, self).get_queryset()
        context['verbose_name'] = queryset.model._meta.verbose_name.title()
        return context

#=====================================================#
class ObjectCreateView(CreateView):
    url_cancel = ''
    url_success_other = ''
    url_success = ''
    url = ''

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        max_registro = 50 #Pyme.get_restricciones(self.request.user.docente.pyme)['max_registro']
        num_registros =  self.model.objects.count()

        if num_registros < max_registro:
            return super(ObjectCreateView, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404

    def form_valid(self, form):
        self.object = form.save(commit=False)

        """if not self.request.user.groups.filter(name = 'pyme'):
            self.object.created_by = self.request.user
        else:
            try:
                self.object.created_by
            except:
                self.object.created_by = self.request.user"""
        try:
            self.object.docente = self.request.user.docente
        except:
            pass

        #self.object.pyme = self.request.user.docente.pyme
        self.object.created_by = self.request.user
        self.object.updated_at = datetime.datetime.now()
        self.object.save()
        return super(ObjectCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Información creada con exito.')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success, args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super(ObjectCreateView, self).get_context_data(**kwargs)
        queryset = super(ObjectCreateView, self).get_queryset()
        context['verbose_name'] = queryset.model._meta.verbose_name.title()
        context['url_cancel'] = reverse_lazy(self.url_cancel)
        context['action'] = 'Crear'

        return context

#=====================================================#
class ObjectUpdateView(UpdateView):
    additional_context = {}
    url_success = ''
    url_cancel = ''

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ObjectUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Información actualizada con exito.')
        return reverse_lazy(self.url_success, args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super(ObjectUpdateView, self).get_context_data(**kwargs)
        context['verbose_name'] = self.object._meta.verbose_name.title()
        context['url_cancel'] = reverse_lazy(self.url_cancel)
        context['action'] = 'Editar'
        return context

#=====================================================#
## Eliminar Class Base View
#=====================================================#
@login_required()
def eliminarView(request, Model, url):
    if request.method == 'POST':
        try:
            ids =  request.POST.getlist('selected_action')
            if eliminar(request, ids, Model) == 1:
                messages.success(request, 'Datos Eliminados Correctamente.')
        except Exception as e:
            #Tools.manejadorErrores(e)
            messages.error(request, 'Ocurrio un Error al Intentar Eliminar, Inténtelo nuevamente.')

    return HttpResponseRedirect(reverse_lazy(url))

#=====================================================#
@login_required()
def eliminarByPkView(request, pk, Model):
    try:
        eliminar(request, [pk], Model)
    except Exception as e:
        #Tools.manejadorErrores(e)
        messages.error(request, 'Ocurrio un Error al Intentar Eliminar, Inténtelo nuevamente.')

    return HttpResponse('')

#=====================================================#
def eliminar(request, ids, Model):
    objetos = Model.objects.filter(id__in = ids)
    for obj in objetos:
        obj.activo = False
        obj.save()
#obj.delete()
    if not objetos:
        messages.error(request, 'Los Datos Predeterminados No Pueden ser Eliminados.')
        return 0
    return 1
#=====================================================#
@login_required()
def cambiarEstadoByPkView(request, pk, Model):
    try:
        cambiar_estado(request, [pk], Model)
    except Exception as e:
        #Tools.manejadorErrores(e)
        messages.error(request, 'Ocurrio un Error al Intentar Eliminar, Inténtelo nuevamente.')

    return HttpResponse('')

#=====================================================#
def cambiar_estado(request, ids, Model):
    objetos = Model.objects.filter(id__in = ids)
    for obj in objetos:
        if obj.activo == False:
            obj.activo = True
        else:
            obj.activo = False


        obj.save()
#obj.delete()
    if not objetos:
        messages.error(request, 'Los Datos Predeterminados No Pueden ser Eliminados.')
        return 0
    return 1


@login_required()
def calcularProforma(request, pk, Model):
    objetos = ProformaDetalle.objects.filter(proforma_id = pk).exclude(no_producir=True)
    subtotal=0
    for obj in objetos:
        subtotal+=obj.total
    
    prof=Proform.objects.get(id = pk)
    porc_desc=prof.porcentaje_descuento
    porc_iva=prof.porcentaje_iva
    monto_desc= round(float(subtotal*porc_desc/100),2)
    subtota_desc=round(float(subtotal+monto_desc),2)
    
    monto_iva= round(float(subtota_desc*porc_iva/100),2)
    subtotal_iva=round(float(subtota_desc+monto_iva),2)
    prof.porcentaje_iva=porc_iva
    prof.iva=monto_iva
    prof.porcentaje_descuento=porc_desc
    prof.descuento=monto_desc
    prof.total=subtotal_iva
    prof.save()
    return HttpResponse('')


@login_required()
def anularByPkView(request, pk, Model,url):
    try:
        anular(request, [pk], Model)
    except Exception as e:
        #Tools.manejadorErrores(e)
        messages.error(request, 'Ocurrio un Error al Intentar Eliminar, Inténtelo nuevamente.')

    return HttpResponseRedirect(reverse_lazy(url))

def anular(request, ids, Model):
    objetos = Model.objects.filter(id__in = ids)
    for obj in objetos:
        obj.anulado = True
        obj.aprobada = False
        obj.save()
#obj.delete()
    if not objetos:
        messages.error(request, 'Los Datos Predeterminados No Pueden ser Eliminados.')
        return 0
    return 1
