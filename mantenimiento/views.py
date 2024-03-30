from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from mantenimiento.forms import *
from config.models import *
from config.forms import *
from contabilidad.models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, \
    eliminarByPkView, cambiarEstadoByPkView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader,Context, Template

from django.contrib import messages
import simplejson as json
import datetime
from .models import *
from .forms import *
# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
from django.db.models import Sum
from django.db import transaction, DatabaseError
now = datetime.now()

@login_required()
def retenciones_list_view(request):
    retenciones = Retenciones.objects.all()
    template = loader.get_template('codigoRetenciones/index.html')
    context = RequestContext(request, {'retenciones': retenciones})
    return HttpResponse(template.render(context))


@login_required()
@transaction.atomic
def RetencionCreateView(request):
    if request.method == 'POST':
        form = RetencionForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                new = form.save()
                new.save()

                return HttpResponseRedirect('/mantenimiento/codigoRetenciones')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = RetencionForm

    return render_to_response('codigoRetenciones/create.html', {'form': form,}, RequestContext(request))

class RetencionUpdateView(ObjectUpdateView):
    model = Retenciones
    form_class = RetencionForm
    template_name = 'codigoRetenciones/create.html'
    url_success = 'retenciones-list'
    url_cancel = 'retenciones-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Retencion actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

@login_required()
def retenciones_nuevo_view(request):
    tipo_retenciones = TipoRetencion.objects.all()
    template = loader.get_template('codigoRetenciones/create.html')
    context = RequestContext(request, {'tipo_retenciones': tipo_retenciones})
    return HttpResponse(template.render(context))

@login_required()
def retenciones_crear_view(request):
    if request.method == 'POST':
        form = RetencionForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            retencion = Retenciones()
            retencion.codigo = cleaned_data.get('codigo')
            retencion.descripcion = cleaned_data.get('descripcion')
            retencion.porcentaje = cleaned_data.get('porcentaje')
            retencion.codigo_anexo = cleaned_data.get('codigo_anexo')
            retencion.tipo_retencion_id = int(cleaned_data.get('tipo_retencion').id)
            retencion.campo_formulario = cleaned_data.get('campo_formulario')
            retencion.codigo_facturacion_electronica=cleaned_data.get('codigo_facturacion_electronica')
            retencion.save()
        return HttpResponseRedirect('/mantenimiento/codigoRetenciones')


@login_required()
def retenciones_edit_view(request, pk):
    retenciones = Retenciones.objects.get(pk=pk)
    tipo_retenciones = TipoRetencion.objects.all()
    template = loader.get_template('codigoRetenciones/edit.html')
    context = RequestContext(request, {'retenciones': retenciones,'tipo_retenciones': tipo_retenciones})
    return HttpResponse(template.render(context))

@login_required()
def retenciones_update_view(request, pk):
    if request.method == 'POST':
        form = RetencionForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            retencion = Retenciones.objects.get(pk=pk)
            retencion.codigo = cleaned_data.get('codigo')
            retencion.descripcion = cleaned_data.get('descripcion')
            retencion.porcentaje = cleaned_data.get('porcentaje')
            retencion.codigo_anexo = cleaned_data.get('codigo_anexo')
            #retencion.tipo_retencion = int(cleaned_data.get('tipo_retencion'))
            retencion.tipo_retencion_id = cleaned_data.get('tipo_retencion').id
            retencion.campo_formulario = cleaned_data.get('campo_formulario')
            retencion.save()
        return HttpResponseRedirect('/mantenimiento/codigoRetenciones')

@login_required()
def formaspagos_list_view(request):
    pagos = FormaPago.objects.all()
    template = loader.get_template('formasPagos/index.html')
    context = RequestContext(request, {'pagos': pagos})
    return HttpResponse(template.render(context))

@login_required()
def formaspagos_nuevo_view(request):
    template = loader.get_template('formasPagos/create.html')
    context = RequestContext(request, { })
    return HttpResponse(template.render(context))

@login_required()
def formaspagos_crear_view(request):
    if request.method == 'POST':
        form = PagosForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            pago = FormaPago()
            pago.descripcion = cleaned_data.get('descripcion')
            pago.codigo = cleaned_data.get('codigo')
            pago.save()
        return HttpResponseRedirect('/mantenimiento/formasPagos')

@login_required()
def formaspagos_edit_view(request, pk):
    pagos = FormaPago.objects.get(pk=pk)
    template = loader.get_template('formasPagos/editar.html')
    context = RequestContext(request, {'pagos': pagos})
    return HttpResponse(template.render(context))

@login_required()
def formaspagos_update_view(request, pk):
    if request.method == 'POST':
        form = PagosForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            pago = FormaPago.objects.get(pk=pk)
            pago.codigo = cleaned_data.get('codigo')
            pago.descripcion = cleaned_data.get('descripcion')
            pago.save()
        return HttpResponseRedirect('/mantenimiento/formasPagos')




# ======================BODEGA=============================#
@login_required()
def SustentoTributarioListView(request):
    if request.method == 'POST':

        sustentos = SustentoTributario.objects.all()
        return render_to_response('sustento_tributario/index.html', {'sustentos': sustentos}, RequestContext(request))
    else:
        sustentos = SustentoTributario.objects.all()
        return render_to_response('sustento_tributario/index.html', {'sustentos': sustentos}, RequestContext(request))


# =====================================================#
def SustentoTributarioCreateView(request):
    if request.method == 'POST':
        form = SustentoTributarioForm(request.POST)

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = now
            new_orden.updated_at = now
            new_orden.save()

            return HttpResponseRedirect('/mantenimiento/sustento_tributario')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = SustentoTributarioForm

    return render_to_response('sustento_tributario/create.html', {'form': form,}, RequestContext(request))

@login_required()
def SustentoTributarioUpdateView(request, pk):
    if request.method == 'POST':
        sustento = SustentoTributario.objects.get(id=pk)
        form = SustentoTributarioForm(request.POST, request.FILES, instance=sustento)
        print form.is_valid(), form.errors, type(form.errors)

        if form.is_valid():

            sustento = form.save()
            return HttpResponseRedirect('/mantenimiento/sustento_tributario')
        else:

            form = SustentoTributarioForm(request.POST)

            context = {
                'section_title': 'Actualizar Sustento',
                'button_text': 'Actualizar',
                'form': form}

        return render_to_response(
            'sustento_tributario/edit.html',
            context,
            context_instance=RequestContext(request))
    else:
        sustento = SustentoTributario.objects.get(id=pk)
        form = SustentoTributarioForm(instance=sustento)


        context = {
            'section_title': 'Actualizar Sustento',
            'button_text': 'Actualizar',
            'sustento': sustento,
            'form': form}

        return render_to_response(
            'sustento_tributario/edit.html',
            context,
            context_instance=RequestContext(request))

@login_required()
@transaction.atomic
def ConfiguracionContabilidad(request):
    if request.method == 'POST':
        form = ParametrosForm(request.POST)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')

        if form.is_valid():
            with transaction.atomic():
                new = form.save()
                new.save()
                return HttpResponseRedirect('/mantenimiento/contabilidad')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = ParametrosForm
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')

    return render_to_response('contabilidad/cuentas.html', {'form': form,'cuentas':cuentas}, RequestContext(request))
