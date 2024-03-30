from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',
                       
      url(
    r'^OrdenEgreso/conceptos/$',
                         'ordenEgreso.views.ConceptoOrdenEgresoListView',
                         name='concepto-orden-egreso-list',
                       ),

                       url(
                           r'^OrdenEgreso/conceptos/nuevo$',
                           ConceptoOrdenEgresoCreateView.as_view(),
                           name='concepto-orden-egreso-create',
                       ),
                       url(
                           r'^OrdenEgreso/conceptos/(?P<pk>\d+)/editar/$',
                           ConceptoOrdenEgresoUpdateView.as_view(),
                           name='concepto-orden-egreso-update',
                       ),                 

   url(
        r'^OrdenEgreso/$',
       'ordenEgreso.views.OrdenEgresoListView',
        name='ordenegreso-list',
    ),

   url(
        r'^OrdenEgreso/nuevo$',
        'ordenEgreso.views.OrdenEgresoCreateView',
        name='ordenegreso-create',
    ),


   url(
         r'^OrdenEgreso/(?P<pk>\d+)/editar/$',
         'ordenEgreso.views.OrdenEgresoUpdateView',
         name='ordenegreso-update',
    ),
   url(
         r'^OrdenEgreso/(?P<pk>\d+)/despachar/$',
         'ordenEgreso.views.OrdenEgresoUpdateView',
         name='ordenegreso-despachar',
    ),
   url(
         r'^OrdenEgreso/(?P<pk>\d+)/actualizar/$',
       'ordenEgreso.views.OrdenEgresoActualizarView',
         name='ordenegreso-actualizar',
    ),
   url(
        r'^OrdenEgreso/(?P<pk>\d+)/detalle/$',
        OrdenEgresoDetailView.as_view(),
        name='ordenegreso-detail',
    ),
    url(
        r'^OrdenEgreso/eliminar/$',
        'ordenEgreso.views.ordenegresoEliminarView',
        name='ordenegreso-delete',
    ),
    url(
        r'^OrdenEgreso/(?P<pk>\d+)/eliminar/$',
        'ordenEgreso.views.ordenegresoEliminarByPkView',
        name='ordenegreso-delete-pk',
    ),

   url(
       r'^OrdenEgresoReversar/$',
       'ordenEgreso.views.OrdenEgresoListReversarView',
       name='ordenegreso-list-reversa',
   ),

   url(
        r'^OrdenEgresoAprobar/$',
        'ordenEgreso.views.OrdenEgresoListAprobarView',
        name='ordenegreso-list-aprobada',
   ),


   url(
        r'^OrdenEgreso/(?P<pk>\d+)/aprobar/$',
        'ordenEgreso.views.ordenegresoAprobarByPkView',
        name='aprobar-orden-egreso',
    ),

   url(
       r'^OrdenEgreso/(?P<pk>\d+)/reversar/$',
       'ordenEgreso.views.ordenegresoReversarByPkView',
       name='reversa-orden-egreso',
   ),

    url(
        r'^EgresoOrdenEgreso/$',
        'ordenEgreso.views.EgresoOrdenEgresoListView',
        name='egresoordenegreso-list',
    ),


    url(
        r'^error500/$',
        'ordenEgreso.views.BadError500',
        name='BadError500',
    ),

    url(
        r'^EgresoOrdenEgreso/crear$',
        'ordenEgreso.views.EgresoOrdenEgresoCreateView',
        name='egresoordenegreso-create',
    ),
    url(
         r'^EgresoOrdenEgreso/(?P<pk>\d+)/editar/$',
         'ordenEgreso.views.EgresoOrdenEgresoUpdateView',
         name='egresoordenegreso-update',
    ),
    url(
        r'^OrdenEgreso/imprimir/(?P<pk>\d+)/$',
        'ordenEgreso.views.index',
        name='ordenegreso-imprimir',
    ),
    url(
        r'^OrdenEgreso/imprimiregresoporordenegreso/(?P<pk>\d+)/$',
        'ordenEgreso.views.imprimirEgresoxOrden',
        name='ordenegreso-imprimir-egresoxordenegreso',
    ),
    url(
         r'^OrdenEgreso/(?P<pk>\d+)/actualizarHistorico/$',
        'ordenEgreso.views.OrdenEgresoActualizarHistoricoView',
         name='ordenegreso-actualizar-historico',
    ),
    url(
        r'^OrdenEgresoHistorico/$',
         'ordenEgreso.views.OrdenEgresoListHistoricoView',
        name='egresoordenegreso-list-historico',
    ),

        url(r'^OrdenEgreso/export/(?P<pk>\d+)/$',
         'ordenEgreso.views.export_to_excel', name='export_to_excel'),

                       url(
                           r'^OrdenEgreso/imprimirOrdenEgreso/(?P<pk>\d+)/$',
                           'ordenEgreso.views.indexOrdenEgreso',
                           name='ordenegreso-nuevo-imprimir',
                       ),
                       url(
                           r'^OrdenEgreso/imprimirEgresoxOrdenNuevo/(?P<pk>\d+)/$',
                           'ordenEgreso.views.imprimirEgresoxOrdenNuevo',
                           name='egreso-ordenegreso-nuevo-imprimir',
                       ),
                       url(
                           r'^egresoporOrdenEgresoReversarListView/$',
                           'ordenEgreso.views.egresoporOrdenEgresoReversarListView',
                           name='egresoordenegreso-list-reversar',
                       ),

                       url(
                           r'^EgresoOrdenEgreso/(?P<pk>\d+)/reversar/$',
                           'ordenEgreso.views.egresoporOrdenEgresoReversar',
                           name='reversar-orden-egreso',
                       ),
                       
    url(r'^OrdenEgreso/ordenEgresoPrueba$','ordenEgreso.views.orden_egreso_list_prueba', name='orden-egreso-list-prueba', ),
	url(r'^orden_egreso/api$','ordenEgreso.views.orden_egreso_api_view', name='orden-egreso-api', ),
	url(r'^egreso_orden_egreso/api$','ordenEgreso.views.egreso_orden_egreso_api_view', name='egreso-orden-egreso-api', ),
    
    url(
       r'^OrdenEgreso/imprimirEgresoxOrdenFinal/(?P<pk>\d+)/$',
       'ordenEgreso.views.imprimir_orden_egreso_actual',
       name='egreso-ordenegreso-actual-imprimir',
   ),

        #Agregar API para reversar
    	url(r'^orden_egreso_aprobar/api$','ordenEgreso.views.orden_egreso_aprobada_api_view', name='orden-egreso-aprobada-api', ),

        #url(r'^orden_egreso_reversar/api$','ordenEgreso.views.orden_egreso_reversada_api_view', name='orden-egreso-reversada-api', ),


)
