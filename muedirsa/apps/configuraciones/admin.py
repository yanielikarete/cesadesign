from django.contrib import admin
from muedirsa.apps.configuraciones.models import Empresa,Conexion
from config.models import *

from bancos.models import *


class EmpresaAdmin(admin.ModelAdmin):
   fields = ['nombre_empresa', 'base_de_datos','condicion', 'icono_asociado','folder_empresa', 'registro_tributario_empresa','direccion1', 'direccion2', 'direccion3','telefono1', 'celular','fax', 'correo_electronico','sitio_web', 'registro_empresarial', 'barrio_distrito','ciudad', 'codigo_postal','pais', 'logo']

admin.site.register(Empresa, EmpresaAdmin)

class ConexionAdmin(admin.ModelAdmin):
   fields = ['string_de_conexion', 'ruta_para_data','computador_base', 'servidor_de_datos']

admin.site.register(Conexion, ConexionAdmin)


class MenuAdmin(admin.ModelAdmin):
    model = MenuGroup
    list_display = ['id','cod_parent', 'nom_option', 'num_order', 'txt_url', ]
    list_filter = ['cod_parent', 'nom_option']
     # Allows column order sorting

admin.site.register(Menu, MenuAdmin)

class MenuGroupAdmin(admin.ModelAdmin):
    model = MenuGroup
    list_display = ['menu', 'get_name', ]
    list_filter = ['menu','group']

    def get_name(self, obj):
        return obj.group.name

    get_name.admin_order_field = 'menu'  # Allows column order sorting
    get_name.short_description = 'GRUPO'  # Renames column head


admin.site.register(MenuGroup, MenuGroupAdmin)


class MovimientoAdmin(admin.ModelAdmin):
    model = Movimiento
    list_display = ['id','tipo_anticipo','proveedor', 'tipo_documento','numero_comprobante', 'monto_cheque', 'monto' ]
    list_filter = ['tipo_anticipo', 'tipo_documento','numero_comprobante', 'monto_cheque', 'monto' ]
    
admin.site.register(Movimiento, MovimientoAdmin)


