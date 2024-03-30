
from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',

    url(
        r'^ordenservicio/$',
        'ordenServicio.views.OrdenServicioListView',
        name='ordenservicio-list',
    ),

   url(
        r'^ordenservicio/nuevo$',
        'ordenServicio.views.OrdenServicioCreateView',
        name='ordenservicio-create',
    ),
   url(
         r'^ordenservicio/(?P<pk>\d+)/editar/$',
         'ordenServicio.views.OrdenServicioUpdateView',
         name='ordenservicio-update',
    ),
   url(
        r'^ordenservicio/(?P<pk>\d+)/detalle/$',
        OrdenServicioDetailView.as_view(),
        name='ordenservicio-detail',
    ),
    url(
        r'^ordenservicio/eliminar/$',
        'ordenServicio.views.OrdenServicioEliminarView',
        name='ordenservicio-delete',
    ),
    url(
        r'^ordenservicio/(?P<pk>\d+)/eliminar/$',
        'ordenServicio.views.OrdenServicioEliminarByPkView',
        name='ordenservicio-delete-pk',
    ),
      url(
        r'^agregarOrdenServicio/$',
        'ordenServicio.views.agregarOrdenServicio',
        name='ordenservicio-agregar',
    ),
)