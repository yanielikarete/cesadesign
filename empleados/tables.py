# coding: utf-8
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.html import escape
from datetime import datetime
import django_tables2 as tables
from .models import *

def action_html(value, delete, update, ):
	td_str = '<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Editar</a><a onclick="if(confirm(\'Confirmar Eliminaciones\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Eliminar</a>'
	return mark_safe(td_str)

class EmpleadoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo_empleado', 'cedula_empleado','nombre_empleado','created_at','created_by',)


	def render_action(self, value):
		delete = reverse_lazy('empleado-delete-pk', args=[value])
		update = reverse_lazy('empleado-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Empleado
		fields = ('id_row', 'codigo_empleado', 'cedula_empleado','nombre_empleado','action')


class TipoEmpleadoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('cargo_empleado', 'descripcion_tipo', 'created_at','created_by',)


	def render_action(self, value):
		delete = reverse_lazy('tipoempleado-delete-pk', args=[value])
		update = reverse_lazy('tipoempleado-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  TipoEmpleado
		fields = ('id_row', 'cargo_empleado', 'descripcion_tipo','action')


class VendedorTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo_vendedor', 'empleado','comision','created_at','created_by',)


	def render_action(self, value):
		delete = reverse_lazy('vendedor-delete-pk', args=[value])
		update = reverse_lazy('vendedor-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Empleado
		fields = ('id_row', 'codigo_vendedor', 'empleado', 'comision','action')

class ChoferTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo_chofer', 'empleado', 'created_at','created_by',)


	def render_action(self, value):
		delete = reverse_lazy('chofer-delete-pk', args=[value])
		update = reverse_lazy('chofer-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Empleado
		fields = ('id_row', 'codigo_chofer', 'empleado', 'action')

class VehiculoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('placa', 'modelo','created_at','created_by',)


	def render_action(self, value):
		delete = reverse_lazy('vehiculo-delete-pk', args=[value])
		update = reverse_lazy('vehiculo-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Empleado
		fields = ('id_row', 'placa', 'modelo', 'action')

class DepartamentoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo', 'nombre')


	def render_action(self, value):
		delete = reverse_lazy('departamento-delete-pk', args=[value])
		update = reverse_lazy('departamento-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Empleado
		fields = ('id_row', 'codigo', 'nombre','action')
