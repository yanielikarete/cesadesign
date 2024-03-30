# -*- encoding: utf-8 -*-
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
from .tables import *
from .filters import *
from clientes.models import *

from django.views.generic import TemplateView
from django import forms
from models import *
from django.db import connection, transaction

from django.forms.extras.widgets import *
from django.contrib.auth import authenticate, login
from inventario.tables import *
# from login.lib.tools import Tools
from inventario.models import *
from config.models import *
from ordenproduccion.models import *
from django.db import IntegrityError, transaction
import csv
from django.utils.encoding import *
# encoding=utf8
# from config.models import Mensajes



from login.lib.tools import Tools
from django.contrib import auth
now = datetime.datetime.now()

# from login.lib.tools import Tools
# from config.models import Mensajes

@login_required()
def ProductoListView(request):
    tipos = TipoProducto.objects.all().order_by('id')
    # row = Producto.objects.all()
    if tipos.exists():
        tipo = tipos.first()
    # row = Producto.objects.filter(tipo_producto_id=tipo.id)
    # else:
    #     row = Producto.objects.all()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT p.producto_id,p.codigo_producto,p.descripcion_producto,p.tipo_producto,p.bloquea,t.descripcion from producto p,tipo_producto t where p.tipo_producto=t.id and t.id = " + str(
            tipo.id))
    row = cursor.fetchall()

    return render_to_response('producto/index.html', {'row': row, 'tipos': tipos}, RequestContext(request))


# =====================================================#

class ProductoDetailView(ObjectDetailView):
    model = Producto
    template_name = 'producto/detail.html'


# =====================================================#
@login_required()
@transaction.atomic

def ProductoCreateView(request):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        kit_form = KitsForm(request.POST)
        presupuesto_producto_form = PresupuestoProductoForm(request.POST)
        # productos = Producto.objects.all()
        productos = Producto.objects.filter(producto_id=10)
        areas = Areas.objects.all()

        if producto_form.is_valid():
            try:
                with transaction.atomic():
                    new_producto = producto_form.save()
                    new_producto.created_by = request.user.get_full_name()
                    new_producto.updated_by = request.user.get_full_name()
                    new_producto.created_at = now
                    new_producto.updated_at = now
                    new_producto.save()
                    # kit1=kit_form.save()
                    presupuesto_pro = presupuesto_producto_form.save()
                    presupuesto_pro.producto_id = new_producto
                    presupuesto_pro.save()
                    try:
                        secuencial = Secuenciales.objects.get(modulo='producto')
                        secuencial.secuencial = secuencial.secuencial + 1
                        secuencial.created_by = request.user.get_full_name()
                        secuencial.updated_by = request.user.get_full_name()
                        secuencial.created_at = now
                        secuencial.updated_at = now
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
                            print('contador actual' + str(i))
                            # print('id'+request.POST["id_kits"+str(i)])

                            # if 'id_kits'+str(i) in request.POST:
                            #    il=request.POST["id_kits"+str(i)]
                            #    print(il)
                            #    print('GUARDAR'+str(i))
                            #    print('GUARDAR34'+request.POST["costo_kits"+str(i)])
                            #    print('cant'+request.POST["cantidad_kits"+str(i)])
                            #    print('total'+request.POST["total_kits"+str(i)])
                            #
                            #    if il:
                            #        kits=Kits()
                            #        kits.padre = new_producto
                            #        kits.hijo_id=request.POST["id_kits"+str(i)]
                            #        kits.cantidad=request.POST["cantidad_kits"+str(i)]
                            #        kits.costo=float(request.POST["costo_kits"+str(i)])
                            #        kits.total=float(request.POST["total_kits"+str(i)])
                            #        kits.areas_id=request.POST["areas"+str(i)]
                            #        kits.save()

            except IntegrityError:
                print 'error'
                print ordenproduccion_form.errors, len(ordenproduccion_form.errors)

            return HttpResponseRedirect('/inventario/producto')
        else:
            print ('error')
    else:
        producto_form = ProductoForm
        kit_form = KitsForm
        presupuesto_producto_form = PresupuestoProductoForm
        # productos = Producto.objects.all()
        productos = Producto.objects.filter(producto_id=10)

        areas = Areas.objects.all()

    return render_to_response('producto/create.html', {'producto_form': producto_form, 'kit_form': kit_form,
                                                       'presupuesto_producto_form': presupuesto_producto_form,
                                                       'productos': productos, 'areas': areas}, RequestContext(request))


