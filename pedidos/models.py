from django.db import models
from restaurante.models import Restaurante, Plato

# Create your models here.
class Forma_pago (models.Model):
	tipo = models.CharField(max_length=50)
	def __unicode__(self):
		return self.tipo
	class Meta:
		verbose_name=u'Forma de pago'
		verbose_name_plural=u'Formas de pago'

class Pedido(models.Model):
 	restaurante = models.ForeignKey(Restaurante)
 	plato = models.ManyToManyField(Plato)
 	forma_pago = models.ForeignKey(Forma_pago)
 	class Meta:
 		verbose_name = u'Pedido'
 		verbose_name_plural = u'Pedidos'

class Opinion(models.Model):
	puntuacion = models.IntegerField()
	valoracion = models.TextField()
	pedido = models.OneToOneField(Pedido)
	class Meta:
		verbose_name = 'Opinion'
		verbose_name_plural = 'Opiniones'