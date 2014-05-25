from django.contrib import admin
from .models import Forma_pago, Plato, Restaurante, Tipo_comida, Seccion, Zona_reparto

class Tipo_comidaAdmin (admin.ModelAdmin):
	exclude = ('slug',)


admin.site.register(Forma_pago)
admin.site.register(Plato)
admin.site.register(Restaurante)
admin.site.register(Tipo_comida, Tipo_comidaAdmin)
admin.site.register(Zona_reparto)
admin.site.register(Seccion)
