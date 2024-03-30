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
from .forms import *
from .tables import *
from .filters import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.db import transaction, DatabaseError
from contabilidad.models import *
from django.db import connection, transaction

def ProveedorListView(request):
      if request.method == 'POST':
        
        proveedores = Proveedor.objects.all()
        return render_to_response('proveedores/index.html', {'proveedores':proveedores},  RequestContext(request))
      else:
        proveedores = Proveedor.objects.all()
        return render_to_response('proveedores/index.html', {'proveedores':proveedores},  RequestContext(request))




@login_required()
@transaction.atomic
def ProveedorCreateView(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                new_proveedor = form.save()
                new_proveedor.activo = True
                new_proveedor.save()
                try:

                    secuencial = Secuenciales.objects.get(modulo='proveedor')
                    secuencial.secuencial = secuencial.secuencial + 1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = datetime.now()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None

                return HttpResponseRedirect('/proveedores/proveedores')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = ProveedorForm

    return render_to_response('proveedores/create.html', {'form': form,}, RequestContext(request))


class ProveedorUpdateView(ObjectUpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/create.html'
    url_success = 'proveedor-list'
    url_cancel = 'proveedor-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Proveedor actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
class ProveedorDetailView(ObjectDetailView):
    model = Cliente
    template_name = 'proveedores/detail.html'

@login_required()
def proveedorEliminarView(request):
    return eliminarView(request, Proveedor, 'proveedor-list')

@login_required()
def proveedorEliminarByPkView(request, pk):
    obj = Proveedor.objects.get(proveedor_id=pk)

    if obj:
        obj.activo = False
        obj.save()

    return HttpResponseRedirect('/proveedores/proveedores')



@login_required()
@csrf_exempt
def validarRuc(request):
    if request.method == 'POST':
      ruc = request.POST.get('ruc')
      ruc2 = request.POST.get('ruc2')
      id = request.POST.get('id')
      #objetos = Proveedor.objects.get(ruc = ruc)
      #modulo_secuencial = objetos.proveedor_id
      
      cursor = connection.cursor()
      if id == '0':
            query = "select proveedor_id,nombre_proveedor,ruc from proveedor where ruc='" + (ruc) + "' or ruc='" + (ruc2) + "';"
      else:
            query = "select proveedor_id,nombre_proveedor,ruc from proveedor where (ruc='" + (ruc) + "' or ruc='" + (ruc2) + "') and proveedor_id!="+ (id) +";"
      print query
      cursor.execute(query)
      ro = cursor.fetchall()
      json_resultados = json.dumps(ro)
      return HttpResponse(json_resultados, content_type="application/json")


    else:
        raise Http404