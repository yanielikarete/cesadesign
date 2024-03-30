# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from login.middlewares import ThreadLocal
from .models import *
from os import path
from django.views.generic import TemplateView
from django.shortcuts import render_to_response

from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import NON_FIELD_ERRORS
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from .models import *



class ProductoForm(forms.ModelForm):
    activo = models.BooleanField(default=False)
    #categoria = forms.ModelChoiceField(queryset=CategoriaProducto.objects.all())

    class Meta:
        model = Producto
        #cuenta_compra y cuenta_venta verificar donde se lo utiiza
        fields = ("codigo_producto","descripcion_producto","descripcion_interna","categoria","sub_categoria","imagen","tipo_producto","linea","activo","precio1","precio2","precio3","cant_minimia","notas","unidad","medida_peso","peso","costo","costo_promedio","acepta_iva","created_at","updated_at","created_by","updated_by","uat","precio_de_compra_max","codigo_produccion","bloquea","cant_maxima")
        widgets = {
            'precio1': forms.TextInput(attrs={'class': 'mask_float'}),
            'precio2': forms.TextInput(attrs={'class': 'mask_float'}),
            'precio3': forms.TextInput(attrs={'class': 'mask_float'}),
            'precio_de_compra_max': forms.TextInput(attrs={'class': 'mask_float'}),
            'costo_promedio': forms.TextInput(attrs={'class': 'mask_float'}),
            'costo': forms.TextInput(attrs={'class': 'mask_float'}),
            'precio_de_compra_max': forms.TextInput(attrs={'class': 'mask_float'}),
            'cant_maxima': forms.TextInput(attrs={'class': 'mask_float'}),
            'cant_minimia': forms.TextInput(attrs={'class': 'mask_float'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['categoria']=forms.ModelChoiceField(queryset=CategoriaProducto.objects.all())



class ProductoUpdateForm(forms.ModelForm):
    activo = models.BooleanField(default=False)
    class Meta:
        model = Producto
        #cuenta_compra y cuenta_venta verificar donde se lo utiiza
        fields = ("codigo_producto","descripcion_producto","categoria","sub_categoria","imagen","tipo_producto","linea","activo","precio1","precio2","precio3","cant_minimia","notas","unidad","medida_peso","peso","costo","costo_promedio","precio_de_compra_0","acepta_iva","created_at","updated_at","created_by","updated_by","codigo_produccion","bloquea","cant_maxima")
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['precio1'].widget.attrs['class'] = 'mask_float'

class CategoriaProductoForm(forms.ModelForm):

    class Meta:
        model = CategoriaProducto
        exclude = ("created_at","updated_at","created_by","updated_by","predeterminado","nro_productos","imagen_categoria")

class SubCategoriaProductoForm(forms.ModelForm):

    class Meta:
        model = SubCategoriaProducto
        fields = ['codigo_sub_categ', 'categoria', 'descripcion_sub_categ']

class BodegaForm(ModelForm):

    class Meta:
        model = Bodega
        exclude = ("created_at","updated_at","created_by","updated_by")


class KardexForm(ModelForm):

    class Meta:
        model = Kardex
        exclude = ("created_at","updated_at","created_by","updated_by")

class LoteForm(ModelForm):

    class Meta:
        model = Lote
        exclude = ("created_at","updated_at","created_by","updated_by")


class SerialesForm(ModelForm):

    class Meta:
        model = Seriales
        exclude = ("created_at","updated_at","created_by","updated_by")

class KitsForm(forms.ModelForm):

    class Meta:
        model = Kits
        exclude = ("padre","created_at","updated_at","created_by","updated_by")

    def __init__(self, *args, **kwargs):
        super(KitsForm, self).__init__(*args, **kwargs)
        self.fields['hijo'].label = "Producto"

class PresupuestoProductoForm(forms.ModelForm):

    class Meta:
        model = PresupuestoProducto
        exclude = ("producto_id","created_at","updated_at","created_by","updated_by")


class UnidadesForm(ModelForm):
    class Meta:
        model = Unidades
        exclude = ("unidad_id","created_at","updated_at","created_by","updated_by")

class TipoProductoForm(ModelForm):

    class Meta:
        model = TipoProducto
        exclude = ("created_at","updated_at","created_by","updated_by")

    def __init__(self, *args, **kwargs):
        super(TipoProductoForm, self).__init__(*args, **kwargs)

        #self.fields['cuenta_contable'].queryset = PlanDeCuentas.objects.filter(tipo_cuenta_id=1, categoria="DETALLE")

class LineaForm(ModelForm):

    class Meta:
        model = Linea
        exclude = ("created_at","updated_at","created_by","updated_by")

class ActualizarSubcategoria(UpdateView):
    model = SubCategoriaProducto
    fields = ['codigo_sub_categ', 'categoria', 'descripcion_sub_categ', 'imagen_subcateg']

    success_url = reverse_lazy('subcategoria-producto-list')
    template_name = 'subcategoria_producto/create.html'




    def get_context_data(self,**kwargs):
        context = super(ActualizarSubcategoria,self).get_context_data(**kwargs)
        context['section_title'] = 'Actualizar Subcategoria'
        context['button_text'] = 'Actualizar'
        return context

class ProformaView(TemplateView):

    def get(self, request, *args, **kwargs):

        productos = Producto.objects.all()



        producto_form = ProductoForm()


        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'producto_form':producto_form,

        'productos':productos,

        }

        return render_to_response(
            'producto/proforma.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        producto = Producto.objects.get(producto_id=kwargs['pk'])
        try:
             presupuesto = PresupuestoProducto.objects.get(producto_id=producto.producto_id)
        except PresupuestoProducto.DoesNotExist:
             presupuesto = None

        producto_form = ProductoForm(request.POST,request.FILES,instance=producto)
        presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES,instance=presupuesto)
        p_id=kwargs['pk']
        if producto_form.is_valid() and presupuesto_form.is_valid:

            producto.precio1 = producto_form.cleaned_data['precio1']
            producto.precio2 = producto_form.cleaned_data['precio2']
            producto.precio3 = producto_form.cleaned_data['precio3']
            producto.categoria = producto_form.cleaned_data['categoria']
            producto.sub_categoria = producto_form.cleaned_data['sub_categoria']
            producto.linea = producto_form.cleaned_data['linea']
            producto.save()

            new_producto=producto.save()
            new_presupuesto = presupuesto_form.save()
            #new_presupuesto.producto_id = new_producto.producto_id
            new_presupuesto.save()

            contador=request.POST["columnas_receta"]
            for i in contador:
                kits=Kits()
                kits.padre = producto
                kits.hijo_id=request.POST["id_kits"+i]
                kits.cantidad=request.POST["cantidad_kits"+i]
                #kits.costo=float(request.POST["costo_kits1"])
                kits.total=request.POST["total_kits"+i]
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
            producto_form = ProductoForm(request.POST,request.FILES)
            presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES)

            context = {
            'section_title':'Actualizar ',
            'button_text':'Actualizar',
            'producto_form':producto_form,
            'presupuesto_producto_form':presupuesto_form }

            return render_to_response(
                'producto/producto_form.html',
                context,
                context_instance=RequestContext(request))

class PedidoView(TemplateView):

    def get(self, request, *args, **kwargs):

        productos = Producto.objects.all()



        producto_form = ProductoForm()


        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'producto_form':producto_form,

        'productos':productos,

        }

        return render_to_response(
            'producto/pedido.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        producto = Producto.objects.get(producto_id=kwargs['pk'])
        try:
             presupuesto = PresupuestoProducto.objects.get(producto_id=producto.producto_id)
        except PresupuestoProducto.DoesNotExist:
             presupuesto = None

        producto_form = ProductoForm(request.POST,request.FILES,instance=producto)
        presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES,instance=presupuesto)
        p_id=kwargs['pk']
        if producto_form.is_valid() and presupuesto_form.is_valid:

            producto.precio1 = producto_form.cleaned_data['precio1']
            producto.precio2 = producto_form.cleaned_data['precio2']
            producto.precio3 = producto_form.cleaned_data['precio3']
            producto.categoria = producto_form.cleaned_data['categoria']
            producto.sub_categoria = producto_form.cleaned_data['sub_categoria']
            producto.linea = producto_form.cleaned_data['linea']
            producto.save()

            new_producto=producto.save()
            new_presupuesto = presupuesto_form.save()
            #new_presupuesto.producto_id = new_producto.producto_id
            new_presupuesto.save()

            contador=request.POST["columnas_receta"]
            for i in contador:
                kits=Kits()
                kits.padre = producto
                kits.hijo_id=request.POST["id_kits"+i]
                kits.cantidad=request.POST["cantidad_kits"+i]
                #kits.costo=float(request.POST["costo_kits1"])
                kits.total=request.POST["total_kits"+i]
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
            producto_form = ProductoForm(request.POST,request.FILES)
            presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES)

            context = {
            'section_title':'Actualizar ',
            'button_text':'Actualizar',
            'producto_form':producto_form,
            'presupuesto_producto_form':presupuesto_form }

            return render_to_response(
                'producto/producto_form.html',
                context,
                context_instance=RequestContext(request))

