from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',

                       url(r'^clientes/$', 'clientes.views.ClienteListView', name='cliente-list'),
                       url(r'^clientes/nuevo$', 'clientes.views.ClienteCreateView', name='cliente-nuevo'),
                       url(r'^clientes/(?P<pk>\d+)/editar/$', ClienteUpdateView.as_view(),name='cliente-editar'),
                       url(r'^clientes/eliminar/$','clientes.views.clienteEliminarView',name='cliente-delete'),
                       url(r'^clientes/(?P<pk>\d+)/eliminar/$','clientes.views.clienteEliminarByPkView',name='cliente-delete-pk',),
                       url(r'^razonsocial/$','clientes.views.RazonSocialListView',name='razonsocial-list'),
                       url(r'^razonsocial/nuevo$','clientes.views.RazonSocialNuevoView',name='razonsocialnuevo-pk'),
                       url(r'^razonsocial/(?P<pk>\d+)/editar/$',RazonSocialUpdateView.as_view(),name='razonsocial-update'),
                       url(r'^razonsocial/eliminar/$','clientes.views.razonsocialEliminarView',name='razonsocial-delete'),
                       url(r'^razonsocial/(?P<pk>\d+)/eliminar/$','clientes.views.razonsocialEliminarByPkView',name='razonsocial-delete-pk'),
                        url(r'^razonsocial/eliminarRazonSocialCliente/$','clientes.views.eliminarRazonSocialCliente',name='eliminar-razon-social-cliente'),
url(
                           r'^obtenerRazonSocial/$',
                           'clientes.views.obtenerRazonSocial',
                           name='obtener-razon-social',
                       ),
                       )
