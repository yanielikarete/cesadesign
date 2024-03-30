from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',
url(
        r'^liquidaciones/$',
        'liquidacion_comisiones.views.liquidacionesListView',
        name='liquidaciones-list',
    ),

   url(
        r'^liquidaciones/nuevo$',
        'liquidacion_comisiones.views.liquidacionesCreateView',
        name='liquidaciones-create',
    ),
  
   url(
        r'^obtenerLiquidacionesComisiones/$',
        'liquidacion_comisiones.views.obtenerLiquidacionesComisiones',
        name='liquidacion-comision-obtenerLiquidacionesComisiones',
    ),

url(
         r'^liquidaciones/(?P<pk>\d+)/editar/$',
        'liquidacion_comisiones.views.liquidacionesUpdateView',
         name='liquidaciones-update',
    ),

                       url(
                           r'^proformaComision/$',
                           'liquidacion_comisiones.views.ProformaComisionListView',
                           name='liquidacion-comision-proforma',
                       ),

                       url(
                           r'^liquidaciones/(?P<pk>\d+)/relacionarComision/$',
                           'liquidacion_comisiones.views.ComisionCreateView',
                           name='liquidaciones-comision-vendedor',
                       ),

url(
                           r'^liquidaciones/(?P<pk>\d+)/adelantoComision/$',
                           'liquidacion_comisiones.views.AdelantoComisionView',
                           name='liquidaciones-adelanto-comision-vendedor',
                       ),
)