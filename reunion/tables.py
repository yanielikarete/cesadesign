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


class ReunionTable(tables.Table):
	id_row = tables.Column(accessor='pk', orderable=False, visible=False,)
	
	action = tables.Column("Acciones", accessor='pk', orderable=False, attrs={"th": {"class": "print-no"}, "td": {"class": "print-no"}})

	def render_action(self, value,record):
		delete = reverse_lazy('reunion-delete-pk', args=[value])
		update = reverse_lazy('reunion-actualizar', args=[value])
		return mark_safe('<a href="'+str(update)+'" class="btn btn-primary" style="margin-right: 15px;"><i class="fa fa-pencil-square-o"></i>Editar</a><a onclick="if(confirm(\'Confirmar Cambiar Estado\')){eliminarFila(this)};return false;" href="'+str(delete)+'" data-id="'+str(value)+'" class="print-no btn btn-danger"><i class="fa fa-trash-o"></i> Cambiar Estado</a>')



	class Meta:
		model =  Bodega
		fields = ('id_row', 'codigo', 'fecha','motivo', 'observacion','action')

