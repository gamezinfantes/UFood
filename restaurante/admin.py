from django.contrib import admin
from .models import Plato, Restaurante, Tipo_comida, Zona_reparto

admin.site.register(Plato)
admin.site.register(Restaurante)
admin.site.register(Tipo_comida)
admin.site.register(Zona_reparto)
