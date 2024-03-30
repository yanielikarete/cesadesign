#Login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from django.template.context import RequestContext
from django.core.urlresolvers import reverse_lazy

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from .models import *
from muedirsa.apps.configuraciones.models import Empresa,Conexion
from inventario.models import Producto
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from config.models import *
from django.core import serializers

#from login.lib.tools import Tools

#=====================================================#
@login_required()
def homeEmpresa(request):
	e = Empresa.objects.all()
        return render(request, 'login/index.html', {'empresa':e})

#=====================================================#
@login_required()
def userPasswordChangeDone(request):
    docente = request.user
    docente.cambio_clave = True
    docente.save()

    return render(request, 'user/password_change_done.html')


#=====================================================#
# Login y Logout
#=====================================================#
def ingresar(request):
    demo = False

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('home-empresa'))

    if request.method == 'GET':
        if request.GET.get('demo'):
            demo = True

    if request.method == 'POST':
        form_user = AuthenticationForm(data = request.POST)

        if form_user.is_valid():
            user = request.POST['username']
            passw = request.POST['password']
            acceso = authenticate(username = user, password = passw)

            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect(request.GET.get('next',reverse_lazy('home-empresa')))
                else:
                    return render_to_response('user/no-activo.html', context_instance = RequestContext(request))
            else:
                return render_to_response('user/no-usuario.html', context_instance = RequestContext(request))

    else:
        form_user = AuthenticationForm()

    return render_to_response('user/login.html', context_instance = RequestContext(request, {'form': form_user, 'demo': demo}))

#=====================================================#
@login_required()
def salir(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('iniciar'))

@login_required()
@csrf_exempt
def getMessages(request):

    if request.method == 'POST':
        user=request.user
        user_groups = request.user.groups.all()

        messages = Notificaciones.objects.filter(Q(user=user) | Q( group__in = user_groups))
        return HttpResponse(serializers.serialize("json", messages))

    return HttpResponse(json.dumps({'return':'0'}), content_type='application/json')