class ProductoActualizarView(TemplateView):
    def get(self, request, *args, **kwargs):

        producto = Producto.objects.get(producto_id=kwargs['pk'])
        # productos = Producto.objects.all()
        # productos = Producto.objects.filter(producto_id=10)
        kits = Kits.objects.filter(padre_id=kwargs['pk'])
        kardex = Kardex.objects.filter(producto_id=kwargs['pk'])

        try:
            presupuesto = PresupuestoProducto.objects.get(producto_id=producto.producto_id)
        except PresupuestoProducto.DoesNotExist:
            presupuesto = None

        producto_form = ProductoForm(instance=producto)
        presupuesto_form = PresupuestoProductoForm(instance=presupuesto)

        context = {
            'section_title': 'Actualizar Presupuesto',
            'button_text': 'Actualizar',
            'producto_form': producto_form,
            'presupuesto_producto_form': presupuesto_form,
            'kardex': kardex,
            'kits': kits

        }

        return render_to_response(
            'producto/producto_form.html', context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        producto = Producto.objects.get(producto_id=kwargs['pk'])
        kardex = Kardex.objects.filter(producto_id=kwargs['pk'])
        try:
            presupuesto = PresupuestoProducto.objects.get(producto_id=producto.producto_id)
        except PresupuestoProducto.DoesNotExist:
            presupuesto = None

        producto_form = ProductoForm(request.POST, request.FILES, instance=producto)
        presupuesto_form = PresupuestoProductoForm(request.POST, request.FILES, instance=presupuesto)
        p_id = kwargs['pk']
        if producto_form.is_valid() and presupuesto_form.is_valid:

            producto.precio1 = producto_form.cleaned_data['precio1']
            producto.precio2 = producto_form.cleaned_data['precio2']
            producto.precio3 = producto_form.cleaned_data['precio3']
            producto.categoria = producto_form.cleaned_data['categoria']
            producto.sub_categoria = producto_form.cleaned_data['sub_categoria']
            producto.linea = producto_form.cleaned_data['linea']
            producto.updated_by = self.request.user.get_full_name()
            producto.updated_at=now
            producto.save()

            new_producto = producto.save()
            new_presupuesto = presupuesto_form.save()
            # new_presupuesto.producto_id = new_producto.producto_id
            new_presupuesto.save()

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
                        idk = request.POST['id_kits' + str(i)]
                        if (len(idk) != 0):
                            kits = Kits()
                            kits.padre = producto
                            kits.hijo_id = request.POST.get('id_kits' + str(i), None)
                            kits.cantidad = request.POST.get('cantidad_kits' + str(i), None)
                            # kits.costo=float(request.POST["costo_kits1"])
                            kits.total = request.POST.get('total_kits' + str(i), None)
                            kits.save()
            # if presupuesto != None:

            #     presupuesto.enero = presupuesto_form.cleaned_data['enero']
            #     presupuesto.febrero = presupuesto_form.cleaned_data['febrero']
            #     presupuesto.marzo = presupuesto_form.cleaned_data['marzo']
            #     presupuesto.abril = presupuesto_form.cleaned_data['abril']
            #     presupuesto.mayo = presupuesto_form.cleaned_data['mayo']
            #     presupuesto.junio = presupuesto_form.cleaned_data['junio']
            #     presupuesto.julio = presupuesto_form.cleaned_data['julio']
            #     presupuesto.agosto = presupuesto_form.cleaned_data['agosto']
            #     presupuesto.septiembre = presupuesto_form.cleaned_data['septiembre']
            #     presupuesto.octubre = presupuesto_form.cleaned_data['octubre']
            #     presupuesto.noviembre = presupuesto_form.cleaned_data['noviembre']
            #     presupuesto.diciembre = presupuesto_form.cleaned_data['diciembre']
            #     presupuesto.producto_id = new_producto.producto_id
            #     presupuesto.save()

            # else:
            #     # presupuesto.save()
            #     # presupuesto.producto_id = new_producto.producto_id
            #     # presupuesto.save()
            #     new_presupuesto = presupuesto_form.save()
            #     new_presupuesto.producto_id = new_producto.producto_id
            #     new_presupuesto.save()

            #     presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES)



            return HttpResponseRedirect(reverse('producto-list'))

        else:
            producto_form = ProductoForm(request.POST, request.FILES)
            presupuesto_form = PresupuestoProductoForm(request.POST, request.FILES)

            context = {
                'section_title': 'Actualizar ',
                'button_text': 'Actualizar',
                'producto_form': producto_form,
                'kardex': kardex,
                'presupuesto_producto_form': presupuesto_form}

            return render_to_response(
                'producto/producto_form.html',
                context,
                context_instance=RequestContext(request))


# =====================================================#

class ProductoUpdateView(TemplateView):
    def get(self, request, *args, **kwargs):

        producto = Producto.objects.get(producto_id=kwargs['pk'])
        try:
            presupuesto = PresupuestoProducto.objects.get(producto_id=producto.producto_id)
        except PresupuestoProducto.DoesNotExist:
            presupuesto = None

        producto_form = ProductoForm(instance=producto)
        presupuesto_form = PresupuestoProductoForm(instance=presupuesto)

        context = {
            'section_title': 'Actualizar Presupuesto',
            'button_text': 'Actualizar',
            'producto_form': producto_form,
            'presupuesto_form': presupuesto_form
        }

        return render_to_response(
            'producto/create.html', context, context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        producto = Producto.objects.get(producto_id=kwargs['pk'])
        try:
            presupuesto = PresupuestoProducto.objects.get(producto_id=producto.producto_id)
        except PresupuestoProducto.DoesNotExist:
            presupuesto = None

        producto_form = ProductoForm(request.POST, request.FILES, instance=producto)
        presupuesto_form = PresupuestoProductoForm(request.POST, request.FILES, instance=presupuesto)

        if producto_form.is_valid():

            producto.precio1 = producto_form.cleaned_data['precio1']
            producto.precio2 = producto_form.cleaned_data['precio2']
            producto.precio3 = producto_form.cleaned_data['precio3']
            producto.categoria = producto_form.cleaned_data['categoria']
            producto.sub_categoria = producto_form.cleaned_data['sub_categoria']
            producto.linea = producto_form.cleaned_data['linea']
            producto.save()

            return HttpResponseRedirect(reverse('producto-list'))

        else:
            producto_form = ProductoForm(request.POST, request.FILES)
            presupuesto_form = PresupuestoProductoForm(request.POST, request.FILES)

            context = {
                'section_title': 'Actualizar ',
                'button_text': 'Actualizar',
                'producto_form': producto_form,
                'presupuesto_form': presupuesto_form}

            return render_to_response(
                'producto/create.html',
                context,
                context_instance=RequestContext(request))


# =====================================================#
@login_required()
def productoEliminarView(request):
    return eliminarView(request, Producto, 'producto-list')


# =====================================================#
@login_required()
def productoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Producto)


# ===============CATEGORIA PRODUCTO=====================#

class CategoriaProductoListView(ObjectListView):
    model = CategoriaProducto
    paginate_by = 100
    template_name = 'categoria_producto/index.html'
    table_class = CategoriaProductoTable
    filter_class = CategoriaProductoFilter

    def get_context_data(self, **kwargs):
        context = super(CategoriaProductoListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('categoria-producto-delete')
        return context


# =====================================================#

class CategoriaProductoDetailView(ObjectDetailView):
    model = CategoriaProducto
    template_name = 'categoria_producto/detail.html'


# =====================================================#

class CategoriaProductoCreateView(ObjectCreateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    template_name = 'categoria_producto/create.html'
    url_success = 'categoria-producto-list'
    url_success_other = 'categoria-producto-create'
    url_cancel = 'categoria-producto-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo_categoria = str(self.object.codigo_categoria).upper()
        self.object.descripcion_categoria = str(self.object.descripcion_categoria).upper()
        self.object.created_by = self.request.user
        self.object.created_at = now
        self.object.updated_at = now
        self.object.save()

        return super(CategoriaProductoCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva categoria del producto."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#

class CategoriaProductoUpdateView(ObjectUpdateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    template_name = 'categoria_producto/create.html'
    url_success = 'categoria-producto-list'
    url_cancel = 'categoria-producto-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo_categoria = str(self.object.codigo_categoria).upper()
        self.object.descripcion_categoria = str(self.object.descripcion_categoria).upper()
        self.object.updated_at = now
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Categoria de Producto actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def CategoriaproductoEliminarView(request):
    return eliminarView(request, CategoriaProducto, 'categoria-producto-list')


# =====================================================#
@login_required()
def CategoriaproductoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, CategoriaProducto)


# ======================================================#
@login_required()
@csrf_exempt
def misCategoriasProductosGuardar(request):
    item = {'exito': 0}
    if request.method == 'POST':
        try:

            categorias = request.POST['data']
            categorias = json.loads(categorias)

            for categoria in categorias:
                if not alumno['codigo_categoria'] == "" and not alumno['codigo_categoria'] == None:
                    try:
                        a = CategoriaProducto()
                        a.codigo_categoria = categoria['codigo_categoria']
                        a.descripcion_categoria = categoria['descripcion_categoria']
                        a.predeterminado = categoria['predeterminado']
                        a.created_by = request.user
                        a.updated_at = now
                        a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar al estudiante")
                        pass

                    item = {'exito': 1}

            if item['exito'] == 1:
                messages.info(request, 'Categorias guardadas!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito': 0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')


# ======================BODEGA=============================#
@login_required()
def BodegaListView(request):
    if request.method == 'POST':

        bodegas = Bodega.objects.all()
        return render_to_response('bodega/index.html', {'bodegas': bodegas}, RequestContext(request))
    else:
        bodegas = Bodega.objects.all()
        return render_to_response('bodega/index.html', {'bodegas': bodegas}, RequestContext(request))


# ====
# =====================================================#

class BodegaDetailView(ObjectDetailView):
    model = Bodega
    template_name = 'bodega/detail.html'


# =====================================================#

class BodegaCreateView(ObjectCreateView):
    model = Bodega
    form_class = BodegaForm
    template_name = 'bodega/create.html'
    url_success = 'bodega-list'
    url_success_other = 'bodega-create'
    url_cancel = 'bodega-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo_bodega = self.object.codigo_bodega
        self.object.nombre = self.object.nombre
        self.object.created_by = self.request.user
        self.object.created_at = now
        self.object.updated_at = now
        self.object.save()

        objetos = Secuenciales.objects.get(modulo='bodega')

        modulo_secuencial = objetos.secuencial + 1
        objetos.secuencial = modulo_secuencial
        objetos.save()

        return super(BodegaCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva bodega."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#

class BodegaUpdateView(ObjectUpdateView):
    model = Bodega
    form_class = BodegaForm
    template_name = 'bodega/create.html'
    url_success = 'bodega-list'
    url_cancel = 'bodega-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo_bodega = self.object.codigo_bodega
        self.object.nombre = self.object.nombre
        self.object.updated_at = now
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Bodega actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def BodegaEliminarView(request):
    return eliminarView(request, Bodega, 'bodega-list')


# =====================================================#
@login_required()
def BodegaEliminarByPkView(request, pk):
    objetos = Bodega.objects.filter(id__in=pk)
    for obj in objetos:
        if obj.activo_bodega:
            obj.activo_bodega = False
        else:
            obj.activo_bodega = True

        obj.save()

    return HttpResponseRedirect('/inventario/bodega')


# ======================================================#
@login_required()
@csrf_exempt
def misBodegaGuardar(request):
    item = {'exito': 0}
    if request.method == 'POST':
        try:

            bodegas = request.POST['data']
            bodegas = json.loads(bodegas)

            for bodega in bodegas:
                if not alumno['codigo_bodega'] == "" and not alumno['codigo_bodega'] == None:
                    try:
                        a = Bodega()
                        a.codigo_bodega = bodega['codigo_bodega']
                        a.nombre = bodega['nombre']
                        a.direccion1 = bodega['direccion1']
                        a.created_by = request.user
                        a.updated_at = now
                        a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar la bodega")
                        pass

                    item = {'exito': 1}

            if item['exito'] == 1:
                messages.info(request, 'Bodegas guardadas!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito': 0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')


# ===============SUBCATEGORIA PRODUCTO=====================#

class SubCategoriaProductoListView(ObjectListView):
    model = SubCategoriaProducto
    paginate_by = 100
    template_name = 'subcategoria_producto/index.html'
    table_class = SubCategoriaProductoTable
    filter_class = SubCategoriaProductoFilter

    def get_context_data(self, **kwargs):
        context = super(SubCategoriaProductoListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('subcategoria-producto-delete')
        return context


# =====================================================#

class SubCategoriaProductoDetailView(ObjectDetailView):
    model = SubCategoriaProducto
    template_name = 'subcategoria_producto/detail.html'


# =====================================================#
class SubCategoriaProductoCreateView(ObjectCreateView):
    model = SubCategoriaProducto
    form_class = SubCategoriaProductoForm
    template_name = 'subcategoria_producto/create.html'
    url_success = 'subcategoria-producto-list'
    url_success_other = 'subcategoria-producto-create'
    url_cancel = 'subcategoria-producto-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo_sub_categ = str(self.object.codigo_sub_categ).upper()
        self.object.descripcion_sub_categ = str(self.object.descripcion_sub_categ).upper()
        self.object.created_by = self.request.user
        self.object.created_at = now
        self.object.updated_at = now
        self.object.save()

        return super(SubCategoriaProductoCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva categoria del producto."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
class SubCategoriaProductoUpdateView(ObjectUpdateView):
    model = SubCategoriaProducto
    fields = ['codigo_sub_categ', 'categoria', 'descripcion_sub_categ', 'imagen_subcateg']
    template_name = 'subcategoria_producto/create.html'
    url_success = 'subcategoria-producto-list'
    url_cancel = 'subcategoria-producto-list'

    def get_success_url(self):
        messages.success(self.request, 'Subcategoria Producto actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def SubCategoriaproductoEliminarView(request):
    return eliminarView(request, SubCategoriaProducto, 'subcategoria-producto-list')


# =====================================================#
@login_required()
def SubCategoriaproductoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, SubCategoriaProducto)


# ======================================================#
@login_required()
@csrf_exempt
def misSubCategoriasProductosGuardar(request):
    item = {'exito': 0}
    if request.method == 'POST':
        try:

            subcategorias = request.POST['data']
            subcategorias = json.loads(subcategorias)

            for categoria in categorias:
                if not alumno['codigo_sub_categ'] == "" and not alumno['codigo_sub_categ'] == None:
                    try:
                        a = CategoriaProducto()
                        a.codigo_categoria = categoria['codigo_categoria']
                        a.descripcion_categoria = categoria['descripcion_categoria']
                        a.predeterminado = categoria['predeterminado']
                        a.created_by = request.user
                        a.updated_at = now
                        a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar al estudiante")
                        pass

                    item = {'exito': 1}

            if item['exito'] == 1:
                messages.info(request, 'Categorias guardadas!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito': 0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')


class KardexListView(ObjectListView):
    model = Kardex
    paginate_by = 100
    template_name = 'kardex/index.html'
    table_class = KardexTable
    filter_class = KardexFilter
    context_object_name = 'kardexs'

    def get_context_data(self, **kwargs):
        context = super(KardexListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('kardex-delete')
        return context


# =====================================================#

class KardexDetailView(ObjectDetailView):
    model = Kardex
    template_name = 'kardex/detail.html'


# =====================================================#
class KardexCreateView(ObjectCreateView):
    model = Kardex
    form_class = KardexForm
    template_name = 'kardex/create.html'
    url_success = 'kardex-list'
    url_success_other = 'kardex-create'
    url_cancel = 'kardex-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.nro_documento = str(self.object.nro_documento).upper()
        self.object.created_by = self.request.user
        self.object.updated_at = now
        self.object.save()

        return super(KardexCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo kardex."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
class KardexUpdateView(ObjectUpdateView):
    model = Kardex
    form_class = KardexForm
    template_name = 'kardex/create.html'
    url_success = 'kardex-list'
    url_cancel = 'kardex-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.nro_documento = str(self.object.nro_documento).upper()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Kardex actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
def kardexEliminarView(request):
    return eliminarView(request, Kardex, 'kardex-list')


# =====================================================#
def kardexEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Kardex)


class LoteListView(ObjectListView):
    model = Lote
    paginate_by = 100
    template_name = 'lote/index.html'
    table_class = LoteTable
    filter_class = LoteFilter

    def get_context_data(self, **kwargs):
        context = super(LoteListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('lote-delete')
        return context


# =====================================================#
class LoteDetailView(ObjectDetailView):
    model = Lote
    template_name = 'lote/detail.html'


# =====================================================#
class LoteCreateView(ObjectCreateView):
    model = Lote
    form_class = LoteForm
    template_name = 'lote/create.html'
    url_success = 'lote-list'
    url_success_other = 'lote-create'
    url_cancel = 'lote-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.nro_lote = str(self.object.nro_lote).upper()
        self.object.created_by = self.request.user
        self.object.updated_at = now
        self.object.save()

        return super(LoteCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo lote."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
class LoteUpdateView(ObjectUpdateView):
    model = Lote
    form_class = LoteForm
    template_name = 'lote/create.html'
    url_success = 'lote-list'
    url_cancel = 'lote-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.nro_lote = str(self.object.nro_lote).upper()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Lote actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def loteEliminarView(request):
    return eliminarView(request, Lote, 'lote-list')


# =====================================================#
@login_required()
def loteEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Lote)


class SerialesListView(ObjectListView):
    model = Seriales
    paginate_by = 100
    template_name = 'seriales/index.html'
    table_class = SerialesTable
    filter_class = SerialesFilter

    def get_context_data(self, **kwargs):
        context = super(SerialesListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('seriales-delete')
        return context


# =====================================================#
class SerialesDetailView(ObjectDetailView):
    model = Seriales
    template_name = 'seriales/detail.html'


# =====================================================#
class SerialesCreateView(ObjectCreateView):
    model = Seriales
    form_class = SerialesForm
    template_name = 'seriales/create.html'
    url_success = 'seriales-list'
    url_success_other = 'seriales-create'
    url_cancel = 'seriales-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.nro_serial = str(self.object.nro_serial).upper()
        self.object.created_by = self.request.user
        self.object.updated_at = now
        self.object.save()

        return super(SerialesCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo ."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
class SerialesUpdateView(ObjectUpdateView):
    model = Seriales
    form_class = SerialesForm
    template_name = 'seriales/create.html'
    url_success = 'seriales-list'
    url_cancel = 'seriales-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.nro_serial = str(self.object.nro_serial).upper()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, ' actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def serialesEliminarView(request):
    return eliminarView(request, Seriales, 'seriales-list')


# =====================================================#
@login_required()
def serialesEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Seriales)


@login_required()
def contact(request):
    if request.method == 'POST':  # If the form has been submitted...
        kit_form = KitsForm(request.POST)
        producto_form = ProductoForm(request.POST)  # A form bound to the POST data
        if kit_form.is_valid() and producto_form.is_valid():
            new_kit = kit_form.save()
            new_producto = producto_form.save()
            new_kit.padre = new_producto
            new_kit.save()

            messages.info(request, 'Nuevo producto creado')

            url = reverse(
                'inventario:producto-list')

            return HttpResponseRedirect(url)
    else:
        kit_form = KitsForm()
        producto_form = ProductoForm()

        forms = [kit_form, producto_form]
        context = {
            'section_title': 'Nuevo Producto',
            'button_text': 'Crear',
        }
        url = reverse(
            'inventario:producto-list')
        return HttpResponseRedirect(reverse_lazy(url))


# =========================Unidades============================#
class UnidadesListView(ObjectListView):
    model = Unidades
    paginate_by = 100
    template_name = 'unidades/index.html'
    table_class = UnidadesTable
    filter_class = UnidadesFilter

    def get_context_data(self, **kwargs):
        context = super(UnidadesListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('unidades-delete')
        return context


class UnidadesDetailView(ObjectDetailView):
    model = Unidades
    template_name = 'unidades/detail.html'


# def UnidadesCreateView(request):
#     if request.method == 'POST':
#         unidades_form=UnidadesForm(request.POST)

#         if unidades_form.is_valid() :
#             unidades.save()
#             return HttpResponseRedirect('/inventario/unidades')
#     else:
#         unidades_form=UnidadesForm
#     return render_to_response('unidades/create.html', { 'unidades': unidades_form},  RequestContext(request))
class UnidadesCreateView(ObjectCreateView):
    model = Unidades
    form_class = UnidadesForm
    template_name = 'unidades/create.html'
    url_success = 'unidades-list'
    url_success_other = 'unidades-create'
    url_cancel = 'unidades-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.abreviatura = str(self.object.abreviatura).upper()
        self.object.descripcion_unidad = str(self.object.descripcion_unidad).upper()
        self.object.created_by = self.request.user
        self.object.created_at = now
        self.object.updated_at = now
        self.object.save()

        return super(UnidadesCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva unidad."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


class UnidadesUpdateView(ObjectUpdateView):
    model = Unidades
    form_class = UnidadesForm
    template_name = 'unidades/create.html'
    url_success = 'unidades-list'
    url_cancel = 'unidades-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Producto actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def unidadesEliminarView(request):
    return eliminarView(request, Producto, 'producto-list')


# =====================================================#
@login_required()
def unidadesEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Producto)


# ===============Tipo PRODUCTO=====================#
class TipoProductoListView(ObjectListView):
    model = TipoProducto
    paginate_by = 100
    template_name = 'tipo_producto/index.html'
    table_class = TipoProductoTable
    filter_class = TipoProductoFilter

    def get_context_data(self, **kwargs):
        context = super(TipoProductoListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('tipo-producto-delete')
        return context


# =====================================================#
class TipoProductoDetailView(ObjectDetailView):
    model = TipoProducto
    template_name = 'tipo_producto/detail.html'


# =====================================================#
class TipoProductoCreateView(ObjectCreateView):
    model = TipoProducto
    form_class = TipoProductoForm
    template_name = 'tipo_producto/create.html'
    url_success = 'tipo-producto-list'
    url_success_other = 'tipo-producto-create'
    url_cancel = 'tipo-producto-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = now
        self.object.updated_at = now
        self.object.save()

        return super(TipoProductoCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva tipo de producto."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
class TipoProductoUpdateView(ObjectUpdateView):
    model = TipoProducto
    form_class = TipoProductoForm
    template_name = 'tipo_producto/create.html'
    url_success = 'tipo-producto-list'
    url_cancel = 'tipo-producto-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = now
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Tipo de Producto actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def TipoproductoEliminarView(request):
    return eliminarView(request, TipoProducto, 'tipo-producto-list')


# =====================================================#
@login_required()
def TipoproductoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, TipoProducto)


# ======================================================#
@login_required()
@csrf_exempt
def misTiposProductosGuardar(request):
    item = {'exito': 0}
    if request.method == 'POST':
        try:

            tipos = request.POST['data']
            tipos = json.loads(tipos)

            for tipo in tipos:
                if not tipo['codigo'] == "" and not tipo['codigo'] == None:
                    try:
                        a = TipoProducto()
                        a.codigo = tipo['codigo']
                        a.descripcion = tipo['descripcion']
                        a.created_by = request.user
                        a.updated_at = now
                        a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar el tipo de producto")
                        pass

                    item = {'exito': 1}

            if item['exito'] == 1:
                messages.info(request, 'Tipo de productos guardados!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito': 0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')


# ------------------LINEA----------------#
class LineaListView(ObjectListView):
    model = Linea
    paginate_by = 100
    template_name = 'linea/index.html'
    table_class = LineaTable
    filter_class = LineaFilter

    def get_context_data(self, **kwargs):
        context = super(LineaListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('linea-delete')
        return context


# =====================================================#
class LineaDetailView(ObjectDetailView):
    model = Linea
    template_name = 'linea/detail.html'


# =====================================================#

class LineaCreateView(ObjectCreateView):
    model = Linea
    form_class = LineaForm
    template_name = 'linea/create.html'
    url_success = 'linea-list'
    url_success_other = 'linea-create'
    url_cancel = 'linea-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = now
        self.object.updated_at = now
        self.object.save()

        return super(LineaCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva linea de producto."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
class LineaUpdateView(ObjectUpdateView):
    model = Linea
    form_class = LineaForm
    template_name = 'linea/create.html'
    url_success = 'linea-list'
    url_cancel = 'linea-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = now
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'TLinea actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def LineaEliminarView(request):
    return eliminarView(request, Linea, 'linea-list')


# =====================================================#
@login_required()
def LineaEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Linea)


# ======================================================#
@login_required()
@csrf_exempt
def misLineasGuardar(request):
    item = {'exito': 0}
    if request.method == 'POST':
        try:

            lineas = request.POST['data']
            lineas = json.loads(lineas)

            for linea in lineas:
                if not linea['codigo'] == "" and not linea['codigo'] == None:
                    try:
                        a = Lineas()
                        a.codigo = linea['codigo']
                        a.descripcion = linea['descripcion']
                        a.created_by = request.user
                        a.updated_at = now
                        a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar la linea de producto")
                        pass

                    item = {'exito': 1}

            if item['exito'] == 1:
                messages.info(request, 'Linea guardados!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito': 0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')


@login_required()
@transaction.atomic
def ProductoCreateOrdenProduccionView(request, pk):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        kit_form = KitsForm(request.POST)
        presupuesto_producto_form = PresupuestoProductoForm(request.POST)
        productos = Producto.objects.all()
        areas = Areas.objects.all()
        ordenproduccion = OrdenProduccion.objects.get(id=pk)

        if producto_form.is_valid():
            with transaction.atomic():
                new_producto = producto_form.save()
                new_producto.created_by = request.user.get_full_name()
                new_producto.updated_by = request.user.get_full_name()
                new_producto.created_at = now
                new_producto.updated_at = now
                new_producto.save()
                # kit1=kit_form.save()
                ordenproduccion.finalizada = True
                ordenproduccion.producto_creado = new_producto
                ordenproduccion.save()

                presupuesto_pro = presupuesto_producto_form.save()
                presupuesto_pro.producto_id = new_producto
                presupuesto_pro.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='producto')
                    secuencial.secuencial = secuencial.secuencial + 1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = now
                    secuencial.updated_at = now
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
                        print('contador actual' + str(i))
                        print('id' + request.POST["id_kits" + str(i)])

                        if 'id_kits' + str(i) in request.POST:
                            il = request.POST["id_kits" + str(i)]
                            print(il)
                            print('GUARDAR' + str(i))
                            print('GUARDAR34' + request.POST["costo_kits" + str(i)])
                            print('cant' + request.POST["cantidad_kits" + str(i)])
                            print('total' + request.POST["total_kits" + str(i)])

                            if il:
                                kits = Kits()
                                kits.padre = new_producto
                                kits.hijo_id = request.POST["id_kits" + str(i)]
                                kits.cantidad = request.POST["cantidad_kits" + str(i)]
                                kits.costo = float(request.POST["costo_kits" + str(i)])
                                kits.total = float(request.POST["total_kits" + str(i)])
                                kits.areas_id = request.POST["areas" + str(i)]
                                kits.save()

                return HttpResponseRedirect('/inventario/producto')
        else:
            print 'error'
            print producto_form.errors
    else:
        producto_form = ProductoForm
        kit_form = KitsForm
        presupuesto_producto_form = PresupuestoProductoForm
        productos = Producto.objects.all()
        areas = Areas.objects.all()

        ordenproduccion = OrdenProduccion.objects.get(id=pk)

    return render_to_response('producto/create_orden_produccion.html',
                              {'producto_form': producto_form, 'kit_form': kit_form,
                               'presupuesto_producto_form': presupuesto_producto_form, 'productos': productos,
                               'areas': areas, 'ordenproduccion': ordenproduccion}, RequestContext(request))


@login_required()
def ProductoAreasListView(request, pk):
    if request.method == 'POST':
        subordenes = ProductoAreas.objects.filter(producto_id=pk)
        ambientes = Areas.objects.all()
        id = pk
        contador = request.POST["columnas_receta"]
        if 'imagen' in request.FILES:
            produc = Producto.objects.get(producto_id=pk)
            produc.imagen = request.FILES["imagen"]
            produc.save()

        i = 0
        while int(i) <= int(contador):
            i += 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'id' + str(i) in request.POST:
                    detalle_id = request.POST["id" + str(i)]
                    subor = ProductoAreas.objects.get(id=detalle_id)
                    subor.updated_by = request.user.get_full_name()
                    subor.areas_id = request.POST["id_areas" + str(i)]
                    subor.secuencia = request.POST["secuencia_guardar" + str(i)]
                    subor.updated_at = now
                    subor.save()

                    print('Tiene detalle' + str(i))
                else:
                    print('No tiene detalle' + str(i))
        subordenes = ProductoAreas.objects.filter(producto_id=pk)
        productos = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto',
                                            'bloquea', 'medida_peso', 'costo').filter(tipo_producto=2)
        p = Producto.objects.get(producto_id=pk)
        p.horas = request.POST["horas"]
        p.costo_horas = request.POST["costo_horas"]
        p.costo_material = request.POST["costo_material"]
        p.costo_fijo = request.POST["costo_fijo"]
        p.total = request.POST["costo_total"]
        p.precio1 = request.POST["precio1"]
        p.precio2 = request.POST["precio2"]
        p.precio3 = request.POST["precio3"]

        p.porcentaje_precio1 = request.POST["porcentaje_precio1"]
        p.porcentaje_precio2 = request.POST["porcentaje_precio2"]
        p.porcentaje_precio3 = request.POST["porcentaje_precio3"]
        p.save()
        id = pk
        ambientes = Areas.objects.all()
        prod = Producto.objects.get(producto_id=pk)

        return render_to_response('producto/producto_ambiente.html',
                                  {'subordenes': subordenes, 'id': id, 'ambientes': ambientes, 'productos': productos,
                                   'prod': prod}, RequestContext(request))

    else:
        subordenes = ProductoAreas.objects.filter(producto_id=pk)
        id = pk
        ambientes = Areas.objects.all()
        productos = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto',
                                            'bloquea', 'medida_peso', 'costo').filter(tipo_producto=2)
        prod = Producto.objects.get(producto_id=pk)

        return render_to_response('producto/producto_ambiente.html',
                                  {'subordenes': subordenes, 'id': id, 'ambientes': ambientes, 'productos': productos,
                                   'prod': prod}, RequestContext(request))


@login_required()
@csrf_exempt
def agregarAmbiente(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        secuencia = request.POST.get('secuencia')
        ambiente = request.POST.get('ambiente')
        areas = Areas.objects.get(id=ambiente)

        re = ProductoAreas()
        re.producto_id = id
        re.areas_id = ambiente
        re.secuencia = secuencia
        re. horas= 0
        re.costo_horas=0
        re.total=0
        re.costo_materiales =0

        # re.costo_hora=areas.costo_hora
        re.save()

        subordenes = ProductoAreas.objects.filter(producto_id=id)

        ambientes = Areas.objects.all()

        return render_to_response('producto/producto_ambiente.html',
                                  {'subordenes': subordenes, 'id': id, 'ambientes': ambientes}, RequestContext(request))

    else:
        raise Http404


@login_required()
@csrf_exempt
def eliminarProductoReceta(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        detalle = ProductoAreas.objects.get(id=id)
        ar = detalle.areas_id
        pr = detalle.producto_id

        kits = Kits.objects.filter(areas_id=ar).filter(padre_id=pr)

        for obj in kits:
            obj.delete()

        manos = ProductoManoObra.objects.filter(producto_areas_id=id)

        for obj in manos:
            obj.delete()

        detalle.delete()
        return HttpResponse(

        )
    else:
        subordenes = ProductoAreas.objects.filter(producto_id=pk)
        id = pk
        ambientes = Areas.objects.all()

        return render_to_response('subordenproduccion/list.html',
                                  {'subordenes': subordenes, 'id': id, 'ambientes': ambientes}, RequestContext(request))


@login_required()
def recetaView(request, pk):
    if request.method == 'POST':

        contador = request.POST["columnas_receta"]
        area = request.POST["areas_id"]

        id = request.POST["id_product"]
        total = 0
        i = 1
        while i <= contador:
            print('i' + str(i))
            print('cont' + str(contador))
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                print('ert' + str(i))
                if 'material_kits' + str(i) in request.POST:

                    if 'id_detalle_kits' + str(i) in request.POST:
                        detalle_id = request.POST["id_detalle_kits" + str(i)]
                        detallecompra = Kits.objects.get(id=detalle_id)
                        detallecompra.updated_by = request.user.get_full_name()
                        detallecompra.cantidad = request.POST["cantidad_kits" + str(i)]
                        detallecompra.medida = request.POST["medida_kits" + str(i)]
                        detallecompra.costo = request.POST["costo_kits" + str(i)]
                        detallecompra.hijo_id = request.POST["producto_kits" + str(i)]
                        detallecompra.total = request.POST["total_kits" + str(i)]
                        detallecompra.otros_costos = request.POST.get('otros_costos_kits' + str(i), False)
                        detallecompra.nombre=request.POST["material_kits" + str(i)]
                        detallecompra.areas_id = area
                        detallecompra.padre_id = id
                        t1 = request.POST["total_kits" + str(i)]
                        total = total + float(t1)
                        # detallecompra.imagen=request.POST["imagen_kits"+str(i)]
                        # detallecompra.updated_at = now
                        # detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                        detallecompra.save()

                        print('Tiene detalle' + str(i))
                    else:
                        comprasdetalle = Kits()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                        comprasdetalle.medida = request.POST["medida_kits" + str(i)]
                        comprasdetalle.costo = request.POST["costo_kits" + str(i)]
                        comprasdetalle.areas_id = area
                        comprasdetalle.otros_costos= request.POST.get('otros_costos_kits' + str(i), False)
                        comprasdetalle.hijo_id = request.POST["producto_kits" + str(i)]
                        comprasdetalle.total = request.POST["total_kits" + str(i)]
                        comprasdetalle.nombre = request.POST["material_kits" + str(i)]
                        comprasdetalle.padre_id = id
                        t1 = request.POST["total_kits" + str(i)]
                        total = total + float(t1)

                        comprasdetalle.save()
                        print('No Tiene detalle' + str(i))
                else:
                    print('OJOOOO' + str(i))
            i = i + 1


            # ordencompra_form=OrdenCompraForm(request.POST)
        subop = ProductoAreas.objects.get(id=pk)
        subop.costo_materiales = total
        subop.save()
        suborden = Kits.objects.filter(padre_id=subop.producto_id).filter(areas_id=subop.areas_id)
        areas = Areas.objects.get(id=subop.areas_id)
        id_product = subop.producto_id
        productos = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto',
                                            'bloquea', 'medida_peso', 'costo', 'unidad').exclude(tipo_producto=2)
        prod = Producto.objects.get(producto_id=subop.producto_id)

        context = {
            'section_title': 'Actualizar Producto',
            'button_text': 'Actualizar',
            'id': pk,
            'subop': subop,
            'productos': productos,
            'suborden': suborden,
            'areas': areas,
            'id_product': id_product,
            'prod': prod,
            'mensaje': 'Actualizada con exito1'}

        return render_to_response(
            'producto/receta.html',
            context,
            context_instance=RequestContext(request))



    else:
        subop = ProductoAreas.objects.get(id=pk)
        suborden = Kits.objects.filter(padre_id=subop.producto_id).filter(areas_id=subop.areas_id)
        areas = Areas.objects.get(id=subop.areas_id)
        id_product = subop.producto_id
        productos = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto',
                                            'bloquea', 'medida_peso', 'costo', 'unidad').exclude(tipo_producto=2)
        prod = Producto.objects.get(producto_id=subop.producto_id)

        context = {
            'section_title': 'Actualizar Producto',
            'button_text': 'Actualizar',
            'id': pk,
            'subop': subop,
            'productos': productos,
            'suborden': suborden,
            'areas': areas,
            'id_product': id_product,
            'prod': prod,
        }

        return render_to_response(
            'producto/receta.html', context, context_instance=RequestContext(request))


@login_required()
@csrf_exempt
@transaction.atomic

def copiarReceta(request):
    id = request.POST["id"]
    prod = request.POST["prod"]
    if request.method == 'POST':
        subordenes = ProductoAreas.objects.filter(producto_id=id)
        with transaction.atomic():
            for detal in subordenes:
                re = ProductoAreas()
                re.producto_id = prod
                re.areas_id = detal.areas_id
                re.secuencia = detal.secuencia
                re.horas = detal.horas
                re.costo_horas = detal.costo_horas
                re.total = detal.total
                re.costo_materiales = detal.costo_materiales
                re.created_by = request.user.get_full_name()
                re.updated_by = request.user.get_full_name()
                re.created_at = now
                re.updated_at = now
                re.save()
                manoobra = ProductoManoObra.objects.filter(producto_areas_id=detal.id)
                for d in manoobra:
                    r = ProductoManoObra()
                    r.producto_areas_id = re.id
                    r.operacion_unitaria = d.operacion_unitaria
                    r.hora_total = d.hora_total
                    r.costo_hora = d.costo_hora
                    r.total = d.total
                    r.created_by = request.user.get_full_name()
                    r.updated_by = request.user.get_full_name()
                    r.created_at = now
                    r.updated_at = now
                    r.save()
            kits = Kits.objects.filter(padre_id=id)
            for det in kits:
                r = Kits()
                r.padre_id = prod
                r.hijo_id = det.hijo_id
                r.cantidad = det.cantidad
                r.costo = det.costo
                r.total = det.total
                r.areas_id = det.areas_id
                r.medida = det.medida
                r.nombre = det.nombre
                r.otros_costos = det.otros_costos
                r.created_by = request.user.get_full_name()
                r.updated_by = request.user.get_full_name()
                r.created_at = now
                r.updated_at = now
                r.save()

            producto_copiar = Producto.objects.get(producto_id=id)
            p = Producto.objects.get(producto_id=prod)
            p.horas = producto_copiar.horas
            p.costo_horas = producto_copiar.costo_horas
            p.costo_material = producto_copiar.costo_material
            p.costo_fijo = producto_copiar.costo_fijo
            p.total = producto_copiar.total
            p.precio1 = producto_copiar.precio1
            p.precio2 = producto_copiar.precio2
            p.save()
            ambientes = Areas.objects.all()
            productos = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto',
                                                'bloquea', 'medida_peso', 'costo').filter(tipo_producto=2)
            id = prod

            return render_to_response('producto/producto_ambiente.html',
                                      {'subordenes': subordenes, 'id': id, 'ambientes': ambientes, 'productos': productos},
                                      RequestContext(request))

    else:
        raise Http404


@login_required()
def ProductoBodegaListView(request, pk):
    if request.method == 'POST':
        if pk:
            id = pk
        else:
            id = 1

        bodega = Bodega.objects.order_by('id')
        prod = ProductoEnBodega.objects.filter(bodega_id=id)
        return render_to_response('producto/producto_bodega.html', {'bodega': bodega, 'productosenbodega': prod},
                                  RequestContext(request))
    else:
        if pk:
            id = pk
        else:
            id = 1
        bodega = Bodega.objects.order_by('id')
        prod = ProductoEnBodega.objects.filter(bodega_id=id)

        return render_to_response('producto/producto_bodega.html', {'bodega': bodega, 'productosenbodega': prod},
                                  RequestContext(request))


@login_required()
@csrf_exempt
def ObtenerProductoBodegaListView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        detalle = ProductoEnBodega.objects.filter(bodega_id=id)
        html = ''
        for detal in detalle:
            html += '<tr><td>' + str(detal.producto) + '</td>'
            html += '<td>' + str(detal.bodega) + '</td>'
            if detal.cantidad < detal.producto.cant_minimia:
                html += '<td style="color:red;font-weight:bold">' + str(detal.cantidad) + '</td>'
            else:
                html += '<td style="color:green">' + str(detal.cantidad) + '</td>'
            html += '<td>' + str(detal.producto.cant_maxima) + '</td>'
            html += '<td>' + str(detal.producto.cant_minimia) + '</td>'
            if detal.cantidad < detal.producto.cant_minimia:
                html += '<td style="color:red;font-weight:bold">Comprar</td>'
            else:
                html += '<td style="color:green"></td>'

        return HttpResponse(
            html
        )
    else:
        raise Http404


@login_required()
def manoObraView(request, pk):
    if request.method == 'POST':
        contador = request.POST["columnas_receta"]
        id = request.POST["id_subop"]
        total = 0
        totalh = 0
        i = 1
        while i <= contador:
            print('i' + str(i))
            print('cont' + str(contador))
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                print('ert' + str(i))
                if 'operacion_kits' + str(i) in request.POST:

                    if 'id_detalle_kits' + str(i) in request.POST:
                        detalle_id = request.POST["id_detalle_kits" + str(i)]
                        detallecompra = ProductoManoObra.objects.get(id=detalle_id)
                        detallecompra.updated_by = request.user.get_full_name()
                        # detallecompra.fecha =request.POST["fecha_kits"+str(i)]
                        detallecompra.operacion_unitaria = request.POST["operacion_kits" + str(i)]
                        # detallecompra.empleado=request.POST["empleado_kits"+str(i)]
                        # detallecompra.hora_inicio=request.POST["hora_inicio_kits"+str(i)]
                        # detallecompra.hora_fin=request.POST["hora_fin_kits"+str(i)]
                        detallecompra.hora_total = request.POST["hora_total_kits" + str(i)]
                        detallecompra.tipo_hora = request.POST["tipo_hora_kits" + str(i)]
                        detallecompra.costo_hora = request.POST["costo_hora_kits" + str(i)]
                        detallecompra.total = request.POST["total_kits" + str(i)]
                        detallecompra.producto_areas_id = pk
                        t1 = request.POST["total_kits" + str(i)]
                        t2 = request.POST["hora_total_kits" + str(i)]
                        total = total + float(t1)
                        totalh = totalh + float(t2)
                        # detallecompra.imagen=request.POST["imagen_kits"+str(i)]
                        # detallecompra.updated_at = now
                        # detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                        detallecompra.save()

                        print('Tiene detalle' + str(i))
                    else:
                        comprasdetalle = ProductoManoObra()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        # comprasdetalle.fecha =request.POST["fecha_kits"+str(i)]
                        comprasdetalle.operacion_unitaria = request.POST["operacion_kits" + str(i)]
                        # comprasdetalle.empleado=request.POST["empleado_kits"+str(i)]
                        # comprasdetalle.hora_inicio=request.POST["hora_inicio_kits"+str(i)]
                        # comprasdetalle.hora_fin=request.POST["hora_fin_kits"+str(i)]
                        comprasdetalle.hora_total = request.POST["hora_total_kits" + str(i)]
                        comprasdetalle.costo_hora = request.POST["costo_hora_kits" + str(i)]
                        comprasdetalle.tipo_hora = request.POST["tipo_hora_kits" + str(i)]
                        comprasdetalle.total = request.POST["total_kits" + str(i)]
                        comprasdetalle.producto_areas_id = pk
                        t1 = request.POST["total_kits" + str(i)]
                        t2 = request.POST["hora_total_kits" + str(i)]
                        totalh = totalh + float(t2)
                        total = total + float(t1)
                        comprasdetalle.save()
                        print('No Tiene detalle' + str(i))
                else:
                    print('OJOOOO' + str(i))
            i = i + 1
            # ordencompra_form=OrdenCompraForm(request.POST)
        suborden = ProductoManoObra.objects.filter(producto_areas_id=pk)
        subop = ProductoAreas.objects.get(id=pk)
        subop.costo_horas = total
        subop.horas = totalh
        subop.save()
        areas = Areas.objects.get(id=subop.areas_id)
        prod = Producto.objects.get(producto_id=subop.producto_id)

        context = {
            'section_title': 'Actualizar Mano de Obra',
            'button_text': 'Actualizar mano de Obra',
            'suborden': suborden,
            'id': pk,
            'subop': subop,
            'prod': prod,
            'areas': areas,
            'mensaje': 'Actualizada con exito1'}

        return render_to_response(
            'producto/manoobra.html',
            context,
            context_instance=RequestContext(request))



    else:
        suborden = ProductoManoObra.objects.filter(producto_areas_id=pk)
        subop = ProductoAreas.objects.get(id=pk)
        areas = Areas.objects.get(id=subop.areas_id)
        prod = Producto.objects.get(producto_id=subop.producto_id)

        context = {
            'section_title': 'Actualizar SubOrdenProduccion',
            'button_text': 'Actualizar',
            'id': pk,
            'subop': subop,
            'areas': areas,
            'prod': prod,
            'suborden': suborden
        }

        return render_to_response(
            'producto/manoobra.html', context, context_instance=RequestContext(request))


class AnalisisListView(ObjectListView):
    model = AnalisisInventario
    paginate_by = 100
    template_name = 'analisis_inventario/index.html'
    table_class = AnalisisInventarioTable
    filter_class = AnalisisInventarioFilter
    context_object_name = 'analisisinventario'

    def get_context_data(self, **kwargs):
        context = super(AnalisisListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('analisis-delete')
        return context


@login_required()
def AnalisisCreateView(request):
    if request.method == 'POST':
        form = AnalisisInventarioForm(request.POST)
        productos = Producto.objects.all()
        ambientes = Ambiente.objects.all()

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = now
            new_orden.updated_at = now
            new_orden.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='analisis')
                secuencial.secuencial = secuencial.secuencial + 1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = now
                secuencial.updated_at = now
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            contador = request.POST["columnas_receta"]
            print contador
            i = 0
            dif = 0
            while int(i) <= int(contador):
                i += 1
                print('entro comoqw' + str(i))
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits' + str(i) in request.POST:
                        product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])

                        proformadetalle = AnalisisInventarioDetalle()
                        proformadetalle.analisis_inventario_id = new_orden.id
                        proformadetalle.producto_id = request.POST["id_kits" + str(i)]
                        proformadetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                        proformadetalle.cantidad_real = request.POST["cantidad_real_kits" + str(i)]
                        dif = float(request.POST["cantidad_kits" + str(i)]) - float(
                            request.POST["cantidad_real_kits" + str(i)])
                        # if (len(request.POST["imagen_kits"+str(i)]))!=0:
                        #     print('prueba'+str(contador))

                        #     proformadetalle.imagen=request.FILES["imagen_kits"+str(i)]
                        # kits.costo=float(request.POST["costo_kits1"])
                        proformadetalle.diferencia = dif
                        # proformadetalle.total=request.POST["total_kits"+str(i)]
                        proformadetalle.save()

                print(i)
                print('contadorsd prueba' + str(contador))

            return HttpResponseRedirect('/inventario/analisis/list')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = AnalisisInventarioForm
        productos = Producto.objects.all()
        ambientes = Ambiente.objects.all()

    return render_to_response('analisis_inventario/create.html',
                              {'form': form, 'productos': productos, 'ambientes': ambientes}, RequestContext(request))


class AnalisisUpdateView(ObjectUpdateView):
    def get(self, request, *args, **kwargs):

        analisis = AnalisisInventario.objects.get(id=kwargs['pk'])
        productos = Producto.objects.all()

        form = AnalisisInventarioForm(instance=analisis)
        detalle = AnalisisInventarioDetalle.objects.filter(analisis_inventario_id=analisis.id)

        context = {
            'section_title': 'Actualizar ',
            'button_text': 'Actualizar',
            'form': form,
            'productos': productos,
            'detalle': detalle,
            'analisis': analisis
        }

        return render_to_response(
            'analisis_inventario/actualizar.html', context, context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        analisis = AnalisisInventario.objects.get(id=kwargs['pk'])
        form = AnalisisInventarioForm(request.POST, request.FILES, instance=analisis)
        p_id = kwargs['pk']
        print(p_id)
        print form.is_valid(), form.errors, type(form.errors)
        productos = Producto.objects.all()

        if form.is_valid():

            new_orden = form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = now
            new_orden.save()
            contador = request.POST["columnas_receta"]

            i = 0
            while int(i) <= int(contador):
                i += 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits' + str(i) in request.POST:
                        product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
                        detalle_id = request.POST["id_detalle" + str(i)]
                        dif = 0
                        print('detalle_id:' + str(detalle_id))
                        if detalle_id:
                            detallecompra = AnalisisInventarioDetalle.objects.get(id=detalle_id)
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto = product
                            detallecompra.cantidad = request.POST["cantidad_kits" + str(i)]
                            detallecompra.cantidad_real = request.POST["cantidad_real_kits" + str(i)]
                            detallecompra.observaciones = request.POST["detalle_kits" + str(i)]
                            dif = float(request.POST["cantidad_kits" + str(i)]) - float(
                                request.POST["cantidad_real_kits" + str(i)])
                            detallecompra.diferencia = dif
                            detallecompra.save()

                        else:
                            comprasdetalle = AnalisisInventarioDetalle()
                            comprasdetalle.analisis_inventario_id = new_orden.id
                            comprasdetalle.producto = product
                            comprasdetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                            comprasdetalle.cantidad_real = request.POST["cantidad_real_kits" + str(i)]
                            comprasdetalle.total = request.POST["total_kits" + str(i)]
                            # comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
                            comprasdetalle.observaciones = request.POST["detalle_kits" + str(i)]
                            dif = float(request.POST["cantidad_kits" + str(i)]) - float(
                                request.POST["cantidad_real_kits" + str(i)])
                            comprasdetalle.diferencia = dif
                            comprasdetalle.save()
                            i += 1
                            print('No Tiene detalle' + str(i))
                            print('contadorsd prueba' + str(contador))
            # ordencompra_form=OrdenCompraForm(request.POST)
            detalle = AnalisisInventarioDetalle.objects.filter(analisis_inventario_id=p_id)
            productos = Producto.objects.all()

            context = {
                'section_title': 'Actualizar Proforma',
                'button_text': 'Actualizar',
                'form': form,
                'detalle': detalle,
                'productos': productos,
                'analisisinventario': analisisinventario,
                'mensaje': 'Analisis Inventario actualizada con exito'}

            return render_to_response(
                'analisis_inventario/actualizar.html',
                context,
                context_instance=RequestContext(request))
        else:

            form = AnalisisInventarioForm(request.POST)
            detalle = AnalisisInventarioDetalle.objects.filter(analisis_inventario_id=analisis.id)
            productos = Producto.objects.all()

            context = {
                'section_title': 'Actualizar Proforma',
                'button_text': 'Actualizar',
                'form': form,
                'detalle': detalle,
                'mensaje': 'Actualizada con exito'}

        return render_to_response(
            'analisis_inventario/actualizar.html',
            context,
            context_instance=RequestContext(request))


class AnalisisInventarioListAprobarView(ObjectListView):
    model = AnalisisInventario
    paginate_by = 100
    table_class = AnalisisInventarioTable
    filter_class = AnalisisInventarioFilter
    template_name = 'analisis_inventario/aprobada.html'
    context_object_name = 'analisis'

    def get_context_data(self, **kwargs):
        context = super(AnalisisInventarioListAprobarView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('analisis-delete')
        return context


@login_required()
def ProductoListTiposView(request, pk):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute(
            "SELECT p.producto_id,p.codigo_producto,p.descripcion_producto,p.tipo_producto,p.bloquea,t.descripcion from producto p,tipo_producto t where p.tipo_producto=t.id and p.tipo_producto=" + pk)
        row = cursor.fetchall()
        tipos = TipoProducto.objects.all().order_by('id')
        return render_to_response('producto/listTipo.html', {'tipos': tipos, 'row': row}, RequestContext(request))
    else:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT p.producto_id,p.codigo_producto,p.descripcion_producto,p.tipo_producto,p.bloquea,t.descripcion from producto p,tipo_producto t where p.tipo_producto=t.id and p.tipo_producto=" + pk)
        row = cursor.fetchall()
        tipos = TipoProducto.objects.all().order_by('codigo')
        # productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea').filter(tipo_producto=pk)
        return render_to_response('producto/listTipo.html', {'tipos': tipos, 'row': row}, RequestContext(request))


@login_required()
def ProductoGeneralListView(request):
    if request.method == 'POST':

        row = ProductoGeneral.objects.all().order_by('descripcion')
        return render_to_response('producto_general/index.html', {'row': row}, RequestContext(request))
    else:
        row = ProductoGeneral.objects.all().order_by('descripcion')
        return render_to_response('producto_general/index.html', {'row': row}, RequestContext(request))


class ProductoGeneralCreateView(ObjectCreateView):
    model = ProductoGeneral
    form_class = ProductoGeneralForm
    template_name = 'producto_general/nuevo.html'
    url_success = 'producto-general-list'
    url_success_other = 'producto-general-create'
    url_cancel = 'producto-general-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = now
        self.object.updated_at = now
        self.object.save()

        objetos = Secuenciales.objects.get(modulo='productogeneral')

        modulo_secuencial = objetos.secuencial + 1
        objetos.secuencial = modulo_secuencial
        objetos.save()

        return super(ProductoGeneralCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva producto general."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
class ProductoGeneralUpdateView(ObjectUpdateView):
    model = ProductoGeneral
    form_class = ProductoGeneralForm
    template_name = 'producto_general/nuevo.html'
    url_success = 'producto-general-list'
    url_cancel = 'producto-general-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = now
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Producto actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


@login_required()
def ProductoGeneralNuevoView(request):
    if request.method == 'POST':
        proforma_form = ProductoGeneralForm(request.POST)

        if proforma_form.is_valid():
            new_orden = proforma_form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = now
            new_orden.updated_at = now
            new_orden.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='productogeneral')
                secuencial.secuencial = secuencial.secuencial + 1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = now
                secuencial.updated_at = now
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            return HttpResponseRedirect('/inventario/producto_general')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
    else:
        proforma_form = ProductoGeneralForm

    return render_to_response('producto_general/nuevo.html', {'form': proforma_form,}, RequestContext(request))


@login_required()
def RecetaEliminarView(request):
    pk = request.POST["id"]
    objetos = Kits.objects.get(id=pk)

    id = objetos.padre_id
    objetos.delete()
    return HttpResponse(

    )


@login_required()
@csrf_exempt
def eliminarManoObraReceta(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        detalle = ProductoManoObra.objects.get(id=id)
        pk = detalle.producto_areas_id
        detalle.delete()
        horas = 0
        valor_horas = 0
        print('entro1')

        suborden = ProductoManoObra.objects.filter(producto_areas_id=pk)
        for s in suborden:
            horas += s.hora_total
            valor_horas += s.total

        subop = ProductoAreas.objects.get(id=pk)
        subop.costo_horas = valor_horas
        subop.horas = horas
        subop.save()
        return HttpResponse(

        )



    else:
        id = request.POST.get('id')
        detalle = ProductoManoObra.objects.get(id=id)
        print('entro2')
        pk = detalle.producto_areas_id
        detalle.delete()
        horas = 0
        valor_horas = 0

        suborden = ProductoManoObra.objects.filter(producto_areas_id=pk)
        for s in suborden:
            horas += s.hora_total
            valor_horas += s.total

        subop = ProductoAreas.objects.get(id=pk)
        subop.costo_horas = valor_horas
        subop.horas = horas
        subop.save()
        areas = Areas.objects.get(id=subop.areas_id)
        prod = Producto.objects.get(producto_id=subop.producto_id)

        context = {
            'section_title': 'Actualizar ManoObra',
            'button_text': 'Actualizar',
            'id': pk,
            'subop': subop,
            'areas': areas,
            'prod': prod,
            'suborden': suborden
        }

        return render_to_response(
            'producto/manoobra.html', context, context_instance=RequestContext(request))


@login_required()
def BodegaKardexListView(request, pk):
    if request.method == 'POST':

        kardex = Kardex.objects.filter(bodega_id=pk)
        bodega = Bodega.objects.get(id=pk)
        return render_to_response('bodega/kardex.html', {'kardex': kardex, 'bodega': bodega}, RequestContext(request))
    else:
        kardex = Kardex.objects.filter(bodega_id=pk)
        bodega = Bodega.objects.get(id=pk)
        return render_to_response('bodega/kardex.html', {'kardex': kardex, 'bodega': bodega}, RequestContext(request))


@csrf_exempt
def loadProducts(request):
    """
    API endpoint that allows users to be viewed or edited.
    """
    response_data = {}
    if request.method == 'POST':

        productos = Producto.objects.exclude(tipo_producto=2)

        if productos.exists():

            result_products = []

            for p in productos:
                producto = {'producto_id': p.producto_id, 'codigo_producto': p.codigo_producto,
                            'descripcion_producto': p.descripcion_producto, 'medida_peso': p.medida_peso,
                            'codigo_produccion': p.codigo_produccion,'precio1':p.precio1,'descripcion_interna': p.descripcion_interna}
                result_products.append(producto)

            response_data['result'] = 'YES'
            response_data['msg'] = 'Se mostrara el listado de productos.'
            response_data['productos'] = result_products
        else:
            response_data['result'] = 'NO'
            response_data['msg'] = 'Se pueden cargar los productos.'
    else:

        response_data['result'] = 'NO'
        response_data['msg'] = 'no es POST.'

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def migrarArchivoProducto(request):
    if request.method == 'POST':

        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        portfolio = csv.DictReader(paramFile)
        users = []
        html = ""
        texto = ""

        lineas = paramFile.split('\n')
        html += '<table border="1">'
        html +='<tr><td>ID</td><td>CODIGO PRODUCTOeweq</td><td>NOMBRE</td><td>CANTIDAD</td><td>CODIGO/ARCHIVO</td><td>NOMBRE/ARCHIVO</td><td>CANTIDAD/ARCHIVO</td><td></td></tr>'
        for linea in lineas:
            x = linea.split(";")
            print ('Valor de linea' + str(x[0]))
            html += '<tr>'
            if len(x[0]):
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT p.producto_id,CAST(p.codigo_producto AS INT) from producto p where p.codigo_producto::INTEGER = " + str(x[0]))
                row = cursor.fetchall()
                if row:

                    try:
                        product = Producto.objects.get(producto_id=row[0][0])

                    except Producto.DoesNotExist:
                        product = None

                    if product:
                        product.unidad = x[2]
                        product.costo = float(x[4].replace(',', '.'))
                        product.base = True
                        product.save()


                        html += '<td>'+str(product.producto_id)+'</td>'
                        html += '<td>' + str(product.codigo_producto) + '</td>'
                        html += '<td>' + str(product.descripcion_producto.encode('utf8')) + '</td>'
                        try:
                            bodega_product = ProductoEnBodega.objects.get(producto_id=product.producto_id)

                        except ProductoEnBodega.DoesNotExist:
                            bodega_product = None

                        if bodega_product:
                            html += '<td>'+str(bodega_product.cantidad)+'</td>'

                            bodega_product.bodega_id=1
                            bodega_product.producto_id=product.producto_id
                            bodega_product.cantidad=float(x[3].replace(',','.'))
                            bodega_product.cantidad_migrada = float(x[3].replace(',', '.'))
                            bodega_product.created_by = request.user.get_full_name()
                            bodega_product.updated_by = request.user.get_full_name()
                            bodega_product.created_at = now
                            bodega_product.updated_at = now
                            bodega_product.save()
                            #
                            #
                            #KARRDEX INGRESO A BODEGA
                            ingreso = Kardex()
                            ingreso.nro_documento=product.producto_id
                            ingreso.producto_id=product.producto_id
                            ingreso.cantidad=float(x[3].replace(',','.'))
                            ingreso.created_by = request.user.get_full_name()
                            ingreso.updated_by = request.user.get_full_name()
                            ingreso.created_at = now
                            ingreso.updated_at = now
                            ingreso.descripcion='Ingreso a inventario'
                            ingreso.un_doc_soporte = 'Migracion del inventario del mes de Enero 2017'
                            ingreso.bodega_id=1
                            ingreso.fecha_ingreso=now
                            ingreso.costo=float(x[5].replace(',','.'))
                            ingreso.modulo='Migracion de inventario'
                            ingreso.save()
                            #
                        else:
                            inventarioBodega=ProductoEnBodega()
                            inventarioBodega.bodega_id = 1
                            inventarioBodega.producto_id = product.producto_id
                            inventarioBodega.cantidad = float(x[3].replace(',', '.'))
                            inventarioBodega.cantidad_migrada = float(x[3].replace(',', '.'))
                            inventarioBodega.created_by = request.user.get_full_name()
                            inventarioBodega.updated_by = request.user.get_full_name()
                            inventarioBodega.created_at = now
                            inventarioBodega.updated_at = now
                            inventarioBodega.save()
                            #
                            #
                            # KARRDEX INGRESO A BODEGA
                            ingreso = Kardex()
                            ingreso.nro_documento = product.producto_id
                            ingreso.producto_id = product.producto_id
                            ingreso.cantidad = float(x[3].replace(',', '.'))
                            ingreso.created_by = request.user.get_full_name()
                            ingreso.updated_by = request.user.get_full_name()
                            ingreso.created_at = now
                            ingreso.updated_at = now
                            ingreso.descripcion = 'Ingreso a inventario'
                            ingreso.un_doc_soporte = 'Migracion del inventario del mes de Enero 2017'
                            ingreso.bodega_id = 1
                            ingreso.fecha_ingreso = now
                            ingreso.costo = float(x[5].replace(',', '.'))
                            ingreso.modulo = 'Migracion de inventario'
                            ingreso.save()
                            html += '<td>0</td>'
                        html += '<td>' + str(x[0]) + '</td>'
                        html += '<td>' + str(x[1]) + '</td>'
                        html += '<td>' + str(x[2]) + '</td>'
                        html += '<td>' + str(x[3]) + '</td>'

                    else:
                        product = Producto()
                        product.codigo_producto=x[0]
                        product.descripcion_producto = x[1]
                        product.unidad = x[2]
                        product.costo = float(x[4].replace(',', '.'))
                        product.created_by = request.user.get_full_name()
                        product.updated_by = request.user.get_full_name()
                        product.created_at = now
                        product.updated_at = now
                        product.save()

                        inventarioBodega = ProductoEnBodega()
                        inventarioBodega.bodega_id = 1
                        inventarioBodega.producto_id = product.producto_id
                        inventarioBodega.cantidad = float(x[3].replace(',', '.'))
                        inventarioBodega.cantidad_migrada = float(x[3].replace(',', '.'))
                        inventarioBodega.created_by = request.user.get_full_name()
                        inventarioBodega.updated_by = request.user.get_full_name()
                        inventarioBodega.created_at = now
                        inventarioBodega.updated_at = now
                        inventarioBodega.save()
                        #
                        #
                        # KARRDEX INGRESO A BODEGA
                        ingreso = Kardex()
                        ingreso.nro_documento = product.producto_id
                        ingreso.producto_id = product.producto_id
                        ingreso.cantidad = float(x[3].replace(',', '.'))
                        ingreso.created_by = request.user.get_full_name()
                        ingreso.updated_by = request.user.get_full_name()
                        ingreso.created_at = now
                        ingreso.updated_at = now
                        ingreso.descripcion = 'Ingreso a inventario'
                        ingreso.un_doc_soporte = 'Migracion del inventario del mes de Enero 2017'
                        ingreso.bodega_id = 1
                        ingreso.fecha_ingreso = now
                        ingreso.costo = float(x[5].replace(',', '.'))
                        ingreso.modulo = 'Migracion de inventario'
                        ingreso.save()

                        html += '<td></td>'
                        html += '<td></td>'
                        html += '<td></td>'
                        html += '<td></td>'
                        html+='<td>'+str(x[0])+'</td>'
                        html += '<td>' + str(x[1]) + '</td>'
                        html += '<td>' + str(x[2]) + '</td>'
                        html += '<td>' + str(x[3]) + '</td>'
                else:
                    html += '<td></td>'
                    html += '<td></td>'
                    html += '<td></td>'
                    html += '<td></td>'
                    html += '<td>' + str(x[0]) + '</td>'
                    html += '<td>' + str(x[1]) + '</td>'
                    html += '<td>' + str(x[2]) + '</td>'
                    html += '<td>' + str(x[3]) + '</td>'
            else:
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                print('hola')

            html += '</tr>'
        #html = '<table><tr><td>UNO</td><td>DOS</td><td>TRES</td></tr></table>'
        html+='</table>'
        texto +='<p>TEXTO 222222</p>'

        print ('html' + str(html))
        context = {
            'section_title': 'Actualizar ',
            'button_text': 'Actualizar',
            'texto': texto,
            'html': html}

        return render_to_response(
            'producto/migrar.html',
            context,
            context_instance=RequestContext(request))
        # return HttpResponse(
        #     html
        # )




    else:
        texto = "text"
        html="HOLAAA"
        texto += '<p>texto escrito</p>'
        return render_to_response('producto/migrar.html', {'html': html,'texto': texto}, RequestContext(request))
