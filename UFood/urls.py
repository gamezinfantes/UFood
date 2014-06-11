from django.conf.urls import patterns, include, url
from django.contrib import admin
from clientes.views import IngresarFormView, RegistrarCliente
from restaurante.views import Restaurantes_en_zona, RestauranteListView, HomeListView, CartaListView
from pedidos.views import OpinionCreateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^carrito/', 'pedidos.views.carrito', name='carrito'),

    url(r'^pago/exito/$', 'webapp.views.pago_exitoso', name='pago_exitoso'),
    #url(r'^registrar/$', 'webapp.views.registrar', name='registrar'),
    url(r'^opinar/(?P<id_pedido>\d+)/$', OpinionCreateView.as_view(), name='opinion'),
    
    url(r'^detalles-pedido/$', 'pedidos.views.detalles_pedido', name='detalles_pedido'),
   

    url(r'^$', HomeListView.as_view(), name='home'),
    url(r'^restaurantes/(?P<codigo_postal>\d{5})/$', Restaurantes_en_zona.as_view()),
    url(r'^restaurantes/(?P<codigo_postal>\d{5})/(?P<slug>[a-zA-Z0-9-]+)/$', Restaurantes_en_zona.as_view()),

    url(r'^restaurante/(?P<slug>[a-zA-Z0-9-]+)/$', RestauranteListView.as_view()),
    url(r'^restaurante/(?P<slug>[a-zA-Z0-9-]+)/carta/$', CartaListView.as_view()),


    url(r'^ingresar/$', IngresarFormView.as_view(), name='ingresar'),
    url(r'^registrar/$', RegistrarCliente.as_view(), name='registrar'),
    url(r'^salir/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name='salir'),


    # Paypal urls
    url(r'^paypal/create/$', 'pedidos.views.paypal_create', name="paypal_create"),
    url(r'^paypal/execute/$', 'pedidos.views.paypal_execute', name="paypal_execute"),
    
    url(r'^shoping-cart/add-single/$', 'pedidos.views.add_single', name='add_single'),
    url(r'^shoping-cart/remove-single/$', 'pedidos.views.remove_single', name='remove_single'),
    url(r'^pago/$', 'pedidos.views.pago', name='pago'),
)