class OrdenProduccionView(TemplateView):

    def get(self, request, *args, **kwargs):

        productos = Producto.objects.all()



        producto_form = ProductoForm()


        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'producto_form':producto_form,

        'productos':productos,

        }

        return render_to_response(
            'producto/ordenproduccion.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        producto = Producto.objects.get(producto_id=kwargs['pk'])
        try:
             presupuesto = PresupuestoProducto.objects.get(producto_id=producto.producto_id)
        except PresupuestoProducto.DoesNotExist:
             presupuesto = None

        producto_form = ProductoForm(request.POST,request.FILES,instance=producto)
        presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES,instance=presupuesto)
        p_id=kwargs['pk']
        if producto_form.is_valid() and presupuesto_form.is_valid:

            producto.precio1 = producto_form.cleaned_data['precio1']
            producto.precio2 = producto_form.cleaned_data['precio2']
            producto.precio3 = producto_form.cleaned_data['precio3']
            producto.categoria = producto_form.cleaned_data['categoria']
            producto.sub_categoria = producto_form.cleaned_data['sub_categoria']
            producto.linea = producto_form.cleaned_data['linea']
            producto.save()

            new_producto=producto.save()
            new_presupuesto = presupuesto_form.save()
            #new_presupuesto.producto_id = new_producto.producto_id
            new_presupuesto.save()

            contador=request.POST["columnas_receta"]
            for i in contador:
                kits=Kits()
                kits.padre = producto
                kits.hijo_id=request.POST["id_kits"+i]
                kits.cantidad=request.POST["cantidad_kits"+i]
                #kits.costo=float(request.POST["costo_kits1"])
                kits.total=request.POST["total_kits"+i]
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
            producto_form = ProductoForm(request.POST,request.FILES)
            presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES)

            context = {
            'section_title':'Actualizar ',
            'button_text':'Actualizar',
            'producto_form':producto_form,
            'presupuesto_producto_form':presupuesto_form }

            return render_to_response(
                'producto/producto_form.html',
                context,
                context_instance=RequestContext(request))

