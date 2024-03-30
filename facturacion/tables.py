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


class GuiaRemisionTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('nro_guia', 'cliente', 'chofer','created_at','created_by',)

	def render_action(self, value):
		delete = reverse_lazy('guiaremision-delete-pk', args=[value])
		update = reverse_lazy('guiaremision-update', args=[value])
		imprimir = reverse_lazy('guiaremision-imprimir', args=[value])

		#return action_html(value, delete, update)
		return mark_safe('<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i> Editar</a><a href="'+str(imprimir)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Imprimir</a>')

	class Meta:
		model =  GuiaRemision
		fields = ('id_row', 'nro_guia', 'cliente', 'chofer','action')

# class FacturaTable(tables.Table):
# 	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
# 	
# 	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
# 	fields_report = ('nro_factura', 'cliente', 'vendedor','created_at','created_by',)
# 
# 	def render_action(self, value):
# 		delete = reverse_lazy('factura-delete-pk', args=[value])
# 		update = reverse_lazy('factura-update', args=[value])
# 		return action_html(value, delete, update)
# 
# 	class Meta:
# 		model =  Factura
# 		fields = ('id_row', 'nro_factura', 'cliente', 'vendedor','action')
# 
# class NotaCreditoTable(tables.Table):
# 	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
# 	
# 	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
# 	fields_report = ('nro_nota_credito', 'cliente', 'vendedor','created_at','created_by',)
# 
# 	def render_action(self, value):
# 		delete = reverse_lazy('nota-credito-delete-pk', args=[value])
# 		update = reverse_lazy('nota-credito-update', args=[value])
# 		return action_html(value, delete, update)
# 
# 	class Meta:
# 		model =  NotaCredito
# 		fields = ('id_row', 'nro_nota_credito', 'cliente', 'vendedor','action')