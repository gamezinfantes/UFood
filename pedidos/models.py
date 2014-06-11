from clientes.models import Cliente
from django.db import models
#from restaurante.models import Restaurante, Plato

# Create your models here.
class Pedido(models.Model):
 	restaurante = models.ForeignKey('restaurante.Restaurante')
 	plato = models.ManyToManyField('restaurante.Plato', through='Detalle_pedido')
 	cliente = models.ForeignKey(Cliente)
 	def __unicode__(self):
 		return "Pedido %d" % self.id
 	class Meta:
 		verbose_name = u'Pedido'
 		verbose_name_plural = u'Pedidos'

class Detalle_pedido(models.Model):
	#relaciones foraneas de las tablas
	plato = models.ForeignKey('restaurante.Plato')
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
	def __unicode__(self):
 		return "Opinion pedido %d" % self.pedido.id
	class Meta:
		verbose_name = 'Opinion'
		verbose_name_plural = 'Opiniones'