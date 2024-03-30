
from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',

   url(
         r'^subordenproduccion/(?P<pk>\d+)/list/$',
         'subordenproduccion.views.SubOrdenProduccionListView',
         name='subordenproduccion-list',
    ),
 url(
        r'^agregarSubordenproduccion/$',
        'subordenproduccion.views.agregarSubordenproduccion',
        name='subordenproduccion-agregar',
    ),
 url(
        r'^eliminarSubordenproduccion/$',
        'subordenproduccion.views.eliminarSubordenproduccion',
        name='subordenproduccion-eliminar',
    ),
  url(
         r'^subordenproduccion/(?P<pk>\d+)/manoObra/$',
         'subordenproduccion.views.manoObraView',
         name='subordenproduccion-manoobra',
    ),
  url(
         r'^subordenproduccion/(?P<pk>\d+)/receta/$',
         'subordenproduccion.views.recetaView',
         name='subordenproduccion-receta',
    ),
   url(
         r'^subordenproduccion/enviarBodega/$',
         'subordenproduccion.views.enviarBodegaView',
         name='enviar-bodega',
    ),
     url(
         r'^recepcionBodega/list/$',
         'subordenproduccion.views.BodegaRecepcionView',
         name='bodegarecepcion-list',
    ),
    url(
         r'^subordenproduccion/enviarBodegaCrudo/$',
         'subordenproduccion.views.enviarBodegaCrudoView',
         name='enviar-bodega-crudo',
    ),
    url(
         r'^recepcionBodega/(?P<pk>\d+)/editar/$',
         'subordenproduccion.views.OrdenProduccionBodegaUpdateView',
         name='recepcionbodega-editar',
    ),

     url(
         r'^subordenproduccion/(?P<pk>\d+)/listdetalle/$',
         'subordenproduccion.views.SubOrdenProduccionListDetalleView',
         name='subordenproduccion-list-detalle',
    ),
    url(
        r'^imprimir/(?P<pk>\d+)/$',
        'subordenproduccion.views.index',
        name='subordenproduccion-imprimir',
    ),
    url(
        r'^subordenproduccion/eliminarManoObra/$',
        'subordenproduccion.views.eliminarManoObra',
        name='subordenproduccion-manoobra-eliminar',
    ),
                       url(
                           r'^subordenproduccion/eliminarRecetaSubop/$',
                           'subordenproduccion.views.EliminarRecetaSubopView',
                           name='subordenproduccion-receta-eliminar',
                       ),
                       url(
                           r'^SubOrdenProduccionListDetalleImprimir/(?P<pk>\d+)/$',
                           'subordenproduccion.views.SubOrdenProduccionListDetalleImprimirView',
                           name='subordenproduccion-imprimir-detalle',
                       ),
                        url(
        r'^guardarCosto/$',
        'subordenproduccion.views.guardarCosto',
        name='subordenproduccion-guardar-costo',
    ),
                        
url(r'^export_to_excel_mano_obra/(?P<pk>\d+)/$',
         'subordenproduccion.views.export_to_excel_mano_obra', name='export_to_excel_mano_obra'),

url(r'^export_to_excel_receta/(?P<pk>\d+)/$',
         'subordenproduccion.views.export_to_excel_receta', name='export_to_excel_receta'),
url(r'^subordenproduccion/consultar_subop_receta', 'subordenproduccion.views.consultar_subop_receta', name='consultar-subop-receta'),

  url(
        r'^subordenproduccionDespachar/$',
         'subordenproduccion.views.SubOrdenProduccionListDespacharView',
        name='subordenproduccion-list-despachar',
    ),

    url(
        r'^subordenproduccionDespachar/(?P<pk>\d+)/despachar/$',
        'subordenproduccion.views.OrdenProduccionAprobarDespachoByPkView',
        name='despachar-subordenesproduccion',
    ),
    
     url(
        r'^consultar_subopxarea_receta/$',
        'subordenproduccion.views.consultar_subopxarea_receta',
        name='consultar-subopxarea-receta',
    ),
     
     
     
      url(
        r'^analizar_receta/$',
        'subordenproduccion.views.analisisCostoMateriales',
        name='analizar-receta',
    ),
      
       url(
        r'^consultar_analisis_receta/$',
        'subordenproduccion.views.obtenerAnalisisCostoMateriales',
        name='consultar-analisis-receta',
    ),
       
        url(
        r'^analizar_mano_obra/$',
        'subordenproduccion.views.analisisManoObra',
        name='analizar-mano-obra',
    ),
        
         url(
        r'^consultar_analisis_mano_obra/$',
        'subordenproduccion.views.obtenerAnalisisManoObra',
        name='consultar-analisis-mano-obra',
    ),
         
          url(
        r'^cierre_mensual_produccion/$',
        'subordenproduccion.views.cierreMensualProduccion',
        name='cierre-mensual-produccion',
    ),
          
           url(
        r'^consultar_analisis_receta_mes/$',
        'subordenproduccion.views.obtenerAnalisisCostoMaterialesMes',
        name='consultar-analisis-receta-mes',
    ),
               url(
        r'^obtenerAnalisisMano/$',
        'subordenproduccion.views.obtenerAnalisisMano',
        name='consultar-analisis-mano-obra-nueo',
    ),
                url(
        r'^costeo_produccion_list/$',
        'subordenproduccion.views.costeoProduccionList',
        name='costeo-produccion-list',
    ),
                
  url(
        r'^costeo_produccion/(?P<pk>\d+)/ver/$',
        'subordenproduccion.views.costeoProduccionVer',
        name='costeo-produccion-ver',
    ),
    
           
           
)
