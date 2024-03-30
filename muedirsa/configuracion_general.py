from muedirsa.apps.configuraciones.models import Empresa,Conexion
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

def datos_globales(request):
    empresa = Empresa.objects.all()
    row=None
    row1=None
    row2 = None

    if request.user.is_superuser:
        cursor = connection.cursor()
        cursor.execute(
            "select distinct m.cod_parent,m.nom_option,m.txt_url,m.num_order,m.id from menu m where  m.cod_parent IS NULL  order by num_order")
        row = cursor.fetchall()
        cursor = connection.cursor()
        cursor.execute(
            "select distinct m.cod_parent,m.nom_option,m.txt_url,m.num_order,m.id ,( select  count(s.id) from menu s where s.cod_parent=m.id ) as cont from menu m where m.cod_parent IS NOT NULL order by num_order")
        row1 = cursor.fetchall()

        cursor = connection.cursor()
        cursor.execute(
            "select distinct m.cod_parent,m.nom_option,m.txt_url,m.num_order,( select  count(s.id) from menu s where s.cod_parent=m.id ) as cont  from menu m where m.cod_parent IS NOT NULL order by num_order")
        row2 = cursor.fetchall()
    else:
        if request.user.id:
            cursor = connection.cursor()
            cursor.execute("select distinct m.cod_parent,m.nom_option,m.txt_url,m.num_order,m.id from menu_group mg,auth_user_groups aug,menu m where mg.menu_id=m.id and aug.group_id=mg.group_id and m.cod_parent IS NULL and aug.user_id="+str(request.user.id)+" order by num_order")
            row = cursor.fetchall()
            cursor = connection.cursor()
            cursor.execute("select distinct m.cod_parent,m.nom_option,m.txt_url,m.num_order,m.id,( select  count(s.id) from menu s where s.cod_parent=m.id ) as cont  from menu_group mg,auth_user_groups aug,menu m where mg.menu_id=m.id and aug.group_id=mg.group_id and m.cod_parent IS NOT NULL and aug.user_id="+str(request.user.id)+" order by num_order")
            row1 = cursor.fetchall()

            cursor = connection.cursor()
            cursor.execute(
                "select distinct m.cod_parent,m.nom_option,m.txt_url,m.num_order,( select  count(s.id) from menu s where s.cod_parent=m.id ) as cont  from menu_group mg,auth_user_groups aug,menu m where mg.menu_id=m.id and aug.group_id=mg.group_id and m.cod_parent IS NOT NULL and aug.user_id=" + str(
                    request.user.id) + " order by num_order")
            row2 = cursor.fetchall()

    dict = {
        'SITE_URL': 'http://ejemplo.com',
        'SITE_NAME': 'Mi Sitio de Ejemplo',
        'SITE_AUTHOR': 'Hector Costa',
        'EMPRESASDB': empresa,
        'menu': row,
        'submenu': row1,
        'submenu_sub': row2
    }
    return dict