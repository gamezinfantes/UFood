from django.conf.urls import patterns, include, url
from django.contrib import admin
from restaurante.views import Restaurantes_en_zona, RestauranteListView

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'webapp.views.home', name='home'),
    url(r'^carta/$', 'webapp.views.carta', name='carta'),
    #url(r'^restaurante/$', 'webapp.views.restaurante'),
    #url(r'^busqueda/$', 'webapp.views.busqueda', name='busqueda'),
    url(r'^ingresar/$', 'webapp.views.login', name='login'),


    url(r'^$', 'restaurante.views.home', name='home'),
    url(r'^restaurantes/(\d{5})/$', Restaurantes_en_zona.as_view()),
    url(r'^restaurante/([-\w]+)/$', RestauranteListView.as_view()),
    url(r'^restaurante/([-\w]+)/carta/$', RestauranteListView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
)
