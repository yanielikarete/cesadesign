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


# class ProformaTable(tables.Table):
# 	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
#
# 	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
# 	fields_report = ('fecha', 'created_at','created_by',)
#
#
# 	def render_action(self, value):
# 		delete = reverse_lazy('proforma-delete-pk', args=[value])
# 		update = reverse_lazy('proforma-update', args=[value])
# 		return action_html(value, delete, update)
#
# 	class Meta:
# 		model =  Proforma
# 		fields = ('id_row', 'fecha', 'cliente')

class RegistroDocumentoTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})
	fields_report = ('fecha', 'created_at','created_by',)


	def render_action(self, value):
		delete = reverse_lazy('registrodocumento-delete-pk', args=[value])
		update = reverse_lazy('registrodocumento-update', args=[value])
		return action_html(value, delete, update)

	class Meta:
		model =  RegistroDocumento
		fields = ('id_row', 'fecha', 'cliente')
