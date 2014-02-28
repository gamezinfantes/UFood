from django.db import models

# Create your models here.
class Restaurante(models.Model):
	nombre = models.CharField(, max_length=50)
	direccion = models.CharField(, max_length=50)
	logo = models.ImageField()

    class Meta:
        verbose_name = _('Restaurante')
        verbose_name_plural = _('Restaurantes')

    def __unicode__(self):
        pass

