from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',

   url(
        r'^ordenIngreso/$',
        'ordenIngreso.views.OrdenIngresoListView',
        name='ordeningreso-list',
    ),

   url(
        r'^ordenIngreso/nuevo$',
        'ordenIngreso.views.OrdenIngresoCreateView',
        name='ordeningreso-create',
    ),
   

   url(
         r'^ordenIngreso/(?P<pk>\d+)/editar/$',
         'ordenIngreso.views.OrdenIngresoUpdateView',
         name='ordeningreso-update',
    ),
   url(
         r'^ordenIngreso/(?P<pk>\d+)/despachar/$',
         'ordenIngreso.views.OrdenIngresoUpdateView',
         name='ordeningreso-despachar',
    ),
   url(
         r'^ordenIngreso/(?P<pk>\d+)/actualizar/$',
           #OrdenIngresoActualizarView.as_view(),
           'ordenIngreso.views.OrdenIngresoActualizarView',
         name='ordeningreso-actualizar',
    ),
   url(
        r'^ordenIngreso/(?P<pk>\d+)/detalle/$',
        OrdenIngresoDetailView.as_view(),
        name='ordeningreso-detail',
    ),
    url(
        r'^ordenIngreso/eliminar/$',
        'ordenIngreso.views.ordeningresoEliminarView',
        name='ordeningreso-delete',
    ),
    url(
        r'^ordenIngreso/(?P<pk>\d+)/eliminar/$',
        'ordenIngreso.views.ordeningresoEliminarByPkView',
        name='ordeningreso-delete-pk',
    ),
    url(
        r'^ordenIngresoAprobar/$',
        'ordenIngreso.views.OrdenIngresoListAprobarView',
        name='ordeningreso-list-aprobada',
    ),

    url(
        r'^OrdenIngreso/(?P<pk>\d+)/aprobar/$',
        'ordenIngreso.views.ordeningresoAprobarByPkView',
        name='aprobar-orden-ingreso',
    ),
    url(
        r'^IngresoOrdenIngreso/$',
        IngresoOrdenIngresoListView.as_view(),
        name='ingresoordeningreso-list',
    ),
    url(
        r'^IngresoOrdenIngreso/crear$',
        'ordenIngreso.views.IngresoOrdenIngresoCreateView',

        name='ingresoordeningreso-create',
    ),
    url(
         r'^IngresoOrdenIngreso/(?P<pk>\d+)/editar/$',
         'ordenIngreso.views.IngresoOrdenIngresoUpdateView',
         name='ingresoordeningreso-update',
    ),
 url(
        r'^ordenIngreso/(?P<pk>\d+)/nuevarecepcion/$',
        'ordenIngreso.views.ordeningresoNuevoRecepcionByPkView',
        name='orden-ingreso-nuevo-recepcion',
    ),
 url(
        r'^OrdenIngreso/(?P<pk>\d+)/imprimir/$',
        'ordenIngreso.views.index',
        name='orden-ingreso-imprimir',
    ),
 
       url(
    r'^OrdenIngreso/conceptosIngreso/$',
                           'ordenIngreso.views.ConceptoOrdenIngresoListView',
                           name='concepto-orden-ingreso-list',
                       ),

                       url(
                           r'^ordenIngreso/conceptos/nuevo$',
                           ConceptoOrdenIngresoCreateView.as_view(),

                           name='concepto-orden-ingreso-create',
                       ),
                       url(
                           r'^ordenIngreso/conceptos/(?P<pk>\d+)/editar/$',
                           ConceptoOrdenIngresoUpdateView.as_view(),
                           name='concepto-orden-ingreso-update',
                       ),
                         url(
                           r'^ordenIngreso/corregirOrdenIngreso/(?P<pk>\d+)/editar/$',
                           'ordenIngreso.views.corregirOrdenIngresoAsiento',
                           name='corregir-orden-ingreso-asiento',
                       ),   

)