class GuiaRemisionView(TemplateView):

    def get(self, request, *args, **kwargs):

        productos = Producto.objects.all()



        producto_form = ProductoForm()


        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'producto_form':producto_form,

        'productos':productos,

        }

        return render_to_response(
            'producto/guia.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        producto = Producto.objects.get(producto_id=kwargs['pk'])
        try:
             presupuesto = PresupuestoProducto.objects.get(producto_id=producto.producto_id)
        except PresupuestoProducto.DoesNotExist:
             presupuesto = None

        producto_form = ProductoForm(request.POST,request.FILES,instance=producto)
        presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES,instance=presupuesto)
        p_id=kwargs['pk']
        if producto_form.is_valid() and presupuesto_form.is_valid:

            producto.precio1 = producto_form.cleaned_data['precio1']
            producto.precio2 = producto_form.cleaned_data['precio2']
            producto.precio3 = producto_form.cleaned_data['precio3']
            producto.categoria = producto_form.cleaned_data['categoria']
            producto.sub_categoria = producto_form.cleaned_data['sub_categoria']
            producto.linea = producto_form.cleaned_data['linea']
            producto.save()

            new_producto=producto.save()
            new_presupuesto = presupuesto_form.save()
            #new_presupuesto.producto_id = new_producto.producto_id
            new_presupuesto.save()

            contador=request.POST["columnas_receta"]
            for i in contador:
                kits=Kits()
                kits.padre = producto
                kits.hijo_id=request.POST["id_kits"+i]
                kits.cantidad=request.POST["cantidad_kits"+i]
                #kits.costo=float(request.POST["costo_kits1"])
                kits.total=request.POST["total_kits"+i]
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
            producto_form = ProductoForm(request.POST,request.FILES)
            presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES)

            context = {
            'section_title':'Actualizar ',
            'button_text':'Actualizar',
            'producto_form':producto_form,
            'presupuesto_producto_form':presupuesto_form }

            return render_to_response(
                'producto/producto_form.html',
                context,
                context_instance=RequestContext(request))

