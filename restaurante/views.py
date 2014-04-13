from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView
from restaurante.models import Restaurante, Zona_reparto


class Restaurantes_en_zona(ListView):
    template_name = "restaurante/busqueda.html"
    context_object_name = "restaurantes"

    def get_queryset(self):
    	zonas = Zona_reparto.objects.filter(codigo_postal=self.args[0])
    	restaurantes = []
    	for zona in zonas:
    		restaurantes.append(zona.restaurante)
    	return restaurantes

class RestauranteListView(ListView):
    #model = Restaurante
    context_object_name = "restaurante"
    template_name = "restaurante/restaurante.html"
    def get_queryset(self):
    	return get_object_or_404(Restaurante, slug=self.args[0])




def home(request):
	return render_to_response('restaurante/home.html', context_instance=RequestContext(request))
