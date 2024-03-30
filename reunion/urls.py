# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',

url(
        r'^reunion/$',
        ReunionListView.as_view(),
        name='reunion-list',
    ),
url(
        r'^reunion/cotizacion_bodega$',
        ReunionCotizacionBodegaListView.as_view(),
        name='cotizacion-bodega-list',
    ),
   url(
        r'^reunion/nuevo$',
        ReunionCreateView.as_view(),
        name='reunion-create',
    ),
   url(
         r'^reunion/(?P<pk>\d+)/editar/$',
         'reunion.views.ReunionUpdateView',
         name='reunion-update',
    ),
   url(
         r'^reunion/(?P<pk>\d+)/actualizar/$',
         ReunionActualizarView.as_view(),
         name='reunion-actualizar',
    ),
   
   url(
         r'^reunion/(?P<pk>\d+)/respuesta_bodega/$',
         RespuestaReunionBodegaView.as_view(),
         name='reunion-respuesta-bodega',
    ),
   url(
        r'^reunion/(?P<pk>\d+)/detalle/$',
        ReunionDetailView.as_view(),
        name='reunion-detail',
    ),
    url(
        r'^reunion/eliminar/$',
        'reunion.views.ReunionEliminarView',
        name='reunion-delete',
    ),
    url(
        r'^reunion/(?P<pk>\d+)/eliminar/$',
        'reunion.views.ReunionEliminarByPkView',
        name='reunion-delete-pk',
    ),
     url(
        r'^reunion/guardar/$',
        'reunion.views.misReunionGuardar',
        name='configuracion-reunion-guardar',
    ),
url(
        r'^reunion/subirImagen$',
        'reunion.views.SubirImagenesReunionView',
         name='reunion-subir-imagen',
    ),
 url(
         r'^reunion/(?P<pk>\d+)/editarSubirImagen/$',
         'reunion.views.SubirImagenesReunionActualizarView',
         name='subir-imagen-update',
    ),
 url(
        r'^imagenesreunion/$',
        ImagenesReunionListView.as_view(),
        name='imagenesreunion-list',
    ),

)