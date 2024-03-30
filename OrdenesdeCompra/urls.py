from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',

   url(
        r'^OrdenesdeCompra/$',
       'OrdenesdeCompra.views.OrdenCompraListView',
        name='ordenescompra-list',
    ),

   url(
        r'^OrdenesdeCompra/nuevo$',
        'OrdenesdeCompra.views.OrdenCompraCreateView',
        name='ordenescompra-create',
    ),
   url(
        r'^OrdenesdeCompra/new$',
        OrdenCreateView.as_view(),
        name='ordenes-create',
    ),
   url(
        r'^OrdenesdeCompra/crear$',
        'OrdenesdeCompra.views.OrdenNuevoView',

        name='ordenes-nuevo',
    ),
   url(
         r'^OrdenesdeCompra/(?P<pk>\d+)/editar/$',
         'OrdenesdeCompra.views.OrdenCompraUpdateView',
         name='ordenescompra-update',
    ),
   url(
         r'^OrdenesdeCompra/(?P<pk>\d+)/actualizar/$',
           OrdenCompraActualizarView.as_view(),
         name='ordenescompra-actualizar',
    ),
   url(
        r'^OrdenesdeCompra/(?P<pk>\d+)/detalle/$',
        OrdenCompraDetailView.as_view(),
        name='ordenescompra-detail',
    ),
    url(
        r'^OrdenesdeCompra/eliminar/$',
        'OrdenesdeCompra.views.ordenescompraEliminarView',
        name='ordenescompra-delete',
    ),
    url(
        r'^OrdenesdeCompra/(?P<pk>\d+)/eliminar/$',
        'OrdenesdeCompra.views.ordenescompraEliminarByPkView',
        name='ordenescompra-delete-pk',
    ),
    url(
        r'^OrdenesdeCompraAprobar/$',
        'OrdenesdeCompra.views.OrdenCompraListAprobarView',
        name='ordenescompra-list-aprobada',
    ),

    url(
        r'^OrdenesdeCompra/(?P<pk>\d+)/aprobar/$',
        'OrdenesdeCompra.views.ordenescompraAprobarByPkView',
        name='aprobar-orden-compra',
    ),
    url(
        r'^comprasLocales/$',
        'OrdenesdeCompra.views.ComprasLocalesListView',
        name='compraslocales-list',
    ),
    url(
        r'^comprasLocales/crear$',
        'OrdenesdeCompra.views.ComprasLocalesCreateView',

        name='compraslocales-create',
    ),
    url(
         r'^comprasLocales/(?P<pk>\d+)/editar/$',
         'OrdenesdeCompra.views.ComprasLocalesUpdateView',
         name='compraslocales-update',
    ),
    url(
        r'^ordenescomprasLocales/(?P<pk>\d+)/crear$',
        'OrdenesdeCompra.views.OrdenesComprasLocalesCreateView',

        name='ordenes-compraslocales-create',
    ),
     url(
        r'^comprasLocales/(?P<pk>\d+)/imprimir$',
        'OrdenesdeCompra.views.index',

        name='compraslocales-imprimir',
    ),
      url(
        r'^ordencompra/(?P<pk>\d+)/imprimir$',
        'OrdenesdeCompra.views.indexOrdenCompra',

        name='ordencompra-imprimir',
    ),
url(
        r'^obtenerPrecioProducto/$',
        'OrdenesdeCompra.views.obtenerPrecioProducto',
        name='obtener-precio-producto',
    ),
url(
        r'^comprasLocales/api$',
        'OrdenesdeCompra.views.compras_locales_api_view',

        name='compraslocales-api',
    ),

)