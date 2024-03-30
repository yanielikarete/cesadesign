

from django.db import models

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
    name = models.CharField(max_length=80)
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
    username = models.CharField(max_length=30)
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

class Conexion(models.Model):
    id_conexion = models.AutoField(primary_key=True)
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
    def __unicode__(self):
	 	return self.string_de_conexion

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
    session_key = models.CharField(max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class Empresa(models.Model):
    empresa_id = models.AutoField(primary_key=True)
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
    def __unicode__(self):
	 	return self.nombre_empresa

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

