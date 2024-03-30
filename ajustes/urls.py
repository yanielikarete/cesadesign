from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',

   url(
        r'^ajustes/$',
        'ajustes.views.AjustesListView',
        name='ajustes-list',
    ),

   url(
        r'^ajustes/nuevo$',
        'ajustes.views.AjustesCreateView',
        name='ajustes-create',
    ),

   url(
         r'^ajustes/(?P<pk>\d+)/editar/$',
         'ajustes.views.AjustesUpdateView',
         name='ajustes-update',
    ),
   # url(
   #       r'^ajustes/(?P<pk>\d+)/despachar/$',
   #       'ajustes.views.AjustesUpdateView',
   #       name='ajustes-despachar',
   #  ),
    url(
        r'^ajustes/(?P<pk>\d+)/actualizar/$',
        'ajustes.views.AjustesActualizarView',
        name='ajustes-actualizar',
    ),

    url(
        r'^ajustes/(?P<pk>\d+)/detalle/$',
        AjustesDetailView.as_view(),
        name='ajustes-detail',
    ),
    url(
        r'^ajustes/eliminar/$',
        'ajustes.views.ajustesEliminarView',
        name='ajustes-delete',
    ),
    url(
        r'^ajustes/(?P<pk>\d+)/eliminar/$',
        'ajustes.views.ajustesEliminarByPkView',
        name='ajustes-delete-pk',
    ),
    url(
        r'^ajustesAprobar/$',
        'ajustes.views.AjustesListAprobarView',
        name='ajustes-list-aprobada',
    ),

    url(
        r'^ajustes/(?P<pk>\d+)/aprobar/$',
        'ajustes.views.ajustesAprobarByPkView',
        name='aprobar-ajustes',
    ),
    # url(
    #     r'^IngresoOrdenIngreso/$',
    #     IngresoOrdenIngresoListView.as_view(),
    #     name='ingresoordeningreso-list',
    # ),
    # url(
    #     r'^IngresoOrdenIngreso/crear$',
    #     'ordenIngreso.views.IngresoOrdenIngresoCreateView',
    #
    #     name='ingresoordeningreso-create',
    # ),
    # url(
    #      r'^IngresoOrdenIngreso/(?P<pk>\d+)/editar/$',
    #      'ordenIngreso.views.IngresoOrdenIngresoUpdateView',
    #      name='ingresoordeningreso-update',
    # ),
    url(
        r'^ajustes/(?P<pk>\d+)/nuevarecepcion/$',
        'ajustes.views.ajustesNuevoRecepcionByPkView',
        name='ajustes-nuevo-recepcion',
    ),
    url(
        r'^ajustes/(?P<pk>\d+)/imprimir/$',
        'ajustes.views.index',
        name='ajustes-imprimir',
    ),
 
    url(
        r'^ajustes/conceptosAjustes/$',
        'ajustes.views.ConceptoAjustesListView',
        name='concepto-ajustes-list',
    ),

    url(
        r'^ajustes/conceptos/nuevo$',
        ConceptoAjustesCreateView.as_view(),
        name='concepto-ajustes-create',
    ),

    url(
        r'^ajustes/conceptos/(?P<pk>\d+)/editar/$',
        ConceptoAjustesUpdateView.as_view(),
        name='concepto-ajustes-update',
    ),

    url(
        r'^ajustes/corregirAjustes/(?P<pk>\d+)/editar/$',
        'ajustes.views.corregirAjustesAsiento',
        name='corregir-ajustes-asiento',
    ),

)