from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',
   url(r'^proveedores/$','proveedores.views.ProveedorListView',name='proveedor-list',),
   url(r'^proveedores/nuevo$','proveedores.views.ProveedorCreateView',name='proveedor-nuevo',),
   url(r'^proveedores/(?P<pk>\d+)/editar/$', ProveedorUpdateView.as_view(), name='proveedor-editar',),
   url(r'^proveedores/eliminar/$','proveedores.views.proveedorEliminarView',name='proveedor-delete',),
   url(r'^proveedores/(?P<pk>\d+)/eliminar/$','proveedores.views.proveedorEliminarByPkView',name='proveedor-delete-pk',),
      url(r'^proveedores/validarRuc/$','proveedores.views.validarRuc',name='proveedor-validar-ruc',),

)