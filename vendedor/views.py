# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, eliminarByPkView,cambiarEstadoByPkView
from django.core.urlresolvers import reverse_lazy
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

from login.lib.tools import Tools

from config.models import Mensajes
from django.template import RequestContext
from django.forms.extras.widgets import *
from django.contrib import auth

def VendedoresListView(request):
    if request.method == 'POST':
        empleados = Vendedor.objects.all().order_by('nombre')
        return render_to_response('vendedores/index.html', {'vendedores': empleados}, RequestContext(request))
    else:
        empleados = Vendedor.objects.all().order_by('nombre')
        return render_to_response('vendedores/index.html', {'vendedores': empleados}, RequestContext(request))

#=====================================================#
class VendedorDetailView(ObjectDetailView):
    model = Vendedor
    template_name = 'vendedores/detail.html'

#=====================================================#
class VendedorCreateView(ObjectCreateView):
    model = Vendedor
    form_class = VendedoresForm
    template_name = 'vendedores/create.html'
    url_success = 'vendedores-list'
    url_success_other = 'vendedores-create'
    url_cancel = 'vendedores-list'


    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        
        # objetos = Secuenciales.objects.get(modulo = 'vendedor')
        
        # modulo_secuencial = objetos.secuencial+1
        # objetos.secuencial=modulo_secuencial
        # objetos.save()

        return super(VendedorCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo vendedor."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
class VendedorUpdateView(ObjectUpdateView):
    model = Vendedor
    form_class = VendedoresForm
    template_name = 'vendedores/create.html'
    url_success = 'vendedores-list'
    url_cancel = 'vendedores-list'

  
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Vendedor actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def VendedorEliminarView(request):
    return eliminarView(request, Vendedor, 'vendedores-list')

#=====================================================#
@login_required()
def VendedorEliminarByPkView(request, pk):
    objetos = Vendedor.objects.filter(id__in = pk)
    for obj in objetos:
        if obj.activo:
            obj.activo = False
        else:
            obj.activo= True

        obj.save()

    return HttpResponseRedirect('/vendedores/vendedores')

