from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',
                       url(
                           r'^reporte/principal$',
                           'reporte.views.principal',
                           name='reporte-principal',
                       ),
                       url(
                           r'^reporte/pedido$',
                           'reporte.views.reportepedido',
                           name='reporte-pedido',
                       ),

                       url(
                           r'^obtenerPedidoPendiente/$',
                           'reporte.views.obtenerPedidoPendiente',
                           name='reporte-obtenerpedidopendiente',
                       ),
                       url(
                           r'^reporte/ordenproduccion$',
                           'reporte.views.reporteordenproduccion',
                           name='reporte-ordenproduccion',
                       ),

                       url(
                           r'^obtenerOrdenProduccionCliente/$',
                           'reporte.views.obtenerOrdenProduccionCliente',
                           name='reporte-obtenerordenproduccioncliente',
                       ),
                       url(
                           r'^reporte/guiaremision$',
                           'reporte.views.reporteguias',
                           name='reporte-guiaremision',
                       ),

                       url(
                           r'^obtenerGuiaEmitida/$',
                           'reporte.views.obtenerGuiaEmitida',
                           name='reporte-obtenerguiaemitida',
                       ),
                       url(
                           r'^reporte/reportepedidoporfacturar$',
                           'reporte.views.reportepedidoporfacturar',
                           name='reporte-reportepedidoporfacturar',
                       ),

                       url(
                           r'^obtenerPedidoPorFacturar/$',
                           'reporte.views.obtenerPedidoPorFacturar',
                           name='reporte-obtenerpedidoporfacturar',
                       ),
                       url(
                           r'^reporte/global$',
                           'reporte.views.reporteglobal',
                           name='reporte-reporteglobal',
                       ),

                       url(
                           r'^obtenerGlobal/$',
                           'reporte.views.obtenerGlobal',
                           name='reporte-obtenerglobal',
                       ),
                       url(
                           r'^reporte/reporteliquidacioncomisiones/$',
                           'reporte.views.reporteliquidacioncomisiones',
                           name='reporte-liquidacion-comisiones',
                       ),

                       url(
                           r'^obtenerLiquidacionesComisiones/$',
                           'reporte.views.obtenerLiquidacionesComisiones',
                           name='reporte-obtenerLiquidacionesComisiones',
                       ),
                       url(
                           r'^reporte/reporteDiarioVentas/$',
                           'reporte.views.reporteDiarioVentas',
                           name='reporte-diario-ventas',
                       ),

                       url(
                           r'^obtenerDiarioVentas/$',
                           'reporte.views.obtenerDiarioVentas',
                           name='reporte-obtener-diarioventas',
                       ),
                       url(
                           r'^reporte/reporteDiarioGuias/$',
                           'reporte.views.reporteDiarioGuias',
                           name='reporte-diario-guias',
                       ),

                       url(
                           r'^obtenerDiarioGuias/$',
                           'reporte.views.obtenerDiarioGuias',
                           name='reporte-obtener-diarioguias',
                       ),
                       url(
                           r'^reporte/principal-inventario$',
                           'reporte.views.principalInventario',
                           name='reporte-principal-inventario',
                       ),
                       url(
                           r'^reporte/inventario$',
                           'reporte.views.reporteInventario',
                           name='reporte-inventario',
                       ),
                       url(
                           r'^obtenerInventario/$',
                           'reporte.views.obtenerInventario',
                           name='obtener-inventario',
                       ),
                       url(
                           r'^reporte/ordencompra$',
                           'reporte.views.reporteOrdenCompra',
                           name='reporte-orden-compra',
                       ),
                       url(
                           r'^obtenerOrdenCompra/$',
                           'reporte.views.obtenerOrdenCompra',
                           name='obtener-orden-compra',
                       ),
                       url(
                           r'^reporte/ordeningreso$',
                           'reporte.views.reporteOrdenIngreso',
                           name='reporte-orden-ingreso',
                       ),
                       url(
                           r'^obtenerOrdenIngreso/$',
                           'reporte.views.obtenerOrdenIngreso',
                           name='obtener-orden-ingreso',
                       ),
                       url(
                           r'^reporte/ordenegreso$',
                           'reporte.views.reporteOrdenEgreso',
                           name='reporte-orden-egreso',
                       ),
                       url(
                           r'^obtenerOrdenEgreso/$',
                           'reporte.views.obtenerOrdenEgreso',
                           name='obtener-orden-egreso',
                       ),
                       url(
                           r'^reporte/reporteDiarioVentasActual/$',
                           'reporte.views.reporteDiarioVentasActual',
                           name='reporte-diario-ventas-actual',
                       ),

                       url(
                           r'^obtenerDiarioVentasActual/$',
                           'reporte.views.obtenerDiarioVentasActual',
                           name='reporte-obtener-diarioventas-actual',
                       ),
                       url(
                           r'^reporte/reporteGuiasGeneral/$',
                           'reporte.views.reporteGuiasGeneral',
                           name='reporte-guias-general',
                       ),

                       url(
                           r'^obtenerGuiasGeneral/$',
                           'reporte.views.obtenerGuiasGeneral',
                           name='reporte-obtener-guias-general',
                       ),
                       url(
                           r'^reporte/compraslocales$',
                           'reporte.views.reporteComprasLocales',
                           name='reporte-compras-locales',
                       ),
                       url(
                           r'^obtenerComprasLocales/$',
                           'reporte.views.obtenerComprasLocales',
                           name='obtener-compras-locales',
                       ),
                       url(
                           r'^obtenerComprasLocalesAgruparProducto/$',
                           'reporte.views.obtenerComprasLocalesAgruparProducto',
                           name='obtener-compras-locales-agrupado-producto',
                       ),
                       url(
                           r'^obtenerOrdenCompraAgruparProducto/$',
                           'reporte.views.obtenerOrdenCompraAgruparProducto',
                           name='obtener-compras-agrupado-producto',
                       ),
                       url(
                           r'^obtenerInventarioTipoProducto/$',
                           'reporte.views.obtenerInventarioTipoProducto',
                           name='obtener-inventario-tipo-producto',
                       ),
                       url(r'^export/$',
                           'reporte.views.export_to_excel', name='export_to_excel'),

                       url(
                           r'^reporteLiquidacionTotal/$',
                           'reporte.views.reporteLiquidacionTotal',
                           name='reporte-liquidacion-total',
                       ),

                       url(
                           r'^obtenerLiquidacionTotal/$',
                           'reporte.views.obtenerLiquidacionTotal',
                           name='reporte-obtener-liquidacion-total',
                       ),

                       url(
                           r'^reporte/reporteDiarioVentasMensual/$',
                           'reporte.views.reporteDiarioVentasMensual',
                           name='reporte-diario-ventas-mensual',
                       ),

                       url(
                           r'^obtenerDiarioVentasMensual/$',
                           'reporte.views.obtenerDiarioVentasMensual',
                           name='reporte-obtener-diarioventas-mensual',
                       ),

                       url(
                           r'^reporte/reporteDiarioVentasAnual/$',
                           'reporte.views.reporteDiarioVentasAnual',
                           name='reporte-diario-ventas-anual',
                       ),

                       url(
                           r'^obtenerDiarioVentasAnual/$',
                           'reporte.views.obtenerDiarioVentasAnual',
                           name='reporte-obtener-diarioventas-anual',
                       ),

                       url(
                           r'^reporte/reporteCuentasCobrar/$',
                           'reporte.views.reporteCuentasCobrar',
                           name='reporte-cuentas-cobrar',
                       ),

                       url(
                           r'^obtenerCuentasCobrar/$',
                           'reporte.views.obtenerCuentasCobrar',
                           name='reporte-obtener-cuentas-cobrar',
                       ),

                       url(
                           r'^leerArchivoCSV/$',
                           'reporte.views.leerArchivoCSV',
                           name='reporte-leer-archivo',
                       ),
                       url(
                           r'^cargarPlantilla/$',
                           'reporte.views.cargarPlantillaCSV',
                           name='reporte-cargar-plantilla',
                       ),

                       url(
                           r'^reporte/reporteVentas/$',
                           'reporte.views.reporteVentas',
                           name='reporte-ventas',
                       ),

                       url(
                           r'^obtenerReporteVentas/$',
                           'reporte.views.obtenerReporteVentas',
                           name='reporte-obtener-ventas',
                       ),
                       url(
                           r'^control-cobro-diario/$',
                           'reporte.views.controlCobroDiarioReport',
                           name='control-cobro-diario',
                       ),

                       url(
                           r'^cargarPlantillaNormalCSV/$',
                           'reporte.views.cargarPlantillaNormalCSV',
                           name='reporte-cargar-plantilla-normal',
                       ),
                       url(
                           r'^prueba/$',
                           'reporte.views.prueba',
                           name='reporte-prueba',
                       ),

