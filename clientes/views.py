import urlparse
from .forms import ClienteFormset, UserCreationFormExtend
from django.conf import settings
from django.contrib.auth import (REDIRECT_FIELD_NAME, login, logout, authenticate)
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic.edit import FormView

from django.contrib.auth.forms import AuthenticationForm



class IngresarFormView(FormView):
    form_class = AuthenticationForm
    #redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "clientes/ingresar.html"
    success_url = '/'
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
            
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
        else:        
            return self.form_invalid(form)
    
    def get_success_url(self):
        redirect_to = self.request.session.get('success_url', None)
        if redirect_to is not None:
            return redirect_to
        return success_url
      
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:                
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.success_url)
        suc = self.request.META.get('HTTP_REFERER', "")
        request.session['success_url'] = suc
        return super(IngresarFormView, self).get(request, *args, **kwargs)
         




class RegistrarCliente(CreateView):
    template_name = 'clientes/registrar-cliente.html'
    model = User
    form_class = UserCreationFormExtend
    success_url = '/'

    def get(self, request, *args, **kwargs):
        """
        Captura la peticion GET y instacia el formulario en blanco 
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        cliente_form = ClienteFormset()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  cliente_form=cliente_form))

    def post(self, request, *args, **kwargs):
        """
        Captura la peticion POST y procesa el formulario validando los datos
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        cliente_form = ClienteFormset(self.request.POST)
        if form.is_valid() and cliente_form.is_valid():
            return self.form_valid(form, cliente_form)
        else:
            return self.form_invalid(form, cliente_form)

    def form_valid(self, form, cliente_form):
        self.object = form.save()
        cliente_form.instance = self.object
        cliente_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, cliente_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  cliente_form=cliente_form))

