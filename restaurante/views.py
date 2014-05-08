from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView, DetailView
from .models import Restaurante, Zona_reparto, Tipo_comida


class Restaurantes_en_zona(ListView):
    template_name = "restaurante/busqueda.html"
    context_object_name = "restaurantes"
    def get_queryset(self):
    	zonas = Zona_reparto.objects.filter(codigo_postal=self.kwargs['codigo_postal'])
    	restaurantes = []
    	for zona in zonas:
    		restaurantes.append(zona.restaurante)
    	return restaurantes

class RestauranteListView(DetailView):
    context_object_name = "restaurante"
    template_name = "restaurante/restaurante.html"
    def get_object(self):
    	return get_object_or_404(Restaurante, slug=self.kwargs['slug'])

class HomeListView(ListView):
    model = Tipo_comida
    template_name = "restaurante/home.html"
    context_object_name = "tipos_comida"
    queryset = Tipo_comida.objects.all().order_by('comida')