url(
                           r'^migracionCliente/$',
                           'reporte.views.MigracionCliente',
                           name='migracion-cliente',
                       ),


url(
                           r'^reporte/egresoxordenegreso$',
                           'reporte.views.reporteEgresoxOrdenEgreso',
                           name='reporte-egreso-orden-egreso',
                       ),
                       url(
                           r'^obtenerEgresoxOrdenEgreso/$',
                           'reporte.views.obtenerEgresoxOrdenEgreso',
                           name='obtener-egreso-orden-egreso',
                       ),

url(
                           r'^reporte/kardex',
                           'reporte.views.reporteKardex',
                           name='reporte-kardex',
                       ),
                       url(
                           r'^obtenerKardex/$',
                           'reporte.views.obtenerKardex',
                           name='obtener-kardex',
                       ),

url(
                           r'^cargarReloj/$',
                           'reporte.views.cargarReloj',
                           name='reporte-cargar-reloj',
                       ),


url(
                           r'^cargarRelojFinal/$',
                           'reporte.views.cargarRelojFinal',
                           name='reporte-cargar-reloj-final',
                       ),

url(
                           r'^reporteInventarioExistente/$',
                           'reporte.views.reporteInventarioExistente',
                           name='reporte-inventario-existente',
                       ),
url(
                           r'^obtenerInventarioInicial/$',
                           'reporte.views.obtenerInventarioInicial',
                           name='obtener-inventario-inicial',
                       ),
  url(
                           r'^reporte/factura_proveedor$',
                           'reporte.views.reporteFacturaProveedor',
                           name='reporte-factura-proveedor',
                       ),
                      url(
                           r'^obtenerFacturaProveedor/$',
                           'reporte.views.obtenerFacturaProveedor',
                           name='obtener-fatura-proveedor',
                       ),
                      
                      
                      
                        url(
                           r'^reporte/factura_proveedor_cancelada_cheque$',
                           'reporte.views.reportePorProveedorFacurasCanceladasCheque',
                           name='reporte-factura-proveedor-cancelada-cheque',
                       ),
                      url(
                           r'^obtenerFacturaProveedorCanceladaCheque/$',
                           'reporte.views.obtenerFacturaProveedorFacurasCanceladasCheque',
                           name='obtener-fatura-proveedor-cancelada-cheque',
                       ),
                      
                         url(
                           r'^reporte/proforma_vs_factura$',
                           'reporte.views.reporteProformavsFactura',
                           name='reporte-proforma-vs-factura',
                       ),
                      url(
                           r'^obtenerProformavsFactura/$',
                           'reporte.views.obtenerProformavsFactura',
                           name='obtener-proforma-vs-factura',
                       ),
                      
                       url(
                           r'^reporte/facturas_pagadas_abonadas$',
                           'reporte.views.reporteFacturasPagadasAbonadas',
                           name='reporte-facturas-abonadas-pagadas',
                       ),
                      url(
                           r'^obtenerFacturasPagadasAbonadas/$',
                           'reporte.views.obtenerFacturasPagadasAbonadas',
                           name='obtener-facturas-pagadas-abonadas',
                       ),
                      
                       url(
                           r'^reporte/movimiento_tarjeta_credito$',
                           'reporte.views.reporteMovimientoTarjetaCredito',
                           name='reporte-movimiento-tarjeta-credito',
                       ),
                      url(
                           r'^obtenerMovimientosTarjetaCredito/$',
                           'reporte.views.obtenerMovimientosTarjetaCredito',
                           name='obtener-movimientos-tarjeta-credito',
                       ),

                      #------------------------------->
                       url(
                           r'^reporte/estado_cuenta_cliente_resumen$',
                           'reporte.views.reportePorEstadoCuentaClientesResumen',
                           name='reporte-estado-cuenta-cliente-resumen',
                       ),

                       url(
                           r'^obtenerEstadoCuentaClientesResumen/$',
                           'reporte.views.obtenerEstadoCuentaClientesResumen',
                           name='obtener-estado-cuenta-cliente-resumen',
                       ),

                      #------------------------------->
                       url(
                           r'^reporte/saldos_anticipos_clientes$',
                           'reporte.views.reporteAnticiposClientesResumen',
                           name='reporte-anticipos-cliente-resumen',
                       ),

                      #------------------------------->
                        url(
                           r'^reporte/estado_cuenta_cliente$',
                           'reporte.views.reportePorEstadoCuentaFacturasClientes',
                           name='reporte-estado-cuenta-cliente',
                        ),
                      url(
                           r'^obtenerEstadoCuentaFacturasClientes/$',
                           'reporte.views.obtenerEstadoCuentaFacturasClientes',
                           name='obtener-estado-cuenta-cliente',
                       ),
                      
                         url(
                           r'^reporte/inventarioNuevo$',
                           'reporte.views.reporteInventarioNuevo',
                           name='reporte-inventario-nuevo',
                       ),
                       url(
                           r'^obtenerInventarioNuevo/$',
                           'reporte.views.obtenerInventarioNuevo',
                           name='obtener-inventario-nuevo',
                       ),
                       
                        url(
                           r'^reporte/ordencompraNuevo$',
                           'reporte.views.reporteOrdenCompraNuevo',
                           name='reporte-orden-compra-nuevo',
                       ),
                       url(
                           r'^obtenerOrdenCompraNuevo/$',
                           'reporte.views.obtenerOrdenCompraNuevo',
                           name='obtener-orden-compra-nuevo',
                       ),
                        url(
                           r'^reporte/compraslocalesNuevo$',
                           'reporte.views.reporteComprasLocalesNuevo',
                           name='reporte-compras-locales-nuevo',
                       ),
                       url(
                           r'^obtenerComprasLocalesNuevo/$',
                           'reporte.views.obtenerComprasLocalesNuevo',
                           name='obtener-compras-locales-nuevo',
                       ),
                        url(
                           r'^reporte/ordenegresoNuevo$',
                           'reporte.views.reporteOrdenEgresoNuevo',
                           name='reporte-orden-egreso-nuevo',
                       ),
                       url(
                           r'^obtenerOrdenEgresoNuevo/$',
                           'reporte.views.obtenerOrdenEgresoNuevo',
                           name='obtener-orden-egreso-nuevo',
                       ),
                       
                       url(
                           r'^reporte/egresoxordenegresoNuevo$',
                           'reporte.views.reporteEgresoxOrdenEgresoNuevo',
                           name='reporte-egreso-orden-egreso-nuevo',
                       ),
                       url(
                           r'^obtenerEgresoxOrdenEgresoNuevo/$',
                           'reporte.views.obtenerEgresoxOrdenEgresoNuevo',
                           name='obtener-egreso-orden-egreso-nuevo',
                       ),
                       url(
                           r'^kardexNuevo/$',
                           'reporte.views.reporteKardexNuevo',
                           name='reporte-kardex-nuevo',
                       ),
                       url(
                           r'^obtenerKardexNuevo/$',
                           'reporte.views.obtenerKardexNuevo',
                           name='obtener-kardex-nuevo',
                       ),
                        url(
                           r'^reporte/principal-inventario-nuevo$',
                           'reporte.views.principalInventarioNuevo',
                           name='reporte-principal-inventario-nuevo',
                       ),
                         url(
                           r'^reporte/reporteManoObra$',
                           'reporte.views.reporteManoObra',
                           name='reporte-mano-obra',
                       ),
                      url(
                           r'^obtenerManoObra/$',
                           'reporte.views.obtenerManoObra',
                           name='obtener-mano-obra',
                       ),
                      
                       url(
                           r'^reporte/reporteCostoMateriales$',
                           'reporte.views.reporteCostoMateriales',
                           name='reporte-costo-materiales',
                       ),
                      url(
                           r'^obtenerCostoMateriales/$',
                           'reporte.views.obtenerCostoMateriales',
                           name='obtener-costo-materiales',
                       ),
                      
                         url(
                           r'^reporteValoresReaudados$',
                           'reporte.views.reporteValoresReaudados',
                           name='reporte-valores-recaudados',
                       ),
                      url(
                           r'^obtenerValoresRecaudados/$',
                           'reporte.views.obtenerValoresRecaudados',
                           name='obtener-valores-recaudados',
                       ),
                      
                       url(
                           r'^reportePorClientesDiarioVentas$',
                           'reporte.views.reportePorClientesDiarioVentas',
                           name='reporte-clientes-diario-ventas',
                       ),
                      url(
                           r'^obtenerClientesDiarioVentas/$',
                           'reporte.views.obtenerClientesDiarioVentas',
                           name='obtener-clientes-diario-ventas',
                       ),
                      
                      
                      
                      url(
                           r'^reporte/reportePorDiarioRecaudaciones$',
                           'reporte.views.reportePorDiarioRecaudaciones',
                           name='reporte-diario-recaudaciones',
                       ),
                      url(
                           r'^obtenerDiarioRecaudaciones/$',
                           'reporte.views.obtenerDiarioRecaudaciones',
                           name='obtener-diario-recaudaciones',
                       ),
                      
                       url(
                           r'^reporte/estado_cuenta_cliente_sin_proforma$',
                           'reporte.views.reportePorEstadoCuentaFacturasClientesSinProforma',
                           name='reporte-estado-cuenta-cliente-sin-proforma',
                       ),
                      url(
                           r'^obtenerEstadoCuentaFacturasClientesSinProforma/$',
                           'reporte.views.obtenerEstadoCuentaFacturasClientesSinProforma',
                           name='obtener-estado-cuenta-cliente-sin-proforma',
                       ),
                      
                      
                      url(
                           r'^reporte/reporteordenproduccionxEstado$',
                           'reporte.views.reporteordenproduccionxEstado',
                           name='reporte-ordenproduccion-estado',
                       ),

                       url(
                           r'^obtenerOrdenProduccionxEstado/$',
                           'reporte.views.obtenerOrdenProduccionxEstado',
                           name='reporte-obtenerordenproduccionestado',
                       ),

                       #Cuentas por Cobrar Clientes
                       url(
                           r'^reporte/reporteSaldosClientesCobrar/$',
                           'reporte.views.reporteSaldosClientesCobrar',
                           name='reporte-saldos-clientes-cobrar',
                       ),

                       url(
                           r'^reporte/reporteSaldosClientesCobrarVenc/$',
                           'reporte.views.reporteSaldosClientesCobrarVenc',
                           name='reporte-saldos-clientes-cobrar-venc',
                       ),

                       url(
                           r'^obtenerSaldosClientesCobrar/$',
                           'reporte.views.obtenerSaldosClientesCobrar',
                           name='reporte-obtener-saldos-clientes-cobrar',
                       ),

                       url(
                           r'^obtenerSaldosClientesCobrarVenc/$',
                           'reporte.views.obtenerSaldosClientesCobrarVenc',
                           name='reporte-obtener-saldos-clientes-cobrar-venc',
                       ),

                       url(
                           r'^reporte/reporteSaldosAnticiposCobrar/$',
                           'reporte.views.reporteSaldosAnticiposCobrar',
                           name='reporte-saldos-anticipos-cobrar',
                       ),

                       url(
                           r'^obtenerSaldosAnticiposCobrar/$',
                           'reporte.views.obtenerSaldosAnticiposCobrar',
                           name='reporte-obtener-saldos-anticipos-cobrar',
                       ),
                       
                         url(
                           r'^reporte/reporteSaldosProveedoresPagar/$',
                           'reporte.views.reporteSaldosProveedoresPagar',
                           name='reporte-saldos-proveedores-pagar',
                       ),

                       url(
                           r'^obtenerSaldosProveedoresPagar/$',
                           'reporte.views.obtenerSaldosProveedoresPagar',
                           name='reporte-obtener-saldos-proveedor-pagar',
                       ),
                       
                       
                         url(
                           r'^reporte/reporteRangoProveedores/$',
                           'reporte.views.reporteRangoProveedores',
                           name='reporte-rango-proveedores',
                       ),

                       url(
                           r'^obtenerRangoProveedores/$',
                           'reporte.views.obtenerRangoProveedores',
                           name='reporte-obtener-rango-proveedores',
                       ),
                       
                        url(
                           r'^reporte/reporteSaldosEmpleadosCobrar/$',
                           'reporte.views.reporteSaldosEmpleadosCobrar',
                           name='reporte-saldos-empleados-cobrar',
                       ),

                       url(
                           r'^obtenerSaldosEmpleadosCobrar/$',
                           'reporte.views.obtenerSaldosEmpleadosCobrar',
                           name='reporte-obtener-saldos-empleados',
                       ),
                       
                       
                       
                        url(
                           r'^reporte/reporteSaldosAnticiposPagados/$',
                           'reporte.views.reporteSaldosAnticiposPagados',
                           name='reporte-saldos-anticipos-pagados',
                       ),

                       url(
                           r'^obtenerSaldosAnticiposPagados/$',
                           'reporte.views.obtenerSaldosAnticiposPagados',
                           name='reporte-obtener-saldos-anticipos-pagados',
                       ),
                       
                       
                      
                        url(
                           r'^inventarioNuevoContable$',
                           'reporte.views.reporteInventarioNuevoContable',
                           name='reporte-inventario-nuevo-contable',
                       ),
                       url(
                           r'^obtenerInventarioNuevoContable/$',
                           'reporte.views.obtenerInventarioNuevoContable',
                           name='obtener-inventario-nuevo-contable',
                       ),
                       )
