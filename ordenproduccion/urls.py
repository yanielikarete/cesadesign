
from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',

    url(
        r'^ordenproduccion/$',
        'ordenproduccion.views.OrdenProduccionListView',
        name='ordenproduccion-list',
    ),

   url(
        r'^ordenproduccion/nuevo$',
        'ordenproduccion.views.OrdenProduccionCreateView',
        name='ordenproduccion-create',
    ),
   url(
         r'^ordenproduccion/(?P<pk>\d+)/editar/$',
         'ordenproduccion.views.OrdenProduccionUpdateView',
         name='ordenproduccion-update',
    ),
   # url(
   #       r'^ordenproduccion/(?P<pk>\d+)/actualizar/$',
   #       OrdenProduccionActualizarView.as_view(),
   #       name='ordenproduccion-actualizar',
   #  ),

    url(
        r'^ordenproduccion/eliminar/$',
        'ordenproduccion.views.OrdenProduccionEliminarView',
        name='ordenproduccion-delete',
    ),
    url(
        r'^ordenproduccion/(?P<pk>\d+)/eliminar/$',
        'ordenproduccion.views.OrdenProduccionEliminarByPkView',
        name='ordenproduccion-delete-pk',
    ),
     url(
        r'^ordenproduccionAprobar/$',
         'ordenproduccion.views.OrdenProduccionListAprobarView',
        name='ordenproduccion-list-aprobada',
    ),

    url(
        r'^ordenproduccion/(?P<pk>\d+)/aprobar/$',
        'ordenproduccion.views.OrdenProduccionAprobarByPkView',
        name='aprobar-ordenes',
    ),
    url(
        r'^imprimir/(?P<pk>\d+)/$',
        'ordenproduccion.views.index',
        name='ordenproduccion-imprimir',
    ),
    url(
        r'^rop/$',
        RopListView.as_view(),
        name='rop-list',
    ),
    url(
        r'^rop/nuevo/$',
        'ordenproduccion.views.RopCreateView',
        name='rop-create',
    ),
      url(
         r'^rop/(?P<pk>\d+)/editar/$',
         'ordenproduccion.views.RopUpdateView',
         name='rop-update',
    ),
    url(
        r'^ropAprobar/$',
        RopListAprobarView.as_view(),
        name='rop-list-aprobada',
    ),

    url(
        r'^rop/(?P<pk>\d+)/aprobar/$',
        'ordenproduccion.views.RopAprobarByPkView',
        name='aprobar-rop',
    ),
     url(
        r'^ordenproduccion/subordenes$',
         'ordenproduccion.views.OrdenProduccionListSubordenesView',
        name='ordenproduccion-list-subordenes',
    ),

      url(
        r'^ordenproduccion/historico/$',
        OrdenProduccionHistoricoListView.as_view(),
        name='ordenproduccion-historico-list',
    ),

   url(
         r'^ordenproduccion/(?P<pk>\d+)/editarhistorico/$',
         'ordenproduccion.views.OrdenProduccionHistoricoUpdateView',
         name='ordenproduccion-historico-update',
    ),
   url(
        r'^ordenproduccion/api$',
        'ordenproduccion.views.orden_produccion_api_view',
        name='ordenproduccion-api',
    ),
    url(
        r'^ordenproduccion/subopapi$',
        'ordenproduccion.views.orden_produccion_suborden_api_view',
        name='ordenproduccion-subop-api',
    ),
)
