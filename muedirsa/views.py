from django.template import RequestContext
from django.shortcuts import render_to_response
from muedirsa.forms import LoginForm
from django.contrib.auth import authenticate, login
from muedirsa.models import Empresa

def login_page(request):
	message= None
	if request.method== "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username= request.POST['username']
			password= request.POST['password']
			empresa= request.POST['empresa']
			empresa = Empresa.objects.get(id=request.POST['empresa'])
			empresa=Empresa.objects
			if user is not None:
				if user.is_active:
					login(request, user)
					message="Logueo exitoso"+empresa
				else:
					message="Usuario inactivo"
			else:
				message="Nombre de usuario y/o password incorrecto"
	else:
	     form=LoginForm()
	return render_to_response('login.html',{'message': message, 'form': form}, 
				context_instance= RequestContext(request))