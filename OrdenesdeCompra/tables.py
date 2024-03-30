# coding: utf-8
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.html import escape
from datetime import datetime
import django_tables2 as tables
from .models import *
from muedirsa.models import *

def action_html(value, delete, update, ):
	td_str = '<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Editar</a><a onclick="if(confirm(\'Confirmar Eliminaciones\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Eliminar</a>'
	return mark_safe(td_str)


class OrdenCompraTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('nro_compra','proveedor','created_at','created_by',)

	def render_action(self, value):
		delete = reverse_lazy('ordenescompra-delete-pk', args=[value])
		update = reverse_lazy('ordenescompra-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  OrdenCompra
		fields = ('id_row', 'nro_compra', 'proveedor','action')

class OrdenCompraAprobadaTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	#selected_action = tables.CheckBoxColumn(accessor='pk', orderable=False, attrs={"th": {"id": "action-toggle", "class": "action-checkbox"}, "td": {"class": "action-checkbox"}, "class":"action-select", "name":"selected_action",})
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value):
	    notas = reverse_lazy('aprobar-orden-compra', args=[value])
	    td_str = '<a href="%s" title="Aprobar Orden de Compra" class="pull-right"><i class="fa fa-pencil-square-o"></i> Aprobar</a>' % str(notas)
	    return mark_safe(td_str)

	class Meta:
		model = OrdenCompra
		fields = ('id_row','nro_compra', 'proveedor','created_at','created_by','action')

class ComprasLocalesTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('nro_compra','proveedor','created_at','created_by',)

	def render_action(self, value):
		delete = reverse_lazy('ordenescompra-delete-pk', args=[value])
		update = reverse_lazy('ordenescompra-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  OrdenCompra
		fields = ('id_row', 'nro_compra', 'proveedor','action')