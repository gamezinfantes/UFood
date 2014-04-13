from django.shortcuts import render, render_to_response
from django.template import RequestContext
# Create your views here.
def home(request):
	return render_to_response('webapp/home.html', context_instance=RequestContext(request))

def carta(request):
	return render_to_response('webapp/carta.html', context_instance=RequestContext(request))

def restaurante(request):
	return render_to_response('webapp/restaurante.html', context_instance=RequestContext(request))

def busqueda(request):
	return render_to_response('webapp/busqueda.html', context_instance=RequestContext(request))
	
def login(request):
	return render_to_response('webapp/login.html', context_instance=RequestContext(request))