class ReunionView(TemplateView):

    def get(self, request, *args, **kwargs):

        productos = Producto.objects.all()



        producto_form = ProductoForm()


        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'producto_form':producto_form,

        'productos':productos,

        }

        return render_to_response(
            'producto/reunion.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        producto = Producto.objects.get(producto_id=kwargs['pk'])
        try:
             presupuesto = PresupuestoProducto.objects.get(producto_id=producto.producto_id)
        except PresupuestoProducto.DoesNotExist:
             presupuesto = None

        producto_form = ProductoForm(request.POST,request.FILES,instance=producto)
        presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES,instance=presupuesto)
        p_id=kwargs['pk']
        if producto_form.is_valid() and presupuesto_form.is_valid:

            producto.precio1 = producto_form.cleaned_data['precio1']
            producto.precio2 = producto_form.cleaned_data['precio2']
            producto.precio3 = producto_form.cleaned_data['precio3']
            producto.categoria = producto_form.cleaned_data['categoria']
            producto.sub_categoria = producto_form.cleaned_data['sub_categoria']
            producto.linea = producto_form.cleaned_data['linea']
            producto.save()

            new_producto=producto.save()
            new_presupuesto = presupuesto_form.save()
            #new_presupuesto.producto_id = new_producto.producto_id
            new_presupuesto.save()

            contador=request.POST["columnas_receta"]
            for i in contador:
                kits=Kits()
                kits.padre = producto
                kits.hijo_id=request.POST["id_kits"+i]
                kits.cantidad=request.POST["cantidad_kits"+i]
                #kits.costo=float(request.POST["costo_kits1"])
                kits.total=request.POST["total_kits"+i]
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
            producto_form = ProductoForm(request.POST,request.FILES)
            presupuesto_form = PresupuestoProductoForm(request.POST,request.FILES)

            context = {
            'section_title':'Actualizar ',
            'button_text':'Actualizar',
            'producto_form':producto_form,
            'presupuesto_producto_form':presupuesto_form }

            return render_to_response(
                'producto/producto_form.html',
                context,
                context_instance=RequestContext(request))

class AnalisisInventarioForm(forms.ModelForm):
    #categoria = forms.ModelChoiceField(queryset=CategoriaProducto.objects.all())

    class Meta:
        model = AnalisisInventario
        #cuenta_compra y cuenta_venta verificar donde se lo utiiza
        fields = ('codigo','fecha','bodega','descripcion')

    def __init__(self, *args, **kwargs):
        super(AnalisisInventarioForm, self).__init__(*args, **kwargs)


class ProductoGeneralForm(forms.ModelForm):
    #categoria = forms.ModelChoiceField(queryset=CategoriaProducto.objects.all())

    class Meta:
        model = ProductoGeneral
        #cuenta_compra y cuenta_venta verificar donde se lo utiiza
        fields = ("codigo","descripcion","precio1","precio2")

    def __init__(self, *args, **kwargs):
        super(ProductoGeneralForm, self).__init__(*args, **kwargs)
