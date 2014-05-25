from clientes.models import Cliente
from django.db import models
from restaurante.models import Restaurante, Plato

# Create your models here.
class Pedido(models.Model):
 	restaurante = models.ForeignKey(Restaurante)
 	plato = models.ManyToManyField(Plato, through='Detalle_pedido')
 	cliente = models.ForeignKey(Cliente)
 	class Meta:
 		verbose_name = u'Pedido'
 		verbose_name_plural = u'Pedidos'

class Detalle_pedido(models.Model):
	#relaciones foraneas de las tablas
	plato = models.ForeignKey(Plato)
	pedido = models.ForeignKey(Pedido)

	#Extra para el detalle
	cantidad = models.IntegerField()

	class Meta:
		verbose_name=u'Detalle pedido'
		verbose_name_plural = u'Detalle pedidos'


class Opinion(models.Model):
	puntuacion = models.IntegerField()
	valoracion = models.TextField()
	pedido = models.OneToOneField(Pedido)
	class Meta:
		verbose_name = 'Opinion'
		verbose_name_plural = 'Opiniones'