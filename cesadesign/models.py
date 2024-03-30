# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class CategoriasClte(models.Model):
    categoria_clte_id = models.IntegerField(primary_key=True)
    descripcion_categ = models.CharField(max_length=35)
    predeterminado = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'Categorias_clte'

class Ambiente(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'ambiente'

class AnalisisInventario(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    bodega_id = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'analisis_inventario'

class AnalisisInventarioDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    analisis_inventario = models.ForeignKey(AnalisisInventario, blank=True, null=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    cantidad_real = models.FloatField(blank=True, null=True)
    diferencia = models.FloatField(blank=True, null=True)
    observaciones = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'analisis_inventario_detalle'

class AnalisisPrestamo(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=255, blank=True)
    fecha = models.DateField(blank=True, null=True)
    sueldo_fijo = models.FloatField(blank=True, null=True)
    empleado = models.ForeignKey('EmpleadosEmpleado', blank=True, null=True)
    departamento = models.ForeignKey('Departamento', blank=True, null=True)
    tipoempleado = models.ForeignKey('EmpleadosTipoempleado', blank=True, null=True)
    tiempo_servicio = models.CharField(max_length=255, blank=True)
    motivo_anticipo = models.CharField(max_length=500, blank=True)
    monto_solicitado = models.FloatField(blank=True, null=True)
    plazo_solicitar = models.CharField(max_length=255, blank=True)
    monto_neto_promedio = models.FloatField(blank=True, null=True)
    monto_promedio_fin_mes = models.FloatField(blank=True, null=True)
    monto_disponible_descuento = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'analisis_prestamo'

class AnalisisPrestamoDescuentos(models.Model):
    id = models.IntegerField(primary_key=True)
    mes = models.IntegerField(blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)
    quincena = models.IntegerField(blank=True, null=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey('TipoIngresoEgresoEmpleado', blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    analisis_prestamo = models.ForeignKey(AnalisisPrestamo, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'analisis_prestamo_descuentos'

class AnalisisPrestamoPromedio(models.Model):
    id = models.IntegerField(primary_key=True)
    mes = models.IntegerField(blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)
    quincena = models.IntegerField(blank=True, null=True)
    total_ingreso = models.FloatField(blank=True, null=True)
    anticipo = models.FloatField(blank=True, null=True)
    sueldo_mensual = models.FloatField(blank=True, null=True)
    total_descuento = models.FloatField(blank=True, null=True)
    neto_recibir = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    analisis_prestamo = models.ForeignKey(AnalisisPrestamo, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'analisis_prestamo_promedio'

class Areas(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    activo = models.NullBooleanField()
    costo_hora = models.FloatField(blank=True, null=True)
    costo_hora_suplementaria = models.FloatField(blank=True, null=True)
    costo_hora_extraordinaria = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'areas'

class Asientos(models.Model):
    asiento_id = models.IntegerField(primary_key=True)
    codigo_asiento = models.IntegerField(blank=True, null=True)
    fecha_asiento = models.DateTimeField(blank=True, null=True)
    nro_consecutivo = models.IntegerField(blank=True, null=True)
    cuenta_contable = models.CharField(max_length=255, blank=True)
    debe_haber = models.FloatField(blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    libro_id = models.IntegerField(blank=True, null=True)
    explicacion_asiento = models.CharField(max_length=255, blank=True)
    referencia_por_cta = models.CharField(max_length=255, blank=True)
    nro_comprobante = models.IntegerField(blank=True, null=True)
    fuente_id = models.IntegerField(blank=True, null=True)
    nro_nit = models.IntegerField(blank=True, null=True)
    centro_costo_id = models.IntegerField(blank=True, null=True)
    modulo_origen = models.CharField(max_length=255, blank=True)
    dcto_origen_id = models.IntegerField(blank=True, null=True)
    nro_documento = models.IntegerField(blank=True, null=True)
    valor_base = models.FloatField(blank=True, null=True)
    dcto_id = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True)
    motivo_anulacion = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'asientos'

class AsignacionPermisos(models.Model):
    id_usuario = models.ForeignKey('Usuario', db_column='id_usuario', blank=True, null=True)
    opcion = models.ForeignKey('Opcion', db_column='opcion', blank=True, null=True)
    opcion_grupo = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'asignacion_permisos'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class Banco(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'banco'

class Bodega(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo_bodega = models.CharField(max_length=26, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    direccion1 = models.CharField(max_length=255, blank=True)
    direccion2 = models.CharField(max_length=255, blank=True)
    direccion3 = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=255, blank=True)
    predeterminado = models.CharField(max_length=255, blank=True)
    nro_productos = models.IntegerField(blank=True, null=True)
    activo = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo_bodega = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'bodega'

class CategoriaCliente(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=26, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    activo = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'categoria_cliente'

class CategoriaProducto(models.Model):
    categoria_id = models.IntegerField(primary_key=True)
    codigo_categoria = models.CharField(max_length=10, blank=True)
    descripcion_categoria = models.CharField(max_length=255, blank=True)
    predeterminado = models.IntegerField(blank=True, null=True)
    nro_productos = models.IntegerField(blank=True, null=True)
    imagen_categoria = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'categoria_producto'

class Chofer(models.Model):
    id = models.IntegerField()
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    ruc = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_ini = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'chofer'

class Ciudad(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ciudad'

class ClasificacionCuenta(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=-1, blank=True)
    class Meta:
        managed = False
        db_table = 'clasificacion_cuenta'

class Cliente(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    codigo_cliente = models.CharField(max_length=20, blank=True)
    nombre_cliente = models.CharField(max_length=255, blank=True)
    direccion1 = models.CharField(max_length=255, blank=True)
    direccion2 = models.CharField(max_length=255, blank=True)
    direccion3 = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=255, blank=True)
    pais = models.CharField(max_length=255, blank=True)
    codigo_postal = models.CharField(max_length=255, blank=True)
    telefono1 = models.CharField(max_length=255, blank=True)
    telefono2 = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    contacto = models.CharField(max_length=255, blank=True)
    email1 = models.CharField(max_length=255, blank=True)
    email2 = models.CharField(max_length=255, blank=True)
    categoria_cliente_id = models.IntegerField(blank=True, null=True)
    vendedor_id = models.IntegerField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    cliente_activo = models.NullBooleanField()
    registro_empresarial = models.CharField(max_length=255, blank=True)
    registro_tributario = models.CharField(max_length=255, blank=True)
    cuenta_cont_ventas = models.CharField(max_length=255, blank=True)
    giro_id = models.IntegerField(blank=True, null=True)
    creado = models.CharField(max_length=255, blank=True)
    maximo_credito = models.FloatField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    interes_anual = models.FloatField(blank=True, null=True)
    termino_id = models.IntegerField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    facturar_con = models.CharField(max_length=255, blank=True)
    campo1 = models.CharField(max_length=255, blank=True)
    campo2 = models.CharField(max_length=255, blank=True)
    campo3 = models.CharField(max_length=255, blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    aplica_reten_impto = models.NullBooleanField()
    reten_impto = models.FloatField(blank=True, null=True)
    aplica_reten_ica = models.NullBooleanField()
    reten_ica = models.FloatField(blank=True, null=True)
    aplica_reten_fuente = models.NullBooleanField()
    reten_fuente = models.FloatField(blank=True, null=True)
    aplica_2do_impto = models.NullBooleanField()
    segundo_impto = models.FloatField(blank=True, null=True)
    aplica_impto = models.NullBooleanField()
    impto = models.FloatField(blank=True, null=True)
    primer_apellido = models.CharField(max_length=255, blank=True)
    segundo_apellido = models.CharField(max_length=255, blank=True)
    primer_nombre = models.CharField(max_length=255, blank=True)
    segundo_nombre = models.CharField(max_length=255, blank=True)
    tipo_empresa = models.CharField(max_length=255, blank=True)
    impto_incluido = models.CharField(max_length=255, blank=True)
    monto_ult_transac = models.FloatField(blank=True, null=True)
    fecha_ult_transac = models.DateTimeField(blank=True, null=True)
    descri_ult_transac = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    ruc = models.CharField(max_length=30, blank=True)
    fecha_nacimiento = models.DateTimeField(blank=True, null=True)
    sexo = models.CharField(max_length=10, blank=True)
    clase_id = models.IntegerField(blank=True, null=True)
    validez = models.DateTimeField(blank=True, null=True)
    incluye_ice = models.NullBooleanField()
    convenio_hasta = models.DateTimeField(blank=True, null=True)
    consignacion = models.NullBooleanField()
    cuenta_anticipo = models.CharField(max_length=-1, blank=True)
    pasaporte = models.NullBooleanField()
    tipo_precio_id = models.IntegerField(blank=True, null=True)
    zona_id = models.IntegerField(blank=True, null=True)
    provincia_id = models.IntegerField(blank=True, null=True)
    ciudad_id = models.IntegerField(blank=True, null=True)
    banco_id = models.IntegerField(blank=True, null=True)
    plan_de_cuentas = models.ForeignKey('ContabilidadPlandecuentas', blank=True, null=True)
    cupo_credito = models.FloatField(blank=True, null=True)
    dias_credito = models.IntegerField(blank=True, null=True)
    tipo_cliente_id = models.IntegerField(blank=True, null=True)
    base = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'cliente'

class ComprasDetalle(models.Model):
    compras_detalle_id = models.IntegerField(primary_key=True)
    compra_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', blank=True, null=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    recibido = models.NullBooleanField()
    unidad = models.ForeignKey('Unidades', blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    impto_pciento = models.FloatField(blank=True, null=True)
    impto_monto = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    descto_monto = models.FloatField(blank=True, null=True)
    impto2_pciento = models.FloatField(blank=True, null=True)
    impto2_monto = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    tipo_cambio = models.CharField(max_length=255, blank=True)
    moneda = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    tipo_precio = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'compras_detalle'

class ComprasLocales(models.Model):
    id = models.IntegerField(primary_key=True)
    orden_compra = models.ForeignKey('OrdenCompra', blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', blank=True, null=True)
    nro_fact_proveedor = models.CharField(max_length=255, blank=True)
    terminos_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    recibida = models.CharField(max_length=255, blank=True)
    impto_en_precio = models.FloatField(blank=True, null=True)
    retefuente_pciento = models.FloatField(blank=True, null=True)
    retefuente_monto = models.FloatField(blank=True, null=True)
    reteiva_pciento = models.FloatField(blank=True, null=True)
    reteiva_monto = models.FloatField(blank=True, null=True)
    reteica_pciento = models.FloatField(blank=True, null=True)
    reteica_monto = models.FloatField(blank=True, null=True)
    monto_base = models.FloatField(blank=True, null=True)
    anulado = models.NullBooleanField()
    compra_cancelada = models.NullBooleanField()
    actualizado = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=255, blank=True)
    iva_pciento = models.FloatField(blank=True, null=True)
    subtotal_descuento = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'compras_locales'

class Conexion(models.Model):
    id_conexion = models.IntegerField(primary_key=True)
    string_de_conexion = models.CharField(max_length=250, blank=True)
    ruta_para_data = models.CharField(max_length=250, blank=True)
    computador_base = models.CharField(max_length=250, blank=True)
    servidor_de_datos = models.CharField(max_length=250, blank=True)
    ultima_actual_sp = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'conexion'

class ContabilidadAsiento(models.Model):
    asiento_id = models.IntegerField(primary_key=True)
    codigo_asiento = models.CharField(max_length=30)
    fecha = models.DateField()
    glosa = models.CharField(max_length=50)
    gasto_no_deducible = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'contabilidad_asiento'

class ContabilidadAsientodetalle(models.Model):
    detalle_id = models.IntegerField(primary_key=True)
    asiento = models.ForeignKey(ContabilidadAsiento)
    cuenta = models.ForeignKey('ContabilidadPlandecuentas')
    debe = models.DecimalField(max_digits=18, decimal_places=4)
    haber = models.DecimalField(max_digits=18, decimal_places=4)
    centro_costo = models.ForeignKey('ContabilidadCentrocosto')
    class Meta:
        managed = False
        db_table = 'contabilidad_asientodetalle'

class ContabilidadCentrocosto(models.Model):
    centro_id = models.IntegerField(primary_key=True)
    nombre_centro = models.CharField(max_length=50)
    padre = models.ForeignKey('self', blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'contabilidad_centrocosto'

class ContabilidadEjerciciocontable(models.Model):
    ejercicio_id = models.IntegerField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    abierto = models.BooleanField()
    cierremensual = models.BooleanField(db_column='cierreMensual') # Field name made lowercase.
    dia_cierre = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'contabilidad_ejerciciocontable'

class ContabilidadPlandecuentas(models.Model):
    plan_id = models.IntegerField(primary_key=True)
    grupo = models.ForeignKey('self', blank=True, null=True)
    nombre_plan = models.CharField(max_length=50)
    tipo_cuenta = models.ForeignKey('ContabilidadTipocuenta')
    codigo_plan = models.CharField(max_length=20)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'contabilidad_plandecuentas'

class ContabilidadTipocuenta(models.Model):
    tipo_id = models.IntegerField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField()
    codigo = models.CharField(max_length=10, blank=True)
    class Meta:
        managed = False
        db_table = 'contabilidad_tipocuenta'

class CotizacionProforma(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    detalle = models.TextField(blank=True)
    cantidad = models.IntegerField(blank=True, null=True)
    largo = models.CharField(max_length=250, blank=True)
    fondo = models.CharField(max_length=250, blank=True)
    alto = models.CharField(max_length=250, blank=True)
    madera = models.NullBooleanField()
    vidrio = models.NullBooleanField()
    hierro = models.NullBooleanField()
    marmol = models.NullBooleanField()
    enchape = models.NullBooleanField()
    enchape_detalle = models.CharField(max_length=250, blank=True)
    tallado = models.NullBooleanField()
    tallado_detalle = models.CharField(max_length=250, blank=True)
    tono = models.CharField(max_length=250, blank=True)
    retractil = models.NullBooleanField()
    panorama = models.NullBooleanField()
    corredizo = models.NullBooleanField()
    oleo = models.NullBooleanField()
    conchaperla = models.NullBooleanField()
    tela_almacen = models.NullBooleanField()
    tela_cliente = models.NullBooleanField()
    agarraderas = models.CharField(max_length=250, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    guia = models.IntegerField(blank=True, null=True)
    adicional = models.NullBooleanField()
    fechapedido = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=250, blank=True)
    estado = models.IntegerField(blank=True, null=True)
    tipo_mue = models.IntegerField(blank=True, null=True)
    doc = models.IntegerField(blank=True, null=True)
    mate = models.NullBooleanField()
    semimate = models.NullBooleanField()
    brillante = models.NullBooleanField()
    pulido = models.NullBooleanField()
    aluminio = models.NullBooleanField()
    acero = models.NullBooleanField()
    abrillantado = models.NullBooleanField()
    pintado = models.NullBooleanField()
    satinado = models.NullBooleanField()
    fechacotizacion = models.NullBooleanField()
    engrampe = models.NullBooleanField()
    impulso = models.NullBooleanField()
    poroabierto = models.NullBooleanField()
    ingreso = models.IntegerField(blank=True, null=True)
    cantaux = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    tiempo_respuesta = models.CharField(max_length=255, blank=True)
    fuera_ciudad = models.NullBooleanField()
    observacion = models.CharField(max_length=-1, blank=True)
    forma_pago = models.ForeignKey('FormaPago', blank=True, null=True)
    ambiente_id = models.IntegerField(blank=True, null=True)
    maqueteado_proforma = models.NullBooleanField()
    terminado_maqueteado_proforma = models.NullBooleanField()
    reunion_codigo = models.CharField(max_length=255, blank=True)
    reunion = models.ForeignKey('Reunion', blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    direccion_entrega = models.CharField(max_length=255, blank=True)
    iva = models.FloatField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    porcentaje_descuento = models.FloatField(blank=True, null=True)
    aprobada = models.NullBooleanField()
    anulada = models.NullBooleanField()
    tipo_lugar = models.ForeignKey('TipoLugar', blank=True, null=True)
    cotizacion_finalizada = models.NullBooleanField()
    puntos_venta = models.ForeignKey('PuntosVenta', blank=True, null=True)
    abreviatura_codigo = models.CharField(max_length=10, blank=True)
    hierro_proforma = models.NullBooleanField()
    porcentaje_iva = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'cotizacion_proforma'

class CotizacionProformaDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    cotizacion_proforma = models.ForeignKey(CotizacionProforma, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    observaciones = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    detalle = models.CharField(max_length=-1, blank=True)
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    reparacion = models.NullBooleanField()
    almacen = models.NullBooleanField()
    largo = models.CharField(max_length=255, blank=True)
    fondo = models.CharField(max_length=255, blank=True)
    alto = models.CharField(max_length=255, blank=True)
    producto_creado = models.ForeignKey('Producto', blank=True, null=True)
    nombre_producto_creado = models.CharField(max_length=255, blank=True)
    producto_general = models.ForeignKey('ProductoGeneral', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'cotizacion_proforma_detalle'

class Departamento(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=10, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'departamento'

class Devolucion(models.Model):
    devolucion_id = models.IntegerField(primary_key=True)
    nro_devolucion = models.CharField(max_length=10)
    proveedor = models.ForeignKey('Proveedor')
    supl_direccion1 = models.CharField(max_length=80)
    supl_direccion2 = models.CharField(max_length=80)
    supl_direccion3 = models.CharField(max_length=80)
    supl_direccion4 = models.CharField(max_length=80)
    registro_tributario = models.CharField(max_length=80)
    envia = models.CharField(max_length=80)
    enviar_direccion1 = models.CharField(max_length=80)
    enviar_direccion2 = models.CharField(max_length=80)
    enviar_direccion3 = models.CharField(max_length=80)
    enviar_direccion4 = models.CharField(max_length=80)
    nro_fact_proveedor = models.CharField(db_column='Nro_fact_proveedor', max_length=30) # Field name made lowercase.
    tipo_envio = models.CharField(max_length=80)
    vendedor = models.CharField(max_length=80)
    terminos_id = models.IntegerField()
    fecha = models.CharField(max_length=10)
    hora = models.CharField(max_length=16)
    fecha_vcmto = models.CharField(max_length=10)
    computador = models.TextField()
    moneda = models.IntegerField()
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    total = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    dscto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    dscto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    dscto_parcial_monto = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto2_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto2_monto = models.DecimalField(max_digits=18, decimal_places=4)
    miscelaneos = models.DecimalField(max_digits=18, decimal_places=4)
    miscelaneos_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    comentario = models.CharField(max_length=100)
    comentario_detalle = models.TextField(db_column='comentario_Detalle') # Field name made lowercase.
    tipo_cambio = models.DecimalField(max_digits=18, decimal_places=4)
    notas = models.TextField()
    asiento_id = models.IntegerField()
    docs_cp_id = models.IntegerField()
    kardex_id = models.IntegerField()
    impto_en_precio = models.IntegerField()
    actualizado = models.DateTimeField()
    pago = models.DecimalField(max_digits=18, decimal_places=4)
    devolucion_cancelada = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'devolucion'

class DevolucionDetalle(models.Model):
    detalle_id = models.IntegerField(primary_key=True)
    devolucion = models.ForeignKey(Devolucion)
    fecha = models.CharField(max_length=10)
    proveedor_id = models.IntegerField()
    producto = models.ForeignKey('Producto')
    bodega_id = models.IntegerField()
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    unidad = models.ForeignKey('Unidades')
    precio_compra = models.DecimalField(max_digits=18, decimal_places=4)
    impto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    descto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    descto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    impto2_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impto2_monto = models.DecimalField(max_digits=18, decimal_places=4)
    comentario = models.TextField()
    tipo_cambio = models.DecimalField(max_digits=18, decimal_places=4)
    moneda = models.IntegerField()
    nro_item = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'devolucion_Detalle'

class DevolucionClte(models.Model):
    devolucion_clte_id = models.IntegerField(primary_key=True)
    nro_devolucion_clte = models.CharField(max_length=10)
    cliente = models.ForeignKey(Cliente)
    clte_direccion1 = models.CharField(max_length=80)
    clte_direccion2 = models.CharField(max_length=80)
    clte_direccion3 = models.CharField(max_length=80)
    clte_direccion4 = models.CharField(max_length=80)
    registro_tributario = models.CharField(max_length=80)
    enviar = models.CharField(max_length=80)
    enviar_direccion1 = models.CharField(max_length=80)
    enviar_direccion2 = models.CharField(max_length=80)
    enviar_direccion3 = models.CharField(max_length=80)
    enviar_direccion4 = models.CharField(max_length=80)
    refer_cliente = models.CharField(max_length=20)
    tipo_envio = models.CharField(max_length=80)
    vendedor_id = models.IntegerField()
    termino = models.ForeignKey('TerminosPago')
    fecha_emision = models.CharField(max_length=10)
    hora = models.CharField(max_length=16)
    fecha_vcmto = models.CharField(max_length=10)
    computador = models.TextField()
    moneda = models.IntegerField()
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    total = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    dscto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    dscto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    dscto_parcial_monto = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto2_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto2_monto = models.DecimalField(max_digits=18, decimal_places=4)
    miscelaneos = models.DecimalField(max_digits=18, decimal_places=4)
    miscelaneos_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    comentario = models.TextField()
    comentario_detalle = models.TextField(db_column='comentario_Detalle') # Field name made lowercase.
    tipo_cambio = models.DecimalField(max_digits=18, decimal_places=4)
    notas = models.TextField()
    impto_en_precio = models.IntegerField()
    tipo_documento = models.CharField(max_length=40)
    retefuente_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    retefuente_monto = models.DecimalField(max_digits=18, decimal_places=4)
    reteiva_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    reteiva_monto = models.DecimalField(max_digits=18, decimal_places=4)
    reteica_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    reteica_monto = models.DecimalField(max_digits=18, decimal_places=4)
    monto_base = models.DecimalField(max_digits=18, decimal_places=4)
    nro_estimado = models.CharField(max_length=10)
    actualizado = models.DateTimeField()
    ncf = models.CharField(max_length=10)
    en_anexo = models.CharField(max_length=2)
    campo1 = models.CharField(max_length=30)
    campo2 = models.DecimalField(max_digits=18, decimal_places=4)
    campo3 = models.CharField(max_length=20)
    asiento_id = models.IntegerField()
    docs_cc_id = models.IntegerField()
    kardex_id = models.IntegerField()
    pagos = models.DecimalField(max_digits=18, decimal_places=4)
    anulada = models.IntegerField()
    causa_anulacion = models.TextField()
    class Meta:
        managed = False
        db_table = 'devolucion_clte'

class DevolucionClteDetalle(models.Model):
    detalle_id = models.IntegerField(primary_key=True)
    devolucion_clte = models.ForeignKey(DevolucionClte)
    fecha_emision = models.CharField(max_length=10)
    cliente_id = models.IntegerField()
    producto = models.ForeignKey('Producto')
    bodega_id = models.IntegerField()
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    recibido = models.DecimalField(max_digits=18, decimal_places=4)
    unidad_id = models.IntegerField()
    precio_devolucion_clte = models.DecimalField(max_digits=18, decimal_places=4)
    impto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    descto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    descto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    impto2_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impto2_monto = models.DecimalField(max_digits=18, decimal_places=4)
    comentario = models.TextField()
    tipo_cambio = models.DecimalField(max_digits=18, decimal_places=4)
    moneda = models.IntegerField()
    anulada = models.IntegerField()
    costo_producto = models.DecimalField(max_digits=18, decimal_places=4)
    class Meta:
        managed = False
        db_table = 'devolucion_clte_detalle'

class DiasFeriados(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'dias_feriados'

class DiasNoLaboradosRolEmpleado(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo_ausencia = models.ForeignKey('TipoAusencia', blank=True, null=True)
    rol_pago_detalle = models.ForeignKey('RolPagoDetalle', blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    anio = models.CharField(max_length=10, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    empleado = models.ForeignKey('EmpleadosEmpleado', blank=True, null=True)
    dias = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    fecha = models.CharField(max_length=255, blank=True)
    hora_inicio = models.CharField(max_length=255, blank=True)
    hora_fin = models.CharField(max_length=255, blank=True)
    descontar = models.NullBooleanField()
    cargar_vacaciones = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'dias_no_laborados_rol_empleado'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class DocsCp(models.Model):
    cp_id = models.IntegerField(primary_key=True)
    nro_dcmto = models.IntegerField(blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True)
    fecha_emision = models.DateTimeField(blank=True, null=True)
    descripcion_dcmto = models.CharField(max_length=255, blank=True)
    monto_dcmto = models.FloatField(blank=True, null=True)
    monto_parcial = models.FloatField(blank=True, null=True)
    moneda = models.CharField(max_length=255, blank=True)
    fecha_vcmto = models.DateTimeField(blank=True, null=True)
    nro_de_pagos = models.IntegerField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    balance_mon = models.FloatField(blank=True, null=True)
    nro_dcmto_pagado = models.IntegerField(blank=True, null=True)
    id_pagado = models.IntegerField(blank=True, null=True)
    modulo_origen = models.CharField(max_length=255, blank=True)
    id_origen = models.IntegerField(blank=True, null=True)
    modulo_destino = models.CharField(max_length=255, blank=True)
    id_destino = models.IntegerField(blank=True, null=True)
    nombre_pc = models.CharField(max_length=255, blank=True)
    hora = models.CharField(max_length=255, blank=True)
    monto_mora = models.FloatField(blank=True, null=True)
    interes_mora = models.FloatField(blank=True, null=True)
    dias_gracia_mora = models.IntegerField(blank=True, null=True)
    instrumento_pago = models.CharField(max_length=255, blank=True)
    tipo_cambio = models.CharField(max_length=255, blank=True)
    nro_dcmto_proveedor = models.IntegerField(blank=True, null=True)
    clase_registro = models.CharField(max_length=255, blank=True)
    estado_registro = models.CharField(max_length=255, blank=True)
    motivo_anulacion = models.CharField(max_length=255, blank=True)
    impuesto_1 = models.FloatField(blank=True, null=True)
    impuesto_2 = models.FloatField(blank=True, null=True)
    impto_incluido = models.FloatField(blank=True, null=True)
    observaciones = models.CharField(max_length=255, blank=True)
    grupo_pago = models.CharField(max_length=255, blank=True)
    termino_idlpv = models.CharField(max_length=255, blank=True)
    forma_pago = models.CharField(max_length=255, blank=True)
    nro_pago = models.IntegerField(blank=True, null=True)
    ref_pago = models.CharField(max_length=255, blank=True)
    fecha_hora = models.DateTimeField(blank=True, null=True)
    id_base = models.IntegerField(blank=True, null=True)
    id_cta_cte = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'docs_cp'

class EgresoOrdenEgreso(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=255, blank=True)
    orden_egreso_id = models.IntegerField(blank=True, null=True)
    terminos_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    recibida = models.CharField(max_length=255, blank=True)
    impto_en_precio = models.FloatField(blank=True, null=True)
    retefuente_pciento = models.FloatField(blank=True, null=True)
    retefuente_monto = models.FloatField(blank=True, null=True)
    reteiva_pciento = models.FloatField(blank=True, null=True)
    reteiva_monto = models.FloatField(blank=True, null=True)
    reteica_pciento = models.FloatField(blank=True, null=True)
    reteica_monto = models.FloatField(blank=True, null=True)
    monto_base = models.FloatField(blank=True, null=True)
    anulado = models.NullBooleanField()
    compra_cancelada = models.NullBooleanField()
    actualizado = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    concepto = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'egreso_orden_egreso'

class EgresosProyectadosEmpleado(models.Model):
    id = models.IntegerField(primary_key=True)
    empleado = models.ForeignKey('EmpleadosEmpleado', blank=True, null=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey('TipoIngresoEgresoEmpleado', blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    valor_mensual = models.FloatField(blank=True, null=True)
    valor_diario = models.FloatField(blank=True, null=True)
    deducible = models.NullBooleanField()
    aportaciones = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'egresos_proyectados_empleado'

class EgresosRolEmpleado(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey('TipoIngresoEgresoEmpleado', blank=True, null=True)
    rol_pago_detalle = models.ForeignKey('RolPagoDetalle', blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    anio = models.CharField(max_length=10, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    empleado = models.ForeignKey('EmpleadosEmpleado', blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    memo = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    plantilla_rrhh = models.ForeignKey('PlantillaRrhh', blank=True, null=True)
    egresos_proyectados = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'egresos_rol_empleado'

class EmpleadosChofer(models.Model):
    chofer_id = models.IntegerField(primary_key=True)
    codigo_chofer = models.CharField(max_length=10)
    empleado = models.ForeignKey('EmpleadosEmpleado', blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.NullBooleanField()
    nombre = models.CharField(max_length=255, blank=True)
    ruc = models.CharField(max_length=20, blank=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    fecha_ini = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'empleados_chofer'

class EmpleadosEmpleado(models.Model):
    empleado_id = models.IntegerField(primary_key=True)
    codigo_empleado = models.CharField(max_length=10)
    cedula_empleado = models.CharField(max_length=10)
    nombre_empleado = models.CharField(max_length=50)
    tipo_empleado = models.ForeignKey('EmpleadosTipoempleado', blank=True, null=True)
    direccion = models.CharField(max_length=80, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField()
    fecha_fin = models.DateField(blank=True, null=True)
    fecha_ini = models.DateField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=20, blank=True)
    estado_civil = models.ForeignKey('EstadoCivil', blank=True, null=True)
    tipo_documento = models.CharField(max_length=-1, blank=True)
    pais_id = models.IntegerField(blank=True, null=True)
    cargas_familiares = models.IntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True)
    provincia = models.ForeignKey('Provincia', blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, blank=True, null=True)
    imagen = models.CharField(max_length=250, blank=True)
    gastos_vivienda = models.FloatField(blank=True, null=True)
    gastos_educacion = models.FloatField(blank=True, null=True)
    gastos_salud = models.FloatField(blank=True, null=True)
    gastos_alimentacion = models.FloatField(blank=True, null=True)
    gastos_vestimenta = models.FloatField(blank=True, null=True)
    rebajada_discapacidad = models.FloatField(blank=True, null=True)
    rebajas_tercera_edad = models.FloatField(blank=True, null=True)
    situacion_previsional = models.CharField(max_length=250, blank=True)
    iess = models.CharField(max_length=250, blank=True)
    numero_afiliacion = models.CharField(max_length=50, blank=True)
    sociedad_medica = models.CharField(max_length=250, blank=True)
    numero_sociedad_medica = models.CharField(max_length=100, blank=True)
    impuesto_renta_cargo_empleador = models.NullBooleanField()
    forma_pago_cliente_id = models.IntegerField(blank=True, null=True)
    banco = models.ForeignKey(Banco, blank=True, null=True)
    tipo_cuenta_id = models.IntegerField(blank=True, null=True)
    cuenta_contable = models.CharField(max_length=100, blank=True)
    pago_decimo_tercero_mensual = models.NullBooleanField()
    aportacion_conyugal = models.NullBooleanField()
    pago_decimo_cuarto_mensual = models.NullBooleanField()
    pago_fondo_reserva = models.NullBooleanField()
    horas_trabajo_semanal = models.CharField(max_length=-1, blank=True)
    relacion_laboral_id = models.IntegerField(blank=True, null=True)
    tipo_remuneracion_id = models.IntegerField(blank=True, null=True)
    compensacion = models.FloatField(blank=True, null=True)
    sueldo = models.FloatField(blank=True, null=True)
    puntos_venta = models.ForeignKey('PuntosVenta', blank=True, null=True)
    fecha_ini_reconocida = models.DateField(blank=True, null=True)
    apellido = models.CharField(max_length=255, blank=True)
    forma_pago_empleado = models.ForeignKey('FormaPagoEmpleado', blank=True, null=True)
    departamento = models.ForeignKey(Departamento, blank=True, null=True)
    tipo_contrato = models.ForeignKey('TipoContrato', blank=True, null=True)
    discapacidad = models.NullBooleanField()
    grupo_pago = models.ForeignKey('GrupoPago', blank=True, null=True)
    acumular_decimo_tercero = models.NullBooleanField()
    extension_conyugal = models.NullBooleanField()
    pago_fondos_reserva = models.ForeignKey('PagoFondosReserva', blank=True, null=True)
    nota = models.CharField(max_length=-1, blank=True)
    aviso_entrada = models.NullBooleanField()
    contrato_trabajo = models.NullBooleanField()
    acta_juramentada = models.NullBooleanField()
    certificado_trabajo = models.NullBooleanField()
    nombre_conyugue = models.CharField(max_length=500, blank=True)
    acumular_fondo_reserva = models.NullBooleanField()
    acumular_decimo_cuarto = models.NullBooleanField()
    acumular_iess_asumido = models.NullBooleanField()
    asumir_impuesto_renta = models.NullBooleanField()
    codigo_reloj = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'empleados_empleado'

class EmpleadosTipoempleado(models.Model):
    tipo_empleado_id = models.IntegerField(primary_key=True)
    cargo_empleado = models.CharField(max_length=250)
    descripcion_tipo = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField()
    departamento = models.ForeignKey(Departamento, blank=True, null=True)
    sueldo = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'empleados_tipoempleado'

class EmpleadosVehiculo(models.Model):
    vehiculo_id = models.IntegerField(primary_key=True)
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=30, blank=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.NullBooleanField()
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_ini = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'empleados_vehiculo'

class EmpleadosVendedor(models.Model):
    vendedor_id = models.IntegerField(primary_key=True)
    codigo_vendedor = models.CharField(max_length=10)
    empleado = models.ForeignKey(EmpleadosEmpleado)
    comision = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'empleados_vendedor'

class Empresa(models.Model):
    empresa_id = models.IntegerField(primary_key=True)
    nombre_empresa = models.CharField(max_length=250, blank=True)
    base_de_datos = models.CharField(max_length=250, blank=True)
    condicion = models.CharField(max_length=255, blank=True)
    icono_asociado = models.CharField(max_length=255, blank=True)
    folder_empresa = models.CharField(max_length=255, blank=True)
    registro_tributario_empresa = models.CharField(max_length=255, blank=True)
    direccion1 = models.CharField(max_length=255, blank=True)
    direccion2 = models.CharField(max_length=255, blank=True)
    direccion3 = models.CharField(max_length=255, blank=True)
    telefono1 = models.CharField(max_length=255, blank=True)
    celular = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    correo_electronico = models.CharField(max_length=255, blank=True)
    sitio_web = models.CharField(max_length=255, blank=True)
    registro_empresarial = models.CharField(max_length=255, blank=True)
    barrio_distrito = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=255, blank=True)
    codigo_postal = models.CharField(max_length=255, blank=True)
    pais = models.CharField(max_length=255, blank=True)
    logo = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'empresa'

class EstadoCivil(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'estado_civil'

class EstadosPro(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'estados_pro'

class Factura(models.Model):
    factura_id = models.IntegerField(primary_key=True)
    nro_factura = models.CharField(max_length=10)
    tipo_factura = models.IntegerField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente)
    clte_direccion1 = models.CharField(max_length=80)
    clte_direccion2 = models.CharField(max_length=80)
    clte_direccion3 = models.CharField(max_length=80)
    clte_direccion4 = models.CharField(max_length=80)
    registro_tributario = models.CharField(max_length=80)
    enviar = models.CharField(max_length=80)
    enviar_direccion1 = models.CharField(max_length=80)
    enviar_direccion2 = models.CharField(max_length=80)
    enviar_direccion3 = models.CharField(max_length=80)
    enviar_direccion4 = models.CharField(max_length=80)
    refer_cliente = models.CharField(max_length=20)
    tipo_envio = models.CharField(max_length=80)
    vendedor = models.ForeignKey('Vendedor')
    termino = models.ForeignKey('TerminosPago', blank=True, null=True)
    fecha_emision = models.CharField(max_length=10, blank=True)
    hora = models.CharField(max_length=16)
    fecha_vcmto = models.CharField(max_length=10)
    computador = models.TextField()
    moneda = models.IntegerField(blank=True, null=True)
    subtotal = models.FloatField()
    total = models.FloatField()
    iva_pciento = models.FloatField(blank=True, null=True)
    iva_monto = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    dscto_parcial_monto = models.FloatField(blank=True, null=True)
    impuesto2_pciento = models.FloatField(blank=True, null=True)
    impuesto2_monto = models.FloatField(blank=True, null=True)
    miscelaneos = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    miscelaneos_pciento = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    observacion = models.TextField(blank=True)
    comentario_detalle = models.TextField(db_column='comentario_Detalle', blank=True) # Field name made lowercase.
    tipo_cambio = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    notas = models.TextField()
    impto_en_precio = models.IntegerField(blank=True, null=True)
    tipo_documento = models.CharField(max_length=40, blank=True)
    retefuente_pciento = models.FloatField(blank=True, null=True)
    retefuente_monto = models.FloatField(blank=True, null=True)
    reteiva_pciento = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    reteiva_monto = models.FloatField(blank=True, null=True)
    reteica_pciento = models.FloatField(blank=True, null=True)
    reteica_monto = models.FloatField(blank=True, null=True)
    monto_base = models.FloatField(blank=True, null=True)
    nro_estimado = models.CharField(max_length=10, blank=True)
    actualizado = models.DateTimeField(blank=True, null=True)
    ncf = models.CharField(max_length=50, blank=True)
    en_anexo = models.CharField(max_length=2, blank=True)
    campo1 = models.CharField(max_length=30, blank=True)
    campo2 = models.FloatField(blank=True, null=True)
    campo3 = models.CharField(max_length=20, blank=True)
    asiento_id = models.IntegerField(blank=True, null=True)
    docs_cc_id = models.IntegerField(blank=True, null=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    pagos = models.FloatField(blank=True, null=True)
    anulada = models.IntegerField(blank=True, null=True)
    causa_anulacion = models.TextField(blank=True)
    fecha = models.DateField(blank=True, null=True)
    puntos_venta = models.ForeignKey('PuntosVenta', blank=True, null=True)
    ruc = models.CharField(max_length=20, blank=True)
    bodega_id = models.IntegerField(blank=True, null=True)
    plazo = models.IntegerField(blank=True, null=True)
    proforma_codigo = models.CharField(max_length=50, blank=True)
    razon_social = models.ForeignKey('RazonSocial', blank=True, null=True)
    proforma_factura_codigo = models.CharField(max_length=50, blank=True)
    proforma_factura = models.ForeignKey('ProformaFactura', blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    proforma = models.ForeignKey('Proforma', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'factura'

class FacturaDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    factura = models.ForeignKey(Factura, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    observaciones = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    detalle = models.CharField(max_length=-1, blank=True)
    codigo_produccion = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'factura_detalle'

class FacturacionGuiadetalle(models.Model):
    detalle_id = models.IntegerField(primary_key=True)
    guia_id = models.ForeignKey('FacturacionGuiaremision')
    producto_id = models.ForeignKey('Producto')
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    class Meta:
        managed = False
        db_table = 'facturacion_guiadetalle'

class FacturacionGuiaremision(models.Model):
    guia_id = models.IntegerField(primary_key=True)
    nro_guia = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_documento = models.CharField(max_length=20)
    fecha_emision = models.DateField()
    nro_autorizacion = models.CharField(max_length=30, blank=True)
    nro_comprobante = models.CharField(max_length=30, blank=True)
    motivo_traslado = models.CharField(max_length=80, blank=True)
    partida = models.CharField(max_length=256)
    destino = models.CharField(max_length=256)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    chofer = models.ForeignKey(EmpleadosChofer, blank=True, null=True)
    vehiculo = models.ForeignKey(EmpleadosVehiculo, blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField()
    tipo_guia = models.ForeignKey('TipoGuia', blank=True, null=True)
    aprobada = models.NullBooleanField()
    ingreso = models.NullBooleanField()
    egreso = models.NullBooleanField()
    puntos_venta = models.ForeignKey('PuntosVenta', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'facturacion_guiaremision'

class FormaPago(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'forma_pago'

class FormaPagoClie(models.Model):
    forma_pago_id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=4)
    descripcion = models.CharField(max_length=50)
    tipo_cuenta = models.IntegerField()
    predeterminado = models.IntegerField()
    cta_contable = models.CharField(max_length=20)
    enlaza_id = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'forma_pago_clie'

class FormaPagoEmpleado(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'forma_pago_empleado'

class GrupoPago(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'grupo_pago'

class ImagenesCotizacionProforma(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.TextField(blank=True)
    cotizacion_proforma_detalle = models.ForeignKey(CotizacionProformaDetalle, blank=True, null=True)
    imagen = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'imagenes_cotizacion_proforma'

class ImagenesKardex(models.Model):
    imagen_id = models.IntegerField(primary_key=True)
    nro_documento = models.CharField(max_length=10)
    imagen_dcto = models.TextField()
    class Meta:
        managed = False
        db_table = 'imagenes_kardex'

class ImagenesProducto(models.Model):
    imagen_id = models.IntegerField(primary_key=True)
    producto_id = models.IntegerField()
    imagen_producto = models.TextField()
    class Meta:
        managed = False
        db_table = 'imagenes_producto'

class ImagenesPv(models.Model):
    imagen_idpv = models.IntegerField(primary_key=True)
    proveedor_id = models.IntegerField()
    imagen_proveedor = models.TextField()
    class Meta:
        managed = False
        db_table = 'imagenes_pv'

class ImagenesReunion(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=250, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    reunion = models.ForeignKey('Reunion', blank=True, null=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'imagenes_reunion'

class ImagenesReunionDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=250, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    imagenes_reunion = models.ForeignKey(ImagenesReunion, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'imagenes_reunion_detalle'

class Impuesto(models.Model):
    impuesto_id = models.IntegerField(primary_key=True)
    abreviatura = models.CharField(max_length=255, blank=True)
    descripcion_impto = models.CharField(max_length=255, blank=True)
    valor_impto = models.FloatField(blank=True, null=True)
    cta_cont_ventas = models.CharField(max_length=255, blank=True)
    cta_cont_compras = models.CharField(max_length=255, blank=True)
    predeterminado = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'impuesto'

class IngresoOrdenIngreso(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=255, blank=True)
    orden_ingreso = models.ForeignKey('OrdenIngreso', blank=True, null=True)
    terminos_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    recibida = models.CharField(max_length=255, blank=True)
    impto_en_precio = models.FloatField(blank=True, null=True)
    retefuente_pciento = models.FloatField(blank=True, null=True)
    retefuente_monto = models.FloatField(blank=True, null=True)
    reteiva_pciento = models.FloatField(blank=True, null=True)
    reteiva_monto = models.FloatField(blank=True, null=True)
    reteica_pciento = models.FloatField(blank=True, null=True)
    reteica_monto = models.FloatField(blank=True, null=True)
    monto_base = models.FloatField(blank=True, null=True)
    anulado = models.NullBooleanField()
    compra_cancelada = models.NullBooleanField()
    actualizado = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ingreso_orden_ingreso'

class IngresosProyectadosEmpleado(models.Model):
    id = models.IntegerField(primary_key=True)
    empleado = models.ForeignKey(EmpleadosEmpleado, blank=True, null=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey('TipoIngresoEgresoEmpleado', blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    valor_mensual = models.FloatField(blank=True, null=True)
    valor_diario = models.FloatField(blank=True, null=True)
    deducible = models.NullBooleanField()
    aportaciones = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ingresos_proyectados_empleado'

class IngresosRolEmpleado(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey('TipoIngresoEgresoEmpleado', blank=True, null=True)
    rol_pago_detalle = models.ForeignKey('RolPagoDetalle', blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    deducible = models.NullBooleanField()
    aportaciones = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    anio = models.CharField(max_length=10, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    empleado = models.ForeignKey(EmpleadosEmpleado, blank=True, null=True)
    horas = models.FloatField(blank=True, null=True)
    plantilla_rrhh = models.ForeignKey('PlantillaRrhh', blank=True, null=True)
    fecha = models.CharField(max_length=255, blank=True)
    hora_inicio = models.CharField(max_length=255, blank=True)
    hora_fin = models.CharField(max_length=255, blank=True)
    pagar = models.NullBooleanField()
    valor_diario = models.FloatField(blank=True, null=True)
    ingresos_proyectados = models.NullBooleanField()
    valor_mensual = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ingresos_rol_empleado'

class InvFisico(models.Model):
    inv_fisico_id = models.IntegerField(primary_key=True)
    fecha_inv_fisico = models.CharField(max_length=10)
    descrip_inv_fisico = models.CharField(db_column='Descrip_inv_fisico', max_length=200) # Field name made lowercase.
    almacen_id = models.IntegerField()
    prod_cont_almacen = models.DecimalField(max_digits=18, decimal_places=4)
    total_prod_almacen = models.DecimalField(db_column='Total_prod_almacen', max_digits=18, decimal_places=4) # Field name made lowercase.
    campo1 = models.CharField(max_length=100)
    campo2 = models.DecimalField(max_digits=18, decimal_places=4)
    campo3 = models.TextField()
    class Meta:
        managed = False
        db_table = 'inv_fisico'

class InvFisicoDetalle(models.Model):
    detalle_inv_fis_id = models.IntegerField(primary_key=True)
    producto_id = models.CharField(max_length=30)
    bodega_id = models.IntegerField()
    unidades_contadas = models.DecimalField(max_digits=18, decimal_places=4)
    campo1 = models.CharField(max_length=100)
    campo2 = models.DecimalField(max_digits=18, decimal_places=4)
    campo3 = models.TextField()
    class Meta:
        managed = False
        db_table = 'inv_fisico_detalle'

class Kardex(models.Model):
    kardex_id = models.IntegerField(primary_key=True)
    nro_documento = models.CharField(max_length=250, blank=True)
    empresa_tipo = models.CharField(max_length=250, blank=True)
    empresa_id = models.IntegerField(blank=True, null=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    cantidad = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    tipo = models.IntegerField(blank=True, null=True)
    fecha_ingreso = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    cant_disponible = models.IntegerField(blank=True, null=True)
    cant_dispoxbodega = models.IntegerField(blank=True, null=True)
    modificable = models.NullBooleanField()
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    modulo = models.CharField(max_length=250, blank=True)
    documento_id = models.IntegerField(blank=True, null=True)
    nro_doc_soporte = models.IntegerField(blank=True, null=True)
    un_doc_soporte = models.CharField(max_length=250, blank=True)
    hora = models.CharField(max_length=250, blank=True)
    costo_old = models.FloatField(blank=True, null=True)
    lote_id = models.IntegerField(blank=True, null=True)
    ingreso = models.CharField(max_length=250, blank=True)
    nro_item = models.IntegerField(blank=True, null=True)
    fecha_hora = models.DateTimeField(blank=True, null=True)
    cant_disponible_x = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_egreso = models.DateTimeField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'kardex'

class Kits(models.Model):
    padre = models.ForeignKey('Producto', blank=True, null=True)
    hijo = models.ForeignKey('Producto', blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    areas = models.ForeignKey(Areas, blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'kits'

class Linea(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'linea'

class LiquidacionComisiones(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    subtotal = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    retencion_fuente = models.FloatField(blank=True, null=True)
    retencion_iva = models.FloatField(blank=True, null=True)
    neto_pagar = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    valor_cancelado_sin_iva = models.FloatField(blank=True, null=True)
    valor_cancelado = models.FloatField(blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    total_retenciones = models.FloatField(blank=True, null=True)
    adelanto = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'liquidacion_comisiones'

class LiquidacionComisionesDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    proforma = models.ForeignKey('Proforma', blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    proforma_codigo = models.CharField(max_length=255, blank=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    detalle = models.TextField(blank=True)
    subtotal = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    valor_cancelado = models.FloatField(blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    valor_cancelado_sin_iva = models.FloatField(blank=True, null=True)
    porcentaje_comision = models.FloatField(blank=True, null=True)
    total_comision = models.FloatField(blank=True, null=True)
    liquidacion_comisiones = models.ForeignKey(LiquidacionComisiones, blank=True, null=True)
    proforma_factura = models.ForeignKey('ProformaFactura', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'liquidacion_comisiones_detalle'

class ListaCliente(models.Model):
    lista_cliente_id = models.IntegerField(primary_key=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    precio = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lista_cliente'

class ListaPrecio(models.Model):
    lista_suplidor_id = models.IntegerField(primary_key=True)
    proveedor = models.ForeignKey('Proveedor', blank=True, null=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    precio_de_compra_1 = models.FloatField(blank=True, null=True)
    precio_en_dolar_1 = models.FloatField(blank=True, null=True)
    rango_inicial_1 = models.FloatField(blank=True, null=True)
    rango_final_1 = models.FloatField(blank=True, null=True)
    precio_de_compra_2 = models.FloatField(blank=True, null=True)
    precio_en_dolar_2 = models.FloatField(blank=True, null=True)
    rango_inicial_2 = models.FloatField(blank=True, null=True)
    rango_final_2 = models.FloatField(blank=True, null=True)
    actualizado = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lista_precio'

class Lote(models.Model):
    lote_id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    nro_lote = models.CharField(max_length=250, blank=True)
    descripcion_lote = models.CharField(max_length=250, blank=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    fecha_ingreso = models.DateTimeField(blank=True, null=True)
    fecha_expiracion = models.DateTimeField(blank=True, null=True)
    ubicacion = models.CharField(max_length=250, blank=True)
    cantidad = models.FloatField(blank=True, null=True)
    comentario_lote = models.CharField(max_length=250, blank=True)
    nro_documento = models.IntegerField(blank=True, null=True)
    disponible = models.FloatField(blank=True, null=True)
    agotado_en = models.DateTimeField(blank=True, null=True)
    nro_item = models.IntegerField(blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lote'

class Mensajes(models.Model):
    mensajes_id = models.IntegerField()
    codigo = models.CharField(max_length=50, blank=True)
    mensaje = models.CharField(max_length=255, blank=True)
    activo = models.NullBooleanField()
    cuenta_contable = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'mensajes'

class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    cod_parent = models.ForeignKey('self', db_column='cod_parent', blank=True, null=True)
    nom_option = models.CharField(max_length=40)
    num_order = models.IntegerField(blank=True, null=True)
    txt_url = models.TextField(blank=True)
    txt_description = models.TextField(blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'menu'

class MenuGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup, blank=True, null=True)
    menu = models.ForeignKey(Menu, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sts_show = models.NullBooleanField()
    sts_modify = models.NullBooleanField()
    sts_delete = models.NullBooleanField()
    sts_new = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'menu_group'

class NotaCredito(models.Model):
    id = models.IntegerField(primary_key=True)
    nro_nota_credito = models.CharField(max_length=10, blank=True)
    tipo_factura = models.IntegerField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    clte_direccion1 = models.CharField(max_length=80, blank=True)
    clte_direccion2 = models.CharField(max_length=80, blank=True)
    clte_direccion3 = models.CharField(max_length=80, blank=True)
    clte_direccion4 = models.CharField(max_length=80, blank=True)
    registro_tributario = models.CharField(max_length=80, blank=True)
    enviar = models.CharField(max_length=80, blank=True)
    enviar_direccion1 = models.CharField(max_length=80, blank=True)
    enviar_direccion2 = models.CharField(max_length=80, blank=True)
    enviar_direccion3 = models.CharField(max_length=80, blank=True)
    enviar_direccion4 = models.CharField(max_length=80, blank=True)
    refer_cliente = models.CharField(max_length=20, blank=True)
    tipo_envio = models.CharField(max_length=80, blank=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    termino_id = models.IntegerField(blank=True, null=True)
    hora = models.CharField(max_length=16, blank=True)
    fecha_vcmto = models.CharField(max_length=10, blank=True)
    computador = models.TextField(blank=True)
    moneda = models.IntegerField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    iva_pciento = models.FloatField(blank=True, null=True)
    iva_monto = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    dscto_parcial_monto = models.FloatField(blank=True, null=True)
    impuesto2_pciento = models.FloatField(blank=True, null=True)
    impuesto2_monto = models.FloatField(blank=True, null=True)
    miscelaneos = models.FloatField(blank=True, null=True)
    miscelaneos_pciento = models.FloatField(blank=True, null=True)
    observacion = models.TextField(blank=True)
    comentario_detalle = models.TextField(db_column='comentario_Detalle', blank=True) # Field name made lowercase.
    tipo_cambio = models.FloatField(blank=True, null=True)
    notas = models.TextField(blank=True)
    impto_en_precio = models.IntegerField(blank=True, null=True)
    tipo_documento = models.CharField(max_length=40, blank=True)
    retefuente_pciento = models.FloatField(blank=True, null=True)
    retefuente_monto = models.FloatField(blank=True, null=True)
    reteiva_pciento = models.FloatField(blank=True, null=True)
    reteiva_monto = models.FloatField(blank=True, null=True)
    reteica_pciento = models.FloatField(blank=True, null=True)
    reteica_monto = models.FloatField(blank=True, null=True)
    monto_base = models.FloatField(blank=True, null=True)
    nro_estimado = models.CharField(max_length=10, blank=True)
    actualizado = models.DateTimeField(blank=True, null=True)
    ncf = models.CharField(max_length=50, blank=True)
    en_anexo = models.CharField(max_length=2, blank=True)
    campo1 = models.CharField(max_length=30, blank=True)
    campo2 = models.FloatField(blank=True, null=True)
    campo3 = models.CharField(max_length=20, blank=True)
    asiento_id = models.IntegerField(blank=True, null=True)
    docs_cc_id = models.IntegerField(blank=True, null=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    pagos = models.FloatField(blank=True, null=True)
    anulada = models.IntegerField(blank=True, null=True)
    causa_anulacion = models.TextField(blank=True)
    fecha = models.DateField(blank=True, null=True)
    puntos_venta = models.ForeignKey('PuntosVenta', blank=True, null=True)
    ruc = models.CharField(max_length=20, blank=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    plazo = models.IntegerField(blank=True, null=True)
    proforma_codigo = models.CharField(max_length=50, blank=True)
    razon_social = models.ForeignKey('RazonSocial', blank=True, null=True)
    factura_codigo = models.CharField(max_length=20, blank=True)
    class Meta:
        managed = False
        db_table = 'nota_credito'

class NotaCreditoDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    nota_credito = models.ForeignKey(NotaCredito, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    observaciones = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    detalle = models.CharField(max_length=-1, blank=True)
    codigo_produccion = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'nota_credito_detalle'

class Opcion(models.Model):
    opcion = models.IntegerField(primary_key=True)
    descrip = models.CharField(max_length=250, blank=True)
    accion = models.CharField(max_length=250, blank=True)
    tab = models.CharField(max_length=250, blank=True)
    icono = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'opcion'

class OrdenservicioOrdenservicio(models.Model):
    orden_id = models.IntegerField(primary_key=True)
    nro_orden = models.CharField(max_length=30, blank=True)
    ciudad = models.CharField(max_length=-1, blank=True)
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    direccion = models.CharField(max_length=-1, blank=True)
    objeto_orden = models.CharField(max_length=-1, blank=True)
    hora_salida_fabrica = models.TimeField(blank=True, null=True)
    hora_llegada_obra = models.TimeField(blank=True, null=True)
    hora_salida_obra = models.TimeField(blank=True, null=True)
    hora_llegada_fabrica = models.TimeField(blank=True, null=True)
    novedades = models.CharField(max_length=-1, blank=True)
    pedido = models.ForeignKey('Pedido', blank=True, null=True)
    orden_produccion = models.ForeignKey('OrdenProduccion', blank=True, null=True)
    guia_remision = models.ForeignKey(FacturacionGuiaremision, blank=True, null=True)
    reporte_visita = models.CharField(max_length=-1, blank=True)
    trabajos_realizar = models.CharField(max_length=-1, blank=True)
    observaciones = models.CharField(max_length=-1, blank=True)
    maestro_encargado = models.ForeignKey(EmpleadosEmpleado, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    codigo_pedido = models.CharField(max_length=250, blank=True)
    codigo_orden_produccion = models.CharField(max_length=255, blank=True)
    maestro = models.CharField(max_length=-1, blank=True)
    class Meta:
        managed = False
        db_table = 'ordenServicio_ordenservicio'

class OrdenservicioOrdenservicioMaestrosResponsables(models.Model):
    id = models.IntegerField(primary_key=True)
    ordenservicio = models.ForeignKey(OrdenservicioOrdenservicio)
    empleado = models.ForeignKey(EmpleadosEmpleado)
    class Meta:
        managed = False
        db_table = 'ordenServicio_ordenservicio_maestros_responsables'

class OrdenCompra(models.Model):
    compra_id = models.IntegerField(primary_key=True)
    nro_compra = models.IntegerField(blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', blank=True, null=True)
    supl_direccion1 = models.CharField(max_length=255, blank=True)
    supl_direccion2 = models.CharField(max_length=255, blank=True)
    supl_direccion3 = models.CharField(max_length=255, blank=True)
    supl_direccion4 = models.CharField(max_length=255, blank=True)
    registro_tributario = models.CharField(max_length=255, blank=True)
    enviar = models.NullBooleanField()
    enviar_direccion1 = models.CharField(max_length=255, blank=True)
    enviar_direccion2 = models.CharField(max_length=255, blank=True)
    enviar_direccion3 = models.CharField(max_length=255, blank=True)
    enviar_direccion4 = models.CharField(max_length=255, blank=True)
    nro_fact_proveedor = models.CharField(max_length=255, blank=True)
    tipo_envio = models.CharField(max_length=255, blank=True)
    vendedor = models.CharField(max_length=255, blank=True)
    terminos_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    hora = models.DateTimeField(blank=True, null=True)
    fecha_vcmto = models.DateTimeField(blank=True, null=True)
    pagos = models.CharField(max_length=255, blank=True)
    computador = models.CharField(max_length=255, blank=True)
    moneda = models.CharField(max_length=255, blank=True)
    subtotal = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    impuesto_pciento = models.FloatField(blank=True, null=True)
    impuesto_monto = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    dscto_parcial_monto = models.FloatField(blank=True, null=True)
    impuesto2_pciento = models.FloatField(blank=True, null=True)
    impuesto2_monto = models.FloatField(blank=True, null=True)
    miscelaneos = models.CharField(max_length=255, blank=True)
    miscelaneos_pciento = models.CharField(max_length=255, blank=True)
    comentario = models.CharField(max_length=255, blank=True)
    comentario_detalle = models.CharField(max_length=255, blank=True)
    tipo_cambio = models.CharField(max_length=255, blank=True)
    notas = models.CharField(max_length=255, blank=True)
    asiento_id = models.IntegerField(blank=True, null=True)
    docs_cp_id = models.IntegerField(blank=True, null=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    recibida = models.CharField(max_length=255, blank=True)
    impto_en_precio = models.FloatField(blank=True, null=True)
    tipo_compra = models.CharField(max_length=255, blank=True)
    retefuente_pciento = models.FloatField(blank=True, null=True)
    retefuente_monto = models.FloatField(blank=True, null=True)
    reteiva_pciento = models.FloatField(blank=True, null=True)
    reteiva_monto = models.FloatField(blank=True, null=True)
    reteica_pciento = models.FloatField(blank=True, null=True)
    reteica_monto = models.FloatField(blank=True, null=True)
    monto_base = models.FloatField(blank=True, null=True)
    tipo_registracion = models.CharField(max_length=255, blank=True)
    anulado = models.NullBooleanField()
    compra_cancelada = models.NullBooleanField()
    actualizado = models.NullBooleanField()
    ncf = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    aprobada = models.NullBooleanField()
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    facturada = models.NullBooleanField()
    subtotal_descuento = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'orden_compra'

class OrdenEgreso(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=255, blank=True)
    proveedor = models.ForeignKey('Proveedor', blank=True, null=True)
    supl_direccion1 = models.CharField(max_length=255, blank=True)
    supl_direccion2 = models.CharField(max_length=255, blank=True)
    supl_direccion3 = models.CharField(max_length=255, blank=True)
    supl_direccion4 = models.CharField(max_length=255, blank=True)
    registro_tributario = models.CharField(max_length=255, blank=True)
    enviar = models.NullBooleanField()
    enviar_direccion1 = models.CharField(max_length=255, blank=True)
    enviar_direccion2 = models.CharField(max_length=255, blank=True)
    enviar_direccion3 = models.CharField(max_length=255, blank=True)
    enviar_direccion4 = models.CharField(max_length=255, blank=True)
    nro_fact_proveedor = models.CharField(max_length=255, blank=True)
    tipo_envio = models.CharField(max_length=255, blank=True)
    vendedor = models.CharField(max_length=255, blank=True)
    terminos_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    hora = models.DateTimeField(blank=True, null=True)
    fecha_vcmto = models.DateTimeField(blank=True, null=True)
    pagos = models.CharField(max_length=255, blank=True)
    computador = models.CharField(max_length=255, blank=True)
    moneda = models.CharField(max_length=255, blank=True)
    subtotal = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    impuesto_pciento = models.FloatField(blank=True, null=True)
    impuesto_monto = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    dscto_parcial_monto = models.FloatField(blank=True, null=True)
    impuesto2_pciento = models.FloatField(blank=True, null=True)
    impuesto2_monto = models.FloatField(blank=True, null=True)
    miscelaneos = models.CharField(max_length=255, blank=True)
    miscelaneos_pciento = models.CharField(max_length=255, blank=True)
    comentario = models.CharField(max_length=255, blank=True)
    comentario_detalle = models.CharField(max_length=255, blank=True)
    tipo_cambio = models.CharField(max_length=255, blank=True)
    notas = models.CharField(max_length=255, blank=True)
    asiento_id = models.IntegerField(blank=True, null=True)
    docs_cp_id = models.IntegerField(blank=True, null=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    recibida = models.CharField(max_length=255, blank=True)
    impto_en_precio = models.FloatField(blank=True, null=True)
    tipo_compra = models.CharField(max_length=255, blank=True)
    retefuente_pciento = models.FloatField(blank=True, null=True)
    retefuente_monto = models.FloatField(blank=True, null=True)
    reteiva_pciento = models.FloatField(blank=True, null=True)
    reteiva_monto = models.FloatField(blank=True, null=True)
    reteica_pciento = models.FloatField(blank=True, null=True)
    reteica_monto = models.FloatField(blank=True, null=True)
    monto_base = models.FloatField(blank=True, null=True)
    tipo_registracion = models.CharField(max_length=255, blank=True)
    anulado = models.NullBooleanField()
    compra_cancelada = models.NullBooleanField()
    actualizado = models.NullBooleanField()
    ncf = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    aprobada = models.NullBooleanField()
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    facturada = models.NullBooleanField()
    orden_produccion_codigo = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'orden_egreso'

class OrdenEgresoDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    orden_egreso = models.ForeignKey(OrdenEgreso, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    proveedor_id = models.IntegerField(blank=True, null=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    bodega_id = models.IntegerField(blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    recibido = models.NullBooleanField()
    unidad_id = models.IntegerField(blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    impto_pciento = models.FloatField(blank=True, null=True)
    impto_monto = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    descto_monto = models.FloatField(blank=True, null=True)
    impto2_pciento = models.FloatField(blank=True, null=True)
    impto2_monto = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    tipo_cambio = models.CharField(max_length=255, blank=True)
    moneda = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    despachar = models.NullBooleanField()
    disminuir_kardex = models.NullBooleanField()
    unidad_medida = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'orden_egreso_detalle'

class OrdenIngreso(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=255, blank=True)
    supl_direccion1 = models.CharField(max_length=255, blank=True)
    supl_direccion2 = models.CharField(max_length=255, blank=True)
    supl_direccion3 = models.CharField(max_length=255, blank=True)
    supl_direccion4 = models.CharField(max_length=255, blank=True)
    registro_tributario = models.CharField(max_length=255, blank=True)
    enviar = models.NullBooleanField()
    enviar_direccion1 = models.CharField(max_length=255, blank=True)
    enviar_direccion2 = models.CharField(max_length=255, blank=True)
    enviar_direccion3 = models.CharField(max_length=255, blank=True)
    enviar_direccion4 = models.CharField(max_length=255, blank=True)
    tipo_envio = models.CharField(max_length=255, blank=True)
    vendedor = models.CharField(max_length=255, blank=True)
    terminos_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    hora = models.DateTimeField(blank=True, null=True)
    fecha_vcmto = models.DateTimeField(blank=True, null=True)
    pagos = models.CharField(max_length=255, blank=True)
    computador = models.CharField(max_length=255, blank=True)
    moneda = models.CharField(max_length=255, blank=True)
    subtotal = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    impuesto_pciento = models.FloatField(blank=True, null=True)
    impuesto_monto = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    dscto_parcial_monto = models.FloatField(blank=True, null=True)
    impuesto2_pciento = models.FloatField(blank=True, null=True)
    impuesto2_monto = models.FloatField(blank=True, null=True)
    miscelaneos = models.CharField(max_length=255, blank=True)
    miscelaneos_pciento = models.CharField(max_length=255, blank=True)
    comentario = models.CharField(max_length=255, blank=True)
    comentario_detalle = models.CharField(max_length=255, blank=True)
    tipo_cambio = models.CharField(max_length=255, blank=True)
    notas = models.CharField(max_length=255, blank=True)
    asiento_id = models.IntegerField(blank=True, null=True)
    docs_cp_id = models.IntegerField(blank=True, null=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    recibida = models.CharField(max_length=255, blank=True)
    impto_en_precio = models.FloatField(blank=True, null=True)
    tipo_compra = models.CharField(max_length=255, blank=True)
    retefuente_pciento = models.FloatField(blank=True, null=True)
    retefuente_monto = models.FloatField(blank=True, null=True)
    reteiva_pciento = models.FloatField(blank=True, null=True)
    reteiva_monto = models.FloatField(blank=True, null=True)
    reteica_pciento = models.FloatField(blank=True, null=True)
    reteica_monto = models.FloatField(blank=True, null=True)
    monto_base = models.FloatField(blank=True, null=True)
    tipo_registracion = models.CharField(max_length=255, blank=True)
    anulado = models.NullBooleanField()
    compra_cancelada = models.NullBooleanField()
    actualizado = models.NullBooleanField()
    ncf = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    aprobada = models.NullBooleanField()
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    facturada = models.NullBooleanField()
    orden_produccion_codigo = models.CharField(max_length=255, blank=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    tipo_ingreso_id = models.IntegerField(blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'orden_ingreso'

class OrdenIngresoDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    orden_ingreso = models.ForeignKey(OrdenIngreso, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    producto_id = models.IntegerField(blank=True, null=True)
    bodega_id = models.IntegerField(blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    recibido = models.NullBooleanField()
    unidad_id = models.IntegerField(blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    impto_pciento = models.FloatField(blank=True, null=True)
    impto_monto = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    descto_monto = models.FloatField(blank=True, null=True)
    impto2_pciento = models.FloatField(blank=True, null=True)
    impto2_monto = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    tipo_cambio = models.CharField(max_length=255, blank=True)
    moneda = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    despachar = models.NullBooleanField()
    disminuir_kardex = models.NullBooleanField()
    medida = models.CharField(max_length=-1, blank=True)
    class Meta:
        managed = False
        db_table = 'orden_ingreso_detalle'

class OrdenProduccion(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    detalle = models.TextField(blank=True)
    cantidad = models.FloatField(blank=True, null=True)
    largo = models.CharField(max_length=250, blank=True)
    fondo = models.CharField(max_length=250, blank=True)
    alto = models.CharField(max_length=250, blank=True)
    madera = models.NullBooleanField()
    vidrio = models.NullBooleanField()
    hierro = models.NullBooleanField()
    marmol = models.NullBooleanField()
    enchape = models.NullBooleanField()
    enchape_detalle = models.CharField(max_length=250, blank=True)
    tallado = models.NullBooleanField()
    tallado_detalle = models.CharField(max_length=250, blank=True)
    tono = models.CharField(max_length=250, blank=True)
    retractil = models.NullBooleanField()
    panorama = models.NullBooleanField()
    corredizo = models.NullBooleanField()
    oleo = models.NullBooleanField()
    conchaperla = models.NullBooleanField()
    tela_almacen = models.NullBooleanField()
    tela_cliente = models.NullBooleanField()
    agarraderas = models.CharField(max_length=250, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    guia = models.IntegerField(blank=True, null=True)
    adicional = models.NullBooleanField()
    fechapedido = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=250, blank=True)
    estado = models.IntegerField(blank=True, null=True)
    tipo_mueb = models.ForeignKey('TipoMueb', blank=True, null=True)
    doc = models.IntegerField(blank=True, null=True)
    mate = models.NullBooleanField()
    semimate = models.NullBooleanField()
    brillante = models.NullBooleanField()
    pulido = models.NullBooleanField()
    aluminio = models.NullBooleanField()
    acero = models.NullBooleanField()
    abrillantado = models.NullBooleanField()
    pintado = models.NullBooleanField()
    satinado = models.NullBooleanField()
    fechacotizacion = models.NullBooleanField()
    engrampe = models.NullBooleanField()
    impulso = models.NullBooleanField()
    poroabierto = models.NullBooleanField()
    ingreso = models.IntegerField(blank=True, null=True)
    cantaux = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    tiempo_respuesta = models.CharField(max_length=255, blank=True)
    fuera_ciudad = models.NullBooleanField()
    observacion = models.CharField(max_length=-1, blank=True)
    forma_pago = models.ForeignKey(FormaPago, blank=True, null=True)
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    maqueteado_proforma = models.NullBooleanField()
    terminado_maqueteado_proforma = models.NullBooleanField()
    pedido_codigo = models.CharField(max_length=255, blank=True)
    pedido = models.ForeignKey('Pedido', blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    codigo_item = models.CharField(max_length=255, blank=True)
    profundidad = models.CharField(max_length=255, blank=True)
    ancho = models.CharField(max_length=255, blank=True)
    patina_color = models.CharField(max_length=255, blank=True)
    pintado_mano = models.NullBooleanField()
    cuero_cliente = models.NullBooleanField()
    cuero_almacen = models.NullBooleanField()
    fechainicio = models.DateField(blank=True, null=True)
    fechaentrega = models.DateField(blank=True, null=True)
    pedido_detalle = models.ForeignKey('PedidoDetalle', blank=True, null=True)
    finalizada = models.NullBooleanField()
    producto_creado = models.ForeignKey('Producto', blank=True, null=True)
    bodega_productos_blanco = models.NullBooleanField()
    subop_productos_blanco = models.IntegerField(blank=True, null=True)
    metal_hierro = models.NullBooleanField()
    imagen_global = models.CharField(max_length=250, blank=True)
    aprobada = models.NullBooleanField()
    neumatico = models.NullBooleanField()
    venta_local = models.NullBooleanField()
    exportacion = models.NullBooleanField()
    acero_brillante = models.NullBooleanField()
    semiabierto = models.NullBooleanField()
    polyester = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'orden_produccion'

class OrdenProduccionBodega(models.Model):
    id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, blank=True, null=True)
    observaciones = models.CharField(max_length=-1, blank=True)
    cantidad_recibida = models.FloatField(blank=True, null=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    suborden_produccion = models.ForeignKey('SubordenProduccion', blank=True, null=True)
    largo = models.CharField(max_length=255, blank=True)
    fondo = models.CharField(max_length=255, blank=True)
    alto = models.CharField(max_length=255, blank=True)
    codigo = models.CharField(max_length=255, blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    ingresado_bodega = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'orden_produccion_bodega'

class OrdenProduccionReceta(models.Model):
    id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    areas = models.ForeignKey(Areas, blank=True, null=True)
    suborden_produccion = models.ForeignKey('SubordenProduccion', blank=True, null=True)
    material = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'orden_produccion_receta'

class OtroSuplidor(models.Model):
    otro_suplidor_id = models.IntegerField(primary_key=True)
    producto_id_principal = models.ForeignKey('Producto', db_column='producto_id_principal', blank=True, null=True)
    proveedor_id_principal = models.ForeignKey('Proveedor', db_column='proveedor_id_principal', blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'otro_suplidor'

class OtrosEgresosRolEmpleado(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey('TipoIngresoEgresoEmpleado', blank=True, null=True)
    rol_pago_detalle = models.ForeignKey('RolPagoDetalle', blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    anio = models.CharField(max_length=10, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    empleado_id = models.IntegerField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    memo = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    plantilla_rrhh = models.ForeignKey('PlantillaRrhh', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'otros_egresos_rol_empleado'

class OtrosIngresosRolEmpleado(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey('TipoIngresoEgresoEmpleado', blank=True, null=True)
    rol_pago_detalle = models.ForeignKey('RolPagoDetalle', blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    deducible = models.NullBooleanField()
    aportaciones = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    anio = models.CharField(max_length=10, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    empleado = models.ForeignKey(EmpleadosEmpleado, blank=True, null=True)
    horas = models.FloatField(blank=True, null=True)
    plantilla_rrhh = models.ForeignKey('PlantillaRrhh', blank=True, null=True)
    fecha = models.CharField(max_length=255, blank=True)
    hora_inicio = models.CharField(max_length=255, blank=True)
    hora_fin = models.CharField(max_length=255, blank=True)
    pagar = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'otros_ingresos_rol_empleado'

class PagoFondosReserva(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'pago_fondos_reserva'

class Pais(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'pais'

class Parametros(models.Model):
    id = models.IntegerField(primary_key=True)
    clave = models.CharField(max_length=50, blank=True)
    valor = models.CharField(max_length=150, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'parametros'

class Pedido(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    fechacord = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    val_descuento = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    val_iva = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    incompleto = models.NullBooleanField()
    observacion = models.TextField(blank=True)
    abono = models.DateField(blank=True, null=True)
    pago = models.NullBooleanField()
    abona = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    tiempo_respuesta = models.CharField(max_length=255, blank=True)
    fuera_ciudad = models.NullBooleanField()
    fechaentrega = models.DateField(blank=True, null=True)
    condiciones_fisicas = models.CharField(max_length=500, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    proforma_codigo = models.CharField(max_length=255, blank=True)
    maqueteado = models.NullBooleanField()
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    fechapedido = models.DateField(blank=True, null=True)
    aprobada = models.NullBooleanField()
    direccion_entrega = models.CharField(max_length=-1, blank=True)
    forma_pago = models.ForeignKey(FormaPago, blank=True, null=True)
    aprobadavendedor = models.NullBooleanField()
    terminado_maqueteado_pedido = models.NullBooleanField()
    anulada = models.NullBooleanField()
    tipo_lugar = models.ForeignKey('TipoLugar', blank=True, null=True)
    porcentaje_descuento = models.FloatField(blank=True, null=True)
    puntos_venta = models.ForeignKey('PuntosVenta', blank=True, null=True)
    abreviatura_codigo = models.CharField(max_length=10, blank=True)
    porcentaje_iva = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'pedido'

class PedidoDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    pedido = models.ForeignKey(Pedido, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    producto_id = models.IntegerField(blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    observaciones = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    detalle = models.CharField(max_length=-1, blank=True)
    ambiente_id = models.IntegerField(blank=True, null=True)
    reparacion = models.NullBooleanField()
    almacen = models.NullBooleanField()
    largo = models.CharField(max_length=255, blank=True)
    fondo = models.CharField(max_length=255, blank=True)
    alto = models.CharField(max_length=255, blank=True)
    codigo_produccion = models.CharField(max_length=255, blank=True)
    no_producir = models.NullBooleanField()
    proforma_detalle = models.ForeignKey('ProformaDetalle', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'pedido_detalle'

class Permiso(models.Model):
    id = models.IntegerField(primary_key=True)
    empleados_empleado = models.ForeignKey(EmpleadosEmpleado, blank=True, null=True)
    tipo_solicitud = models.ForeignKey('TipoSolicitud', blank=True, null=True)
    fecha_solicitud = models.DateTimeField(blank=True, null=True)
    permisos_dias = models.NullBooleanField()
    permisos_horas = models.NullBooleanField()
    licencia_dias = models.NullBooleanField()
    descanso_iess_dias = models.NullBooleanField()
    cita_iess_horas = models.NullBooleanField()
    fecha_desde = models.DateTimeField(blank=True, null=True)
    fecha_hasta = models.DateTimeField(blank=True, null=True)
    hora_desde = models.TimeField(blank=True, null=True)
    hora_hasta = models.TimeField(blank=True, null=True)
    total_dias_ausencia = models.IntegerField(blank=True, null=True)
    total_horas_ausencia = models.IntegerField(blank=True, null=True)
    motivo_trabajo = models.NullBooleanField()
    motivo_personal = models.NullBooleanField()
    motivo_calamidad = models.NullBooleanField()
    motivo_enfermedad = models.NullBooleanField()
    cargo_vacaciones = models.NullBooleanField()
    activo = models.NullBooleanField()
    observacion = models.CharField(max_length=255, blank=True)
    nombre_empleado = models.CharField(max_length=255, blank=True)
    cargo_empleado = models.CharField(max_length=255, blank=True)
    area_empleado = models.CharField(max_length=255, blank=True)
    vacaciones = models.NullBooleanField()
    periodo = models.NullBooleanField()
    total_dias_pendientes = models.IntegerField(blank=True, null=True)
    periodo_dias_pendiente = models.IntegerField(blank=True, null=True)
    total_horas_laboradas = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'permiso'

class PlantillaRrhh(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=10, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    observaciones = models.CharField(max_length=-1, blank=True)
    abreviatura = models.CharField(max_length=500, blank=True)
    class Meta:
        managed = False
        db_table = 'plantilla_rrhh'

class PlantillaRrhhDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    empleado = models.ForeignKey(EmpleadosEmpleado, blank=True, null=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey('TipoIngresoEgresoEmpleado', blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    plantilla_rrhh = models.ForeignKey(PlantillaRrhh, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'plantilla_rrhh_detalle'

class Prestamo(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    empleado = models.ForeignKey(EmpleadosEmpleado, blank=True, null=True)
    concepto = models.CharField(max_length=250, blank=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey('TipoIngresoEgresoEmpleado', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    valor_mensual = models.FloatField(blank=True, null=True)
    plazos = models.IntegerField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    aprobado = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'prestamo'

class PresupuestoProducto(models.Model):
    id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey('Producto', blank=True, null=True)
    enero = models.IntegerField(blank=True, null=True)
    febrero = models.IntegerField(blank=True, null=True)
    marzo = models.IntegerField(blank=True, null=True)
    abril = models.IntegerField(blank=True, null=True)
    mayo = models.IntegerField(blank=True, null=True)
    junio = models.IntegerField(blank=True, null=True)
    julio = models.IntegerField(blank=True, null=True)
    agosto = models.IntegerField(blank=True, null=True)
    septiembre = models.IntegerField(blank=True, null=True)
    octubre = models.IntegerField(blank=True, null=True)
    noviembre = models.IntegerField(blank=True, null=True)
    diciembre = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'presupuesto_producto'

class Producto(models.Model):
    producto_id = models.IntegerField(primary_key=True)
    codigo_producto = models.CharField(max_length=26, blank=True)
    descripcion_producto = models.CharField(max_length=255, blank=True)
    precio1 = models.FloatField(blank=True, null=True)
    precio2 = models.FloatField(blank=True, null=True)
    precio3 = models.FloatField(blank=True, null=True)
    precio4 = models.FloatField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    unidad_en_compra = models.IntegerField(blank=True, null=True)
    equivalencia_en_compra = models.FloatField(blank=True, null=True)
    cant_total = models.FloatField(blank=True, null=True)
    cant_minimia = models.FloatField(blank=True, null=True)
    categoria = models.ForeignKey(CategoriaProducto, blank=True, null=True)
    sub_categoria = models.ForeignKey('SubCategoriaProducto', blank=True, null=True)
    acepta_lote = models.NullBooleanField()
    valor_inventario = models.FloatField(blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True)
    incremento1 = models.FloatField(blank=True, null=True)
    incremento2 = models.FloatField(blank=True, null=True)
    incremento3 = models.FloatField(blank=True, null=True)
    incremento4 = models.FloatField(blank=True, null=True)
    codigo_fabricante = models.CharField(max_length=20, blank=True)
    producto_fisico = models.IntegerField(blank=True, null=True)
    situacion_producto = models.IntegerField(blank=True, null=True)
    tipo_producto = models.ForeignKey('TipoProducto', db_column='tipo_producto', blank=True, null=True)
    bodega_id = models.IntegerField(blank=True, null=True)
    mostrar_componente = models.NullBooleanField()
    factura_sin_stock = models.NullBooleanField()
    avisa_expiracion = models.NullBooleanField()
    factura_con_precio = models.IntegerField(blank=True, null=True)
    producto_equivalente = models.CharField(max_length=20, blank=True)
    cuenta_compra = models.CharField(max_length=20, blank=True)
    cuenta_venta = models.CharField(max_length=20, blank=True)
    suplidor1_id = models.IntegerField(blank=True, null=True)
    impuesto1_id = models.IntegerField(blank=True, null=True)
    impto1_en_vtas = models.CharField(max_length=20, blank=True)
    impto1_en_compras = models.CharField(max_length=20, blank=True)
    ultima_venta = models.DateTimeField(blank=True, null=True)
    otro_impto_id = models.IntegerField(blank=True, null=True)
    otro_impto_id_vtas = models.CharField(max_length=20, blank=True)
    otro_impto_id_compras = models.CharField(max_length=20, blank=True)
    precio_de_compra_0 = models.FloatField(blank=True, null=True)
    precio_actualizado = models.DateTimeField(blank=True, null=True)
    requiere_nro_serie = models.NullBooleanField()
    costo_dolar = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    comenta_factura = models.CharField(max_length=255, blank=True)
    retencion_id = models.IntegerField(blank=True, null=True)
    rete_vtas = models.CharField(max_length=255, blank=True)
    rete_compras = models.CharField(max_length=255, blank=True)
    notas = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    linea = models.ForeignKey(Linea, blank=True, null=True)
    activo = models.NullBooleanField()
    unidad = models.CharField(max_length=255, blank=True)
    medida_peso = models.CharField(max_length=255, blank=True)
    acepta_iva = models.NullBooleanField()
    peso = models.CharField(max_length=255, blank=True)
    costo_promedio = models.FloatField(blank=True, null=True)
    precio_de_compra_max = models.FloatField(blank=True, null=True)
    uat = models.FloatField(blank=True, null=True)
    codigo_produccion = models.CharField(max_length=255, blank=True)
    horas = models.FloatField(blank=True, null=True)
    costo_horas = models.FloatField(blank=True, null=True)
    costo_produccion = models.FloatField(blank=True, null=True)
    costo_material = models.FloatField(blank=True, null=True)
    costo_fijo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    servicio = models.NullBooleanField()
    precio5 = models.FloatField(blank=True, null=True)
    fecha_ult_vta = models.DateField(blank=True, null=True)
    fecha_ult_com = models.DateField(blank=True, null=True)
    descrip_tipo_producto = models.CharField(max_length=255, blank=True)
    ice = models.NullBooleanField()
    val_uat1 = models.FloatField(blank=True, null=True)
    val_uat2 = models.FloatField(blank=True, null=True)
    bloquea = models.NullBooleanField()
    ultimo_costo = models.FloatField(blank=True, null=True)
    cant_media = models.FloatField(blank=True, null=True)
    cant_maxima = models.FloatField(blank=True, null=True)
    cant_venta = models.FloatField(blank=True, null=True)
    cant_compra = models.FloatField(blank=True, null=True)
    irbp = models.FloatField(blank=True, null=True)
    val_uat3 = models.FloatField(blank=True, null=True)
    val_uat4 = models.FloatField(blank=True, null=True)
    val_uat5 = models.FloatField(blank=True, null=True)
    val_uat6 = models.FloatField(blank=True, null=True)
    descripcion_interna = models.CharField(max_length=500, blank=True)
    porcentaje_precio1 = models.FloatField(blank=True, null=True)
    porcentaje_precio2 = models.FloatField(blank=True, null=True)
    porcentaje_precio3 = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'producto'

class ProductoAreas(models.Model):
    id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    areas = models.ForeignKey(Areas, blank=True, null=True)
    secuencia = models.IntegerField(blank=True, null=True)
    horas = models.FloatField(blank=True, null=True)
    costo_horas = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    costo_materiales = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo_produccion = models.FloatField(blank=True, null=True)
    costo_fijo = models.FloatField(blank=True, null=True)
    precio1 = models.FloatField(blank=True, null=True)
    precio2 = models.FloatField(blank=True, null=True)
    porcentaje_precio2 = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'producto_areas'

class ProductoCategoria(models.Model):
    producto_id = models.IntegerField(blank=True, null=True)
    codigo_producto = models.CharField(max_length=26, blank=True)
    costo = models.FloatField(blank=True, null=True)
    codigo_categoria = models.CharField(max_length=10, blank=True)
    descripcion_categoria = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'producto_categoria'

class ProductoEnBodega(models.Model):
    producto_bodega_id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    ubicacion = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'producto_en_bodega'

class ProductoEquivalente(models.Model):
    producto_equivalente_id = models.IntegerField(primary_key=True)
    producto_id_principal = models.ForeignKey(Producto, db_column='producto_id_principal', blank=True, null=True)
    comentario = models.CharField(max_length=500, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    producto_id_equivalente = models.ForeignKey(Producto, db_column='producto_id_equivalente', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'producto_equivalente'

class ProductoGeneral(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=26, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    precio1 = models.FloatField(blank=True, null=True)
    precio2 = models.FloatField(blank=True, null=True)
    precio3 = models.FloatField(blank=True, null=True)
    precio4 = models.FloatField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    unidad_en_compra = models.IntegerField(blank=True, null=True)
    categoria = models.ForeignKey(CategoriaProducto, blank=True, null=True)
    sub_categoria = models.ForeignKey('SubCategoriaProducto', blank=True, null=True)
    tipo_producto = models.ForeignKey('TipoProducto', blank=True, null=True)
    linea = models.ForeignKey(Linea, blank=True, null=True)
    activo = models.NullBooleanField()
    unidad = models.CharField(max_length=255, blank=True)
    medida_peso = models.CharField(max_length=255, blank=True)
    acepta_iva = models.NullBooleanField()
    peso = models.CharField(max_length=255, blank=True)
    codigo_produccion = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'producto_general'

class ProductoManoObra(models.Model):
    id = models.IntegerField(primary_key=True)
    producto_areas = models.ForeignKey(ProductoAreas, blank=True, null=True)
    operacion_unitaria = models.CharField(max_length=255, blank=True)
    empleado = models.CharField(max_length=255, blank=True)
    hora_inicio = models.CharField(max_length=255, blank=True)
    hora_fin = models.CharField(max_length=255, blank=True)
    hora_total = models.FloatField(blank=True, null=True)
    costo_hora = models.FloatField(blank=True, null=True)
    costo_total = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    tipo_hora = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'producto_mano_obra'

class Proforma(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    detalle = models.TextField(blank=True)
    cantidad = models.IntegerField(blank=True, null=True)
    largo = models.CharField(max_length=250, blank=True)
    fondo = models.CharField(max_length=250, blank=True)
    alto = models.CharField(max_length=250, blank=True)
    madera = models.NullBooleanField()
    vidrio = models.NullBooleanField()
    hierro = models.NullBooleanField()
    marmol = models.NullBooleanField()
    enchape = models.NullBooleanField()
    enchape_detalle = models.CharField(max_length=250, blank=True)
    tallado = models.NullBooleanField()
    tallado_detalle = models.CharField(max_length=250, blank=True)
    tono = models.CharField(max_length=250, blank=True)
    retractil = models.NullBooleanField()
    panorama = models.NullBooleanField()
    corredizo = models.NullBooleanField()
    oleo = models.NullBooleanField()
    conchaperla = models.NullBooleanField()
    tela_almacen = models.NullBooleanField()
    tela_cliente = models.NullBooleanField()
    agarraderas = models.CharField(max_length=250, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    guia = models.IntegerField(blank=True, null=True)
    adicional = models.NullBooleanField()
    fechapedido = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=250, blank=True)
    estado = models.ForeignKey(EstadosPro, db_column='estado', blank=True, null=True)
    tipo_mue = models.ForeignKey('TipoMueb', db_column='tipo_mue', blank=True, null=True)
    doc = models.IntegerField(blank=True, null=True)
    mate = models.NullBooleanField()
    semimate = models.NullBooleanField()
    brillante = models.NullBooleanField()
    pulido = models.NullBooleanField()
    aluminio = models.NullBooleanField()
    acero = models.NullBooleanField()
    abrillantado = models.NullBooleanField()
    pintado = models.NullBooleanField()
    satinado = models.NullBooleanField()
    fechacotizacion = models.NullBooleanField()
    engrampe = models.NullBooleanField()
    impulso = models.NullBooleanField()
    poroabierto = models.NullBooleanField()
    ingreso = models.IntegerField(blank=True, null=True)
    cantaux = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    tiempo_respuesta = models.CharField(max_length=255, blank=True)
    fuera_ciudad = models.NullBooleanField()
    observacion = models.CharField(max_length=-1, blank=True)
    forma_pago = models.ForeignKey(FormaPago, blank=True, null=True)
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    maqueteado_proforma = models.NullBooleanField()
    terminado_maqueteado_proforma = models.NullBooleanField()
    reunion_codigo = models.CharField(max_length=255, blank=True)
    reunion = models.ForeignKey('Reunion', blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    direccion_entrega = models.CharField(max_length=255, blank=True)
    iva = models.FloatField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    porcentaje_descuento = models.FloatField(blank=True, null=True)
    aprobada = models.NullBooleanField()
    anulada = models.NullBooleanField()
    tipo_lugar = models.ForeignKey('TipoLugar', blank=True, null=True)
    puntos_venta = models.ForeignKey('PuntosVenta', blank=True, null=True)
    abreviatura_codigo = models.CharField(max_length=10, blank=True)
    hierro_proforma = models.NullBooleanField()
    porcentaje_iva = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'proforma'

class ProformaComision(models.Model):
    id = models.IntegerField(primary_key=True)
    proforma = models.ForeignKey(Proforma, blank=True, null=True)
    porcentaje_comision = models.FloatField(blank=True, null=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'proforma_comision'

class ProformaComisionAbono(models.Model):
    id = models.IntegerField(primary_key=True)
    proforma_comision = models.ForeignKey(ProformaComision, blank=True, null=True)
    abono = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'proforma_comision_abono'

class ProformaDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    proforma = models.ForeignKey(Proforma, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    observaciones = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    detalle = models.CharField(max_length=-1, blank=True)
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    reparacion = models.NullBooleanField()
    almacen = models.NullBooleanField()
    largo = models.CharField(max_length=255, blank=True)
    fondo = models.CharField(max_length=255, blank=True)
    alto = models.CharField(max_length=255, blank=True)
    codigo_produccion = models.CharField(max_length=255, blank=True)
    no_producir = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'proforma_detalle'

class ProformaDetalleFactura(models.Model):
    id = models.IntegerField(primary_key=True)
    proforma_factura_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    producto_id = models.IntegerField(blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    observaciones = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    detalle = models.CharField(max_length=-1, blank=True)
    ambiente_id = models.IntegerField(blank=True, null=True)
    reparacion = models.NullBooleanField()
    almacen = models.NullBooleanField()
    largo = models.CharField(max_length=255, blank=True)
    fondo = models.CharField(max_length=255, blank=True)
    alto = models.CharField(max_length=255, blank=True)
    codigo_produccion = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'proforma_detalle_factura'

class ProformaFactura(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    cliente_id = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    detalle = models.TextField(blank=True)
    cantidad = models.IntegerField(blank=True, null=True)
    largo = models.CharField(max_length=250, blank=True)
    fondo = models.CharField(max_length=250, blank=True)
    alto = models.CharField(max_length=250, blank=True)
    madera = models.NullBooleanField()
    vidrio = models.NullBooleanField()
    hierro = models.NullBooleanField()
    marmol = models.NullBooleanField()
    enchape = models.NullBooleanField()
    enchape_detalle = models.CharField(max_length=250, blank=True)
    tallado = models.NullBooleanField()
    tallado_detalle = models.CharField(max_length=250, blank=True)
    tono = models.CharField(max_length=250, blank=True)
    retractil = models.NullBooleanField()
    panorama = models.NullBooleanField()
    corredizo = models.NullBooleanField()
    oleo = models.NullBooleanField()
    conchaperla = models.NullBooleanField()
    tela_almacen = models.NullBooleanField()
    tela_cliente = models.NullBooleanField()
    agarraderas = models.CharField(max_length=250, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    guia = models.IntegerField(blank=True, null=True)
    adicional = models.NullBooleanField()
    fechapedido = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=250, blank=True)
    estado = models.IntegerField(blank=True, null=True)
    tipo_mue = models.IntegerField(blank=True, null=True)
    doc = models.IntegerField(blank=True, null=True)
    mate = models.NullBooleanField()
    semimate = models.NullBooleanField()
    brillante = models.NullBooleanField()
    pulido = models.NullBooleanField()
    aluminio = models.NullBooleanField()
    acero = models.NullBooleanField()
    abrillantado = models.NullBooleanField()
    pintado = models.NullBooleanField()
    satinado = models.NullBooleanField()
    fechacotizacion = models.NullBooleanField()
    engrampe = models.NullBooleanField()
    impulso = models.NullBooleanField()
    poroabierto = models.NullBooleanField()
    ingreso = models.IntegerField(blank=True, null=True)
    cantaux = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vendedor_id = models.IntegerField(blank=True, null=True)
    tiempo_respuesta = models.CharField(max_length=255, blank=True)
    fuera_ciudad = models.NullBooleanField()
    observacion = models.CharField(max_length=-1, blank=True)
    forma_pago_id = models.IntegerField(blank=True, null=True)
    ambiente_id = models.IntegerField(blank=True, null=True)
    maqueteado_proforma = models.NullBooleanField()
    terminado_maqueteado_proforma = models.NullBooleanField()
    reunion_codigo = models.CharField(max_length=255, blank=True)
    reunion_id = models.IntegerField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    direccion_entrega = models.CharField(max_length=255, blank=True)
    iva = models.FloatField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    porcentaje_descuento = models.FloatField(blank=True, null=True)
    aprobada = models.NullBooleanField()
    anulada = models.NullBooleanField()
    tipo_lugar_id = models.IntegerField(blank=True, null=True)
    puntos_venta_id = models.IntegerField(blank=True, null=True)
    abreviatura_codigo = models.CharField(max_length=10, blank=True)
    hierro_proforma = models.NullBooleanField()
    porcentaje_iva = models.FloatField(blank=True, null=True)
    proforma_id = models.IntegerField(blank=True, null=True)
    proforma_codigo = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'proforma_factura'

class Proveedor(models.Model):
    proveedor_id = models.IntegerField(primary_key=True)
    codigo_proveedor = models.CharField(max_length=26, blank=True)
    nombre_proveedor = models.CharField(max_length=255, blank=True)
    direccion1 = models.CharField(max_length=255, blank=True)
    direccion2 = models.CharField(max_length=255, blank=True)
    direccion3 = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=255, blank=True)
    pais = models.CharField(max_length=255, blank=True)
    codigo_postal = models.CharField(max_length=255, blank=True)
    telefono1 = models.CharField(max_length=255, blank=True)
    telefono2 = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    contacto = models.CharField(max_length=255, blank=True)
    e_mail1 = models.CharField(max_length=255, blank=True)
    e_mail2 = models.CharField(max_length=255, blank=True)
    categoria_idpv = models.IntegerField(blank=True, null=True)
    vendedor = models.IntegerField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    proveedor_activo = models.NullBooleanField()
    aplica_impto = models.NullBooleanField()
    registro_empresarial = models.CharField(max_length=255, blank=True)
    registro_tributario = models.CharField(max_length=255, blank=True)
    cuenta_cont_compras = models.CharField(max_length=255, blank=True)
    giro_idpv = models.CharField(max_length=255, blank=True)
    creado = models.CharField(max_length=255, blank=True)
    maximo_credito = models.CharField(max_length=255, blank=True)
    descuento = models.FloatField(blank=True, null=True)
    interes_anual = models.FloatField(blank=True, null=True)
    termino_idpv = models.CharField(max_length=255, blank=True)
    monto_ult_transac = models.CharField(max_length=255, blank=True)
    fecha_ult_transac = models.DateTimeField(blank=True, null=True)
    descri_ult_transac = models.CharField(max_length=255, blank=True)
    comentario = models.CharField(max_length=255, blank=True)
    campo1 = models.CharField(max_length=255, blank=True)
    campo2 = models.CharField(max_length=255, blank=True)
    campo3 = models.CharField(max_length=255, blank=True)
    primer_nombre = models.CharField(max_length=255, blank=True)
    segundo_nombre = models.CharField(max_length=255, blank=True)
    primer_apellido = models.CharField(max_length=255, blank=True)
    segundo_apellido = models.CharField(max_length=255, blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    tipo_empresa = models.CharField(max_length=255, blank=True)
    impto = models.CharField(max_length=255, blank=True)
    segundo_impto = models.CharField(max_length=255, blank=True)
    aplica_reten_impto = models.NullBooleanField()
    reten_impto = models.CharField(max_length=255, blank=True)
    aplica_2do_impto = models.NullBooleanField()
    aplica_reten_fuente = models.NullBooleanField()
    reten_fuente = models.FloatField(blank=True, null=True)
    reten_ica = models.FloatField(blank=True, null=True)
    aplica_reten_ica = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_nacimiento = models.DateTimeField(blank=True, null=True)
    clase_id = models.IntegerField(blank=True, null=True)
    categoria_cliente_id = models.IntegerField(blank=True, null=True)
    zona_id = models.IntegerField(blank=True, null=True)
    provincia_id = models.IntegerField(blank=True, null=True)
    ciudad_id = models.IntegerField(blank=True, null=True)
    tipo_vta_id = models.IntegerField(blank=True, null=True)
    ruc = models.CharField(max_length=20, blank=True)
    cupo = models.FloatField(blank=True, null=True)
    serie = models.CharField(max_length=255, blank=True)
    esnatural = models.IntegerField(blank=True, null=True)
    hasnfac = models.CharField(max_length=255, blank=True)
    descnfac = models.CharField(max_length=255, blank=True)
    obligcont = models.NullBooleanField()
    autoriza = models.CharField(max_length=255, blank=True)
    validez = models.DateTimeField(blank=True, null=True)
    ret_fue = models.IntegerField(blank=True, null=True)
    ret_iva = models.IntegerField(blank=True, null=True)
    pag_cheque = models.NullBooleanField()
    incluye_ice = models.NullBooleanField()
    convenio_hasta = models.DateTimeField(blank=True, null=True)
    consignacion = models.NullBooleanField()
    prod_usr = models.IntegerField(blank=True, null=True)
    cod_local = models.IntegerField(blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True)
    pasaporte = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'proveedor'

class Provincia(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    fecha_ini = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'provincia'

class PuntosVenta(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=26, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=255, blank=True)
    nro_productos = models.IntegerField(blank=True, null=True)
    activo = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo_proforma = models.CharField(max_length=10, blank=True)
    class Meta:
        managed = False
        db_table = 'puntos_venta'

class RazonSocial(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo_razon_social = models.CharField(max_length=20, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    direccion1 = models.CharField(max_length=255, blank=True)
    direccion2 = models.CharField(max_length=255, blank=True)
    direccion3 = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=255, blank=True)
    pais = models.CharField(max_length=255, blank=True)
    codigo_postal = models.CharField(max_length=255, blank=True)
    telefono1 = models.CharField(max_length=255, blank=True)
    telefono2 = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    contacto = models.CharField(max_length=255, blank=True)
    email1 = models.CharField(max_length=255, blank=True)
    email2 = models.CharField(max_length=255, blank=True)
    categoria_cliente_id = models.IntegerField(blank=True, null=True)
    vendedor_id = models.IntegerField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    cliente_activo = models.NullBooleanField()
    registro_empresarial = models.CharField(max_length=255, blank=True)
    registro_tributario = models.CharField(max_length=255, blank=True)
    cuenta_cont_ventas = models.CharField(max_length=255, blank=True)
    giro_id = models.IntegerField(blank=True, null=True)
    creado = models.CharField(max_length=255, blank=True)
    maximo_credito = models.FloatField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    interes_anual = models.FloatField(blank=True, null=True)
    termino_id = models.IntegerField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    facturar_con = models.CharField(max_length=255, blank=True)
    campo1 = models.CharField(max_length=255, blank=True)
    campo2 = models.CharField(max_length=255, blank=True)
    campo3 = models.CharField(max_length=255, blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    aplica_reten_impto = models.NullBooleanField()
    reten_impto = models.FloatField(blank=True, null=True)
    aplica_reten_ica = models.NullBooleanField()
    reten_ica = models.FloatField(blank=True, null=True)
    aplica_reten_fuente = models.NullBooleanField()
    reten_fuente = models.FloatField(blank=True, null=True)
    aplica_2do_impto = models.NullBooleanField()
    segundo_impto = models.FloatField(blank=True, null=True)
    aplica_impto = models.NullBooleanField()
    impto = models.FloatField(blank=True, null=True)
    primer_apellido = models.CharField(max_length=255, blank=True)
    segundo_apellido = models.CharField(max_length=255, blank=True)
    primer_nombre = models.CharField(max_length=255, blank=True)
    segundo_nombre = models.CharField(max_length=255, blank=True)
    tipo_empresa = models.CharField(max_length=255, blank=True)
    impto_incluido = models.CharField(max_length=255, blank=True)
    monto_ult_transac = models.FloatField(blank=True, null=True)
    fecha_ult_transac = models.DateTimeField(blank=True, null=True)
    descri_ult_transac = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    ruc = models.CharField(max_length=13, blank=True)
    fecha_nacimiento = models.DateTimeField(blank=True, null=True)
    sexo = models.CharField(max_length=10, blank=True)
    clase_id = models.IntegerField(blank=True, null=True)
    validez = models.DateTimeField(blank=True, null=True)
    incluye_ice = models.NullBooleanField()
    convenio_hasta = models.DateTimeField(blank=True, null=True)
    consignacion = models.NullBooleanField()
    cuenta_anticipo = models.CharField(max_length=-1, blank=True)
    pasaporte = models.NullBooleanField()
    tipo_precio_id = models.IntegerField(blank=True, null=True)
    zona_id = models.IntegerField(blank=True, null=True)
    provincia_id = models.IntegerField(blank=True, null=True)
    ciudad_id = models.IntegerField(blank=True, null=True)
    banco_id = models.IntegerField(blank=True, null=True)
    plan_de_cuentas = models.ForeignKey(ContabilidadPlandecuentas, blank=True, null=True)
    cupo_credito = models.FloatField(blank=True, null=True)
    dias_credito = models.IntegerField(blank=True, null=True)
    tipo_cliente_id = models.IntegerField(blank=True, null=True)
    tipo_razon_social = models.ForeignKey('TipoRazonSocial', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'razon_social'

class RazonSocialClientes(models.Model):
    id = models.IntegerField(primary_key=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    razon_social = models.ForeignKey(RazonSocial, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'razon_social_clientes'

class RegistrarCobroPago(models.Model):
    id = models.IntegerField(primary_key=True)
    numero_documento = models.CharField(max_length=250, blank=True)
    tipo_transaccion = models.ForeignKey('TipoTransaccion', blank=True, null=True)
    forma_cobro_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    cuenta_pago_cobro = models.CharField(max_length=255, blank=True)
    numero_comprobante = models.CharField(max_length=255, blank=True)
    efectivo = models.NullBooleanField()
    descripcion = models.CharField(max_length=255, blank=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    plan_cuenta = models.ForeignKey(ContabilidadPlandecuentas, blank=True, null=True)
    puntos_venta = models.ForeignKey(PuntosVenta, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'registrar_cobro_pago'

class RegistrarCobroPagoDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    documento = models.CharField(max_length=250, blank=True)
    fecha_emision = models.DateField(blank=True, null=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    tipo_documento = models.CharField(max_length=250, blank=True)
    valor = models.FloatField(blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    valor_a_pagar = models.FloatField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    proforma_factura = models.ForeignKey(ProformaFactura, blank=True, null=True)
    factura = models.ForeignKey(Factura, blank=True, null=True)
    registrar_cobro_pago = models.ForeignKey(RegistrarCobroPago, blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    proforma = models.ForeignKey(Proforma, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'registrar_cobro_pago_detalle'

class RelacionLaboral(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'relacion_laboral'

class RetencionesTiporetencion(models.Model):
    tipo_retencion_id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=255)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    impuesto = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'retenciones_tiporetencion'

class Reunion(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    motivo = models.CharField(max_length=250, blank=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    observacion = models.CharField(max_length=500, blank=True)
    tiempo_respuesta = models.CharField(max_length=250, blank=True)
    observacion_tiempo_respuesta = models.CharField(max_length=500, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    bodega = models.NullBooleanField()
    respuesta_bodega = models.CharField(max_length=-1, blank=True)
    finalizado_bodega = models.NullBooleanField()
    direccion = models.CharField(max_length=-1, blank=True)
    class Meta:
        managed = False
        db_table = 'reunion'

class RolPago(models.Model):
    id = models.IntegerField(primary_key=True)
    anio = models.CharField(max_length=250, blank=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    salario_base = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rol_pago'

class RolPagoConfiguraciones(models.Model):
    id = models.IntegerField(primary_key=True)
    dia_pago = models.IntegerField(blank=True, null=True)
    porcentaje_primera_quincena = models.FloatField(blank=True, null=True)
    mensual = models.NullBooleanField()
    quincenal = models.NullBooleanField()
    porcentaje_iess = models.FloatField(blank=True, null=True)
    extension_conyugal_iess = models.FloatField(blank=True, null=True)
    plan_cuentas = models.ForeignKey(ContabilidadPlandecuentas, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    banco = models.ForeignKey(Banco, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rol_pago_configuraciones'

class RolPagoCuentaContable(models.Model):
    id = models.IntegerField(primary_key=True)
    rol_pago_configuraciones = models.ForeignKey(RolPagoConfiguraciones, blank=True, null=True)
    grupo_pago = models.ForeignKey(GrupoPago, blank=True, null=True)
    clave = models.CharField(max_length=255, blank=True)
    plandecuentas = models.ForeignKey(ContabilidadPlandecuentas, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tipo_cuenta = models.ForeignKey(ContabilidadTipocuenta, blank=True, null=True)
    clasificacion_cuenta = models.ForeignKey(ClasificacionCuenta, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rol_pago_cuenta_contable'

class RolPagoDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    rol_pago = models.ForeignKey(RolPago, blank=True, null=True)
    empleado = models.ForeignKey(EmpleadosEmpleado, blank=True, null=True)
    ingresos = models.FloatField(blank=True, null=True)
    egresos = models.FloatField(blank=True, null=True)
    otros_ingresos = models.FloatField(blank=True, null=True)
    otros_egresos = models.FloatField(blank=True, null=True)
    dias = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    tipo_pago = models.ForeignKey('TipoPago', blank=True, null=True)
    banco = models.ForeignKey(Banco, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    numero_comprobante = models.CharField(max_length=255, blank=True)
    fondo_reserva = models.FloatField(blank=True, null=True)
    decimo_tercero = models.FloatField(blank=True, null=True)
    decimo_cuarto = models.FloatField(blank=True, null=True)
    iess_asumido = models.FloatField(blank=True, null=True)
    impuesto_renta = models.FloatField(blank=True, null=True)
    nueve_cuarenta_cinco = models.FloatField(blank=True, null=True)
    tres_cuarenta_uno = models.FloatField(blank=True, null=True)
    descuento_dias = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rol_pago_detalle'

class RolPagoPlantilla(models.Model):
    id = models.IntegerField(primary_key=True)
    plantilla_rrhh = models.ForeignKey(PlantillaRrhh, blank=True, null=True)
    rol_pago = models.ForeignKey(RolPago, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    mes = models.IntegerField(blank=True, null=True)
    anio = models.CharField(max_length=10, blank=True)
    quincena = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'rol_pago_plantilla'

class Rop(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    detalle = models.TextField(blank=True)
    cantidad = models.FloatField(blank=True, null=True)
    largo = models.CharField(max_length=250, blank=True)
    fondo = models.CharField(max_length=250, blank=True)
    alto = models.CharField(max_length=250, blank=True)
    madera = models.NullBooleanField()
    vidrio = models.NullBooleanField()
    hierro = models.NullBooleanField()
    marmol = models.NullBooleanField()
    enchape = models.NullBooleanField()
    enchape_detalle = models.CharField(max_length=250, blank=True)
    tallado = models.NullBooleanField()
    tallado_detalle = models.CharField(max_length=250, blank=True)
    tono = models.CharField(max_length=250, blank=True)
    retractil = models.NullBooleanField()
    panorama = models.NullBooleanField()
    corredizo = models.NullBooleanField()
    oleo = models.NullBooleanField()
    conchaperla = models.NullBooleanField()
    tela_almacen = models.NullBooleanField()
    tela_cliente = models.NullBooleanField()
    agarraderas = models.CharField(max_length=250, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    guia = models.IntegerField(blank=True, null=True)
    adicional = models.NullBooleanField()
    fechapedido = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=250, blank=True)
    estado = models.IntegerField(blank=True, null=True)
    tipo_mueb = models.ForeignKey('TipoMueb', blank=True, null=True)
    doc = models.IntegerField(blank=True, null=True)
    mate = models.NullBooleanField()
    semimate = models.NullBooleanField()
    brillante = models.NullBooleanField()
    pulido = models.NullBooleanField()
    aluminio = models.NullBooleanField()
    acero = models.NullBooleanField()
    abrillantado = models.NullBooleanField()
    pintado = models.NullBooleanField()
    satinado = models.NullBooleanField()
    fechacotizacion = models.NullBooleanField()
    engrampe = models.NullBooleanField()
    impulso = models.NullBooleanField()
    poroabierto = models.NullBooleanField()
    ingreso = models.IntegerField(blank=True, null=True)
    cantaux = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True)
    tiempo_respuesta = models.CharField(max_length=255, blank=True)
    fuera_ciudad = models.NullBooleanField()
    observacion = models.CharField(max_length=-1, blank=True)
    forma_pago = models.ForeignKey(FormaPago, blank=True, null=True)
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    codigo_item = models.CharField(max_length=255, blank=True)
    profundidad = models.CharField(max_length=255, blank=True)
    ancho = models.CharField(max_length=255, blank=True)
    patina_color = models.CharField(max_length=255, blank=True)
    pintado_mano = models.NullBooleanField()
    cuero_cliente = models.NullBooleanField()
    cuero_almacen = models.NullBooleanField()
    fechainicio = models.DateField(blank=True, null=True)
    fechaentrega = models.DateField(blank=True, null=True)
    finalizada = models.NullBooleanField()
    bodega_productos_blanco = models.NullBooleanField()
    subop_productos_blanco = models.IntegerField(blank=True, null=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, blank=True, null=True)
    metal_hierro = models.NullBooleanField()
    codigo_orden_produccion = models.CharField(max_length=255, blank=True)
    aprobada = models.NullBooleanField()
    neumatico = models.NullBooleanField()
    venta_local = models.NullBooleanField()
    exportacion = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'rop'

class Secuenciales(models.Model):
    id = models.IntegerField(primary_key=True)
    modulo = models.CharField(max_length=255, blank=True)
    secuencial = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'secuenciales'

class Seriales(models.Model):
    serial_id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    nro_serial = models.CharField(max_length=255, blank=True)
    ingresado = models.CharField(max_length=255, blank=True)
    modulo_ingreso = models.CharField(max_length=255, blank=True)
    nro_doc_ingreso = models.CharField(max_length=255, blank=True)
    salida = models.CharField(max_length=255, blank=True)
    cliente_mid = models.ForeignKey(Cliente, db_column='cliente_mid', blank=True, null=True)
    modulo_salida = models.CharField(max_length=255, blank=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    nro_item = models.IntegerField(blank=True, null=True)
    nro_doc_salida = models.IntegerField(blank=True, null=True)
    nro_item_s = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    proveedor_mid = models.ForeignKey(Proveedor, db_column='proveedor_mid', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'seriales'

class SubCategoriaProducto(models.Model):
    sub_categoria_producto_id = models.IntegerField(primary_key=True)
    codigo_sub_categ = models.CharField(max_length=10, blank=True)
    categoria = models.ForeignKey(CategoriaProducto, blank=True, null=True)
    descripcion_sub_categ = models.CharField(max_length=255, blank=True)
    predeterminado = models.IntegerField(blank=True, null=True)
    nro_productos = models.IntegerField(blank=True, null=True)
    imagen_subcateg = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sub_categoria_producto'

class SubordenProduccion(models.Model):
    id = models.IntegerField(primary_key=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    areas = models.ForeignKey(Areas, blank=True, null=True)
    secuencia = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)
    observaciones = models.CharField(max_length=-1, blank=True)
    finalizada = models.NullBooleanField()
    producto_en_blanco = models.NullBooleanField()
    reproceso = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'suborden_produccion'

class SubordenProduccionDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    suborden_produccion = models.ForeignKey(SubordenProduccion, blank=True, null=True)
    operacion_unitaria = models.CharField(max_length=255, blank=True)
    empleado = models.CharField(max_length=255, blank=True)
    hora_inicio = models.CharField(max_length=255, blank=True)
    hora_fin = models.CharField(max_length=255, blank=True)
    hora_total = models.FloatField(blank=True, null=True)
    costo_hora = models.FloatField(blank=True, null=True)
    costo_total = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    tipo_hora = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'suborden_produccion_detalle'

class SubordenProduccionReproceso(models.Model):
    id = models.IntegerField(primary_key=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    areas = models.ForeignKey(Areas, blank=True, null=True)
    secuencia = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)
    observaciones = models.CharField(max_length=-1, blank=True)
    finalizada = models.NullBooleanField()
    producto_en_blanco = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'suborden_produccion_reproceso'

class SubordenProduccionReprocesoDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    suborden_produccion_reproceso = models.ForeignKey(SubordenProduccionReproceso, blank=True, null=True)
    operacion_unitaria = models.CharField(max_length=255, blank=True)
    empleado = models.CharField(max_length=255, blank=True)
    hora_inicio = models.CharField(max_length=255, blank=True)
    hora_fin = models.CharField(max_length=255, blank=True)
    hora_total = models.FloatField(blank=True, null=True)
    costo_hora = models.FloatField(blank=True, null=True)
    costo_total = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'suborden_produccion_reproceso_detalle'

class SubordenProduccionReprocesoReceta(models.Model):
    id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    areas_id = models.IntegerField(blank=True, null=True)
    suborden_produccion_reproceso = models.ForeignKey(SubordenProduccionReproceso, blank=True, null=True)
    material = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'suborden_produccion_reproceso_receta'

class SueldosUnificados(models.Model):
    id = models.IntegerField(primary_key=True)
    anio = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sueldo = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sueldos_unificados'

class TerminosPago(models.Model):
    termino_id = models.IntegerField(primary_key=True)
    codigo_termino = models.CharField(max_length=4)
    descripcion_termino = models.CharField(db_column='Descripcion_termino', max_length=40) # Field name made lowercase.
    tipo_pago = models.CharField(max_length=2)
    monto = models.DecimalField(max_digits=18, decimal_places=4)
    dias = models.IntegerField()
    inicial = models.DecimalField(max_digits=18, decimal_places=4)
    cuotas = models.IntegerField()
    dscto_pronto_pago = models.DecimalField(max_digits=18, decimal_places=4)
    cuenta_contable = models.CharField(max_length=20)
    predeterminado = models.IntegerField()
    cuenta_corriente = models.CharField(max_length=40)
    cliente_paga_en = models.CharField(max_length=2)
    class Meta:
        managed = False
        db_table = 'terminos_pago'

class TerminosPagopv(models.Model):
    termino_idpv = models.IntegerField()
    codigo_terminopv = models.IntegerField(blank=True, null=True)
    descripcion_terminopv = models.CharField(max_length=255, blank=True)
    tipo_pago = models.CharField(max_length=255, blank=True)
    monto = models.FloatField(blank=True, null=True)
    dias = models.IntegerField(blank=True, null=True)
    inicial = models.FloatField(blank=True, null=True)
    cuotas = models.FloatField(blank=True, null=True)
    dscto_pronto_pago = models.FloatField(blank=True, null=True)
    cuenta_contable = models.IntegerField(blank=True, null=True)
    predeterminado = models.CharField(max_length=255, blank=True)
    cuenta_corriente = models.CharField(max_length=255, blank=True)
    cliente_paga_en = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'terminos_pagopv'

class TipoAusencia(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_ausencia'

class TipoCliente(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=26, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    activo = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_cliente'

class TipoContrato(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_contrato'

class TipoGuia(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    accion = models.CharField(max_length=250, blank=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'tipo_guia'

class TipoIngresoEgresoEmpleado(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True)
    ingreso = models.NullBooleanField()
    egreso = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    calcular_ingreso = models.NullBooleanField()
    parte_ingreso = models.NullBooleanField()
    otros_ingresos = models.NullBooleanField()
    otros_egresos = models.NullBooleanField()
    orden = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_ingreso_egreso_empleado'

class TipoLugar(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_lugar'

class TipoMueb(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_mueb'

class TipoPago(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_pago'

class TipoProducto(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'tipo_producto'

class TipoRazonSocial(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=10, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_razon_social'

class TipoRemuneracion(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'tipo_remuneracion'

class TipoSolicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_solicitud'

class TipoTransaccion(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_transaccion'

class TransaccionesProforma(models.Model):
    proforma_id = models.IntegerField(primary_key=True)
    numero_documento = models.CharField(max_length=250)
    tipo_registro_documento = models.IntegerField()
    tipo_documento = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente)
    referencia = models.CharField(max_length=255)
    vendedor = models.ForeignKey(EmpleadosEmpleado, blank=True, null=True)
    vencimiento = models.IntegerField()
    proyecto = models.CharField(max_length=255)
    atencion = models.CharField(max_length=255)
    forma_de_pago = models.CharField(max_length=255)
    garantia = models.CharField(max_length=255)
    activo = models.BooleanField()
    bodega = models.ForeignKey(Bodega)
    descripcion = models.CharField(max_length=255)
    subtotal12 = models.DecimalField(max_digits=18, decimal_places=4)
    subtotal0 = models.DecimalField(max_digits=18, decimal_places=4)
    descuento = models.DecimalField(max_digits=18, decimal_places=4)
    iva = models.DecimalField(max_digits=18, decimal_places=4)
    total = models.DecimalField(max_digits=18, decimal_places=4)
    saldo = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    saldo_cobrar = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'transacciones_proforma'

class TransaccionesProformadetalle(models.Model):
    detalle_id = models.IntegerField(primary_key=True)
    proforma = models.ForeignKey(TransaccionesProforma)
    tipo = models.IntegerField()
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto)
    cuenta = models.ForeignKey(ContabilidadPlandecuentas)
    centro = models.ForeignKey(ContabilidadCentrocosto)
    valor = models.DecimalField(max_digits=18, decimal_places=4)
    iva = models.DecimalField(max_digits=4, decimal_places=2)
    ice = models.DecimalField(max_digits=4, decimal_places=2)
    retencion_ir = models.ForeignKey(RetencionesTiporetencion, blank=True, null=True)
    retencion_iva = models.ForeignKey(RetencionesTiporetencion, blank=True, null=True)
    desc = models.DecimalField(max_digits=18, decimal_places=4)
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    class Meta:
        managed = False
        db_table = 'transacciones_proformadetalle'

class TransaccionesRegistrodocumento(models.Model):
    registrodoc_id = models.IntegerField(primary_key=True)
    numero_documento = models.CharField(max_length=250)
    tipo_registro_documento = models.IntegerField()
    tipo_documento = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente)
    referencia = models.CharField(max_length=255)
    vendedor = models.ForeignKey(EmpleadosEmpleado, blank=True, null=True)
    vencimiento = models.IntegerField()
    proyecto = models.CharField(max_length=255)
    atencion = models.CharField(max_length=255)
    forma_de_pago = models.CharField(max_length=255)
    garantia = models.CharField(max_length=255)
    activo = models.BooleanField()
    bodega = models.ForeignKey(Bodega)
    descripcion = models.CharField(max_length=255)
    subtotal12 = models.DecimalField(max_digits=18, decimal_places=4)
    subtotal0 = models.DecimalField(max_digits=18, decimal_places=4)
    descuento = models.DecimalField(max_digits=18, decimal_places=4)
    iva = models.DecimalField(max_digits=18, decimal_places=4)
    total = models.DecimalField(max_digits=18, decimal_places=4)
    saldo = models.DecimalField(max_digits=18, decimal_places=4)
    saldo_cobrar = models.DecimalField(max_digits=18, decimal_places=4)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'transacciones_registrodocumento'

class TransaccionesRegistrodocumentodetalle(models.Model):
    detalle_id = models.IntegerField(primary_key=True)
    registrodoc = models.ForeignKey(TransaccionesRegistrodocumento)
    tipo = models.IntegerField()
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto)
    cuenta = models.ForeignKey(ContabilidadPlandecuentas)
    centro = models.ForeignKey(ContabilidadCentrocosto)
    valor = models.DecimalField(max_digits=18, decimal_places=4)
    iva = models.DecimalField(max_digits=4, decimal_places=2)
    ice = models.DecimalField(max_digits=4, decimal_places=2)
    retencion_ir = models.ForeignKey(RetencionesTiporetencion)
    retencion_iva = models.ForeignKey(RetencionesTiporetencion)
    desc = models.DecimalField(max_digits=18, decimal_places=4)
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    class Meta:
        managed = False
        db_table = 'transacciones_registrodocumentodetalle'

class Unidades(models.Model):
    unidad_id = models.IntegerField(primary_key=True)
    abreviatura = models.CharField(max_length=255, blank=True)
    descripcion_unidad = models.CharField(max_length=255, blank=True)
    predeterminado_vta = models.CharField(max_length=255, blank=True)
    predeterminado_com = models.CharField(max_length=255, blank=True)
    nro_productos = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'unidades'

class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    usuario = models.CharField(max_length=50, blank=True)
    clave = models.CharField(max_length=50, blank=True)
    categoria = models.CharField(max_length=50, blank=True)
    activo = models.NullBooleanField()
    nombre_completo = models.CharField(max_length=255, blank=True)
    codven = models.CharField(max_length=50, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    prefijo = models.CharField(max_length=50, blank=True)
    class Meta:
        managed = False
        db_table = 'usuario'

class Vehiculo(models.Model):
    id = models.IntegerField(primary_key=True)
    numero_serie = models.CharField(max_length=100, blank=True)
    marca = models.CharField(max_length=100, blank=True)
    placa = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=255, blank=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    fecha_ini = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'vehiculo'

class Vendedor(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    fecha_fin = models.DateTimeField(blank=True, null=True)
    fecha_ini = models.DateTimeField(blank=True, null=True)
    externo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'vendedor'

class Zona(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    fecha_ini = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'zona'

