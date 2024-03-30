# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',

                       url(
                           r'^producto/$',
                           'inventario.views.ProductoListView',
                           name='producto-list',
                       ),
                       url(
                           r'^producto/tipos/(?P<pk>\d+)/$',
                           'inventario.views.ProductoListTiposView',
                           name='producto-list-tipos',
                       ),

                       url(
                           r'^producto/nuevo$',
                           'inventario.views.ProductoCreateView',
                           name='producto-create',
                       ),
                       url(
                           r'^producto/(?P<pk>\d+)/editar/$',
                           ProductoUpdateView.as_view(),
                           name='producto-update',
                       ),
                       url(
                           r'^producto/(?P<pk>\d+)/detalle/$',
                           ProductoDetailView.as_view(),
                           name='producto-detail',
                       ),
                       url(
                           r'^producto/eliminar/$',
                           'inventario.views.productoEliminarView',
                           name='producto-delete',
                       ),
                       url(
                           r'^producto/(?P<pk>\d+)/eliminar/$',
                           'inventario.views.productoEliminarByPkView',
                           name='producto-delete-pk',
                       ),
                       url(
                           r'^producto/crear$',
                           'inventario.views.contact',
                           name='crear',
                       ),

                       # =================CATEGORIA pRODUCTO===========================#
                       url(
                           r'^categoria-producto/$',
                           CategoriaProductoListView.as_view(),
                           name='categoria-producto-list',
                       ),

                       url(
                           r'^categoria-producto/nuevo$',
                           CategoriaProductoCreateView.as_view(),
                           name='categoria-producto-create',
                       ),
                       url(
                           r'^categoria-producto/(?P<pk>\d+)/editar/$',
                           CategoriaProductoUpdateView.as_view(),
                           name='categoria-producto-update',
                       ),
                       url(
                           r'^categoria-producto/(?P<pk>\d+)/detalle/$',
                           CategoriaProductoDetailView.as_view(),
                           name='categoria-producto-detail',
                       ),
                       url(
                           r'^categoria-producto/eliminar/$',
                           'inventario.views.CategoriaproductoEliminarView',
                           name='categoria-producto-delete',
                       ),
                       url(
                           r'^categoria-producto/(?P<pk>\d+)/eliminar/$',
                           'inventario.views.CategoriaproductoEliminarByPkView',
                           name='categoria-producto-delete-pk',
                       ),
                       url(
                           r'^categoria-producto/productos/guardar/$',
                           'inventario.views.misCategoriasProductosGuardar',
                           name='configuracion-categoria-producto-guardar',
                       ),
                       # =================BODEGA===========================#
                       url(
                           r'^bodega/$',
                           'inventario.views.BodegaListView',
                           name='bodega-list',
                       ),

                       url(
                           r'^bodega/nuevo$',
                           BodegaCreateView.as_view(),
                           name='bodega-create',
                       ),
                       url(
                           r'^bodega/(?P<pk>\d+)/editar/$',
                           BodegaUpdateView.as_view(),
                           name='bodega-update',
                       ),
                       url(
                           r'^bodega/(?P<pk>\d+)/detalle/$',
                           BodegaDetailView.as_view(),
                           name='bodega-detail',
                       ),
                       url(
                           r'^bodega/eliminar/$',
                           'inventario.views.BodegaEliminarView',
                           name='bodega-delete',
                       ),
                       url(
                           r'^bodega/(?P<pk>\d+)/eliminar/$',
                           'inventario.views.BodegaEliminarByPkView',
                           name='bodega-delete-pk',
                       ),
                       url(
                           r'^bodega/guardar/$',
                           'inventario.views.misBodegaGuardar',
                           name='configuracion-bodega-guardar',
                       ),

                       # =================SUBCATEGORIA pRODUCTO===========================#
                       url(
                           r'^subcategoria-producto/$',
                           SubCategoriaProductoListView.as_view(),
                           name='subcategoria-producto-list',
                       ),

                       url(
                           r'^subcategoria-producto/nuevo$',
                           SubCategoriaProductoCreateView.as_view(),
                           name='subcategoria-producto-create',
                       ),
                       url(
                           r'^subcategoria-producto/(?P<pk>\d+)/editar/$',
                           SubCategoriaProductoUpdateView.as_view(),
                           name='subcategoria-producto-update',
                       ),
                       url(
                           r'^subcategoria-producto/(?P<pk>\d+)/detalle/$',
                           SubCategoriaProductoDetailView.as_view(),
                           name='subcategoria-producto-detail',
                       ),
                       url(
                           r'^subcategoria-producto/eliminar/$',
                           'inventario.views.SubCategoriaproductoEliminarView',
                           name='subcategoria-producto-delete',
                       ),
                       url(
                           r'^subcategoria-producto/(?P<pk>\d+)/eliminar/$',
                           'inventario.views.SubCategoriaproductoEliminarByPkView',
                           name='subcategoria-producto-delete-pk',
                       ),
                       url(
                           r'^subcategoria-producto/productos/guardar/$',
                           'inventario.views.misSubCategoriasProductosGuardar',
                           name='configuracion-subcategoria-producto-guardar',
                       ),

                        #Carga Catalogo
                       url(
                           r'^kardex/$',
                           'inventario.views.KardexListView',
                           name='kardex-list',
                       ),

                        #Consulta
                       url(
                           r'^kardex_actual/$',
                           'inventario.views.KardexListViewActual',
                           name='kardex-actual',
                       ),

                        #Saldos por Fecha
                       #url(
                       #    r'^saldospf/$',
                       #    'inventario.views.KardexListViewActual',
                       #    name='kardex-actual',
                       #),

                       url(
                           r'^kardex/nuevo$',
                           KardexCreateView.as_view(),
                           name='kardex-create',
                       ),
                       url(
                           r'^kardex/(?P<pk>\d+)/editar/$',
                           KardexUpdateView.as_view(),
                           name='kardex-update',
                       ),
                       url(
                           r'^kardex/(?P<pk>\d+)/detalle/$',
                           KardexDetailView.as_view(),
                           name='kardex-detail',
                       ),
                       url(
                           r'^kardex/eliminar/$',
                           'inventario.views.kardexEliminarView',
                           name='kardex-delete',
                       ),
                       url(
                           r'^kardex/(?P<pk>\d+)/eliminar/$',
                           'inventario.views.kardexEliminarByPkView',
                           name='kardex-delete-pk',
                       ),

                       #Saldos Nuevo
                       url(
                           r'^saldos/$',
                           'inventario.views.SaldosListViewActual',
                           name='saldos-actual',
                       ),
                       #'inventario.views.SaldosListView',


                       url(
                           r'^seriales/$',
                           SerialesListView.as_view(),
                           name='seriales-list',
                       ),

                       url(
                           r'^seriales/nuevo$',
                           SerialesCreateView.as_view(),
                           name='seriales-create',
                       ),
                       url(
                           r'^seriales/(?P<pk>\d+)/editar/$',
                           SerialesUpdateView.as_view(),
                           name='seriales-update',
                       ),
                       url(
                           r'^seriales/(?P<pk>\d+)/detalle/$',
                           SerialesDetailView.as_view(),
                           name='seriales-detail',
                       ),
                       url(
                           r'^seriales/eliminar/$',
                           'inventario.views.serialesEliminarView',
                           name='seriales-delete',
                       ),
                       url(
                           r'^seriales/(?P<pk>\d+)/eliminar/$',
                           'inventario.views.serialesEliminarByPkView',
                           name='seriales-delete-pk',
                       ),

                       # ====================Unidades=========================#

                       url(
                           r'^unidades/$',
                           UnidadesListView.as_view(),
                           name='unidades-list',
                       ),

                       url(
                           r'^unidades/nuevo$',
                           UnidadesCreateView.as_view(),
                           name='unidades-create',
                       ),
                       url(
                           r'^unidades/(?P<pk>\d+)/editar/$',
                           UnidadesUpdateView.as_view(),
                           name='unidades-update',
                       ),
                       url(
                           r'^unidades/(?P<pk>\d+)/detalle/$',
                           UnidadesDetailView.as_view(),
                           name='unidades-detail',
                       ),
                       url(
                           r'^unidades/eliminar/$',
                           'inventario.views.unidadesEliminarView',
                           name='unidades-delete',
                       ),
                       url(
                           r'^unidades/(?P<pk>\d+)/eliminar/$',
                           'inventario.views.unidadesEliminarByPkView',
                           name='unidades-delete-pk',
                       ),

                       # =================TIPO pRODUCTO===========================#
                       url(
                           r'^tipo-producto/$',
                           TipoProductoListView.as_view(),
                           name='tipo-producto-list',
                       ),

                       url(
                           r'^tipo-producto/nuevo$',
                           TipoProductoCreateView.as_view(),
                           name='tipo-producto-create',
                       ),
                       url(
                           r'^tipo-producto/(?P<pk>\d+)/editar/$',
                           TipoProductoUpdateView.as_view(),
                           name='tipo-producto-update',
                       ),
                       url(
                           r'^tipo-producto/(?P<pk>\d+)/detalle/$',
                           TipoProductoDetailView.as_view(),
                           name='tipo-producto-detail',
                       ),
                       url(
                           r'^tipo-producto/eliminar/$',
                           'inventario.views.TipoproductoEliminarView',
                           name='tipo-producto-delete',
                       ),
                       url(
                           r'^tipo-producto/(?P<pk>\d+)/eliminar/$',
                           'inventario.views.TipoproductoEliminarByPkView',
                           name='tipo-producto-delete-pk',
                       ),
                       url(
                           r'^tipo-producto/productos/guardar/$',
                           'inventario.views.misTiposProductosGuardar',
                           name='configuracion-tipo-producto-guardar',
                       ),

                       # =================LINEA===========================#
                       url(
                           r'^linea/$',
                           LineaListView.as_view(),
                           name='linea-list',
                       ),

                       url(
                           r'^linea/nuevo$',
                           LineaCreateView.as_view(),
                           name='linea-create',
                       ),
                       url(
                           r'^linea/(?P<pk>\d+)/editar/$',
                           LineaUpdateView.as_view(),
                           name='linea-update',
                       ),
                       url(
                           r'^linea/(?P<pk>\d+)/detalle/$',
                           LineaDetailView.as_view(),
                           name='tipo-producto-detail',
                       ),
                       url(
                           r'^linea/eliminar/$',
                           'inventario.views.LineaEliminarView',
                           name='linea-delete',
                       ),
                       url(
                           r'^linea/(?P<pk>\d+)/eliminar/$',
                           'inventario.views.LineaEliminarByPkView',
                           name='linea-delete-pk',
                       ),
                       url(
                           r'^linea/guardar/$',
                           'inventario.views.misLineasGuardar',
                           name='configuracion-linea-guardar',
                       ),
                       url(r'^subcategoria-producto/(?P<pk>\d+)/$', ActualizarSubcategoria.as_view(),
                           name='actualizars'),
                       url(r'^producto/(?P<pk>\d+)/actualizar/$', ProductoActualizarView.as_view(),
                           name='actualizar-producto'),
                       url(r'^producto/proforma/$', ProformaView.as_view(), name='proforma'),
                       url(r'^producto/pedido/$', PedidoView.as_view(), name='pedido'),
                       url(r'^producto/ordenproduccion/$', OrdenProduccionView.as_view(), name='ordenproduccion'),
                       url(r'^producto/guia/$', GuiaRemisionView.as_view(), name='guiaremision'),
                       url(r'^producto/reunion/$', ReunionView.as_view(), name='reunion'),
                       url(
                           r'^producto/(?P<pk>\d+)/nuevo_orden_produccion$',
                           'inventario.views.ProductoCreateOrdenProduccionView',
                           name='producto-crear-ordenproduccion',
                       ),
                       url(
                           r'^producto_areas/(?P<pk>\d+)/list/$',
                           'inventario.views.ProductoAreasListView',
                           name='producto-areas-list',
                       ),
                       url(
                           r'^producto/agregarAmbiente/$',
                           'inventario.views.agregarAmbiente',
                           name='producto-areas-agregar',
                       ),
                       url(
                           r'^producto/eliminarProductoReceta/$',
                           'inventario.views.eliminarProductoReceta',
                           name='producto-areas-eliminar',
                       ),
                       url(
                           r'^producto/(?P<pk>\d+)/receta/$',
                           'inventario.views.recetaView',
                           name='producto-receta',
                       ),
                       url(
                           r'^copiarReceta/$',
                           'inventario.views.copiarReceta',
                           name='copiar-receta',
                       ),
                       url(
                           r'^productoenbodega/(?P<pk>\d+)/$',
                           'inventario.views.ProductoBodegaListView',
                           name='productoenbodega-list',
                       ),
                       url(
                           r'^obtenerproductoenbodega/$',
                           'inventario.views.ObtenerProductoBodegaListView',
                           name='obtener-productoenbodega-list',
                       ),
                       url(
                           r'^producto/(?P<pk>\d+)/manoobra/$',
                           'inventario.views.manoObraView',
                           name='producto-mano-obra',
                       ),
                       url(
                           r'^analisis/list/$',
                           AnalisisListView.as_view(),
                           name='analisis-list',
                       ),
                       url(
                           r'^analisis/crear/$',
                           'inventario.views.AnalisisCreateView',
                           name='analisis-create',
                       ),
                       url(
                           r'^analisis/(?P<pk>\d+)/editar/$',
                           AnalisisUpdateView.as_view(),
                           name='analisis-update',
                       ),
                       url(
                           r'^analisisAprobar/$',
                           AnalisisInventarioListAprobarView.as_view(),
                           name='analisis-list-aprobada',
                       ),
                       url(
                           r'^producto_general/$',
                           'inventario.views.ProductoGeneralListView',
                           name='producto-general-list',
                       ),
                       url(
                           r'^producto_general/nuevo$',
                           ProductoGeneralCreateView.as_view(),
                           name='producto-general-create2',
                       ),
                       url(
                           r'^producto_general/(?P<pk>\d+)/editar/$',
                           ProductoGeneralUpdateView.as_view(),
                           name='producto-general-update',
                       ),
                       url(
                           r'^producto_general/new$',
                           'inventario.views.ProductoGeneralNuevoView',
                           name='producto-general-nuevo',
                       ),
                       url(
                           r'^producto/RecetaEliminar/$',
                           'inventario.views.RecetaEliminarView',
                           name='receta-detalle-eliminar',
                       ),
                       url(
                           r'^producto/eliminarManoObraReceta/$',
                           'inventario.views.eliminarManoObraReceta',
                           name='mano-obra-receta-eliminar',
                       ),
                       url(
                           r'^bodega/(?P<pk>\d+)/kardex/$',
                           'inventario.views.BodegaKardexListView',
                           name='bodega-kardex',
                       ),
                        url(
                           r'^producto/load',
                           'inventario.views.loadProducts',
                       ),

                       url(
                           r'^producto/migrarArchivoProducto',
                           'inventario.views.migrarArchivoProducto',
                       ),


                       )
