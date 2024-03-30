from django.conf.urls import patterns, url
from django.views.defaults import *


urlpatterns = patterns('',
    #=================Bancos===========================#
    url(r'^bancos/$', 'bancos.views.banco_list_view', name='bancos-list',),
    url(r'^bancos/add', 'bancos.views.BancoCreateView', name='bancos-add',),
    url(r'^bancos/(?P<pk>\d+)/update/', 'bancos.views.BancoUpdateView', name='bancos-update',),
    url(r'^bancos/(?P<pk>\d+)/eliminar/$','bancos.views.BancoEliminarByPkView',name='banco-delete-pk',),

    #=================Movimientos===========================#
    url(r'^movimiento$', 'bancos.views.movimiento_list_view', name='movimiento-list',),
    url(r'^movimiento/nuevo$', 'bancos.views.movimiento_nuevo_view', name='movimiento-nuevo',),
    url(r'^movimiento/crear$', 'bancos.views.movimiento_crear_view', name='movimiento-crear',),
    url(r'^movimiento/crear_proforma$', 'bancos.views.movimiento_crear_proforma_view', name='movimiento-crear-proforma',),
    url(r'^movimiento/(?P<pk>\d+)/editar/', 'bancos.views.movimiento_edit_view', name='movimiento-edit',),
    url(r'^movimiento/(?P<pk>\d+)/update/', 'bancos.views.movimiento_update_view', name='movimiento-update',),
    url(r'^movimiento/consultar/secuencia', 'bancos.views.consultar_secuencia_cheque', name='consultar-secuencia-cheque'),
    url(r'^movimiento/otros/nuevo$', 'bancos.views.movimiento_otros_nuevo_view', name='movimiento-nuevo-otros',),
    url(r'^movimiento/consultar/facturas', 'bancos.views.consultar_facturas', name='consultar-facturas'),
    url(r'^movimiento_proforma$', 'bancos.views.movimiento_list_proforma_view', name='movimiento-proforma-list',),
    url(r'^movimiento_proforma/nuevo$', 'bancos.views.movimiento_nuevo_proforma_view', name='movimiento-proforma-nuevo',),
    url(r'^movimiento/consultar/proformasAbonar', 'bancos.views.consultar_proformas_abonar', name='consultar-proformas-abonar'),
    url(r'^movimiento_proforma/(?P<pk>\d+)/editar/', 'bancos.views.movimiento_edit_proforma_view', name='movimiento-edit-proforma',),
    url(r'^movimiento/nuevo_cliente$', 'bancos.views.movimiento_nuevo_cliente_view', name='movimiento-nuevo-cliente',),
    url(r'^movimiento/crear_cliente$', 'bancos.views.movimiento_crear_cliente_view', name='movimiento-crear-cliente',),
    url(r'^movimiento_cliente$', 'bancos.views.movimiento_cliente_list_view', name='movimiento-cliente-list', ),
    url(r'^movimiento_cliente/(?P<pk>\d+)/editar/', 'bancos.views.movimiento_edit_cliente_view', name='movimiento-edit-cliente',),
    url(r'^movimiento/(?P<pk>\d+)/debito/consultar', 'bancos.views.debito_consultar_view', name='movimiento-debito-consultar',),
    url(r'^movimiento/(?P<pk>\d+)/consultar_cheque/', 'bancos.views.movimiento_consultar_cheque_view', name='movimiento-consultar-cheque',),

    #=================ChequesProtestados===========================#
    url(r'^cheques_protestados/$', 'bancos.views.cheques_prestados_list_view', name='cheque-protestados-list',),
    url(r'^cheques_protestados/nuevo$', 'bancos.views.cheques_prestados_nuevo_view', name='cheque-protestados-nuevo',),
    url(r'^cheques_protestados/crear$', 'bancos.views.cheques_prestados_crear_view', name='cheque-protestados-crear',),
    url(r'^cheques_protestados/(?P<pk>\d+)/editar/', 'bancos.views.cheques_prestados_edit_view', name='cheque-protestados-edit',),
    url(r'^cheques_protestados/(?P<pk>\d+)/update/', 'bancos.views.cheques_prestados_update_view', name='cheque-protestados-update',),
    url(r'^cheques_protestados/consultar/cheques', 'bancos.views.consultar_cheques_clientes', name='consultar-cheques-clientes'),
    url(r'^cheques_protestados/(?P<pk>\d+)/eliminar/$','bancos.views.chequeProtestadoEliminarByPkView',name='cheques-protestados-eliminar-pk',),
    url(r'^cheques_protestados/abono/$', 'bancos.views.documento_abono_cheque_list_view', name='cheque-protestados-abono',),
    url(r'^cheques_protestados/abono/crear$', 'bancos.views.movimiento_nuevo_abono_cheque_view', name='cheque-protestados-abono-crear',),
    url(r'^cheques_protestados/abono/guardar$', 'bancos.views.movimiento_crear_abono_cheque_view', name='cheque-protestados-abono-guardar',),
url(r'^cheques_protestados/consultar/abono_cheques', 'bancos.views.consultar_abono_cheques_protestados', name='consultar-abono-cheques-protestados'),
    url(r'^cheques_protestados/abono_cheques/(?P<pk>\d+)/eliminar/$','bancos.views.movimientoEliminarAbonoChequeByPkView',name='movimiento-delete-abono-cheque-pk',),

    # =================Conciliaciones===========================#
    url(r'^conciliaciones/$', 'bancos.views.conciliaciones_list_view', name='conciliaciones-list', ),
    url(r'^conciliaciones/nuevo$', 'bancos.views.conciliaciones_nuevo_view', name='conciliaciones-nuevo', ),
    url(r'^conciliaciones/crear$', 'bancos.views.conciliaciones_crear_view', name='conciliaciones-crear', ),
    url(r'^conciliaciones/(?P<pk>\d+)/editar/', 'bancos.views.conciliaciones_edit_view', name='conciliaciones-edit', ),
    url(r'^conciliaciones/(?P<pk>\d+)/update/', 'bancos.views.conciliaciones_update_view', name='conciliaciones-update', ),
    url(r'^conciliaciones/consultar/movimiento_conciliar', 'bancos.views.consultar_movimiento_conciliar', name='consultar-movimiento-conciliar'),
    url(r'^conciliaciones/(?P<pk>\d+)/consultar/', 'bancos.views.conciliaciones_consultar_view', name='conciliaciones-consultar', ),
    url(r'^conciliaciones/consultar/cheques_protestados', 'bancos.views.consultar_ch_protestados_conciliar', name='consultar-cheques-protestados'),
    


    # =================Conciliaciones===========================#
    url(r'^estado_cuenta/$', 'bancos.views.estado_cuenta_list_view', name='estado-cuenta-list', ),
    url(r'^consultar_plan_cuentas_personas_bancos', 'bancos.views.consultar_plan_cuentas_personas_bancos', name='consultar_plan_cuentas_personas_bancos',),
    url(r'^consultar_plan_cobrar_cliente', 'bancos.views.consultar_plan_cobrar_cliente', name='consultar_plan_cobrar_cliente',),
    url(r'^movimiento/(?P<pk>\d+)/imprimir$','bancos.views.imprimir_cheque',name='bancos-imprimir-cheque',),
    url(r'^movimiento/(?P<pk>\d+)/eliminar/$','bancos.views.movimientoEliminarByPkView',name='movimiento-delete-pk',),
    url(r'^movimiento/(?P<pk>\d+)/imprimir_orden_egreso/$','bancos.views.imprimir_comprobante_egreso',name='movimiento-comprobante-egreso',),
    url(r'^movimiento/(?P<pk>\d+)/imprimir_conciliacion/$','bancos.views.imprimir_pdf_conciliaciones_view',name='imprimir-conciliacion',),

    #===================REPORTES===============================#
    url(r'^reporte/estado_cuenta_proveedor/$','bancos.views.estadoCuentaProveedorView',name='estado-cuenta-proveedor',),
    url(r'^reporte/consulta_cuenta_proveedor/$','bancos.views.consultaCuentaProveedorView',name='consulta-cuenta-proveedor',),

                       # =================ChequesNoCobrados===========================#
                       url(r'^cheques_no_cobrados/$', 'bancos.views.cheques_no_cobrados_list_view',
                           name='cheque-no-cobrado-list', ),
                       url(r'^cheques_no_cobrados/nuevo$', 'bancos.views.cheques_no_cobrados_nuevo_view',
                           name='cheque-no-cobrado-nuevo', ),
                       url(r'^cheques_no_cobrados/crear$', 'bancos.views.cheques_no_cobrados_crear_view',
                           name='cheque-no-cobrado-crear', ),
                       url(r'^cheques_no_cobrados/(?P<pk>\d+)/editar/', 'bancos.views.cheques_no_cobrados_edit_view',
                           name='cheque-no-cobrado-edit', ),
                       url(r'^cheques_no_cobrados/(?P<pk>\d+)/update/', 'bancos.views.cheques_no_cobrados_update_view',
                           name='cheque-no-cobrado-update', ),
                       url(r'^movimiento/consultar_factura_proforma', 'bancos.views.consultar_factura_proforma', name='consultar-factura-proforma'),
                       url(r'^movimiento/consultar_actual_factura_proforma', 'bancos.views.consultar_actual_factura_proforma', name='consultar-factura-proforma-actual'),

  url(r'^movimientoClienteUpdateView/(?P<pk>\d+)/update/', 'bancos.views.MovimientoClienteUpdateView',
                           name='movimiento-update-cliente', ),
  url(r'^consultar_plan_cuentas_parametros', 'bancos.views.consultar_plan_cuentas_parametros', name='consultar_plan_cuentas_parametros',),
                       
                       #====================NOTA DE CREDITO==============#
                           url(r'^movimiento/proveedor/nota_credito$', 'bancos.views.movimiento_list_nota_credito_proveedor_view', name='movimiento_list_nota_credito_proveedor',),

                       url(r'^movimiento/movimiento_proveedor_nota_credito_view$', 'bancos.views.movimiento_proveedor_nota_credito_view', name='movimiento_proveedor_nota_credito_view',),
                       url(r'^movimiento/consultar/consultar_factura_pagadas_proveedor', 'bancos.views.consultar_factura_pagadas_proveedor', name='consultar_factura_pagadas_proveedor'),
    url(r'^movimiento/(?P<pk>\d+)/imprimir_nc_proveedor/$','bancos.views.imprimir_comprobante_nc_proveedor',name='movimiento-imprimir-nc-proveedor',),


  url(r'^movimiento/nc/bancaria/cliente$', 'bancos.views.movimiento_list_nc_cliente_bancaria_view', name='movimiento-nc-bancaria-cliente-list',),
    url(r'^movimiento/nc/bancaria/cliente/nuevo$', 'bancos.views.movimiento_nuevo_nc_bancaria_cliente_view', name='movimiento-nc-bancaria-cliente-nuevo',),
    url(r'^movimiento/nc/bancaria/cliente/crear$', 'bancos.views.movimiento_crear_nc_bancaria_cliente_view', name='movimiento-nc-bancaria-cliente-crear',),
        url(r'^movimiento/(?P<pk>\d+)/eliminar/nc_bancaria_cliente/$','bancos.views.movimientoNotaCreditoClienteEliminarByPkView',name='movimiento-nc-cliente-delete-pk',),

    url(r'^movimiento/nc/comercial$', 'bancos.views.NotaCreditoComercialListView', name='movimiento-nc-comercial',),
    url(r'^movimiento/nc/comercial/cliente/nuevo$', 'bancos.views.NotaCreditoComercialCreateView', name='movimiento-nc-comercial-cliente-nuevo',),
        url(r'^movimiento/(?P<pk>\d+)/imprimir_nc_comercial/$','bancos.views.imprimir_comprobante_nc_comercial',name='movimiento-imprimir-nc-comercial',),
    url(r'^movimiento/(?P<pk>\d+)/clienteeliminar/$','bancos.views.movimientoEliminarClienteByPkView',name='movimiento-deletecliente-pk',),
      url(r'^movimiento/validarCheque/$','bancos.views.validarCheque',name='movimiento-validar-numero-cheque',),

        url(r'^movimiento/nuevo_deposito$', 'bancos.views.movimiento_deposito_view', name='movimiento-nuevo-deposito',),
        url(r'^movimiento/crear_deposito$', 'bancos.views.movimiento_crear_deposito_view', name='movimiento-crear-deposito',),
    url(r'^movimiento/deposito$', 'bancos.views.movimiento_list_deposito_view', name='movimiento-deposito-list',),
    url(r'^movimiento/(?P<pk>\d+)/imprimir_deposito/$','bancos.views.imprimir_deposito',name='movimiento-imprimir-deposito',),
 url(r'^movimiento/debito$', 'bancos.views.nota_debito_list_view', name='movimiento-debito-list',),
    url(r'^movimiento/debito/nuevo$', 'bancos.views.nota_debito_nuevo_view', name='movimiento-debito-nuevo',),
    url(r'^movimiento/debito/crear$', 'bancos.views.nota_debito_crear_view', name='movimiento-debito-crear',),
    url(r'^movimiento/(?P<pk>\d+)/imprimir_nd/$','bancos.views.imprimir_nd',name='movimiento-imprimir-nd',),
    url(r'^movimiento/cheques_posfechados$', 'bancos.views.movimiento_cliente_cheques_posfechados', name='movimiento-cheques-posfechados-list',),
url(r'^movimiento/nuevo_cliente_cheques_posfechados$', 'bancos.views.movimiento_nuevo_cliente_cheques_posfechados_view', name='movimiento-nuevo-cliente-cheques-posfechados',),
    url(r'^movimiento/movimiento_crear_cliente_cheques_posfechados$', 'bancos.views.movimiento_crear_cliente_cheques_posfechados_view', name='movimiento-crear-cliente-cheques-posfechados',),
        url(r'^movimiento/guardarMovimientoDescripcion$', 'bancos.views.guardarMovimientoDescripcion', name='movimiento-guardar-descripcion',),
url(r'^movimiento/(?P<pk>\d+)/imprimir_cheque_actual$','bancos.views.imprimir_cheque_actual',name='bancos-imprimir-cheque-actual',),

url(r'^movimiento/(?P<pk>\d+)/imprimir_cheque_pdf$','bancos.views.imprimir_cheque_pdf',name='bancos-imprimir-cheque-pdf',),
url(r'^movimiento/(?P<pk>\d+)/editar_proveedor_nota_credito_view/', 'bancos.views.edit_movimiento_proveedor_nota_credito_view', name='editar-movimiento-nc',),
url(r'^movimiento/deposito/(?P<pk>\d+)/editar/', 'bancos.views.movimiento_edit_deposito_view', name='movimiento-edit-deposito',),
    url(r'^movimiento/deposito/(?P<pk>\d+)/update/', 'bancos.views.movimiento_update_deposito_view', name='movimiento-update-deposito',),
    url(r'^movimiento/deposito/(?P<pk>\d+)/consultar/', 'bancos.views.movimiento_consultar_deposito_view', name='movimiento-consultar-deposito',),

    #REEMPLAZO DE PROFORMAS A abonos de facturas
        url(r'^proformas_reemplazo_abono/$', 'bancos.views.proforma_factura_list_view', name='proformas-facturas-reemplazo-list',),
        url(r'^proformas_reemplazo_abono/(?P<pk>\d+)/abonar/', 'bancos.views.proforma_factura_corregir_abono_view', name='proforma-factura-corregir-abono',),
        url(r'^mostrar_proformas_abonos_facturas/$', 'bancos.views.MostrarProformasFacturasAbonoView', name='mostrar-proformas-abonos-facturas',),
        url(r'^guardarInversionAbonoProformaFactura/$', 'bancos.views.guardarInversionAbonoProformaFactura', name='guardar-proformas-abonos-facturas',),

url(r'^movimiento/prueba$', 'bancos.views.movimiento_prueba_list_view', name='movimiento-prueba-list',),
    url(r'^movimiento/api$', 'bancos.views.movimiento_api_view', name='movimiento-api',),
        url(r'^movimiento/nc/bancaria/cliente/(?P<pk>\d+)/consultar', 'bancos.views.movimiento_nc_cliente_bancaria_consultar_view', name='movimiento-nc-cliente-bancaria-consultar',),
        url(r'^movimiento/cliente/(?P<pk>\d+)/consultar', 'bancos.views.movimiento_deposito_cliente_consultar_view', name='movimiento-deposito-cliente-consultar',),
        
        url(r'^movimiento/validarBloqueoPeriodo/$','bancos.views.validarBloqueoPeriodo',name='movimiento-validar-bloqueo-periodo',),

  url(
                           r'^reporte_por_movimiento/$',
                           'bancos.views.ReporteTipoMovimientoView',
                           name='reporte-por-movimiento',
                       ),
                       url(
                           r'^consulta_reporte_por_movimiento/$',
                           'bancos.views.ConsultaReporteTipoMovimientoView',
                           name='consulta-reporte-por-movimiento',
                       ),
                       
                       url(
                           r'^movimientoNotaCreditoComercialEliminarByPkView/(?P<pk>\d+)/$',
                           'bancos.views.movimientoNotaCreditoComercialEliminarByPkView',
                           name='delete-movimiento-nc-comercial',
                       ),
                       url(
                           r'^reporte_por_cheque/$',
                           'bancos.views.reporteporChequesView',
                           name='reporte-por-cheque',
                       ),
                       url(
                           r'^consulta_reporte_por_cheque/$',
                           'bancos.views.ConsultaReporteporChequeView',
                           name='consulta-reporte-por-cheque',
                       ),
                       
                       url(
                           r'^reporte_por_deposito/$',
                           'bancos.views.reporteporDepositoView',
                           name='reporte-por-deposito',
                       ),
                       url(
                           r'^consulta_reporte_por_deposito/$',
                           'bancos.views.ConsultaReporteporDepositoView',
                           name='consulta-reporte-por-deposito',
                       ),
                       
                        url(
                           r'^reporte_por_nota_credito/$',
                           'bancos.views.reporteporNotadeCreditoView',
                           name='reporte-por-nota-credito',
                       ),
                       url(
                           r'^consulta_reporte_por_nota_credito/$',
                           'bancos.views.ConsultaReporteporNotadeCreditoView',
                           name='consulta-reporte-por-nota-credito',
                       ),
                       
                       url(
                           r'^reporte_por_nota_debito/$',
                           'bancos.views.reporteporNotadeDebitoView',
                           name='reporte-por-nota-debito',
                       ),
                       url(
                           r'^consulta_reporte_por_nota_debito/$',
                           'bancos.views.ConsultaReporteporNotadeDebitoView',
                           name='consulta-reporte-por-nota-debito',
                       ),
                       
                       
                        url(
                           r'^consulta_nota_credito_electronica/$',
                           'bancos.views.consultar_nota_credito_electronica',
                           name='consulta-nota-credito-electronica',
                       ),
                        
                        
                        	url(r'^consultar_datos_nota_credito_electronica/(?P<pk>\d+)/', 'bancos.views.consultar_datos_nota_credito_electronica', name='consultar-datos-nota-electronica', ),

                       )
