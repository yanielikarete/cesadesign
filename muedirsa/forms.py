from django import forms
from muedirsa.apps.configuraciones.models import Empresa,Conexion

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	empresa = forms.IntegerField(
    		widget=forms.Select(
       		 choices=Empresa.objects.all().values_list('empresa_id', 'nombre_empresa')
        	)
     )