# coding: utf-8
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.html import escape
from datetime import datetime
import django_tables2 as tables
from .models import *
from muedirsa.models import *

def action_html(value, delete, update, ):
	td_str = '<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Editar</a><a onclick="if(confirm(\'Confirmar Eliminaciones\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Cambiar Estado</a>'
	return mark_safe(td_str)


class AreasTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
		delete = reverse_lazy('areas-delete-pk', args=[value])
		update = reverse_lazy('areas-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Areas
		fields = ('id_row', 'codigo', 'descripcion','costo_hora','action')


class VehiculoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
		delete = reverse_lazy('vehiculo-delete-pk', args=[value])
		update = reverse_lazy('vehiculo-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Vehiculo
		fields = ('id_row','placa','marca','action')

class EstadosProTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
		delete = reverse_lazy('estadospro-delete-pk', args=[value])
		update = reverse_lazy('estadospro-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  EstadosPro
		fields = ('id_row','codigo','descripcion','action')

class TipoMuebTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
		delete = reverse_lazy('tipomueb-delete-pk', args=[value])
		update = reverse_lazy('tipomueb-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  TipoMueb
		fields = ('id_row','codigo','descripcion','action')

class SecuencialesTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
		delete = reverse_lazy('secuenciales-delete-pk', args=[value])
		update = reverse_lazy('secuenciales-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Secuenciales
		fields = ('id_row','modulo','secuencial','action')

class MenuTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
		delete = reverse_lazy('menu-delete-pk', args=[value])
		update = reverse_lazy('menu-update', args=[value])
		grupo = reverse_lazy('menu-group-list')
		return mark_safe('<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Editar</a><a href="'+str(grupo)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Grupos</a><a onclick="if(confirm(\'Confirmar Eliminaciones\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Eliminar</a>')

	class Meta:
		model =  Menu
		fields = ('id_row','nom_option','cod_parent','num_order','action')

class MenuGroupTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
		delete = reverse_lazy('menu-group-delete-pk', args=[value])
		update = reverse_lazy('menu-group-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  MenuGroup
		fields = ('id_row','menu','group','sts_show','action')

class TipoLugarTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
		delete = reverse_lazy('tipolugar-delete-pk', args=[value])
		update = reverse_lazy('tipolugar-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  TipoLugar
		fields = ('id_row', 'codigo', 'descripcion','action')
class PuntosVentaTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
		delete = reverse_lazy('puntosventa-delete-pk', args=[value])
		update = reverse_lazy('puntosventa-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  PuntosVenta
		fields = ('id_row', 'codigo', 'nombre','action')