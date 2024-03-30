
from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',

    url(
        r'^pedido/$',
        'pedido.views.PedidoListView',
        name='pedido-list',
    ),

   url(
        r'^pedido/nuevo$',
        'pedido.views.PedidoCreateView',
        name='pedido-create',
    ),
   url(
         r'^pedido/(?P<pk>\d+)/editar/$',
         PedidoUpdateView.as_view(),
         name='pedido-update',
    ),
   url(
         r'^pedido/(?P<pk>\d+)/actualizar/$',
         PedidoActualizarView.as_view(),
         name='pedido-actualizar',
    ),
   url(
        r'^pedido/(?P<pk>\d+)/detalle/$',
        PedidoDetailView.as_view(),
        name='pedido-detail',
    ),
    url(
        r'^pedido/eliminar/$',
        'pedido.views.PedidoEliminarView',
        name='pedido-delete',
    ),
    url(
        r'^pedido/(?P<pk>\d+)/eliminar/$',
        'pedido.views.PedidoEliminarByPkView',
        name='pedido-delete-pk',
    ),
     url(
        r'^pedido/guardar/$',
        'pedido.views.misPedidoGuardar',
        name='configuracion-pedido-guardar',
    ),
    url(
        r'^pedidoAprobar/$',
        'pedido.views.PedidoListAprobarView',
        name='pedido-list-aprobada',
    ),

    url(
        r'^pedido/(?P<pk>\d+)/aprobar/$',
        'pedido.views.PedidoAprobarByPkView',
        name='aprobar-pedido',
    ),
    url(
        r'^pedido/(?P<pk>\d+)/crearproforma/$',
        'pedido.views.PedidoCrearProformaView',
        name='crear-pedido-proforma',
    ),

     url(
        r'^pedidoAprobarVendor/$',
        PedidoListAprobarVendedorView.as_view(),
        name='pedido-list-aprobada-vendedor',
    ),

    url(
        r'^pedido/(?P<pk>\d+)/aprobarvendedor/$',
        'pedido.views.PedidoAprobarVendedorByPkView',
        name='aprobar-pedido-vendedor',
    ),
    url(
        r'^pedido_render/$',
        'pedido.views.PedidoRenderListView',
        name='pedido-render-list',
    ),
     url(
         r'^pedido/(?P<pk>\d+)/subirrender/$',
         PedidoRenderView.as_view(),
         name='pedido-subir-render',
    ),
    url(
        r'^pedido/(?P<pk>\d+)/anular/$',
        'pedido.views.PedidoAnularByPkView',
        name='anular-pedido',
    ),
    url(
        r'^imprimir/(?P<pk>\d+)/$',
        'pedido.views.index',
        name='pedido-imprimir',
    ),
      url(
        r'^pedido/historico/$',
          'pedido.views.PedidoHistoricoListView',
        name='pedido-historico-list',
    ),
     url(
         r'^pedido/(?P<pk>\d+)/editarhistorico/$',
         PedidoHistoricoUpdateView.as_view(),
         name='pedido-historico-update',
    ),
     url(
        r'^imprimirValores/(?P<pk>\d+)/$',
        'pedido.views.imprimirValores',
        name='pedido-imprimir-valores',
    ),
                       url(
                           r'^subir/(?P<pk>\d+)/subirimagen$',
                           'pedido.views.SubirImagenesRenderView',
                           name='subir-imagenes-render-pedido',
                       ),

                       # url(
                       #     r'^mostrar_render/$',
                       #     'pedido.views.SubirImagenesRenderView',
                       #     name='subir-imagenes-render-pedido',
                       # ),
url(
                           r'^guardarImagenes/$',
                           'pedido.views.guardarImagenesView',
                           name='guardar-imagenes-pedido',
                       ),




url(
    r'^ver/(?P<pk>\d+)/imagenRender$',
    'pedido.views.VerImagenesRenderPedidoView',
    name='ver-imagenes-render-pedido',
),
url(
                           r'^pedido/api/$',
                           'pedido.views.pedido_api_view',
                           name='pedido-api',
                       ),




                       )
