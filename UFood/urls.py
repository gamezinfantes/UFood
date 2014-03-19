from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'restaurante.views.home', name='home'),
    url(r'^carta/$', 'restaurante.views.carta', name='carta'),
    url(r'^restaurante/$', 'restaurante.views.restaurante'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
