
from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',
url(
        r'^vendedores/$',
        'vendedor.views.VendedoresListView',
        name='vendedores-list',
    ),

   url(
        r'^vendedores/nuevo$',
        VendedorCreateView.as_view(),
        name='vendedores-create',
    ),
   url(
         r'^vendedores/(?P<pk>\d+)/editar/$',
         VendedorUpdateView.as_view(),
         name='vendedores-update',
    ),
   url(
        r'^vendedores/(?P<pk>\d+)/detalle/$',
        VendedorDetailView.as_view(),
        name='vendedores-detail',
    ),
    url(
        r'^vendedores/eliminar/$',
        'vendedor.views.VendedorEliminarView',
        name='vendedores-delete',
    ),
    url(
        r'^vendedores/(?P<pk>\d+)/eliminar/$',
        'vendedor.views.VendedorEliminarByPkView',
        name='vendedores-delete-pk',
    ),


)