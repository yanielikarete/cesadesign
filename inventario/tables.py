# coding: utf-8
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.html import escape
from datetime import datetime
import django_tables2 as tables
from .models import *
from muedirsa.models import *
from django_tables2.utils import A  # alias for Accessor


def action_html(value, delete, update, ):
	td_str = '<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Editar</a><a onclick="if(confirm(\'Confirmar Eliminaciones\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Eliminar</a>'
	return mark_safe(td_str)


class ProductoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo_producto','descripcion_producto','created_at','created_by',)

	def render_action(self, value):
		delete = reverse_lazy('producto-delete-pk', args=[value])
		update = reverse_lazy('actualizar-producto', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Producto
		fields = ('id_row', 'codigo_producto', 'descripcion_producto','action')

class CategoriaProductoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	def render_action(self, value):
		delete = reverse_lazy('categoria-producto-delete-pk', args=[value])
		update = reverse_lazy('categoria-producto-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  CategoriaProducto
		fields = ('id_row', 'codigo_categoria', 'descripcion_categoria','action')

class BodegaTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo_bodega','nombre','direccion1','created_at','created_by',)

	def render_action(self, value,record):
		delete = reverse_lazy('bodega-delete-pk', args=[value])
		update = reverse_lazy('bodega-update', args=[value])
		# if record.activo == True:
		# 	return mark_safe('<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Editar</a><a onclick="if(confirm(\'Confirmar Eliminaciones\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Inactivar</a>')
		# else:
		# 	return mark_safe('<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i>Editar</a><a onclick="if(confirm(\'Confirmar Eliminaciones\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Activar</a>')
   		return mark_safe('<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i>Editar</a><a onclick="if(confirm(\'Confirmar Cambiar Estado\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Cambiar Estado</a>')



	class Meta:
		model =  Bodega
		fields = ('id_row', 'codigo_bodega', 'nombre','direccion1', 'activo_bodega','action')

class SubCategoriaProductoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo_sub_categ','descripcion_sub_categ','predeterminado','created_at','created_by',)

	def render_action(self, value):
		delete = reverse_lazy('subcategoria-producto-delete-pk', args=[value])
		update = reverse_lazy('subcategoria-producto-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  SubCategoriaProducto
		fields = ('id_row', 'codigo_sub_categ', 'descripcion_sub_categ','action')

class KardexTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('fecha_ingreso','descripcion','tipo','bodega_id','producto','cantidad',)
        def render_action(self, value):
		delete = reverse_lazy('kardex-delete-pk', args=[value])
		update = reverse_lazy('kardex-update', args=[value])
		return mark_safe('')

	
	class Meta:
		model =  Kardex
		fields = ('id_row','fecha_ingreso','descripcion','tipo','bodega_id','producto','cantidad','action')

class SerialesTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('nro_serial','producto','ingresado','nro_doc_ingreso','nro_doc_salida',)

	def render_action(self, value):
		delete = reverse_lazy('seriales-delete-pk', args=[value])
		update = reverse_lazy('seriales-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Seriales
		fields = ('id_row', 'nro_serial', 'producto','nro_doc_ingreso','nro_doc_salida','action')

class LoteTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('nro_lote','producto','descripcion_lote','fecha_ingreso',)

	
	class Meta:
		model =  Lote
		fields = ('id_row','nro_lote','nro_documento','producto','descripcion_lote','fecha_ingreso','cantidad','action')

class UnidadesTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('abreviatura','descripcion_unidad','created_at','created_by',)


	def render_action(self, value):
		delete = reverse_lazy('unidades-delete-pk', args=[value])
		update = reverse_lazy('unidades-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Unidades
		fields = ('id_row', 'abreviatura', 'descripcion_unidad','action')

class TipoProductoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	
	def render_action(self, value,record):
		delete = reverse_lazy('tipo-producto-delete-pk', args=[value])
		update = reverse_lazy('tipo-producto-update', args=[value])
		act=tables.A('activo')
		if tables.Column('activo')== True:
			return mark_safe('<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Editar</a><a onclick="if(confirm(\'Confirmar Eliminaciones\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Inactivar</a>')
		else:
			return mark_safe('<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Editar</a><a onclick="if(confirm(\'Confirmar Eliminaciones\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Activar</a>')



	
	class Meta:
		model =  TipoProducto
		fields = ('id_row','codigo','descripcion','activo','action')

class LineaTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	
	def render_action(self, value):
		delete = reverse_lazy('linea-delete-pk', args=[value])
		update = reverse_lazy('linea-update', args=[value])
		return action_html(value, delete, update)


	
	class Meta:
		model = Linea
		fields = ('id_row','codigo','descripcion','action')
class ProductoEnBodegaTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
		delete = reverse_lazy('producto-delete-pk', args=[value])
		update = reverse_lazy('actualizar-producto', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  ProductoEnBodega
		fields = ('id_row', 'producto', 'bodega','action')

class AnalisisInventarioTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo','fecha','bodega','descripcion')

	def render_action(self, value):
		delete = reverse_lazy('analisis-delete-pk', args=[value])
		update = reverse_lazy('analisis-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  AnalisisInventario
		fields = ('id_row', 'codigo','fecha','bodega','descripcion','action')
