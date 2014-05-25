from django.db import models
from django.contrib.auth.models import User

class Cliente (models.Model):
	# Referesncia al model de usuarios
	user = models.OneToOneField(User)
	# Atributos extra del cliente
	nombre = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=100)
	direccion = models.CharField(max_length=150)
	codigo_postal = models.CharField(max_length=5)
	telefono = models.CharField(max_length=15)

	def __unicode__(self):
		return self.user.username