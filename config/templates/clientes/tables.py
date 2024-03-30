# coding: utf-8
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.html import escape
from datetime import datetime
import django_tables2 as tables
from .models import *
from clientes.models import *

def action_html(value, delete, update, ):
	td_str = '<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Editar</a><a onclick="if(confirm(\'Confirmar Eliminaciones\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Eliminar</a>'
	return mark_safe(td_str)


class ClienteTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo_cliente','nombre_cliente','created_at','created_by',)

	def render_action(self, value):
		delete = reverse_lazy('cliente-delete-pk', args=[value])
		update = reverse_lazy('cliente-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Cliente
		fields = ('id_row', 'codigo_cliente', 'nombre_cliente','action')

class RazonSocialTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo_razon_social','nombre','created_at','created_by',)

	def render_action(self, value):
		delete = reverse_lazy('razonsocial-delete-pk', args=[value])
		update = reverse_lazy('razonsocial-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  RazonSocial
		fields = ('id_row', 'codigo_razon_social', 'nombre','action')
