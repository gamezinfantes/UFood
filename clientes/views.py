import urlparse

from django.conf import settings
from django.contrib.auth import (REDIRECT_FIELD_NAME, login, logout, authenticate)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
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
        suc = self.request.META.get('HTTP_REFERER', "")
        request.session['success_url'] = suc
        return super(IngresarFormView, self).get(request, *args, **kwargs)
         
