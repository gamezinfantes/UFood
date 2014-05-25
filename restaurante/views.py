from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.views.generic import ListView, DetailView
from .models import Plato, Restaurante, Tipo_comida, Zona_reparto
from carton.cart import Cart

class Restaurantes_en_zona(ListView):
    template_name = "restaurante/busqueda.html"
    context_object_name = "restaurantes"
    def get_queryset(self):
        if 'slug' in self.kwargs:
    	   zonas = Zona_reparto.objects.filter(codigo_postal=self.kwargs['codigo_postal'], restaurante__tipo_comida__slug=self.kwargs['slug'])
        else:
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


class CartaListView(ListView):
    template_name = "restaurante/carta.html"
    context_object_name = "platos"
    def get_queryset(self):
        return get_list_or_404(Plato, restaurante__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(CartaListView, self).get_context_data(**kwargs)
        context['cart'] = Cart(self.request.session)
        return context

