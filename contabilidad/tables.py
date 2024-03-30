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


class EjercicioContableTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('fecha_inicio', 'fecha_fin','abierto','created_at','created_by',)


	def render_action(self, value):
		delete = reverse_lazy('ejerciciocontable-delete-pk', args=[value])
		update = reverse_lazy('ejerciciocontable-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  EjercicioContable
		fields = ('id_row', 'fecha_inicio', 'fecha_fin', 'abierto')

class PlanDeCuentasTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('codigo_plan', 'nombre_plan', 'grupo','created_at','created_by',)

	def render_action(self, value):
		delete = reverse_lazy('plandecuentas-delete-pk', args=[value])
		update = reverse_lazy('plandecuentas-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  PlanDeCuentas
		fields = ('id_row', 'codigo_plan', 'nombre_plan', 'tipo_cuenta', )


class TipoCuentaTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('nombre_tipo','created_at','created_by',)


	def render_action(self, value):
		delete = reverse_lazy('tipocuenta-delete-pk', args=[value])
		update = reverse_lazy('tipocuenta-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  TipoCuenta
		fields = ('id_row', 'nombre_tipo', 'acreedora', 'deudora',)

        
class CentroCostoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('nombre_centro', 'padre', 'created_at','created_by',)

	def render_action(self, value):
		delete = reverse_lazy('centrocosto-delete-pk', args=[value])
		update = reverse_lazy('centrocosto-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  CentroCosto
		fields = ('id_row', 'nombre_centro', 'padre')

class AsientoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('fecha', 'codigo_asiento', 'created_at','created_by',)


	def render_action(self, value):
		delete = reverse_lazy('asiento-delete-pk', args=[value])
		update = reverse_lazy('asiento-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  Asiento
		fields = ('id_row', 'codigo_asiento', 'fecha', 'glosa')