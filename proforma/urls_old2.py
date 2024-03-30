
from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',

    url(
        r'^proforma/$',
        ProformaListView.as_view(),
        name='proforma-list',
    ),
    
    url(
        r'^consultarproforma/$',
        ConsultaProformaListView.as_view(),
        name='proforma-consultar-list',
    ),
    url(
        r'^proforma_render/$',
        ProformaRenderListView.as_view(),
        name='proforma-render-list',
    ),

   url(
        r'^proforma/nuevo$',
	'proforma.views.ProformaCreateView',
        name='proforma-create',
    ),
   url(
        r'^proforma/pdf$',
	'proforma.views.libro_pdf',
        name='proforma-pdf',
    ),
   url(
        r'^proforma/(?P<pk>\d+)/crear$',
    'proforma.views.ProformaCreateReunionView',
        name='proforma-create-reunion',
    ),
   url(
        r'^proforma/seguimiento_reuniones$',
    'proforma.views.SeguimientoReuniones',
        name='proforma-seguimiento',
    ),
   url(
         r'^proforma/(?P<pk>\d+)/editar/$',
         ProformaUpdateView.as_view(),
         name='proforma-update',
    ),
   url(
         r'^proforma/(?P<pk>\d+)/subirrender/$',
         ProformaRenderView.as_view(),
         name='proforma-subir-render',
    ),
   url(
        r'^proforma/(?P<pk>\d+)/detalle/$',
        ProformaDetailView.as_view(),
        name='proforma-detail',
    ),
    url(
        r'^proforma/eliminar/$',
        'proforma.views.ProformaEliminarView',
        name='proforma-delete',
    ),
    url(
        r'^proforma/(?P<pk>\d+)/eliminar/$',
        'proforma.views.ProformaEliminarByPkView',
        name='proforma-delete-pk',
    ),
    url(
        r'^proforma/guardar/$',
        'proforma.views.misProformaGuardar',
        name='configuracion-proforma-guardar',
    ),
    url(
        r'^proformaAprobar/$',
        ProformaListAprobarView.as_view(),
        name='proforma-list-aprobada',
    ),

    url(
        r'^proforma/(?P<pk>\d+)/aprobar/$',
        'proforma.views.ProformaAprobarByPkView',
        name='aprobar-proforma',
    ),
)