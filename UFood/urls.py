from django.conf.urls import patterns, include, url
from django.contrib import admin
from restaurante.views import Restaurantes_en_zona, RestauranteListView, HomeListView
from clientes.views import IngresarFormView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^carta/$', 'webapp.views.carta', name='carta'),
   

    url(r'^$', HomeListView.as_view(), name='home'),
    url(r'^restaurantes/(?P<codigo_postal>\d{5})/$', Restaurantes_en_zona.as_view()),
    url(r'^restaurante/(?P<slug>[a-zA-Z0-9-]+)/$', RestauranteListView.as_view()),
    url(r'^restaurante/(?P<slug>[a-zA-Z0-9-]+)/carta/$', RestauranteListView.as_view()),

    url(r'^ingresar/$', IngresarFormView.as_view(), name='ingresar'),
    url(r'^salir/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name='salir'),


    url(r'^admin/', include(admin.site.urls)),
)
