from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Tipo_comida(models.Model):
	comida = models.CharField(max_length=50)
	def __unicode__(self):
		return self.comida

	class Meta:
		verbose_name = u'Tipo de comida'
		verbose_name_plural = u'Tipos de comida'

class Restaurante(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=200)
	lat_cord = models.DecimalField(max_digits=9, decimal_places=7)
	lon_cord = models.DecimalField(max_digits=9, decimal_places=7)
	direccion = models.CharField(max_length=100)
	codigo_postal = models.PositiveIntegerField()
	telefono = models.CharField(max_length=12)
	tiempo_envio = models.SmallIntegerField()
	logo = models.ImageField(upload_to='logos')
	tipo_comida = models.ForeignKey(Tipo_comida)
	slug = models.SlugField(max_length=50, unique=True)
	def save(self, *args, **kwargs):
		self.slug = slugify(self.nombre)
		super(Restaurante, self).save(*args, **kwargs)
	def __unicode__(self):
		return self.nombre
	class Meta:
		verbose_name = u'Restaurante'
		verbose_name_plural = u'Restaurantes'

class Zona_reparto(models.Model):
	codigo_postal = models.SmallIntegerField()
 	restaurante = models.ForeignKey(Restaurante)
 	def __unicode__(self):
 		return "%s - %d" % (self.restaurante.nombre, self.codigo_postal)
 	class Meta:
 		verbose_name = u'Zona de reparto'
 		verbose_name_plural = u'Zonas de reparto'

class Plato(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=200)
	precio = models.DecimalField(max_digits=5, decimal_places=2)
	restaurante = models.ForeignKey(Restaurante)
	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = 'Plato'
		verbose_name_plural = 'Platos'








