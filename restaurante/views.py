from django.shortcuts import render, render_to_response
from django.template import RequestContext
# Create your views here.
def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

def carta(request):
	return render_to_response('carta.html', context_instance=RequestContext(request))

def restaurante(request):
	return render_to_response('restaurante.html', context_instance=RequestContext(request))



