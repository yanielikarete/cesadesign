# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',

                       # =================	LIBRO DIARIO ===========================#
                       url(
                           r'^registrar_libro_diario/$',
                           'contabilidad.views.libro_diario_index',
                           name='registrar-libro-diario',
                       ),
                       url(
                           r'^consulta/$',
                           'contabilidad.views.consultar_libro_diario',
                           name='consulta-libro-diario'),
                       # ================= MAYORES CONTABLES =========================#
                       url(
                           r'^mayores_contables/$',
                           'contabilidad.views.MayoresContablesView',
                           name='mayores-contables',
                       ),
                       url(
                           r'^consulta_mayor/$',
                           'contabilidad.views.ConsultaMayorView',
                           name='consulta-mayor',
                       ),
                       
                       
                        url(
                           r'^mayores_contables_actual/$',
                           'contabilidad.views.MayoresContablesActualView',
                           name='mayores-contables-actual',
                       ),
                       url(
                           r'^consulta_mayor_actual/$',
                           'contabilidad.views.ConsultaMayorActualView',
                           name='consulta-mayor-actual',
                       ),
                       # =================EjercicioContable===========================#
                       url(
                           r'^ejerciciocontable/$',
                           EjercicioContableListView.as_view(),
                           name='ejerciciocontable-list',
                       ),
                       url(
                           r'^ejerciciocontable/nuevo$',
                           EjercicioContableCreateView.as_view(),
                           name='ejerciciocontable-create',
                       ),
                       url(
                           r'^ejerciciocontable/(?P<pk>\d+)/editar/$',
                           EjercicioContableUpdateView.as_view(),
                           name='ejerciciocontable-update',
                       ),
                       url(
                           r'^ejerciciocontable/(?P<pk>\d+)/detalle/$',
                           EjercicioContableDetailView.as_view(),
                           name='ejerciciocontable-detail',
                       ),
                       url(
                           r'^ejerciciocontable/eliminar/$',
                           'contabilidad.views.ejercicioContableEliminarView',
                           name='ejerciciocontable-delete',
                       ),
                       url(
                           r'^ejerciciocontable/(?P<pk>\d+)/eliminar/$',
                           'contabilidad.views.ejercicioContableEliminarByPkView',
                           name='ejerciciocontable-delete-pk',
                       ),

                       # ======================PlanDeCuentas======================#
                       url(
                           r'^plandecuentas/$',
                           'contabilidad.views.PlanDeCuentasListView',
                           name='plandecuentas-list',
                       ),
                       url(
                           r'^plandecuentas/nuevo$',
                           'contabilidad.views.PlanDeCuentasCreateView',
                           name='plandecuentas-create',
                       ),
                       url(
                           r'^plandecuentas/(?P<pk>\d+)/editar/$',
                           PlanDeCuentasUpdateView.as_view(),
                           name='plandecuentas-update',
                       ),
                       url(
                           r'^plandecuentas/(?P<pk>\d+)/detalle/$',
                           PlanDeCuentasDetailView.as_view(),
                           name='plandecuentas-detail',
                       ),
                       url(
                           r'^plandecuentas/eliminar/$',
                           'contabilidad.views.planDeCuentasEliminarView',
                           name='plandecuentas-delete',
                       ),
                       url(
                           r'^plandecuentas/(?P<pk>\d+)/eliminar/$',
                           'contabilidad.views.planDeCuentasEliminarByPkView',
                           name='plandecuentas-delete-pk',
                       ),

                       # =================TipoCuenta===========================#
                       url(
                           r'^tipocuenta/$',
                           TipoCuentaListView.as_view(),
                           name='tipocuenta-list',
                       ),
                       url(
                           r'^tipocuenta/nuevo$',
                           TipoCuentaCreateView.as_view(),
                           name='tipocuenta-create',
                       ),
                       url(
                           r'^tipocuenta/(?P<pk>\d+)/editar/$',
                           TipoCuentaUpdateView.as_view(),
                           name='tipocuenta-update',
                       ),
                       url(
                           r'^tipocuenta/(?P<pk>\d+)/detalle/$',
                           TipoCuentaDetailView.as_view(),
                           name='tipocuenta-detail',
                       ),
                       url(
                           r'^tipocuenta/eliminar/$',
                           'contabilidad.views.tipoCuentaEliminarView',
                           name='tipocuenta-delete',
                       ),
                       url(
                           r'^tipocuenta/(?P<pk>\d+)/eliminar/$',
                           'contabilidad.views.tipoCuentaEliminarByPkView',
                           name='tipocuenta-delete-pk',
                       ),

                       # =================CentroCosto===========================#
                       url(
                           r'^centrocosto/$',
                           'contabilidad.views.CentroCostoListView',
                           name='centrocosto-list',
                       ),
                       url(
                           r'^centrocosto/nuevo$',
                           CentroCostoCreateView.as_view(),
                           name='centrocosto-create',
                       ),
                       url(
                           r'^centrocosto/(?P<pk>\d+)/editar/$',
                           CentroCostoUpdateView.as_view(),
                           name='centrocosto-update',
                       ),
                       url(
                           r'^centrocosto/(?P<pk>\d+)/detalle/$',
                           CentroCostoDetailView.as_view(),
                           name='centrocosto-detail',
                       ),
                       url(
                           r'^centrocosto/eliminar/$',
                           'contabilidad.views.centroCostoEliminarView',
                           name='centrocosto-delete',
                       ),
                       url(
                           r'^centrocosto/(?P<pk>\d+)/eliminar/$',
                           'contabilidad.views.centroCostoEliminarByPkView',
                           name='centrocosto-delete-pk',
                       ),

                       # =================Asiento===========================#
                       url(
                           r'^asiento/$',
                           'contabilidad.views.AsientoListView',
                           name='asiento-list',
                       ),
                       url(
                           r'^asiento/nuevo$',
                           'contabilidad.views.AsientoCreateView',
                           name='asiento-create',
                       ),
                       url(
                           r'^asiento/(?P<pk>\d+)/editar/$',
                           'contabilidad.views.AsientoUpdateView',
                           name='asiento-update',
                       ),
                       url(
                           r'^asiento/(?P<pk>\d+)/detalle/$',
                           AsientoDetailView.as_view(),
                           name='asiento-detail',
                       ),
                       url(
                           r'^asiento/eliminar/$',
                           'contabilidad.views.asientoEliminarView',
                           name='asiento-delete',
                       ),
                       url(
                           r'^asiento/(?P<pk>\d+)/eliminar/$',
                           'contabilidad.views.asientoEliminarByPkView',
                           name='asiento-delete-pk',
                       ),
                       url(
                           r'^asiento/(?P<pk>\d+)/consultar/$',
                           'contabilidad.views.AsientoConsultarView',
                           name='asiento-consultar',
                       ),
                       # ============ESTADOS FINANCIEROS================#
                       url(
                           r'^estado_situacion_financiera/$',
                           'contabilidad.views.estadoSituacionFinancieraView',
                           name='estado-situacion-financiera',
                       ),
                       
                       
                       url(
                           r'^asiento/(?P<pk>\d+)/relacionarFacturas/$',
                           'contabilidad.views.asientoRelacionarFacturasView',
                           name='asiento-relacionar-facturas',
                       ),
                     url(
                           r'^asiento_factura_list/$',
                           'contabilidad.views.asiento_factura_list',
                           name='asiento-factura-list',
                       ),
                     
                     
                     
                     #Asiento asociar Libro Diario
                      url(
                           r'^asiento/(?P<pk>\d+)/asientoRelacionarFacturasLibroDiarioView/$',
                           'contabilidad.views.asientoRelacionarFacturasLibroDiarioView',
                           name='asiento-relacionar-facturas-libro',
                       ),
                     url(
                           r'^asiento_factura_libro_list/$',
                           'contabilidad.views.asiento_factura_libro_list',
                           name='asiento-factura-list-libro',
                       ),
                     
                     url(
                           r'^asiento/asientoRelacionarFacturasLibroDiarioCreateView/$',
                           'contabilidad.views.asientoRelacionarFacturasLibroDiarioCreateView',
                           name='asiento-relacionar-facturas-libro-create',
                       ),
                     
                         url(r'^asiento/(?P<pk>\d+)/imprimir/$','contabilidad.views.imprimir_asiento',name='asiento-imprimir',),
                         url(r'^asiento/(?P<pk>\d+)/imprimir_baja/$','contabilidad.views.imprimir_asiento_baja',name='asiento-imprimir-baja',),
    url(r'^asiento/movimiento/(?P<pk>\d+)/eliminar/$','contabilidad.views.asientoMovimientoEliminarByPkView',name='asiento-movimiento-delete-pk',),
    
                            url(r'^asiento/(?P<pk>\d+)/eliminarbyPk/$','contabilidad.views.asiento_eliminarView',name='asiento-eliminar-pk',),

     url(
                           r'^consultarBalanceDiarioActual/$',
                           'contabilidad.views.consultar_balance_diario',
                           name='consultar-balance-diario',
                       ),
     
     
     url(
                           r'^estado_resultados/$',
                           'contabilidad.views.estadoResultadoView',
                           name='estado-resultado',
                       ),
                       
   
      url(
                           r'^consultarEstadosResultados/$',
                           'contabilidad.views.consultar_estados_resultados',
                           name='consultar-estados-resultados',
                       ),
      
        url(
                           r'^estado_situacion_financiera_mensualizado/$',
                           'contabilidad.views.estadoSituacionFinancieraMensualizadoView',
                           name='estado-situacion-financiera-mensualizado',
                       ),
                        url(
                           r'^consultarBalanceMensualizado/$',
                           'contabilidad.views.consultar_balance_mensualizado',
                           name='consultar-balance-mensualizado',
                       ),
     
     
     url(r'^asiento/prueba/$','contabilidad.views.asiento_list_prueba',name='asiento-prueba',),
     url(r'^asiento/api$','contabilidad.views.asiento_api_view',name='asiento-api',),
     url(
                           r'^estado_resultados_mensual/$',
                           'contabilidad.views.estadoResultadoMensualView',
                           name='estado-resultado-mensual',
                       ),
                       
   
      url(
                           r'^consultarEstadosResultadosMensual/$',
                           'contabilidad.views.consultar_estados_resultados_mensual',
                           name='consultar-estados-resultados-mensual',
                       ),
      
      url(
                           r'^centrocosto/obtenerSubCentro/$',
                           'contabilidad.views.consultarSubCentro',
                           name='centrocosto-consultar-subcentro',
                       ),
      
      url(
                           r'^balance_comprobacion/$',
                           'contabilidad.views.balancedeComprobacionView',
                           name='balance-comprobacion',
                       ),
      
        url(
                           r'^consultarBalanceComprobacion/$',
                           'contabilidad.views.consultar_balance_comprobacion',
                           name='consultar-balance-comprobacion',
                       ),
         url(
                           r'^balance_comprobacion_mensual/$',
                           'contabilidad.views.balanceComprobacionMensualizadoView',
                           name='balance-comprobacion-mensual',
                       ),
      
        url(
                           r'^consultarBalanceComprobacionMensual/$',
                           'contabilidad.views.consultar_balance_comprobacion_mensualizado',
                           name='consultar-balance-comprobacion-mensual',
                       ),
            url(
                           r'^mostrar_motivo_anulacion/$',
                           'contabilidad.views.mostrar_motivo_anulacion',
                           name='mostrar-motivo-anulacion',
                       ),
             url(
                           r'^anulacion_asiento_motivo/$',
                           'contabilidad.views.anulacion_asiento_motivo',
                           name='anulacion-asiento-motivo',
                       ),
             
             
               url(
                           r'^mayores_contables_prueba/$',
                           'contabilidad.views.MayoresContablesActualPruebaView',
                           name='mayores-contables-prueba',
                       ),
                       url(
                           r'^consulta_mayor_actual_prueba/$',
                           'contabilidad.views.ConsultaMayorActualPruebaView',
                           name='consulta-mayor-actual-prueba',
                       ),
                       )
